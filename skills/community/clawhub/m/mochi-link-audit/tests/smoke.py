import contextlib,gzip,http.server,json,os,sqlite3,tempfile,threading,unittest,sys
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from core import *
import link_audit as links


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

class LinkTests(NetworkBase):
 module=links
 def crawl(self,**kw):return self.result(action='crawl',url=self.url+'/',allowPrivateHosts=['127.0.0.1'],**kw)
 def test_broken_link(self):r=self.crawl();self.assertEqual(r['brokenInternalLinks'][0]['status'],404)
 def test_fragment(self):r=self.crawl();self.assertEqual(r['missingFragments'][0]['fragment'],'missing')
 def test_duplicate_title(self):r=self.crawl();self.assertEqual(r['duplicateTitles'][0]['title'],'Home')
 def test_alt(self):r=self.crawl();self.assertEqual(r['pages'][0]['missingAlt'],1)
 def test_bound(self):r=self.crawl(maxPages=1);self.assertEqual(r['visited'],1);self.assertTrue(r['limitReached'])
 def test_external_not_crawled(self):
  p=links.Page();p.feed('<a href="https://outside.example/a">Out</a>');self.assertEqual(p.links,['https://outside.example/a'])
 def test_private_denied(self):r=self.result(action='crawl',url='https://127.0.0.1/');self.assertEqual(r['pages'][0]['errorType'],'ValueError')
 def test_script_not_executed(self):p=links.Page();p.feed('<script>fetch("/hidden")</script><a href="/ok">ok</a>');self.assertEqual(p.links,['/ok'])

if __name__=="__main__": unittest.main(verbosity=2)
