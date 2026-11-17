import contextlib,gzip,http.server,json,os,sqlite3,tempfile,threading,unittest,sys
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from core import *
import backup_vault as backup


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

class BackupTests(Base):
 module=backup
 def snap(self,id='first'):return self.call(action='snapshot',id=id,directory='docs')
 def test_snapshot_verify(self):self.file('docs/a.txt','a');self.snap();self.assertTrue(self.call(action='verify',id='first')['verified'])
 def test_incremental_content(self):self.file('docs/a.txt','same');self.snap();r=self.snap('second');self.assertEqual(r['newContentBlobs'],0)
 def test_new_restore(self):self.file('docs/a.txt','a');self.snap();r=self.call(action='restore',id='first',destination='restored');self.assertTrue(r['verified']);self.assertEqual((self.root/'restored/a.txt').read_text(),'a')
 def test_restore_existing_denied(self):
  self.file('docs/a.txt','a');self.snap()
  with self.assertRaises(ValueError):self.call(action='restore',id='first',destination='docs')
 def test_corruption_detected(self):self.file('docs/a.txt','a');self.snap();m=self.store.get('snapshot','first');backup.blob(self.store,m['files'][0]['sha256']).write_text('broken');self.assertFalse(self.call(action='verify',id='first')['verified'])
 def test_exclude(self):self.file('docs/a.txt','a');self.file('docs/private.key','secret');self.call(action='snapshot',id='first',directory='docs',exclude=['*.key']);self.assertEqual(self.call(action='verify',id='first')['files'],1)
 def test_compare(self):self.file('docs/a.txt','a');self.snap();self.file('docs/a.txt','b');self.file('docs/b.txt','b');self.snap('second');r=self.result(action='compare',left='first',right='second');self.assertEqual(r['changed'],['a.txt']);self.assertEqual(r['added'],['b.txt'])
 def test_snapshot_id_conflict(self):
  self.file('docs/a.txt','a');self.snap()
  with self.assertRaises(ValueError):self.snap()
 def test_exclude_directory_before_scan(self):self.file('docs/a.txt','a');self.file('docs/node_modules/deep/one.txt','ignored');self.snap();self.assertEqual(self.call(action='verify',id='first')['files'],1)

if __name__=="__main__": unittest.main(verbosity=2)
