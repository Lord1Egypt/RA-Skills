import unittest,tempfile,json,sys,zipfile,io,datetime as dt
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from core import Store,local,readbytes,csvbytes
import ui_accessibility

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

class AccessibilityTests(Base):
 def scan(self,html):self.put('index.html',html);return self.report(ui_accessibility.handle(self.s,{'action':'audit','file':'index.html'}))
 def test_missing(self):d=self.scan('<html><img src="x"><input><button></button></html>');self.assertEqual({x['rule'] for x in d['issues']},{'missing-document-language','missing-image-alt','input-without-label','empty-button'})
 def test_labels(self):self.assertFalse(self.scan('<html lang="en"><label for="q">Name</label><input id="q"><button>Go</button></html>')['issues'])
 def test_duplicate(self):self.assertIn('duplicate-id',[x['rule'] for x in self.scan('<html lang="en"><p id="a"></p><p id="a"></p></html>')['issues']])
 def test_contrast(self):self.assertEqual(ui_accessibility.contrast('#000000','#FFFFFF'),21)
 def test_bad_colour(self):
  with self.assertRaises(ValueError):ui_accessibility.contrast('white','#FFFFFF')

if __name__=="__main__":unittest.main(verbosity=2)
