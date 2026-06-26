#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from html import unescape
from pathlib import Path
from typing import Iterable


USER_AGENT = "Mozilla/5.0 (compatible; gold-news-sentiment/1.1)"

DEFAULT_QUERIES = [
    "gold price",
    "spot gold",
    "Fed rates gold",
    "US Treasury yields gold",
    "dollar index gold",
    "inflation gold",
    "central bank gold buying",
    "gold ETF flows",
    "geopolitics gold safe haven",
]

PROVIDERS = {
    "google": "https://news.google.com/rss/search",
    "bing": "https://www.bing.com/news/search",
}


@dataclass
class NewsItem:
    title: str
    source: str
    published_at: str
    age_hours: float | None
    link: str
    query: str
    provider: str
    tags: list[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch recent global gold-related news from RSS-style providers."
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
        choices=sorted(PROVIDERS),
        dest="providers",
        help="Restrict to specific provider(s). Default: google + bing.",
    )
    parser.add_argument(
        "--hours",
        type=int,
        default=48,
        help="Only keep items newer than this many hours. Default: 48.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=40,
        help="Maximum number of items to print after filtering. Default: 40.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=12,
        help="HTTP timeout in seconds per request. Default: 12.",
    )
    parser.add_argument(
        "--lang",
        default="en-US",
        help="Language code for providers that support it. Default: en-US.",
    )
    parser.add_argument(
        "--country",
        default="US",
        help="Country edition for providers that support it. Default: US.",
    )
    parser.add_argument(
        "--max-workers",
        type=int,
        default=4,
        help="Maximum concurrent network requests. Default: 4.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        help="Optional output path for the JSON payload.",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print the JSON output.",
    )
    return parser.parse_args()


def build_url(provider: str, query: str, lang: str, country: str) -> str:
    if provider == "google":
        params = {
            "q": query,
            "hl": lang,
            "gl": country,
            "ceid": f"{country}:{lang.split('-')[0]}",
        }
        return f"{PROVIDERS[provider]}?{urllib.parse.urlencode(params)}"

    if provider == "bing":
        params = {
            "q": query,
            "format": "rss",
            "setlang": lang,
        }
        return f"{PROVIDERS[provider]}?{urllib.parse.urlencode(params)}"

    raise ValueError(f"Unsupported provider: {provider}")


def fetch_feed(url: str, timeout: int) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def extract_source(item: ET.Element) -> str:
    source = item.findtext("source")
    if source:
        return source.strip()

    source_node = item.find("{http://search.yahoo.com/mrss/}source")
    if source_node is not None and source_node.text:
        return source_node.text.strip()

    return ""


def extract_published_at(item: ET.Element) -> datetime | None:
    raw = item.findtext("pubDate")
    if not raw:
        return None
    try:
        dt = parsedate_to_datetime(raw)
    except (TypeError, ValueError):
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def normalize_title(title: str) -> str:
    title = unescape(title).strip()
    separators = [" - ", " | ", " — ", " – "]
    for separator in separators:
        if separator in title:
            title = title.split(separator)[0].strip()
            break
    return " ".join(title.split())


def infer_tags(text: str) -> list[str]:
    lowered = text.lower()
    tags: list[str] = []
    keyword_map = {
        "fed": ["fed", "federal reserve", "rate cut", "rate hike"],
        "usd": ["dollar", "usd", "dxy"],
        "yields": ["yield", "treasury", "bond"],
        "inflation": ["inflation", "cpi", "ppi"],
        "labor": ["payroll", "jobs", "unemployment", "labor"],
        "geopolitics": ["war", "missile", "tariff", "sanction", "middle east"],
        "etf_flows": ["etf", "inflow", "outflow"],
        "central_bank": ["central bank", "reserve", "buying"],
        "safe_haven": ["safe haven", "risk-off"],
    }
    for tag, keywords in keyword_map.items():
        if any(keyword in lowered for keyword in keywords):
            tags.append(tag)
    if "gold" not in lowered:
        tags.append("gold_indirect")
    return sorted(set(tags))


