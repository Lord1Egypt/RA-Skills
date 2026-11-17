import contextlib,gzip,http.server,json,os,sqlite3,tempfile,threading,unittest,sys
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from core import *
import knowledge_desk as kb


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

class KnowledgeTests(Base):
 module=kb
 def index(self):self.file('docs/one.md','退款申请需要订单编号。\nRefund requests need an order number.');return self.call(action='index',directory='docs',tags=['support'])
 def test_chinese_search(self):
  self.index();r=self.result(action='search',query='退款');self.assertEqual(r['totalHits'],1);self.assertTrue(r['matches'][0]['indexCurrent'])
 def test_english_search(self):self.index();self.assertIn('Refund',self.result(action='search',query='refund')['matches'][0]['snippet'])
 def test_incremental(self):self.index();self.assertEqual(self.call(action='index',directory='docs',tags=['support'])['unchanged'],['docs/one.md'])
 def test_stale(self):self.index();self.file('docs/one.md','changed');self.assertFalse(self.result(action='search',query='refund')['matches'][0]['indexCurrent'])
 def test_prune(self):self.index();self.file('docs/two.txt','second');(self.root/'docs/one.md').unlink();r=self.call(action='index',directory='docs',prune=True);self.assertEqual(r['pruned'],['docs/one.md'])
 def test_html_ignores_scripts(self):self.file('page.html','<title>Useful</title><script>hiddenkeyword</script>');self.call(action='index',files=['page.html']);self.assertEqual(self.result(action='search',query='hiddenkeyword')['totalHits'],0)
 def test_remove_keeps_source(self):self.index();key=self.call(action='list')[0]['id'];self.call(action='remove',id=key);self.assertTrue((self.root/'docs/one.md').exists());self.assertEqual(self.call(action='list'),[])
 def test_tag_filter(self):self.index();self.assertEqual(self.result(action='search',query='refund',tag='other')['totalHits'],0)
 def test_invalid_tags(self):
  self.file('one.txt','hello')
  with self.assertRaises(ValueError):self.call(action='index',files=['one.txt'],tags='not-a-list')

if __name__=="__main__": unittest.main(verbosity=2)
