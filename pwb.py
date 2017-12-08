# -*- coding: utf-8  -*-
# AUTHOR: Kizar (ngosang@hotmail.es)
# para purgar las páginas de la categoría
# python pwb.py touch -lang:en -family:wikivoyage -cat:"Banner missing from Wikidata"
# python pwb.py newitem -lang:en -family:wikivoyage -namespace:0 -pageage:0 -lastedit:0 -cat:"Banner missing from Wikidata"

import sys, re, time

import pwb  # only needed if you haven't installed the framework as side-package
import pywikibot
from pywikibot import pagegenerators

clean = re.compile('\\s*(.*\\S)?\\s*')

def tiene_regexp(articulo, regexp):
    old = re.compile(regexp, re.UNICODE | re.DOTALL) # Importante, sino no toma el . como cualquier caracter
    tmp_articulo = pywikibot.replaceExcept(articulo, old, r'88888888888888888888999998888888888888888888', [])
    if articulo != tmp_articulo: 
        return True
    else:
        return False

def remplaza_regexp(articulo, regexp, chang):
    old = re.compile(regexp, re.UNICODE | re.DOTALL) # Importante, sino no toma el . como cualquier caracter
    return pywikibot.replaceExcept(articulo, old, chang, [])

def busca_regexp(articulo, regexp):
    old = re.compile(regexp, re.UNICODE | re.DOTALL) # Importante, sino no toma el . como cualquier caracter
    return re.search(old, articulo)
    
def is_commons_img(img): #Devuelve verdadero si la imagen se encuentra en commons
    img_page = pywikibot.ImagePage(pywikibot.Site('commons', 'commons'), u'Image:'+img)
    if img_page.exists():
        return True
    else:
        return False

site = pywikibot.Site('en', 'wikivoyage')  # any site will work, this is just an example
repo = pywikibot.Site("wikidata", "wikidata").data_repository()  # this is a DataSite object

cat = pywikibot.Category(site, 'Category:Banner missing from Wikidata')
gen = pagegenerators.CategorizedPageGenerator(cat)
for pagina in gen:
    if pagina.isRedirectPage() or pagina.isDisambig():
        continue
    pywikibot.output(pagina.title())
    
    try:
        item = pywikibot.ItemPage.fromPage(pagina)  # this can be used for any page object
    except:
        print("!!! No existe en Wikidata")
        continue
    item.get()  # you need to call it to access any data.
    
    if not 'P948' in item.claims:
        content = pagina.text

        if tiene_regexp(content, r'\{\{\s*[Pp]agebanner\s*\|\s*([^|}]+)\s*[|}]' ) == True: # Si tiene imagen perfect
            # Comprobamos si la imagen está en commons
            imagen = busca_regexp(content, r'\{\{\s*[Pp]agebanner\s*\|\s*([^|}]+)\s*[|}]' ).group(1)
            imagen = clean.match(imagen).group(1) # Limpiar todo lo raro
            pywikibot.output(imagen)
            if imagen != 'Pagebanner default.jpg' and imagen != 'Disambiguation banner.png' and imagen != 'TT Banner.jpg' and imagen != 'Mena-asia_default_banner.jpg':
                #if is_commons_img(imagen):
                img_page = pywikibot.ImagePage(pywikibot.Site('commons', 'commons'), u'Image:'+imagen)
                if img_page.exists():
                    claim = pywikibot.Claim(repo, 'P948')
                    claim.setTarget(img_page)
                    item.addClaim(claim)
                else:
                    print("!!! No existe en Commons")
 
    # para purgar utilizar los comandos de arriba
    pagina.save() # purge cache
    time.sleep(2)
