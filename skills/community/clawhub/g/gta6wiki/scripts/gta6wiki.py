#!/usr/bin/env python3
"""Zero-dependency Python 3.9+ CLI helper for GTA6 Wiki (https://gta6wiki.wiki)."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

DEFAULT_BASE_URL = os.environ.get("GTA6WIKI_URL", "https://gta6wiki.wiki").rstrip("/")
USER_AGENT = "gta6wiki-skill-py/1.0.0 (+https://gta6wiki.wiki/skill)"


def api_get(base_url: str, path: str, params: dict[str, Any]) -> Any:
    clean = {
        k: ("1" if v is True else str(v))
        for k, v in params.items()
        if v is not None and v != "" and v is not False
    }
    qs = urllib.parse.urlencode(clean)
    url = f"{base_url}{path}" + (f"?{qs}" if qs else "")
    req = urllib.request.Request(
        url,
        headers={"Accept": "application/json", "User-Agent": USER_AGENT},
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")[:240]
        raise SystemExit(f"GTA6 Wiki HTTP {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"Network error contacting {base_url}: {exc.reason}") from exc

    if not isinstance(payload, dict) or payload.get("code") != 0:
        raise SystemExit(f"API error: {payload.get('message') if isinstance(payload, dict) else payload}")
    return payload.get("data")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Query GTA6 Wiki from Python.")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--locale", choices=["en", "zh"], default="en")
    parser.add_argument("--json", action="store_true", help="Print raw JSON output")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_search = sub.add_parser("search", help="Search Wiki entries")
    p_search.add_argument("query", nargs="?", default="")
    p_search.add_argument("--type", default="")
    p_search.add_argument("--intent", default="")
    p_search.add_argument("--limit", type=int, default=15)

    p_entry = sub.add_parser("entry", help="Get full Wiki entry by slug")
    p_entry.add_argument("slug")
    p_entry.add_argument("--markdown", action="store_true")

    p_map = sub.add_parser("map", help="Search 3,843 Leonida & Vice City map pins")
    p_map.add_argument("query", nargs="?", default="")
    p_map.add_argument("--region", default="")
    p_map.add_argument("--category", default="")
    p_map.add_argument("--enterable", action="store_true")
    p_map.add_argument("--marker", default="")
    p_map.add_argument("--limit", type=int, default=20)

    p_missions = sub.add_parser("missions", help="List & filter GTA 6 missions")
    p_missions.add_argument("query", nargs="?", default="")
    p_missions.add_argument("--chapter", type=int, default=None)
    p_missions.add_argument("--character", default="")
    p_missions.add_argument("--missable", action="store_true")
    p_missions.add_argument("--optional", action="store_true")
    p_missions.add_argument("--limit", type=int, default=40)

    p_cheats = sub.add_parser("cheats", help="Look up 61 GTA 6 cheats")
    p_cheats.add_argument("query", nargs="?", default="")
    p_cheats.add_argument("--category", default="")
    p_cheats.add_argument("--auto-unlock", action="store_true")

    p_articles = sub.add_parser("articles", help="List or read blog articles & updates")
    p_articles.add_argument("slug", nargs="?", default="")
    p_articles.add_argument("--kind", choices=["all", "blog", "recent_changes"], default="all")
    p_articles.add_argument("--limit", type=int, default=15)

    args = parser.parse_args(argv)
    base = args.base_url.rstrip("/")

    if args.cmd == "search":
        data = api_get(
            base,
            "/api/wiki/search",
            {"q": args.query, "type": args.type, "intent": args.intent, "limit": args.limit, "locale": args.locale},
        )
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
            return 0
        for idx, item in enumerate(data or [], 1):
            print(f"{idx:2d}. {item['name']} [{item['type']}] — slug: {item['slug']}")
            print(f"    {item.get('answerSnippet') or item.get('summary')}")
        return 0

    if args.cmd == "entry":
        data = api_get(base, "/api/wiki/entity", {"slug": args.slug, "locale": args.locale})
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        elif args.markdown and data.get("markdown"):
            print(data["markdown"], end="")
        else:
            print(f"{data['name']} ({data['slug']})\n{data['summary']}\nURL: {data['canonicalUrl']}")
        return 0

    if args.cmd == "map":
        data = api_get(
            base,
            "/api/wiki/landmarks",
            {
                "q": args.query,
                "region": args.region,
                "category": args.category,
                "enterable": args.enterable,
                "marker": args.marker,
                "limit": args.limit,
                "locale": args.locale,
            },
        )
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
            return 0
        for idx, pin in enumerate(data.get("landmarks", []), 1):
            ent = " · ENTERABLE" if pin.get("enterable") else ""
            print(f"{idx:2d}. {pin['title']} ({pin['id']} · {pin['region']} · X {pin['x']}m, Y {pin['y']}m{ent}) -> {pin['mapPinUrl']}")
        return 0

    if args.cmd == "missions":
        data = api_get(
            base,
            "/api/wiki/missions",
            {
                "q": args.query,
                "chapter": args.chapter,
                "character": args.character,
                "missable": args.missable,
                "optional": args.optional,
                "limit": args.limit,
                "locale": args.locale,
            },
        )
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
            return 0
        for idx, m in enumerate(data.get("missions", []), 1):
            print(f"{idx:2d}. {m['name']} [{m['chapterTitle']}] -> {m.get('walkthroughUrl', '')}")
        return 0

    if args.cmd == "cheats":
        data = api_get(
            base,
            "/api/wiki/cheats",
            {"q": args.query, "category": args.category, "autoUnlock": args.auto_unlock, "locale": args.locale},
        )
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
            return 0
        for idx, c in enumerate(data.get("cheats", []), 1):
            seq = f" | {' > '.join(c['sequence'])}" if c.get("sequence") else ""
            print(f"{idx:2d}. {c['name']} [{c['categoryLabel']}]{seq} — {c['effect']}")
        return 0

    if args.cmd == "articles":
        data = api_get(
            base,
            "/api/wiki/articles",
            {"kind": args.kind, "slug": args.slug, "limit": args.limit, "locale": args.locale},
        )
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        elif args.slug and data.get("markdown"):
            print(data["markdown"], end="")
        else:
            for item in data.get("articles", []):
                print(f"• {item['title']} ({item['slug']}) -> {item['canonicalUrl']}")
            for item in data.get("recentChanges", []):
                print(f"• [{item['updatedAt']}] {item['name']} -> {item['canonicalUrl']}")
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
