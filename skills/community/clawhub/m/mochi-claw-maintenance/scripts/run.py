"""Explicit-instance inventory, verified snapshots and restore rehearsals."""
import argparse,hashlib,json,os,re,shutil,sqlite3,stat,subprocess,sys,uuid,zipfile
from pathlib import Path,PurePosixPath
from io_utils import require,safe,read_file,source,write_json,digest,json_text,transaction
MAX=512*1024*1024
SECRET=re.compile(r'key|token|secret|password|authorization|cookie',re.I)

def redact(v):
 if isinstance(v,dict):return {k:'[redacted]' if SECRET.search(k) else redact(x) for k,x in v.items()}
 if isinstance(v,list):return [redact(x) for x in v]
 if isinstance(v,str):return re.sub(r'\b(?:sk-|mls_|mlk_)[A-Za-z0-9_\-]{8,}', '[redacted]',v)
 return v

def root_path(value):
 p=Path(value).absolute();require(p.is_dir() and p!=Path(p.anchor),'Choose the exact OpenClaw state directory, not a drive root')
 for q in [p,*p.parents]:require(not q.is_symlink() and not(getattr(q,'is_junction',lambda:False)()),'Linked instance roots are unsupported')
 require((p/'openclaw.json').is_file(),'instanceRoot must contain openclaw.json');return p.resolve()

def inventory(root):
 raw=(root/'openclaw.json').read_text(encoding='utf-8-sig');require(len(raw)<=2*1024*1024,'Config too large')
 try:config=json.loads(raw)
 except ValueError:raise ValueError('Config uses JSON5; normalize a copy to strict JSON before this helper. Do not rewrite the live file.')
 require(isinstance(config,dict),'Config must be an object');agent_settings=config.get('agents',{});agents=agent_settings.get('entries',agent_settings.get('list',[]))
 if isinstance(agents,dict):agents=[{**v,'id':k} for k,v in agents.items()]
 require(isinstance(agents,list),'Unsupported agent roster');bindings=config.get('bindings',[]);warnings=[];routes={};ids=set()
 for a in agents:
  require(isinstance(a,dict) and isinstance(a.get('id'),str),'Invalid agent declaration')
  if a['id'] in ids:warnings.append('Duplicate agent ID: '+a['id'])
  ids.add(a['id'])
 for b in bindings:
  m=b.get('match',{});key=json.dumps(m,sort_keys=True);agent=b.get('agentId')
  if key in routes and routes[key]!=agent:warnings.append('Same binding match routes to multiple agents')
  routes[key]=agent
  if agent not in ids and agent!='main':warnings.append('Binding references an undeclared agent: '+str(agent))
 return config,{'agents':[{'id':a.get('id'),'workspace':a.get('workspace'),'model':redact(a.get('model'))} for a in agents],'bindings':redact(bindings),'warnings':warnings,'configSha256':digest(root/'openclaw.json'),'configurationOnly':True}

def selected(root,job):
 names=job.get('include')
 if names is None:names=['openclaw.json']+[p.name for p in root.iterdir() if p.is_dir() and (p.name in ['agents','credentials','identity'] or p.name=='workspace' or p.name.startswith('workspace-'))]
 require(isinstance(names,list) and 1<=len(names)<=50,'include: 1..50 paths relative to the selected instance')
 files={};size=0
 for name in names:
  p=safe(root,name);require(p!=root,'Select specific config/state/workspace entries')
  entries=sorted(p.rglob('*')) if p.is_dir() else [p]
  for f in entries:
   require(not f.is_symlink() and not getattr(f,'is_junction',lambda:False)(),'Backup entries cannot be links');safe(root,str(f))
   if not f.is_file():continue
   rel=f.relative_to(root).as_posix()
   # Derived/cache/volatile files are not silently copied as application state.
   if any(x in ['node_modules','__pycache__','.git'] for x in f.relative_to(root).parts) or f.name.endswith(('-wal','-shm','write.lock')):continue
   size+=f.stat().st_size;require(size<=MAX and len(files)<20000,'Snapshot limit: 512 MiB / 20000 files');files[rel]=f
 require('openclaw.json' in files,'Backup must include openclaw.json');return files

