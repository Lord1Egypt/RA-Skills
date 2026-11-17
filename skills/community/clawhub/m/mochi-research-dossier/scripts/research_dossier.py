from helpers import *
from urllib.parse import parse_qsl,urlencode,urlunsplit

def canonical(u):
 p=urlsplit(public_url(u));query=[(k,v) for k,v in parse_qsl(p.query,keep_blank_values=True) if not k.lower().startswith('utm_') and k.lower() not in ('fbclid','gclid')]
 return urlunsplit((p.scheme,p.netloc.lower(),p.path or '/',urlencode(sorted(query)),''))

def handle(s,r):
 require(r.get('action')=='build','Action: build');d=readjson(local(s.root,r['file'],'file'));sources=objects(d,'sources',200);claims=objects(d,'claims',500);byid={};seen={};duplicates=[]
 for x in sources:
  key=ident(x['id']);require(key not in byid,'Duplicate source ID');u=canonical(x['url']);body=text(x['text'],100000);title=text(x['title'],500);date(x['accessedAt']);byid[key]={'id':key,'url':u,'title':title,'text':body,'accessedAt':x['accessedAt'],'sha256':sha(body.encode())}
  if u in seen:duplicates.append([seen[u],key])
  else:seen[u]=key
 results=[]
 for x in claims:
  key=ident(x['id']);claim=text(x['claim'],3000);supports=strings(x.get('sources',[]),20);require(all(k in byid for k in supports),'Claim references an unknown source');status=x.get('status','unverified');require(status in ('supported','disputed','unverified'),'Unknown claim status')
  require(status=='unverified' or supports,'Supported/disputed claims require sources');quote=x.get('quote');matched=None
  if quote is not None:
   quote=text(quote,4000);matched=any(quote in byid[k]['text'] for k in supports);require(matched,'Quote absent from cited source text')
  results.append({'id':key,'claim':claim,'sources':supports,'status':status,'quoteVerifiedInProvidedText':matched,'distinctDomains':len({urlsplit(byid[k]['url']).hostname for k in supports})})
 require(len({x['id'] for x in results})==len(results),'Duplicate claim ID')
 public=[{k:v for k,v in x.items() if k!='text'} for x in byid.values()]
 data={'sources':public,'claims':results,'duplicateSources':duplicates,'unverifiedClaims':sum(x['status']=='unverified' for x in results),'limitation':'Evidence links and supplied quotes checked locally; truth and source independence require researcher review.'}
 md='# Research dossier\n\n'+'\n\n'.join('## '+x['id']+' · '+x['status']+'\n'+x['claim']+'\nSources: '+', '.join('['+k+']('+byid[k]['url']+')' for k in x['sources']) for x in results)
 return file_report(s,data,'dossier.md',md.encode())
