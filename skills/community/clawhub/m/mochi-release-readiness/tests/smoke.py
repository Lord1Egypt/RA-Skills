import copy,itertools,json,os,shutil,subprocess,sys,tempfile,unittest,zipfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from runtime import Store
from task import handle
BASE=Path(__file__).resolve().parents[1]
CASE=json.loads((BASE/'tests/case.json').read_text(encoding='utf-8'))
class SkillCases(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory(prefix='mochi40-test-');self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)/'workspace';self.root.mkdir();shutil.copytree(BASE/'samples',self.root/'samples');self.store=Store(self.root)
 def test_domain_positive(self):
  result=handle(copy.deepcopy(CASE['sample']),self.store)
  for key,value in CASE['expected'].items():self.assertEqual(result[key],value,key)
  if CASE['mode']=='calendar_availability':self.assertEqual(sum(x['minutes'] for x in result['available']),120)
  if CASE['mode']=='test_matrix':
   factors=CASE['sample']['factors'];keys=sorted(factors)
   for a,b in itertools.combinations(keys,2):self.assertEqual({(x[a],x[b]) for x in result['cases']},set(itertools.product(factors[a],factors[b])))
  if CASE['mode']=='context_pack':
   self.assertLessEqual(len((self.root/self.store.artifacts[0]['path']).read_text(encoding='utf-8')),CASE['sample']['maxChars'])
  if CASE['mode']=='docx_review_map':
   self.assertEqual(result['commentAnchors'],[{'id':'1','paragraph':1}]);self.assertEqual(result['missingCommentDefinitions'],[]);self.assertEqual({x['kind'] for x in result['revisions']},{'insert','delete'})
 def test_invalid_domain_input(self):
  with self.assertRaises((ValueError,KeyError,TypeError,OSError,zipfile.BadZipFile)):handle(copy.deepcopy(CASE['invalid']),self.store)
 def test_cli_new_artifacts_and_source_preserved(self):
  p=self.root/'request.json';raw=json.dumps(CASE['sample'],ensure_ascii=False).encode();p.write_bytes(raw)
  done=subprocess.run([sys.executable,'-B',str(BASE/'scripts/run.py'),'--workspace',str(self.root),'--input','request.json'],capture_output=True,timeout=45,cwd=self.root)
  self.assertEqual(done.returncode,0,done.stderr.decode(errors='replace')+done.stdout.decode(errors='replace'));value=json.loads(done.stdout);self.assertIs(value['ok'],True);self.assertEqual(p.read_bytes(),raw)
  for item in value['artifacts']:self.assertTrue((self.root/item['path']).is_file());self.assertTrue((self.root/item['path']).resolve().is_relative_to(self.root.resolve()))
 def test_parent_and_absolute_paths_rejected(self):
  for value in ['../outside.txt',str(self.root.parent/'outside.txt')]:
   with self.assertRaises(ValueError):self.store.path(value)
 def test_output_never_overwrites_existing_file(self):
  name=self.store.emit('same.txt','first')
  with self.assertRaises(FileExistsError):self.store.emit('same.txt','second')
  self.assertEqual((self.root/name).read_text(),'first')
if __name__=='__main__':unittest.main(verbosity=2)
