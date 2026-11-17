import datetime as dt,io,json,os,subprocess,tempfile,unittest,zipfile,uuid,sys
from pathlib import Path
from unittest.mock import patch,MagicMock
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from core import *
import important_dates as dates

class Base(unittest.TestCase):
    def setUp(self):
        self.root=Path(os.environ.get('MOCHI_TEST_TEMP',tempfile.gettempdir()))/('case-'+uuid.uuid4().hex); self.root.mkdir(); self.st=Store(self.root,'test')
    def tearDown(self): self.st.db.close()
    def file(self,name,data):
        p=self.root/name; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(data if isinstance(data,bytes) else data.encode()); return p

class DateTests(Base):
    def event(self,**extra): return {'id':'birthday','title':'生日','month':2,'day':29,**extra}
    def test_feb29_policies(self):
        self.assertEqual(str(dates.occurrence(self.event(),2027)),'2027-02-28'); self.assertEqual(str(dates.occurrence(self.event(feb29='mar1'),2027)),'2027-03-01'); self.assertIsNone(dates.occurrence(self.event(feb29='skip'),2027))
    def test_lunar_newyear(self): self.assertEqual(str(dates.occurrence(self.event(calendar='lunar',month=1,day=1),2026)),'2026-02-17')
    def test_lunar_leap_policy(self):
        e=self.event(calendar='lunar',month=2,day=1,leapMonth=True); self.assertIsNone(dates.occurrence(e,2026)); self.assertEqual(str(dates.occurrence({**e,'leapPolicy':'regular'},2026)),'2026-03-19')
    def test_lunar_short_month_policy(self):
        from lunar_python import LunarMonth
        month=next(m for m in range(1,13) if LunarMonth.fromYm(2026,m).getDayCount()==29); e=self.event(calendar='lunar',month=month,day=30)
        self.assertEqual(dates.occurrence(e,2026),dates.occurrence({**e,'day':29},2026)); self.assertIsNone(dates.occurrence({**e,'lunarShortMonth':'skip'},2026))
    def test_dst_gap(self): self.assertEqual(dates.wall(dt.date(2026,3,8),'02:30','America/New_York').hour,3)
    def test_dst_fold(self): self.assertEqual(dates.wall(dt.date(2026,11,1),'01:30','America/New_York').fold,0)
    def test_notifications_retry_ack(self):
        dates.handle(self.st,{'action':'put','event':self.event(month=10,day=24,advanceDays=[0])}); r={'action':'poll','now':'2026-10-24T09:05:00+08:00'}
        a=dates.handle(self.st,r); b=dates.handle(self.st,r); self.assertEqual(len(a['notifications']),1); self.assertEqual(a,b); self.st.ack([a['notifications'][0]['noticeId']]); self.assertEqual(dates.handle(self.st,r)['notifications'],[])
    def test_revision_clears_stale(self):
        e=self.event(month=10,day=24,advanceDays=[0]); dates.handle(self.st,{'action':'put','event':e}); dates.handle(self.st,{'action':'poll','now':'2026-10-24T09:05:00+08:00'}); dates.handle(self.st,{'action':'put','event':{**e,'day':25}}); self.assertEqual(self.st.pending(),[])
    def test_unknown_age(self):
        dates.handle(self.st,{'action':'put','event':self.event(month=10,day=24)}); result=dates.handle(self.st,{'action':'upcoming','from':'2026-10-23','days':3}); self.assertNotIn('years',result[0])
    def test_holiday_year_and_source(self):
        self.file('holidays.json',json.dumps({'country':'test','year':2026,'source':'https://example.test/official','days':[{'date':'2026-10-24','name':'Example','type':'workday'}]})); result=dates.handle(self.st,{'action':'import-holidays','file':'holidays.json'}); self.assertEqual(result['imported'],1); self.assertEqual(self.st.all('event')[0]['kind'],'workday')
    def test_ics_export(self):
        dates.handle(self.st,{'action':'put','event':self.event()}); out=dates.handle(self.st,{'action':'export-ics','from':'2026-01-01','to':'2026-12-31'}); self.assertIn(b'20260228',Path(out['file']).read_bytes())

if __name__=="__main__": unittest.main(verbosity=2)
