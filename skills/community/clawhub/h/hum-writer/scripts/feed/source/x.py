#!/usr/bin/env python3
from __future__ import annotations
"""
x.py — X/Twitter feed source: scrape home feed, threads, and tweets with media.

Profile scraping has two modes:
  - Bird (direct): uses AUTH_TOKEN + CT0 session credentials to call X's
    GraphQL API via the vendored bird-search.mjs. Returns feed items directly.
  - Browser (fallback): returns structured JSON instructions for the browser
    automation agent when credentials are not available.

Home feed and thread/tweet scraping always use browser instructions.

Usage:
    python3 -m feed.source.x home [--scrolls N] [--output PATH]
    python3 -m feed.source.x thread <url> [--output PATH]
    python3 -m feed.source.x tweet <url> [--output PATH]
"""
import argparse
import json
import re
import sys
from pathlib import Path

_SCRIPTS_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_SCRIPTS_ROOT))

from config import load_config, load_topics, load_x_credentials
from lib import bird_x as _bird

_CFG = load_config()

# ── Bird credential bootstrap ──────────────────────────────────────────────

def _init_bird() -> None:
    """Inject X credentials into the Bird client (once per process)."""
    if not hasattr(_init_bird, "_done"):
        creds = load_x_credentials()
        _bird.set_credentials(creds.get("auth_token"), creds.get("ct0"))
        _init_bird._done = True


# ── Profile scraping via Bird ──────────────────────────────────────────────

def fetch_profile_via_bird(
    handle: str,
    since: str | None = None,
    count: int = 20,
) -> list[dict] | None:
    """Fetch recent posts from an X profile directly using Bird (no browser needed).

    Returns a list of hum feed items if Bird credentials are available and the
    fetch succeeds, or None if Bird is not available (caller should fall back to
    browser instructions).

    Args:
        handle: X handle (without @)
        since: ISO 8601 timestamp — only return tweets posted after this date
        count: Max number of tweets to fetch
    """
    _init_bird()
    if not _bird.is_available():
        return None
    return _bird.fetch_profile(handle, since=since, count=count)


def fetch_home_feed_via_bird(
    since: str | None = None,
    count: int = 40,
) -> list[dict] | None:
    """Fetch X home feed directly via Bird (filter:follows). No browser needed.

    Returns feed items with topic classification applied, or None if Bird
    credentials are not configured.

    Args:
        since: ISO 8601 timestamp — only return tweets posted after this date
        count: Max number of tweets to fetch
    """
    _init_bird()
    if not _bird.is_available():
        return None

    items = _bird.fetch_home_feed(since=since, count=count)
    # Classify each item by topic so the ranker/digest see the same shape
    # that HN items carry. The home feed is the broadest intake — topic
    # tagging matters most here.
    for item in items:
        item["topics"] = classify(item.get("content", ""))
    return items


# ── Topic classification ───────────────────────────────────────────────────


def get_topics() -> dict[str, list[str]]:
    """Load topics from CONTENT.md (data_dir). Cached after first call."""
    if not hasattr(get_topics, "_cache"):
        get_topics._cache = load_topics(_CFG["data_dir"])
    return get_topics._cache


def classify(text: str, topics: dict[str, list[str]] | None = None) -> list[str]:
    """Classify text into topic categories based on keyword matching."""
    if topics is None:
        topics = get_topics()
    lower = text.lower()
    return [topic for topic, kws in topics.items() if any(re.search(r'\b' + re.escape(kw) + r'\b', lower) for kw in kws)]


# ── Shared schemas ─────────────────────────────────────────────────────────

MEDIA_SCHEMA = {
    "type": "image | video | gif",
    "url": "direct media URL (highest resolution available)",
    "alt_text": "alt text if present, else null",
    "thumbnail_url": "video thumbnail URL if type is video, else null",
}

TWEET_SCHEMA = {
    "author": "@handle",
    "display_name": "display name",
    "text": "full tweet text (expand 'Show more' if truncated); for threads, all tweets concatenated with '\\n\\n'",
    "likes": "integer or null; for threads, sum across all tweets",
    "retweets": "integer or null; for threads, sum across all tweets",
    "replies": "integer or null; for threads, sum across all tweets",
    "views": "integer or null; for threads, sum across all tweets",
    "url": "https://x.com/<handle>/status/<id>; for threads, URL of first tweet",
    "timestamp": "ISO 8601 or relative time string",
    "media": [MEDIA_SCHEMA],
    "is_thread": "boolean — true if this item represents a multi-tweet thread",
    "is_quote_tweet": "boolean",
    "quoted_tweet": "nested tweet object if quote tweet, else null",
}


