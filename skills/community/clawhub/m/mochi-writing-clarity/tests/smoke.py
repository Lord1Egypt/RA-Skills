import unittest,tempfile,json,sys,zipfile,io,datetime as dt
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from core import Store,local,readbytes,csvbytes
import writing_clarity

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

class WritingTests(Base):
 def test_lint(self):self.put('draft.txt','值得注意的是，文本。');self.assertEqual(self.report(writing_clarity.handle(self.s,{'action':'lint','file':'draft.txt'}))['findings'][0]['rule'],'generic-phrase')
 def test_compare_same(self):self.put('a.txt','Price 9.90');self.put('b.txt','The price is 9.90');self.assertTrue(self.report(writing_clarity.handle(self.s,{'action':'compare','before':'a.txt','after':'b.txt'}))['factTokensUnchanged'])
 def test_compare_changed(self):self.put('a.txt','9.90');self.put('b.txt','99');self.assertFalse(self.report(writing_clarity.handle(self.s,{'action':'compare','before':'a.txt','after':'b.txt'}))['factTokensUnchanged'])
 def test_repeated(self):self.put('a.txt','same\n\nsame');self.assertEqual(len(self.report(writing_clarity.handle(self.s,{'action':'lint','file':'a.txt'}))['repeatedParagraphs']),1)
 def test_source(self):self.put('a.txt','你好123');writing_clarity.handle(self.s,{'action':'lint','file':'a.txt'});self.assertEqual((self.root/'a.txt').read_text(encoding='utf-8'),'你好123')

if __name__=="__main__":unittest.main(verbosity=2)
