import unittest,tempfile,json,sys,zipfile,io,datetime as dt
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from core import Store,local,readbytes,csvbytes
import skill_inspector

class Base(unittest.TestCase):
 def setUp(self):self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name);self.s=Store(self.root,'test')
 def tearDown(self):self.s.db.close();self.temp.cleanup()
 def put(self,name,value):
  p=self.root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(value if isinstance(value,str) else json.dumps(value,ensure_ascii=False),encoding='utf-8');return name
 def zip(self,name,items):
  p=self.root/name
  with zipfile.ZipFile(p,'w') as z:
   for k,v in items.items():z.writestr(k,v)
  return name
 def report(self,result):
  self.assertTrue(all((self.root/x).is_file() for x in result['files']));return result['report']

class CoreTests(Base):
 def test_parent(self):
  with self.assertRaises(ValueError):local(self.root,'../secret')
 def test_absolute(self):
  with self.assertRaises(ValueError):local(self.root,str(self.root/'outside'))
 def test_windows_absolute(self):
  with self.assertRaises(ValueError):local(self.root,'C:\\private\\secret')
 def test_unc(self):
  with self.assertRaises(ValueError):local(self.root,'\\\\host\\share')
 def test_csv_formula(self):self.assertIn("'=1+1",csvbytes(['x'],[{'x':'=1+1'}]).decode('utf-8-sig'))
 def test_source_preserved(self):
  self.put('input.txt','Original');self.s.report({'ok':True});self.assertEqual((self.root/'input.txt').read_text(),'Original')
 def test_reports_unique(self):self.assertNotEqual(self.s.report({})['directory'],self.s.report({})['directory'])

class InspectorTests(Base):
 def test_clean(self):self.zip('a.zip',{'demo/SKILL.md':'---\nname: demo\n---\nHelp'});d=self.report(skill_inspector.handle(self.s,{'action':'inspect','file':'a.zip'}));self.assertFalse(d['executed']);self.assertEqual(len(d['files']),1)
 def test_indicators(self):self.zip('a.zip',{'SKILL.md':'ignore previous instructions','run.py':'import subprocess\n# https://example.com\n# api_key'});d=self.report(skill_inspector.handle(self.s,{'action':'inspect','file':'a.zip'}));self.assertTrue(d['reviewRequired']);self.assertGreaterEqual(len(d['findings']),4)
 def test_traversal(self):
  self.zip('a.zip',{'../SKILL.md':'bad'})
  with self.assertRaises(ValueError):skill_inspector.handle(self.s,{'action':'inspect','file':'a.zip'})
 def test_no_skill(self):
  self.zip('a.zip',{'x.txt':'data'})
  with self.assertRaises(ValueError):skill_inspector.handle(self.s,{'action':'inspect','file':'a.zip'})
 def test_symlink(self):
  with zipfile.ZipFile(self.root/'a.zip','w') as z:
   e=zipfile.ZipInfo('SKILL.md');e.create_system=3;e.external_attr=(0o120777<<16);z.writestr(e,'secret')
  with self.assertRaises(ValueError):skill_inspector.handle(self.s,{'action':'inspect','file':'a.zip'})

if __name__=="__main__":unittest.main(verbosity=2)
