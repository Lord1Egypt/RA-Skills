"""Local media preparation, bounded transcription cache, subtitles and clips."""
import hashlib,html,json,math,os,re,shutil,subprocess,uuid
from pathlib import Path
from io_utils import require,read_file,safe,source,write_json,digest,archive,cli

def number(v,name,lo=0,hi=14400):
 require(type(v) in [int,float] and math.isfinite(v) and lo<=v<=hi,name+' outside supported range');return float(v)

def ffmpeg():
 found=shutil.which('ffmpeg')
 if found:return found
 try:
  import imageio_ffmpeg
  return imageio_ffmpeg.get_ffmpeg_exe()
 except ImportError:raise ValueError('Install FFmpeg or imageio-ffmpeg locally')

def run(args,timeout=1800):
 args=list(args)
 if '-protocol_whitelist' in args:
  idx=args.index('-i');args[idx:idx]=['-format_whitelist','mov,mp4,m4a,3gp,3g2,mj2,matroska,webm,mp3,wav,flac,ogg,aac']
 p=subprocess.run([ffmpeg(),'-hide_banner','-nostdin','-loglevel','error','-n',*map(str,args)],stdin=subprocess.DEVNULL,capture_output=True,timeout=timeout)
 require(p.returncode==0,'FFmpeg failed: '+p.stderr.decode('utf8','replace')[-1200:]);return p

def probe(p):
 import av
 with av.open(str(p),options={'protocol_whitelist':'file,pipe','format_whitelist':'mov,mp4,m4a,3gp,3g2,mj2,matroska,webm,mp3,wav,flac,ogg,aac'}) as c:
  streams=[{'index':s.index,'type':s.type,'codec':s.codec_context.name,'duration':float(s.duration*s.time_base) if s.duration is not None and s.time_base else None} for s in c.streams]
  duration=float(c.duration/av.time_base) if c.duration is not None else max([s['duration'] or 0 for s in streams]+[0]);require(0<duration<=14400,'Media duration must be known and <=4 hours')
  return {'duration':duration,'streams':streams,'format':c.format.name}

def stamp(t,sep=','):
 ms=round(t*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000);return f'{h:02}:{m:02}:{s:02}{sep}{ms:03}'

def segments_valid(rows,duration):
 require(isinstance(rows,list) and len(rows)<=30000,'Provide <=30000 subtitle segments');last=-1
 result=[]
 for r in rows:
  require(isinstance(r,dict),'Segment must be an object');start=number(r.get('start'),'subtitle start',0,duration);end=number(r.get('end'),'subtitle end',0,duration)
  txt=r.get('text');require(start<end and start>=last,'Subtitle start must be sorted and end > start');require(isinstance(txt,str) and 0<len(txt.strip())<=5000 and '-->' not in txt,'Invalid subtitle text');last=start;result.append({'start':start,'end':end,'text':txt.strip()})
 return result

def subtitles(out,rows):
 srt='\n\n'.join(str(i)+'\n'+stamp(r['start'])+' --> '+stamp(r['end'])+'\n'+r['text'] for i,r in enumerate(rows,1))+'\n'
 vtt='WEBVTT\n\n'+'\n\n'.join(stamp(r['start'],'.')+' --> '+stamp(r['end'],'.')+'\n'+r['text'] for r in rows)+'\n'
 (out/'subtitles.srt').write_text(srt,encoding='utf8');(out/'subtitles.vtt').write_text(vtt,encoding='utf8');write_json(out/'transcript.json',{'segments':rows})
 (out/'transcript.md').write_text('# Transcript\n\n'+'\n\n'.join('['+stamp(r['start'],'.')+'] '+r['text'] for r in rows)+'\n',encoding='utf8')

