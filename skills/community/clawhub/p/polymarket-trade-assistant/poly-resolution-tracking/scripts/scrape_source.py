#!/usr/bin/env python3
"""
Generic HTML/JSON scraper for resolution data sources.

Supports known source types (e.g., Chatbot Arena leaderboard) and provides
generic table extraction for unknown sources.

Usage:
    python scrape_source.py --url <url> [--type arena_leaderboard] [--output FILE]
"""

import argparse
import json
import re
import sys
import http.client
import time
import urllib.request
from html.parser import HTMLParser


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

# Mapping from Polymarket candidate names to org identifiers for matching
# Used for Arena leaderboard mapping
MARKET_MAPPING = {
    "Anthropic": ["anthropic", "claude"],
    "Google": ["google", "gemini"],
    "OpenAI": ["openai", "gpt", "chatgpt", "o1", "o3", "o4"],
    "xAI": ["xai", "grok"],
    "Meta": ["meta", "llama"],
    "DeepSeek": ["deepseek"],
    "Amazon": ["amazon", "nova"],
    "Alibaba": ["alibaba", "qwen"],
    "Mistral": ["mistral"],
    "ByteDance": ["bytedance", "doubao"],
    "Nvidia": ["nvidia", "nemotron"],
}


# ---------------------------------------------------------------------------
# HTTP fetching
# ---------------------------------------------------------------------------

def fetch_html(url: str, max_retries: int = 3, backoff: float = 1.0) -> str:
    """Fetch URL content as string with retry."""
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except (urllib.error.URLError,
                http.client.IncompleteRead,
                http.client.RemoteDisconnected,
                TimeoutError,
                ConnectionResetError) as e:
            if attempt < max_retries - 1:
                wait = backoff * (2 ** attempt)
                print(f"[WARN] Retry {attempt + 1}/{max_retries} for {url[:80]}... ({e})", file=sys.stderr)
                time.sleep(wait)
            else:
                raise


# ---------------------------------------------------------------------------
# HTML table parsing
# ---------------------------------------------------------------------------

class TableParser(HTMLParser):
    """Parse HTML tables into rows of cells."""

    def __init__(self):
        super().__init__()
        self.tables = []
        self._current_table = None
        self._current_row = None
        self._current_cell = None
        self._in_cell = False

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self._current_table = []
        elif tag == "tr" and self._current_table is not None:
            self._current_row = []
        elif tag in ("td", "th") and self._current_row is not None:
            self._current_cell = ""
            self._in_cell = True

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self._in_cell:
            self._current_row.append(self._current_cell.strip())
            self._current_cell = None
            self._in_cell = False
        elif tag == "tr" and self._current_row is not None:
            if self._current_row:
                self._current_table.append(self._current_row)
            self._current_row = None
        elif tag == "table" and self._current_table is not None:
            if self._current_table:
                self.tables.append(self._current_table)
            self._current_table = None

    def handle_data(self, data):
        if self._in_cell and self._current_cell is not None:
            self._current_cell += data


def parse_html_tables(html: str) -> list:
    """Extract tables from HTML."""
    parser = TableParser()
    parser.feed(html)
    return parser.tables