# ── Home feed scraping ─────────────────────────────────────────────────────

def home_feed_instructions(scrolls: int = 5, output: str | None = None) -> dict:
    """Generate browser automation instructions for scraping the X home feed."""
    out = output or str(_CFG["feeds_file"])
    return {
        "action": "scrape_x_home_feed",
        "steps": [
            "Navigate to https://x.com/home",
            f"Scroll {scrolls} times, waiting 2s between each scroll to load content",
            "For each visible tweet:",
            "  - Extract author handle, display name, full text — you MUST click 'Show more' on every tweet that has it before reading the text; never use the truncated inline preview",
            "  - Extract engagement counts: likes, retweets, replies, views",
            "  - Extract tweet URL",
            "  - Extract all attached media:",
            "    - Images: right-click or inspect to get full-res URL (format=jpg&name=large)",
            "    - Videos: note the thumbnail URL and video URL if accessible",
            "    - GIFs: extract the video/mp4 URL",
            "  - If tweet is a quote tweet, also extract the quoted tweet content and media",
            "  - Detect threads: if the tweet shows a thread indicator (vertical line connecting tweets, '🧵', '1/', numbered continuation, or 'Show this thread' link), it is a thread",
            "    - For thread tweets: click the tweet URL to open the full thread page",
            "    - Scroll through the thread and collect ALL tweets by the same author in the reply chain",
            "    - Concatenate all tweet texts in order, separated by '\\n\\n'",
            "    - Sum likes, retweets, replies, views across all tweets in the thread",
            "    - Use the first tweet's URL as the canonical thread URL",
            "    - Set is_thread=true on the item",
            "Filter to tweets matching at least one topic keyword (see topics below)",
            "Deduplicate by URL",
            "Set source='x' on every item",
            f"Output JSON to: {out}",
        ],
        "topics": get_topics(),
        "output_schema": {
            "items": [{**TWEET_SCHEMA, "source": "x"}],
            "note": "topics field is added per-item based on keyword classification",
        },
    }


# ── Profile scraping ──────────────────────────────────────────────────────

def profile_instructions(
    handle: str,
    output: str | None = None,
    limit: int = 20,
    since: str | None = None,
) -> dict:
    """Generate browser automation instructions for scraping an X profile's posts.

    Args:
        handle: X handle (without @)
        output: Path to write JSON results
        limit: Max number of tweets to extract (default 20)
        since: ISO 8601 timestamp — stop when a tweet is older than this
    """
    out = output or str(_CFG["feed_raw"] / f"x_{handle}.json")
    since_step = (
        f"  - Check the tweet's timestamp: if it was posted BEFORE {since}, STOP immediately — do not extract this or any further tweets"
        if since else None
    )
    steps = [
        f"Navigate to https://x.com/{handle}",
        "Wait for the page to fully load",
        f"Extract up to {limit} tweets from this profile's timeline, scrolling as needed",
    ]
    if since:
        steps.append(f"Stop as soon as you encounter a tweet posted before {since} — do not extract it")
    steps += [
        "For each tweet in chronological reverse order (newest first):",
        "  - Extract author handle, display name, full text — you MUST click 'Show more' on every tweet that has it before reading the text; never use the truncated inline preview",
        "  - Extract engagement counts: likes, retweets, replies, views",
        "  - Extract tweet URL",
        "  - Extract all attached media:",
        "    - Images: get full-res URL (format=jpg&name=large)",
        "    - Videos: note the thumbnail URL and video URL if accessible",
        "    - GIFs: extract the video/mp4 URL",
        "  - If tweet is a quote tweet, also extract the quoted tweet content and media",
        "  - Detect threads: if the tweet has a thread indicator (vertical connecting line, '🧵', '1/', numbered continuation, or 'Show this thread' link), it is a thread",
        "    - Click the tweet URL to open the full thread page",
        "    - Scroll through and collect ALL tweets by the same author in the reply chain",
        "    - Concatenate all tweet texts in order, separated by '\\n\\n'",
        "    - Sum likes, retweets, replies, views across all tweets in the thread",
        "    - Use the first tweet's URL as the canonical thread URL",
        "    - Set is_thread=true on the item",
        "    - Treat the entire thread as a single feed item — do not add individual thread tweets separately",
    ]
    if since_step:
        steps.append(since_step)
    steps += [
        "Deduplicate by URL",
        "Set source='x' on every item",
        f"Output JSON to: {out}",
    ]
    return {
        "action": "scrape_x_profile",
        "profile": {
            "handle": handle,
            "url": f"https://x.com/{handle}",
        },
        "steps": steps,
        "output_schema": {
            "handle": handle,
            "tweet_count": "number of tweets extracted",
            "items": [{**TWEET_SCHEMA, "source": "x"}],
        },
    }


