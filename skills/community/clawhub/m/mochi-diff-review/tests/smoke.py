import contextlib,gzip,http.server,json,os,sqlite3,tempfile,threading,unittest,sys
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from core import *
import diff_review as diff


class Base(unittest.TestCase):
 module=None
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name);self.store=Store(self.root,'test-desk')
 def tearDown(self):self.store.db.close();self.temp.cleanup()
 def file(self,name,value):
  p=self.root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(value if isinstance(value,bytes) else value.encode('utf-8'));return p
 def call(self,**request):
  with self.store.db:return self.module.handle(self.store,request)
 def result(self,**request):return self.call(**request)['report']

class CoreTests(Base):
 def test_traversal(self):
  for name in ('../escape','a/../../escape','/etc/passwd','C:/Windows/test'):
   with self.assertRaises(ValueError):local(self.root,name)
 def test_existing_output_refused(self):
  p=self.file('one.txt','old')
  with self.assertRaises(FileExistsError):write_new(p,b'new')
  self.assertEqual(p.read_text(),'old')
 def test_atomic_rollback(self):
  with self.assertRaises(ValueError):
   with self.store.db:self.store.put('x','a',{'x':1});raise ValueError('rollback')
  self.assertIsNone(self.store.get('x','a'))
 def test_csv_width(self):
  with self.assertRaises(ValueError):csv_rows(self.file('bad.csv','a,b\n1,2,3\n'))
 def test_csv_formula(self):
  out=csvbytes(['name'],[{'name':'=SUM(A1:A2)'}]).decode('utf-8-sig');self.assertIn("'=SUM",out)
 def test_html_escape(self):self.assertNotIn('<script>',htmlreport('<script>',{'x':'<script>'}).decode())
 def test_network_private_denied(self):
  with self.assertRaises(ValueError):safe_request('https://127.0.0.1/')
 def test_network_url_credentials(self):
  with self.assertRaises(ValueError):safe_request('https://user:password@example.com/')
 def test_ics_unicode_folding(self):
  data=icalbytes(['SUMMARY:'+'中文'*80]);self.assertTrue(all(len(x)<=75 for x in data.split(b'\r\n')));self.assertEqual(data.decode().replace('\r\n ',''),'SUMMARY:'+'中文'*80+'\r\n')

class DiffTests(Base):
 module=diff
 def test_text_diff(self):self.file('a.txt','one\ntwo');self.file('b.txt','one\nthree');r=self.result(action='text',left='a.txt',right='b.txt');self.assertFalse(r['equal']);self.assertIn('+three',r['unifiedDiff'])
 def test_ignore_spaces(self):self.file('a.txt','one two');self.file('b.txt','one   two');self.assertTrue(self.result(action='text',left='a.txt',right='b.txt',ignoreWhitespace=True)['equal'])
 def test_json_order(self):self.file('a.json','{"a":1,"b":2}');self.file('b.json','{"b":2,"a":1}');self.assertTrue(self.result(action='json',left='a.json',right='b.json')['equal'])
 def test_json_path(self):self.file('a.json','{"x":[1]}');self.file('b.json','{"x":[2]}');self.assertEqual(self.result(action='json',left='a.json',right='b.json')['differences'][0]['path'],'/x/0')
 def test_csv_keyed(self):self.file('a.csv','id,value\n1,a\n2,b\n');self.file('b.csv','id,value\n2,c\n1,a\n');r=self.result(action='csv',left='a.csv',right='b.csv',keys=['id']);self.assertEqual(r['changedRowCount'],1);self.assertEqual(r['changedRows'][0]['key'],['2'])
 def test_csv_duplicates(self):self.file('a.csv','id,v\n1,a\n1,b\n');self.file('b.csv','id,v\n1,c\n');r=self.result(action='csv',left='a.csv',right='b.csv',keys=['id']);self.assertEqual(r['leftDuplicateKeys'],[['1']]);self.assertEqual(r['changedRowCount'],0)
 def test_directory(self):self.file('old/a.txt','old');self.file('new/a.txt','new');self.file('new/b.txt','b');r=self.result(action='directories',left='old',right='new');self.assertEqual(r['changed'],['a.txt']);self.assertEqual(r['added'],['b.txt'])
 def test_manifest_verify(self):self.file('docs/a.txt','a');v=self.call(action='manifest',directory='docs');r=self.result(action='verify',directory='docs',manifest=v['directory']+'/report.json');self.assertTrue(r['verified'])

if __name__=="__main__": unittest.main(verbosity=2)
