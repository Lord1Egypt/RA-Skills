import unittest,tempfile,json,sys,zipfile,io,datetime as dt
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from core import Store,local,readbytes,csvbytes
import entity_graph

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

class GraphTests(Base):
 def node(self,n):return entity_graph.handle(self.s,{'action':'entity','id':n,'type':'project','name':n,'source':'user supplied'})
 def test_entity(self):self.assertEqual(self.node('a')['name'],'a')
 def test_relation(self):self.node('a');self.node('b');e=entity_graph.handle(self.s,{'action':'relate','from':'a','to':'b','relation':'depends','source':'plan'});self.assertEqual(e['to'],'b')
 def test_dangling(self):
  self.node('a')
  with self.assertRaises(ValueError):entity_graph.handle(self.s,{'action':'relate','from':'a','to':'b','relation':'depends','source':'plan'})
 def test_depth(self):
  self.node('a');self.node('b');entity_graph.handle(self.s,{'action':'relate','from':'a','to':'b','relation':'depends','source':'plan'});d=self.report(entity_graph.handle(self.s,{'action':'query','id':'a','depth':0}));self.assertEqual(len(d['entities']),1)
 def test_cycle(self):
  self.node('a');entity_graph.handle(self.s,{'action':'relate','from':'a','to':'a','relation':'self','source':'plan'});d=self.report(entity_graph.handle(self.s,{'action':'query','id':'a','depth':4}));self.assertEqual(len(d['entities']),1)

if __name__=="__main__":unittest.main(verbosity=2)