def inspect_archive(p):
 require(p.stat().st_size<=MAX,'Backup archive exceeds 512 MiB')
 with zipfile.ZipFile(p) as z:
  entries=z.infolist();require(len(entries)<=20001 and sum(i.file_size for i in entries)<=MAX,'Expanded backup exceeds limits');seen=set()
  for i in entries:
   name=i.filename;path=PurePosixPath(name);require(not path.is_absolute() and '..' not in path.parts and '\\' not in name and ':' not in name and name.casefold() not in seen and not name.endswith('/'),'Invalid or duplicate ZIP entry');seen.add(name.casefold())
   require(not stat.S_ISLNK(i.external_attr>>16),'ZIP links are unsupported')
  exact_names={i.filename for i in entries};require('backup-manifest.json' in exact_names,'Missing backup manifest');raw=z.read('backup-manifest.json');require(len(raw)<=5*1024*1024,'Manifest too large');manifest=json.loads(raw)
  require(manifest.get('format')=='mochi-claw-snapshot-v1','Unsupported snapshot format');rows=manifest.get('files',[]);require(isinstance(rows,list),'Invalid manifest')
  names=[r['path'] for r in rows];require(len(set(names))==len(names) and set(names)|{'backup-manifest.json'}==exact_names,'Archive contents do not match manifest')
  for r in rows:
   info=z.getinfo(r['path']);require(info.file_size==r['bytes'],'Backup size mismatch');require(hashlib.sha256(z.read(info)).hexdigest()==r['sha256'],'Backup SHA256 mismatch')
  require('openclaw.json' in names,'Snapshot has no config');config=json.loads(z.read('openclaw.json').decode('utf-8-sig'));require(isinstance(config,dict),'Snapshot config invalid')
 return manifest

