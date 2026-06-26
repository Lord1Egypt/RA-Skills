#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Video-Gen: 从脚本 Markdown 生成视频号竖版短视频

依赖：
- TTS 工具（推荐 lh-edge-tts）
- templates/slide.html
- FFmpeg
- Chrome headless（仅在未提供 --images-dir 时需要）
"""

import os
import re
import sys
import json
import shlex
import shutil
import subprocess
import argparse
from pathlib import Path

# 路径自动检测（相对于脚本位置）
SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = SKILL_DIR / "templates"
TEMPLATE_HTML = TEMPLATES_DIR / "slide.html"

# 默认配置
DEFAULT_WIDTH = 1080
DEFAULT_HEIGHT = 1920  # 9:16 竖版
DEFAULT_VOICE = "zh-CN-YunxiNeural"
DEFAULT_RATE = "+0%"
DEFAULT_OUTPUT = "tmp/video-output.mp4"
TEMP_DIR = "tmp/video-gen-temp"


def _detect_tts():
    """自动检测 lh-edge-tts 路径"""
    sibling = SKILL_DIR.parent / "lh-edge-tts" / "scripts" / "tts_converter.py"
    if sibling.exists():
        return str(sibling)
    env_path = os.environ.get("EDGE_TTS_PATH")
    if env_path and Path(env_path).exists():
        return env_path
    return None


def _detect_chrome():
    """自动检测 Chrome 路径"""
    env_path = os.environ.get("CHROME_PATH")
    if env_path:
        if os.path.exists(env_path) or shutil.which(env_path):
            return env_path
    mac_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    if os.path.exists(mac_path):
        return mac_path
    for name in ["google-chrome", "google-chrome-stable", "chromium-browser", "chromium"]:
        found = shutil.which(name)
        if found:
            return found
    return None


def parse_args():
    parser = argparse.ArgumentParser(
        description="从脚本 Markdown 生成视频号竖版短视频",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  python3 generate.py script.md -o output.mp4
  python3 generate.py script.md -v zh-CN-XiaoxiaoNeural -r +10%
  python3 generate.py script.md --images-dir ./slides --keep-temp
  python3 generate.py script.md --tts-command "my-tts {text} -o {output}"
        """
    )
    parser.add_argument("script", help="脚本 Markdown 文件路径")
    parser.add_argument("-o", "--output", default=DEFAULT_OUTPUT, help=f"输出 MP4 路径（默认：{DEFAULT_OUTPUT}）")
    parser.add_argument("-v", "--voice", default=DEFAULT_VOICE, help=f"TTS 音色（默认：{DEFAULT_VOICE}）")
    parser.add_argument("-r", "--rate", default=DEFAULT_RATE, help=f"语速（默认：{DEFAULT_RATE}，如 +10%、-10%）")
    parser.add_argument("-w", "--width", type=int, default=DEFAULT_WIDTH, help=f"视频宽度（默认：{DEFAULT_WIDTH}）")
    parser.add_argument("--height", type=int, default=DEFAULT_HEIGHT, help=f"视频高度（默认：{DEFAULT_HEIGHT}）")
    parser.add_argument("--keep-temp", action="store_true", help="保留临时文件")
    parser.add_argument("--no-subs", action="store_true", help="不烧录字幕（字幕已渲染在图片中）")
    parser.add_argument("--images-dir", default=None,
                        help="使用已有图片目录（slide_01.png, slide_02.png...），跳过图片生成")
    parser.add_argument("--tts-command", default=None,
                        help="自定义 TTS 命令模板，占位符：{text} {output} {voice} {rate}。"
                             "默认自动检测 lh-edge-tts 或 EDGE_TTS_PATH 环境变量")
    return parser.parse_args()


def check_dependencies(args):
    """检查依赖工具是否可用"""
    missing = []

    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        missing.append("FFmpeg（需安装：brew install ffmpeg）")

    if not args.tts_command and not _detect_tts():
        missing.append("TTS（安装 lh-edge-tts 到同级目录，或设置 EDGE_TTS_PATH 环境变量）")

    if not args.images_dir:
        if not _detect_chrome():
            missing.append("Chrome（安装 Google Chrome，或设置 CHROME_PATH 环境变量）")
        if not TEMPLATE_HTML.exists():
            missing.append(f"模板文件（{TEMPLATE_HTML}）")

    if missing:
        print("缺少依赖：\n  " + "\n  ".join(missing))
        sys.exit(1)


