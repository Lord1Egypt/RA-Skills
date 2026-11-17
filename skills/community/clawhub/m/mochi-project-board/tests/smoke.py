import contextlib,gzip,http.server,json,os,sqlite3,tempfile,threading,unittest,sys
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from core import *
import project_board as project


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

class ProjectTests(Base):
 module=project
 def setup_project(self):self.call(action='project.upsert',id='p1',name='Website launch')
 def task(self,id,**kw):return self.call(action='task.upsert',id=id,project='p1',title=id,**kw)
 def test_dependency_blocks_completion(self):
  self.setup_project();self.task('a');self.task('b',dependencies=['a'])
  with self.assertRaises(ValueError):self.task('b',dependencies=['a'],status='done')
 def test_dependency_completion(self):self.setup_project();self.task('a',status='done');self.task('b',dependencies=['a'],status='done');self.assertEqual(self.call(action='list')['counts']['done'],2)
 def test_cycle(self):
  self.setup_project();self.task('a');self.task('b',dependencies=['a'])
  with self.assertRaises(ValueError):self.task('a',dependencies=['b'])
 def test_missing_dependency(self):
  self.setup_project()
  with self.assertRaises(ValueError):self.task('a',dependencies=['missing'])
 def test_overdue(self):self.setup_project();self.task('a',due='2026-01-01');self.assertTrue(self.call(action='list',today='2026-01-02')['tasks'][0]['overdue'])
 def test_workload(self):self.setup_project();self.task('a',owner='Amy',estimateHours=2.5);self.assertEqual(self.call(action='list')['remainingHoursByOwner'],{'Amy':2.5})
 def test_report_calendar_escape(self):self.setup_project();self.call(action='task.upsert',id='a',project='p1',title='Line\nBEGIN:VEVENT',due='2026-11-01');r=self.call(action='report');ics=(self.root/r['directory']/'deadlines.ics').read_text();self.assertEqual(ics.count('\nBEGIN:VEVENT'),1);self.assertIn('Line\\nBEGIN:VEVENT',ics)
 def test_delete_dependency_guard(self):
  self.setup_project();self.task('a');self.task('b',dependencies=['a'])
  with self.assertRaises(ValueError):self.call(action='task.remove',id='a')
 def test_reopen_prerequisite_guard(self):
  self.setup_project();self.task('a',status='done');self.task('b',status='done',dependencies=['a'])
  with self.assertRaises(ValueError):self.task('a',status='todo')

if __name__=="__main__": unittest.main(verbosity=2)
