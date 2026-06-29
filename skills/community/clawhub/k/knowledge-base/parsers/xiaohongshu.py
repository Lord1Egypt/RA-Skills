#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书笔记下载器（yt-dlp 方案）
用法: python xiaohongshu.py <小红书链接> [--output-dir <目录>]
"""

import sys
import json
import argparse
import subprocess
import re
from pathlib import Path


def extract_xhs_url(text: str) -> str:
    """从文本中提取小红书链接"""
    patterns = [
        r"https?://xhslink\.com/\S+",
        r"https?://www\.xiaohongshu\.com/\S+",
    ]
    for p in patterns:
        m = re.search(p, text)
        if m:
            return m.group().rstrip(".,;!?)")
    return text.strip()


def download(url: str, output_dir: Path) -> dict:
    """使用 yt-dlp 下载小红书笔记，返回 {title, path, author, size, type}"""
    output_dir.mkdir(parents=True, exist_ok=True)

    # 先获取元数据：标题 + 上传者
    meta_cmd = [
        "yt-dlp",
        "--get-title",
        "--get-filename",
        "-o", "%(title).s|||%(uploader)s",
        "--no-playlist",
        url,
    ]
    try:
        r = subprocess.run(meta_cmd, capture_output=True, text=True, timeout=30)
        lines = [l.strip() for l in r.stdout.strip().split("\n") if l.strip()]
        title = lines[0] if len(lines) > 0 else "xiaohongshu_note"
        author = lines[-1].split("|||")[-1] if "|||" in lines[-1] else "unknown"
    except Exception:
        title = "xiaohongshu_note"
        author = "unknown"

    # 下载：视频用 mp4 合并，图文也会被 yt-dlp 处理
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
        # 尝试简化方案
        print(f"  [yt-dlp] 首次尝试失败，尝试简化方案...")
        dl_cmd2 = ["yt-dlp", "-o", outtmpl, "--no-playlist", url]
        r = subprocess.run(dl_cmd2, capture_output=True, text=True, timeout=300)

    if r.returncode != 0:
        raise RuntimeError(f"yt-dlp 下载失败: {r.stderr[:300]}")

    # 找到下载的文件
    downloaded_path = None
    for line in r.stdout.split("\n") + r.stderr.split("\n"):
        if "Destination:" in line or "has already been downloaded" in line:
            f = line.split(": ", 1)[-1].strip()
            if Path(f).exists():
                downloaded_path = Path(f)
                break

    if not downloaded_path:
        # 按 id 或最新文件查找
        for f in sorted(output_dir.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True):
            if f.suffix.lower() in (".mp4", ".webm", ".mkv", ".flv", ".jpg", ".png", ".webp"):
                downloaded_path = f
                break

    if not downloaded_path or not downloaded_path.exists():
        raise FileNotFoundError("找不到下载后的文件")

    size = downloaded_path.stat().st_size
    ext = downloaded_path.suffix.lower()
    file_type = "mp4" if ext in (".mp4", ".webm", ".mkv", ".flv") else ext.strip(".")

    print(f"  [完成] {title[:40]} ({size // 1024}KB, {file_type})")
    return {
        "title": title,
        "path": str(downloaded_path),
        "author": author,
        "size": size,
        "type": file_type,
    }


def main():
    parser = argparse.ArgumentParser(description="小红书笔记下载（yt-dlp 方案）")
    parser.add_argument("url", help="小红书分享链接")
    parser.add_argument("--output-dir", default=None, help="保存目录")
    args = parser.parse_args()

    output_dir = Path(args.output_dir) if args.output_dir else Path.home() / "Downloads" / "xhs-downloads"
    url = extract_xhs_url(args.url)

    print(f"[小红书] 解析: {url[:80]}")
    result = download(url, output_dir)

    print(json.dumps({
        "title": result["title"],
        "author": result["author"],
        "file": result["path"],
        "size_bytes": result["size"],
        "type": result["type"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    raise SystemExit(main())