def parse_script(script_path):
    """解析脚本 Markdown 文件"""
    with open(script_path, "r", encoding="utf-8") as f:
        content = f.read()

    sections_raw = re.split(r"^---+$", content, flags=re.MULTILINE)
    sections = []

    for section in sections_raw:
        section = section.strip()
        if not section:
            continue

        title_match = re.search(r"^#+\s*(.+)$", section, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else "未命名"

        dialogue_match = re.search(r"\*\*口播\*\*[:：]\s*(.+?)(?=\\n\\n|\*\*|$)", section, re.DOTALL)
        dialogue = dialogue_match.group(1).strip() if dialogue_match else ""

        subtitle_match = re.search(r"\*\*字幕\*\*[:：]\s*(.+?)(?=\\n\\n|\*\*|$)", section, re.DOTALL)
        subtitle = subtitle_match.group(1).strip() if subtitle_match else ""

        visual_match = re.search(r"\*\*画面\*\*[:：]\s*(.+?)(?=\\n\\n|\*\*|$)", section, re.DOTALL)
        visual = visual_match.group(1).strip() if visual_match else ""

        if dialogue or subtitle:
            sections.append({
                "title": title,
                "dialogue": dialogue,
                "subtitle": subtitle,
                "visual": visual,
            })

    if not sections:
        print("未解析到有效分段，请检查脚本格式")
        sys.exit(1)

    return sections


def generate_audio(dialogue, output_path, voice, rate, tts_command=None):
    """生成配音"""
    if tts_command:
        cmd_str = tts_command.format(
            text=shlex.quote(dialogue),
            output=shlex.quote(output_path),
            voice=shlex.quote(voice),
            rate=shlex.quote(rate),
        )
        result = subprocess.run(cmd_str, shell=True, capture_output=True, text=True)
    else:
        tts_path = _detect_tts()
        cmd = [
            "python3", tts_path,
            dialogue,
            "-v", voice,
            "-r", rate,
            "-o", output_path,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f" TTS 生成失败：{result.stderr}")
        sys.exit(1)

    return output_path


def generate_slide(subtitle, visual, output_path, width, height, index):
    """用 HTML 截图生成字幕卡片"""
    with open(TEMPLATE_HTML, "r", encoding="utf-8") as f:
        template = f.read()

    subtitle_html = subtitle.replace("\\n", "<br>").replace("\n", "<br>")
    visual_html = visual.replace("\\n", "<br>").replace("\n", "<br>")

    html = template.replace("{{SUBTITLE}}", subtitle_html)
    html = html.replace("{{VISUAL}}", visual_html)
    html = html.replace("{{INDEX}}", str(index))

    temp_html = Path(output_path).with_suffix(".html")
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html)

    chrome = _detect_chrome()
    cmd = [
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--screenshot=" + str(output_path),
        "--window-size=" + f"{width},{height}",
        "--hide-scrollbars",
        "--force-device-scale-factor=1",
        "file://" + str(temp_html.absolute()),
    ]

    subprocess.run(cmd, capture_output=True)
    temp_html.unlink()

    if not os.path.exists(output_path):
        print(f" 图片生成失败：{output_path}")
        sys.exit(1)

    return output_path


def get_audio_duration(audio_path):
    """获取音频时长（秒）"""
    cmd = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "json",
        audio_path,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(result.stdout)
    return float(data["format"]["duration"])


def compose_segment(image_path, audio_path, output_path):
    """图 + 音频合成视频片段"""
    cmd = [
        "ffmpeg",
        "-y",
        "-loop", "1",
        "-i", image_path,
        "-i", audio_path,
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-c:a", "aac",
        "-pix_fmt", "yuv420p",
        "-shortest",
        output_path,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f" 片段合成失败：{result.stderr}")
        sys.exit(1)

    return output_path


def concat_segments(segment_paths, output_path):
    """拼接多个视频片段"""
    concat_list = Path(output_path).parent / "concat_list.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for seg in segment_paths:
            f.write(f"file '{seg.absolute()}'\n")

    cmd = [
        "ffmpeg",
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        output_path,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f" 视频拼接失败：{result.stderr}")
        sys.exit(1)

    if concat_list.exists():
        concat_list.unlink()

    return output_path


def get_video_duration(video_path):
    """获取视频时长（秒）"""
    cmd = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "json",
        video_path,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(result.stdout)
    return float(data["format"]["duration"])


def main():
    args = parse_args()

    check_dependencies(args)

    temp_dir = Path(args.output).parent / TEMP_DIR
    temp_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"Video-Gen: 从脚本生成视频")
    print(f"{'='*60}\n")

    # 解析脚本
    print("[1/3] 解析脚本...")
    sections = parse_script(args.script)
    print(f"  解析到 {len(sections)} 个分段")

    # 生成素材
    print("\n[2/3] 生成素材...")
    segment_files = []

    for i, section in enumerate(sections, 1):
        print(f"\n  - 分段 {i}（{section['title']}）：")

        # 生成配音
        audio_output = temp_dir / f"audio_{i:02d}.mp3"
        print(f"    生成配音 mp3...", end="", flush=True)
        generate_audio(section["dialogue"], str(audio_output), args.voice, args.rate, args.tts_command)
        duration = get_audio_duration(str(audio_output))
        print(f" {duration:.1f}s")

        # 生成/加载字幕卡
        image_output = temp_dir / f"slide_{i:02d}.png"
        if args.images_dir:
            src = Path(args.images_dir) / f"slide_{i:02d}.png"
            if not src.exists():
                print(f"    图片不存在：{src}")
                sys.exit(1)
            shutil.copy2(str(src), str(image_output))
            print(f"    使用预制图片：{src}")
        else:
            print(f"    生成字幕卡...", end="", flush=True)
            generate_slide(section["subtitle"], section["visual"], str(image_output),
                           args.width, args.height, i)
            print(" done")

        # 合成片段
        segment_output = temp_dir / f"seg_{i:02d}.mp4"
        compose_segment(str(image_output), str(audio_output), str(segment_output))
        segment_files.append(segment_output)

    # 合成视频
    print("\n[3/3] 合成视频...")

    print(f"  拼接视频：{args.output}...", end="", flush=True)
    concat_segments(segment_files, args.output)
    print(" done")

    total_duration = get_video_duration(args.output)

    if not args.keep_temp:
        print(f"\n  清理临时文件：{temp_dir}", end="", flush=True)
        shutil.rmtree(temp_dir)
        print(" done")

    print(f"\n{'='*60}")
    print(f"完成！输出：{args.output}")
    print(f"  总时长：{total_duration:.1f}秒")
    print(f"  画幅：{args.width}x{args.height}（{(args.height/args.width):.2f}:1）")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
