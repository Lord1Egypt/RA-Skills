import unittest,tempfile,json,sys,zipfile,io,datetime as dt
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from core import Store,local,readbytes,csvbytes
import research_dossier

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

class ResearchTests(Base):
 def fixture(self):return {'sources':[{'id':'s1','url':'https://example.com/a?utm_source=x','title':'Source','text':'Exact evidence line','accessedAt':'2026-10-26T00:00:00Z'}],'claims':[{'id':'c1','claim':'Statement','sources':['s1'],'status':'supported','quote':'Exact evidence'}]}
 def runrow(self,d):self.put('research.json',d);return self.report(research_dossier.handle(self.s,{'action':'build','file':'research.json'}))
 def test_quote(self):self.assertTrue(self.runrow(self.fixture())['claims'][0]['quoteVerifiedInProvidedText'])
 def test_noquote(self):
  d=self.fixture();d['claims'][0]['quote']='Not in source'
  with self.assertRaises(ValueError):self.runrow(d)
 def test_unknown(self):
  d=self.fixture();d['claims'][0]['sources']=['missing']
  with self.assertRaises(ValueError):self.runrow(d)
 def test_unverified(self):d=self.fixture();d['claims']=[{'id':'c1','claim':'Unknown'}];self.assertEqual(self.runrow(d)['unverifiedClaims'],1)
 def test_canonical(self):d=self.runrow(self.fixture());self.assertNotIn('utm_',d['sources'][0]['url'])

if __name__=="__main__":unittest.main(verbosity=2)
