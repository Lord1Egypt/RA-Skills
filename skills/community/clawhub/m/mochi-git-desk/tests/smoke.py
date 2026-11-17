import datetime as dt,io,json,os,subprocess,tempfile,unittest,zipfile,uuid,sys
from pathlib import Path
from unittest.mock import patch,MagicMock
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from core import *
import git_desk as gd

class Base(unittest.TestCase):
    def setUp(self):
        self.root=Path(os.environ.get('MOCHI_TEST_TEMP',tempfile.gettempdir()))/('case-'+uuid.uuid4().hex); self.root.mkdir(); self.st=Store(self.root,'test')
    def tearDown(self): self.st.db.close()
    def file(self,name,data):
        p=self.root/name; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(data if isinstance(data,bytes) else data.encode()); return p

class GitTests(Base):
    def setup_repo(self):
        repo=self.root/'repo'; repo.mkdir(); subprocess.run(['git','init','--quiet',str(repo)],check=True); subprocess.run(['git','-C',str(repo),'config','user.name','Test'],check=True); subprocess.run(['git','-C',str(repo),'config','user.email','test@example.com'],check=True); self.file('repo/a.txt','original\n'); subprocess.run(['git','-C',str(repo),'add','a.txt'],check=True); subprocess.run(['git','-C',str(repo),'commit','--quiet','-m','Initial'],check=True); return repo
    def test_real_status_history(self):
        self.setup_repo(); self.file('repo/a.txt','changed\n'); s=gd.handle(self.st,{'action':'status','repository':'repo'}); self.assertEqual(s['changes'][0]['path'],'a.txt'); h=gd.handle(self.st,{'action':'history','repository':'repo'}); self.assertEqual(h[0]['subject'],'Initial')
    def test_real_checkpoint(self):
        self.setup_repo(); self.file('repo/a.txt','changed\n'); self.file('repo/new.txt','new\n'); out=gd.handle(self.st,{'action':'checkpoint','repository':'repo','id':'snap','includeUntracked':True})
        with zipfile.ZipFile(out['file']) as z: self.assertIn('untracked/new.txt',z.namelist()); self.assertIn(b'+changed',z.read('working.patch'))
        self.assertEqual((self.root/'repo/a.txt').read_text(),'changed\n')
    def test_checkpoint_inside_repo_rejected(self):
        self.setup_repo()
        with self.assertRaises(ValueError): gd.handle(self.st,{'action':'checkpoint','repository':'repo','id':'snap','output':'repo/snap.zip'})

if __name__=="__main__": unittest.main(verbosity=2)
