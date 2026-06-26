#!/usr/bin/env python3
"""Image compression and conversion tool."""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


def check_ffmpeg():
    """Check if ffmpeg is installed."""
    if not shutil.which('ffmpeg'):
        print("错误：未检测到 ffmpeg")
        print("请安装：")
        print("  Ubuntu/Debian: sudo apt install ffmpeg")
        print("  macOS: brew install ffmpeg")
        print("  Windows: https://ffmpeg.org/download.html")
        sys.exit(1)


def get_image_info(filepath):
    """Get image dimensions using ffprobe."""
    cmd = [
        'ffprobe', '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height',
        '-of', 'csv=s=x:p=0',
        filepath
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            parts = result.stdout.strip().split('x')
            return int(parts[0]), int(parts[1])
    except:
        pass
    return None, None


def compress_image(input_path, output_path, max_width=None, max_height=None,
                   quality=85, strip=True, max_size=None, dry_run=False, backup=False):
    """Compress a single image."""
    input_path = Path(input_path)
    output_path = Path(output_path)

    # Backup original if requested
    if backup:
        backup_path = input_path.parent / f"{input_path.stem}.backup{input_path.suffix}"
        if not backup_path.exists():
            shutil.copy2(input_path, backup_path)
            print(f"  已备份原文件: {backup_path.name}")

    # Determine output format
    ext = output_path.suffix.lower()
    if ext in ['.jpg', '.jpeg']:
        codec = 'mjpeg'
        options = ['-q:v', str(quality)]
    elif ext == '.png':
        codec = 'png'
        options = ['-compression_level', '9']
    elif ext == '.webp':
        codec = 'libwebp'
        options = ['-q:v', str(quality)]
    else:
        # Default to jpeg
        codec = 'mjpeg'
        options = ['-q:v', str(quality)]
    
    # Build filter for resizing
    filters = []
    if max_width or max_height:
        width = max_width or -1
        height = max_height or -1
        filters.append(f'scale={width}:{height}:force_original_aspect_ratio=decrease')
    
    # Build command
    cmd = ['ffmpeg', '-y', '-i', str(input_path)]
    
    if filters:
        cmd.extend(['-vf', ','.join(filters)])
    
    if strip:
        cmd.extend(['-map_metadata', '-1'])
    
    cmd.extend(['-c:v', codec] + options)
    cmd.append(str(output_path))

    # Preview mode: estimate compression result
    if dry_run:
        print(f"\n  [预览模式] 不会实际压缩")
        print(f"  原文件: {input_path.name}")
        width, height = get_image_info(input_path)
        if width and height:
            print(f"  分辨率: {width}x{height}")
        print(f"  当前大小: {input_path.stat().st_size/1024:.1f}KB")
        print(f"  设置参数:")
        print(f"    - 质量: {quality}")
        if max_width or max_height:
            print(f"    - 最大尺寸: {max_width or 'auto'}x{max_height or 'auto'}")
        if max_size:
            print(f"    - 目标大小: {max_size}")
        print(f"  预估: 压缩后约减少 40-80% 大小")
        return True

    # Execute
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"错误: {result.stderr}")
        return False
    
    # Check if we need to iterate for target size
    if max_size:
        target_bytes = parse_size(max_size)
        current_size = output_path.stat().st_size
        
        if current_size > target_bytes:
            # Need to reduce quality further
            print(f"当前大小: {current_size/1024:.1f}KB, 目标: {target_bytes/1024:.1f}KB, 调整质量...")
            # Simple approach: reduce quality by 10 and try again
            new_quality = max(10, quality - 15)
            if new_quality < quality:
                return compress_image(input_path, output_path, max_width, max_height, 
                                    new_quality, strip, max_size)
    
    return True


