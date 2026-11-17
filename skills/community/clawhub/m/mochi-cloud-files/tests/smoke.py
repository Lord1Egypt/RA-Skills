import datetime as dt,io,json,os,subprocess,tempfile,unittest,zipfile,uuid,sys
from pathlib import Path
from unittest.mock import patch,MagicMock
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from core import *
import cloud_files as cloud

class Base(unittest.TestCase):
    def setUp(self):
        self.root=Path(os.environ.get('MOCHI_TEST_TEMP',tempfile.gettempdir()))/('case-'+uuid.uuid4().hex); self.root.mkdir(); self.st=Store(self.root,'test')
    def tearDown(self): self.st.db.close()
    def file(self,name,data):
        p=self.root/name; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(data if isinstance(data,bytes) else data.encode()); return p

class CloudTests(Base):
    def client(self): return MagicMock()
    def test_upload_conditional(self):
        self.file('a.txt','hello'); d=self.client(); d.request.return_value=(201,{'ETag':'"one"'},b''); d.base='https://example.test/files/'
        with patch.object(cloud,'DAV',return_value=d): out=cloud.handle(self.st,{'action':'upload','profile':'unused','file':'a.txt','remote':'a.txt'})
        self.assertEqual(d.request.call_args.args[3]['If-None-Match'],'*'); self.assertEqual(out['etag'],'"one"')
    def test_download_conflict(self):
        self.file('a.txt','old')
        with patch.object(cloud,'DAV'):
            with self.assertRaises(ValueError): cloud.handle(self.st,{'action':'download','profile':'unused','remote':'a.txt','file':'a.txt'})
    def test_download_hash(self):
        d=self.client(); d.base='https://example.test/'; d.request.return_value=(200,{'ETag':'"1"'},b'new')
        with patch.object(cloud,'DAV',return_value=d): out=cloud.handle(self.st,{'action':'download','profile':'unused','remote':'a.txt','file':'a.txt'})
        self.assertEqual(Path(out['file']).read_bytes(),b'new'); self.assertEqual(out['sha256'],digest(b'new'))
    def test_download_concurrent_local_edit(self):
        p=self.file('a.txt','old'); d=self.client(); d.base='https://example.test/'
        def incoming(*a,**k): p.write_text('edited'); return (200,{},b'new')
        d.request.side_effect=incoming
        with patch.object(cloud,'DAV',return_value=d):
            with self.assertRaises(ValueError): cloud.handle(self.st,{'action':'download','profile':'unused','remote':'a.txt','file':'a.txt','localSha256':digest(b'old')})
        self.assertEqual(p.read_text(),'edited')
    def test_delete_requires_etag(self):
        with patch.object(cloud,'DAV'):
            with self.assertRaises(ValueError): cloud.handle(self.st,{'action':'delete','profile':'unused','remote':'a.txt'})
    def test_dav_path_escape(self):
        from dav import DAV
        d=DAV.__new__(DAV); d.base='https://example.test/files/'
        for p in ('../secret','https://evil.test/a','/secret','%2e%2e/file','file?x=1'):
            with self.assertRaises(ValueError): d.url(p)
        self.assertEqual(d.url('中文.txt'),'https://example.test/files/%E4%B8%AD%E6%96%87.txt')

if __name__=="__main__": unittest.main(verbosity=2)
