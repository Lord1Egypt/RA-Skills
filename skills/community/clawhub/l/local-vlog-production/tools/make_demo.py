"""Create public, fully synthetic media for an installation smoke test."""
import argparse
import json
import math
from pathlib import Path
import subprocess
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFont


def make(root, output, ffmpeg):
    output.mkdir(parents=True, exist_ok=True)
    names = ['demo_photo.jpg', 'demo_card.png', 'demo_video.mp4', 'demo_audio.m4a', 'README.txt']
    if any((output / name).exists() for name in names):
        raise ValueError('Demo outputs already exist; use a new empty output directory.')
    candidates = json.loads((root / '公共资源/style.default.json').read_text(encoding='utf-8-sig')).get('font_candidates', [])
    font_path = None
    for value in candidates:
        candidate = root / value
        if candidate.is_symlink() or not candidate.resolve().is_relative_to(root.resolve()):
            raise ValueError('Font must be a regular file inside the workspace.')
        if candidate.is_file():
            font_path = candidate
            break
    if font_path is None:
        raise ValueError('No configured Chinese font. Supply --body-font during workspace initialization or configure style.font_candidates before generating the demo.')
    font = ImageFont.truetype(str(font_path), 48)
    photo = Image.new('RGB', (900, 1200), '#7cb4cf')
    draw = ImageDraw.Draw(photo)
    draw.ellipse((640, 100, 770, 230), fill='#fff5c9')
    draw.polygon([(0,800),(250,350),(510,770),(720,480),(900,750),(900,1200),(0,1200)], fill='#425c75')
    draw.polygon([(172,490),(250,350),(343,508),(275,450),(240,480)], fill='#f3efe5')
    draw.polygon([(0,940),(300,760),(650,980),(900,820),(900,1200),(0,1200)], fill='#466d55')
    draw.text((70,90), '合成示例 / 非实拍', font=font, fill='#163e48')
    photo.save(output / 'demo_photo.jpg', quality=95)
    card = Image.new('RGB', (720,1280), '#13221e')
    cd = ImageDraw.Draw(card)
    cd.text((75,330), '静态文字页', font=font, fill='#fff7e5')
    cd.text((75,460), '此图仅作测试', font=font, fill='#d4ec50')
    cd.text((75,590), '正式设计按故事制作', font=ImageFont.truetype(str(font_path),32), fill='#fff7e5')
    card.save(output / 'demo_card.png')

    w,h,fps,seconds=360,640,30,6
    command = [ffmpeg,'-hide_banner','-v','error','-nostdin','-n','-f','rawvideo',
        '-pix_fmt','rgb24','-s',f'{w}x{h}','-r',str(fps),'-i','-',
        '-an','-c:v','libx264','-preset','fast','-crf','20',
        '-vf','scale=in_range=full:out_range=tv:out_color_matrix=bt709',
        '-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709',
        '-colorspace','bt709','-color_range','tv',
        '-x264-params','colorprim=bt709:transfer=bt709:colormatrix=bt709',str(output/'demo_video.mp4')]
    with (output/'demo_video.encoder.log').open('wb') as error:
        process=subprocess.Popen(command,stdin=subprocess.PIPE,stderr=error)
        try:
            small = ImageFont.truetype(str(font_path),22)
            for i in range(fps*seconds):
                im=photo.resize((w,h)).copy()
                dr=ImageDraw.Draw(im)
                x=round(15+(w-70)*(i/(fps*seconds-1)))
                dr.rectangle((x,500,x+50,550), fill='#f9e66a')
                dr.text((20,590),f'MOVING  {i:03d}',font=small,fill='white',stroke_width=1,stroke_fill='black')
                process.stdin.write(im.tobytes())
            process.stdin.close()
            if process.wait()!=0: raise RuntimeError('Synthetic video encoder failed; see log.')
        finally:
            if process.poll() is None:
                process.kill();process.wait()
    sr=48000
    t=np.arange(sr*8,dtype=np.float64)/sr
    # Low-level tone, not speech, music, or a clone of any person.
    envelope=np.minimum(1,t/.2)*np.minimum(1,(8-t)/.4)
    signal=(np.sin(2*math.pi*220*t)*.025+np.sin(2*math.pi*330*t)*.012)*envelope
    pcm=(signal*32767).astype('<i2')
    wav=output/'demo_audio.wav'
    with wave.open(str(wav),'wb') as out:
        out.setnchannels(1);out.setsampwidth(2);out.setframerate(sr);out.writeframes(pcm.tobytes())
    result=subprocess.run([ffmpeg,'-hide_banner','-v','error','-nostdin','-n','-i',str(wav),
        '-c:a','aac','-b:a','128k',str(output/'demo_audio.m4a')],capture_output=True)
    if result.returncode: raise RuntimeError(result.stderr.decode('utf-8','replace'))
    (output/'README.txt').write_text('全部为程序生成的测试图形和低电平合成音，不是真实照片、用户语音或配乐。\n'
        '静态文字页只是输入格式示范，不代表完成了AI笔刷纹理设计。\n'
        '这些样本只验证渲染、相对路径和背景运动，不验证真实素材的故事性或混音听感。\n',encoding='utf-8')
    print(json.dumps({'status':'generated','synthetic':True,'files':names},ensure_ascii=False))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parent.parent)
    parser.add_argument('--output-dir',type=Path,default=Path('examples/media'))
    parser.add_argument('--ffmpeg',default='ffmpeg')
    args=parser.parse_args()
    root=args.root.resolve()
    output=(root/args.output_dir).resolve()
    if not output.is_relative_to(root) or output.is_relative_to(root/'素材'):
        parser.error('Output must stay in the workspace and outside 素材.')
    make(root,output,args.ffmpeg)
