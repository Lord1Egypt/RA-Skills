"""Technical video inspection. Never claims human viewing or listening."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys


def run(args):
    return subprocess.run([str(a) for a in args],capture_output=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parent.parent)
    parser.add_argument('--input',required=True,type=Path)
    parser.add_argument('--out',required=True,type=Path)
    parser.add_argument('--expected-duration',type=float)
    parser.add_argument('--ffmpeg')
    parser.add_argument('--ffprobe')
    args=parser.parse_args()
    root=args.root.resolve()
    source=(root/args.input).resolve()
    target=(root/args.out).resolve()
    config=json.loads((root/'workspace_config.json').read_text(encoding='utf-8-sig'))
    srcdir=(root/config.get('paths',{}).get('sources','素材')).resolve()
    if not source.is_relative_to(root) or not source.is_file(): parser.error('Input must exist inside the workspace.')
    if not target.is_relative_to(root) or target.is_relative_to(srcdir) or target.exists():
        parser.error('Report must be a new file inside the workspace, outside sources.')
    exe=config.get('executables',{})
    local=root/'environment.local.json'
    if local.exists(): exe.update(json.loads(local.read_text(encoding='utf-8-sig')).get('executables',{}))
    ff=args.ffmpeg or exe.get('ffmpeg') or 'ffmpeg'
    fp=args.ffprobe or exe.get('ffprobe') or 'ffprobe'
    def executable(value):
        p=Path(value)
        return str(root/p) if not p.is_absolute() and len(p.parts)>1 else value
    ff,fp=executable(ff),executable(fp)
    probe=run([fp,'-v','error','-show_format','-show_streams','-of','json',source])
    if probe.returncode: raise RuntimeError(probe.stderr.decode('utf-8','replace'))
    metadata=json.loads(probe.stdout)
    duration=float(metadata.get('format',{}).get('duration',0))
    decode=run([ff,'-hide_banner','-nostdin','-v','error','-xerror','-i',source,'-map','0:v:0','-map','0:a?', '-f','null','-'])
    signals=run([ff,'-hide_banner','-nostdin','-i',source,'-vf','blackdetect=d=0.12:pix_th=0.10',
                 '-af','volumedetect','-f','null','-'])
    log=signals.stderr.decode('utf-8','replace')
    black=[{'start':float(a),'end':float(b),'duration':float(c)} for a,b,c in
           re.findall(r'black_start:([\d.]+) black_end:([\d.]+) black_duration:([\d.]+)',log)]
    maxvol=re.search(r'max_volume:\s*([\-\w.]+) dB',log)
    meanvol=re.search(r'mean_volume:\s*([\-\w.]+) dB',log)
    duration_ok=None if args.expected_duration is None else abs(duration-args.expected_duration)<=.1
    report={'schema_version':1,'file':source.relative_to(root).as_posix(),'duration_seconds':duration,
        'streams':[{k:s.get(k) for k in ['codec_type','codec_name','width','height','avg_frame_rate','sample_rate','color_space','color_transfer','color_primaries','color_range']} for s in metadata.get('streams',[])],
        'decode_passed':decode.returncode==0,'decode_error':decode.stderr.decode('utf-8','replace')[-4000:],
        'expected_duration_seconds':args.expected_duration,'duration_passed':duration_ok,
        'signal_scan_passed':signals.returncode==0,'black_intervals_for_review':black,
        'sample_peak_dbfs':maxvol.group(1) if maxvol else None,
        'mean_volume_dbfs':meanvol.group(1) if meanvol else None,
        'warnings':['Black intervals can be deliberate; inspect them. Sample peaks are not true peaks or a loudness judgement.'],
        'visual_frames_reviewed':False,'continuous_playback':False,'actual_listening':False,'user_accepted':False}
    target.parent.mkdir(parents=True,exist_ok=True)
    with target.open('x',encoding='utf-8') as out: json.dump(report,out,ensure_ascii=False,indent=2)
    print(json.dumps({'report':target.relative_to(root).as_posix(),'decode_passed':report['decode_passed'],'duration_passed':duration_ok},ensure_ascii=False))
    return 0 if decode.returncode==0 and duration_ok is not False and signals.returncode==0 else 1


if __name__=='__main__':
    try: sys.exit(main())
    except (OSError,ValueError,RuntimeError) as e:
        print(str(e),file=sys.stderr);sys.exit(1)