# ── Thread scraping ────────────────────────────────────────────────────────

def thread_instructions(thread_url: str, output: str | None = None) -> dict:
    """Generate browser automation instructions for scraping an X thread."""
    out = output or str(_CFG["feed_raw"] / "thread.json")
    return {
        "action": "scrape_x_thread",
        "steps": [
            f"Navigate to {thread_url}",
            "Identify the thread author from the original tweet",
            "Scroll down to load the full thread — keep scrolling until all replies by the "
            "original author in the thread chain are visible",
            "Collect each tweet in the thread (tweets by the same author in the reply chain):",
            "  - Extract author handle, display name, full text (click 'Show more' if truncated)",
            "  - Extract engagement counts: likes, retweets, replies, views",
            "  - Extract tweet URL (each tweet in a thread has its own URL)",
            "  - Extract all attached media per tweet:",
            "    - Images: get full-res URL (format=jpg&name=large)",
            "    - Videos: note the thumbnail URL and video URL if accessible",
            "    - GIFs: extract the video/mp4 URL",
            "  - If any tweet is a quote tweet, also extract the quoted tweet content",
            "Order tweets chronologically (first tweet first)",
            "Stop collecting when the thread ends (next reply is by a different author "
            "and not a continuation)",
            f"Output JSON to: {out}",
        ],
        "output_schema": {
            "thread_url": thread_url,
            "author": "@handle of thread author",
            "tweet_count": "number of tweets in thread",
            "tweets": [
                {
                    **TWEET_SCHEMA,
                    "position": "1-indexed position in thread",
                }
            ],
            "total_likes": "sum of likes across all thread tweets",
            "total_retweets": "sum of retweets across all thread tweets",
            "topics": ["classified from combined thread text"],
        },
    }


# ── Single tweet scraping ──────────────────────────────────────────────────

def tweet_instructions(tweet_url: str, output: str | None = None) -> dict:
    """Generate browser automation instructions for scraping a single tweet with media."""
    out = output or str(_CFG["feed_raw"] / "tweet.json")
    return {
        "action": "scrape_x_tweet",
        "steps": [
            f"Navigate to {tweet_url}",
            "Extract the full tweet content:",
            "  - Author handle and display name",
            "  - Full text (click 'Show more' if truncated)",
            "  - Engagement counts: likes, retweets, replies, views, bookmarks",
            "  - Timestamp",
            "Extract all attached media:",
            "  - Images: click to open full size, get URL with format=jpg&name=large",
            "  - Videos: extract video URL and thumbnail",
            "  - GIFs: extract the video/mp4 source URL",
            "If this is a quote tweet, also extract the quoted tweet and its media",
            "Check if this tweet is part of a thread (look for 'Show this thread' or "
            "replies by the same author). If so, note is_thread=true and thread_url",
            f"Output JSON to: {out}",
        ],
        "output_schema": {
            **TWEET_SCHEMA,
            "bookmarks": "integer or null",
            "is_thread": "boolean — true if tweet is part of a thread by same author",
            "thread_url": "URL of first tweet in thread if is_thread, else null",
            "topics": ["classified from tweet text"],
        },
    }


# ── CLI ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="X/Twitter feed source — generate scraping instructions"
    )
    sub = parser.add_subparsers(dest="command")

    home_p = sub.add_parser("home", help="Scrape home feed")
    home_p.add_argument("--scrolls", type=int, default=5, help="Feed scrolls (default 5)")
    home_p.add_argument("--output", default=None, help="Output JSON path")

    thread_p = sub.add_parser("thread", help="Scrape a thread")
    thread_p.add_argument("url", help="URL of any tweet in the thread")
    thread_p.add_argument("--output", default=None, help="Output JSON path")

    tweet_p = sub.add_parser("tweet", help="Scrape a single tweet with media")
    tweet_p.add_argument("url", help="Tweet URL")
    tweet_p.add_argument("--output", default=None, help="Output JSON path")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "home":
        result = home_feed_instructions(args.scrolls, args.output)
    elif args.command == "thread":
        result = thread_instructions(args.url, args.output)
    elif args.command == "tweet":
        result = tweet_instructions(args.url, args.output)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
