#!/usr/bin/env python3
"""
digest.py — Format scraped feed posts into a Telegram digest.

Usage:
    python3 digest.py --input /tmp/feed_posts.json [--youtube-input /tmp/youtube_feed.json] [--max-posts 10]

Output: Formatted Telegram message (plain text, no markdown tables)
"""
import argparse, json, os, re, sys
from datetime import datetime, timedelta
from pathlib import Path

_SCRIPTS_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SCRIPTS_ROOT))

from config import load_config
from feed.utils import STOPWORDS, parse_likes
_CFG = load_config()
SEEN_HISTORY_FILE = str(_CFG["feed_assets"] / "seen_history.json")

MAX_TEXT_LEN = 200
SEEN_EXPIRY_DAYS = 7  # Forget seen items after this many days


def truncate(text, n=MAX_TEXT_LEN):
    return text[:n].rstrip() + "…" if len(text) > n else text


def load_items(path):
    if not path:
        return []
    try:
        with open(path) as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except FileNotFoundError:
        return []


def make_story_fingerprint(text: str) -> str:
    """
    Create a rough 'story fingerprint' from tweet text for cross-source deduplication.
    Strips stopwords, lowercases, extracts key words, and joins the top 5.
    Two tweets about the same story should share several keywords.
    """
    words = re.findall(r"[a-zA-Z]{3,}", text.lower())
    filtered = [w for w in words if w not in STOPWORDS]
    # Use the first 8 meaningful words as fingerprint
    return " ".join(filtered[:8])


def post_sort_key(post: dict) -> tuple:
    if "_score" in post:
        return (3, float(post.get("_score", 0)))
    if post.get("source") == "youtube":
        return (2, int(post.get("views", 0) or 0))
    return (1, parse_likes(post.get("likes", 0)))


def load_seen_history() -> dict:
    """Load the seen history file. Returns {url: iso_date, fingerprint: iso_date}."""
    if os.path.exists(SEEN_HISTORY_FILE):
        try:
            with open(SEEN_HISTORY_FILE) as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            print(f"[digest] Error: {e}", file=sys.stderr)
    return {}


def save_seen_history(history: dict):
    """Save seen history, pruning entries older than SEEN_EXPIRY_DAYS."""
    cutoff = (datetime.now() - timedelta(days=SEEN_EXPIRY_DAYS)).isoformat()
    pruned = {k: v for k, v in history.items() if v >= cutoff}
    os.makedirs(os.path.dirname(SEEN_HISTORY_FILE), exist_ok=True)
    with open(SEEN_HISTORY_FILE, "w") as f:
        json.dump(pruned, f, indent=2)


def is_seen(post: dict, history: dict) -> bool:
    """Return True if this post (or a very similar one) has been shown before."""
    url = post.get("url", "")
    if url and url in history:
        return True
    # Story-level fingerprint check: require strong overlap (7+ words) to avoid
    # flagging legitimately different stories that share a few common words
    fp = make_story_fingerprint(post.get("content", "") or post.get("title", ""))
    fp_words = set(fp.split())
    if len(fp_words) >= 4:
        for key in history:
            if key.startswith("fp:"):
                seen_words = set(key[3:].split())
                overlap = fp_words & seen_words
                if len(overlap) >= min(7, len(fp_words) - 1):
                    return True
    return False


def mark_seen(post: dict, history: dict):
    """Add post URL and fingerprint to the seen history."""
    now = datetime.now().isoformat()
    url = post.get("url", "")
    if url:
        history[url] = now
    fp = make_story_fingerprint(post.get("content", "") or post.get("title", ""))
    if fp:
        history[f"fp:{fp}"] = now


def format_digest(posts: list[dict], max_posts: int) -> str:
    if not posts:
        return None

    history = load_seen_history()

    # Filter out previously seen posts/stories
    fresh_posts = [p for p in posts if not is_seen(p, history)]
    skipped = len(posts) - len(fresh_posts)

    fresh_posts.sort(key=post_sort_key, reverse=True)

    # Deduplicate within this batch: each post appears in at most one section (highest-priority topic wins)
    topic_priority = ["ai_monetize", "AI", "startup", "crypto"]
    by_topic = {"ai_monetize": [], "AI": [], "startup": [], "crypto": []}
    seen_urls = set()

    for p in fresh_posts:
        url = p.get("url", "")
        if url in seen_urls:
            continue
        topics = p.get("topics", [])
        for t in topic_priority:
            if t in topics and len(by_topic[t]) < max_posts // 3 + 1:
                by_topic[t].append(p)
                seen_urls.add(url)
                break

    today = datetime.now().strftime("%a %d %b")
    lines = [f"🗞 *Morning Feed — {today}*\n"]

    counter = 1
    digest_map = {}
    labels = {"ai_monetize": "💰 AI Monetization", "AI": "🤖 AI", "startup": "🚀 Startups", "crypto": "🪙 Crypto"}

    # First pass: topic-sections (show up to 3 per topic)
    for topic, label in labels.items():
        items = by_topic.get(topic, [])
        if not items:
            continue
        lines.append(f"\n*{label}*")
        for p in items[:3]:
            author = p.get("author", "")
            url = p.get("url", "")
            if p.get("source") == "youtube":
                title = truncate(p.get("title", ""), 110)
                summary = truncate(p.get("content", ""))
                published = p.get("timestamp", "")
                date_suffix = f" ({published[:10]})" if published else ""
                lines.append(f"{counter}. ▶ {author}: {title}{date_suffix}")
                if summary:
                    lines.append(f"   {summary}")
            else:
                text = truncate(p.get("content", "") or p.get("title", ""))
                lines.append(f"{counter}. {author}: {text}")
            if url:
                lines.append(f"   {url}")
            digest_map[str(counter)] = p
            counter += 1
            mark_seen(p, history)

    # Fallback: show untagged posts if topic sections are empty
    untagged = [p for p in fresh_posts if p.get("url", "") not in seen_urls]
    if untagged:
        lines.append(f"\n*📌 General*")
        for p in untagged[:6]:
            author = p.get("author", "") or p.get("channel_name", "")
            url = p.get("url", "")
            if p.get("source") == "youtube":
                title = truncate(p.get("title", ""), 110)
                published = p.get("timestamp", "")
                date_suffix = f" ({published[:10]})" if published else ""
                lines.append(f"{counter}. ▶ {author}: {title}{date_suffix}")
            else:
                text = truncate(p.get("content", "") or p.get("title", ""))
                lines.append(f"{counter}. {author}: {text}")
            if url:
                lines.append(f"   {url}")
            digest_map[str(counter)] = p
            counter += 1
            mark_seen(p, history)
            seen_urls.add(p.get("url", ""))

    if skipped > 0:
        lines.append(f"\n_(Filtered {skipped} repeated/similar post{'s' if skipped != 1 else ''} from prior feeds)_")

    # Save updated seen history
    save_seen_history(history)

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(_CFG["feeds_file"]))
    parser.add_argument("--youtube-input", default=str(_CFG["feed_raw"] / "youtube_feed.json"))
    parser.add_argument("--max-posts", type=int, default=12)
    args = parser.parse_args()

    posts = load_items(args.input)
    youtube_posts = load_items(args.youtube_input)
    posts.extend(youtube_posts)

    if not posts:
        print("ERROR: No input items found. Run refresh.py and/or source/youtube.py first.", file=sys.stderr)
        sys.exit(1)

    digest = format_digest(posts, args.max_posts)
    if digest:
        print(digest)
    else:
        print("No relevant posts found today.")


if __name__ == "__main__":
    main()
