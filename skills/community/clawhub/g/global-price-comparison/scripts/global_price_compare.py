#!/usr/bin/env python3
"""Global price comparison helper.

Two workflows:
1) discover: search candidate product links across countries/sites (Brave + Tavily)
2) compare: normalize offer prices to USD and rank best/worst offers

Designed as a portable script for an AgentSkill.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import textwrap
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

DEFAULT_COUNTRIES = ["US", "UK", "JP", "DE", "FR", "CA", "AU", "SG", "HK", "TW"]

COUNTRY_META: dict[str, dict[str, str]] = {
    "US": {"name": "United States", "currency": "USD", "brave_country": "US", "lang": "en"},
    "UK": {"name": "United Kingdom", "currency": "GBP", "brave_country": "GB", "lang": "en"},
    "JP": {"name": "Japan", "currency": "JPY", "brave_country": "JP", "lang": "ja"},
    "DE": {"name": "Germany", "currency": "EUR", "brave_country": "DE", "lang": "de"},
    "FR": {"name": "France", "currency": "EUR", "brave_country": "FR", "lang": "fr"},
    "CA": {"name": "Canada", "currency": "CAD", "brave_country": "CA", "lang": "en"},
    "AU": {"name": "Australia", "currency": "AUD", "brave_country": "AU", "lang": "en"},
    "SG": {"name": "Singapore", "currency": "SGD", "brave_country": "SG", "lang": "en"},
    "HK": {"name": "Hong Kong", "currency": "HKD", "brave_country": "HK", "lang": "en"},
    "TW": {"name": "Taiwan", "currency": "TWD", "brave_country": "TW", "lang": "zh"},
    "CN": {"name": "China", "currency": "CNY", "brave_country": "CN", "lang": "zh"},
    "KR": {"name": "South Korea", "currency": "KRW", "brave_country": "KR", "lang": "ko"},
}

# Generic, globally reusable source categories.
SOURCE_QUERY_TEMPLATES: dict[str, str] = {
    "official_store": "{product} official store {country_name}",
    "marketplace": "{product} buy {country_name} marketplace",
    "electronics_retailer": "{product} electronics retailer {country_name}",
    "general_retailer": "{product} online store {country_name}",
}


def parse_list_arg(value: str | None, fallback: list[str]) -> list[str]:
    if not value:
        return fallback
    return [x.strip() for x in value.split(",") if x.strip()]


def http_json(url: str, headers: dict[str, str] | None = None, timeout: int = 20) -> Any:
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        charset = resp.headers.get_content_charset() or "utf-8"
        return json.loads(resp.read().decode(charset, errors="replace"))


def fetch_usd_rates(timeout: int = 20) -> dict[str, float]:
    # Base = USD; rates[x] means 1 USD = x currency.
    payload = http_json("https://open.er-api.com/v6/latest/USD", timeout=timeout)
    rates = payload.get("rates") or {}
    if not rates:
        raise RuntimeError("Failed to fetch USD exchange rates")
    rates["USD"] = 1.0
    return rates


def to_float(raw: str | float | int) -> float:
    if isinstance(raw, (int, float)):
        return float(raw)
    s = str(raw).strip()
    s = re.sub(r"[^0-9.,-]", "", s)
    # Handle both 1,234.56 and 1.234,56 heuristically.
    if s.count(",") > 0 and s.count(".") > 0:
        if s.rfind(",") > s.rfind("."):
            s = s.replace(".", "").replace(",", ".")
        else:
            s = s.replace(",", "")
    elif s.count(",") > 0 and s.count(".") == 0:
        s = s.replace(",", "")
    return float(s)


@dataclass
class Offer:
    product: str
    country: str
    currency: str
    source_type: str
    source_name: str
    price: float
    url: str


def load_offers_csv(path: Path) -> list[Offer]:
    required = {"product", "country", "currency", "source_type", "source_name", "price"}
    offers: list[Offer] = []
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Missing columns in CSV: {', '.join(sorted(missing))}")
        for row in reader:
            if not row.get("product") or not row.get("price"):
                continue
            offers.append(
                Offer(
                    product=row["product"].strip(),
                    country=row["country"].strip().upper(),
                    currency=row["currency"].strip().upper(),
                    source_type=row["source_type"].strip().lower(),
                    source_name=row["source_name"].strip(),
                    price=to_float(row["price"]),
                    url=(row.get("url") or "").strip(),
                )
            )
    return offers


def compare_offers(offers: list[Offer], rates: dict[str, float]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for o in offers:
        if o.currency not in rates:
            continue
        rate = rates[o.currency]
        usd = o.price / rate
        out.append(
            {
                "product": o.product,
                "country": o.country,
                "currency": o.currency,
                "source_type": o.source_type,
                "source_name": o.source_name,
                "price": round(o.price, 4),
                "price_usd": round(usd, 4),
                "url": o.url,
            }
        )
    out.sort(key=lambda r: r["price_usd"])

    if out:
        best = out[0]["price_usd"]
        worst = out[-1]["price_usd"]
        spread = worst - best
        for r in out:
            r["delta_vs_best_usd"] = round(r["price_usd"] - best, 4)
            r["delta_vs_best_pct"] = round(((r["price_usd"] - best) / best) * 100, 2) if best else 0.0
        out_summary = {
            "best_usd": round(best, 4),
            "worst_usd": round(worst, 4),
            "spread_usd": round(spread, 4),
            "spread_pct": round((spread / best) * 100, 2) if best else 0.0,
            "offer_count": len(out),
        }
    else:
        out_summary = {"best_usd": None, "worst_usd": None, "spread_usd": None, "spread_pct": None, "offer_count": 0}

    return [{"summary": out_summary, "offers": out}]


def print_compare_markdown(result: dict[str, Any]) -> None:
    s = result["summary"]
    offers = result["offers"]
    print("## Global Price Comparison (USD normalized)")
    if not offers:
        print("No valid offers to compare.")
        return
    print(f"- Offers: {s['offer_count']}")
    print(f"- Best: ${s['best_usd']:.2f}")
    print(f"- Worst: ${s['worst_usd']:.2f}")
    print(f"- Spread: ${s['spread_usd']:.2f} ({s['spread_pct']:.2f}%)")
    print()
    print("| Rank | Country | Source Type | Source | Local Price | USD | Δ vs Best | Link |")
    print("|---:|---|---|---|---:|---:|---:|---|")
    for i, r in enumerate(offers, start=1):
        local = f"{r['currency']} {r['price']:.2f}"
        usd = f"${r['price_usd']:.2f}"
        delta = f"${r['delta_vs_best_usd']:.2f} ({r['delta_vs_best_pct']:.2f}%)"
        link = r["url"] or ""
        print(f"| {i} | {r['country']} | {r['source_type']} | {r['source_name']} | {local} | {usd} | {delta} | {link} |")


def brave_search(query: str, country: str, search_lang: str, count: int, timeout: int) -> list[dict[str, str]]:
    key = os.environ.get("BRAVE_API_KEY", "").strip()
    if not key:
        raise RuntimeError("BRAVE_API_KEY is required for Brave search")

    candidates = [
        {
            "q": query,
            "count": str(count),
            "country": country,
            "search_lang": search_lang,
            "ui_lang": f"{search_lang}-{country}",
        },
        {
            "q": query,
            "count": str(count),
            "country": country,
            "search_lang": "en",
            "ui_lang": "en-US",
        },
    ]

    last_err: Exception | None = None
    for params in candidates:
        url = "https://api.search.brave.com/res/v1/web/search?" + urllib.parse.urlencode(params)
        try:
            payload = http_json(url, headers={"Accept": "application/json", "X-Subscription-Token": key}, timeout=timeout)
            results = []
            for item in (payload.get("web", {}) or {}).get("results", []) or []:
                results.append(
                    {
                        "title": item.get("title", ""),
                        "url": item.get("url", ""),
                        "description": item.get("description", ""),
                        "engine": "brave",
                    }
                )
            return results
        except urllib.error.HTTPError as e:
            last_err = e
            # Retry with fallback params for 422; 429 should bubble.
            if e.code == 422:
                continue
            raise

    if last_err:
        raise last_err
    return []


def tavily_search(query: str, count: int, timeout: int) -> list[dict[str, str]]:
    key = os.environ.get("TAVILY_API_KEY", "").strip()
    if not key:
        raise RuntimeError("TAVILY_API_KEY is required for Tavily search")

    url = "https://api.tavily.com/search"
    body = json.dumps(
        {
            "api_key": key,
            "query": query,
            "search_depth": "advanced",
            "max_results": count,
            "include_answer": False,
            "include_raw_content": False,
        }
    ).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/json")

    with urllib.request.urlopen(req, timeout=timeout) as resp:
        charset = resp.headers.get_content_charset() or "utf-8"
        payload = json.loads(resp.read().decode(charset, errors="replace"))

    results = []
    for item in payload.get("results", []) or []:
        results.append(
            {
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "description": item.get("content", ""),
                "engine": "tavily",
            }
        )
    return results


def dedupe_results(items: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[str] = set()
    out: list[dict[str, str]] = []
    for r in items:
        url = (r.get("url") or "").strip()
        if not url or url in seen:
            continue
        seen.add(url)
        out.append(r)
    return out


def discover_search(engine: str, query: str, country: str, search_lang: str, count: int, timeout: int) -> list[dict[str, str]]:
    engine = engine.lower()
    if engine == "brave":
        return brave_search(query, country=country, search_lang=search_lang, count=count, timeout=timeout)
    if engine == "tavily":
        return tavily_search(query, count=count, timeout=timeout)
    if engine == "all":
        # Preferred strategy: Brave first, Tavily only as fallback.
        brave_err: Exception | None = None
        try:
            brave_hits = discover_search("brave", query, country=country, search_lang=search_lang, count=count, timeout=timeout)
            if brave_hits:
                return dedupe_results(brave_hits)
        except Exception as ex:
            brave_err = ex

        try:
            tavily_hits = discover_search("tavily", query, country=country, search_lang=search_lang, count=count, timeout=timeout)
            if tavily_hits:
                return dedupe_results(tavily_hits)
        except Exception as ex:
            if brave_err:
                raise RuntimeError(f"brave: {brave_err}; tavily: {ex}") from ex
            raise

        if brave_err:
            raise RuntimeError(f"brave: {brave_err}; tavily: no results")
        return []
    raise ValueError(f"Unsupported search engine: {engine}")


def cmd_discover(args: argparse.Namespace) -> int:
    countries = [c.upper() for c in parse_list_arg(args.countries, DEFAULT_COUNTRIES)]
    source_types = parse_list_arg(args.source_types, list(SOURCE_QUERY_TEMPLATES.keys()))

    rows: list[dict[str, Any]] = []
    for c in countries:
        meta = COUNTRY_META.get(c, {"name": c, "brave_country": c, "lang": "en"})
        for st in source_types:
            if st not in SOURCE_QUERY_TEMPLATES:
                continue
            q = SOURCE_QUERY_TEMPLATES[st].format(product=args.product, country_name=meta["name"])
            try:
                hits = discover_search(
                    args.engine,
                    q,
                    country=meta["brave_country"],
                    search_lang=meta["lang"],
                    count=args.count,
                    timeout=args.timeout,
                )
            except Exception as e:
                rows.append({"country": c, "source_type": st, "query": q, "engine": args.engine, "error": str(e), "results": []})
                continue
            rows.append({"country": c, "source_type": st, "query": q, "engine": args.engine, "results": hits})

    payload = {
        "product": args.product,
        "countries": countries,
        "source_types": source_types,
        "engine": args.engine,
        "discoveries": rows,
    }

    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"## Candidate links for: {args.product}")
        print(f"Engine: `{args.engine}`")
        for row in rows:
            print(f"\n### {row['country']} · {row['source_type']}")
            print(f"Query: `{row['query']}`")
            if row.get("error"):
                print(f"- Error: {row['error']}")
                continue
            for i, r in enumerate(row.get("results", [])[: args.count], start=1):
                engine = r.get("engine", row.get("engine", ""))
                print(f"{i}. [{r['title']}]({r['url']}) {'· ' + engine if engine else ''}")

    if args.out:
        Path(args.out).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\nSaved: {args.out}")

    return 0


def cmd_compare(args: argparse.Namespace) -> int:
    offers = load_offers_csv(Path(args.input))
    if args.product:
        offers = [o for o in offers if o.product.lower() == args.product.lower()]

    rates = fetch_usd_rates(timeout=args.timeout)
    grouped: dict[str, list[Offer]] = {}
    for o in offers:
        grouped.setdefault(o.product, []).append(o)

    all_results: list[dict[str, Any]] = []
    for _, items in grouped.items():
        all_results.extend(compare_offers(items, rates))

    if args.format == "json":
        print(json.dumps(all_results, ensure_ascii=False, indent=2))
    else:
        for result in all_results:
            print_compare_markdown(result)
            print()

    if args.out:
        out = Path(args.out)
        if out.suffix.lower() == ".json":
            out.write_text(json.dumps(all_results, ensure_ascii=False, indent=2), encoding="utf-8")
        else:
            # flatten to CSV
            rows: list[dict[str, Any]] = []
            for result in all_results:
                rows.extend(result["offers"])
            if rows:
                with out.open("w", newline="", encoding="utf-8") as f:
                    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
                    w.writeheader()
                    w.writerows(rows)
            else:
                out.write_text("", encoding="utf-8")
        print(f"Saved: {out}")

    return 0


def cmd_template(args: argparse.Namespace) -> int:
    sample = textwrap.dedent(
        """\
        product,country,currency,source_type,source_name,price,url
        iPhone 16 Pro 256GB,US,USD,official_store,Apple US,1099,https://www.apple.com/
        iPhone 16 Pro 256GB,JP,JPY,official_store,Apple JP,159800,https://www.apple.com/jp/
        iPhone 16 Pro 256GB,DE,EUR,electronics_retailer,MediaMarkt,1229,https://www.mediamarkt.de/
        iPhone 16 Pro 256GB,HK,HKD,marketplace,HK Marketplace,8999,https://example.com/
        """
    )
    if args.out:
        Path(args.out).write_text(sample, encoding="utf-8")
        print(f"Saved template: {args.out}")
    else:
        print(sample)
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="global_price_compare.py",
        description="Global product price discovery + USD-normalized comparison",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """
            Examples:
              python scripts/global_price_compare.py template --out /tmp/offers.csv
              python scripts/global_price_compare.py discover --product "iPhone 16 Pro 256GB" --countries US,JP,DE --engine all --out /tmp/discover.json
              python scripts/global_price_compare.py compare --input /tmp/offers.csv --format markdown
            """
        ),
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    p_template = sub.add_parser("template", help="Print/write sample offers CSV template")
    p_template.add_argument("--out", help="Optional template output path")
    p_template.set_defaults(func=cmd_template)

    p_discover = sub.add_parser("discover", help="Find candidate product links by country/source type")
    p_discover.add_argument("--product", required=True, help="Product name/model to discover")
    p_discover.add_argument("--countries", help="Comma-separated country codes (e.g., US,JP,DE)")
    p_discover.add_argument(
        "--source-types",
        help="Comma-separated source types (official_store,marketplace,electronics_retailer,general_retailer)",
    )
    p_discover.add_argument("--count", type=int, default=3, help="Results per query (default: 3)")
    p_discover.add_argument("--engine", choices=["brave", "tavily", "all"], default="all", help="Search backend (default: all)")
    p_discover.add_argument("--format", choices=["markdown", "json"], default="markdown")
    p_discover.add_argument("--out", help="Optional JSON output file")
    p_discover.add_argument("--timeout", type=int, default=20)
    p_discover.set_defaults(func=cmd_discover)

    p_compare = sub.add_parser("compare", help="Compare offer prices (CSV input) in USD")
    p_compare.add_argument("--input", required=True, help="CSV input file path")
    p_compare.add_argument("--product", help="Optional exact product filter")
    p_compare.add_argument("--format", choices=["markdown", "json"], default="markdown")
    p_compare.add_argument("--out", help="Optional output file (.json or .csv)")
    p_compare.add_argument("--timeout", type=int, default=20)
    p_compare.set_defaults(func=cmd_compare)

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
