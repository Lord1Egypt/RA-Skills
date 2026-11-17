import unittest,tempfile,json,sys,zipfile,io,datetime as dt
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from core import Store,local,readbytes,csvbytes
import docx_composer

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

class DocxTests(Base):
 def make(self,sections=None):return docx_composer.handle(self.s,{'action':'create','title':'中文 & report','sections':sections or [{'heading':'Results','paragraphs':['A < B'], 'table':[['Name','Value'],['Demo','1']]}]})
 def test_package(self):r=self.make();f=next(x for x in r['files'] if x.endswith('.docx'));self.assertTrue(zipfile.is_zipfile(self.root/f))
 def test_inspect(self):r=self.make();f=next(x for x in r['files'] if x.endswith('.docx'));d=self.report(docx_composer.handle(self.s,{'action':'inspect','file':f}));self.assertIn('A < B',d['paragraphs']);self.assertEqual(d['tables'],1)
 def test_xml(self):
  from xml.etree import ElementTree as ET
  r=self.make();f=next(x for x in r['files'] if x.endswith('.docx'))
  with zipfile.ZipFile(self.root/f) as z:
   for name in z.namelist():ET.fromstring(z.read(name))
   self.assertIn('word/styles.xml',z.namelist());self.assertNotIn(b'vbaProject',z.read('[Content_Types].xml'))
 def test_badtable(self):
  with self.assertRaises(ValueError):self.make([{'heading':'x','table':[['a'],['b','c']]}])
 def test_control(self):
  with self.assertRaises(ValueError):docx_composer.handle(self.s,{'action':'create','title':'bad\x01','sections':[]})

if __name__=="__main__":unittest.main(verbosity=2)
