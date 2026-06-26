#!/usr/bin/env python3
"""
schema.py — Canonical FeedItem schema for hum.

All feed sources must produce dicts conforming to this schema.
normalize_item() converts any old or inconsistent item to the standard shape,
handling all legacy field names (text, summary, engagement nested dict,
is_thread_start/is_article flags, etc.).
"""
from __future__ import annotations


def normalize_item(d: dict) -> dict:
    """Normalize any feed item dict to the canonical FeedItem schema.

    Handles all legacy field names and nested structures:
    - content/text/summary → content
    - is_thread_start/is_article/type → post_type
    - engagement.{likes,views,comments} → flat likes/views/replies
    - timestamp/date/scraped_at/published → timestamp
    """
    # Content: prefer content > text > summary
    content = d.get("content") or d.get("text") or d.get("summary") or ""

    # Engagement: flatten nested engagement dict if present
    eng = d.get("engagement") or {}

    # Post type: unified from various flag/field patterns
    post_type = (
        d.get("post_type")
        or ("thread" if (d.get("is_thread_start") or d.get("is_thread")) else None)
        or ("article" if (d.get("is_article") or d.get("type") == "article") else None)
        or ("video" if d.get("source") == "youtube" else None)
        or ("story" if d.get("source") == "hn" else None)
        or "tweet"
    )

    # Timestamp: prefer timestamp > date > scraped_at > published
    timestamp = (
        d.get("timestamp")
        or d.get("date")
        or d.get("scraped_at")
        or d.get("published")
        or None
    )

    result: dict = {
        "source": d.get("source") or "",
        "author": d.get("author") or "",
        "content": content,
        "post_type": post_type,
        "url": d.get("url") or None,
        "timestamp": timestamp,
        "topics": list(d.get("topics") or []),
        "likes": _to_int(d.get("likes") or eng.get("likes")),
        "retweets": _to_int(d.get("retweets")),
        "replies": _to_int(d.get("replies") or eng.get("comments")),
        "views": _to_int(d.get("views") or eng.get("views")),
        "title": d.get("title") or None,
        "media": list(d.get("media") or []),
        "tweet_id": d.get("tweet_id") or None,
        "display_name": d.get("display_name") or None,
    }

    # Preserve pipeline-internal fields set by ranker/brainstorm
    if "_score" in d:
        result["_score"] = d["_score"]
    if "_from" in d:
        result["_from"] = d["_from"]

    return result


def _to_int(val) -> int:
    if val is None:
        return 0
    try:
        return int(val)
    except (ValueError, TypeError):
        return 0
