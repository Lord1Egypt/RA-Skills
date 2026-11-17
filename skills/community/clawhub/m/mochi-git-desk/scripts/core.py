"""Shared source, copied into each standalone distribution. Python 3.10+."""
import contextlib, datetime as dt, hashlib, json, os, re, sqlite3, tempfile
from pathlib import Path

UTC=dt.timezone.utc
def stamp(): return dt.datetime.now(UTC).isoformat()
def digest(b): return hashlib.sha256(b).hexdigest()
def ident(s):
    if not isinstance(s,str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,99}',s): raise ValueError('Invalid identifier')
    return s
def local(root,p,exists=False):
    root=Path(root).resolve(); p=Path(p)
    if p.is_absolute(): raise ValueError('Use workspace-relative paths')
    candidate=root/p
    if any(x.is_symlink() for x in [candidate,*candidate.parents] if x!=root and root in x.parents): raise ValueError('Symbolic links rejected')
    p=candidate.resolve()
    if p==root or root not in p.parents: raise ValueError('Path escapes workspace')
    if exists and not p.is_file(): raise ValueError('Input file missing')
    return p
def atomic(p,b,private=True):
    p=Path(p); p.parent.mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(dir=p.parent,prefix='.'+p.name+'-')
    try:
        with os.fdopen(fd,'wb') as f: f.write(b); f.flush(); os.fsync(f.fileno())
        if private: os.chmod(tmp,0o600)
        os.replace(tmp,p)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)
def writejson(p,v): atomic(p,(json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode())
def readjson(p):
    p=Path(p)
    if p.stat().st_size>10*1024*1024: raise ValueError('JSON exceeds 10 MiB')
    return json.loads(p.read_text(encoding='utf-8-sig'))
def privateconfig(p):
    p=Path(p).expanduser().resolve()
    if not p.is_file(): raise ValueError('Private profile missing')
    if os.name!='nt' and p.stat().st_mode&0o077: raise ValueError('Set profile permissions to 600')
    return readjson(p)
def secret(c,key='passwordEnv'):
    name=c.get(key,''); value=os.environ.get(name,'')
    if not value: raise ValueError('Required credential environment variable is empty')
    return value
class Store:
    def __init__(self,root,name):
        self.root=Path(root).resolve(); self.root.mkdir(parents=True,exist_ok=True)
        self.home=self.root/'.mochilab'/ident(name); self.home.mkdir(parents=True,exist_ok=True)
        if os.name!='nt': os.chmod(self.root/'.mochilab',0o700); os.chmod(self.home,0o700)
        self.db=sqlite3.connect(self.home/'state.sqlite',timeout=20); self.db.row_factory=sqlite3.Row
        os.chmod(self.home/'state.sqlite',0o600)
        self.db.executescript('CREATE TABLE IF NOT EXISTS objects(kind TEXT,id TEXT,data TEXT,PRIMARY KEY(kind,id)); CREATE TABLE IF NOT EXISTS notices(id TEXT PRIMARY KEY,data TEXT,acked TEXT);')
        self.db.commit()
    def put(self,kind,id,data):
        self.db.execute('INSERT INTO objects VALUES(?,?,?) ON CONFLICT(kind,id) DO UPDATE SET data=excluded.data',(kind,id,json.dumps(data,ensure_ascii=False))); self.db.commit(); return data
    def get(self,kind,id,default=None):
        r=self.db.execute('SELECT data FROM objects WHERE kind=? AND id=?',(kind,id)).fetchone(); return json.loads(r[0]) if r else default
    def all(self,kind): return [json.loads(r[0]) for r in self.db.execute('SELECT data FROM objects WHERE kind=? ORDER BY id',(kind,))]
    def delete(self,kind,id):
        self.db.execute('DELETE FROM objects WHERE kind=? AND id=?',(kind,id)); self.db.commit()
    def notice(self,id,data):
        self.db.execute('INSERT OR IGNORE INTO notices VALUES(?,?,NULL)',(id,json.dumps(data,ensure_ascii=False))); self.db.commit()
    def pending(self): return [{'noticeId':r[0],**json.loads(r[1])} for r in self.db.execute('SELECT id,data FROM notices WHERE acked IS NULL ORDER BY rowid LIMIT 500')]
    def ack(self,ids):
        for id in ids: self.db.execute('UPDATE notices SET acked=? WHERE id=?',(stamp(),id))
        self.db.commit(); return {'pending':self.pending()}
def iso_date(s): return dt.date.fromisoformat(s)
def zoned(s):
    d=dt.datetime.fromisoformat(s.replace('Z','+00:00'))
    if d.tzinfo is None: raise ValueError('Timestamp must include UTC offset')
    return d
def bounded(v,lo,hi):
    if isinstance(v,bool) or isinstance(v,float) and not v.is_integer(): raise ValueError('Expected an integer')
    n=int(v)
    if not lo<=n<=hi: raise ValueError('Value outside allowed range')
    return n
def runmain(handler,name):
    import argparse,sys
    p=argparse.ArgumentParser(); p.add_argument('--workspace',required=True); p.add_argument('--input',required=True); a=p.parse_args()
    try:
        r=readjson(local(a.workspace,a.input,True)); result=handler(Store(a.workspace,name),r)
        print(json.dumps({'ok':True,'result':result},ensure_ascii=False))
    except Exception as e:
        # Protocol errors may contain credentials or private server responses.
        safe=isinstance(e,(ValueError,FileNotFoundError,KeyError,ImportError))
        print(json.dumps({'ok':False,'errorType':type(e).__name__,'error':str(e)[:300] if safe else 'Operation failed; check connection and provider settings privately'},ensure_ascii=False)); sys.exit(1)