def extract_next_data(html: str) -> dict | None:
    """Extract __NEXT_DATA__ JSON from Next.js page."""
    pattern = r'<script\s+id="__NEXT_DATA__"\s+type="application/json">(.*?)</script>'
    match = re.search(pattern, html, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            return None
    return None


# ---------------------------------------------------------------------------
# Arena leaderboard specific
# ---------------------------------------------------------------------------

def parse_arena_table(tables: list) -> list:
    """Parse Arena-style leaderboard tables into model entries."""
    models = []
    for table in tables:
        if len(table) < 2:
            continue

        header = [h.lower() for h in table[0]]

        score_cols = [i for i, h in enumerate(header) if any(k in h for k in ["score", "elo", "rating", "arena"])]
        name_cols = [i for i, h in enumerate(header) if any(k in h for k in ["model", "name", "system"])]
        rank_cols = [i for i, h in enumerate(header) if any(k in h for k in ["rank", "#", "pos"])]

        if not score_cols or not name_cols:
            continue

        score_col = score_cols[0]
        name_col = name_cols[0]
        rank_col = rank_cols[0] if rank_cols else None

        for i, row in enumerate(table[1:], 1):
            if len(row) <= max(score_col, name_col):
                continue
            name = row[name_col].strip()
            score_str = row[score_col].strip()

            score_match = re.match(r'([\d.]+)\s*(?:[±+\-/]+\s*([\d.]+))?', score_str)
            if not score_match:
                continue

            score = float(score_match.group(1))
            ci = float(score_match.group(2)) if score_match.group(2) else None

            rank = i
            if rank_col is not None and len(row) > rank_col:
                try:
                    rank = int(re.sub(r'[^\d]', '', row[rank_col]))
                except ValueError:
                    rank = i

            entry = {
                "rank": rank,
                "model": name,
                "score": score,
            }
            if ci is not None:
                entry["ci"] = ci

            for j, h in enumerate(header):
                if j in (score_col, name_col, rank_col):
                    continue
                if j < len(row) and row[j].strip():
                    entry[h] = row[j].strip()

            models.append(entry)

    return models


def identify_org(model_name: str) -> str | None:
    """Identify which Polymarket candidate an Arena model belongs to."""
    name_lower = model_name.lower()
    for org, keywords in MARKET_MAPPING.items():
        for kw in keywords:
            if kw in name_lower:
                return org
    return None


def map_to_market_candidates(models: list) -> dict:
    """Map leaderboard models to Polymarket market candidates.

    Returns: {org_name: {"best_model": str, "score": float, "ci": float|None, "rank": int}}
    """
    candidates = {}
    for m in models:
        org = identify_org(m["model"])
        if org is None:
            continue
        if org not in candidates or m["score"] > candidates[org]["score"]:
            candidates[org] = {
                "best_model": m["model"],
                "score": m["score"],
                "ci": m.get("ci"),
                "rank": m["rank"],
            }
    return candidates


def scrape_arena_leaderboard(url: str) -> dict:
    """Scrape Chatbot Arena leaderboard."""
    try:
        html = fetch_html(url)
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to fetch URL: {e}",
            "suggestion": "Use WebFetch tool to retrieve the leaderboard page content",
            "url": url,
        }

    print(f"[INFO] Received {len(html)} bytes from {url}", file=sys.stderr)

    # Strategy 1: HTML table parsing
    tables = parse_html_tables(html)
    if tables:
        models = parse_arena_table(tables)
        if models:
            print(f"[INFO] Parsed {len(models)} models from HTML tables", file=sys.stderr)
            candidates = map_to_market_candidates(models)
            return {
                "success": True,
                "method": "html_table",
                "url": url,
                "models_count": len(models),
                "models": models,
                "market_mapping": candidates,
            }

    # Strategy 2: Embedded JSON
    next_data = extract_next_data(html)
    if next_data:
        try:
            props = next_data.get("props", {}).get("pageProps", {})
            for key in ["leaderboard", "data", "models", "rankings", "entries"]:
                if key in props:
                    raw = props[key]
                    if isinstance(raw, list):
                        models = []
                        for i, entry in enumerate(raw):
                            if not isinstance(entry, dict):
                                continue
                            name = entry.get("model") or entry.get("name") or ""
                            score = entry.get("score") or entry.get("elo") or entry.get("rating")
                            if name and score:
                                try:
                                    score = float(score)
                                except (ValueError, TypeError):
                                    continue
                                model = {"rank": i + 1, "model": name, "score": score}
                                ci = entry.get("ci") or entry.get("se")
                                if ci:
                                    try:
                                        model["ci"] = float(ci)
                                    except (ValueError, TypeError):
                                        pass
                                models.append(model)
                        if models:
                            models.sort(key=lambda x: x["score"], reverse=True)
                            for i, m in enumerate(models):
                                m["rank"] = i + 1
                            candidates = map_to_market_candidates(models)
                            return {
                                "success": True,
                                "method": "embedded_json",
                                "url": url,
                                "models_count": len(models),
                                "models": models,
                                "market_mapping": candidates,
                            }
        except (AttributeError, TypeError):
            pass

    return {
        "success": False,
        "error": "Could not extract leaderboard data from page",
        "suggestion": (
            "The page likely renders content via JavaScript. "
            "Use WebFetch tool to get the rendered page content."
        ),
        "url": url,
    }


