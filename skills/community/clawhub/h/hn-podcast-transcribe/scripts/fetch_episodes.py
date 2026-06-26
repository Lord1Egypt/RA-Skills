#!/usr/bin/env python3
"""Fetch new podcast episodes from RSS feed and download audio.

Supports multiple download strategies:
1. Direct HTTP download (works for most podcast CDNs)
2. yt-dlp fallback (handles some Cloudflare-protected hosts)
3. Manual mode: skip download, use pre-existing audio files

If a download fails, the episode directory is created with metadata only
so you can manually place the audio file.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from xml.etree import ElementTree

import requests

DEFAULT_RSS = "https://rss.buzzsprout.com/2170103.rss"
DEFAULT_ARCHIVE = os.environ.get("HN_ARCHIVE_DIR", "./hn-podcast-archive")

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return text[:80].strip("-")


def parse_rss(url: str) -> list[dict]:
    resp = requests.get(url, timeout=30, headers={"User-Agent": UA})
    resp.raise_for_status()
    root = ElementTree.fromstring(resp.content)
    episodes = []
    for item in root.iter("item"):
        title = item.findtext("title", "").strip()
        pub_date = item.findtext("pubDate", "").strip()
        desc = item.findtext("description", "").strip()
        enc = item.find("enclosure")
        audio_url = enc.get("url") if enc is not None else None
        link = item.findtext("link", "").strip()
        episodes.append({
            "title": title,
            "pub_date": pub_date,
            "description": desc,
            "audio_url": audio_url,
            "link": link,
        })
    return episodes


def existing_episodes(archive_dir: Path) -> set[str]:
    slugs = set()
    if not archive_dir.exists():
        return slugs
    for d in archive_dir.iterdir():
        if d.is_dir() and (d / "episode.json").exists():
            slugs.add(d.name)
    return slugs


def download_direct(url: str, dest: Path) -> bool:
    """Try direct HTTP download."""
    try:
        resp = requests.get(url, timeout=120, stream=True, headers={"User-Agent": UA})
        resp.raise_for_status()
        ct = resp.headers.get("content-type", "")
        if "audio" in ct or "octet-stream" in ct or url.endswith(".mp3"):
            with open(dest, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
    except Exception:
        pass
    return False


def download_ytdlp(url: str, dest: Path) -> bool:
    """Try yt-dlp download (handles some Cloudflare cases)."""
    if not shutil.which("yt-dlp"):
        return False
    try:
        result = subprocess.run(
            ["yt-dlp", "--no-check-certificates", "-f", "bestaudio",
             "--extractor-args", "generic:impersonate",
             "-o", str(dest), url],
            capture_output=True, text=True, timeout=120
        )
        return result.returncode == 0 and dest.exists()
    except Exception:
        return False


def fetch_episodes(rss_url: str, archive_dir: str, limit: int = 0, no_download: bool = False) -> list[str]:
    archive = Path(archive_dir)
    archive.mkdir(parents=True, exist_ok=True)

    print(f"Fetching RSS: {rss_url}")
    episodes = parse_rss(rss_url)
    existing = existing_episodes(archive)
    print(f"Found {len(episodes)} episodes in feed, {len(existing)} already archived")

    new_dirs = []
    count = 0
    for ep in episodes:
        if not ep["audio_url"]:
            continue

        slug = slugify(ep["title"])
        date_prefix = ""
        try:
            from email.utils import parsedate_to_datetime
            dt = parsedate_to_datetime(ep["pub_date"])
            date_prefix = dt.strftime("%Y-%m-%d")
        except Exception:
            pass
        dir_name = f"{date_prefix}_{slug}" if date_prefix else slug
        if dir_name in existing:
            continue

        ep_dir = archive / dir_name
        ep_dir.mkdir(exist_ok=True)

        # Save metadata
        meta = {k: v for k, v in ep.items() if k != "audio_url"}
        meta["slug"] = dir_name
        with open(ep_dir / "episode.json", "w") as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)

        if no_download:
            print(f"  Metadata only: {ep['title']}")
            new_dirs.append(str(ep_dir))
            count += 1
            continue

        # Download audio
        print(f"  Downloading: {ep['title']}")
        audio_dest = ep_dir / "audio.mp3"
        success = download_direct(ep["audio_url"], audio_dest)
        if not success:
            print(f"    Direct download failed, trying yt-dlp...")
            success = download_ytdlp(ep["audio_url"], audio_dest)

        if success:
            print(f"    ✓ Saved to {audio_dest}")
            new_dirs.append(str(ep_dir))
        else:
            print(f"    ✗ Download failed. Place audio manually at: {audio_dest}")
            meta["download_failed"] = True
            with open(ep_dir / "episode.json", "w") as f:
                json.dump(meta, f, indent=2, ensure_ascii=False)
            new_dirs.append(str(ep_dir))

        count += 1
        if limit and count >= limit:
            break

    print(f"Processed {count} episodes ({limit} limit)" if limit else f"Processed {count} new episodes")
    return new_dirs


def main():
    parser = argparse.ArgumentParser(description="Fetch podcast episodes from RSS")
    parser.add_argument("--rss", default=os.environ.get("HN_PODCAST_RSS", DEFAULT_RSS))
    parser.add_argument("--archive", default=DEFAULT_ARCHIVE)
    parser.add_argument("--limit", type=int, default=0, help="Max new episodes to download (0=all)")
    parser.add_argument("--no-download", action="store_true", help="Only save metadata, skip audio download")
    args = parser.parse_args()
    fetch_episodes(args.rss, args.archive, args.limit, args.no_download)


if __name__ == "__main__":
    main()
