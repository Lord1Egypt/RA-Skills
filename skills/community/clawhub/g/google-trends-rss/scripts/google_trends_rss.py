#!/usr/bin/env python3
"""Fetch Google Trends daily trending searches via public RSS feed.

No external dependencies.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import textwrap
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass, asdict
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any, Iterable

PRIMARY_RSS_URL = "https://trends.google.com/trending/rss"
LEGACY_RSS_URL = "https://trends.google.com/trends/trendingsearches/daily/rss"


COMMON_GEOS = {
    "HK": "Hong Kong",
    "US": "United States",
    "GB": "United Kingdom",
    "CA": "Canada",
    "AU": "Australia",
    "IN": "India",
    "SG": "Singapore",
    "JP": "Japan",
    "KR": "South Korea",
    "TW": "Taiwan",
    "DE": "Germany",
    "FR": "France",
    "ES": "Spain",
    "IT": "Italy",
    "BR": "Brazil",
    "MX": "Mexico",
}


@dataclass
class NewsItem:
    title: str
    snippet: str
    url: str
    source: str


@dataclass
class TrendItem:
    title: str
    approx_traffic: str
    link: str
    pub_date: str
    picture: str
    news_items: list[NewsItem]


def _local_name(tag: str) -> str:
    return tag.split("}", 1)[-1] if "}" in tag else tag


def _child_anyns(el: ET.Element | None, name: str) -> ET.Element | None:
    if el is None:
        return None
    for child in list(el):
        if _local_name(child.tag) == name:
            return child
    return None


def _children_anyns(el: ET.Element | None, name: str) -> list[ET.Element]:
    if el is None:
        return []
    return [child for child in list(el) if _local_name(child.tag) == name]


def _text_anyns(el: ET.Element | None, name: str) -> str:
    node = _child_anyns(el, name)
    return (node.text or "").strip() if node is not None else ""


def fetch_daily_rss(geo: str, timeout: int = 20) -> str:
    urls = [
        f"{PRIMARY_RSS_URL}?geo={urllib.parse.quote(geo)}",
        f"{LEGACY_RSS_URL}?geo={urllib.parse.quote(geo)}",
    ]

    last_http_error: RuntimeError | None = None
    for url in urls:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                charset = resp.headers.get_content_charset() or "utf-8"
                return resp.read().decode(charset, errors="replace")
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace") if hasattr(e, "read") else ""
            last_http_error = RuntimeError(f"HTTP {e.code} from Google Trends: {body[:300]}")
            # Try legacy endpoint only when primary 404s.
            if e.code == 404:
                continue
            raise last_http_error from e
        except urllib.error.URLError as e:
            raise RuntimeError(f"Network error fetching Google Trends: {e}") from e

    if last_http_error:
        raise last_http_error
    raise RuntimeError("Google Trends request failed without an explicit error.")


def parse_rss(xml_text: str) -> list[TrendItem]:
    root = ET.fromstring(xml_text)
    channel = _child_anyns(root, "channel")
    if channel is None:
        return []

    rows: list[TrendItem] = []
    for item in _children_anyns(channel, "item"):
        news_items: list[NewsItem] = []
        for news in _children_anyns(item, "news_item"):
            news_items.append(
                NewsItem(
                    title=_text_anyns(news, "news_item_title"),
                    snippet=_text_anyns(news, "news_item_snippet"),
                    url=_text_anyns(news, "news_item_url"),
                    source=_text_anyns(news, "news_item_source"),
                )
            )

        rows.append(
            TrendItem(
                title=_text_anyns(item, "title"),
                approx_traffic=_text_anyns(item, "approx_traffic"),
                link=_text_anyns(item, "link"),
                pub_date=_text_anyns(item, "pubDate"),
                picture=_text_anyns(item, "picture"),
                news_items=news_items,
            )
        )
    return rows


def to_flat_rows(items: Iterable[TrendItem], max_news: int = 2) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for it in items:
        base: dict[str, Any] = {
            "title": it.title,
            "approx_traffic": it.approx_traffic,
            "link": it.link,
            "pub_date": it.pub_date,
            "picture": it.picture,
        }
        for i in range(max_news):
            n = it.news_items[i] if i < len(it.news_items) else None
            idx = i + 1
            base[f"news_{idx}_title"] = n.title if n else ""
            base[f"news_{idx}_snippet"] = n.snippet if n else ""
            base[f"news_{idx}_url"] = n.url if n else ""
            base[f"news_{idx}_source"] = n.source if n else ""
        out.append(base)
    return out


def print_table(rows: list[TrendItem], limit: int) -> None:
    rows = rows[:limit]
    if not rows:
        print("No trends returned.")
        return

    print("#  Trend                              Traffic     Date")
    print("-  ---------------------------------- ---------- ------------------------")
    for i, r in enumerate(rows, start=1):
        title = (r.title[:34] + "…") if len(r.title) > 35 else r.title
        print(f"{i:<2} {title:<34} {r.approx_traffic[:10]:<10} {r.pub_date[:24]}")


def write_csv(path: Path, flat_rows: list[dict[str, Any]]) -> None:
    if not flat_rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(flat_rows[0].keys()))
        writer.writeheader()
        writer.writerows(flat_rows)


def traffic_score(approx_traffic: str) -> int:
    s = (approx_traffic or "").strip().lower()
    if not s:
        return 0
    m = re.search(r"([0-9]+(?:\.[0-9]+)?)\s*([kmb]?)", s)
    if not m:
        digits = re.sub(r"\D", "", s)
        return int(digits) if digits else 0

    num = float(m.group(1))
    suffix = m.group(2)
    mult = {"": 1, "k": 1_000, "m": 1_000_000, "b": 1_000_000_000}.get(suffix, 1)
    return int(num * mult)


def pub_date_ts(pub_date: str) -> float:
    try:
        return parsedate_to_datetime(pub_date).timestamp()
    except Exception:
        return 0.0


def sort_items(items: list[TrendItem], mode: str) -> list[TrendItem]:
    if mode == "feed":
        return items
    if mode == "recency":
        return sorted(items, key=lambda x: pub_date_ts(x.pub_date), reverse=True)
    if mode == "traffic":
        return sorted(items, key=lambda x: (traffic_score(x.approx_traffic), pub_date_ts(x.pub_date)), reverse=True)
    raise ValueError(f"Unsupported sort mode: {mode}")


def cmd_daily(args: argparse.Namespace) -> int:
    xml_text = fetch_daily_rss(args.geo.upper(), timeout=args.timeout)
    items = parse_rss(xml_text)
    items = sort_items(items, args.sort)
    items = items[: args.limit]

    if args.format == "table":
        print_table(items, args.limit)
    elif args.format == "json":
        payload = {
            "geo": args.geo.upper(),
            "sort": args.sort,
            "count": len(items),
            "items": [asdict(i) for i in items],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(f"## Google Trends Daily ({args.geo.upper()})")
        print(f"- Sort: {args.sort}")
        for i, r in enumerate(items, start=1):
            print(f"{i}. **{r.title}** — {r.approx_traffic}  ")
            print(f"   - Date: {r.pub_date}")
            print(f"   - Link: {r.link}")
            if r.news_items:
                print("   - News:")
                for ni in r.news_items[:2]:
                    print(f"     - {ni.title} ({ni.source})")
    else:
        raise ValueError(f"Unsupported format: {args.format}")

    if args.out:
        out_path = Path(args.out)
        if out_path.suffix.lower() == ".csv":
            write_csv(out_path, to_flat_rows(items, max_news=2))
        else:
            out_path.write_text(
                json.dumps(
                    {
                        "geo": args.geo.upper(),
                        "sort": args.sort,
                        "count": len(items),
                        "items": [asdict(i) for i in items],
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )
        print(f"\nSaved: {out_path}")

    return 0


def cmd_list_geos(_: argparse.Namespace) -> int:
    print("Common geo codes (pass to --geo):")
    for code, name in sorted(COMMON_GEOS.items()):
        print(f"- {code}: {name}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="google_trends_rss.py",
        description="Google Trends daily trending searches (public RSS).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """
            Examples:
              python scripts/google_trends_rss.py list-geos
              python scripts/google_trends_rss.py daily --geo HK --limit 20 --sort traffic --format table
              python scripts/google_trends_rss.py daily --geo US --format json --out /tmp/us-trends.json
              python scripts/google_trends_rss.py daily --geo JP --out /tmp/jp-trends.csv
            """
        ),
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    p_geos = sub.add_parser("list-geos", help="Print common geo codes.")
    p_geos.set_defaults(func=cmd_list_geos)

    p_daily = sub.add_parser("daily", help="Fetch daily trending searches for one geo.")
    p_daily.add_argument("--geo", required=True, help="Country/region code, e.g. HK, US, JP.")
    p_daily.add_argument("--limit", type=int, default=20, help="Max trends to return (default: 20).")
    p_daily.add_argument(
        "--format",
        choices=["table", "json", "markdown"],
        default="table",
        help="Output format (default: table).",
    )
    p_daily.add_argument(
        "--sort",
        choices=["traffic", "feed", "recency"],
        default="traffic",
        help="Sort mode (default: traffic).",
    )
    p_daily.add_argument("--out", help="Optional output file path (.json or .csv).")
    p_daily.add_argument("--timeout", type=int, default=20, help="HTTP timeout seconds (default: 20).")
    p_daily.set_defaults(func=cmd_daily)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except KeyboardInterrupt:
        return 130
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
