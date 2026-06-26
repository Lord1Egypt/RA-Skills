#!/usr/bin/env python3
"""
MovieMovie torrent search engine.

Searches multiple sources in parallel, merges/dedupes results,
classifies by size tier, and outputs JSON with magnet links.

Sources (basic, no key needed):
  - apibay.org (TPB JSON API) — best for new releases
  - bitsearch.to (HTML scrape) — best for catalog depth
  - torrentdownload.info (HTML scrape) — good all-around
  - YTS (JSON API, may be unreachable) — backup

Sources (enhanced, with TORRENTCLAW_API_KEY):
  - TorrentClaw — 30+ aggregated sources with quality scoring

Usage:
  python3 search_torrents.py "Inception" --year 2010 --json
  python3 search_torrents.py "Sinners" --quality 2160p
  python3 search_torrents.py "Night King" --imdb tt37284356 --top3
"""

import argparse
import json
import os
import re
import sys
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import (
    APIBAY_API, BITSEARCH_URL, TORRENTDL_URL, YTS_DOMAINS, TORRENTCLAW_API,
    CAT_MOVIES_HD, BROWSER_UA,
    http_get, http_get_json, build_magnet, make_result,
    dedupe_results, pick_top3, parse_quality,
    ok, fail, info, warn,
)


# ---------------------------------------------------------------------------
# Source: apibay.org (TPB JSON API)
# ---------------------------------------------------------------------------
def search_apibay(query, category=CAT_MOVIES_HD):
    """Search apibay.org. Returns list of result dicts."""
    q = urllib.parse.quote_plus(query)
    url = f"{APIBAY_API}/q.php?q={q}&cat={category}"
    data = http_get_json(url, timeout=8)
    if not data or not isinstance(data, list):
        return []
    results = []
    for item in data:
        if item.get("id") == "0" or item.get("name") == "No results returned":
            continue
        results.append(make_result(
            info_hash=item.get("info_hash", ""),
            name=item.get("name", ""),
            size_bytes=int(item.get("size", 0)),
            seeders=int(item.get("seeders", 0)),
            leechers=int(item.get("leechers", 0)),
            source="apibay",
            imdb=item.get("imdb", ""),
        ))
    return results


# ---------------------------------------------------------------------------
# Source: bitsearch.to (HTML scrape)
# ---------------------------------------------------------------------------
def search_bitsearch(query):
    """Scrape bitsearch.to search results. Returns list of result dicts."""
    q = urllib.parse.quote_plus(query)
    url = f"{BITSEARCH_URL}/search?q={q}&category=1&subcat=2"
    raw = http_get(url, timeout=10)
    if not raw:
        return []
    html = raw.decode("utf-8", errors="ignore")

    # Extract: /download/torrent/{HASH}?title={TITLE}
    pattern = r'/download/torrent/([0-9a-fA-F]{40})\?title=([^"&]+)'
    matches = re.findall(pattern, html)

    # Extract sizes
    sizes = re.findall(r'(\d+(?:\.\d+)?)\s*(GB|MB|TB|KB)', html, re.I)

    results = []
    seen_hashes = set()
    size_idx = 0
    for info_hash, title_enc in matches:
        h = info_hash.upper()
        if h in seen_hashes:
            size_idx += 1
            continue
        seen_hashes.add(h)

        name = urllib.parse.unquote_plus(title_enc)
        size_bytes = 0
        if size_idx < len(sizes):
            val, unit = float(sizes[size_idx][0]), sizes[size_idx][1].upper()
            multipliers = {"KB": 1024, "MB": 1024**2, "GB": 1024**3, "TB": 1024**4}
            size_bytes = int(val * multipliers.get(unit, 0))
        size_idx += 1

        results.append(make_result(
            info_hash=h, name=name, size_bytes=size_bytes,
            seeders=0,  # bitsearch HTML doesn't easily expose seeders
            source="bitsearch",
        ))
    return results


