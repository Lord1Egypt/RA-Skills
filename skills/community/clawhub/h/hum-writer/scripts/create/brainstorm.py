#!/usr/bin/env python3
"""
brainstorm.py — Filter and format feed posts for topic brainstorming.

Scores posts against content pillars defined in CONTENT.md. Posts spanning
multiple pillars get a cross-pillar bonus — these intersection ideas are
the most interesting for content.

Also loads knowledge/ articles (influencer blogs) and merges them into the
ranked list so trends reinforced across both sources surface to the top.

Scoring weights live in <data_dir>/ideas/brainstorm.json.

Usage:
    python3 scripts/create/brainstorm.py [--input feeds.json] [--max 10]
                                          [--knowledge-days 30] [--no-knowledge]
"""
import argparse
import json
import os
import sys
from datetime import date, timedelta
from pathlib import Path

_SCRIPTS_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SCRIPTS_ROOT))

from config import load_config, load_topics

_CFG = load_config()

DEFAULT_WEIGHTS = {
    "keyword_weight": 50,
    "cross_pillar_bonus": 100,
    "min_pillars_for_bonus": 2,
    "likes_divisor": 100,
}


def load_weights() -> dict:
    """Load scoring weights, creating or updating brainstorm.json if needed."""
    path = _CFG["ideas_dir"] / "brainstorm.json"
    if path.exists():
        with open(path) as f:
            saved = json.load(f)
        merged = {**DEFAULT_WEIGHTS, **saved}
        # Backfill any new default keys
        if merged != saved:
            path.write_text(json.dumps(merged, indent=2) + "\n")
        return merged
    # First run — create with defaults
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(DEFAULT_WEIGHTS, indent=2) + "\n")
    return dict(DEFAULT_WEIGHTS)


def score_post(post: dict, pillars: dict[str, list[str]], weights: dict) -> tuple[int, list[str]]:
    """Score a post against all pillars. Returns (score, matched_pillar_names)."""
    text = (post.get("content") or post.get("text") or post.get("title") or "").lower()
    kw_weight = weights["keyword_weight"]
    matched_pillars = []
    total_hits = 0

    for pillar_name, keywords in pillars.items():
        hits = sum(1 for kw in keywords if kw in text)
        if hits > 0:
            matched_pillars.append(pillar_name)
            total_hits += hits

    score = total_hits * kw_weight

    if len(matched_pillars) >= weights["min_pillars_for_bonus"]:
        score += weights["cross_pillar_bonus"]

    likes = min(post.get("likes", 0), 50000)
    divisor = weights["likes_divisor"]
    if divisor > 0:
        score += likes // divisor

    return score, matched_pillars


def load_knowledge_items(knowledge_dir: Path, days_back: int = 30) -> list[dict]:
    """Load knowledge/ markdown articles published within days_back days.

    Files follow the naming convention YYYY-MM-DD-slug.md so we can pre-filter
    by filename before reading any file content.
    """
    if not knowledge_dir.exists():
        return []

    cutoff = date.today() - timedelta(days=days_back)
    items = []

    for md_file in knowledge_dir.rglob("*.md"):
        # Pre-filter: filename must start with a valid date
        name = md_file.stem  # e.g. "2026-04-01-some-post"
        date_prefix = name[:10]
        try:
            file_date = date.fromisoformat(date_prefix)
        except ValueError:
            continue
        if file_date < cutoff:
            continue

        # Parse frontmatter and body
        try:
            raw = md_file.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue

        title = ""
        url = ""
        source = md_file.parent.name  # folder name = author/source slug
        author = source
        fm_done = False
        body_lines: list[str] = []
        in_fm = False

        for line in raw.splitlines():
            if not fm_done:
                if line.strip() == "---":
                    if not in_fm:
                        in_fm = True
                        continue
                    else:
                        fm_done = True
                        continue
                if in_fm:
                    if line.lower().startswith("title:"):
                        title = line[6:].strip().strip('"').strip("'")
                    elif line.lower().startswith("url:"):
                        url = line[4:].strip()
                    elif line.lower().startswith("source:"):
                        source = line[7:].strip()
                    elif line.lower().startswith("author:"):
                        author = line[7:].strip().strip('"').strip("'")
            else:
                body_lines.append(line)

        body = " ".join(body_lines)[:800]
        text = f"{title} {body}".strip()

        items.append({
            "source": source,
            "author": author,
            "title": title,
            "text": text,
            "url": url,
            "timestamp": file_date.isoformat(),
            "likes": 0,
            "_from": "knowledge",
        })

    return items


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(_CFG["feeds_file"]))
    parser.add_argument("--max", type=int, default=10)
    parser.add_argument("--knowledge-days", type=int, default=30,
                        help="Include knowledge articles from last N days (default: 30)")
    parser.add_argument("--no-knowledge", action="store_true",
                        help="Skip knowledge folder, show feed items only")
    args = parser.parse_args()

    pillars = load_topics()
    if not pillars:
        print("No content pillars found. Set up CONTENT.md first.", file=sys.stderr)
        sys.exit(1)

    weights = load_weights()

    if not os.path.exists(args.input):
        print(f"No feed data at {args.input}. Run scrape first.")
        sys.exit(1)

    with open(args.input) as f:
        feed_posts = json.load(f)

    knowledge_items = []
    if not args.no_knowledge:
        knowledge_items = load_knowledge_items(_CFG["knowledge_dir"], args.knowledge_days)

    all_posts = [
        {**p, "_from": "feed"} for p in feed_posts
    ] + knowledge_items

    scored = []
    for p in all_posts:
        s, matched = score_post(p, pillars, weights)
        if s > 0:
            scored.append((s, matched, p))

    scored.sort(key=lambda x: -x[0])
    scored = scored[:args.max]

    if not scored:
        print("No relevant posts found.")
        sys.exit(0)

    feed_count = sum(1 for _, _, p in scored if p.get("_from") == "feed")
    knowledge_count = sum(1 for _, _, p in scored if p.get("_from") == "knowledge")

    pillar_names = ", ".join(pillars.keys())
    header_parts = []
    if feed_count:
        header_parts.append(f"FEED ({feed_count})")
    if knowledge_count:
        header_parts.append(f"KNOWLEDGE ({knowledge_count})")
    print(f"BRAINSTORM: {' + '.join(header_parts)} of {len(all_posts)} total")
    print(f"Pillars: {pillar_names}\n")
    print("=" * 60)

    for i, (score, matched, p) in enumerate(scored, 1):
        pillars_str = " + ".join(matched)
        if p.get("_from") == "knowledge":
            source = p.get("source", "?")
            ts = p.get("timestamp", "")
            print(f"\n[{i}] {source} | {ts} | {pillars_str} (score: {score})")
        else:
            author = p.get("author", "?").lstrip("@")
            likes = p.get("likes", 0)
            print(f"\n[{i}] @{author} | {likes:,} likes | {pillars_str} (score: {score})")
        print(f"    {(p.get('text') or p.get('title') or '').strip()[:300]}")
        if p.get("url"):
            print(f"    {p['url']}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
