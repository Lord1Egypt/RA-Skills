import unittest,tempfile,json,sys,zipfile,io,datetime as dt
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from core import Store,local,readbytes,csvbytes
import lessons

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

class LessonsTests(Base):
 def record(self):return lessons.handle(self.s,{'action':'record','id':'l1','situation':'bad command','correction':'check flag','evidence':'exit 2','tags':['cli']})
 def test_record(self):self.assertEqual(self.record()['status'],'open')
 def test_duplicate(self):
  self.record()
  with self.assertRaises(ValueError):self.record()
 def test_resolve(self):self.record();self.assertEqual(lessons.handle(self.s,{'action':'resolve','id':'l1','verification':'ret est exit 0'})['status'],'verified')
 def test_review(self):self.record();d=self.report(lessons.handle(self.s,{'action':'review','query':'flag'}));self.assertEqual(len(d['lessons']),1);self.assertFalse(d['automaticPolicyChanges'])
 def test_missing(self):
  with self.assertRaises(ValueError):lessons.handle(self.s,{'action':'resolve','id':'missing','verification':'ok'})

if __name__=="__main__":unittest.main(verbosity=2)
