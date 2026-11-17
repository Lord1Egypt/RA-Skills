import csv,hashlib,json,os,shutil,sqlite3,sys,tempfile,unittest,zipfile,uuid
from pathlib import Path
DOMAINS=Path(__file__).resolve().parents[1]/"scripts"
sys.path.insert(0,str(DOMAINS))
import run as claw
from io_utils import transaction,digest

class Base(unittest.TestCase):
 def setUp(self):
  self.base=Path(os.environ.get('MOCHI_TEST_ROOT',tempfile.gettempdir()))/('case-'+uuid.uuid4().hex);self.base.mkdir(parents=True);self.ws=self.base/'workspace';self.ws.mkdir();self.seq=0
 def tearDown(self):pass # Retain isolated artifacts as functional-test evidence.
 def execute(self,module,job):
  self.seq+=1;return transaction(self.ws,'test-'+module.__name__,{'requestId':'r'+str(self.seq),**job},module.process)
 def output(self,r,name):return next(self.ws/f['path'] for f in r['files'] if f['path'].endswith('/'+name))
 def csv(self,name,rows,headers=None):
  p=self.ws/name
  with p.open('w',encoding='utf-8-sig',newline='') as f:csv.writer(f).writerows([headers or ['id','date','currency','category','amount','kind'],*rows])
  return p
 def spec(self,name):return {'file':name,'mapping':{k:k for k in ['id','date','currency','category','amount','kind']}}
 def row(self,rid='001',amount='9.90',currency='USD',date='2026-10-01',kind='sale',category='Software'):return [rid,date,currency,category,amount,kind]

class MaintenanceTests(Base):
 def setUp(self):
  super().setUp();self.root=self.base/'instance';self.root.mkdir();(self.root/'openclaw.json').write_text(json.dumps({'agents':{'list':[{'id':'main','workspace':str(self.root/'workspace')},{'id':'family','workspace':str(self.root/'workspace-family')}]},'bindings':[{'agentId':'family','match':{'channel':'openclaw-weixin','accountId':'family-test'}}],'models':{'providers':{'example':{'apiKey':'test-private-credential'}}}}));(self.root/'workspace').mkdir();(self.root/'workspace'/'notes.md').write_text('preserve my notes');(self.root/'credentials').mkdir();(self.root/'credentials'/'token.txt').write_text('private-fixture-only');self.op=type('Maintenance',(),{'__name__':'maintenance','process':staticmethod(claw.worker(self.root))})
 def backup(self):return self.execute(self.op,{'action':'backup','sensitiveBackupAccepted':True})
 def test_inventory_redacts(self):
  r=self.execute(self.op,{'action':'inspect'});txt=self.output(r,'config-redacted.json').read_text();self.assertNotIn('test-private-credential',txt);self.assertIn('[redacted]',txt);self.assertEqual(len(r['agents']),2)
 def test_backup_verified_credentials_included(self):
  r=self.backup();m=claw.inspect_archive(self.output(r,'openclaw-snapshot.zip'));self.assertEqual(len(m['files']),3);self.assertIn('credentials/token.txt',[a['path'] for a in m['files']])
 def test_sensitive_ack_required(self):self.assertRaises(ValueError,self.execute,self.op,{'action':'backup'})
 def test_restore_rehearsal(self):
  r=self.backup();p=self.output(r,'openclaw-snapshot.zip');r=self.execute(self.op,{'action':'rehearse','archive':str(p)});rest=self.output(r,'notes.md');self.assertEqual(rest.read_text(),'preserve my notes');self.assertFalse(r['liveInstanceModified']);self.assertEqual((self.root/'workspace'/'notes.md').read_text(),'preserve my notes')
 def test_compare(self):
  r=self.backup();p=self.output(r,'openclaw-snapshot.zip');(self.root/'workspace'/'notes.md').write_text('new');r=self.execute(self.op,{'action':'compare','archive':str(p)});self.assertEqual(r['changes'],[{'path':'workspace/notes.md','state':'changed'}])
 def test_archive_tamper(self):
  r=self.backup();p=self.output(r,'openclaw-snapshot.zip');q=self.ws/'bad.zip'
  with zipfile.ZipFile(p) as z,zipfile.ZipFile(q,'w') as w:
   for i in z.infolist():w.writestr(i,z.read(i) if i.filename!='workspace/notes.md' else b'changed')
  self.assertRaises(ValueError,claw.inspect_archive,q)
 def test_zip_traversal(self):
  p=self.ws/'bad.zip'
  with zipfile.ZipFile(p,'w') as z:z.writestr('../secret','bad')
  self.assertRaises(ValueError,claw.inspect_archive,p)
 def test_sqlite_online_backup(self):
  p=self.root/'workspace'/'memory.sqlite';c=sqlite3.connect(p);c.execute('PRAGMA journal_mode=WAL');c.execute('CREATE TABLE notes (v TEXT)');c.execute('INSERT INTO notes VALUES (?)',('important',));c.commit();r=self.backup();m=claw.inspect_archive(self.output(r,'openclaw-snapshot.zip'));self.assertEqual(next(x['method'] for x in m['files'] if x['path'].endswith('.sqlite')),'sqlite-online-backup');c.close()
 def test_binding_collision(self):
  p=self.root/'openclaw.json';j=json.loads(p.read_text());j['bindings'].append({'agentId':'main','match':j['bindings'][0]['match']});p.write_text(json.dumps(j));r=self.execute(self.op,{'action':'inspect'});self.assertTrue(r['warnings'])
 def test_root_selection(self):self.assertRaises(ValueError,claw.root_path,self.ws)
 def test_include_escape(self):self.assertRaises(ValueError,self.execute,self.op,{'action':'backup','sensitiveBackupAccepted':True,'include':['openclaw.json','../workspace']})
 def test_original_config_untouched(self):
  p=self.root/'openclaw.json';old=digest(p);self.backup();self.assertEqual(digest(p),old)
 def test_current_entries_roster(self):
  p=self.root/'openclaw.json';j=json.loads(p.read_text());j['agents']={'entries':{a['id']:{k:v for k,v in a.items() if k!='id'} for a in j['agents']['list']}};p.write_text(json.dumps(j));r=self.execute(self.op,{'action':'inspect'});self.assertEqual([a['id'] for a in r['agents']],['main','family'])
 def test_skill_state_preserved(self):
  folder=self.root/'workspace/.mochilab/mochi-quick-notes';folder.mkdir(parents=True);(folder/'notes.json').write_text('["keep me"]');r=self.backup();m=claw.inspect_archive(self.output(r,'openclaw-snapshot.zip'));self.assertIn('workspace/.mochilab/mochi-quick-notes/notes.json',[a['path'] for a in m['files']])
 def test_zip_case_collision(self):
  p=self.ws/'case.zip'
  with zipfile.ZipFile(p,'w') as z:z.writestr('A.txt','first');z.writestr('a.txt','second')
  self.assertRaises(ValueError,claw.inspect_archive,p)
 def test_cli_root_overlap_rejected(self):
  import subprocess
  result=subprocess.run([sys.executable,'-B',str(Path(claw.__file__)), '--workspace',str(self.root),'--instance-root',str(self.root),'--input','missing.json'],capture_output=True,text=True)
  self.assertNotEqual(result.returncode,0);self.assertIn('separate maintenance workspace',result.stderr+result.stdout)

if __name__=="__main__":unittest.main(verbosity=2)
