#!/usr/bin/env python3
"""First-party standalone installer; Python 3.9+, standard library only."""
import argparse, contextlib, hashlib, json, os, shutil, stat, sys, tempfile, time, urllib.request, zipfile
from pathlib import Path
ID='openlx-weixin-baimindan'
OFFICIAL='https://wx.openlx.cn/api/skills/'+ID+'/manifest'
GITHUB='https://github.com/openlxcn/'+ID+'/releases/download/'
ROOT=Path.home()/'.openlx'/'skills'/ID
HOSTS={'codex':('.codex','codex'),'claude':('.claude','claude'),'cursor':('.cursor','cursor')}
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def write(p,v):
 p.parent.mkdir(parents=True,exist_ok=True); os.chmod(p.parent,0o700)
 q=p.with_suffix('.tmp'); q.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8'); os.chmod(q,0o600); q.replace(p)
def digest(b): return hashlib.sha256(b).hexdigest()
def hashes(p):
 if any(x.is_symlink() for x in p.rglob('*')): raise ValueError('SYMLINK_NOT_ALLOWED')
 return {str(x.relative_to(p)).replace('\\','/'):digest(x.read_bytes()) for x in sorted(p.rglob('*')) if x.is_file() and '__pycache__' not in x.parts}
def fetch(url,timeout=15):
 if not url.startswith('https://'): raise ValueError('HTTPS_REQUIRED')
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':ID+'/0.1.1'}),timeout=timeout) as r:
  if not r.url.startswith('https://'): raise ValueError('HTTPS_REQUIRED')
  return r.read(30*1024*1024+1)
def manifest(a):
 if a.manifest_file: return read(Path(a.manifest_file))
 url=GITHUB+'v'+a.version+'/release-manifest.json' if a.source=='github' and a.version else OFFICIAL
 m=json.loads(fetch(url,4 if a.command=='check-update' else 15))
 if m.get('skill_id')!=ID: raise ValueError('MANIFEST_ID_MISMATCH')
 return m
def select(a):
 if a.agent!='auto': return a.agent
 found=[k for k,(d,c) in HOSTS.items() if (Path.home()/d).is_dir() or shutil.which(c)]
 if len(found)!=1: raise ValueError('AGENT_SELECTION_REQUIRED: '+', '.join(found or HOSTS))
 return found[0]
def location(agent): return Path.home()/HOSTS[agent][0]/'skills'/ID
def confirm(a,message,flag='yes'):
 if getattr(a,flag): return True
 return sys.stdin.isatty() and input(message+' [y/N] ').lower()=='y'
def backup(dest,base,state):
 folder=base/'backups'/str(time.time_ns()); folder.mkdir(parents=True)
 shutil.copytree(dest,folder/'skill'); write(folder/'state.json',state)
 return str(folder)
def install(a,agent,base,state,dest):
 m=manifest(a); v=a.version or m['latest']['beta']
 if not v or not v.startswith('0.'): raise ValueError('BETA_VERSION_REQUIRED')
 entry=m['versions'][v]; f=entry['files'][0]
 if m['skill_id']!=ID or not entry['pre_release']: raise ValueError('MANIFEST_INVALID')
 b=Path(a.package_file).read_bytes() if a.package_file else fetch(f['github_url'] if a.source=='github' else f['official_mirror_url'])
 if len(b)!=f['size'] or digest(b)!=f['sha256']: raise ValueError('PACKAGE_HASH_MISMATCH')
 dest.parent.mkdir(parents=True,exist_ok=True)
 if dest.is_symlink(): raise ValueError('SYMLINK_NOT_ALLOWED')
 with tempfile.TemporaryDirectory(prefix='.openlx-',dir=dest.parent) as temp:
  stage=Path(temp)/'skill'; stage.mkdir()
  import io
  with zipfile.ZipFile(io.BytesIO(b)) as z:
   seen=set(); total=0
   for zi in z.infolist():
    name=zi.filename; parts=name.split('/'); mode=zi.external_attr>>16
    total+=zi.file_size
    if name in seen or total>60*1024*1024 or name.startswith('/') or '\\' in name or '..' in parts or stat.S_ISLNK(mode): raise ValueError('UNSAFE_ARCHIVE')
    seen.add(name)
    prefix=ID+'/skills/'+ID+'/'
    if not name.startswith(prefix) or zi.is_dir(): continue
    rel=name[len(prefix):]
    if not rel or ':' in rel: raise ValueError('UNSAFE_ARCHIVE')
    out=stage/rel; out.parent.mkdir(parents=True,exist_ok=True); out.write_bytes(z.read(zi)); os.chmod(out,0o755 if out.suffix in ('.sh','.py') else 0o644)
  if not (stage/'SKILL.md').is_file() or (stage/'VERSION').read_text(encoding='utf-8').strip()!=v: raise ValueError('PACKAGE_LAYOUT_INVALID')
  prior=[]
  if dest.exists():
   modified=hashes(dest)!=state.get('files',{})
   snap=backup(dest,base,state); prior=state.get('backups',[])+[snap]
   if modified and not confirm(a,'Local edits backed up. Replace?', 'confirm_local_changes'):
    print('LOCAL_MODIFICATIONS_PROTECTED: '+snap); return
   if not confirm(a,'Install version '+v+'?'):
    print('UPDATE_DECLINED'); return
  tomb=Path(temp)/'previous'
  if dest.exists(): dest.rename(tomb)
  try:
   stage.rename(dest)
   write(base/'state.json',{'skill_id':ID,'agent':agent,'installed_version':v,'release_channel':'beta','installed_from':a.source,'package_sha256':f['sha256'],'last_checked_at':None,'latest_seen_version':v,'local_modified':False,'files':hashes(dest),'backups':prior})
  except BaseException:
   if dest.exists(): shutil.rmtree(dest)
   if tomb.exists(): tomb.rename(dest)
   raise
 print('INSTALLED '+v); doctor(dest,read(base/'state.json')); print('https://wx.openlx.cn/account?authorize=1')
