#!/usr/bin/env python3
"""Query public lu.ma events the way the Luma app search box does."""

from __future__ import annotations

import argparse
import json
import urllib.error
import urllib.parse
import urllib.request

LUMA = "https://api.lu.ma/discover/get-paginated-events"
UA = "luma-events-query/1.2"

# App-style keyword + match needles.
CITY_GROUPS = [
    (["hangzhou", "杭州"], ["Hangzhou", "杭州"], ["hangzhou", "杭州", "hang zhou", "杭州市"]),
    (["chongqing", "重庆", "重慶"], ["Chongqing", "重庆"], ["chongqing", "重庆", "chong qing", "重庆市"]),
    (["shanghai", "上海"], ["Shanghai", "上海"], ["shanghai", "上海", "shang hai", "上海市"]),
    (["beijing", "北京"], ["Beijing", "北京"], ["beijing", "北京", "北京市"]),
    (["shenzhen", "深圳"], ["Shenzhen", "深圳"], ["shenzhen", "深圳", "shen zhen", "深圳市"]),
    (["chengdu", "成都"], ["Chengdu", "成都"], ["chengdu", "成都", "cheng du", "成都市"]),
    (["guangzhou", "广州", "廣州"], ["Guangzhou", "广州"], ["guangzhou", "广州", "广州市"]),
    (["nanjing", "南京"], ["Nanjing", "南京"], ["nanjing", "南京"]),
    (["wuhan", "武汉", "武漢"], ["Wuhan", "武汉"], ["wuhan", "武汉"]),
    (["suzhou", "苏州", "蘇州"], ["Suzhou", "苏州"], ["suzhou", "苏州"]),
    (["tokyo", "东京", "東京"], ["Tokyo", "东京"], ["tokyo", "东京", "東京"]),
    (["osaka", "大阪"], ["Osaka", "大阪"], ["osaka", "大阪"]),
    (["nyc", "new york", "纽约", "紐約"], ["New York"], ["new york", "nyc", "brooklyn", "manhattan"]),
    (["sf", "san francisco", "旧金山", "三藩"], ["San Francisco"], ["san francisco", "bay area"]),
    (["singapore", "新加坡"], ["Singapore"], ["singapore", "新加坡"]),
    (["hongkong", "hong kong", "香港"], ["Hong Kong", "香港"], ["hong kong", "hongkong", "香港"]),
    (["taipei", "台北"], ["Taipei", "台北"], ["taipei", "台北"]),
    (["seoul", "首尔", "首爾"], ["Seoul", "首尔"], ["seoul", "首尔", "首爾"]),
    (["london", "伦敦", "倫敦"], ["London"], ["london", "伦敦"]),
]

CITIES: dict[str, dict] = {}
for aliases, queries, needles in CITY_GROUPS:
    spec = {"queries": queries, "needles": needles}
    for alias in aliases:
        CITIES[alias] = spec
        CITIES[alias.lower()] = spec


def fail(message: str, **extra) -> None:
    print(json.dumps({"ok": False, "error": message, **extra}, ensure_ascii=False, indent=2))
    raise SystemExit(1)


def luma_get(params: dict[str, str]) -> dict:
    qs = urllib.parse.urlencode(params)
    url = f"{LUMA}?{qs}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        fail(f"Luma HTTP {exc.code}", body=exc.read().decode("utf-8", "replace")[:500])
    except urllib.error.URLError as exc:
        fail(f"网络错误: {exc.reason}")
    except json.JSONDecodeError:
        fail("Luma 响应不是 JSON")
    raise SystemExit(1)


def resolve_city(text: str) -> tuple[str, list[str], list[str], str | None]:
    raw = text.strip()
    key = raw.lower()
    spec = CITIES.get(key) or CITIES.get(raw)
    topic = None
    parts = raw.split()
    if spec is None and len(parts) >= 2:
        maybe_city = " ".join(parts[:-1])
        maybe_topic = parts[-1]
        spec = CITIES.get(maybe_city.lower()) or CITIES.get(maybe_city)
        if spec:
            raw = maybe_city
            topic = maybe_topic
    if spec:
        return raw, list(spec["queries"]), list(spec["needles"]), topic
    return raw, [raw], [raw.lower(), raw], topic


