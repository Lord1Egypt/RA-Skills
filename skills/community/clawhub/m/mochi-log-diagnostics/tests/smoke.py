import contextlib,gzip,http.server,json,os,sqlite3,tempfile,threading,unittest,sys
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from core import *
import log_diagnostics as logs


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

class LogTests(Base):
 module=logs
 def access(self,ua='Browser',status=200):return '8.8.8.8 - - [25/Oct/2026:10:00:00 +0800] "GET /hello?token=abc HTTP/1.1" '+str(status)+' 100 "-" "'+ua+'"\n'
 def test_combined(self):self.file('web.log',self.access());r=self.result(action='analyze',files=['web.log']);self.assertEqual(r['selectedLines'],1);self.assertEqual(r['uniqueIPCount'],1);self.assertEqual(r['topRoutes'][0]['path'],'/hello')
 def test_bot_default(self):self.file('web.log',self.access('Googlebot'));r=self.result(action='analyze',files=['web.log']);self.assertEqual(r['excludedBotLines'],1);self.assertEqual(r['selectedLines'],0)
 def test_bot_optin(self):self.file('web.log',self.access('Googlebot'));self.assertEqual(self.result(action='analyze',files=['web.log'],includeBots=True)['selectedLines'],1)
 def test_json_errors(self):self.file('app.jsonl',json.dumps({'timestamp':'2026-10-25T10:00:00+08:00','level':'ERROR','message':'token=private123 fail order 123'})+'\n');r=self.result(action='analyze',files=['app.jsonl']);self.assertEqual(r['errors'],1);self.assertNotIn('private123',json.dumps(r))
 def test_gzip(self):self.file('web.log.gz',gzip.compress(self.access().encode()));self.assertEqual(self.result(action='analyze',files=['web.log.gz'])['selectedLines'],1)
 def test_invalid_lines(self):self.file('bad.log','nonsense\n'+self.access());r=self.result(action='analyze',files=['bad.log']);self.assertEqual(r['invalidLines'],1);self.assertEqual(r['selectedLines'],1)
 def test_status_filter(self):self.file('web.log',self.access(status=404)+self.access());r=self.result(action='analyze',files=['web.log'],statuses=[404]);self.assertEqual(r['statusCounts'],{'404':1})
 def test_sources_untouched(self):p=self.file('web.log',self.access());before=sha(p.read_bytes());self.call(action='analyze',files=['web.log']);self.assertEqual(before,sha(p.read_bytes()))
 def test_json_string_status(self):self.file('one.jsonl',json.dumps({'status':'500','message':'failure'})+'\n');r=self.result(action='analyze',files=['one.jsonl']);self.assertEqual(r['statusCounts'],{'500':1});self.assertEqual(r['errors'],1)

if __name__=="__main__": unittest.main(verbosity=2)
