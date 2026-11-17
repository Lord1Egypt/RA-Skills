import argparse,hashlib,json,os,re,shutil,sys,uuid,warnings,zipfile
from pathlib import Path

def require(condition,message):
 if not condition:raise ValueError(message)
def digest(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  while chunk:=f.read(1024*1024):h.update(chunk)
 return h.hexdigest()
def safe(workspace,value,exists=True):
 require(isinstance(value,str) and value and '\x00' not in value,'Provide a file path')
 require(re.match(r'^[A-Za-z][A-Za-z0-9+.-]*://',value) is None,'Use a local file, not a network URL')
 ws=Path(workspace).resolve(strict=True);raw=Path(value);raw=raw if raw.is_absolute() else ws/raw
 require('..' not in raw.parts,'Parent traversal is unsupported')
 absolute=Path(os.path.abspath(raw));require(absolute.is_relative_to(ws),'Path must be inside the active workspace')
 for p in [absolute,*absolute.parents]:
  if p==ws.parent:break
  require(not p.is_symlink() and not (hasattr(p,'is_junction') and p.is_junction()),'Linked paths are unsupported')
 resolved=absolute.resolve(strict=exists);require(resolved.is_relative_to(ws),'Path escaped workspace');return resolved
def read_file(ws,value,max_bytes):
 p=safe(ws,value);require(p.is_file() and 0<p.stat().st_size<=max_bytes,'Input file is empty or exceeds the size limit');return p
def json_text(data):return json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False)+'\n'
def write_json(p,data):Path(p).write_text(json_text(data),encoding='utf8')
def receipt_files(ws,out):
 return [{'path':p.relative_to(ws).as_posix(),'bytes':p.stat().st_size,'sha256':digest(p)} for p in sorted(out.rglob('*')) if p.is_file()]
def transaction(ws,slug,job,worker):
 ws=Path(ws).resolve(strict=True);require(ws.is_dir(),'Workspace must exist');rid=job.get('requestId','');require(re.fullmatch(r'[A-Za-z0-9_-]{1,80}',rid or '') is not None,'requestId: 1..80 letters, numbers, hyphen or underscore')
 home=safe(ws,'.mochilab/'+slug,False);home.mkdir(parents=True,exist_ok=True);safe(ws,str(home));lock=home/'write.lock'
 fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
 out=None;committed=False
 try:
  fingerprint=hashlib.sha256(json_text(job).encode()).hexdigest();record=home/(rid+'.json')
  if record.exists():
   saved=json.loads(record.read_text(encoding='utf8'));require(saved['inputHash']==fingerprint,'requestId was used with different input')
   for item in saved['result']['files']:
    p=safe(ws,item['path']);require(p.stat().st_size==item['bytes'] and digest(p)==item['sha256'],'Saved output changed or is missing')
   for item in saved['result'].get('sources',[]):require(digest(safe(ws,item['path']))==item['sha256'],'Source changed; use a new requestId')
   return {**saved['result'],'replayed':True}
  out=safe(ws,'.mochilab/'+slug+'/exports/'+str(uuid.uuid4()),False);out.mkdir(parents=True);safe(ws,str(out))
  result=worker(ws,job,out);sources=result.get('sources',[])
  for item in sources:require(digest(safe(ws,item['path']))==item['sha256'],'Source changed during processing')
  result={'ok':True,**result,'files':receipt_files(ws,out)};require(result['files'],'No output was produced')
  temp=home/('.pending-'+str(uuid.uuid4()));write_json(temp,{'inputHash':fingerprint,'result':result});os.replace(temp,record);committed=True;return result
 finally:
  os.close(fd);lock.unlink()
  if out is not None and not committed and out.exists():shutil.rmtree(out)
def source(ws,p):return {'path':p.relative_to(ws).as_posix(),'bytes':p.stat().st_size,'sha256':digest(p)}
def archive(out,name,paths):
 with zipfile.ZipFile(out/name,'w',zipfile.ZIP_DEFLATED) as z:
  for p in paths:z.write(p,p.relative_to(out))
def cli(slug,worker):
 try:
  parser=argparse.ArgumentParser();parser.add_argument('--workspace',required=True);parser.add_argument('--input',required=True);a=parser.parse_args()
  p=read_file(a.workspace,a.input,1024*1024);job=json.loads(p.read_text(encoding='utf-8-sig'));require(isinstance(job,dict),'Input must be a JSON object')
  print(json_text(transaction(a.workspace,slug,job,worker)))
 except Exception as e:
  print(json_text({'ok':False,'error':str(e)}),file=sys.stderr);raise SystemExit(1)
