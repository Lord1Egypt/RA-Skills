"""Local artifact runtime. No network, subprocess, credentials or shared state."""
import argparse,csv,datetime as dt,hashlib,io,json,math,os,re,sys,uuid,zipfile
from pathlib import Path,PurePosixPath

def need(condition,message):
 if not condition:raise ValueError(message)
def instant(value):
 v=dt.datetime.fromisoformat(value.replace('Z','+00:00'));need(v.tzinfo is not None,'ISO timestamps must include a timezone');return v
def decimal(value):
 from decimal import Decimal
 d=Decimal(str(value));need(d.is_finite(),'Number must be finite');return d
def table(text):return list(csv.DictReader(io.StringIO(text)))
def safezip(blob):
 need(len(blob)<=25*1024*1024,'Archive exceeds25MiB');z=zipfile.ZipFile(io.BytesIO(blob));items=z.infolist();need(len(items)<=5000 and sum(x.file_size for x in items)<=100*1024*1024,'Archive expansion limit');need(len({x.filename for x in items})==len(items),'Duplicate archive entries')
 for item in items:
  p=PurePosixPath(item.filename);need(not p.is_absolute() and '..' not in p.parts and '\\' not in item.filename and not re.match(r'^[A-Za-z]:',item.filename),'Unsafe archive path');need((item.external_attr>>16)&0o170000!=0o120000,'Archive symlink refused')
 return z

class Store:
 def __init__(self,root):
  self.root=Path(root).absolute();need(self.root.is_dir() and not self.link(self.root),'Workspace must be an existing ordinary directory');self.out=None;self.artifacts=[]
 @staticmethod
 def link(p):return p.is_symlink() or (getattr(p,'is_junction',lambda:False)())
 def path(self,name):
  p=Path(name);need(not p.is_absolute() and '..' not in p.parts,'Use workspace-relative paths without parent traversal');cur=self.root
  for part in p.parts:
   cur=cur/part;need(not self.link(cur),'Linked path refused')
  need(cur.resolve().is_relative_to(self.root.resolve()),'Path outside workspace')
  if cur.is_file():need(cur.stat().st_nlink==1 and cur.stat().st_size<=25*1024*1024,'Input size or hardlink refused')
  return cur
 def read(self,name):return self.path(name).read_text(encoding='utf-8-sig')
 def data(self,name):
  def invalid_constant(value):raise ValueError('Non-finite numeric constants are not JSON')
  return json.loads(self.read(name),parse_constant=invalid_constant)
 def bytes(self,name):return self.path(name).read_bytes()
 def emit(self,name,content):
  need(bool(re.fullmatch(r'[A-Za-z0-9_.-]{1,120}',name)),'Output name must be a simple file name')
  if self.out is None:
   base=self.path('exports');base.mkdir(mode=0o700,exist_ok=True);self.out=base/('mochi-'+uuid.uuid4().hex);self.out.mkdir(mode=0o700)
  dest=self.out/name
  with dest.open('xb') as f:f.write(content.encode('utf-8') if isinstance(content,str) else content)
  self.artifacts.append({'path':dest.relative_to(self.root).as_posix(),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'bytes':dest.stat().st_size})
  return self.artifacts[-1]['path']

def run(handler):
 parser=argparse.ArgumentParser();parser.add_argument('--workspace',required=True);parser.add_argument('--input',required=True);args=parser.parse_args()
 try:
  ctx=Store(args.workspace);request=ctx.data(args.input);need(isinstance(request,dict),'Request must be a JSON object');result=handler(request,ctx);need(isinstance(result,dict),'Handler result must be an object')
  report=ctx.emit('report.json',json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'ok':True,'result':result,'report':report,'artifacts':ctx.artifacts},ensure_ascii=True));return 0
 except (ValueError,TypeError,KeyError,OSError,ArithmeticError,RecursionError,zipfile.BadZipFile) as e:
  print(json.dumps({'ok':False,'error':type(e).__name__,'message':str(e)[:250]},ensure_ascii=True));return 2
