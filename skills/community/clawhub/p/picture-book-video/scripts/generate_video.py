#!/usr/bin/env python3
"""
绘本故事视频 - 主管线脚本

输入：
  - 合集名称（可选）
  - 合集描述（可选）
  - 序列号（可选，如 S02E01）
  - 故事脚本（必需）

输出：
  - 中文视频 mp4
  - 英文视频 mp4
  - 抖音发布描述文件
"""
import argparse
import glob
import json
import os
import re
import subprocess
import sys
import tempfile
import shutil
from pathlib import Path

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FFMPEG = os.path.expanduser("~/bin/ffmpeg")

# 默认角色图路径
DEFAULT_QIQI = os.path.expanduser("~/.openclaw/workspace/characters/qiqi_default.png")


def get_duration(path):
    """获取视频/音频时长"""
    result = subprocess.run(
        [FFMPEG, '-i', path, '-f', 'null', '-'],
        capture_output=True, text=True
    )
    m = re.search(r'Duration: (\d{2}):(\d{2}):(\d{2})\.(\d{2})', result.stderr)
    if m:
        h, mn, s, ms = m.groups()
        return int(h)*3600 + int(mn)*60 + int(s) + int(ms)/100
    return 0


def run_stage(name, cmd):
    """运行一个阶段"""
    print(f"\n{'='*50}")
    print(f"  🎬 {name}")
    print(f"{'='*50}")
    result = subprocess.run(cmd, capture_output=False, text=True)
    if result.returncode != 0:
        print(f"❌ {name} 失败", file=sys.stderr)
        sys.exit(1)
    return result


def parse_script(script_path):
    """解析故事脚本，提取分镜信息"""
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    scenes = []
    current_scene = {}
    
    for line in content.split('\n'):
        line = line.strip()
        
        # 匹配场景标题
        scene_match = re.match(r'###\s*(?:SCENE\s*\d+|场景\s*\d+)(?:：|:)?\s*(.+)', line)
        if scene_match:
            if current_scene:
                scenes.append(current_scene)
            current_scene = {'title': scene_match.group(1), 'narration': '', 'prompt': '', 'animation': ''}
            continue
        
        # 匹配旁白
        narration_match = re.match(r'\*\*旁白\*\*(?:：|:)\s*(.+)', line)
        if narration_match:
            current_scene['narration'] = narration_match.group(1).strip()
            continue
        
        # 匹配画面 prompt
        prompt_match = re.match(r'\*\*画面(?:prompt)?\*\*(?:：|:)\s*(.+)', line)
        if prompt_match:
            current_scene['prompt'] = prompt_match.group(1).strip()
            continue
        
        # 匹配动画描述
        anim_match = re.match(r'\*\*动画\*\*(?:：|:)\s*(.+)', line)
        if anim_match:
            current_scene['animation'] = anim_match.group(1).strip()
    
    if current_scene:
        scenes.append(current_scene)
    
    return scenes


def generate_tts(text, output_mp3, output_srt, voice, rate="-15%"):
    """生成 TTS 旁白"""
    cmd = [
        sys.executable, os.path.join(SCRIPT_DIR, "tts.py"),
        "--text", text,
        "--output", output_mp3,
        "--srt", output_srt,
        "--voice", voice,
        f"--rate={rate}",
    ]
    run_stage(f"TTS: {voice}", cmd)


def generate_ass(srt_path, ass_path, font_size=80):
    """生成 ASS 字幕"""
    cmd = [
        sys.executable, os.path.join(SCRIPT_DIR, "srt_to_ass.py"),
        "--srt", srt_path,
        "--output", ass_path,
        "--font-size", str(font_size),
    ]
    run_stage(f"ASS: {os.path.basename(ass_path)}", cmd)


