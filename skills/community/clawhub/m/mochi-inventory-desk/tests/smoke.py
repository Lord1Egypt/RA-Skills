import contextlib,gzip,http.server,json,os,sqlite3,tempfile,threading,unittest,sys
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from core import *
import inventory_desk as stock


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

class StockTests(Base):
 module=stock
 def item(self):self.call(action='item.upsert',sku='A',name='USB cable',currency='CNY',reorderPoint='3',targetStock='10')
 def move(self,id='in1',**kw):return self.call(action='move',id=id,sku='A',**kw)
 def test_decimal_valuation(self):self.item();self.move(kind='in',quantity='3',unitCost='0.10');v=self.call(action='stock');self.assertEqual(v['valueByCurrency'],{'CNY':'0.30'})
 def test_idempotent(self):self.item();self.move(kind='in',quantity='3',unitCost='1');r=self.move(kind='in',quantity='3',unitCost='1');self.assertTrue(r['replayed']);self.assertEqual(self.call(action='stock')['stock'][0]['quantity'],'3')
 def test_conflicting_id(self):
  self.item();self.move(kind='in',quantity='3',unitCost='1')
  with self.assertRaises(ValueError):self.move(kind='in',quantity='4',unitCost='1')
 def test_insufficient(self):
  self.item()
  with self.assertRaises(ValueError):self.move(kind='out',quantity='1')
 def test_weighted_average(self):self.item();self.move(kind='in',quantity='2',unitCost='10');self.move('in2',kind='in',quantity='2',unitCost='20');self.move('out1',kind='out',quantity='1');v=self.call(action='stock')['stock'][0];self.assertEqual(v['quantity'],'3');self.assertEqual(v['stockValue'],'45.00')
 def test_reorder(self):self.item();self.move(kind='in',quantity='2',unitCost='1');v=self.call(action='stock')['stock'][0];self.assertTrue(v['lowStock']);self.assertEqual(v['suggestedReorder'],'8')
 def test_adjust_reason(self):
  self.item()
  with self.assertRaises(ValueError):self.move(kind='adjust',quantity='5',unitCost='1')
 def test_currency_separate(self):self.item();self.call(action='item.upsert',sku='B',name='Other',currency='USD');self.move(kind='in',quantity='2',unitCost='1');self.call(action='move',id='b1',sku='B',kind='in',quantity='1',unitCost='3');self.assertEqual(self.call(action='stock')['valueByCurrency'],{'CNY':'2.00','USD':'3.00'})
 def test_unstocked_reorder(self):self.item();v=self.call(action='stock');self.assertEqual(v['stock'][0]['quantity'],'0');self.assertTrue(v['stock'][0]['lowStock']);self.assertEqual(v['unstockedSKUs'],['A'])
 def test_unit_change_guard(self):
  self.item();self.move(kind='in',quantity='1',unitCost='2')
  with self.assertRaises(ValueError):self.call(action='item.upsert',sku='A',unit='kg')
 def test_high_precision_cost(self):self.item();self.move(kind='in',quantity='1000000000000',unitCost='1000000000000');self.assertEqual(self.call(action='stock')['valueByCurrency']['CNY'],'1000000000000000000000000.00')

if __name__=="__main__": unittest.main(verbosity=2)