def parse_size(size_str):
    """Parse size string like '500kb', '2mb' to bytes."""
    size_str = size_str.lower().strip()
    if size_str.endswith('kb'):
        return int(float(size_str[:-2]) * 1024)
    elif size_str.endswith('mb'):
        return int(float(size_str[:-2]) * 1024 * 1024)
    elif size_str.endswith('gb'):
        return int(float(size_str[:-2]) * 1024 * 1024 * 1024)
    else:
        return int(size_str)


def process_batch(input_dir, output_dir, dry_run=False, backup=False, **kwargs):
    """Process all images in a directory."""
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    image_exts = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff', '.gif'}
    files = [f for f in input_dir.iterdir() if f.suffix.lower() in image_exts]

    print(f"找到 {len(files)} 个图像文件")

    for i, file in enumerate(files, 1):
        output_file = output_dir / file.name
        # Change extension if format specified
        if kwargs.get('format'):
            output_file = output_file.with_suffix(f".{kwargs['format']}")

        print(f"[{i}/{len(files)}] 处理: {file.name}")

        if compress_image(file, output_file, dry_run=dry_run, backup=backup, **kwargs):
            if dry_run:
                continue
            original_size = file.stat().st_size
            new_size = output_file.stat().st_size
            ratio = (1 - new_size/original_size) * 100
            print(f"  ✓ {original_size/1024:.1f}KB → {new_size/1024:.1f}KB ({ratio:.1f}% 减少)")
        else:
            print(f"  ✗ 失败")


def main():
    parser = argparse.ArgumentParser(description='压缩图像文件')
    parser.add_argument('input', help='输入文件或目录')
    parser.add_argument('--output', '-o', help='输出文件或目录')
    parser.add_argument('--max-size', help='目标最大大小 (如 500kb, 2mb)')
    parser.add_argument('--quality', '-q', type=int, default=85, help='质量 1-100 (默认: 85)')
    parser.add_argument('--width', '-w', type=int, help='最大宽度')
    parser.add_argument('--height', type=int, help='最大高度')
    parser.add_argument('--format', '-f', choices=['jpg', 'png', 'webp'], help='输出格式')
    parser.add_argument('--no-strip', action='store_true', help='保留元数据')
    parser.add_argument('--preview', '-p', action='store_true',
                       help='预览模式：显示压缩预估，不实际执行')
    parser.add_argument('--backup', '-b', action='store_true',
                       help='保留原文件备份')

    args = parser.parse_args()
    
    check_ffmpeg()
    
    input_path = Path(args.input)
    
    if input_path.is_dir():
        # Batch mode
        output_dir = Path(args.output) if args.output else input_path.parent / 'compressed'
        kwargs = {
            'max_width': args.width,
            'max_height': args.height,
            'quality': args.quality,
            'strip': not args.no_strip,
            'max_size': args.max_size,
            'format': args.format
        }
        process_batch(input_path, output_dir, dry_run=args.preview, backup=args.backup, **kwargs)
    else:
        # Single file mode
        if args.output:
            output_path = Path(args.output)
        else:
            suffix = f".{args.format}" if args.format else input_path.suffix
            output_path = input_path.parent / f"{input_path.stem}_compressed{suffix}"
        
        print(f"压缩: {input_path}")

        if args.preview:
            compress_image(input_path, output_path,
                          max_width=args.width,
                          max_height=args.height,
                          quality=args.quality,
                          strip=not args.no_strip,
                          max_size=args.max_size,
                          dry_run=True)
            return

        if compress_image(input_path, output_path,
                         max_width=args.width,
                         max_height=args.height,
                         quality=args.quality,
                         strip=not args.no_strip,
                         max_size=args.max_size,
                         backup=args.backup):
            original_size = input_path.stat().st_size
            new_size = output_path.stat().st_size
            ratio = (1 - new_size/original_size) * 100
            print(f"✓ 完成: {original_size/1024:.1f}KB → {new_size/1024:.1f}KB ({ratio:.1f}% 减少)")
            print(f"输出: {output_path}")
        else:
            print("✗ 失败")
            sys.exit(1)


if __name__ == '__main__':
    main()