def run_pipeline(scenes_dir, audio, ass, output, title, subtitle, episode_id, brand="琪琪的魔法故事屋", qiqi=None, cover_duration=4.0, fade_duration=0.8):
    """运行完整管线"""
    if qiqi is None:
        qiqi = DEFAULT_QIQI
    
    cmd = [
        sys.executable, os.path.join(SCRIPT_DIR, "pipeline.py"),
        "--scenes-dir", scenes_dir,
        "--audio", audio,
        "--ass", ass,
        "--output", output,
        "--title", title,
        "--subtitle", subtitle,
        "--episode-id", episode_id,
        "--brand", brand,
        "--cover-duration", str(cover_duration),
        "--fade-duration", str(fade_duration),
    ]
    if os.path.exists(qiqi):
        cmd += ["--qiqi", qiqi]
    
    run_stage("管线合成", cmd)


def generate_publish_desc(episode_id, title_cn, title_en, subtitle_cn, subtitle_en, description_cn, description_en):
    """生成抖音发布描述"""
    return f"""# 抖音发布描述

## 基本信息
- 集号: {episode_id}

## 中文版
- 标题: {title_cn}｜{subtitle_cn}
- 描述: {description_cn}
- 话题: #儿童故事 #{subtitle_cn} #睡前故事 #绘本动画

## 英文版
- 标题: {title_en}｜{subtitle_en}
- 描述: {description_en}
- 话题: #英语启蒙 #磨耳朵英语 #{subtitle_en} #儿童英语
"""