# ---------------------------------------------------------------------------
# Source: torrentdownload.info (HTML scrape)
# ---------------------------------------------------------------------------
def search_torrentdownload(query):
    """Scrape torrentdownload.info. Returns list of result dicts."""
    q = urllib.parse.quote_plus(query)
    url = f"{TORRENTDL_URL}/search?q={q}"
    raw = http_get(url, timeout=10)
    if not raw:
        return []
    html = raw.decode("utf-8", errors="ignore")

    # Extract: /{HASH}/{TITLE}
    pattern = r'/([0-9a-fA-F]{40})/([^"<]+)'
    matches = re.findall(pattern, html)

    results = []
    seen_hashes = set()
    for info_hash, title_raw in matches:
        h = info_hash.upper()
        if h in seen_hashes:
            continue
        seen_hashes.add(h)
        name = title_raw.replace("-", " ").replace("+", " ").strip()
        results.append(make_result(
            info_hash=h, name=name, source="torrentdownload",
        ))
    return results


# ---------------------------------------------------------------------------
# Source: YTS (JSON API, backup — may be unreachable)
# ---------------------------------------------------------------------------
def search_yts(query, imdb_id=None, quality=None):
    """Search YTS API. Tries multiple mirror domains. Returns list of result dicts."""
    params = {"limit": 20, "sort_by": "seeds", "order_by": "desc"}
    if imdb_id:
        params["query_term"] = imdb_id
    else:
        params["query_term"] = query
    if quality:
        params["quality"] = quality

    qs = urllib.parse.urlencode(params)

    for domain in YTS_DOMAINS:
        url = f"{domain}/list_movies.json?{qs}"
        data = http_get_json(url, timeout=6, retries=1)
        if not data:
            continue
        movies = data.get("data", {}).get("movies") or []
        results = []
        for movie in movies:
            for t in movie.get("torrents", []):
                results.append(make_result(
                    info_hash=t.get("hash", ""),
                    name=f"{movie.get('title', '')} ({movie.get('year', '')}) [{t.get('quality', '')}]",
                    size_bytes=int(t.get("size_bytes", 0)),
                    seeders=int(t.get("seeds", 0)),
                    leechers=int(t.get("peers", 0)),
                    source="yts",
                    imdb=movie.get("imdb_code", ""),
                ))
        if results:
            return results
    return []


# ---------------------------------------------------------------------------
# Source: TorrentClaw (enhanced, needs API key)
# ---------------------------------------------------------------------------
def search_torrentclaw(query, api_key, quality=None):
    """Search TorrentClaw API. Requires free API key. Returns list of result dicts."""
    params = {"q": query, "type": "movie"}
    if quality:
        params["quality"] = quality

    qs = urllib.parse.urlencode(params)
    url = f"{TORRENTCLAW_API}/search?{qs}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "User-Agent": BROWSER_UA,
    }
    data = http_get_json(url, headers=headers, timeout=12)
    if not data or "results" not in data:
        return []

    results = []
    for item in data.get("results", []):
        for t in item.get("torrents", []):
            info_hash = t.get("infoHash", "")
            magnet = t.get("magnetLink", "") or (build_magnet(info_hash, t.get("rawTitle", "")) if info_hash else "")
            results.append(make_result(
                info_hash=info_hash,
                name=t.get("rawTitle", item.get("title", "")),
                size_bytes=int(t.get("sizeBytes", 0)),
                seeders=int(t.get("seeders", 0)),
                leechers=int(t.get("leechers", 0)),
                source=f"torrentclaw:{t.get('source', '')}",
                magnet=magnet,
                imdb=item.get("imdbId", ""),
            ))
    return results


