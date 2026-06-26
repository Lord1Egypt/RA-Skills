#!/usr/bin/env python3
from __future__ import annotations
"""
ranker.py — Score and sort scraped posts using learned preferences.

Usage:
    python3 ranker.py --input /tmp/feed_posts.json --output /tmp/feed_ranked.json

Reads preferences.json and applies author/topic/keyword weights to each post.
Score = log(likes+1) * author_weight * topic_avg_weight * keyword_avg_weight
"""
import argparse, json, math, os, sys
from pathlib import Path

_SCRIPTS_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SCRIPTS_ROOT))

from config import load_config
from feed.utils import STOPWORDS, parse_likes
_CFG = load_config()
ASSETS_DIR = str(_CFG["feed_assets"])
PREFS_FILE = os.path.join(ASSETS_DIR, "preferences.json")
FEED_SOURCE_CONFIG_FILE = str(_CFG["feed_dir"] / "feed_source_config.json")

def load_json(path, default):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return default

def extract_keywords(text: str) -> list[str]:
    words = text.lower().replace("'s", "").split()
    cleaned = []
    for w in words:
        w = w.strip(".,!?\"'()[]#@:")
        if len(w) > 3 and w not in STOPWORDS and not w.startswith("http") and not w.startswith("@"):
            cleaned.append(w)
    return list(set(cleaned))

def _prefer_longform_for_post(post: dict, feed_config: dict) -> bool:
    """Return True if prefer_longform is enabled for this post's source."""
    source = post.get("source", "")
    if source == "x":
        return feed_config.get("x_feed", {}).get("prefer_longform", False)
    return False


def score_post(post: dict, prefs: dict, feed_config: dict | None = None) -> float:
    author = post.get("author", "")
    topics = post.get("topics", [])
    text = post.get("content", "") or post.get("title", "")
    likes = parse_likes(post.get("likes", 0))
    if post.get("source") == "youtube":
        likes = int(post.get("views", likes) or likes)

    # Base score: log scale of likes
    base = math.log(likes + 2)

    # Author weight (default 1.0)
    author_w = prefs["authors"].get(author, 1.0)

    # Topic weight: average of all topics for this post
    topic_weights = [prefs["topics"].get(t, 1.0) for t in topics] if topics else [1.0]
    topic_w = sum(topic_weights) / len(topic_weights)

    # Keyword weight: average of matching keywords in preferences
    keywords = extract_keywords(text)
    kw_scores = [prefs["keywords"].get(kw, 1.0) for kw in keywords]
    kw_w = sum(kw_scores) / len(kw_scores) if kw_scores else 1.0

    score = base * author_w * topic_w * kw_w

    # Article/thread preference: boost long-form, penalise short tweets
    if feed_config and _prefer_longform_for_post(post, feed_config):
        article_multiplier = 1.0
        text_len = len(text)

        # Boost thread-length content (>= 300 chars)
        if text_len >= 300:
            article_multiplier *= 1.5

        # Boost posts ending with truncation markers (more content available)
        text_stripped = text.rstrip()
        text_lower = text_stripped.lower()
        if (
            text_stripped.endswith("…")
            or text_stripped.endswith("...")
            or text_lower.endswith("read more")
            or text_lower.endswith("show more")
        ):
            article_multiplier *= 1.3

        # Boost posts with multiple links (article-link heuristic)
        link_count = text.count("http://") + text.count("https://")
        if link_count >= 2:
            article_multiplier *= 1.3

        # Penalise plain short tweets (< 100 chars)
        if text_len < 100:
            article_multiplier *= 0.7

        score *= article_multiplier

    return score

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(_CFG["feeds_file"]))
    parser.add_argument("--output", default=str(_CFG["feed_raw"] / "feed_ranked.json"))
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    prefs = load_json(PREFS_FILE, {"authors": {}, "topics": {}, "keywords": {}})
    feed_config = load_json(FEED_SOURCE_CONFIG_FILE, {})

    with open(args.input) as f:
        posts = json.load(f)

    scored = []
    for post in posts:
        s = score_post(post, prefs, feed_config)
        post["_score"] = round(s, 3)
        scored.append(post)

    # Sort by score descending within each topic group
    scored.sort(key=lambda p: -p["_score"])

    with open(args.output, "w") as f:
        json.dump(scored, f, indent=2)

    if args.verbose:
        print(f"Ranked {len(scored)} posts:")
        for p in scored:
            print(f"  [{p['_score']:.2f}] {p['author']}: {(p.get('content') or p.get('title', ''))[:60]}...")

    print(f"✅ Ranked {len(scored)} posts → {args.output}")

if __name__ == "__main__":
    main()
