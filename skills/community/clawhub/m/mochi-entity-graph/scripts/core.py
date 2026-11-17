"""Standalone Python 3.10+ runtime copied into each Skill distribution."""
import argparse,csv,datetime as dt,hashlib,html,http.client,io,ipaddress,json,os,re,socket,sqlite3,ssl,stat,sys,uuid
from pathlib import Path
from urllib.parse import urlsplit,urljoin

def require(ok,message):
 if not ok:raise ValueError(message)
def ident(value):
 require(isinstance(value,str) and re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,95}',value),'Invalid identifier');return value
def limit(value,lo,hi):
 require(isinstance(value,int) and not isinstance(value,bool) and lo<=value<=hi,'Integer outside allowed range');return value
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(data):return hashlib.sha256(data).hexdigest()
def linked(p):
 try:s=os.lstat(p);return stat.S_ISLNK(s.st_mode) or bool(getattr(s,'st_file_attributes',0)&0x400)
 except FileNotFoundError:return False
def local(root,value,kind=None):
 require(isinstance(value,str) and value and '\x00' not in value,'Expected workspace-relative path')
 raw=Path(value);require(not raw.is_absolute() and not raw.drive and not re.match(r'^[A-Za-z]:|^\\',value) and '..' not in raw.parts,'Path must stay inside workspace')
 root=Path(root).resolve();p=root
 for part in raw.parts:
  p=p/part;require(not linked(p),'Links and junctions are not allowed')
 p=p.resolve();require(p!=root and root in p.parents,'Path escapes workspace')
 if kind=='file':require(p.is_file(),'Input file missing')
 if kind=='dir':require(p.is_dir(),'Input directory missing')
 return p
def readbytes(p,max_bytes=16*1024*1024):
 require(Path(p).stat().st_size<=max_bytes,'Input exceeds size limit');return Path(p).read_bytes()
