#!/usr/bin/env python3
"""
琪琪 OPC 视频生产管线 — Ken Burns 方案

流程：
  [Stage 1] cover.py          → 封面图片
  [Stage 2] kenburns.py       → Ken Burns 动画片段
  [Stage 3] xfade.py          → 串联 + 交叉淡入淡出
  [Stage 4] audio_sub.py      → 添加音频 + ASS 字幕

每个 Stage 独立运行，可单独测试、升级、替换。
"""
import argparse
import glob
import os
import re
import subprocess
import sys
import tempfile
import shutil

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
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


def run_stage(stage_name, cmd, check=True):
    """运行一个 stage 脚本"""
    print(f"\n{'='*50}")
    print(f"  🎬 Stage {stage_name}")
    print(f"{'='*50}")
    result = subprocess.run(cmd, capture_output=False, text=True)
    if check and result.returncode != 0:
        print(f"❌ Stage {stage_name} 失败", file=sys.stderr)
        sys.exit(1)
    return result


def main():
    p = argparse.ArgumentParser(description="琪琪 OPC 视频管线")
    
    # 输入参数
    p.add_argument("--scenes-dir", required=True, help="场景图片目录 (scene_01.png, ...)")
    p.add_argument("--audio", required=True, help="旁白音频 MP3")
    p.add_argument("--ass", required=True, help="ASS 字幕文件")
    p.add_argument("--output", required=True, help="输出视频路径")
    
    # 可选参数
    p.add_argument("--title", default="玫瑰与告别")
    p.add_argument("--subtitle", default="琪琪遇见小王子")
    p.add_argument("--episode-id", default="S02E01")
    p.add_argument("--brand", default="琪琪的魔法故事屋")
    p.add_argument("--qiqi", default=os.path.expanduser("~/.openclaw/workspace/characters/qiqi_default.png"), help="琪琪角色图路径")
    p.add_argument("--cover-duration", type=float, default=4.0)
    p.add_argument("--fade-duration", type=float, default=0.8)
    p.add_argument("--width", type=int, default=1920)
    p.add_argument("--height", type=int, default=1080)
    p.add_argument("--keep-temp", action="store_true", help="保留临时文件")
    
    args = p.parse_args()

    # 确保输出目录存在
    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)

    # 创建临时工作目录
    work_dir = tempfile.mkdtemp(prefix="qiqi_pipeline_")
    print(f"📁 Work dir: {work_dir}")
    
    try:
        # 获取场景图片列表
        scenes = sorted(glob.glob(os.path.join(args.scenes_dir, "scene_*.png")))
        if not scenes:
            print(f"❌ 未找到场景图片: {args.scenes_dir}/scene_*.png", file=sys.stderr)
            sys.exit(1)
        
        audio_dur = get_duration(args.audio)
        story_dur = audio_dur - args.cover_duration
        per_scene = story_dur / len(scenes)
        print(f"📊 {len(scenes)} scenes | Audio: {audio_dur:.1f}s | Per scene: {per_scene:.1f}s")

        # ====== Stage 1: 封面 ======
        cover_out = os.path.join(work_dir, "cover.png")
        cover_cmd = [
            sys.executable, os.path.join(SCRIPT_DIR, "stage_cover.py"),
            "--output", cover_out,
            "--title", args.title,
            "--subtitle", args.subtitle,
            "--episode-id", args.episode_id,
            "--brand", args.brand,
            "--width", str(args.width),
            "--height", str(args.height),
        ]
        if os.path.exists(args.qiqi):
            cover_cmd += ["--qiqi", args.qiqi]
        run_stage("1/4: 封面", cover_cmd)

        # ====== Stage 2: Ken Burns ======
        kb_dir = os.path.join(work_dir, "kb_clips")
        kb_args = " ".join(f'"{s}"' for s in scenes)
        run_stage("2/4: Ken Burns", [
            sys.executable, os.path.join(SCRIPT_DIR, "stage_kenburns.py"),
            "--scenes"] + scenes + [
            "--output-dir", kb_dir,
            "--per-scene-duration", str(per_scene),
        ])

        # 获取生成的 KB 片段（按顺序）
        kb_clips = sorted(glob.glob(os.path.join(kb_dir, "kb_*.mp4")))
        if len(kb_clips) != len(scenes):
            print(f"⚠️ Expected {len(scenes)} KB clips, got {len(kb_clips)}")

        # ====== Stage 3: 串联 + 交叉淡入淡出 ======
        concat_out = os.path.join(work_dir, "concat.mp4")
        cover_clip_path = os.path.join(work_dir, "cover_clip.mp4")
        
        # 先把封面做成视频片段
        subprocess.run([
            FFMPEG, '-y', '-loop', '1', '-i', cover_out,
            '-vf', f'scale={args.width}:{args.height}:force_original_aspect_ratio=decrease,'
                   f'pad={args.width}:{args.height}:(ow-iw)/2:(oh-ih)/2:color=0x1a1a3e',
            '-t', str(args.cover_duration),
            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-preset', 'fast', '-an',
            cover_clip_path
        ], capture_output=True)
        
        run_stage("3/4: 串联", [
            sys.executable, os.path.join(SCRIPT_DIR, "stage_xfade.py"),
            "--cover", cover_clip_path,
            "--clips"] + kb_clips + [
            "--output", concat_out,
            "--fade-duration", str(args.fade_duration),
        ])

        # ====== Stage 4: 音频 + 字幕 ======
        run_stage("4/4: 音频+字幕", [
            sys.executable, os.path.join(SCRIPT_DIR, "stage_audio_sub.py"),
            "--video", concat_out,
            "--audio", args.audio,
            "--ass", args.ass,
            "--output", args.output,
        ])

        # 最终报告
        print(f"\n{'='*50}")
        print(f"  ✅ 管线完成")
        print(f"{'='*50}")
        sz = os.path.getsize(args.output)
        dur = get_duration(args.output)
        print(f"📁 {args.output}")
        print(f"📊 {sz/1024/1024:.1f}MB | {dur:.0f}s ({dur/60:.1f}min)")

    finally:
        if not args.keep_temp:
            shutil.rmtree(work_dir, ignore_errors=True)
        else:
            print(f"📁 Temp files kept: {work_dir}")


if __name__ == "__main__":
    main()
