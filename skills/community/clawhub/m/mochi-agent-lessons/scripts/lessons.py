from helpers import *

def handle(s,r):
 action=r.get('action')
 if action=='record':
  key=ident(r['id']);require(s.get('lesson',key) is None,'Lesson already exists; use resolve')
  row={'id':key,'situation':text(r['situation']),'correction':text(r['correction']),'evidence':text(r['evidence']),'tags':strings(r.get('tags',[]),20),'status':'open','createdAt':now(),'history':[]}
  s.put('lesson',key,row);return row
 if action=='resolve':
  key=ident(r['id']);row=s.get('lesson',key);require(row is not None,'Unknown lesson')
  row['history'].append({'at':now(),'verification':text(r['verification'])});row['status']='verified';return s.put('lesson',key,row)
 if action=='review':
  query=text(r.get('query',''),300,True).casefold();rows=[x for x in s.all('lesson') if not query or query in json.dumps(x,ensure_ascii=False).casefold()]
  return s.report({'lessons':rows,'open':sum(x['status']=='open' for x in rows),'automaticPolicyChanges':False})
 raise ValueError('Actions: record, resolve, review')