def doctor(dest,state):
 if not dest.exists(): raise ValueError('NOT_INSTALLED')
 changed=hashes(dest)!=state.get('files',{})
 print(json.dumps({'status':'LOCAL_MODIFIED' if changed else 'PASS','version':state.get('installed_version'),'local_modified':changed,'credentials_stored':False}))
 return changed
def run(a):
 agent=select(a); base=ROOT/agent; dest=location(agent); sp=base/'state.json'; state=read(sp) if sp.exists() else {}
 if a.command=='check-update':
  now=time.time()
  if not a.force and now-(state.get('last_checked_at') or 0)<7*86400: print('CHECK_NOT_DUE'); return
  state['last_checked_at']=now; write(sp,state)
  m=manifest(a); v=m['latest']['beta']; state['latest_seen_version']=v; write(sp,state)
  current=state.get('installed_version','0.0.0'); newer=tuple(map(int,v.split('.')))>tuple(map(int,current.split('.')))
  print(json.dumps({'current':current,'latest':v,'update_available':newer,'auto_update':False,'summary':m['versions'][v].get('summary',''),'sources':['official','github']})); return
 if a.command=='doctor': doctor(dest,state); return
 base.mkdir(parents=True,exist_ok=True)
 lock=base/'mutation.lock'
 try: fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600); os.close(fd)
 except FileExistsError: raise ValueError('INSTALLATION_BUSY: inspect mutation.lock before recovery')
 try:
  if a.command in ('install','update'): install(a,agent,base,state,dest)
  elif a.command=='rollback':
   backups=state.get('backups',[])
   if not backups: raise ValueError('NO_BACKUP')
   target=Path(backups[-1]); old=read(target/'state.json')
   if not (target/'skill'/'SKILL.md').is_file(): raise ValueError('INVALID_BACKUP')
   snap=backup(dest,base,state)
   if not confirm(a,'Restore previous backup?'): print('ROLLBACK_DECLINED'); return
   if hashes(dest)!=state.get('files',{}) and not confirm(a,'Current edits backed up. Replace?', 'confirm_local_changes'): print('LOCAL_MODIFICATIONS_PROTECTED'); return
   with tempfile.TemporaryDirectory(prefix='.rollback-',dir=dest.parent) as temp:
    stage=Path(temp)/'restored'; shutil.copytree(target/'skill',stage); tomb=Path(temp)/'previous'; dest.rename(tomb)
    try:
     stage.rename(dest); old['local_modified']=hashes(dest)!=old.get('files',{}); old['backups']=backups[:-1]; write(sp,old)
    except BaseException:
     if dest.exists(): shutil.rmtree(dest)
     tomb.rename(dest); raise
   print('ROLLED_BACK; recovery backup: '+snap)
  elif a.command=='uninstall':
   if dest.exists():
    snap=backup(dest,base,state)
    if not confirm(a,'Remove this skill (backup retained)?'): print('UNINSTALL_DECLINED'); return
    shutil.rmtree(dest); print('UNINSTALLED; backup: '+snap)
 finally: lock.unlink(missing_ok=True)
def main():
 p=argparse.ArgumentParser(); p.add_argument('command',choices=['install','update','check-update','rollback','doctor','uninstall']); p.add_argument('--agent',choices=['auto',*HOSTS],default='auto'); p.add_argument('--source',choices=['official','github'],default='official'); p.add_argument('--version'); p.add_argument('--yes',action='store_true'); p.add_argument('--confirm-local-changes',action='store_true'); p.add_argument('--force',action='store_true'); p.add_argument('--manifest-file'); p.add_argument('--package-file'); a=p.parse_args()
 try: run(a)
 except Exception as e:
  print(('UPDATE_CHECK_UNAVAILABLE_NONBLOCKING: ' if a.command=='check-update' else 'ERROR: ')+str(e),file=sys.stderr)
  return 0 if a.command=='check-update' else 1
 return 0
if __name__=='__main__': sys.exit(main())
