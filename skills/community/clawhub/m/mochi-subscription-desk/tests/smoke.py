import datetime as dt,io,json,os,subprocess,tempfile,unittest,zipfile,uuid,sys
from pathlib import Path
from unittest.mock import patch,MagicMock
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from core import *
import subscription_desk as bills

class Base(unittest.TestCase):
    def setUp(self):
        self.root=Path(os.environ.get('MOCHI_TEST_TEMP',tempfile.gettempdir()))/('case-'+uuid.uuid4().hex); self.root.mkdir(); self.st=Store(self.root,'test')
    def tearDown(self): self.st.db.close()
    def file(self,name,data):
        p=self.root/name; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(data if isinstance(data,bytes) else data.encode()); return p

class BillTests(Base):
    def plan(self,**extra): return {'id':'one','title':'Plan','start':'2026-01-31','amount':'9.90','currency':'USD',**extra}
    def test_month_anchor(self):
        p=self.plan(); self.assertEqual(str(bills.due(p,1)),'2026-02-28'); self.assertEqual(str(bills.due(p,2)),'2026-03-31')
    def test_leap_year_anchor(self):
        p=self.plan(start='2024-02-29',unit='year'); self.assertEqual(str(bills.due(p,1)),'2025-02-28'); self.assertEqual(str(bills.due(p,4)),'2028-02-29')
    def test_currency_separation_decimal(self):
        for id,c in [('a','USD'),('b','CNY')]: bills.handle(self.st,{'action':'put','subscription':self.plan(id=id,currency=c)})
        result=bills.handle(self.st,{'action':'forecast','from':'2026-01-01','to':'2026-03-31'}); self.assertEqual(result['totals'],{'USD':'29.70','CNY':'29.70'})
    def test_cancel_deadline_notice_once(self):
        bills.handle(self.st,{'action':'put','subscription':self.plan(cancelLeadDays=10)}); r={'action':'poll','date':'2026-01-20','advanceDays':2}; a=bills.handle(self.st,r); bills.handle(self.st,r); self.assertEqual(len(a['notifications']),1); self.assertEqual(len(self.st.pending()),1); self.assertEqual(a['notifications'][0]['type'],'cancel-deadline')
    def test_nonfinite_rejected(self):
        with self.assertRaises(ValueError): bills.validate(self.plan(amount='NaN'))
    def test_edit_retires_stale_notice(self):
        bills.handle(self.st,{'action':'put','subscription':self.plan()}); r={'action':'poll','date':'2026-01-31','advanceDays':0}; bills.handle(self.st,r); bills.handle(self.st,{'action':'put','subscription':self.plan(amount='12.00')}); out=bills.handle(self.st,r); self.assertEqual(len(out['notifications']),2); self.assertTrue(all(n['amount']=='12.00' for n in out['notifications']))

if __name__=="__main__": unittest.main(verbosity=2)
