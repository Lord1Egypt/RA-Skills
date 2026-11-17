"""Read-only ffprobe assertions, optionally full ffmpeg decode. Requires existing tools."""
import argparse
import json
import math
import os
from pathlib import Path
import subprocess
import tempfile


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('path',type=Path)
    p.add_argument('--ffprobe',default='ffprobe')
    p.add_argument('--ffmpeg',default='ffmpeg')
    p.add_argument('--min-duration',type=float,required=True)
    p.add_argument('--max-duration',type=float,required=True)
    p.add_argument('--require-audio',action='store_true')
    p.add_argument('--require-video',action='store_true')
    p.add_argument('--width',type=int)
    p.add_argument('--height',type=int)
    p.add_argument('--decode',action='store_true')
    p.add_argument('--decode-timeout',type=float,default=240)
    a=p.parse_args()
    try:
        if not 0<=a.min_duration<=a.max_duration or not math.isfinite(a.max_duration):
            raise ValueError('Invalid duration interval')
        if not .1<=a.decode_timeout<=2592000:
            raise ValueError('Invalid decode timeout')
        with tempfile.TemporaryFile() as output:
            proc=subprocess.run([a.ffprobe,'-v','error','-show_entries','format=duration:stream=codec_type,width,height',
                                 '-of','json',str(a.path.resolve())],stdin=subprocess.DEVNULL,stdout=output,timeout=30)
            if proc.returncode!=0:
                raise ValueError('ffprobe exited '+str(proc.returncode))
            if output.tell()>1048576:
                raise ValueError('ffprobe metadata exceeds 1 MiB')
            output.seek(0)
            data=json.load(output)
        duration=float(data.get('format',{}).get('duration','nan'))
        if not a.min_duration<=duration<=a.max_duration:
            raise ValueError('Duration outside expected interval: '+str(duration))
        streams=data.get('streams',[])
        video=[s for s in streams if s.get('codec_type')=='video']
        audio=[s for s in streams if s.get('codec_type')=='audio']
        if (a.require_video or a.width or a.height) and not video or a.require_audio and not audio:
            raise ValueError('Required audio/video stream missing')
        if a.width and any(s.get('width')!=a.width for s in video) or a.height and any(s.get('height')!=a.height for s in video):
            raise ValueError('Video dimensions mismatch')
        if a.decode:
            proc=subprocess.run([a.ffmpeg,'-nostdin','-v','error','-xerror','-i',str(a.path.resolve()),'-f','null',os.devnull],
                                stdin=subprocess.DEVNULL,timeout=a.decode_timeout)
            if proc.returncode!=0:
                raise ValueError('Decode failed: '+str(proc.returncode))
        print(json.dumps({'ok':True,'duration':duration,'video_streams':len(video),'audio_streams':len(audio),'full_decode':a.decode}))
        return 0
    except (OSError,ValueError,subprocess.TimeoutExpired) as e:
        print(json.dumps({'error':'E_MEDIA','detail':str(e)[:180]}))
        return 1


if __name__=='__main__':
    raise SystemExit(main())