def main():
    p = argparse.ArgumentParser(description="绘本故事视频管线")
    
    # 输入参数
    p.add_argument("--script", required=True, help="故事脚本文件路径")
    p.add_argument("--collection", default="琪琪的魔法故事屋", help="合集名称")
    p.add_argument("--collection-desc", default="", help="合集描述")
    p.add_argument("--episode-id", default=None, help="序列号（如 S02E01）")
    p.add_argument("--output-dir", default=None, help="输出目录")
    
    # 可选参数
    p.add_argument("--title-cn", default=None, help="中文标题")
    p.add_argument("--title-en", default=None, help="英文标题")
    p.add_argument("--qiqi", default=DEFAULT_QIQI, help="琪琪角色图路径")
    p.add_argument("--font-size", type=int, default=80, help="字幕字号")
    p.add_argument("--rate", default="-15%", help="TTS 语速调整")
    p.add_argument("--cover-duration", type=float, default=4.0, help="封面时长")
    p.add_argument("--fade-duration", type=float, default=0.8, help="溶解时长")
    p.add_argument("--keep-temp", action="store_true", help="保留临时文件")
    
    args = p.parse_args()
    
    # 解析脚本
    print(f"📖 解析脚本: {args.script}")
    scenes = parse_script(args.script)
    
    if not scenes:
        print("❌ 未找到场景信息", file=sys.stderr)
        sys.exit(1)
    
    print(f"✅ 解析到 {len(scenes)} 个场景")
    
    # 创建输出目录
    if args.output_dir is None:
        args.output_dir = os.path.join(
            os.path.expanduser("~/Videos/qiqi-opc"),
            args.episode_id or f"episode-{len(glob.glob('~/Videos/qiqi-opc/*/', recursive=True))}"
        )
    os.makedirs(args.output_dir, exist_ok=True)
    
    # 生成中英文旁白全文
    cn_narration = " ".join(s['narration'] for s in scenes if s.get('narration'))
    
    # 英文旁白（需要从脚本中提取或使用翻译）
    en_narration = ""
    for s in scenes:
        if s.get('narration_en'):
            en_narration += s['narration_en'] + " "
    
    if not en_narration:
        print("⚠️ 未找到英文旁白，需要用户提供或自动生成翻译")
        print("提示：可以在脚本中添加 **旁白(EN)** 字段提供英文旁白")
    
    # 提取标题
    title_cn = args.title_cn or os.path.basename(args.script).replace('.md', '')
    title_en = args.title_en or title_cn  # 默认使用中文标题
    
    # Phase 1: 生成 TTS
    print("\n🎤 Phase 1: 生成旁白...")
    
    if cn_narration:
        generate_tts(
            cn_narration,
            os.path.join(args.output_dir, "narration_cn.mp3"),
            os.path.join(args.output_dir, "narration_cn.srt"),
            "zh-CN-XiaoyiNeural",
            args.rate
        )
    
    if en_narration:
        generate_tts(
            en_narration.strip(),
            os.path.join(args.output_dir, "narration_en.mp3"),
            os.path.join(args.output_dir, "narration_en.srt"),
            "en-US-JennyNeural",
            args.rate
        )
    
    # Phase 2: 生成 ASS 字幕
    print("\n📝 Phase 2: 生成字幕...")
    
    if os.path.exists(os.path.join(args.output_dir, "narration_cn.srt")):
        generate_ass(
            os.path.join(args.output_dir, "narration_cn.srt"),
            os.path.join(args.output_dir, "subtitles_cn.ass"),
            args.font_size
        )
    
    if os.path.exists(os.path.join(args.output_dir, "narration_en.srt")):
        generate_ass(
            os.path.join(args.output_dir, "narration_en.srt"),
            os.path.join(args.output_dir, "subtitles_en.ass"),
            args.font_size
        )
    
    # Phase 3: 运行管线
    print("\n🎬 Phase 3: 视频合成...")
    
    # 中文版
    if os.path.exists(os.path.join(args.output_dir, "narration_cn.mp3")):
        run_pipeline(
            scenes_dir=args.output_dir,
            audio=os.path.join(args.output_dir, "narration_cn.mp3"),
            ass=os.path.join(args.output_dir, "subtitles_cn.ass"),
            output=os.path.join(args.output_dir, f"{args.episode_id}_cn.mp4"),
            title=title_cn,
            subtitle=args.collection,
            episode_id=args.episode_id or "EP01",
            qiqi=args.qiqi,
            cover_duration=args.cover_duration,
            fade_duration=args.fade_duration,
        )
    
    # 英文版
    if os.path.exists(os.path.join(args.output_dir, "narration_en.mp3")):
        run_pipeline(
            scenes_dir=args.output_dir,
            audio=os.path.join(args.output_dir, "narration_en.mp3"),
            ass=os.path.join(args.output_dir, "subtitles_en.ass"),
            output=os.path.join(args.output_dir, f"{args.episode_id}_en.mp4"),
            title=title_en,
            subtitle=args.collection,
            episode_id=args.episode_id or "EP01",
            qiqi=args.qiqi,
            cover_duration=args.cover_duration,
            fade_duration=args.fade_duration,
        )
    
    # Phase 4: 生成发布描述
    print("\n📋 Phase 4: 生成发布描述...")
    
    publish_desc = generate_publish_desc(
        args.episode_id or "EP01",
        title_cn,
        title_en,
        args.collection,
        args.collection,
        args.collection_desc or "",
        args.collection_desc or ""
    )
    
    publish_path = os.path.join(args.output_dir, "douyin_publish.md")
    with open(publish_path, 'w', encoding='utf-8') as f:
        f.write(publish_desc)
    
    print(f"✅ 发布描述: {publish_path}")
    
    # 最终报告
    print(f"\n{'='*50}")
    print(f"  ✅ 绘本故事视频生成完成")
    print(f"{'='*50}")
    print(f"📁 输出目录: {args.output_dir}")
    
    for f in glob.glob(os.path.join(args.output_dir, "*.mp4")):
        sz = os.path.getsize(f)
        dur = get_duration(f)
        print(f"📹 {os.path.basename(f)}: {sz/1024/1024:.1f}MB, {dur:.0f}s")
    
    if not args.keep_temp:
        # 清理临时文件（保留 mp4, mp3, srt, ass, md）
        for f in glob.glob(os.path.join(args.output_dir, "scene_*.png")):
            os.remove(f)
        print("🧹 临时场景图片已清理")
    
    print("\n📋 抖音发布:")
    print(f"  中文: {args.episode_id}_cn.mp4")
    print(f"  英文: {args.episode_id}_en.mp4")
    print(f"  描述: douyin_publish.md")


if __name__ == "__main__":
    main()
