import unittest,tempfile,json,sys,zipfile,io,datetime as dt
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from core import Store,local,readbytes,csvbytes
import weather_desk

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

class WeatherTests(Base):
 def fixture(self):return {'timezone':'Asia/Shanghai','daily_units':{'temperature_2m_max':'°C'},'daily':{'time':['2026-10-26'],'temperature_2m_max':[22],'temperature_2m_min':[15],'precipitation_probability_max':[30],'wind_speed_10m_max':[12]}}
 def test_import(self):self.put('weather.json',self.fixture());self.assertEqual(len(self.report(weather_desk.handle(self.s,{'action':'import','file':'weather.json'}))['forecast']),1)
 def test_network_optin(self):
  with self.assertRaises(ValueError):weather_desk.handle(self.s,{'action':'fetch','latitude':0,'longitude':0})
 def test_bad_coordinates(self):
  with self.assertRaises(ValueError):weather_desk.handle(self.s,{'action':'fetch','network':True,'latitude':91,'longitude':0})
 def test_alignment(self):
  d=self.fixture();d['daily']['time'].append('2026-10-27')
  with self.assertRaises(ValueError):weather_desk.summarize(d)
 def test_fetch_mock(self):
  with patch.object(weather_desk,'safe_request',return_value={'status':200,'body':json.dumps(self.fixture()).encode()}) as p:
   d=self.report(weather_desk.handle(self.s,{'action':'fetch','network':True,'latitude':52.52,'longitude':13.41}));self.assertEqual(d['mode'],'live-provider-response');self.assertTrue(p.call_args.args[0].startswith('https://api.open-meteo.com/v1/forecast?'))

if __name__=="__main__":unittest.main(verbosity=2)
