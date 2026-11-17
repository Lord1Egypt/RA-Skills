import unittest,tempfile,json,sys,zipfile,io,datetime as dt
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from core import Store,local,readbytes,csvbytes
import github_triage

class Base(unittest.TestCase):
 def setUp(self):self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name);self.s=Store(self.root,'test')
 def tearDown(self):self.s.db.close();self.temp.cleanup()
 def put(self,name,value):
  p=self.root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(value if isinstance(value,str) else json.dumps(value,ensure_ascii=False),encoding='utf-8');return name
 def zip(self,name,items):
  p=self.root/name
  with zipfile.ZipFile(p,'w') as z:
   for k,v in items.items():z.writestr(k,v)
  return name
 def report(self,result):
  self.assertTrue(all((self.root/x).is_file() for x in result['files']));return result['report']

class CoreTests(Base):
 def test_parent(self):
  with self.assertRaises(ValueError):local(self.root,'../secret')
 def test_absolute(self):
  with self.assertRaises(ValueError):local(self.root,str(self.root/'outside'))
 def test_windows_absolute(self):
  with self.assertRaises(ValueError):local(self.root,'C:\\private\\secret')
 def test_unc(self):
  with self.assertRaises(ValueError):local(self.root,'\\\\host\\share')
 def test_csv_formula(self):self.assertIn("'=1+1",csvbytes(['x'],[{'x':'=1+1'}]).decode('utf-8-sig'))
 def test_source_preserved(self):
  self.put('input.txt','Original');self.s.report({'ok':True});self.assertEqual((self.root/'input.txt').read_text(),'Original')
 def test_reports_unique(self):self.assertNotEqual(self.s.report({})['directory'],self.s.report({})['directory'])

class GithubTests(Base):
 def row(self):return {'number':1,'title':'Fix a login bug','url':'https://github.com/example/demo/issues/1','updatedAt':'2026-09-01T00:00:00Z','state':'OPEN','labels':[{'name':'bug'}],'assignees':[]}
 def runrows(self,rows):self.put('issues.json',rows);return self.report(github_triage.handle(self.s,{'action':'triage','file':'issues.json','asOf':'2026-10-26T00:00:00Z'}))
 def test_triage(self):d=self.runrows([self.row()]);self.assertTrue(d['issues'][0]['needsTriage']);self.assertFalse(d['remoteChanges'])
 def test_closed(self):r=self.row();r['state']='CLOSED';self.assertFalse(self.runrows([r])['issues'][0]['needsTriage'])
 def test_duplicates(self):a=self.row();b=dict(a,number=2,url='https://github.com/example/demo/issues/2');self.assertEqual(len(self.runrows([a,b])['possibleDuplicates']),1)
 def test_same_number(self):
  with self.assertRaises(ValueError):self.runrows([self.row(),self.row()])
 def test_wrong_host(self):
  r=self.row();r['url']='https://evil.example/issues/1'
  with self.assertRaises(ValueError):self.runrows([r])

if __name__=="__main__":unittest.main(verbosity=2)
