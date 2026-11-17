import unittest,subprocess,sys,json,uuid,shutil,hashlib,os
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
class Smoke(unittest.TestCase):
 def setUp(self):
  root=Path(os.environ.get('MOCHI_TEST_WORK',str(Path.cwd()/'.mochi-package-tests')));self.w=root/('sample space '+str(uuid.uuid4()));self.w.mkdir(parents=True);shutil.copytree(BASE/'samples',self.w/'samples');self.job=json.loads((self.w/'samples/request.json').read_text(encoding='utf8'))
 def call(self):
  (self.w/'input.json').write_text(json.dumps(self.job),encoding='utf8');return subprocess.run([sys.executable,str(BASE/'scripts/run.py'),'--workspace',str(self.w),'--input','input.json'],capture_output=True,text=True,encoding='utf8')
 def test_sample_cli_creates_verifiable_files(self):
  p=self.call();self.assertEqual(p.returncode,0,p.stderr);r=json.loads(p.stdout)
  for f in r['files']:
   data=(self.w/f['path']).read_bytes();self.assertEqual(len(data),f['bytes']);self.assertEqual(hashlib.sha256(data).hexdigest(),f['sha256'])
 def test_retry_reuses_output(self):
  p=self.call();self.assertEqual(p.returncode,0,p.stderr);r=json.loads(p.stdout);again=json.loads(self.call().stdout);self.assertTrue(again['replayed']);self.assertEqual(r['files'],again['files'])
 def test_changed_input_cannot_reuse_request_id(self):
  p=self.call();self.assertEqual(p.returncode,0,p.stderr);self.job['extraForTest']=True;p=self.call();self.assertNotEqual(p.returncode,0);self.assertIn('different input',p.stderr)
 def test_invalid_input_is_structured_error(self):
  self.job['requestId']='../invalid';p=self.call();self.assertNotEqual(p.returncode,0);self.assertFalse(json.loads(p.stderr)['ok'])
if __name__=='__main__':unittest.main(verbosity=2)
