import datetime as dt,io,json,os,subprocess,tempfile,unittest,zipfile,uuid,sys
from pathlib import Path
from unittest.mock import patch,MagicMock
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from core import *
import contact_desk as contacts

class Base(unittest.TestCase):
    def setUp(self):
        self.root=Path(os.environ.get('MOCHI_TEST_TEMP',tempfile.gettempdir()))/('case-'+uuid.uuid4().hex); self.root.mkdir(); self.st=Store(self.root,'test')
    def tearDown(self): self.st.db.close()
    def file(self,name,data):
        p=self.root/name; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(data if isinstance(data,bytes) else data.encode()); return p

class ContactTests(Base):
    def put(self,id,name='Alice',**extra): return contacts.handle(self.st,{'action':'put','contact':{'id':id,'name':name,**extra}})
    def test_duplicate_normalization(self):
        self.put('a',emails=['A@example.com'],phones=['+86 123-456']); self.put('b',emails=['a@example.com'],phones=['+86123456']); self.assertEqual(len(contacts.handle(self.st,{'action':'duplicates'})),1)
    def test_merge_conflict_and_history(self):
        self.put('a','Alice',emails=['a@example.com']); self.put('b','Alicia',phones=['123']); contacts.handle(self.st,{'action':'followup','id':'note','contactId':'b','note':'Call','date':'2026-10-24','nextDate':'2026-10-25'}); r={'action':'merge','target':'a','sources':['b']}; self.assertFalse(contacts.handle(self.st,r)['applied']); contacts.handle(self.st,{**r,'choose':{'name':'Alice'}}); self.assertIsNone(self.st.get('contact','b')); self.assertEqual(self.st.get('followup','note')['contactId'],'a')
    def test_vcard_roundtrip(self):
        self.put('a','张三',emails=['a@example.com']); p=contacts.handle(self.st,{'action':'export','format':'vcard'}); result=contacts.handle(self.st,{'action':'import','file':str(Path(p['file']).relative_to(self.root))}); self.assertEqual(result['contacts'][0]['name'],'张三')
    def test_import_preview_no_writes(self):
        self.file('contacts.csv','name,emails\nAlice,a@example.com\n'); result=contacts.handle(self.st,{'action':'import','file':'contacts.csv'}); self.assertEqual(len(result['contacts']),1); self.assertEqual(self.st.all('contact'),[])
    def test_due_latest_followup(self):
        self.put('a'); contacts.handle(self.st,{'action':'followup','id':'n1','contactId':'a','note':'Call','date':'2026-10-24','nextDate':'2026-10-25'}); self.assertEqual(len(contacts.handle(self.st,{'action':'due','date':'2026-10-26'})),1)

if __name__=="__main__": unittest.main(verbosity=2)
