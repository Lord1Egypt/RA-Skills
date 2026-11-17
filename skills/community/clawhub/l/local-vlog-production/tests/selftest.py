"""Exercise a relocated workspace with only synthetic public media.

Keeps evidence below 工作数据/缓存; never deletes or reads real source themes.
"""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone

import numpy as np
from PIL import Image, ImageOps


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parent.parent)
    parser.add_argument('--ffmpeg',default='ffmpeg')
    parser.add_argument('--ffprobe',default='ffprobe')
    args=parser.parse_args()
    root=args.root.resolve()
    ff=shutil.which(args.ffmpeg) or args.ffmpeg
    fp=shutil.which(args.ffprobe) or args.ffprobe
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    relocated=root/'工作数据/缓存'/('portable_selftest_'+stamp)/'迁移后的工作区'
    relocated.mkdir(parents=True,exist_ok=False)
    for folder in ['tools','模板']:
        shutil.copytree(root/folder, relocated/folder,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    shutil.copytree(root/'公共资源/字体',relocated/'公共资源/字体')
    shutil.copy2(root/'公共资源/style.default.json',relocated/'公共资源/style.default.json')
    shutil.copy2(root/'workspace_config.json',relocated/'workspace_config.json')
    shutil.copy2(root/'workspace_state.json',relocated/'workspace_state.json')
    (relocated/'examples').mkdir()
    shutil.copy2(root/'examples/演示时间线.json',relocated/'examples/演示时间线.json')
    (relocated/'environment.local.json').write_text(json.dumps({'executables':{'ffmpeg':ff,'ffprobe':fp}},ensure_ascii=False),encoding='utf-8')
    report={'status':'running','synthetic_only':True,'checks':[],
            'continuous_playback':False,'actual_listening':False,'real_source_media_used':False}
    def invoke(script,*extra):
        result=subprocess.run([sys.executable,'-X','utf8',str(relocated/script),*map(str,extra)],cwd=relocated,capture_output=True)
        if result.returncode:
            raise RuntimeError(result.stderr.decode('utf-8','replace')[-5000:]+'\n'+result.stdout.decode('utf-8','replace')[-3000:])
        return result.stdout
    def passed(name,**evidence): report['checks'].append({'name':name,'passed':True,**evidence})
    try:
        invoke('tools/make_demo.py','--ffmpeg',ff)
        passed('generate_public_synthetic_media_after_relocation')
        originals={p.name:digest(p) for p in (relocated/'examples/media').iterdir() if p.suffix in ['.jpg','.png','.mp4','.wav','.m4a']}
        doctor=json.loads(invoke('tools/workspace.py','doctor'))
        assert doctor['details']['ready_for_rendering'], 'Rendering dependency check did not pass'
        passed('relocated_environment_check')
        theme=relocated/'素材/合成主题'
        theme.mkdir(parents=True)
        shutil.copy2(relocated/'examples/media/demo_photo.jpg',theme/'20300102_030405.jpg')
        shutil.copy2(relocated/'examples/media/demo_video.mp4',theme/'20300102_030500.mp4')
        (relocated/'brief.txt').write_text('仅合成测试，不是真实经历。',encoding='utf-8')
        invoke('tools/workspace.py','new','合成演示','--themes','合成主题','--brief','brief.txt')
        invoke('tools/media.py','inventory','--themes','合成主题','--out','工作数据/索引/合成.json')
        invoke('tools/media.py','contacts','--manifest','工作数据/索引/合成.json','--out','工作数据/缓存/合成联系表','--samples','3')
        inventory=json.loads((relocated/'工作数据/索引/合成.json').read_text(encoding='utf-8'))
        assert len(inventory['assets'])==2
        assert not any(inventory['review'].values())
        assert all(not a['capture_time']['filesystem_mtime_used'] for a in inventory['assets'])
        passed('new_project_inventory_contacts_without_false_review')
        base=['--workspace-root',str(relocated),'--timeline','examples/演示时间线.json','--ffmpeg',ff,'--ffprobe',fp]
        validation=json.loads(invoke('tools/render_timeline.py',*base,'--validate-only'))
        assert validation['frames']==240 and validation['duration']==8
        passed('timeline_validation_in_relocated_workspace')
        video='作品/合成演示/05_exports/demo.mp4'
        invoke('tools/render_timeline.py',*base,'--output',video,'--preset','fast')
        invoke('tools/qa.py','--input',video,'--out','作品/合成演示/05_exports/qa.json','--expected-duration','8','--ffmpeg',ff,'--ffprobe',fp)
        qa=json.loads((relocated/'作品/合成演示/05_exports/qa.json').read_text(encoding='utf-8'))
        assert qa['decode_passed'] and qa['duration_passed']
        assert not qa['continuous_playback'] and not qa['actual_listening']
        passed('full_render_decode_and_expected_duration',frames=240,duration_seconds=8)
        def packets(path):
            data=subprocess.check_output([fp,'-v','error','-select_streams','a:0','-show_packets','-show_data_hash','sha256',
                '-show_entries','packet=pts_time,dts_time,duration_time,data_hash','-of','json',str(path)])
            return json.loads(data)['packets']
        before=packets(relocated/'examples/media/demo_audio.m4a')
        after=packets(relocated/video)
        assert before==after, 'Accepted master AAC content or timestamps changed'
        passed('aac_packet_content_and_timestamps_preserved',packet_count=len(after))
        def frame(seconds):
            data=subprocess.check_output([ff,'-v','error','-ss',str(seconds),'-i',str(relocated/video),'-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','-'])
            return np.frombuffer(data,dtype=np.uint8).reshape((640,360,3))
        a,b=frame(1.5),frame(2.3)
        movement=float(np.abs(a[505:550].astype(float)-b[505:550].astype(float)).mean())
        assert movement>1, 'Moving background appears frozen under the photo overlay'
        passed('background_continues_during_photo_overlay',region_mean_absolute_difference=round(movement,3))
        settled=frame(6.5)
        expected=np.asarray(ImageOps.fit(Image.open(relocated/'examples/media/demo_photo.jpg').convert('RGB'),(360,640),Image.Resampling.LANCZOS))
        edge=float(np.abs(settled[:30].astype(float)-expected[:30].astype(float)).mean())
        assert edge<15, 'Full-screen photo did not expand to expected top edge'
        passed('full_photo_fills_after_placement',top_edge_mean_absolute_error=round(edge,3))
        assert originals=={p.name:digest(p) for p in (relocated/'examples/media').iterdir() if p.name in originals}
        passed('input_media_bytes_unchanged')
        report['status']='passed'
    except Exception as exc:
        report['status']='failed';report['error']=str(exc)
    target=relocated.parent/'selftest_report.json'
    target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':report['status'],'report':target.relative_to(root).as_posix(),'passed_checks':len(report['checks'])},ensure_ascii=False))
    return 0 if report['status']=='passed' else 1


if __name__=='__main__':
    if hasattr(sys.stdout,'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')
    raise SystemExit(main())
