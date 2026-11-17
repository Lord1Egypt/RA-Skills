from helpers import *
from collections import deque

def handle(s,r):
 action=r.get('action')
 if action=='entity':
  key=ident(r['id']);props=r.get('properties',{});require(isinstance(props,dict) and len(jsonbytes(props))<=20000,'Invalid properties')
  row={'id':key,'type':ident(r['type']),'name':text(r['name'],300),'properties':props,'source':text(r['source'],2000),'updatedAt':now()};s.put('entity',key,row);return row
 if action=='relate':
  a=ident(r['from']);b=ident(r['to']);kind=ident(r['relation']);require(s.get('entity',a) and s.get('entity',b),'Both entities must exist')
  row={'id':sha((a+'\0'+kind+'\0'+b).encode())[:32],'from':a,'to':b,'relation':kind,'source':text(r['source'],2000)};s.put('edge',row['id'],row);return row
 if action=='query':
  start=ident(r['id']);require(s.get('entity',start),'Entity not found');depth=limit(r.get('depth',1),0,4);edges=s.all('edge');seen={start};q=deque([(start,0)])
  while q:
   node,d=q.popleft()
   if d>=depth:continue
   for e in edges:
    other=e['to'] if e['from']==node else e['from'] if e['to']==node else None
    if other and other not in seen:seen.add(other);q.append((other,d+1))
   require(len(seen)<=1000,'Query exceeds node limit')
  return s.report({'entities':[s.get('entity',i) for i in sorted(seen)],'relations':[e for e in edges if e['from'] in seen and e['to'] in seen]})
 if action=='export':return s.report({'entities':s.all('entity'),'relations':s.all('edge')})
 raise ValueError('Actions: entity, relate, query, export')
