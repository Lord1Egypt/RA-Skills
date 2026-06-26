# -*- coding: utf-8 -*-
"""
pixel-art-processing - 本地图像处理脚本 / Local Image Processing Script

基于 FrameRonin: https://github.com/systemchester/FrameRonin

无需后端，直接在本地处理图像/GIF/Sprite Sheet。

功能 / Features:
    • GIF拆帧 & 合成GIF
    • Sprite Sheet 拆分 & 合成
    • 图像缩放、裁切、像素化
    • AI抠图 (rembg)
    • 色度键抠图
    • 透明行列检测拆分

用法 / Usage:
    python local_processor.py --help
    python local_processor.py gif-split input.gif output_dir/
    python local_processor.py gif-make input_dir/ output.gif --delay 100
    python local_processor.py sprite-split sprite.png output_dir/ --cols 4 --frame-w 64 --frame-h 64
    python local_processor.py sprite-make input_dir/ output.png --cols 4 --spacing 4
    python local_processor.py resize input.png output.png --w 256 --h 256 --method nearest
    python local_processor.py crop input.png output.png --x 10 --y 10 --w 100 --h 100
    python local_processor.py pixelate input.png output.png --scale 4
    python local_processor.py chromakey input.png output.png --color "0,255,0" --tolerance 30
    python local_processor.py transparency-split input.png output_dir/  (超级拆分)
"""

import argparse
import base64
import io
import json
import math
import os
import shutil
import sys
import tempfile
import urllib.request
from pathlib import Path
from typing import Optional

# 可选依赖 / Optional dependencies
HAS_PIL = False
HAS_REMbg = False
HAS_CV2 = False
HAS_GIFENC = False

try:
    from PIL import Image, ImageDraw
    HAS_PIL = True
except ImportError:
    pass

try:
    from rembg import remove
    HAS_REMbg = True
except ImportError:
    pass

try:
    import cv2
    import numpy as np
    HAS_CV2 = True
except ImportError:
    pass


# =============================================================================
# 工具函数 / Utilities
# =============================================================================

