import collections,csv,datetime as dt,email.parser,email.policy,html,io,itertools,json,re,statistics,textwrap,urllib.parse,xml.etree.ElementTree as ET
from runtime import need,instant,decimal,table,safezip

def handle(r,c):
 query=r['query'].strip();need(query,'Query is required');sites=r.get('sites',[]);need(all(re.fullmatch(r'[A-Za-z0-9.-]+',s) for s in sites),'Sites must be host names')
 terms=[query]+[query+' site:'+s for s in sites]
 if r.get('exact'):terms.append('"'+r['exact'].replace('"','')+'"')
 return {'queries':list(dict.fromkeys(terms)),'encodedQueries':[urllib.parse.quote_plus(q) for q in terms],'liveSearchPerformed':False}