def process(ws,j,out):
 p=read_file(ws,j.get('file'),1024*1024*1024);require(p.suffix.lower() in ['.mp4','.mkv','.mov','.webm','.mp3','.wav','.m4a','.flac','.ogg','.aac'],'Use a supported local media file')
 info=probe(p);duration=info['duration'];action=j.get('action','inspect');require(action in ['inspect','extract-audio','clips','frames','subtitles','transcribe','package'],'Unknown action')
 sources=[source(ws,p)];video=any(s['type']=='video' for s in info['streams']);audio=any(s['type']=='audio' for s in info['streams']);outputs=[];rows=[];origin=None
 if action in ['extract-audio','transcribe'] or action=='package' and j.get('extractAudio',False):
  require(audio,'No audio stream');dest=out/'audio.wav';run(['-protocol_whitelist','file,pipe','-i',p,'-vn','-map','0:a:0','-ac',1,'-ar',16000,'-c:a','pcm_s16le',dest]);outputs.append({'file':dest.name,'probe':probe(dest)})
 if action=='transcribe':
  from faster_whisper import WhisperModel
  model_name=j.get('model','tiny');require(model_name in ['tiny','base','small'],'model: tiny, base or small');require(type(j.get('allowModelDownload',False)) is bool,'allowModelDownload must be boolean')
  threads=j.get('threads',2);require(type(threads) is int and 1<=threads<=8,'threads: 1..8');chunk=300
  lang=j.get('language');require(lang is None or isinstance(lang,str) and re.fullmatch('[a-z]{2,3}',lang),'Use a language code such as zh/en')
  cache=safe(ws,'.mochilab/mochi-media-workbench/transcription-cache',False);cache.mkdir(parents=True,exist_ok=True)
  model_root=safe(ws,'.mochilab/mochi-media-workbench/models',False);model_root.mkdir(parents=True,exist_ok=True)
  model_fingerprint=model_name;model_ref=model_name
  if j.get('modelPath'):
   folder=safe(ws,j['modelPath']);require(folder.is_dir(),'modelPath must be a local converted Whisper model directory');model_ref=str(folder)
   hashes=[]
   for name in ['model.bin','config.json','tokenizer.json','vocabulary.txt']:
    model_file=read_file(ws,str(folder/name),750*1024*1024);sources.append(source(ws,model_file));hashes.append(digest(model_file))
   model_fingerprint=hashlib.sha256(''.join(hashes).encode()).hexdigest()
  model=WhisperModel(model_ref,device='cpu',compute_type='int8',cpu_threads=threads,download_root=str(model_root),local_files_only=not j.get('allowModelDownload',False))
  cachekey=hashlib.sha256(json.dumps({'source':sources[0]['sha256'],'model':model_fingerprint,'language':lang,'engine':__import__('faster_whisper').__version__,'chunkSeconds':chunk,'decoder':'beam1-v1'},sort_keys=True).encode()).hexdigest()
  segments=[];reused=0
  for index,start in enumerate(range(0,math.ceil(duration),chunk)):
   end=min(start+chunk,duration);part=safe(ws,str(cache/(cachekey+'-'+str(index)+'.json')),False)
   if part.exists():
    stored=json.loads(part.read_text(encoding='utf8'));require(stored['key']==cachekey and stored['start']==start,'Invalid transcription cache');seg=segments_valid(stored['segments'],end-start);reused+=1
   else:
    wav=out/('chunk-'+str(index)+'.wav');run(['-ss',start,'-protocol_whitelist','file,pipe','-i',p,'-t',end-start,'-vn','-ac',1,'-ar',16000,wav]);generator,meta=model.transcribe(str(wav),language=lang,beam_size=1,condition_on_previous_text=False,vad_filter=False)
    seg=segments_valid([{'start':max(0,float(s.start)),'end':min(end-start,float(s.end)),'text':s.text} for s in generator if s.text.strip() and s.end>s.start],end-start)
    temp=cache/('.'+uuid.uuid4().hex);write_json(temp,{'key':cachekey,'start':start,'segments':seg});os.replace(temp,part);wav.unlink()
   segments.extend({**s,'start':s['start']+start,'end':s['end']+start} for s in seg)
  rows=segments_valid(segments,duration);origin={'type':'local-asr','model':model_name,'engine':'faster-whisper','cachedChunksReused':reused,'transcriptionNeedsReview':True};subtitles(out,rows)
 elif action in ['subtitles','package'] and j.get('segmentsFile'):
  f=read_file(ws,j['segmentsFile'],5*1024*1024);data=json.loads(f.read_text(encoding='utf-8-sig'));rows=segments_valid(data.get('segments') if isinstance(data,dict) else data,duration);sources.append(source(ws,f));origin={'type':'user-provided-segments'};subtitles(out,rows)
 elif action=='subtitles':raise ValueError('Provide segmentsFile containing timestamped segments')
 if action in ['clips','package']:
  clips=j.get('clips',[]);require(isinstance(clips,list) and len(clips)<=20 and (clips or action=='package'),'Provide 1..20 clips')
  for n,c in enumerate(clips,1):
   a=number(c.get('start'),'clip start',0,duration);b=number(c.get('end'),'clip end',0,duration);require(a<b,'clip end must exceed start');dest=out/(f'clip-{n:02}'+('.mp4' if video else '.wav'))
   opts=['-map','0:v:0','-map','0:a:0?','-c:v','libx264','-preset','fast','-crf','23','-pix_fmt','yuv420p','-c:a','aac','-movflags','+faststart'] if video else ['-vn','-c:a','pcm_s16le']
   run(['-protocol_whitelist','file,pipe','-i',p,'-ss',a,'-t',b-a,*opts,dest]);actual=probe(dest);require(abs(actual['duration']-(b-a))<=0.35,'Clip duration verification failed');outputs.append({'file':dest.name,'requestedStart':a,'requestedEnd':b,'probe':actual})
   if rows:
    clipped=[{'start':max(a,r['start'])-a,'end':min(b,r['end'])-a,'text':r['text']} for r in rows if r['end']>a and r['start']<b];subdir=out/f'clip-{n:02}-subtitles';subdir.mkdir();subtitles(subdir,clipped)
 if action in ['frames','package']:
  times=j.get('frames',[]);require(video,'Frames require a video stream');require(isinstance(times,list) and len(times)<=40 and (times or action=='package'),'Provide 1..40 frame timestamps')
  for n,t in enumerate(times,1):
   t=number(t,'frame timestamp',0,max(0,duration-.05));dest=out/f'frame-{n:02}.jpg';run(['-protocol_whitelist','file,pipe','-i',p,'-ss',t,'-frames:v',1,'-vf','scale=640:-2','-q:v',3,dest]);require(dest.exists() and dest.stat().st_size>0,'Frame extraction produced no image');outputs.append({'file':dest.name,'timestamp':t})
  if times:
   from PIL import Image,ImageDraw
   sheet=Image.new('RGB',(640,210*math.ceil(len(times)/2)),'#eeeeee')
   for n,t in enumerate(times):
    with Image.open(out/f'frame-{n+1:02}.jpg') as im:im.thumbnail((310,175));sheet.paste(im,((n%2)*320+5,(n//2)*210+5))
    ImageDraw.Draw(sheet).text(((n%2)*320+8,(n//2)*210+185),stamp(t,'.'),fill='black')
   sheet.save(out/'preview.jpg',quality=88)
 report={'action':action,'media':info,'outputs':outputs,'subtitleSegments':len(rows),'transcriptOrigin':origin,'sources':sources,'originalsModified':False};write_json(out/'manifest.json',report)
 if action=='package':archive(out,'results.zip',[f for f in sorted(out.rglob('*')) if f.is_file()])
 return report

if __name__=='__main__':cli('mochi-media-workbench',process)