# ---------------------------------------------------------------------------
# Main search orchestrator
# ---------------------------------------------------------------------------
def search(query, year=None, imdb_id=None, quality=None):
    """
    Search all sources in parallel, merge, dedupe, sort.
    Returns list of result dicts sorted by quality then seeders.
    """
    search_query = query
    if year:
        search_query = f"{query} {year}"

    api_key = os.environ.get("TORRENTCLAW_API_KEY", "")
    all_results = []
    errors = []

    with ThreadPoolExecutor(max_workers=5) as pool:
        futures = {
            pool.submit(search_apibay, search_query): "apibay",
            pool.submit(search_bitsearch, search_query): "bitsearch",
            pool.submit(search_torrentdownload, search_query): "torrentdownload",
            pool.submit(search_yts, query, imdb_id, quality): "yts",
        }
        if api_key:
            futures[pool.submit(search_torrentclaw, query, api_key, quality)] = "torrentclaw"

        for future in as_completed(futures, timeout=20):
            source = futures[future]
            try:
                results = future.result()
                all_results.extend(results)
            except Exception as e:
                errors.append(f"{source}: {e}")

    # Deduplicate by info_hash
    all_results = dedupe_results(all_results)

    # Filter dead torrents (seeders = 0), but keep bitsearch results
    # (bitsearch doesn't expose seeders, so we keep them)
    filtered = [r for r in all_results if r["seeders"] > 0 or r["source"] == "bitsearch"]

    # Sort: 4K first, then by seeders
    resolution_rank = {"2160p": 4, "1080p": 3, "720p": 2, "480p": 1, "unknown": 0}
    filtered.sort(key=lambda x: (
        resolution_rank.get(x["quality"].get("resolution", "unknown"), 0),
        x["seeders"],
    ), reverse=True)

    return {
        "query": query,
        "year": year,
        "imdb_id": imdb_id,
        "total": len(filtered),
        "sources_searched": list(set(futures.values())),
        "errors": errors,
        "results": filtered,
        "top3": pick_top3(filtered),
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="MovieMovie torrent search")
    parser.add_argument("query", help="Movie title (English)")
    parser.add_argument("--year", help="Release year")
    parser.add_argument("--imdb", help="IMDB ID (e.g. tt1375666)")
    parser.add_argument("--quality", help="Quality filter (720p, 1080p, 2160p)")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--top3", action="store_true", help="Show only Top 3 tiers")
    args = parser.parse_args()

    result = search(args.query, year=args.year, imdb_id=args.imdb, quality=args.quality)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    # Human-readable output
    print(f"\n🎬 Search: {args.query}" + (f" ({args.year})" if args.year else ""))
    print(f"   Sources: {', '.join(result['sources_searched'])}")
    print(f"   Results: {result['total']} torrents found")
    if result["errors"]:
        for e in result["errors"]:
            warn(f"Source error: {e}")
    print()

    if args.top3 or not args.json:
        top3 = result["top3"]
        if top3:
            print("🏆 Top 3 recommended downloads:\n")
            for i, t in enumerate(top3, 1):
                q = t["quality"]
                res = q.get("resolution", "?")
                src = q.get("source", "?")
                codec = q.get("codec", "")
                hdr = q.get("hdr", "")
                tags = " ".join(filter(None, [res, src, codec, hdr]))
                print(f"  {i}. {t['tier_label']} ({t['size_gb']}GB) — {t['tier_desc']}")
                print(f"     {t['name'][:70]}")
                print(f"     [{tags}] seeds:{t['seeders']}")
                print(f"     {t['magnet'][:100]}...")
                print()
        else:
            fail("No results matching size tiers")

    if not args.top3:
        print(f"--- All {result['total']} results ---\n")
        for r in result["results"][:15]:
            q = r["quality"]
            res = q.get("resolution", "?")
            print(f"  [{res}] {r['size_gb']}GB seeds:{r['seeders']:>5} | {r['name'][:60]}")
            print(f"    src:{r['source']} hash:{r['info_hash'][:16]}...")
        if result["total"] > 15:
            info(f"... and {result['total'] - 15} more. Use --json for full list.")


if __name__ == "__main__":
    main()
