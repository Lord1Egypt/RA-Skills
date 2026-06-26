"""YouTube channel handler -- channel videos.xml + youtube-transcript-api.

Crawls full transcripts into the knowledge base (distinct from feed/source/youtube.py
which produces short feed digest items via yt-dlp).
"""

import time
import feedparser

from .common import (
    DELAY,
    source_dir,
    existing_urls,
    make_filename,
    build_frontmatter,
)

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    _YT_API = YouTubeTranscriptApi()
except Exception as e:
    _YT_API = None
    print(f"! youtube-transcript-api unavailable: {e}")


def _channel_feed_url(ref: str) -> str:
    """Accept a bare channel ID (UC...) or a full videos.xml URL."""
    if ref.startswith("http"):
        return ref
    return f"https://www.youtube.com/feeds/videos.xml?channel_id={ref}"


def _fetch_transcript(video_id: str) -> str:
    """Return plain-text transcript or empty string on failure."""
    if _YT_API is None:
        return ""
    try:
        t = _YT_API.fetch(video_id)
        raw = t.to_raw_data()
        return "\n".join(seg["text"].strip() for seg in raw if seg.get("text"))
    except Exception as e:
        print(f"     ! transcript unavailable: {e}")
        return ""


def crawl(source: dict, max_articles: int = 0, recrawl: bool = False) -> int:
    key = source["key"]
    name = source["name"]
    author = source["author"]
    feed_url = _channel_feed_url(source["url"])

    out_dir = source_dir(key)
    out_dir.mkdir(parents=True, exist_ok=True)

    already = set() if recrawl else existing_urls(key)
    if already:
        print(f"   {len(already)} videos already saved -- skipping those")

    feed = feedparser.parse(feed_url)
    entries = feed.entries
    if not entries:
        print(f"   ! could not fetch YouTube feed: {feed_url}")
        return 0

    print(f"   {len(entries)} videos in feed")

    saved = 0
    for entry in entries:
        if max_articles and saved >= max_articles:
            break

        url = entry.get("link", "")
        if not url or url in already:
            continue

        video_id = entry.get("yt_videoid") or url.split("v=")[-1].split("&")[0]
        title = entry.get("title", "Untitled")
        date = entry.get("published", "")[:10] or ""
        if not date:
            import datetime as _dt
            date = _dt.date.today().strftime("%Y-%m-%d")

        filename = make_filename(date, video_id)
        dest = out_dir / filename
        if not recrawl and dest.exists():
            continue

        print(f"   -> {title[:60]}")
        transcript = _fetch_transcript(video_id)
        description = ""
        media = entry.get("media_description") or entry.get("summary") or ""
        if media:
            description = str(media).strip()

        if transcript:
            body = f"## Transcript\n\n{transcript}\n"
        elif description:
            body = f"## Description\n\n{description}\n\n_Transcript unavailable._\n"
        else:
            print(f"     skipped (no transcript and no description)")
            time.sleep(DELAY)
            continue

        fm = build_frontmatter(
            title, date, url, key, name, author,
            extra={"video_id": video_id, "video_url": url},
        )
        dest.write_text(fm + body, encoding="utf-8")
        saved += 1
        time.sleep(DELAY)

    print(f"   done: {saved} new videos saved")
    return saved
