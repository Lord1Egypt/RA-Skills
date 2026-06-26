#!/usr/bin/env python3
"""Generate search queries and process raw search results into findings.

Usage:
    scan_sources.py --generate-queries              Output JSON queries for web_search
    scan_sources.py --generate-queries --niche "X"  Queries for one niche only
    scan_sources.py --quick "topic description"     Quick queries without full config
    scan_sources.py --ingest <results.json>          Parse search results into findings
    scan_sources.py --ingest - < results.json        Read from stdin
"""

import argparse
import json
import os
import sys
from datetime import datetime

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(SKILL_DIR, "config.json")

# Default signal keywords if not in config
DEFAULT_SIGNAL_KEYWORDS = [
    "I wish", "someone should build", "looking for", "alternative to",
    "frustrated", "anyone solved", "workaround", "why is there no",
    "I'd pay for", "need a tool", "has anyone found",
]


def load_config():
    """Load config.json."""
    if not os.path.exists(CONFIG_PATH):
        print(f"Error: {CONFIG_PATH} not found. Run configure.py --init", file=sys.stderr)
        sys.exit(1)
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def source_to_site_filter(source):
    """Convert source format to search query site filter."""
    if source.startswith("reddit:r/"):
        subreddit = source.replace("reddit:r/", "")
        return f"site:reddit.com/r/{subreddit}"
    elif source == "hackernews":
        return "site:news.ycombinator.com"
    elif source.startswith("github:"):
        repo = source.replace("github:", "")
        return f"site:github.com/{repo}"
    return ""


def generate_queries_for_niche(niche, signal_keywords, max_queries=10):
    """Generate optimized search queries for a single niche.

    Strategy: batch signal keywords into groups and combine with niche keywords
    and source filters. Fewer, broader queries > many narrow ones.
    """
    queries = []
    niche_kws = niche.get("keywords", [])
    sources = niche.get("sources", [])
    extra_signals = niche.get("extra_signal_keywords", [])
    all_signals = signal_keywords + extra_signals

    # Group signal keywords into batches of 3 for OR-combined queries
    signal_batches = []
    for i in range(0, len(all_signals), 3):
        batch = all_signals[i:i + 3]
        signal_batches.append(batch)

    for niche_kw in niche_kws[:3]:  # Top 3 niche keywords
        for source in sources:
            site_filter = source_to_site_filter(source)
            for batch in signal_batches[:3]:  # Top 3 signal batches
                # Build query: site filter + niche keyword + signal keywords (OR'd)
                signal_part = " OR ".join(f'"{s}"' for s in batch)
                query = f"{site_filter} {niche_kw} ({signal_part})"
                queries.append({
                    "query": query.strip(),
                    "niche": niche["name"],
                    "source": source,
                    "niche_keyword": niche_kw,
                    "signal_keywords": batch,
                })

                if len(queries) >= max_queries:
                    return queries

    return queries


def generate_quick_queries(topic):
    """Generate queries for a quick scan without full config."""
    sources = [
        "site:reddit.com",
        "site:news.ycombinator.com",
    ]
    signal_batches = [
        ['"I wish"', '"someone should build"', '"looking for"'],
        ['"frustrated"', '"alternative to"', '"anyone solved"'],
        ['"workaround"', '"need a tool"', '"why is there no"'],
    ]

    queries = []
    for source in sources:
        for batch in signal_batches:
            signal_part = " OR ".join(batch)
            query = f"{source} {topic} ({signal_part})"
            queries.append({
                "query": query.strip(),
                "niche": topic,
                "source": source,
                "niche_keyword": topic,
                "signal_keywords": [s.strip('"') for s in batch],
            })

    return queries


def generate_queries(config, niche_filter=None):
    """Generate all search queries from config."""
    signal_keywords = config.get("default_signal_keywords", DEFAULT_SIGNAL_KEYWORDS)
    max_per_scan = config.get("max_queries_per_scan", 30)
    all_queries = []

    for niche in config.get("niches", []):
        if niche_filter and niche["name"].lower() != niche_filter.lower():
            continue
        per_niche_max = max_per_scan // max(len(config.get("niches", [])), 1)
        queries = generate_queries_for_niche(niche, signal_keywords, per_niche_max)
        all_queries.extend(queries)

    return all_queries[:max_per_scan]


def ingest_results(results_path):
    """Parse raw web_search results into standardized findings.

    Expected input: JSON array of search result objects, each with at minimum:
    - title (str)
    - url (str)
    - description/snippet (str)

    Can also handle the nested format where results are grouped by query.
    """
    if results_path == "-":
        raw = json.load(sys.stdin)
    else:
        with open(results_path, "r") as f:
            raw = json.load(f)

    findings = []
    seen_urls = set()

    # Handle both flat array and grouped-by-query format
    items = []
    if isinstance(raw, list):
        for entry in raw:
            if isinstance(entry, dict) and "results" in entry:
                # Grouped format: [{query: ..., results: [...]}, ...]
                query_meta = {
                    "niche": entry.get("niche", ""),
                    "source": entry.get("source", ""),
                    "signal_keywords": entry.get("signal_keywords", []),
                }
                for r in entry["results"]:
                    items.append({**r, **query_meta})
            else:
                items.append(entry)
    elif isinstance(raw, dict) and "results" in raw:
        items = raw["results"]

    for item in items:
        url = item.get("url", "")
        if not url or url in seen_urls:
            continue
        seen_urls.add(url)

        title = item.get("title", "")
        snippet = item.get("description", item.get("snippet", ""))

        # Detect source from URL
        source = "unknown"
        if "reddit.com" in url:
            source = "reddit"
            # Extract subreddit
            parts = url.split("/r/")
            if len(parts) > 1:
                sub = parts[1].split("/")[0]
                source = f"reddit:r/{sub}"
        elif "news.ycombinator.com" in url:
            source = "hackernews"
        elif "github.com" in url:
            source = "github"

        # Match signal keywords found in title + snippet
        text = f"{title} {snippet}".lower()
        matched = []
        all_signals = item.get("signal_keywords", DEFAULT_SIGNAL_KEYWORDS)
        for kw in all_signals:
            if kw.lower() in text:
                matched.append(kw)

        finding = {
            "title": title,
            "url": url,
            "snippet": snippet,
            "source": item.get("source", source),
            "niche": item.get("niche", ""),
            "date": item.get("date", item.get("age", datetime.now().strftime("%Y-%m-%d"))),
            "matched_keywords": matched,
        }
        findings.append(finding)

    # Sort by number of matched keywords descending (rough signal proxy)
    findings.sort(key=lambda x: len(x["matched_keywords"]), reverse=True)

    return findings


def main():
    parser = argparse.ArgumentParser(description="Scan sources for opportunity signals")
    parser.add_argument("--generate-queries", action="store_true", help="Output search queries")
    parser.add_argument("--niche", help="Filter to a specific niche")
    parser.add_argument("--quick", metavar="TOPIC", help="Quick scan queries for a topic")
    parser.add_argument("--ingest", metavar="FILE", help="Ingest search results (- for stdin)")

    args = parser.parse_args()

    if args.quick:
        queries = generate_quick_queries(args.quick)
        print(json.dumps(queries, indent=2))
        return

    if args.generate_queries:
        config = load_config()
        queries = generate_queries(config, args.niche)
        print(json.dumps(queries, indent=2))
        return

    if args.ingest:
        findings = ingest_results(args.ingest)
        print(json.dumps(findings, indent=2))
        return

    parser.print_help()


if __name__ == "__main__":
    main()
