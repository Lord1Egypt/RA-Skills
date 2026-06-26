#!/usr/bin/env python3
"""
Keyword Intelligence — Multi-Source Autocomplete Fetcher
Fetches keyword suggestions from Google, YouTube, Amazon, DuckDuckGo, Bing
Usage: python3 fetch_suggestions.py <keyword> [--sources all|google|youtube|amazon|ddg|bing] [--lang de] [--expand] [--csv] [--dedup]
"""

import sys
import json
import urllib.request
import urllib.parse
import argparse
import time
import csv
import io

def fetch_google(keyword, lang="de", region="de"):
    url = f"https://suggestqueries.google.com/complete/search?client=firefox&q={urllib.parse.quote(keyword)}&hl={lang}&gl={region}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read().decode())
            return data[1] if len(data) > 1 else []
    except:
        return []

def fetch_youtube(keyword, lang="de"):
    url = f"https://suggestqueries.google.com/complete/search?client=youtube&q={urllib.parse.quote(keyword)}&hl={lang}&ds=yt"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read().decode())
            return data[1] if len(data) > 1 else []
    except:
        return []

def fetch_amazon(keyword, region="de"):
    tld = "de" if region == "de" else "com"
    url = f"https://completion.amazon.{tld}/search/complete?method=completion&q={urllib.parse.quote(keyword)}&search-alias=aps"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read().decode())
            return data[1] if len(data) > 1 else []
    except:
        return []

def fetch_ddg(keyword):
    url = f"https://duckduckgo.com/ac/?q={urllib.parse.quote(keyword)}&type=list"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read().decode())
            return data[1] if len(data) > 1 else []
    except:
        return []

def fetch_bing(keyword, lang="de"):
    url = f"https://api.bing.com/osjson.aspx?query={urllib.parse.quote(keyword)}&language={lang}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read().decode())
            return data[1] if len(data) > 1 else []
    except:
        return []

def expand_suggestions(base_suggestions, source_fn, lang="de"):
    all_expanded = []
    seen = set(base_suggestions)
    for suggestion in base_suggestions[:5]:
        time.sleep(0.2)
        expanded = source_fn(suggestion, lang)
        for s in expanded:
            if s not in seen:
                seen.add(s)
                all_expanded.append(s)
    return all_expanded

def dedup_results(results):
    """Remove duplicates across all sources, keep first occurrence."""
    seen = set()
    deduped = {}
    for src, data in results.items():
        if isinstance(data, dict):
            base = [s for s in data["base"] if s not in seen and not seen.add(s)]
            expanded = [s for s in data.get("expanded", []) if s not in seen and not seen.add(s)]
            deduped[src] = {"base": base, "expanded": expanded}
        else:
            deduped[src] = [s for s in data if s not in seen and not seen.add(s)]
    return deduped

def to_csv(results, keyword):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["keyword", "source", "type"])
    for src, data in results.items():
        if isinstance(data, dict):
            for s in data.get("base", []):
                writer.writerow([s, src, "base"])
            for s in data.get("expanded", []):
                writer.writerow([s, src, "expanded"])
        else:
            for s in data:
                writer.writerow([s, src, "base"])
    return output.getvalue()

def main():
    parser = argparse.ArgumentParser(description="Multi-source keyword intelligence")
    parser.add_argument("keyword", help="Seed keyword")
    parser.add_argument("--sources", default="all", help="all|google|youtube|amazon|ddg|bing (comma-separated)")
    parser.add_argument("--lang", default="de", help="Language code (de, en, tr, ...)")
    parser.add_argument("--region", default="de", help="Region code (de, us, tr, ...)")
    parser.add_argument("--expand", action="store_true", help="Fetch 2nd-level suggestions from Google (~10x more)")
    parser.add_argument("--dedup", action="store_true", help="Remove duplicates across sources")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--csv", action="store_true", help="Output as CSV (keyword, source, type)")
    args = parser.parse_args()

    sources = args.sources.split(",") if args.sources != "all" else ["google", "youtube", "amazon", "ddg", "bing"]
    results = {}

    source_map = {
        "google": lambda: fetch_google(args.keyword, args.lang, args.region),
        "youtube": lambda: fetch_youtube(args.keyword, args.lang),
        "amazon": lambda: fetch_amazon(args.keyword, args.region),
        "ddg": lambda: fetch_ddg(args.keyword),
        "bing": lambda: fetch_bing(args.keyword, args.lang),
    }

    for src in sources:
        if src in source_map:
            suggestions = source_map[src]()
            if args.expand and src == "google":
                expanded = expand_suggestions(suggestions, fetch_google, args.lang)
                results[src] = {"base": suggestions, "expanded": expanded}
            else:
                results[src] = suggestions

    if args.dedup:
        results = dedup_results(results)

    if args.csv:
        print(to_csv(results, args.keyword))
    elif args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        total = 0
        for src, data in results.items():
            print(f"\n{'='*40}")
            print(f"  {src.upper()} — '{args.keyword}'")
            print(f"{'='*40}")
            if isinstance(data, dict):
                print(f"  Base ({len(data['base'])}):")
                for s in data["base"]:
                    print(f"    • {s}")
                    total += 1
                if data.get("expanded"):
                    print(f"\n  Expanded (+{len(data['expanded'])}):")
                    for s in data["expanded"]:
                        print(f"    ◦ {s}")
                        total += 1
            else:
                for s in data:
                    print(f"    • {s}")
                    total += 1
        print(f"\n  ✓ {total} keywords total\n")

if __name__ == "__main__":
    main()
