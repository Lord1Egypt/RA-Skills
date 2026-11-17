import unittest,tempfile,json,sys,zipfile,io,datetime as dt
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from core import Store,local,readbytes,csvbytes
import obsidian_map

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

class ObsidianTests(Base):
 def setupvault(self):self.put('vault/A.md','# A\n[[B#Intro|intro]]');self.put('vault/B.md','# Intro\nText')
 def runmap(self):return self.report(obsidian_map.handle(self.s,{'action':'map','directory':'vault'}))
 def test_backlink(self):self.setupvault();d=self.runmap();self.assertEqual(d['backlinks']['B.md'],['A.md']);self.assertFalse(d['brokenLinks'])
 def test_missing(self):self.put('vault/A.md','[[Missing]]');self.assertEqual(self.runmap()['brokenLinks'][0]['reason'],'note-not-found')
 def test_heading(self):self.setupvault();self.put('vault/B.md','# Other');self.assertEqual(self.runmap()['brokenLinks'][0]['reason'],'heading-not-found')
 def test_code(self):self.put('vault/A.md','```text\n[[NotALink]]\n```');self.assertFalse(self.runmap()['brokenLinks'])
 def test_ambiguous(self):self.put('vault/A.md','[[B]]');self.put('vault/x/B.md','one');self.put('vault/y/B.md','two');self.assertEqual(self.runmap()['brokenLinks'][0]['reason'],'ambiguous')

if __name__=="__main__":unittest.main(verbosity=2)
