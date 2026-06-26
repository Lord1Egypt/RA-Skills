#!/usr/bin/env python3
"""
Stage 3: 视频片段串联 + 交叉淡入淡出
输入：视频片段列表 + 封面片段
输出：串联后的无音频视频
"""
import argparse
import os
import re
import subprocess
import sys
import tempfile

FFMPEG = os.path.expanduser("~/bin/ffmpeg")


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


def xfade_pair(clip_a, clip_b, fade_dur, tmp_dir, idx):
    """两个片段交叉淡入淡出"""
    out = os.path.join(tmp_dir, f"xf_{idx:03d}.mp4")
    dur_a = get_duration(clip_a)
    offset = dur_a - fade_dur  # 从 clip_a 结束前 fade_dur 开始转场
    
    cmd = [
        FFMPEG, '-y',
        '-i', clip_a, '-i', clip_b,
        '-filter_complex',
        f"[0:v][1:v]xfade=transition=fade:duration={fade_dur}:offset={offset}[v]",
        '-map', '[v]',
        '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-preset', 'fast',
        out
    ]
    subprocess.run(cmd, capture_output=True, text=True)
    return out


def main():
    p = argparse.ArgumentParser(description="Stage 3: 串联 + 交叉淡入淡出")
    p.add_argument("--cover", required=True, help="封面片段路径")
    p.add_argument("--clips", required=True, nargs='+', help="场景片段路径列表（按顺序）")
    p.add_argument("--output", required=True, help="输出串联视频")
    p.add_argument("--fade-duration", type=float, default=0.8, help="淡入淡出时长(秒)")
    args = p.parse_args()

    # 所有片段：封面 + 场景
    all_clips = [args.cover] + args.clips
    print(f"🔗 Concatenating {len(all_clips)} clips (fade: {args.fade_duration}s)")

    tmp = tempfile.mkdtemp(prefix="qiqi_xfade_")
    current = all_clips[0]

    for i in range(1, len(all_clips)):
        next_clip = xfade_pair(current, all_clips[i], args.fade_duration, tmp, i-1)
        dur = get_duration(next_clip)
        print(f"  🔗 After xfade {i}/{len(all_clips)-1}: {dur:.1f}s")
        current = next_clip

    # 最终输出
    os.makedirs(os.path.dirname(args.output) or '.', exist_ok=True)
    subprocess.run(['cp', current, args.output], capture_output=True)
    
    final_dur = get_duration(args.output)
    print(f"✅ Concat output: {args.output} ({final_dur:.1f}s)")


if __name__ == "__main__":
    main()
