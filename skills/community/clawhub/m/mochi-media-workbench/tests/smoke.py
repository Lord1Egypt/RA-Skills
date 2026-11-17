import csv,hashlib,json,os,shutil,sqlite3,sys,tempfile,unittest,zipfile,uuid
from pathlib import Path
DOMAINS=Path(__file__).resolve().parents[1]/"scripts"
sys.path.insert(0,str(DOMAINS))
import run as media
from io_utils import transaction,digest

class Base(unittest.TestCase):
 def setUp(self):
  self.base=Path(os.environ.get('MOCHI_TEST_ROOT',tempfile.gettempdir()))/('case-'+uuid.uuid4().hex);self.base.mkdir(parents=True);self.ws=self.base/'workspace';self.ws.mkdir();self.seq=0
 def tearDown(self):pass # Retain isolated artifacts as functional-test evidence.
 def execute(self,module,job):
  self.seq+=1;return transaction(self.ws,'test-'+module.__name__,{'requestId':'r'+str(self.seq),**job},module.process)
 def output(self,r,name):return next(self.ws/f['path'] for f in r['files'] if f['path'].endswith('/'+name))
 def csv(self,name,rows,headers=None):
  p=self.ws/name
  with p.open('w',encoding='utf-8-sig',newline='') as f:csv.writer(f).writerows([headers or ['id','date','currency','category','amount','kind'],*rows])
  return p
 def spec(self,name):return {'file':name,'mapping':{k:k for k in ['id','date','currency','category','amount','kind']}}
 def row(self,rid='001',amount='9.90',currency='USD',date='2026-10-01',kind='sale',category='Software'):return [rid,date,currency,category,amount,kind]

class MediaTests(Base):
 def setUp(self):
  super().setUp();self.video=self.ws/'sample.mp4';media.run(['-f','lavfi','-i','testsrc2=size=320x240:rate=25:duration=3','-f','lavfi','-i','sine=frequency=440:sample_rate=16000:duration=3','-c:v','libx264','-pix_fmt','yuv420p','-c:a','aac','-shortest',self.video]);(self.ws/'segments.json').write_text(json.dumps({'segments':[{'start':0,'end':1.5,'text':'Hello 世界'},{'start':1.5,'end':2.8,'text':'Second line'}]},ensure_ascii=False),encoding='utf8')
 def test_actual_probe(self):
  r=self.execute(media,{'file':'sample.mp4'});self.assertAlmostEqual(r['media']['duration'],3,delta=.1);self.assertEqual(len(r['media']['streams']),2)
 def test_audio_extract(self):
  r=self.execute(media,{'file':'sample.mp4','action':'extract-audio'});self.assertEqual(r['outputs'][0]['probe']['streams'][0]['type'],'audio')
 def test_real_clip(self):
  r=self.execute(media,{'file':'sample.mp4','action':'clips','clips':[{'start':.5,'end':2}]});self.assertAlmostEqual(r['outputs'][0]['probe']['duration'],1.5,delta=.15)
 def test_actual_frame(self):
  r=self.execute(media,{'file':'sample.mp4','action':'frames','frames':[.5,2]});from PIL import Image
  with Image.open(self.output(r,'preview.jpg')) as im:self.assertEqual(im.size,(640,210))
 def test_utf8_subtitles(self):
  r=self.execute(media,{'file':'sample.mp4','action':'subtitles','segmentsFile':'segments.json'});self.assertIn('Hello 世界',self.output(r,'subtitles.srt').read_text(encoding='utf8'));self.assertTrue(self.output(r,'subtitles.vtt').read_text().startswith('WEBVTT'))
 def test_clip_subtitle_offset(self):
  r=self.execute(media,{'file':'sample.mp4','action':'package','segmentsFile':'segments.json','clips':[{'start':1,'end':2.5}],'frames':[1]});files=[self.ws/f['path'] for f in r['files'] if f['path'].endswith('clip-01-subtitles/subtitles.srt')];self.assertIn('00:00:00,000 --> 00:00:00,500',files[0].read_text(encoding='utf8'))
 def test_out_of_range_clip(self):self.assertRaises(ValueError,self.execute,media,{'file':'sample.mp4','action':'clips','clips':[{'start':2,'end':8}]})
 def test_missing_segments(self):self.assertRaises(ValueError,self.execute,media,{'file':'sample.mp4','action':'subtitles'})
 def test_unsorted_segments(self):self.assertRaises(ValueError,media.segments_valid,[{'start':2,'end':3,'text':'x'},{'start':0,'end':1,'text':'y'}],4)
 def test_frame_beyond_end(self):self.assertRaises(ValueError,self.execute,media,{'file':'sample.mp4','action':'frames','frames':[30]})
 def test_network_input_rejected(self):self.assertRaises(ValueError,self.execute,media,{'file':'https://example.com/movie.mp4'})
 def test_outputs_decode(self):
  import av
  r=self.execute(media,{'file':'sample.mp4','action':'clips','clips':[{'start':0,'end':1}]});p=self.output(r,'clip-01.mp4')
  with av.open(str(p)) as c:self.assertGreater(sum(1 for _ in c.decode(video=0)),10)
 def test_timestamp_rounding(self):self.assertEqual(media.stamp(59.9998),'00:01:00,000')
 def test_playlist_disguised_as_media_rejected(self):
  (self.ws/'bad.mp4').write_text('#EXTM3U\n#EXT-X-TARGETDURATION:10\n#EXTINF:10,\nhttps://example.com/private.ts\n');self.assertRaises(Exception,self.execute,media,{'file':'bad.mp4'})
 def test_failure_leaves_original_and_no_result(self):
  before=digest(self.video);self.assertRaises(ValueError,self.execute,media,{'file':'sample.mp4','action':'clips','clips':[{'start':2,'end':1}]});self.assertEqual(before,digest(self.video));home=self.ws/'.mochilab'/('test-'+media.__name__);self.assertFalse(list(home.glob('r*.json')))

if __name__=="__main__":unittest.main(verbosity=2)
