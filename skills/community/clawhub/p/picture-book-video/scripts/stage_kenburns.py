#!/usr/bin/env python3
"""
Stage 2: Ken Burns 效果生成
输入：场景图片列表 + 每段目标时长
输出：Ken Burns MP4 片段目录
"""
import argparse
import os
import re
import subprocess
import sys

FFMPEG = os.path.expanduser("~/bin/ffmpeg")

# Ken Burns 运动模式轮换
KB_PATTERNS = [
    # (zoom_expr, x_expr, y_expr, zmax)
    ("1+0.0003*on",  "(iw-iw/zoom)/2", "(ih-ih/zoom)/2", "1.15"),        # 慢推
    ("1.15-0.0003*on", "(iw-iw/zoom)/2", "(ih-ih/zoom)/2", "1.15"),       # 慢拉
    ("1+0.0002*on",  "iw/2-(iw/zoom)/2+(iw/zoom)*0.1*sin(on*0.02)", "(ih-ih/zoom)/2", "1.1"),  # 慢推+微摇
    ("1.1-0.0002*on", "(iw-iw/zoom)/2", "(ih-ih/zoom)/2+0.05*ih*sin(on*0.015)", "1.1"),        # 慢拉+微上下
    ("1+0.0004*on",  "(iw-iw/zoom)/2-(iw/zoom)*0.1*on/(on+500)", "(ih-ih/zoom)/2", "1.15"),    # 慢推+右移
    ("1+0.00025*on", "(iw-iw/zoom)/2+(iw/zoom)*0.08*on/(on+400)", "(ih-ih/zoom)/2", "1.12"),   # 慢推+左移
    ("1+0.00015*on", "(iw-iw/zoom)/2", "(ih-ih/zoom)/2", "1.08"),         # 极慢推
    ("1.12-0.0003*on", "(iw-iw/zoom)/2", "(ih-ih/zoom)/2", "1.12"),       # 慢拉
]


def make_kb_clip(scene_img, target_dur, output_path, idx):
    """静态画面（取消 Ken Burns 缩放，避免视觉疲劳）"""
    # 直接静态画面 + 淡色背景填充，不再用 zoompan
    fallback_kb_clip(scene_img, target_dur, output_path)
    return True


def fallback_kb_clip(scene_img, target_dur, output_path):
    """备用：静态画面（缩放适配）"""
    subprocess.run([
        FFMPEG, '-y', '-loop', '1', '-i', scene_img,
        '-vf', 'scale=1920:1080:force_original_aspect_ratio=decrease,'
               'pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=0x1a1a3e',
        '-t', str(target_dur),
        '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-preset', 'fast',
        '-an', output_path
    ], capture_output=True)


def get_duration(path):
    result = subprocess.run(
        [FFMPEG, '-i', path, '-f', 'null', '-'],
        capture_output=True, text=True
    )
    m = re.search(r'Duration: (\d{2}):(\d{2}):(\d{2})\.(\d{2})', result.stderr)
    if m:
        h, mn, s, ms = m.groups()
        return int(h)*3600 + int(mn)*60 + int(s) + int(ms)/100
    return 0


def main():
    p = argparse.ArgumentParser(description="Stage 2: Ken Burns 生成")
    p.add_argument("--scenes", required=True, nargs='+', help="场景图片路径列表")
    p.add_argument("--output-dir", required=True, help="输出片段目录")
    p.add_argument("--per-scene-duration", type=float, required=True, help="每段时长(秒)")
    args = p.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    print(f"🎬 Ken Burns: {len(args.scenes)} scenes, {args.per_scene_duration:.1f}s each")

    for i, scene in enumerate(args.scenes):
        out_path = os.path.join(args.output_dir, f"kb_{i+1:03d}.mp4")
        ok = make_kb_clip(scene, args.per_scene_duration, out_path, i)
        dur = get_duration(out_path)
        status = "✅" if ok and abs(dur - args.per_scene_duration) < 1.0 else "⚠️"
        print(f"  {status} Scene {i+1}/{len(args.scenes)}: {os.path.basename(scene)} → {dur:.1f}s")

    # 输出摘要
    print(f"✅ {len(args.scenes)} Ken Burns clips → {args.output_dir}")


if __name__ == "__main__":
    main()
