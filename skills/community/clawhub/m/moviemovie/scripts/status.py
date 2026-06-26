#!/usr/bin/env python3
"""Check moviemovie environment status: python version, API keys, source reachability."""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import (
    APIBAY_API, BITSEARCH_URL, TORRENTDL_URL, TORRENTCLAW_API,
    http_get, ok, fail, info, warn,
)


def check_reachable(url, timeout=5):
    """Quick HEAD-like check: fetch a few bytes to confirm reachability."""
    try:
        data = http_get(url, timeout=timeout, retries=1)
        return data is not None and len(data) > 0
    except Exception:
        return False


def main():
    emit_json = "--json" in sys.argv

    py_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

    results = {
        "python3": sys.version_info >= (3, 10),
        "python3_version": py_ver,
        "torrentclaw_key": bool(os.environ.get("TORRENTCLAW_API_KEY")),
        "tmdb_key": bool(os.environ.get("TMDB_API_KEY")),
        "mode": "basic",
        "sources": {},
    }

    # Determine mode
    if results["torrentclaw_key"] and results["tmdb_key"]:
        results["mode"] = "full"
    elif results["torrentclaw_key"] or results["tmdb_key"]:
        results["mode"] = "enhanced"

    # Check source reachability (quick, parallel would be nice but keep it simple)
    results["sources"]["apibay"] = check_reachable(f"{APIBAY_API}/q.php?q=test&cat=207")
    results["sources"]["bitsearch"] = check_reachable(f"{BITSEARCH_URL}/search?q=test")
    results["sources"]["torrentdownload"] = check_reachable(f"{TORRENTDL_URL}/search?q=test")

    available_sources = sum(1 for v in results["sources"].values() if v)
    results["sources_available"] = available_sources
    results["all_ready"] = results["python3"] and available_sources >= 1

    if emit_json:
        print(json.dumps(results, indent=2))
        sys.exit(0 if results["all_ready"] else 1)

    # Human-readable output
    print()
    print("🎬 MovieMovie environment check")
    print()

    if results["python3"]:
        ok(f"Python {py_ver}")
    else:
        fail(f"Python {py_ver} (need 3.10+)")

    # Sources
    print()
    source_labels = {
        "apibay": "apibay.org (torrent search)",
        "bitsearch": "bitsearch.to (torrent search)",
        "torrentdownload": "torrentdownload.info (torrent search)",
    }
    for key, label in source_labels.items():
        if results["sources"].get(key):
            ok(label)
        else:
            fail(label)

    # API keys
    print()
    if results["torrentclaw_key"]:
        ok("TORRENTCLAW_API_KEY configured (30+ sources)")
    else:
        info("TORRENTCLAW_API_KEY not set (optional, see README)")

    if results["tmdb_key"]:
        ok("TMDB_API_KEY configured (structured movie data)")
    else:
        info("TMDB_API_KEY not set (optional, see README)")

    # Mode
    print()
    mode_labels = {
        "basic": "基础版 (3 torrent sources, WebSearch/WebFetch for movie data)",
        "enhanced": "增强版 (additional API sources enabled)",
        "full": "完整版 (TorrentClaw 30+ sources + TMDb structured data)",
    }
    info(f"Mode: {mode_labels[results['mode']]}")

    if results["mode"] == "basic":
        warn("Configure API keys for better results. See README.md")

    print()
    if results["all_ready"]:
        ok("Ready! Use /moviemovie to search movies.")
    else:
        fail("Some issues detected. Check above.")

    sys.exit(0 if results["all_ready"] else 1)


if __name__ == "__main__":
    main()
