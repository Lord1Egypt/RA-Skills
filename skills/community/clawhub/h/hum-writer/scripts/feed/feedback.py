#!/usr/bin/env python3
"""
feedback.py — Log upvote/downvote on digest items and update preferences.

Usage:
    python3 feedback.py log --item 3 --vote up
    python3 feedback.py log --item 1 --vote down
    python3 feedback.py show               # show current preferences
    python3 feedback.py history            # show recent votes
"""
import argparse, json, os, re, sys
from datetime import datetime
from pathlib import Path

_SCRIPTS_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SCRIPTS_ROOT))

from config import load_config
from feed.utils import STOPWORDS
_CFG = load_config()
ASSETS_DIR = str(_CFG["feed_assets"])
PREFS_FILE = os.path.join(ASSETS_DIR, "preferences.json")
LOG_FILE = os.path.join(ASSETS_DIR, "feedback_log.json")

def load_json(path, default):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return default

def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def extract_keywords(text: str) -> list[str]:
    words = text.lower().replace("'s", "").split()
    cleaned = []
    for w in words:
        w = w.strip(".,!?\"'()[]#@:")
        if len(w) > 3 and w not in STOPWORDS and not w.startswith("http") and not w.startswith("@"):
            cleaned.append(w)
    # Return up to 8 most meaningful words
    return list(set(cleaned))[:8]

def clamp(val, lo, hi):
    return max(lo, min(hi, val))

def parse_latest_digest(news_path: str) -> dict:
    """Parse the most recent day's entries from news.md into a numbered item map."""
    if not os.path.exists(news_path):
        return {}
    with open(news_path) as f:
        content = f.read()
    # Find the first date section (most recent, inserted at top)
    sections = re.split(r'^## \d{4}-\d{2}-\d{2}', content, flags=re.MULTILINE)
    if len(sections) < 2:
        return {}
    latest = sections[1]  # content after the first date header
    # Cut off at the next date section or end
    if "---" in latest:
        latest = latest.split("---")[0]
    # Parse entries: "- @handle: [summary] [url]" or "- [Title] — [points]pts · [url]"
    items = {}
    counter = 1
    for line in latest.split("\n"):
        line = line.strip()
        if not line.startswith("- "):
            continue
        entry = line[2:]
        # Extract URL (last http(s) link on the line)
        urls = re.findall(r'https?://\S+', entry)
        url = urls[-1] if urls else ""
        # Extract author (@handle at start)
        author_match = re.match(r'(@\S+):', entry)
        author = author_match.group(1) if author_match else ""
        # Extract topic from the section header above
        text = re.sub(r'https?://\S+', '', entry).strip().rstrip('·').strip()
        items[str(counter)] = {"author": author, "text": text, "url": url, "topics": []}
        counter += 1
    return items


def log_vote(item_num: int, vote: str):
    feeds_file = str(_CFG["feed_dir"] / "feeds.json")
    last_digest = parse_latest_digest(feeds_file) if os.path.exists(feeds_file) else {}
    key = str(item_num)
    if key not in last_digest:
        print(f"ERROR: Item {item_num} not found in feeds.json. Run /refresh-feed first.", file=sys.stderr)
        sys.exit(1)

    post = last_digest[key]
    author = post.get("author", "")
    topics = post.get("topics", [])
    text = post.get("content", "") or post.get("title", "")
    url = post.get("url", "")
    keywords = extract_keywords(text)
    direction = 1 if vote == "up" else -1

    # Load preferences
    prefs = load_json(PREFS_FILE, {"authors": {}, "topics": {}, "keywords": {}})

    # Update author score (range 0.3 – 2.0, default 1.0)
    current_author = prefs["authors"].get(author, 1.0)
    prefs["authors"][author] = clamp(current_author + (direction * 0.2), 0.3, 2.0)

    # Update topic weights (range 0.5 – 1.5, default 1.0)
    for topic in topics:
        current_topic = prefs["topics"].get(topic, 1.0)
        prefs["topics"][topic] = clamp(current_topic + (direction * 0.05), 0.5, 1.5)

    # Update keyword scores (range 0.3 – 2.0, default 1.0)
    for kw in keywords:
        current_kw = prefs["keywords"].get(kw, 1.0)
        prefs["keywords"][kw] = clamp(current_kw + (direction * 0.1), 0.3, 2.0)

    save_json(PREFS_FILE, prefs)

    # Append to log
    log = load_json(LOG_FILE, [])
    log.append({
        "ts": datetime.utcnow().isoformat(),
        "item": item_num,
        "vote": vote,
        "author": author,
        "topics": topics,
        "keywords": keywords,
        "url": url
    })
    save_json(LOG_FILE, log)

    direction_word = "Upvoted" if vote == "up" else "Downvoted"
    print(f"✅ {direction_word} item {item_num} ({author})")
    print(f"   Author score: {prefs['authors'][author]:.2f}")
    if topics:
        print(f"   Topic weights: { {t: round(prefs['topics'].get(t,1.0),2) for t in topics} }")

def show_prefs():
    prefs = load_json(PREFS_FILE, {"authors": {}, "topics": {}, "keywords": {}})
    print("=== Current Preferences ===\n")
    print("AUTHORS:")
    for k, v in sorted(prefs["authors"].items(), key=lambda x: -x[1]):
        bar = "▓" * int(v * 5)
        print(f"  {k:<25} {v:.2f}  {bar}")
    print("\nTOPICS:")
    for k, v in sorted(prefs["topics"].items(), key=lambda x: -x[1]):
        print(f"  {k:<15} {v:.2f}")
    print("\nTOP KEYWORDS (boosted):")
    boosted = {k: v for k, v in prefs["keywords"].items() if v > 1.0}
    for k, v in sorted(boosted.items(), key=lambda x: -x[1])[:15]:
        print(f"  {k:<20} {v:.2f}")
    print("\nSUPPRESSED KEYWORDS:")
    suppressed = {k: v for k, v in prefs["keywords"].items() if v < 1.0}
    for k, v in sorted(suppressed.items(), key=lambda x: x[1])[:10]:
        print(f"  {k:<20} {v:.2f}")

def show_history():
    log = load_json(LOG_FILE, [])
    if not log:
        print("No votes logged yet.")
        return
    print("=== Recent Votes ===\n")
    for entry in reversed(log[-20:]):
        symbol = "👍" if entry["vote"] == "up" else "👎"
        print(f"  {symbol} Item {entry['item']:>2}  {entry['author']:<25}  {entry['ts'][:10]}")

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="cmd")

    log_p = subparsers.add_parser("log")
    log_p.add_argument("--item", type=int, required=True)
    log_p.add_argument("--vote", choices=["up", "down"], required=True)

    subparsers.add_parser("show")
    subparsers.add_parser("history")

    args = parser.parse_args()

    if args.cmd == "log":
        log_vote(args.item, args.vote)
    elif args.cmd == "show":
        show_prefs()
    elif args.cmd == "history":
        show_history()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
