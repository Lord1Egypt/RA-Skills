#!/usr/bin/env python3
"""
video_export.py — v4.5 deck → MP4 视频（对标 ChatPPT 视频导出）

工作流：
  .pptx → LibreOffice 转 PDF → pdftoppm 拆 PNG → ffmpeg 合成 MP4
  可选：BGM 音乐叠加 / 渐变转场 / 字幕（slide 文字）

适用场景：
  - 视频号 / 抖音 / 小红书的"PPT 改视频"
  - 邮件附件转视频（PPT 太大，视频压缩好）
  - 自动化 demo（每张 slide 几秒）

用法：
    # 默认：每张 slide 4 秒，720p，无 BGM
    python3 scripts/video_export.py /tmp/d.pptx --output /tmp/d.mp4

    # 带 BGM
    python3 scripts/video_export.py d.pptx --bgm /path/music.mp3 \\
        --duration-per-slide 6 --output d.mp4

    # 高画质 1080p
    python3 scripts/video_export.py d.pptx --resolution 1920x1080 \\
        --duration-per-slide 5 --output d-hd.mp4
"""

from __future__ import annotations
import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def pptx_to_pngs(pptx_path: Path, dpi: int = 144,
                 resolution: str | None = None) -> list[Path]:
    """pptx → LibreOffice → PDF → pdftoppm 高 DPI PNG"""
    soffice = '/Applications/LibreOffice.app/Contents/MacOS/soffice'
    if not Path(soffice).exists():
        soffice = shutil.which('soffice') or shutil.which('libreoffice')
    if not soffice:
        raise RuntimeError("缺 LibreOffice")
    pdftoppm = shutil.which('pdftoppm')
    if not pdftoppm:
        raise RuntimeError("缺 pdftoppm：brew install poppler")

    tmp = Path(tempfile.mkdtemp(prefix='ppt-vid-'))
    subprocess.run([
        soffice, '--headless', '--convert-to', 'pdf',
        '--outdir', str(tmp), str(pptx_path),
    ], capture_output=True, check=True, timeout=60)
    pdf = tmp / (pptx_path.stem + '.pdf')
    if not pdf.exists():
        raise RuntimeError("PDF 转换失败")

    subprocess.run([
        pdftoppm, '-png', '-r', str(dpi),
        str(pdf), str(tmp / 'p'),
    ], capture_output=True, check=True)
    pngs = sorted(tmp.glob('p-*.png'))

    # 统一分辨率（避免 ffmpeg 报错）
    if resolution:
        from PIL import Image
        target_w, target_h = map(int, resolution.split('x'))
        for png in pngs:
            img = Image.open(png).convert('RGB')
            # 保持比例 contain（letterbox 黑边）
            ratio = min(target_w / img.width, target_h / img.height)
            new_w, new_h = int(img.width * ratio), int(img.height * ratio)
            img = img.resize((new_w, new_h), Image.LANCZOS)
            canvas = Image.new('RGB', (target_w, target_h), '#000000')
            canvas.paste(img, ((target_w - new_w) // 2,
                               (target_h - new_h) // 2))
            canvas.save(png, 'PNG')

    return pngs


def make_video(pngs: list[Path], output: Path, *,
               duration_per_slide: float = 4.0,
               bgm: Path | None = None,
               fps: int = 30,
               crf: int = 23) -> None:
    """ffmpeg 合成视频"""
    ffmpeg = shutil.which('ffmpeg')
    if not ffmpeg:
        raise RuntimeError("缺 ffmpeg：brew install ffmpeg")

    tmp = Path(tempfile.mkdtemp(prefix='ppt-vid-ff-'))

    # 写 concat list
    concat = tmp / 'concat.txt'
    with concat.open('w') as f:
        for png in pngs:
            f.write(f"file '{png.absolute()}'\n")
            f.write(f"duration {duration_per_slide}\n")
        # 最后一帧重复（ffmpeg concat demuxer 必需）
        f.write(f"file '{pngs[-1].absolute()}'\n")

    # ffmpeg 8.1+ 弃 -vsync 用 -fps_mode；-r 与 vfr 冲突，改成 vsync_input + cfr 输出
    cmd = [
        ffmpeg, '-y',
        '-f', 'concat', '-safe', '0', '-i', str(concat),
        '-fps_mode', 'cfr',
        '-pix_fmt', 'yuv420p',
        '-c:v', 'libx264', '-crf', str(crf),
        '-r', str(fps),
    ]

    if bgm:
        total_duration = duration_per_slide * len(pngs)
        cmd = [
            ffmpeg, '-y',
            '-f', 'concat', '-safe', '0', '-i', str(concat),
            '-stream_loop', '-1', '-i', str(bgm),
            '-fps_mode', 'cfr',
            '-pix_fmt', 'yuv420p',
            '-c:v', 'libx264', '-crf', str(crf),
            '-c:a', 'aac', '-b:a', '128k',
            '-r', str(fps),
            '-shortest',
            '-af', f'afade=t=out:st={total_duration - 1}:d=1',
            str(output),
        ]
    else:
        cmd.append(str(output))

    subprocess.run(cmd, capture_output=True, check=True, timeout=300)


def main():
    parser = argparse.ArgumentParser(description='火一五 PPT v4.5 deck → MP4')
    parser.add_argument('pptx')
    parser.add_argument('--output', '-o', required=True)
    parser.add_argument('--duration-per-slide', type=float, default=4.0,
                        help='每张 slide 几秒（默认 4）')
    parser.add_argument('--resolution', default='1920x1080',
                        help='视频分辨率，默认 1080p')
    parser.add_argument('--fps', type=int, default=30)
    parser.add_argument('--crf', type=int, default=23,
                        help='画质 18(高)~28(低) 默认 23')
    parser.add_argument('--bgm', help='背景音乐 mp3 路径（可选）')
    args = parser.parse_args()

    print(f"  📤 {args.pptx} → PNG ({args.resolution})...", file=sys.stderr)
    pngs = pptx_to_pngs(Path(args.pptx), resolution=args.resolution)
    total_sec = args.duration_per_slide * len(pngs)
    print(f"     {len(pngs)} 张，预计视频 {total_sec:.1f}s", file=sys.stderr)

    print(f"  🎬 ffmpeg 合成 MP4...", file=sys.stderr)
    make_video(pngs, Path(args.output),
               duration_per_slide=args.duration_per_slide,
               bgm=Path(args.bgm) if args.bgm else None,
               fps=args.fps, crf=args.crf)

    size_mb = Path(args.output).stat().st_size / 1024 / 1024
    print(f"  ✅ {args.output} ({size_mb:.1f} MB)", file=sys.stderr)


if __name__ == '__main__':
    main()