# ---------------------------------------------------------------------------
# Generic table scraping
# ---------------------------------------------------------------------------

def scrape_generic_tables(url: str) -> dict:
    """Scrape any HTML page and extract tables."""
    try:
        html = fetch_html(url)
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to fetch URL: {e}",
            "suggestion": "Use WebFetch tool to retrieve the page content",
            "url": url,
        }

    print(f"[INFO] Received {len(html)} bytes from {url}", file=sys.stderr)

    tables = parse_html_tables(html)
    if tables:
        result_tables = []
        for i, table in enumerate(tables):
            if len(table) < 2:
                continue
            result_tables.append({
                "table_index": i,
                "headers": table[0],
                "rows": table[1:],
                "row_count": len(table) - 1,
            })

        if result_tables:
            return {
                "success": True,
                "method": "html_table",
                "url": url,
                "tables_count": len(result_tables),
                "tables": result_tables,
            }

    # Try __NEXT_DATA__
    next_data = extract_next_data(html)
    if next_data:
        return {
            "success": True,
            "method": "next_data",
            "url": url,
            "data": next_data.get("props", {}).get("pageProps", {}),
        }

    return {
        "success": False,
        "error": "Could not extract structured data from page",
        "suggestion": "Use WebFetch tool to get the rendered page content",
        "url": url,
    }


# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------

def scrape_source(url: str, source_type: str = "auto") -> dict:
    """Scrape a resolution data source.

    Args:
        url: The URL to scrape
        source_type: "arena_leaderboard", "generic", or "auto" (detect from URL)
    """
    if source_type == "auto":
        url_lower = url.lower()
        if any(kw in url_lower for kw in ["arena", "lmarena", "lmsys"]):
            source_type = "arena_leaderboard"
        else:
            source_type = "generic"

    if source_type == "arena_leaderboard":
        return scrape_arena_leaderboard(url)
    else:
        return scrape_generic_tables(url)


def main():
    parser = argparse.ArgumentParser(description="Scrape resolution data source")
    parser.add_argument("--url", required=True, help="URL to scrape")
    parser.add_argument("--type", default="auto", choices=["auto", "arena_leaderboard", "generic"],
                        help="Source type (default: auto-detect)")
    parser.add_argument("--output", type=str, default=None, help="Output file path (default: stdout)")
    args = parser.parse_args()

    result = scrape_source(args.url, args.type)

    if result.get("success"):
        if result.get("market_mapping"):
            print(f"[INFO] Market candidate mapping:", file=sys.stderr)
            for org, data in sorted(result["market_mapping"].items(), key=lambda x: x[1]["score"], reverse=True):
                ci_str = f" +/-{data['ci']}" if data.get('ci') else ""
                print(f"  {org}: {data['best_model']} (#{data['rank']}, {data['score']}{ci_str})", file=sys.stderr)
        elif result.get("tables"):
            for t in result["tables"]:
                print(f"[INFO] Table {t['table_index']}: {t['row_count']} rows, headers: {t['headers']}", file=sys.stderr)
    else:
        print(f"[ERROR] {result.get('error', 'Unknown error')}", file=sys.stderr)

    json_str = json.dumps(result, indent=2, ensure_ascii=False)

    if args.output:
        with open(args.output, "w") as f:
            f.write(json_str)
        print(f"[INFO] Output written to {args.output}", file=sys.stderr)
    else:
        print(json_str)


if __name__ == "__main__":
    main()
