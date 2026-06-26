#!/usr/bin/env python3
"""Full-text search across transcribed podcast episodes."""

import argparse
import json
import os
import re
from pathlib import Path

DEFAULT_ARCHIVE = os.environ.get("HN_ARCHIVE_DIR", "./hn-podcast-archive")


def search_archive(archive_dir: str, query: str, context_chars: int = 200) -> list[dict]:
    archive = Path(archive_dir)
    index_path = archive / "archive_index.json"
    if not index_path.exists():
        print("No archive index found. Run build_index.py first.", file=sys.stderr)
        return []

    with open(index_path) as f:
        index = json.load(f)

    results = []
    pattern = re.compile(re.escape(query), re.IGNORECASE)

    for ep in index["episodes"]:
        if not ep.get("transcript_path"):
            continue
        tpath = Path(ep["transcript_path"])
        if not tpath.exists():
            continue
        text = tpath.read_text(errors="replace")

        matches = list(pattern.finditer(text))
        if not matches:
            continue

        # Build context snippets around matches
        snippets = []
        for m in matches[:5]:  # max 5 snippets per episode
            start = max(0, m.start() - context_chars // 2)
            end = min(len(text), m.end() + context_chars // 2)
            snippet = text[start:end].strip()
            if start > 0:
                snippet = "..." + snippet
            if end < len(text):
                snippet = snippet + "..."
            snippets.append(snippet)

        results.append({
            "title": ep["title"],
            "pub_date": ep["pub_date"],
            "slug": ep["slug"],
            "match_count": len(matches),
            "snippets": snippets,
        })

    results.sort(key=lambda r: r["match_count"], reverse=True)
    return results


def main():
    parser = argparse.ArgumentParser(description="Search podcast archive")
    parser.add_argument("--archive", default=DEFAULT_ARCHIVE)
    parser.add_argument("query", help="Search query")
    parser.add_argument("--context", type=int, default=200, help="Context chars around match")
    args = parser.parse_args()

    results = search_archive(args.archive, args.query, args.context)
    if not results:
        print("No results found.")
        return

    print(f"Found matches in {len(results)} episodes:\n")
    for r in results:
        print(f"## {r['title']} ({r['pub_date']}) — {r['match_count']} matches")
        for s in r["snippets"]:
            print(f"  > {s}")
        print()


if __name__ == "__main__":
    main()
