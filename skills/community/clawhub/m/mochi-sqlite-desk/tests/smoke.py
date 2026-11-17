import contextlib,gzip,http.server,json,os,sqlite3,tempfile,threading,unittest,sys
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from core import *
import sqlite_desk as sql


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

class SQLiteTests(Base):
 module=sql
 def db(self):
  p=self.root/'data.sqlite';db=sqlite3.connect(p);db.execute('CREATE TABLE data(id TEXT,amount INTEGER)');db.executemany('INSERT INTO data VALUES(?,?)',[('001',10),('002',20)]);db.commit();db.close();return p
 def test_select(self):self.db();r=self.result(action='query',database='data.sqlite',sql='SELECT SUM(amount) AS total FROM data');self.assertEqual(r['rows'],[{'total':30}])
 def test_write_denied(self):
  self.db()
  with self.assertRaises(ValueError):self.call(action='query',database='data.sqlite',sql='DELETE FROM data')
 def test_attach_denied(self):
  self.db()
  with self.assertRaises(ValueError):self.call(action='query',database='data.sqlite',sql="ATTACH ':memory:' AS extra")
 def test_pragma_denied(self):
  self.db()
  with self.assertRaises(ValueError):self.call(action='query',database='data.sqlite',sql='PRAGMA user_version=10')
 def test_truncate(self):self.db();r=self.result(action='query',database='data.sqlite',sql='SELECT * FROM data',limit=1);self.assertTrue(r['truncated']);self.assertEqual(r['returnedRows'],1)
 def test_schema(self):self.db();r=self.result(action='schema',database='data.sqlite');self.assertEqual(r['objects'][0]['columns'][0]['name'],'id')
 def test_csv_import_ids(self):self.file('in.csv','id,name\n001,Amy\n');v=self.call(action='import-csv',file='in.csv');r=self.result(action='query',database=v['database'],sql='SELECT id FROM data');self.assertEqual(r['rows'][0]['id'],'001')
 def test_source_unchanged(self):p=self.db();before=sha(p.read_bytes());self.call(action='query',database='data.sqlite',sql='SELECT * FROM data');self.assertEqual(before,sha(p.read_bytes()))

if __name__=="__main__": unittest.main(verbosity=2)
