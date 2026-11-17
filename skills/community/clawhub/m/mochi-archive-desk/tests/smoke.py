import datetime as dt,io,json,os,subprocess,tempfile,unittest,zipfile,uuid,sys
from pathlib import Path
from unittest.mock import patch,MagicMock
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from core import *
import archive_desk as archive

class Base(unittest.TestCase):
    def setUp(self):
        self.root=Path(os.environ.get('MOCHI_TEST_TEMP',tempfile.gettempdir()))/('case-'+uuid.uuid4().hex); self.root.mkdir(); self.st=Store(self.root,'test')
    def tearDown(self): self.st.db.close()
    def file(self,name,data):
        p=self.root/name; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(data if isinstance(data,bytes) else data.encode()); return p

class ArchiveTests(Base):
    def test_roundtrip(self):
        self.file('中文/a.txt','Hello'); out=archive.handle(self.st,{'action':'create','files':['中文/a.txt'],'output':'backup.zip'}); result=archive.handle(self.st,{'action':'extract','file':'backup.zip','directory':'restored'}); self.assertEqual((self.root/'restored/中文/a.txt').read_text(),'Hello'); self.assertEqual(result['files'][0]['sha256'],digest(b'Hello'))
    def test_traversal_rejected(self):
        with zipfile.ZipFile(self.root/'bad.zip','w') as z: z.writestr('../secret','bad')
        with self.assertRaises(ValueError): archive.handle(self.st,{'action':'extract','file':'bad.zip','directory':'out'})
        self.assertFalse((self.root/'out').exists())
    def test_case_collision(self):
        with zipfile.ZipFile(self.root/'bad.zip','w') as z: z.writestr('A.txt','a'); z.writestr('a.txt','b')
        with self.assertRaises(ValueError): archive.handle(self.st,{'action':'inspect','file':'bad.zip'})
    def test_existing_directory_rejected(self):
        self.file('a.txt','a'); archive.handle(self.st,{'action':'create','files':['a.txt'],'output':'a.zip'}); (self.root/'out').mkdir()
        with self.assertRaises(ValueError): archive.handle(self.st,{'action':'extract','file':'a.zip','directory':'out'})
    def test_reserved_names(self):
        for name in ('C:/a','NUL.txt','LPT1','a/../b','a.','foo\x00bar'):
            with self.assertRaises(ValueError): archive.safe(name)

if __name__=="__main__": unittest.main(verbosity=2)