def blob(entry: dict) -> str:
    ev = entry.get("event") if isinstance(entry.get("event"), dict) else entry
    geo = ev.get("geo_address_info") or {}
    featured = entry.get("featured_city") or {}
    localized_cities = []
    loc = geo.get("localized") if isinstance(geo.get("localized"), dict) else {}
    for item in loc.values():
        if isinstance(item, dict):
            localized_cities.extend([item.get("city"), item.get("city_state")])
    parts = [
        ev.get("name"),
        ev.get("url"),
        geo.get("city"),
        geo.get("city_state"),
        featured.get("name") if isinstance(featured, dict) else featured,
        featured.get("slug") if isinstance(featured, dict) else None,
        *localized_cities,
    ]
    return " ".join(str(p) for p in parts if p).lower()


def summarize(entry: dict) -> dict:
    ev = entry.get("event") if isinstance(entry.get("event"), dict) else entry
    geo = ev.get("geo_address_info") or {}
    hosts = [
        h.get("name")
        for h in (entry.get("hosts") or [])
        if isinstance(h, dict) and h.get("name")
    ]
    slug = (ev.get("url") or "").strip()
    city = geo.get("city") or geo.get("city_state") or ""
    if geo.get("mode") == "obfuscated" and not city:
        city = "报名后可见"
    return {
        "event_api_id": ev.get("api_id") or entry.get("api_id"),
        "title": ev.get("name"),
        "date": ev.get("start_at") or entry.get("start_at"),
        "end_date": ev.get("end_at"),
        "timezone": ev.get("timezone"),
        "city": city,
        "country": geo.get("country") or "",
        "venue": geo.get("full_address") or geo.get("address") or city,
        "hosts": hosts,
        "luma_url": slug if slug.startswith("http") else (f"https://lu.ma/{slug}" if slug else ""),
        "matched": True,
    }


def matches(entry: dict, needles: list[str]) -> bool:
    text = blob(entry)
    return any(n.lower() in text for n in needles if n)


def cmd_search(args: argparse.Namespace) -> None:
    city = args.city or args.query
    if not city:
        fail("请提供城市或关键词，例如 杭州 / Hangzhou / 重庆 / 东京 AI")
    requested, queries, needles, topic = resolve_city(city)
    topic = args.topic or topic
    if topic:
        extra = []
        for q in queries:
            extra.extend([f"{q} {topic}", f"{topic} {q}"])
        queries = extra + queries
        needles = needles + [topic.lower(), topic]

    limit = max(int(args.limit), 1)
    seen: set[str] = set()
    matched: list[dict] = []
    other: list[dict] = []
    has_more = False

    for q in queries:
        data = luma_get(
            {
                "pagination_limit": str(min(max(limit * 2, 20), 50)),
                "query": q,
            }
        )
        has_more = has_more or bool(data.get("has_more"))
        for entry in data.get("entries") or []:
            ev = entry.get("event") if isinstance(entry.get("event"), dict) else {}
            eid = str(ev.get("api_id") or entry.get("api_id") or "")
            if not eid or eid in seen:
                continue
            seen.add(eid)
            row = summarize(entry)
            if matches(entry, needles):
                matched.append(row)
            else:
                row["matched"] = False
                other.append(row)
        if len(matched) >= limit:
            break

    events = matched[:limit]
    location_mismatch = len(matched) == 0

    print(
        json.dumps(
            {
                "ok": True,
                "source": "luma-discover-query",
                "requested": requested,
                "queries": queries,
                "topic": topic,
                "location_mismatch": location_mismatch,
                "matched": len(matched),
                "unrelated_dropped": len(other),
                "has_more": has_more,
                "total_returned": len(events),
                "events": events,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def cmd_cities(_: argparse.Namespace) -> None:
    print(
        json.dumps(
            {
                "ok": True,
                "note": "跟 Luma App 一样按关键词搜，不局限 87 城目录。中国大陆用中文或拼音。",
                "examples": [
                    "杭州 / Hangzhou",
                    "重庆 / Chongqing",
                    "上海 / 北京 / 深圳 / 成都 / 广州",
                    "东京 / 新加坡 / 香港 / 台北",
                ],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="luma-events")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_search = sub.add_parser("search", help="按 App 搜索框方式查活动")
    p_search.add_argument("query", nargs="?", help="城市或关键词，如 杭州 / Hangzhou / 东京 AI")
    p_search.add_argument("--city")
    p_search.add_argument("--topic", help="附加主题，如 AI")
    p_search.add_argument("--limit", type=int, default=10)
    p_search.set_defaults(func=cmd_search)
    p_cities = sub.add_parser("cities", help="说明搜索方式")
    p_cities.set_defaults(func=cmd_cities)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
