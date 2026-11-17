import datetime as dt,io,json,os,subprocess,tempfile,unittest,zipfile,uuid,sys
from pathlib import Path
from unittest.mock import patch,MagicMock
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from core import *
import feed_hub as feeds

class Base(unittest.TestCase):
    def setUp(self):
        self.root=Path(os.environ.get('MOCHI_TEST_TEMP',tempfile.gettempdir()))/('case-'+uuid.uuid4().hex); self.root.mkdir(); self.st=Store(self.root,'test')
    def tearDown(self): self.st.db.close()
    def file(self,name,data):
        p=self.root/name; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(data if isinstance(data,bytes) else data.encode()); return p

class FeedTests(Base):
    def raw(self): return b'<rss version="2.0"><channel><title>Demo</title><item><guid>one</guid><title>News</title><link>https://example.com/1</link></item></channel></rss>'
    def test_rss_idempotent(self):
        feeds.ingest(self.st,'demo',self.raw()); feeds.ingest(self.st,'demo',self.raw()); self.assertEqual(len(self.st.all('item')),1); self.assertEqual(len(self.st.pending()),1)
    def test_atom(self):
        raw=b'<feed xmlns="http://www.w3.org/2005/Atom"><title>Test</title><entry><id>one</id><title>Atom</title><link href="https://example.com/"/></entry></feed>'; self.assertEqual(feeds.parse_feed(raw)['entries'][0]['title'],'Atom')
    def test_read_state_survives_update(self):
        feeds.ingest(self.st,'demo',self.raw()); id=self.st.all('item')[0]['id']; feeds.handle(self.st,{'action':'mark','ids':[id]}); feeds.ingest(self.st,'demo',self.raw()); self.assertTrue(self.st.get('item',id)['read'])
    def test_opml_roundtrip(self):
        feeds.handle(self.st,{'action':'add','url':'https://example.com/feed'}); out=feeds.handle(self.st,{'action':'opml-export'}); feeds.handle(self.st,{'action':'opml-import','file':str(Path(out['file']).relative_to(self.root))}); self.assertEqual(len(self.st.all('feed')),1)
    def test_entities_rejected(self):
        with self.assertRaises(ValueError): feeds.parse_feed(b'<!DOCTYPE foo [<!ENTITY x SYSTEM "file:///secret">]><rss/>')

if __name__=="__main__": unittest.main(verbosity=2)
