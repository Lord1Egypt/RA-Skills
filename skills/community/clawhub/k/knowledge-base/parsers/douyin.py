#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抖音视频下载器（yt-dlp 方案）
支持：视频下载 + 文案提取（description/旁白/字幕）
用法: python douyin.py <抖音链接> [--output-dir <目录>]
"""

import sys
import json
import argparse
import subprocess
import re
from pathlib import Path
from urllib.parse import urlparse, parse_qs


def extract_douyin_url(text: str) -> str:
    """从文本中提取抖音链接"""
    patterns = [
        r"https?://v\.douyin\.com/\w+",
        r"https?://www\.douyin\.com/video/\d+",
        r"https?://www\.douyin\.com/[\w/]+",
    ]
    for p in patterns:
        m = re.search(p, text)
        if m:
            return m.group()
    return text.strip()


def _safe_filename(s: str) -> str:
    """去除文件名非法字符"""
    return re.sub(r'[\\/:*?"<>|]', '_', s)


def _extract_description(url: str) -> str:
    """通过 yt-dlp --dump-json 提取视频描述（文案旁白）"""
    try:
        r = subprocess.run(
            ["yt-dlp", "--dump-json", "--no-playlist", url],
            capture_output=True, text=True, timeout=30
        )
        if r.returncode == 0 and r.stdout.strip():
            info = json.loads(r.stdout.strip())
            return info.get("description", "")
    except Exception:
        pass
    return ""


def download(url: str, output_dir: Path) -> dict:
    """使用 yt-dlp 下载抖音视频 + 文案提取，返回 {title, description, author, path, size}"""
    output_dir.mkdir(parents=True, exist_ok=True)

    # ── 步骤 1: 提取元数据（标题 + 作者 + 文案） ──
    meta_cmd = [
        "yt-dlp",
        "--get-title",
        "--get-duration",
        "--get-filename",
        "-o", "%(title).s|||%(uploader)s",
        url,
    ]
    try:
        r = subprocess.run(meta_cmd, capture_output=True, text=True, timeout=30)
        lines = [l.strip() for l in r.stdout.strip().split("\n") if l.strip()]
        title = lines[0] if len(lines) > 0 else "douyin_video"
        author = lines[-1].split("|||")[-1] if "|||" in lines[-1] else "unknown"
    except Exception:
        title = "douyin_video"
        author = "unknown"

    # 提取文案（视频描述/旁白文字）
    print(f"  [文案] 提取视频描述...")
    description = _extract_description(url)
    if description:
        print(f"  [文案] 获取到文案 ({len(description)} 字): {description[:60]}...")
    else:
        print(f"  [文案] 未获取到描述文字")

    # ── 步骤 2: 下载视频 ──
    outtmpl = str(output_dir / "%(id)s.%(ext)s")
    dl_cmd = [
        "yt-dlp",
        "-f", "bestvideo+bestaudio/best",
        "--merge-output-format", "mp4",
        "-o", outtmpl,
        "--no-playlist",
        url,
    ]
    print(f"  [yt-dlp] 下载中...")
    r = subprocess.run(dl_cmd, capture_output=True, text=True, timeout=300)
    
    if r.returncode != 0:
        print(f"  [yt-dlp] 首次尝试失败，尝试简化方案...")
        dl_cmd2 = ["yt-dlp", "-o", outtmpl, "--no-playlist", url]
        r = subprocess.run(dl_cmd2, capture_output=True, text=True, timeout=300)
    
    if r.returncode != 0:
        raise RuntimeError(f"yt-dlp 下载失败: {r.stderr[:300]}")

    # ── 步骤 3: 定位下载文件 ──
    downloaded_path = None
    for line in r.stdout.split("\n"):
        if "Destination:" in line or "has already been downloaded" in line:
            f = line.split(": ", 1)[-1].strip()
            if Path(f).exists():
                downloaded_path = Path(f)
                break
    
    if not downloaded_path:
        for f in output_dir.iterdir():
            if f.suffix in (".mp4", ".webm", ".mkv", ".flv"):
                downloaded_path = f
                break

    if not downloaded_path or not downloaded_path.exists():
        raise FileNotFoundError("找不到下载后的视频文件")

    # ── 步骤 4: 保存文案为旁白文件 ──
    if description:
        caption_path = downloaded_path.with_suffix(".caption.txt")
        caption_path.write_text(description, encoding="utf-8")
        print(f"  [文案] 已保存旁白: {caption_path.name}")

    size = downloaded_path.stat().st_size
    print(f"  [完成] {title[:40]} ({size // 1024}KB)")
    return {
        "title": title,
        "author": author,
        "video": str(downloaded_path),
        "size_bytes": size,
        "description": description,
    }


def main():
    parser = argparse.ArgumentParser(description="抖音视频下载 + 文案提取（yt-dlp 方案）")
    parser.add_argument("url", help="抖音分享链接")
    parser.add_argument("--output-dir", default=None, help="保存目录")
    args = parser.parse_args()

    output_dir = Path(args.output_dir) if args.output_dir else Path.home() / "Downloads" / "douyin-downloads"
    url = extract_douyin_url(args.url)

    print(f"[抖音] 解析: {url[:60]}")
    result = download(url, output_dir)

    output = {
        "title": result["title"],
        "author": result["author"],
        "video": result["video"],
        "size_bytes": result["size_bytes"],
        "description": result.get("description", ""),
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    raise SystemExit(main())
