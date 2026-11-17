#!/usr/bin/env python3
"""douyin_download.py — 抖音视频下载去水印 + 提取音频

OpenClaw 专用 skill 的确定性脚本：只做 LLM 做不了的外部命令工作。
下载用 yt-dlp（从抖音 API 获取无水印源），音频提取用 ffmpeg。
转写和总结交给 OpenClaw 运行时（ASR skill + LLM 本身）。

零第三方依赖（仅标准库）。

用法:
  python3 douyin_download.py <抖音链接> [-o 输出目录]

输出:
  <输出目录>/video.mp4   无水印视频
  <输出目录>/audio.mp3   音频（给 ASR skill 用）
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def run(cmd, **kw):
    """运行外部命令，失败抛异常。"""
    return subprocess.run(cmd, check=True, **kw)


def check_bin(name):
    return shutil.which(name) is not None


def die(msg, code=1):
    print(f"❌ {msg}", file=sys.stderr)
    sys.exit(code)


def download_video(url, out_dir):
    """用 yt-dlp 下载抖音无水印视频。

    yt-dlp 的 Douyin extractor 从抖音 API 获取 play_addr（无水印源），
    所以下载下来的就是无水印视频。需要浏览器 fresh cookies（无需登录态）。
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    video_path = out_dir / "video.mp4"

    if video_path.exists():
        print(f"  ↳ 视频已存在，跳过下载: {video_path}")
        return str(video_path)

    print(f"  ↳ 下载视频: {url}")
    cmd = [
        "yt-dlp",
        "-o", str(video_path),
        "--no-playlist",
        "--no-warnings",
        "-f", "best[ext=mp4]/best",
    ]

    # 抖音/B站需要浏览器 cookies
    if "douyin" in url or "v.douyin" in url:
        print("  ↳ 检测到抖音链接，自动从浏览器导入 cookies")
        for browser in ("chrome", "safari", "firefox"):
            test_cmd = ["yt-dlp", "--cookies-from-browser", browser,
                        "--no-warnings", "-F", url]
            try:
                subprocess.run(test_cmd, capture_output=True, timeout=30)
                cmd.extend(["--cookies-from-browser", browser])
                print(f"  ↳ 使用 {browser} cookies")
                break
            except Exception:
                continue

    cmd.append(url)
    print(f"  $ {' '.join(cmd)}")
    run(cmd)
    print(f"  ✅ 已下载: {video_path}")
    return str(video_path)


def extract_audio(video_path, out_dir):
    """用 ffmpeg 提取音频为 MP3（给 ASR skill 用的标准中间格式）。

    用 MP3 而非 WAV：体积小（15分钟视频 ~3MB vs WAV ~30MB），
    且 huo15-openclaw-asr skill 的标准输入就是 MP3。
    """
    audio_path = Path(out_dir) / "audio.mp3"
    if audio_path.exists():
        print(f"  ↳ 音频已存在: {audio_path}")
        return str(audio_path)

    print(f"  ↳ 提取音频: {video_path} → {audio_path}")
    cmd = [
        "ffmpeg", "-y", "-i", video_path,
        "-vn", "-acodec", "libmp3lame", "-q:a", "2",
        str(audio_path),
    ]
    run(cmd, capture_output=True)
    print(f"  ✅ 音频: {audio_path}")
    return str(audio_path)


def main():
    parser = argparse.ArgumentParser(
        description="抖音视频下载去水印 + 提取音频（OpenClaw skill 确定性脚本）",
    )
    parser.add_argument("url", help="抖音视频链接")
    parser.add_argument("-o", "--output", default="./output",
                        help="输出目录（默认 ./output）")
    args = parser.parse_args()

    if not check_bin("yt-dlp"):
        die("yt-dlp 未安装。macOS: brew install yt-dlp")
    if not check_bin("ffmpeg"):
        die("ffmpeg 未安装。macOS: brew install ffmpeg")

    print(f"\n🎬 抖音视频下载去水印\n   链接: {args.url}\n   输出: {args.output}\n")

    video_path = download_video(args.url, args.output)
    audio_path = extract_audio(video_path, args.output)

    print(f"\n{'═' * 50}")
    print(f"  📦 下载完成")
    print(f"{'═' * 50}")
    print(f"  📹 无水印视频: {video_path}")
    print(f"  🎵 音频(MP3): {audio_path}")
    print(f"{'═' * 50}")
    print(f"\n👉 下一步: 用 huo15-openclaw-asr 转写 {audio_path}")
    print(f"   然后由 OpenClaw 对转录文本做内容总结。\n")


if __name__ == "__main__":
    main()