def worker(root):
 def process(ws,j,out):
  action=j.get('action','inspect');require(action in ['inspect','backup','verify','rehearse','compare','cli-status'],'Unknown action')
  config,inv=inventory(root)
  if action=='cli-status':
   binary=shutil.which('openclaw');require(binary,'OpenClaw CLI is not installed on this host')
   env={**os.environ,'OPENCLAW_STATE_DIR':str(root),'OPENCLAW_CONFIG_PATH':str(root/'openclaw.json')};rows=[]
   # Only read-only CLI commands. No model calls, repair, update, restart or sends.
   for args in [['--version'],['gateway','status','--json'],['agents','list','--json']]:
    try:
     result=subprocess.run([binary,*args],env=env,capture_output=True,text=True,encoding='utf8',errors='replace',timeout=45,shell=False)
     try:details=redact(json.loads(result.stdout)) if result.stdout.strip().startswith(('{','[')) else None
     except ValueError:details=None
     rows.append({'command':['openclaw',*args],'returncode':result.returncode,'json':details,'outputSuppressed':details is None})
    except subprocess.TimeoutExpired:rows.append({'command':['openclaw',*args],'timeout':True})
   write_json(out/'cli-status.json',rows);return {'action':action,'commands':rows,'liveMessagesSent':False}
  if action=='inspect':write_json(out/'inventory.json',inv);write_json(out/'config-redacted.json',redact(config));return {'action':action,**inv}
  if action=='backup':
   require(j.get('sensitiveBackupAccepted') is True,'Snapshot includes credentials: acknowledge sensitiveBackupAccepted and store it privately')
   paths=selected(root,j);rows=[];dest=out/'openclaw-snapshot.zip'
   require(not out.is_relative_to(root),'Backup output must be outside the selected instance directory; use a separate maintenance workspace')
   with zipfile.ZipFile(dest,'x',zipfile.ZIP_DEFLATED) as z:
    for rel,p in paths.items():
     before=digest(p)
     if p.suffix.lower() in ['.sqlite','.sqlite3','.db']:
      # SQLite online backup handles WAL/journal consistency; never copy a live db file raw.
      tmp=out/(uuid.uuid4().hex+'.sqlite');conn=sqlite3.connect(p.as_uri()+'?mode=ro',uri=True);target=sqlite3.connect(tmp)
      try:conn.backup(target);require(target.execute('PRAGMA integrity_check').fetchone()[0]=='ok','SQLite snapshot integrity failed')
      finally:target.close();conn.close()
      data=tmp.read_bytes();tmp.unlink();method='sqlite-online-backup'
     else:
      data=p.read_bytes();require(hashlib.sha256(data).hexdigest()==before,'File changed during backup; quiesce the instance and retry');method='stable-file-read'
     z.writestr(rel,data);rows.append({'path':rel,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'method':method,'sourceBefore':before})
    # Detect concurrent non-SQLite changes across the whole snapshot.
    for r in rows:
     if r['method']=='stable-file-read':require(digest(paths[r['path']])==r['sourceBefore'],'Instance changed during snapshot; quiesce and retry')
    manifest={'format':'mochi-claw-snapshot-v1','files':rows,'inventory':inv,'containsCredentials':True,'scope':'selected-instance','externalWorkspacesIncluded':False};z.writestr('backup-manifest.json',json_text(manifest))
   os.chmod(dest,0o600);inspect_archive(dest);write_json(out/'backup-receipt.json',{'file':dest.name,'sha256':digest(dest),'files':len(rows),'verified':True,'containsCredentials':True,'omittedExternalWorkspaces':[a['workspace'] for a in inv['agents'] if a.get('workspace') and not Path(os.path.expanduser(a['workspace'])).resolve().is_relative_to(root)]})
   return {'action':action,'verified':True,'count':len(rows),'containsCredentials':True,'snapshotConsistency':'stable files plus SQLite online backups; stop writes for an application-wide point-in-time snapshot'}
  p=read_file(ws,j.get('archive'),MAX);manifest=inspect_archive(p)
  if action=='verify':write_json(out/'verification.json',{'verified':True,'archiveSha256':digest(p),'count':len(manifest['files'])});return {'action':action,'verified':True,'count':len(manifest['files']),'sources':[source(ws,p)]}
  if action=='rehearse':
   target=out/'restored-instance';target.mkdir(mode=0o700 if os.name!='nt' else 0o777)
   with zipfile.ZipFile(p) as z:
    for r in manifest['files']:
     dest=safe(target,r['path'],False);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(z.read(r['path']));os.chmod(dest,0o600);require(digest(dest)==r['sha256'],'Restored hash mismatch')
   _,restored=inventory(target);write_json(out/'rehearsal.json',{'restoredFiles':len(manifest['files']),'inventory':restored,'liveInstanceModified':False,'gatewayStarted':False})
   return {'action':action,'restoredFiles':len(manifest['files']),'liveInstanceModified':False,'gatewayStarted':False,'sources':[source(ws,p)]}
  old={r['path']:r['sha256'] for r in manifest['files']};current=selected(root,j);changes=[]
  for rel in sorted(set(old)|set(current)):
   state='removed' if rel not in current else 'added' if rel not in old else 'changed' if digest(current[rel])!=old[rel] else 'unchanged'
   if state!='unchanged':changes.append({'path':rel,'state':state})
  write_json(out/'comparison.json',{'changes':changes,'sqliteComparison':'Byte comparison only; online snapshots can differ from a live DB without semantic data changes'})
  return {'action':action,'changes':changes,'sources':[source(ws,p)]}
 return process

def main():
 try:
  p=argparse.ArgumentParser();p.add_argument('--workspace',required=True);p.add_argument('--instance-root',required=True);p.add_argument('--input',required=True);args=p.parse_args();root=root_path(args.instance_root)
  ws=Path(args.workspace).resolve(strict=True);require(not ws.is_relative_to(root) and not root.is_relative_to(ws),'Use a separate maintenance workspace outside the instance root')
  job=json.loads(read_file(ws,args.input,1024*1024).read_text(encoding='utf-8-sig'));require(isinstance(job,dict),'Job must be an object');job={**job,'instanceRoot':str(root)}
  print(json_text(transaction(ws,'mochi-claw-maintenance',job,worker(root))))
 except Exception as e:print(json_text({'ok':False,'error':str(e)}),file=sys.stderr);raise SystemExit(1)

if __name__=='__main__':main()
