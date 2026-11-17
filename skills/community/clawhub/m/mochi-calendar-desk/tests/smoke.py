import datetime as dt,io,json,os,subprocess,tempfile,unittest,zipfile,uuid,sys
from pathlib import Path
from unittest.mock import patch,MagicMock
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from core import *
import calendar_desk as cal

class Base(unittest.TestCase):
    def setUp(self):
        self.root=Path(os.environ.get('MOCHI_TEST_TEMP',tempfile.gettempdir()))/('case-'+uuid.uuid4().hex); self.root.mkdir(); self.st=Store(self.root,'test')
    def tearDown(self): self.st.db.close()
    def file(self,name,data):
        p=self.root/name; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(data if isinstance(data,bytes) else data.encode()); return p

class CalendarTests(Base):
    def fixture(self):
        return b'BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//Test//EN\r\nBEGIN:VEVENT\r\nUID:one\r\nDTSTART:20261024T010000Z\r\nDTEND:20261024T020000Z\r\nRRULE:FREQ=DAILY;COUNT=3\r\nEXDATE:20261025T010000Z\r\nSUMMARY:Daily\r\nEND:VEVENT\r\nEND:VCALENDAR\r\n'
    def test_recurrence_exdate(self):
        cal.store_calendar(self.st,self.fixture(),'test'); rows=cal.range_events(self.st,{'from':'2026-10-24T00:00:00Z','to':'2026-10-28T00:00:00Z'}); self.assertEqual(len(rows),2)
    def test_import_idempotent(self):
        cal.store_calendar(self.st,self.fixture(),'test'); cal.store_calendar(self.st,self.fixture(),'test'); self.assertEqual(len(self.st.all('calendar')),1)
    def test_conflict(self):
        cal.store_calendar(self.st,self.fixture(),'one'); other=self.fixture().replace(b'UID:one',b'UID:two').replace(b'010000Z',b'013000Z'); cal.store_calendar(self.st,other,'two'); out=cal.handle(self.st,{'action':'conflicts','from':'2026-10-24T00:00:00Z','to':'2026-10-25T00:00:00Z'}); self.assertEqual(len(out),1)
    def test_create_utc(self):
        out=cal.handle(self.st,{'action':'create','title':'会议','start':'2026-10-24T09:00:00+08:00','end':'2026-10-24T10:00:00+08:00'}); self.assertEqual(len(cal.parse(Path(out['file']).read_bytes()).walk('VEVENT')),1)
    def test_floating_rejected(self):
        cal.store_calendar(self.st,self.fixture().replace(b'010000Z',b'010000').replace(b'020000Z',b'020000'),'test')
        with self.assertRaises(ValueError): cal.range_events(self.st,{'from':'2026-10-24T00:00:00Z','to':'2026-10-28T00:00:00Z'})

if __name__=="__main__": unittest.main(verbosity=2)
