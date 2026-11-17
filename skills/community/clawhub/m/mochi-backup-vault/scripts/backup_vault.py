import fnmatch
from core import *
def manifest(s,key):
 m=s.get('snapshot',ident(key));require(m is not None,'Snapshot not found');return m
def blob(s,digest):
 require(bool(re.fullmatch('[a-f0-9]{64}',digest)),'Invalid digest');return local(s.root,'.mochilab/'+s.name+'/blobs/'+digest[:2]+'/'+digest)
def verify(s,m):
 bad=[]
 for item in m['files']:
  p=blob(s,item['sha256'])
  if not p.is_file() or p.stat().st_size!=item['bytes'] or sha(readbytes(p,64*1024*1024))!=item['sha256']:bad.append(item['path'])
 return {'snapshot':m['id'],'files':len(m['files']),'verified':not bad,'invalid':bad}
def handle(s,r):
 a=r.get('action')
 if a=='snapshot':
  key=ident(r['id']);require(s.get('snapshot',key) is None,'Snapshot ID already exists');source=r['directory'];base=local(s.root,source,'dir')
  require(s.home!=base and base not in s.home.parents,'Backup source cannot contain its own vault')
  patterns=r.get('exclude',['.git/*','node_modules/*','__pycache__/*']);require(isinstance(patterns,list) and all(isinstance(x,str) for x in patterns),'Invalid exclusion rules')
  rows=[];new_count=0;total=0
  selected=[]
  def excluded(name):return any(fnmatch.fnmatch(name,pattern) for pattern in patterns)
  for folder,dirs,files in os.walk(base,followlinks=False):
   dirs[:]=sorted(d for d in dirs if not excluded((Path(folder)/d).relative_to(base).as_posix()+'/'))
   for name in dirs:require(not linked(Path(folder)/name),'Source directory contains a link or junction')
   for name in sorted(files):
    p=Path(folder)/name
    if excluded(p.relative_to(base).as_posix()):continue
    require(not linked(p) and p.is_file(),'Selected backup file must not be a link');selected.append(p);require(len(selected)<=10000,'Too many selected files')
  for p in selected:
   name=p.relative_to(base).as_posix()
   if any(fnmatch.fnmatch(name,pattern) for pattern in patterns):continue
   raw=readbytes(p,64*1024*1024);total+=len(raw);require(total<=256*1024*1024,'Snapshot exceeds 256 MiB');digest=sha(raw);target=blob(s,digest)
   if target.exists():require(sha(readbytes(target,64*1024*1024))==digest,'Existing backup content is corrupt')
   else:write_new(target,raw);new_count+=1
   require(sha(readbytes(p,64*1024*1024))==digest,'Source changed during backup')
   rows.append({'path':name,'bytes':len(raw),'sha256':digest})
  require(rows,'No selected source files')
  # Recheck all source hashes after capture to detect cross-file changes.
  for item in rows:require(sha(readbytes(local(s.root,str(Path(source)/item['path']),'file'),64*1024*1024))==item['sha256'],'Source changed during snapshot')
  m={'id':key,'source':source,'createdAt':now(),'files':rows,'exclude':patterns,'totalBytes':total};s.put('snapshot',key,m)
  return {'snapshot':key,'files':len(rows),'bytes':total,'newContentBlobs':new_count,'verified':verify(s,m)['verified']}
 if a=='list':return [{k:m[k] for k in ('id','source','createdAt','totalBytes')}|{'fileCount':len(m['files'])} for m in s.all('snapshot')]
 if a=='verify':return verify(s,manifest(s,r['id']))
 if a=='compare':
  left=manifest(s,r['left']);right=manifest(s,r['right']);l={x['path']:x for x in left['files']};rr={x['path']:x for x in right['files']}
  return s.report({'left':left['id'],'right':right['id'],'added':sorted(rr.keys()-l.keys()),'removed':sorted(l.keys()-rr.keys()),'changed':sorted(k for k in l.keys()&rr.keys() if l[k]['sha256']!=rr[k]['sha256'])},'Backup comparison')
 if a=='restore':
  m=manifest(s,r['id']);require(verify(s,m)['verified'],'Backup integrity check failed');dest=local(s.root,r['destination']);require(not dest.exists(),'Restore destination must be new')
  require(not any(x in Path(r['destination']).parts for x in ('.mochilab',)),'Restore into a normal new workspace directory')
  dest.mkdir(parents=True)
  for item in m['files']:
   p=local(s.root,str(Path(r['destination'])/item['path']));write_new(p,readbytes(blob(s,item['sha256']),64*1024*1024));require(sha(readbytes(p,64*1024*1024))==item['sha256'],'Restored hash mismatch')
  return {'snapshot':m['id'],'destination':r['destination'],'restored':len(m['files']),'verified':True,'liveSourceModified':False}
 if a=='export':return s.report(manifest(s,r['id']),'Backup manifest')
 raise ValueError('Actions: snapshot, list, verify, compare, restore, export')
