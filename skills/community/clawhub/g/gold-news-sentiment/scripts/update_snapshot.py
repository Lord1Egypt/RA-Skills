#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from fetch_news import DEFAULT_QUERIES, collect_news


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
DEFAULT_JSON_PATH = DATA_DIR / "latest_news.json"
DEFAULT_DIGEST_PATH = DATA_DIR / "latest_digest.md"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Refresh cached gold-news snapshot files for fast reuse."
    )
    parser.add_argument(
        "--query",
        action="append",
        dest="queries",
        help="Custom query bucket. Can be passed multiple times.",
    )
    parser.add_argument(
        "--provider",
        action="append",
        choices=["google", "bing"],
        dest="providers",
        help="Restrict to specific provider(s). Default: google + bing.",
    )
    parser.add_argument("--hours", type=int, default=48)
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--timeout", type=int, default=12)
    parser.add_argument("--lang", default="en-US")
    parser.add_argument("--country", default="US")
    parser.add_argument("--max-workers", type=int, default=4)
    parser.add_argument("--json-out", type=Path, default=DEFAULT_JSON_PATH)
    parser.add_argument("--digest-out", type=Path, default=DEFAULT_DIGEST_PATH)
    return parser.parse_args()


def render_digest(result: dict) -> str:
    generated_at = result.get("generated_at", "")
    item_count = result.get("item_count", 0)
    providers = ", ".join(result.get("providers", []))
    queries = result.get("queries", [])
    items = result.get("items", [])

    tag_counter: Counter[str] = Counter()
    source_counter: Counter[str] = Counter()
    for item in items:
        tag_counter.update(item.get("tags", []))
        source_counter.update([item.get("source") or item.get("provider") or "unknown"])

    lines = [
        "# Gold News Snapshot",
        "",
        f"- generated_at_utc: {generated_at}",
        f"- item_count: {item_count}",
        f"- providers: {providers or 'none'}",
        f"- lookback_hours: {result.get('hours', '')}",
        "",
        "## Query Buckets",
    ]

    for query in queries:
        lines.append(f"- {query}")

    lines.extend(["", "## Dominant Tags"])
    if tag_counter:
        for tag, count in tag_counter.most_common(8):
            lines.append(f"- {tag}: {count}")
    else:
        lines.append("- none")

    lines.extend(["", "## Top Sources"])
    if source_counter:
        for source, count in source_counter.most_common(8):
            lines.append(f"- {source}: {count}")
    else:
        lines.append("- none")

    lines.extend(["", "## Recent Headlines"])
    if items:
        for index, item in enumerate(items[:12], start=1):
            source = item.get("source") or item.get("provider") or "unknown"
            published_at = item.get("published_at") or "unknown_time"
            query = item.get("query") or "unknown_query"
            lines.extend(
                [
                    f"{index}. {item.get('title', '')}",
                    f"   - source: {source}",
                    f"   - published_at_utc: {published_at}",
                    f"   - query: {query}",
                    f"   - link: {item.get('link', '')}",
                ]
            )
    else:
        lines.append("- no usable items")

    failures = result.get("failures", [])
    lines.extend(["", "## Retrieval Status"])
    if failures:
        lines.append("- partial_failure: true")
        for failure in failures:
            provider = failure.get("provider", "unknown")
            query = failure.get("query", "unknown")
            error = failure.get("error", "unknown")
            lines.append(f"- {provider} / {query}: {error}")
    else:
        lines.append("- partial_failure: false")

    lines.extend(
        [
            "",
            "## Automation Handoff",
            "Use this snapshot as the evidence base for the gold sentiment conclusion.",
            "If item_count is 0 or retrieval shows only failures, report insufficient data instead of guessing.",
            f"Snapshot refreshed at {datetime.now(timezone.utc).isoformat()}.",
        ]
    )

    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    queries = args.queries or DEFAULT_QUERIES
    providers = args.providers or ["google", "bing"]
    result = collect_news(
        queries=queries,
        providers=providers,
        hours=args.hours,
        timeout=args.timeout,
        lang=args.lang,
        country=args.country,
        max_workers=args.max_workers,
        limit=args.limit,
    )

    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    digest = render_digest(result)
    args.digest_out.parent.mkdir(parents=True, exist_ok=True)
    args.digest_out.write_text(digest, encoding="utf-8")

    print(f"Wrote {args.json_out}")
    print(f"Wrote {args.digest_out}")
    return 0 if result["item_count"] or not result.get("failures") else 1


if __name__ == "__main__":
    raise SystemExit(main())
