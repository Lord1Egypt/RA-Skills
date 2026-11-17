from helpers import *

def handle(s,r):
 action=r.get('action')
 if action=='save':
  key=ident(r['id']);sources=[]
  for name in strings(r.get('files',[]),100):
   p=local(s.root,name,'file');sources.append({'path':name,'sha256':sha(readbytes(p))})
  old=s.get('checkpoint',key);row={'id':key,'goal':text(r['goal']),'completed':strings(r.get('completed',[])),'next':strings(r.get('next',[])),'blocked':strings(r.get('blocked',[])),'constraints':strings(r.get('constraints',[])),'files':sources,'revision':1+(old or {}).get('revision',0),'savedAt':now()}
  if old:s.put('history',key+'-'+str(old['revision']),old)
  s.put('checkpoint',key,row);return row
 if action=='load':
  row=s.get('checkpoint',ident(r['id']));require(row is not None,'Checkpoint missing');checks=[]
  for f in row['files']:
   p=local(s.root,f['path']);checks.append({'path':f['path'],'unchanged':p.is_file() and sha(readbytes(p))==f['sha256']})
  md='# '+row['goal']+'\n\n'+'\n\n'.join('## '+k+'\n'+'\n'.join('- '+x for x in row[k]) for k in ['completed','next','blocked','constraints'])
  return file_report(s,{'checkpoint':row,'sourceChecks':checks,'revalidationRequired':any(not x['unchanged'] for x in checks)},'handoff.md',md.encode())
 if action=='list':return s.all('checkpoint')
 raise ValueError('Actions: save, load, list')
