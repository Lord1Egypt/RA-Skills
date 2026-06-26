#!/usr/bin/env python3
"""
image_export.py — v4.5 deck → 长图（对标 ChatPPT 公众号长图导出）

工作流：
  .pptx → LibreOffice 转 PDF → pdftoppm 拆每页 PNG → PIL 垂直拼接 → 长图

适用场景：
  - 微信公众号文章封面 / 文章末尾长图
  - 朋友圈分享（拆 9 张九宫格 / 单张长图）
  - 小红书图文笔记
  - LinkedIn / 微博文字截图

用法：
    # 单张垂直长图（公众号经典）
    python3 scripts/image_export.py /tmp/d.pptx --output /tmp/longpic.jpg

    # 九宫格（朋友圈）
    python3 scripts/image_export.py /tmp/d.pptx --layout grid-3x3 \\
        --output /tmp/grid.jpg

    # 横排（LinkedIn 走廊式）
    python3 scripts/image_export.py /tmp/d.pptx --layout horizontal \\
        --output /tmp/walk.jpg

    # 高 DPI（出版级）
    python3 scripts/image_export.py d.pptx --dpi 200 -o out.jpg
"""

from __future__ import annotations
import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def pptx_to_pngs(pptx_path: Path, dpi: int = 120) -> list[Path]:
    """pptx → LibreOffice → PDF → pdftoppm PNG"""
    soffice = '/Applications/LibreOffice.app/Contents/MacOS/soffice'
    if not Path(soffice).exists():
        soffice = shutil.which('soffice') or shutil.which('libreoffice')
    if not soffice:
        raise RuntimeError("缺 LibreOffice：brew install --cask libreoffice")

    tmp = Path(tempfile.mkdtemp(prefix='ppt-img-'))
    # pptx → pdf
    subprocess.run([
        soffice, '--headless', '--convert-to', 'pdf',
        '--outdir', str(tmp), str(pptx_path),
    ], capture_output=True, check=True, timeout=60)
    pdf = tmp / (pptx_path.stem + '.pdf')
    if not pdf.exists():
        raise RuntimeError("LibreOffice 没出 PDF")

    # pdf → png（每页一张）
    pdftoppm = shutil.which('pdftoppm')
    if not pdftoppm:
        raise RuntimeError("缺 pdftoppm：brew install poppler")
    subprocess.run([
        pdftoppm, '-png', '-r', str(dpi),
        str(pdf), str(tmp / 'p'),
    ], capture_output=True, check=True)

    return sorted(tmp.glob('p-*.png'))


def stitch_vertical(pngs: list[Path], gap: int = 0,
                    bg: str = '#FFFFFF') -> bytes:
    """垂直拼接（公众号长图）"""
    from PIL import Image
    import io
    images = [Image.open(p) for p in pngs]
    width = max(img.width for img in images)
    height = sum(img.height for img in images) + gap * (len(images) - 1)
    canvas = Image.new('RGB', (width, height), bg)
    y = 0
    for img in images:
        x = (width - img.width) // 2
        canvas.paste(img.convert('RGB'), (x, y))
        y += img.height + gap
    buf = io.BytesIO()
    canvas.save(buf, format='JPEG', quality=92, optimize=True)
    return buf.getvalue()


def stitch_horizontal(pngs: list[Path], gap: int = 0,
                      bg: str = '#FFFFFF') -> bytes:
    """横向拼接（走廊式）"""
    from PIL import Image
    import io
    images = [Image.open(p) for p in pngs]
    height = max(img.height for img in images)
    width = sum(img.width for img in images) + gap * (len(images) - 1)
    canvas = Image.new('RGB', (width, height), bg)
    x = 0
    for img in images:
        y = (height - img.height) // 2
        canvas.paste(img.convert('RGB'), (x, y))
        x += img.width + gap
    buf = io.BytesIO()
    canvas.save(buf, format='JPEG', quality=92, optimize=True)
    return buf.getvalue()


def stitch_grid(pngs: list[Path], cols: int = 3, gap: int = 8,
                bg: str = '#FFFFFF') -> bytes:
    """N×N 网格（朋友圈九宫格）"""
    from PIL import Image
    import io
    images = [Image.open(p) for p in pngs]
    cell_w = max(img.width for img in images)
    cell_h = max(img.height for img in images)
    rows = (len(images) + cols - 1) // cols
    width = cell_w * cols + gap * (cols - 1)
    height = cell_h * rows + gap * (rows - 1)
    canvas = Image.new('RGB', (width, height), bg)
    for i, img in enumerate(images):
        r, c = i // cols, i % cols
        x = c * (cell_w + gap) + (cell_w - img.width) // 2
        y = r * (cell_h + gap) + (cell_h - img.height) // 2
        canvas.paste(img.convert('RGB'), (x, y))
    buf = io.BytesIO()
    canvas.save(buf, format='JPEG', quality=92, optimize=True)
    return buf.getvalue()


def main():
    parser = argparse.ArgumentParser(description='火一五 PPT v4.5 deck → 长图')
    parser.add_argument('pptx', help='输入 .pptx')
    parser.add_argument('--output', '-o', required=True)
    parser.add_argument('--layout',
                        choices=['vertical', 'horizontal', 'grid-3x3', 'grid-2x2'],
                        default='vertical')
    parser.add_argument('--dpi', type=int, default=120)
    parser.add_argument('--gap', type=int, default=0,
                        help='slide 之间间距 px')
    parser.add_argument('--bg', default='#FFFFFF', help='背景色 hex')
    args = parser.parse_args()

    print(f"  📤 {args.pptx} → PNG (DPI {args.dpi})...", file=sys.stderr)
    pngs = pptx_to_pngs(Path(args.pptx), dpi=args.dpi)
    print(f"     {len(pngs)} 张 slide PNG", file=sys.stderr)

    print(f"  🧩 拼接 layout={args.layout}...", file=sys.stderr)
    if args.layout == 'vertical':
        data = stitch_vertical(pngs, gap=args.gap, bg=args.bg)
    elif args.layout == 'horizontal':
        data = stitch_horizontal(pngs, gap=args.gap, bg=args.bg)
    elif args.layout == 'grid-3x3':
        data = stitch_grid(pngs, cols=3, gap=max(args.gap, 8), bg=args.bg)
    elif args.layout == 'grid-2x2':
        data = stitch_grid(pngs, cols=2, gap=max(args.gap, 8), bg=args.bg)

    Path(args.output).write_bytes(data)
    print(f"  ✅ {args.output} ({len(data) // 1024} KB)", file=sys.stderr)


if __name__ == '__main__':
    main()
