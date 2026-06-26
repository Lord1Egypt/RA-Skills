#!/usr/bin/env python3
"""
youtube.py — Track YouTube creators, fetch recent videos, transcribe, summarize.

Tracks specific YouTube creators and fetches recent videos + transcripts
via yt-dlp without needing the YouTube Data API.

Usage:
    python3 -m feed.source.youtube
    python3 -m feed.source.youtube --days 3 --output feed/raw/youtube_feed.json
    python3 -m feed.source.youtube --dry-run
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List

_SCRIPTS_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_SCRIPTS_ROOT))

from config import load_config
from feed.source.x import classify
from feed.utils import STOPWORDS

_CFG = load_config()

DEFAULT_SOURCES_FILE = _CFG["sources_file"]

from lib import youtube_yt  # noqa: E402

SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")


def parse_creators(path: Path) -> List[Dict[str, str]]:
    """Parse sources.json for YouTube creators (supports both old and new format)."""
    if not path.exists():
        return []
    with path.open() as f:
        data = json.load(f)
    creators = []
    # New format: feed_sources array with type discriminator
    if "feed_sources" in data:
        entries = [s for s in data["feed_sources"] if s.get("type") == "youtube"]
    else:
        # Legacy format
        entries = data.get("youtube_creators", [])
    for entry in entries:
        url = entry.get("url", "")
        if not url:
            continue
        creators.append({
            "name": entry.get("name", url),
            "url": normalize_channel_url(url),
            "description": entry.get("description", ""),
        })
    return creators


def normalize_channel_url(url: str) -> str:
    cleaned = url.rstrip("/")
    cleaned = re.sub(r"/(featured|streams|shorts|playlists|community|about|videos)$", "", cleaned)
    if "youtu.be/" in cleaned and "/@" not in cleaned:
        return cleaned
    return cleaned + "/videos"


def fetch_creator_videos(url: str, since_date: str, max_videos: int) -> Dict[str, object]:
    cmd = [
        "yt-dlp",
        "--dump-json",
        "--no-warnings",
        "--no-download",
        "--ignore-errors",
        "--playlist-end", str(max_videos),
        "--dateafter", since_date.replace("-", ""),
        url,
    ]

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    except subprocess.TimeoutExpired:
        print(f"[youtube] yt-dlp timed out after 60s", file=sys.stderr)
        return {}
    if proc.returncode != 0 and not proc.stdout.strip():
        error = (proc.stderr or proc.stdout or "yt-dlp failed").strip().splitlines()[:1]
        return {"items": [], "error": error[0] if error else "yt-dlp failed"}

    items = []
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            video = json.loads(line)
        except json.JSONDecodeError:
            continue

        video_id = video.get("id", "")
        upload_date = video.get("upload_date") or ""
        date_str = ""
        if len(upload_date) == 8:
            date_str = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:8]}"

        items.append({
            "video_id": video_id,
            "title": video.get("title", ""),
            "url": video.get("webpage_url") or f"https://www.youtube.com/watch?v={video_id}",
            "channel_name": video.get("channel") or video.get("uploader") or "",
            "date": date_str,
            "engagement": {
                "views": video.get("view_count") or 0,
                "likes": video.get("like_count") or 0,
                "comments": video.get("comment_count") or 0,
            },
            "duration": video.get("duration"),
        })

    items.sort(key=lambda item: (item["date"], item["engagement"]["views"]), reverse=True)
    return {"items": items}


def _tokenize(text: str) -> List[str]:
    return [
        token for token in re.findall(r"[a-z0-9]+", text.lower())
        if len(token) > 2 and token not in STOPWORDS
    ]


def summarize_video(title: str, transcript: str, max_sentences: int = 3) -> str:
    text = (transcript or "").strip()
    if not text:
        return title.strip()

    sentences = [s.strip() for s in SENTENCE_RE.split(text) if s.strip()]
    if not sentences:
        words = text.split()
        return " ".join(words[:50]).strip()

    title_tokens = set(_tokenize(title))
    all_tokens = _tokenize(text)
    token_freq: Dict[str, int] = {}
    for token in all_tokens:
        token_freq[token] = token_freq.get(token, 0) + 1

    ranked = []
    for index, sentence in enumerate(sentences):
        sent_tokens = _tokenize(sentence)
        if not sent_tokens:
            continue
        overlap = len(set(sent_tokens) & title_tokens)
        density = sum(token_freq.get(token, 0) for token in sent_tokens) / len(sent_tokens)
        early_bonus = max(0, 3 - index) * 0.15
        ranked.append((overlap * 2 + density + early_bonus, index, sentence))

    if not ranked:
        return title.strip()

    chosen = sorted(sorted(ranked, reverse=True)[:max_sentences], key=lambda item: item[1])
    summary = " ".join(sentence for _, _, sentence in chosen)
    words = summary.split()
    if len(words) > 80:
        summary = " ".join(words[:80]).rstrip() + "..."
    return summary


def build_feed_items(creators: List[Dict[str, str]], days: int, max_videos: int) -> List[Dict[str, object]]:
    since_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    all_videos: List[Dict[str, object]] = []

    for creator in creators:
        result = fetch_creator_videos(creator["url"], since_date, max_videos)
        for item in result.get("items", []):
            item["creator_name"] = creator["name"]
            item["creator_description"] = creator["description"]
            all_videos.append(item)

    unique_by_id: Dict[str, Dict[str, object]] = {}
    for item in all_videos:
        video_id = str(item.get("video_id") or item.get("url"))
        if video_id and video_id not in unique_by_id:
            unique_by_id[video_id] = item

    videos = list(unique_by_id.values())
    videos.sort(key=lambda item: (item.get("date", ""), item.get("engagement", {}).get("views") or 0), reverse=True)

    transcripts = youtube_yt.fetch_transcripts_parallel(
        [str(item["video_id"]) for item in videos if item.get("video_id")]
    )

    feed_items = []
    for item in videos:
        transcript = transcripts.get(str(item.get("video_id")), "") or ""
        title = str(item.get("title", "")).strip()
        summary = summarize_video(title, transcript)
        body_text = summary if summary else title
        topics = classify(f"{title}\n{transcript[:800]}")

        highlights = youtube_yt.extract_transcript_highlights(transcript, title)

        feed_items.append({
            "source": "youtube",
            "author": item.get("channel_name") or item.get("creator_name") or "",
            "title": title,
            "content": body_text,
            "post_type": "video",
            "url": item.get("url", ""),
            "topics": topics,
            "timestamp": item.get("date", ""),
            "views": item.get("engagement", {}).get("views", 0),
            "likes": item.get("engagement", {}).get("likes", 0),
            "replies": item.get("engagement", {}).get("comments", 0),
            "duration": item.get("duration"),
        })

    return feed_items


def main() -> None:
    parser = argparse.ArgumentParser(description="Track YouTube creators for the newsfeed skill")
    parser.add_argument("--file", default=str(DEFAULT_SOURCES_FILE), help="Path to SOURCES.md")
    parser.add_argument("--days", type=int, default=7, help="Only keep videos from the last N days")
    parser.add_argument("--max-videos-per-creator", type=int, default=3, help="Max recent videos to inspect per creator")
    parser.add_argument("--output", default=str(_CFG["feed_raw"] / "youtube_feed.json"), help="Output JSON path")
    parser.add_argument("--dry-run", action="store_true", help="Print parsed creators and exit")
    args = parser.parse_args()

    creators = parse_creators(Path(args.file))
    if args.dry_run:
        print(json.dumps(creators, indent=2))
        return

    if not creators:
        print("[]")
        return

    items = build_feed_items(creators, args.days, args.max_videos_per_creator)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(items, indent=2), encoding="utf-8")
    print(json.dumps(items, indent=2))


if __name__ == "__main__":
    main()
