#!/usr/bin/env python3
"""Video compression and conversion tool."""

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


def get_video_info(filepath):
    """Get video information using ffprobe."""
    cmd = [
        'ffprobe', '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height,duration',
        '-of', 'csv=p=0',
        filepath
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            parts = result.stdout.strip().split(',')
            return {
                'width': int(parts[0]),
                'height': int(parts[1]),
                'duration': float(parts[2]) if len(parts) > 2 else 0
            }
    except:
        pass
    return None


def compress_video(input_path, output_path, crf=23, preset='medium',
                   max_height=None, target_size=None, fps=None, audio_bitrate='128k',
                   dry_run=False, backup=False):
    """Compress a single video."""
    input_path = Path(input_path)
    output_path = Path(output_path)

    # Get video info
    info = get_video_info(input_path)

    # Backup original if requested
    if backup:
        backup_path = input_path.parent / f"{input_path.stem}.backup{input_path.suffix}"
        if not backup_path.exists():
            shutil.copy2(input_path, backup_path)
            print(f"  已备份原文件: {backup_path.name}")

    # Build command
    cmd = ['ffmpeg', '-y', '-i', str(input_path)]
    
    # Video filters
    filters = []
    
    if max_height and info:
        if info['height'] > max_height:
            filters.append(f'scale=-2:{max_height}')
    
    if fps:
        filters.append(f'fps={fps}')
    
    if filters:
        cmd.extend(['-vf', ','.join(filters)])
    
    # Video codec settings
    cmd.extend([
        '-c:v', 'libx264',
        '-crf', str(crf),
        '-preset', preset,
        '-movflags', '+faststart'  # Web optimization
    ])
    
    # Audio settings
    cmd.extend([
        '-c:a', 'aac',
        '-b:a', audio_bitrate
    ])
    
    # Output
    cmd.append(str(output_path))

    # Preview mode: estimate compression result
    if dry_run:
        print(f"\n  [预览模式] 不会实际压缩")
        print(f"  原文件: {input_path.name}")
        if info:
            print(f"  分辨率: {info['width']}x{info['height']}")
            print(f"  时长: {info['duration']:.1f}秒")
        print(f"  当前大小: {input_path.stat().st_size/1024/1024:.1f}MB")
        print(f"  设置参数:")
        print(f"    - CRF: {crf} (质量)")
        print(f"    - Preset: {preset} (编码速度)")
        if max_height:
            print(f"    - 最大高度: {max_height}px")
        if target_size:
            print(f"    - 目标大小: {target_size}")
        if fps:
            print(f"    - 帧率: {fps}fps")
        print(f"  预估: 压缩后约减少 30-70% 大小")
        return True

    # Execute
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"错误: {result.stderr}")
        return False
    
    # If target size specified, we may need to adjust
    if target_size:
        target_bytes = parse_size(target_size)
        current_size = output_path.stat().st_size
        
        if current_size > target_bytes * 1.1:  # Allow 10% tolerance
            print(f"当前大小: {current_size/1024/1024:.1f}MB, 目标: {target_bytes/1024/1024:.1f}MB")
            print("尝试提高 CRF 值...")
            
            # Calculate new CRF (rough approximation)
            new_crf = min(crf + 5, 35)
            if new_crf > crf:
                return compress_video(input_path, output_path, new_crf, preset, 
                                    max_height, target_size, fps, audio_bitrate)
    
    return True


def parse_size(size_str):
    """Parse size string like '50mb', '1gb' to bytes."""
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
    """Process all videos in a directory."""
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    video_exts = {'.mp4', '.mov', '.avi', '.mkv', '.webm', '.flv', '.wmv', '.m4v'}
    files = [f for f in input_dir.iterdir() if f.suffix.lower() in video_exts]

    print(f"找到 {len(files)} 个视频文件")

    for i, file in enumerate(files, 1):
        output_file = output_dir / f"{file.stem}.mp4"

        print(f"[{i}/{len(files)}] 处理: {file.name}")

        if compress_video(file, output_file, dry_run=dry_run, backup=backup, **kwargs):
            if dry_run:
                continue
            original_size = file.stat().st_size
            new_size = output_file.stat().st_size
            ratio = (1 - new_size/original_size) * 100
            print(f"  ✓ {original_size/1024/1024:.1f}MB → {new_size/1024/1024:.1f}MB ({ratio:.1f}% 减少)")
        else:
            print(f"  ✗ 失败")


def main():
    parser = argparse.ArgumentParser(description='压缩视频文件')
    parser.add_argument('input', help='输入文件或目录')
    parser.add_argument('--output', '-o', help='输出文件或目录')
    parser.add_argument('--crf', type=int, default=23, 
                       help='恒定质量因子 0-51, 越低越好 (默认: 23)')
    parser.add_argument('--preset', default='medium',
                       choices=['ultrafast', 'superfast', 'veryfast', 'faster', 
                               'fast', 'medium', 'slow', 'slower', 'veryslow'],
                       help='编码速度预设 (默认: medium)')
    parser.add_argument('--height', type=int, 
                       help='最大高度 (如 480, 720, 1080)')
    parser.add_argument('--target-size', help='目标大小 (如 50mb, 500mb)')
    parser.add_argument('--fps', type=int, help='限制帧率')
    parser.add_argument('--audio-bitrate', default='128k',
                       help='音频比特率 (默认: 128k)')
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
            'crf': args.crf,
            'preset': args.preset,
            'max_height': args.height,
            'target_size': args.target_size,
            'fps': args.fps,
            'audio_bitrate': args.audio_bitrate
        }
        process_batch(input_path, output_dir, dry_run=args.preview, backup=args.backup, **kwargs)
    else:
        # Single file mode
        if args.output:
            output_path = Path(args.output)
        else:
            output_path = input_path.parent / f"{input_path.stem}_compressed.mp4"
        
        print(f"压缩: {input_path}")

        if args.preview:
            compress_video(input_path, output_path,
                          crf=args.crf,
                          preset=args.preset,
                          max_height=args.height,
                          target_size=args.target_size,
                          fps=args.fps,
                          audio_bitrate=args.audio_bitrate,
                          dry_run=True)
            return

        if compress_video(input_path, output_path,
                         crf=args.crf,
                         preset=args.preset,
                         max_height=args.height,
                         target_size=args.target_size,
                         fps=args.fps,
                         audio_bitrate=args.audio_bitrate,
                         backup=args.backup):
            original_size = input_path.stat().st_size
            new_size = output_path.stat().st_size
            ratio = (1 - new_size/original_size) * 100
            print(f"✓ 完成: {original_size/1024/1024:.1f}MB → {new_size/1024/1024:.1f}MB ({ratio:.1f}% 减少)")
            print(f"输出: {output_path}")
        else:
            print("✗ 失败")
            sys.exit(1)


if __name__ == '__main__':
    main()
