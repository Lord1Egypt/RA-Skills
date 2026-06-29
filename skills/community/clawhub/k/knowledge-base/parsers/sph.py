#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频号下载（sph-download 自研方案）
用法: python sph.py <视频号分享链接> [--output-dir <目录>]
"""

import sys
import json
import argparse
import urllib.request
import urllib.error
from pathlib import Path


PARSER_ENDPOINT = "https://sph.litao.workers.dev/api/fetch_video_profile"


def fix_mojibake(value):
    """修复 latin1 编码的utf-8字符串"""
    if not isinstance(value, str):
        return value
    try:
        return value.encode("latin1").decode("utf-8")
    except (UnicodeError, LookupError):
        return value


def fetch_profile(url: str, timeout: int = 60) -> dict:
    """调用解析 API 获取视频信息"""
    payload = json.dumps({"url": url}).encode("utf-8")
    request = urllib.request.Request(
        PARSER_ENDPOINT,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "KnowledgeBase-Skill/2.1",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def download_video(video_url: str, output_path: Path, timeout: int = 300):
    """直接 HTTP 下载，稳定可靠"""
    request = urllib.request.Request(video_url, headers={"User-Agent": "Mozilla/5.0"})
    downloaded = 0
    with urllib.request.urlopen(request, timeout=timeout) as response, output_path.open("wb") as f:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            f.write(chunk)
            downloaded += len(chunk)
    return downloaded


def download(url: str, output_dir: Path) -> dict:
    """下载视频号视频，返回 {title, path, author, size}"""
    output_dir.mkdir(parents=True, exist_ok=True)

    video_id = url.rstrip("/").split("/")[-1].split("?")[0]
    video_path = output_dir / f"{video_id}.mp4"

    # 1. 解析
    print(f"  [解析] {url[:60]}")
    try:
        profile = fetch_profile(url)
    except (urllib.error.URLError, json.JSONDecodeError) as e:
        raise RuntimeError(f"解析失败: {e}")

    feed = profile.get("data", {}).get("feedInfo", {})
    author_info = profile.get("data", {}).get("authorInfo", {})
    video_url = feed.get("videoUrl")
    title = fix_mojibake(feed.get("description")) or video_id
    author = fix_mojibake(author_info.get("nickname")) or "unknown"

    if not video_url:
        raise RuntimeError("未获取到 videoUrl，解析失败")

    # 2. 下载
    print(f"  [下载] {title[:40]}")
    size = download_video(video_url, video_path)
    print(f"  [完成] {size // 1024}KB")

    return {
        "title": title,
        "author": author,
        "video": str(video_path),
        "size_bytes": size,
    }


def main():
    parser = argparse.ArgumentParser(description="视频号下载（sph-download 方案）")
    parser.add_argument("url", help="视频号分享链接 https://weixin.qq.com/sph/...")
    parser.add_argument("--output-dir", default=None, help="保存目录")
    args = parser.parse_args()

    output_dir = Path(args.output_dir) if args.output_dir else Path.home() / "Downloads" / "sph-downloads"
    url = args.url

    print(f"[视频号] 解析: {url}")
    result = download(url, output_dir)

    print(json.dumps({
        "title": result["title"],
        "author": result["author"],
        "video": result["video"],
        "size_bytes": result["size_bytes"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    raise SystemExit(main())