def error(msg: str):
    print(f"❌ ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def ok(msg: str):
    print(f"✅ {msg}")


def warn(msg: str):
    print(f"⚠️  {msg}")


def ensure_pil():
    if not HAS_PIL:
        error("PIL (Pillow) not installed. Run: pip install pillow")


# =============================================================================
# GIF 处理 / GIF Processing
# =============================================================================

def gif_split(input_path: Path, output_dir: Path, max_frames: int = 0):
    """
    将GIF拆分为帧序列图片
    Split GIF into individual frame images.
    """
    ensure_pil()
    output_dir.mkdir(parents=True, exist_ok=True)
    
    img = Image.open(input_path)
    if not img.is_animated:
        error(f"{input_path} is not an animated GIF")
    
    n_frames = img.n_frames
    if max_frames > 0:
        n_frames = min(n_frames, max_frames)
    
    print(f"Splitting {n_frames} frames from {input_path.name}...")
    
    for i in range(n_frames):
        img.seek(i)
        frame = img.copy().convert("RGBA")
        out_path = output_dir / f"frame_{i:05d}.png"
        frame.save(out_path, "PNG")
        print(f"  Extracted frame {i+1}/{n_frames}")
    
    ok(f"Saved {n_frames} frames to {output_dir}")


def gif_make(input_dir: Path, output_path: Path, delay: int = 100, loop: int = 0):
    """
    将帧序列图片合成为GIF
    Make GIF from frame sequence images.
    """
    ensure_pil()
    
    # 收集所有PNG/JPG文件 / Collect all image files
    frames = sorted(input_dir.glob("*.png")) + sorted(input_dir.glob("*.jpg"))
    if not frames:
        frames = sorted(input_dir.glob("*.gif"))
    
    if not frames:
        error(f"No images found in {input_dir}")
    
    print(f"Making GIF from {len(frames)} frames...")
    
    # 打开第一帧确定尺寸 / Open first frame to determine size
    first = Image.open(frames[0])
    w, h = first.size
    
    # 收集所有帧 / Collect all frames
    images = []
    for f in frames:
        im = Image.open(f).convert("RGBA")
        if im.size != (w, h):
            im = im.resize((w, h), Image.LANCZOS)
        images.append(im)
    
    # 保存GIF / Save GIF
    images[0].save(
        output_path,
        save_all=True,
        append_images=images[1:],
        duration=delay,
        loop=loop,
        optimize=False,
    )
    
    ok(f"Saved GIF to {output_path} ({len(frames)} frames, {delay}ms delay)")


# =============================================================================
# Sprite Sheet 处理 / Sprite Sheet Processing
# =============================================================================

def sprite_split(
    input_path: Path,
    output_dir: Path,
    cols: int,
    rows: int,
    frame_w: int,
    frame_h: int,
    spacing: int = 0
):
    """
    拆分Sprite Sheet为帧序列
    Split sprite sheet into individual frames.
    """
    ensure_pil()
    output_dir.mkdir(parents=True, exist_ok=True)
    
    sheet = Image.open(input_path).convert("RGBA")
    w, h = sheet.size
    
    total = cols * rows
    print(f"Splitting {total} frames ({cols}x{rows}, {frame_w}x{frame_h}px)...")
    
    count = 0
    for row in range(rows):
        for col in range(cols):
            x = col * (frame_w + spacing)
            y = row * (frame_h + spacing)
            
            if x + frame_w > w or y + frame_h > h:
                warn(f"Frame {count} out of bounds, skipping")
                continue
            
            frame = sheet.crop((x, y, x + frame_w, y + frame_h))
            out_path = output_dir / f"sprite_{row}_{col:02d}.png"
            frame.save(out_path, "PNG")
            count += 1
    
    ok(f"Split {count} frames to {output_dir}")


def sprite_make(
    input_dir: Path,
    output_path: Path,
    cols: int,
    rows: int,
    frame_w: int,
    frame_h: int,
    spacing: int = 0,
    bg_color: str = "transparent"
):
    """
    将帧序列图片合成为Sprite Sheet
    Make sprite sheet from frame images.
    """
    ensure_pil()
    
    # 收集所有帧 / Collect all frames
    frames = sorted(input_dir.glob("*.png")) + sorted(input_dir.glob("*.jpg"))
    if not frames:
        error(f"No images found in {input_dir}")
    
    total = cols * rows
    print(f"Making sprite sheet ({cols}x{rows}, {frame_w}x{frame_h}px) from {len(frames)} images...")
    
    # 创建大画布 / Create large canvas
    sheet_w = cols * (frame_w + spacing) - spacing
    sheet_h = rows * (frame_h + spacing) - spacing
    
    if bg_color == "transparent":
        bg = (0, 0, 0, 0)
    else:
        bg = _parse_color(bg_color)
    
    sheet = Image.new("RGBA", (sheet_w, sheet_h), bg)
    
    # 逐帧粘贴 / Paste each frame
    for i, frame_path in enumerate(frames[:total]):
        if i >= total:
            break
        row = i // cols
        col = i % cols
        x = col * (frame_w + spacing)
        y = row * (frame_h + spacing)
        
        frame = Image.open(frame_path).convert("RGBA")
        if frame.size != (frame_w, frame_h):
            frame = frame.resize((frame_w, frame_h), Image.LANCZOS)
        
        sheet.paste(frame, (x, y), frame)
    
    sheet.save(output_path, "PNG")
    
    # 生成index.json / Generate index.json
    index_path = output_path.with_suffix(".json")
    frames_index = []
    for i in range(min(len(frames), total)):
        row = i // cols
        col = i % cols
        x = col * (frame_w + spacing)
        y = row * (frame_h + spacing)
        frames_index.append({
            "i": i,
            "x": x,
            "y": y,
            "w": frame_w,
            "h": frame_h,
            "t": round(i * 0.1, 3)
        })
    
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump({
            "version": "1.0",
            "frame_size": {"w": frame_w, "h": frame_h},
            "sheet_size": {"w": sheet_w, "h": sheet_h},
            "frames": frames_index
        }, f, indent=2)
    
    ok(f"Saved sprite sheet to {output_path} + {index_path}")


def sprite_make_auto(
    input_dir: Path,
    output_path: Path,
    frame_w: int,
    frame_h: int,
    spacing: int = 0,
    layout_mode: str = "auto_square",
    columns: int = 4
):
    """
    自动布局合成Sprite Sheet
    Auto-layout sprite sheet from frames.
    """
    frames = sorted(input_dir.glob("*.png")) + sorted(input_dir.glob("*.jpg"))
    if not frames:
        error(f"No images found in {input_dir}")
    
    frame_count = len(frames)
    
    # 计算布局 / Compute layout
    if layout_mode == "fixed_columns":
        cols = columns
    else:
        cols = max(1, math.ceil(math.sqrt(frame_count)))
    rows = math.ceil(frame_count / cols)
    
    sprite_make(
        input_dir, output_path,
        cols=cols, rows=rows,
        frame_w=frame_w, frame_h=frame_h,
        spacing=spacing
    )


# =============================================================================
# 图像基本处理 / Image Basic Processing
# =============================================================================

def _parse_color(s: str) -> tuple:
    """解析颜色字符串 / Parse color string"""
    s = s.lstrip("#")
    if len(s) == 6:
        return tuple(int(s[i:i+2], 16) for i in (0, 2, 4)) + (255,)
    if len(s) == 8:
        return tuple(int(s[i:i+2], 16) for i in (0, 2, 4, 6))
    return (0, 0, 0, 0)


def image_resize(input_path: Path, output_path: Path, w: int, h: int, method: str = "lanczos"):
    """
    缩放图像
    Resize image.
    """
    ensure_pil()
    
    img = Image.open(input_path).convert("RGBA")
    
    methods = {
        "nearest": Image.NEAREST,
        "bilinear": Image.BILINEAR,
        "bicubic": Image.BICUBIC,
        "lanczos": Image.LANCZOS,
    }
    resample = methods.get(method.lower(), Image.LANCZOS)
    
    resized = img.resize((w, h), resample)
    resized.save(output_path, "PNG")
    ok(f"Resized to {w}x{h} ({method}) → {output_path}")


def image_crop(input_path: Path, output_path: Path, x: int, y: int, w: int, h: int):
    """
    裁切图像
    Crop image.
    """
    ensure_pil()
    img = Image.open(input_path).convert("RGBA")
    
    cropped = img.crop((x, y, x + w, y + h))
    cropped.save(output_path, "PNG")
    ok(f"Cropped to {w}x{h} at ({x},{y}) → {output_path}")


def image_pixelate(input_path: Path, output_path: Path, scale: int = 4):
    """
    像素化效果 (缩小再放大)
    Pixelate effect.
    """
    ensure_pil()
    img = Image.open(input_path).convert("RGBA")
    
    small_w = max(1, img.width // scale)
    small_h = max(1, img.height // scale)
    
    small = img.resize((small_w, small_h), Image.NEAREST)
    pixelated = small.resize((img.width, img.height), Image.NEAREST)
    
    pixelated.save(output_path, "PNG")
    ok(f"Pixelated (scale={scale}) → {output_path}")


def image_chromakey(
    input_path: Path,
    output_path: Path,
    color: str = "0,255,0",
    tolerance: int = 30,
    smooth: bool = False
):
    """
    色度键抠图 (绿幕/蓝幕)
    Chroma key background removal.
    """
    ensure_pil()
    
    r, g, b = [int(x) for x in color.split(",")]
    
    img = Image.open(input_path).convert("RGBA")
    pixels = img.load()
    w, h = img.size
    
    # 第一遍：标记要抠掉的像素 / First pass: mark pixels to remove
    to_remove = []
    for y in range(h):
        for x in range(w):
            p = pixels[x, y]
            dr = abs(p[0] - r)
            dg = abs(p[1] - g)
            db = abs(p[2] - b)
            if max(dr, dg, db) <= tolerance:
                to_remove.append((x, y))
    
    # 设为透明 / Set to transparent
    for x, y in to_remove:
        pixels[x, y] = (0, 0, 0, 0)
    
    if smooth:
        # 边缘平滑 (简化版) / Edge smooth (simplified)
        temp = img.copy()
        temp_pixels = temp.load()
        for x, y in to_remove:
            # 检查周围8邻域的不透明像素
            alpha_sum = 0
            cnt = 0
            for dy in range(-2, 3):
                for dx in range(-2, 3):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h:
                        a = temp_pixels[nx, ny][3]
                        if a > 0:
                            alpha_sum += a
                            cnt += 1
            if cnt > 0:
                avg_alpha = min(255, alpha_sum // cnt * 3)
                pixels[x, y] = (0, 0, 0, avg_alpha)
    
    img.save(output_path, "PNG")
    ok(f"Chromakey ({color}, tolerance={tolerance}) → {output_path}")


def image_matting(input_path: Path, output_path: Path):
    """
    AI抠图 (需要rembg)
    AI background removal (requires rembg).
    """
    if not HAS_REMbg:
        error("rembg not installed. Run: pip install rembg")
    
    with open(input_path, "rb") as f:
        input_data = f.read()
    
    output_data = remove(input_data)
    
    with open(output_path, "wb") as f:
        f.write(output_data)
    
    ok(f"AI matting → {output_path}")


# =============================================================================
# 透明行列智能拆分 / Transparent Row/Col Smart Split
# =============================================================================

def transparency_split(input_path: Path, output_dir: Path):
    """
    超级拆分：按透明行/列智能切割图像
    Smart split by detecting transparent rows and columns.
    
    原理 / Algorithm:
    1. 找出所有完全透明的行和列
    2. 将透明区域转换为区间（gaps）
    3. 按区间切割出每个子图
    4. 统一尺寸（最大帧尺寸）并居中输出
    """
    ensure_pil()
    output_dir.mkdir(parents=True, exist_ok=True)
    
    img = Image.open(input_path).convert("RGBA")
    w, h = img.size
    
    # 获取像素数据 / Get pixel data
    data = list(img.getdata())
    
    # 找出透明行 / Find transparent rows
    transparent_rows = []
    for y in range(h):
        all_transparent = True
        for x in range(w):
            if data[y * w + x][3] != 0:
                all_transparent = False
                break
        if all_transparent:
            transparent_rows.append(y)
    
    # 找出透明列 / Find transparent cols
    transparent_cols = []
    for x in range(w):
        all_transparent = True
        for y in range(h):
            if data[y * w + x][3] != 0:
                all_transparent = False
                break
        if all_transparent:
            transparent_cols.append(x)
    
    # 转换为区间 / Convert to runs
    def get_runs(arr):
        if not arr:
            return []
        runs = []
        start = end = arr[0]
        for v in arr[1:]:
            if v == end + 1:
                end = v
            else:
                runs.append([start, end])
                start = end = v
        runs.append([start, end])
        return runs
    
    def gaps_from_runs(runs, total):
        if not runs:
            return [[0, total - 1]]
        regions = []
        regions.append([0, runs[0][0] - 1])
        for i in range(len(runs) - 1):
            regions.append([runs[i][1] + 1, runs[i+1][0] - 1])
        regions.append([runs[-1][1] + 1, total - 1])
        return [[a, b] for a, b in regions if a <= b]
    
    row_runs = get_runs(transparent_rows)
    row_regions = gaps_from_runs(row_runs, h)
    
    # 对每一行区域，检测列分割 / For each row region, detect col splits
    frames = []
    for y0, y1 in row_regions:
        row_height = y1 - y0 + 1
        if row_height <= 0:
            continue
        
        # 收集这行的透明列 / Collect transparent cols in this row region
        row_transparent_cols = []
        for x in range(w):
            all_transparent = True
            for y in range(y0, y1 + 1):
                if data[y * w + x][3] != 0:
                    all_transparent = False
                    break
            if all_transparent:
                row_transparent_cols.append(x)
        
        col_runs = get_runs(row_transparent_cols)
        col_regions = gaps_from_runs(col_runs, w)
        
        for x0, x1 in col_regions:
            col_width = x1 - x0 + 1
            if col_width <= 0:
                continue
            frames.append((x0, y0, col_width, row_height))
    
    if not frames:
        error("No frames found (image may be fully transparent)")
    
    # 计算最大尺寸 / Compute max size
    max_w = max(f[2] for f in frames)
    max_h = max(f[3] for f in frames)
    
    print(f"Found {len(frames)} frames, max size: {max_w}x{max_h}")
    
    # 创建输出帧 / Create output frames
    base_name = input_path.stem
    for i, (x, y, fw, fh) in enumerate(frames):
        frame = img.crop((x, y, x + fw, y + fh))
        
        # 居中到最大尺寸 / Center to max size
        canvas = Image.new("RGBA", (max_w, max_h), (0, 0, 0, 0))
        paste_x = (max_w - fw) // 2
        paste_y = (max_h - fh) // 2
        canvas.paste(frame, (paste_x, paste_y), frame)
        
        out_path = output_dir / f"{base_name}_super_{i:03d}.png"
        canvas.save(out_path, "PNG")
        print(f"  Saved frame {i+1}/{len(frames)}")
    
    ok(f"Super split {len(frames)} frames to {output_dir}")


# =============================================================================
# 主程序 / Main
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Local pixel art / sprite sheet processor (based on FrameRonin)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="cmd", required=True)
    
    # GIF拆帧 / GIF split
    p = sub.add_parser("gif-split", help="Split GIF into frames")
    p.add_argument("input", type=Path, help="Input GIF file")
    p.add_argument("output", type=Path, help="Output directory")
    p.add_argument("--max", dest="max_frames", type=int, default=0, help="Max frames (0=all)")
    
    # GIF合成 / GIF make
    p = sub.add_parser("gif-make", help="Make GIF from frames")
    p.add_argument("input", type=Path, help="Input directory with frames")
    p.add_argument("output", type=Path, help="Output GIF file")
    p.add_argument("--delay", type=int, default=100, help="Frame delay in ms (default: 100)")
    p.add_argument("--loop", type=int, default=0, help="Loop count (0=infinite)")
    
    # Sprite Sheet 拆分 / Sprite split
    p = sub.add_parser("sprite-split", help="Split sprite sheet into frames")
    p.add_argument("input", type=Path, help="Input sprite sheet")
    p.add_argument("output", type=Path, help="Output directory")
    p.add_argument("--cols", type=int, required=True, help="Number of columns")
    p.add_argument("--rows", type=int, required=True, help="Number of rows")
    p.add_argument("--frame-w", type=int, required=True, help="Frame width in pixels")
    p.add_argument("--frame-h", type=int, required=True, help="Frame height in pixels")
    p.add_argument("--spacing", type=int, default=0, help="Spacing between frames")
    
    # Sprite Sheet 合成 / Sprite make
    p = sub.add_parser("sprite-make", help="Make sprite sheet from frames")
    p.add_argument("input", type=Path, help="Input directory with frames")
    p.add_argument("output", type=Path, help="Output sprite sheet")
    p.add_argument("--cols", type=int, required=True, help="Number of columns")
    p.add_argument("--rows", type=int, required=True, help="Number of rows")
    p.add_argument("--frame-w", type=int, required=True, help="Frame width")
    p.add_argument("--frame-h", type=int, required=True, help="Frame height")
    p.add_argument("--spacing", type=int, default=0, help="Spacing between frames")
    p.add_argument("--bg", dest="bg_color", default="transparent", help="Background color")
    
    # Sprite Sheet 自动布局合成 / Sprite auto make
    p = sub.add_parser("sprite-make-auto", help="Make sprite sheet with auto layout")
    p.add_argument("input", type=Path, help="Input directory")
    p.add_argument("output", type=Path, help="Output sprite sheet")
    p.add_argument("--frame-w", type=int, required=True, help="Frame width")
    p.add_argument("--frame-h", type=int, required=True, help="Frame height")
    p.add_argument("--spacing", type=int, default=0)
    p.add_argument("--mode", dest="layout_mode", default="auto_square", choices=["auto_square", "fixed_columns"])
    p.add_argument("--columns", type=int, default=4)
    
    # 图像缩放 / Image resize
    p = sub.add_parser("resize", help="Resize image")
    p.add_argument("input", type=Path)
    p.add_argument("output", type=Path)
    p.add_argument("--w", type=int, required=True)
    p.add_argument("--h", type=int, required=True)
    p.add_argument("--method", default="lanczos", choices=["nearest", "bilinear", "bicubic", "lanczos"])
    
    # 图像裁切 / Image crop
    p = sub.add_parser("crop", help="Crop image")
    p.add_argument("input", type=Path)
    p.add_argument("output", type=Path)
    p.add_argument("--x", type=int, required=True)
    p.add_argument("--y", type=int, required=True)
    p.add_argument("--w", type=int, required=True)
    p.add_argument("--h", type=int, required=True)
    
    # 像素化 / Pixelate
    p = sub.add_parser("pixelate", help="Pixelate image")
    p.add_argument("input", type=Path)
    p.add_argument("output", type=Path)
    p.add_argument("--scale", type=int, default=4)
    
    # 色度键 / Chromakey
    p = sub.add_parser("chromakey", help="Chroma key background removal")
    p.add_argument("input", type=Path)
    p.add_argument("output", type=Path)
    p.add_argument("--color", default="0,255,0", help="Target color R,G,B (default: 0,255,0=green)")
    p.add_argument("--tolerance", type=int, default=30)
    p.add_argument("--smooth", action="store_true")
    
    # AI抠图 / AI Matting
    p = sub.add_parser("matting", help="AI background removal (requires rembg)")
    p.add_argument("input", type=Path)
    p.add_argument("output", type=Path)
    
    # 超级拆分 / Super split
    p = sub.add_parser("transparency-split", help="Smart split by transparent rows/cols")
    p.add_argument("input", type=Path)
    p.add_argument("output", type=Path)
    
    args = parser.parse_args()
    
    if args.cmd == "gif-split":
        gif_split(args.input, args.output, args.max_frames)
    elif args.cmd == "gif-make":
        gif_make(args.input, args.output, args.delay, args.loop)
    elif args.cmd == "sprite-split":
        sprite_split(args.input, args.output, args.cols, args.rows, args.frame_w, args.frame_h, args.spacing)
    elif args.cmd == "sprite-make":
        sprite_make(args.input, args.output, args.cols, args.rows, args.frame_w, args.frame_h, args.spacing, args.bg_color)
    elif args.cmd == "sprite-make-auto":
        sprite_make_auto(args.input, args.output, args.frame_w, args.frame_h, args.spacing, args.layout_mode, args.columns)
    elif args.cmd == "resize":
        image_resize(args.input, args.output, args.w, args.h, args.method)
    elif args.cmd == "crop":
        image_crop(args.input, args.output, args.x, args.y, args.w, args.h)
    elif args.cmd == "pixelate":
        image_pixelate(args.input, args.output, args.scale)
    elif args.cmd == "chromakey":
        image_chromakey(args.input, args.output, args.color, args.tolerance, args.smooth)
    elif args.cmd == "matting":
        image_matting(args.input, args.output)
    elif args.cmd == "transparency-split":
        transparency_split(args.input, args.output)


if __name__ == "__main__":
    main()
