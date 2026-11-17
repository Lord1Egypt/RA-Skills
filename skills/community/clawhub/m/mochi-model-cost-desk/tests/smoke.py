import unittest,tempfile,json,sys,zipfile,io,datetime as dt
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from core import Store,local,readbytes,csvbytes
import model_costs

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

class CostTests(Base):
 def request(self):return {'action':'estimate','file':'usage.csv','ratesAsOf':'2026-10-26','rates':[{'model':'demo','currency':'USD','inputPerMillion':'2','cachedInputPerMillion':'.2','outputPerMillion':'8'}]}
 def csv(self,line='demo,1000000,100000,100000'):self.put('usage.csv','model,input_tokens,cached_input_tokens,output_tokens\n'+line+'\n')
 def test_calculation(self):self.csv();d=self.report(model_costs.handle(self.s,self.request()));self.assertEqual(float(d['totals'][0]['estimatedCost']),2.62)
 def test_budget(self):self.csv();r=self.request();r['budget']={'USD':'2'};self.assertTrue(self.report(model_costs.handle(self.s,r))['budgetChecks'][0]['exceeded'])
 def test_cache(self):
  self.csv('demo,1,2,0')
  with self.assertRaises(ValueError):model_costs.handle(self.s,self.request())
 def test_negative(self):
  self.csv('demo,-1,0,0')
  with self.assertRaises(ValueError):model_costs.handle(self.s,self.request())
 def test_rates(self):
  self.csv('unknown,1,0,0')
  with self.assertRaises(ValueError):model_costs.handle(self.s,self.request())

if __name__=="__main__":unittest.main(verbosity=2)
