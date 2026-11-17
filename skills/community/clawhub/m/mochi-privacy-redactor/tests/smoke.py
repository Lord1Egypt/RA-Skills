import contextlib,gzip,http.server,json,os,sqlite3,tempfile,threading,unittest,sys
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from core import *
import privacy_redactor as privacy


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

class PrivacyTests(Base):
 module=privacy
 def test_text(self):self.file('one.txt','mail me at a@example.com phone 13812345678');r=self.call(action='redact',files=['one.txt']);out=self.root/r['report']['files'][0]['output'];self.assertEqual(out.read_text(),'mail me at [EMAIL] phone [PHONE]')
 def test_json_secret(self):self.file('one.json',json.dumps({'nested':{'password':'my-private','name':'Amy'}}));r=self.call(action='redact',files=['one.json']);v=json.loads((self.root/r['report']['files'][0]['output']).read_text());self.assertEqual(v['nested']['password'],'[SECRET]')
 def test_custom(self):self.file('one.txt','Project Secret Internal');r=self.call(action='redact',files=['one.txt'],literals=['Secret Internal']);self.assertNotIn('Secret Internal',(self.root/r['report']['files'][0]['output']).read_text())
 def test_no_secret_in_report(self):self.file('one.txt','a@example.com');r=self.call(action='scan',files=['one.txt']);self.assertNotIn('a@example.com',json.dumps(r));self.assertEqual(r['report']['files'][0]['matches']['email'],1)
 def test_source_unchanged(self):p=self.file('one.txt','13812345678');self.call(action='redact',files=['one.txt']);self.assertEqual(p.read_text(),'13812345678')
 def test_csv_structure(self):self.file('one.csv','name,email\nAmy,a@example.com\n');r=self.call(action='redact',files=['one.csv']);fields,rows=csv_rows(self.root/r['report']['files'][0]['output']);self.assertEqual(rows[0]['email'],'[EMAIL]')
 def test_ipv4_validation(self):self.file('one.txt','8.8.8.8 and 999.999.999.999');r=self.call(action='redact',files=['one.txt']);v=(self.root/r['report']['files'][0]['output']).read_text();self.assertIn('[IPV4]',v);self.assertIn('999.999',v)
 def test_token(self):self.file('one.txt','Bearer abcdefghijklmnopqrstuvwxyz123456');r=self.call(action='redact',files=['one.txt']);self.assertEqual((self.root/r['report']['files'][0]['output']).read_text(),'[TOKEN]')

if __name__=="__main__": unittest.main(verbosity=2)
