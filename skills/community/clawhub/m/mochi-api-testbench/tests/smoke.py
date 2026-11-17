import contextlib,gzip,http.server,json,os,sqlite3,tempfile,threading,unittest,sys
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from core import *
import api_testbench as api


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

class HTTPFixture(http.server.BaseHTTPRequestHandler):
 def log_message(self,*args):pass
 def do_HEAD(self):self.do_GET()
 def do_GET(self):
  pages={'/':'<html><title>Home</title><h1>Home</h1><a href="/about#missing">About</a><a href="/gone">Gone</a><img src="one.png"></html>','/about':'<html><title>Home</title><h1>About</h1><div id="present"></div></html>','/api':'{"ok":true,"items":[{"id":1}]}','/redirect':''}
  if self.path=='/redirect':self.send_response(302);self.send_header('Location','/api');self.end_headers();return
  status=200 if self.path in pages else 404;body=pages.get(self.path,'missing').encode();self.send_response(status);self.send_header('Content-Type','application/json' if self.path=='/api' else 'text/html');self.send_header('X-Test','yes');self.end_headers()
  if self.command!='HEAD':self.wfile.write(body)
 def do_POST(self):self.do_GET()

class NetworkBase(Base):
 @classmethod
 def setUpClass(cls):cls.server=http.server.ThreadingHTTPServer(('127.0.0.1',0),HTTPFixture);cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start();cls.url='http://127.0.0.1:'+str(cls.server.server_port)
 @classmethod
 def tearDownClass(cls):cls.server.shutdown();cls.server.server_close();cls.thread.join()

class APITests(NetworkBase):
 module=api
 def case(self,**kw):return {'id':'one','url':self.url+'/api','assert':{'status':200,'jsonEquals':{'/ok':True},'jsonExists':['/items/0/id']},**kw}
 def test_success(self):r=self.result(action='run',cases=[self.case()],allowPrivateHosts=['127.0.0.1']);self.assertTrue(r['passed'])
 def test_failure_assert(self):r=self.result(action='run',cases=[self.case(assertx='ignored',**{'assert':{'status':404}})],allowPrivateHosts=['127.0.0.1']);self.assertFalse(r['passed'])
 def test_validate_no_network(self):self.assertEqual(self.call(action='validate',cases=[self.case()])['networkRequests'],0)
 def test_mutation_requires_optin(self):
  with self.assertRaises(ValueError):self.call(action='run',cases=[self.case(method='POST')],allowPrivateHosts=['127.0.0.1'])
 def test_private_requires_optin(self):r=self.result(action='run',cases=[self.case()]);self.assertFalse(r['passed']);self.assertEqual(r['cases'][0]['errorType'],'ValueError')
 def test_secret_not_saved(self):
  with patch.dict(os.environ,{'MOCHI_TEST_TOKEN':'private-test-secret'}):r=self.call(action='run',cases=[self.case(headerEnv={'Authorization':'MOCHI_TEST_TOKEN'})],allowPrivateHosts=['127.0.0.1'])
  self.assertNotIn('private-test-secret',json.dumps(r));self.assertTrue(r['report']['passed'])
 def test_duplicate_ids(self):
  with self.assertRaises(ValueError):self.call(action='validate',cases=[self.case(),self.case()])
 def test_redirect_explicit(self):r=self.result(action='run',cases=[self.case(url=self.url+'/redirect',**{'assert':{'status':302}})],allowPrivateHosts=['127.0.0.1']);self.assertTrue(r['passed'])
 def test_missing_secret_prevents_all_requests(self):
  with patch('api_testbench.safe_request') as call:
   with self.assertRaises(ValueError):self.call(action='run',cases=[self.case(),self.case(id='two',bearerEnv='MOCHI_ABSENT_TEST_TOKEN')],allowPrivateHosts=['127.0.0.1'])
   call.assert_not_called()

if __name__=="__main__": unittest.main(verbosity=2)
