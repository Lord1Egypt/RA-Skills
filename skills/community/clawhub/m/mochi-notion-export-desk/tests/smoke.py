import unittest,tempfile,json,sys,zipfile,io,datetime as dt
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from core import Store,local,readbytes,csvbytes
import notion_export

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

class NotionTests(Base):
 def test_index(self):self.zip('export.zip',{'Page.md':'# Demo\nData','Table.csv':'name,value\na,1\n'});d=self.report(notion_export.handle(self.s,{'action':'index','file':'export.zip'}));self.assertEqual(d['tables'][0]['rows'],1);self.assertEqual(d['pages'][0]['title'],'Demo')
 def test_path(self):
  self.zip('a.zip',{'../x.md':'bad'})
  with self.assertRaises(ValueError):notion_export.handle(self.s,{'action':'index','file':'a.zip'})
 def test_unsupported(self):
  self.zip('a.zip',{'x.html':'html'})
  with self.assertRaises(ValueError):notion_export.handle(self.s,{'action':'index','file':'a.zip'})
 def test_skip(self):self.zip('a.zip',{'x.md':'text','image.png':'bytes'});self.assertEqual(self.report(notion_export.handle(self.s,{'action':'index','file':'a.zip'}))['skipped'],['image.png'])
 def test_bad_csv(self):
  self.zip('a.zip',{'x.csv':'a,a\n1,2'})
  with self.assertRaises(ValueError):notion_export.handle(self.s,{'action':'index','file':'a.zip'})

if __name__=="__main__":unittest.main(verbosity=2)