def readjson(p):return json.loads(readbytes(p).decode('utf-8-sig'))
def jsonbytes(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def write_new(p,data):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f:f.write(data)
 if os.name!='nt':p.chmod(0o600)
 return p
def newjson(p,v):return write_new(p,jsonbytes(v))
def textfile(root,name,max_bytes=8*1024*1024):return readbytes(local(root,name,'file'),max_bytes).decode('utf-8-sig')
def walkfiles(root,relative,max_files=5000):
 base=local(root,relative,'dir');out=[]
 for d,dirs,files in os.walk(base,followlinks=False):
  for n in dirs+files:require(not linked(Path(d)/n),'Directory contains link or junction')
  dirs.sort()
  for n in sorted(files):
   p=Path(d)/n;require(p.is_file(),'Not an ordinary file');out.append(p);require(len(out)<=max_files,'Too many files')
 return out
def csv_rows(p):
 text=readbytes(p).decode('utf-8-sig');reader=csv.DictReader(io.StringIO(text));fields=reader.fieldnames
 require(fields and len(fields)==len(set(fields)) and all(fields),'CSV headers must be nonempty and unique')
 rows=[]
 for row in reader:
  require(None not in row and None not in row.values(),'CSV row width differs from header');rows.append(row);require(len(rows)<=100000,'Too many CSV rows')
 return fields,rows
def csvbytes(fields,rows):
 f=io.StringIO(newline='');w=csv.writer(f)
 def safe(x):
  x='' if x is None else str(x)
  return "'"+x if x.lstrip().startswith(('=','+','-','@','\t','\r')) else x
 w.writerow([safe(x) for x in fields])
 for row in rows:w.writerow([safe(row.get(k,'')) for k in fields])
 return ('\ufeff'+f.getvalue()).encode('utf-8')
def htmlreport(title,data):
 return ('<!doctype html><meta charset="utf-8"><title>'+html.escape(title)+'</title><style>body{font:16px/1.6 system-ui;max-width:1100px;margin:32px auto;padding:16px}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f5f6fa;padding:20px}</style><h1>'+html.escape(title)+'</h1><pre>'+html.escape(json.dumps(data,ensure_ascii=False,indent=2))+'</pre>').encode('utf-8')
def icalbytes(lines):
 folded=[]
 for line in lines:
  part=''
  for char in line:
   if len((part+char).encode('utf-8'))>75:folded.append(part);part=' '
   part+=char
  folded.append(part)
 return ('\r\n'.join(folded)+'\r\n').encode('utf-8')
class Store:
 def __init__(self,root,name):
  self.root=Path(root).resolve();require(self.root.is_dir(),'Workspace must exist');self.name=ident(name)
  self.home=local(self.root,'.mochilab/'+self.name);self.home.mkdir(parents=True,exist_ok=True)
  dbpath=local(self.root,'.mochilab/'+self.name+'/state.sqlite');self.db=sqlite3.connect(dbpath,timeout=20);self.db.execute('PRAGMA busy_timeout=20000');self.db.execute('CREATE TABLE IF NOT EXISTS objects(kind TEXT,id TEXT,data TEXT,PRIMARY KEY(kind,id))');self.db.commit()
  if os.name!='nt':self.home.chmod(0o700);(self.home/'state.sqlite').chmod(0o600)
 def get(self,kind,key,default=None):
  row=self.db.execute('SELECT data FROM objects WHERE kind=? AND id=?',(kind,key)).fetchone();return json.loads(row[0]) if row else default
 def all(self,kind):return [json.loads(r[0]) for r in self.db.execute('SELECT data FROM objects WHERE kind=? ORDER BY id',(kind,))]
 def put(self,kind,key,data):self.db.execute('INSERT INTO objects VALUES(?,?,?) ON CONFLICT(kind,id) DO UPDATE SET data=excluded.data',(kind,ident(key),json.dumps(data,ensure_ascii=False)));return data
 def delete(self,kind,key):self.db.execute('DELETE FROM objects WHERE kind=? AND id=?',(kind,key))
 def exports(self):
  p=local(self.root,'exports/'+self.name+'/'+uuid.uuid4().hex);p.mkdir(parents=True,exist_ok=False);return p
 def rel(self,p):return Path(p).relative_to(self.root).as_posix()
 def report(self,data,title=None,table=None):
  out=self.exports();newjson(out/'report.json',data);write_new(out/'report.html',htmlreport(title or self.name,data))
  if table:write_new(out/'report.csv',csvbytes(*table))
  return {'report':data,'directory':self.rel(out),'files':[self.rel(p) for p in sorted(out.iterdir())]}
def safe_request(url,method='GET',headers=None,body=None,private_hosts=(),max_bytes=1024*1024,timeout=12,redirects=0):
 require(isinstance(url,str) and len(url)<=4096,'URL exceeds supported length')
 require(method in ('GET','HEAD','POST','PUT','PATCH','DELETE','OPTIONS'),'Unsupported HTTP method')
 headers=dict(headers or {});headers.setdefault('User-Agent','MochiLab-Skill/1.0 (+https://mochilab.bz)')
 for _ in range(redirects+1):
  u=urlsplit(url);host=u.hostname;require(host and not u.username and not u.password and not u.fragment,'Invalid URL')
  require(u.scheme=='https' or u.scheme=='http' and host in private_hosts,'HTTPS required; local HTTP needs explicit host opt-in')
  port=u.port or (443 if u.scheme=='https' else 80);addresses=socket.getaddrinfo(host,port,type=socket.SOCK_STREAM)
  ips=[x[4][0] for x in addresses];require(ips,'Host has no address')
  require(host in private_hosts or all(ipaddress.ip_address(x).is_global for x in ips),'Private or reserved address rejected')
  addr=ips[0];ctx=ssl.create_default_context()
  class Pinned(http.client.HTTPSConnection if u.scheme=='https' else http.client.HTTPConnection):
   def connect(self):
    self.sock=socket.create_connection((addr,port),timeout)
    if u.scheme=='https':self.sock=ctx.wrap_socket(self.sock,server_hostname=host)
  connection=Pinned(host,port=port,timeout=timeout)
  try:
   connection.request(method,(u.path or '/')+('?' +u.query if u.query else ''),body=body,headers=headers)
   response=connection.getresponse();raw=response.read(max_bytes+1);require(len(raw)<=max_bytes,'HTTP response too large')
   result={'url':url,'status':response.status,'headers':{k.lower():v for k,v in response.getheaders()},'body':raw}
  finally:connection.close()
  if result['status'] not in (301,302,303,307,308) or not result['headers'].get('location') or not redirects:return result
  require(method in ('GET','HEAD'),'Redirect for mutation refused')
  new=urljoin(url,result['headers']['location']);newparts=urlsplit(new)
  if (newparts.scheme,newparts.netloc)!=(u.scheme,u.netloc):headers={k:v for k,v in headers.items() if k.lower() in ('user-agent','accept')}
  url=new
 raise ValueError('Too many redirects')
def runmain(handle,name):
 p=argparse.ArgumentParser();p.add_argument('--workspace',required=True);p.add_argument('--input',required=True);a=p.parse_args();s=None
 try:
  request=readjson(local(a.workspace,a.input,'file'));require(isinstance(request,dict),'Request must be a JSON object');s=Store(a.workspace,name)
  with s.db:result=handle(s,request)
  print(json.dumps({'ok':True,'result':result},ensure_ascii=False))
 except Exception as e:
  # Raw network/database errors can contain secrets or source content. Expose only controlled validation errors.
  message=str(e)[:260] if isinstance(e,ValueError) and not isinstance(e,(json.JSONDecodeError,UnicodeError)) else 'Operation failed; check the selected input and connection settings'
  print(json.dumps({'ok':False,'errorType':type(e).__name__,'error':message},ensure_ascii=False));return 1
 finally:
  if s:s.db.close()
 return 0