def parse_feed(
    xml_bytes: bytes,
    query: str,
    provider: str,
    max_age: timedelta,
) -> list[NewsItem]:
    now = datetime.now(timezone.utc)
    root = ET.fromstring(xml_bytes)
    channel = root.find("channel")
    if channel is None:
        return []

    items: list[NewsItem] = []
    for item in channel.findall("item"):
        title = normalize_title(item.findtext("title") or "")
        if not title:
            continue
        link = (item.findtext("link") or "").strip()
        source = extract_source(item)
        published_at = extract_published_at(item)
        age_hours = None
        if published_at is not None:
            age = now - published_at
            if age > max_age:
                continue
            age_hours = round(age.total_seconds() / 3600, 2)

        context_text = " ".join(
            part for part in [title, source, item.findtext("description") or "", query] if part
        )
        items.append(
            NewsItem(
                title=title,
                source=source,
                published_at=published_at.isoformat() if published_at else "",
                age_hours=age_hours,
                link=link,
                query=query,
                provider=provider,
                tags=infer_tags(context_text),
            )
        )
    return items


def dedupe(items: Iterable[NewsItem]) -> list[NewsItem]:
    seen: set[tuple[str, str]] = set()
    deduped: list[NewsItem] = []
    for item in items:
        source = item.source.lower() if item.source else item.provider.lower()
        key = (item.title.lower(), source)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    return deduped


def sort_items(items: list[NewsItem]) -> list[NewsItem]:
    def sort_key(item: NewsItem) -> tuple[float, str, str]:
        age = item.age_hours if item.age_hours is not None else float("inf")
        return (age, item.title.lower(), item.provider)

    return sorted(items, key=sort_key)


def fetch_bucket(
    provider: str,
    query: str,
    lang: str,
    country: str,
    timeout: int,
    max_age: timedelta,
) -> tuple[list[NewsItem], dict[str, str] | None]:
    url = build_url(provider, query, lang, country)
    try:
        payload = fetch_feed(url, timeout)
        return parse_feed(payload, query, provider, max_age), None
    except Exception as exc:  # noqa: BLE001
        return [], {"provider": provider, "query": query, "error": str(exc)}


def collect_news(
    queries: list[str],
    providers: list[str],
    hours: int,
    timeout: int,
    lang: str,
    country: str,
    max_workers: int,
    limit: int,
) -> dict:
    max_age = timedelta(hours=max(hours, 1))
    all_items: list[NewsItem] = []
    failures: list[dict[str, str]] = []

    jobs = [(provider, query) for provider in providers for query in queries]
    with ThreadPoolExecutor(max_workers=max(1, min(max_workers, len(jobs) or 1))) as executor:
        future_map = {
            executor.submit(
                fetch_bucket, provider, query, lang, country, timeout, max_age
            ): (provider, query)
            for provider, query in jobs
        }
        for future in as_completed(future_map):
            items, failure = future.result()
            all_items.extend(items)
            if failure:
                failures.append(failure)
            time.sleep(0.05)

    items = sort_items(dedupe(all_items))[: max(limit, 1)]
    result = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "hours": hours,
        "providers": providers,
        "queries": queries,
        "item_count": len(items),
        "items": [asdict(item) for item in items],
    }
    if failures:
        result["failures"] = sorted(
            failures, key=lambda failure: (failure["provider"], failure["query"])
        )
    return result


def write_output(result: dict, out_path: Path | None, pretty: bool) -> None:
    payload = json.dumps(result, ensure_ascii=False, indent=2 if pretty else None)
    if out_path is not None:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(payload + "\n", encoding="utf-8")
    print(payload)


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
    write_output(result, args.out, args.pretty)
    return 0 if result["item_count"] or not result.get("failures") else 1


if __name__ == "__main__":
    raise SystemExit(main())
