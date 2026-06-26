#!/usr/bin/env python3
"""
crawl.py — Web Crawler for GraphRAG Builder

Fetches pages using requests + BeautifulSoup (fast, lightweight).
Automatically falls back to Playwright when a page requires JavaScript.
Tracks crawl state in SQLite for incremental re-runs.
Outputs one JSON file per page into output/<slug>/raw_content/.

Usage:
    python crawl.py --url https://strudel.cc/workshop/getting-started/
    python crawl.py --url https://fastapi.tiangolo.com/tutorial/ --max-depth 2
    python crawl.py --url https://docs.example.com --force
"""

import argparse
import hashlib
import json
import os
import re
import sqlite3
import sys
import time
import urllib.robotparser
from collections import deque
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse, urlunparse

# ---------------------------------------------------------------------------
# Dependency bootstrap
# ---------------------------------------------------------------------------

def _ensure_deps():
    """Install missing dependencies at runtime."""
    deps = {
        "requests": "requests",
        "bs4": "beautifulsoup4",
        "lxml": "lxml",
    }
    missing = []
    for module, package in deps.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(package)

    if missing:
        print(f"Installing missing packages: {', '.join(missing)}")
        os.system(f"pip install {' '.join(missing)} --break-system-packages -q")
        print()

_ensure_deps()

import requests
from bs4 import BeautifulSoup


# ---------------------------------------------------------------------------
# URL utilities
# ---------------------------------------------------------------------------

def url_to_slug(url: str) -> str:
    """Turn a URL's domain into a filesystem-safe slug. strudel.cc → strudel-cc"""
    domain = urlparse(url).netloc.lstrip("www.")
    return re.sub(r"[^a-zA-Z0-9]", "-", domain).strip("-")


def url_to_hash(url: str) -> str:
    """Short SHA256 of URL for use as a stable filename."""
    return hashlib.sha256(url.encode()).hexdigest()[:16]


def content_hash(text: str) -> str:
    """SHA256 of page content for change detection."""
    return hashlib.sha256(text.encode()).hexdigest()


def normalize_url(url: str) -> str:
    """
    Canonicalize a URL for deduplication:
    - Remove fragment (#section)
    - Strip trailing slash from non-root paths
    - Lowercase scheme + host
    """
    p = urlparse(url)
    path = p.path.rstrip("/") or "/"
    return urlunparse((p.scheme.lower(), p.netloc.lower(), path, p.params, p.query, ""))


def same_domain(url: str, base_domain: str) -> bool:
    """True if url belongs to base_domain (with or without www.)."""
    host = urlparse(url).netloc.lower()
    base = base_domain.lower()
    return host == base or host == f"www.{base}" or f"www.{host}" == base


def is_crawlable_url(url: str) -> bool:
    """Skip binary files, mailto, javascript:, etc."""
    p = urlparse(url)
    if p.scheme not in ("http", "https"):
        return False
    skip_exts = {
        # Documents handled via extract_pdf_links(), not as HTML pages
        ".pdf",
        # Binary / media
        ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico",
        ".css", ".js", ".woff", ".woff2", ".ttf", ".eot",
        ".zip", ".tar", ".gz", ".mp3", ".mp4", ".webm", ".avi",
    }
    ext = os.path.splitext(p.path)[1].lower()
    return ext not in skip_exts


# ---------------------------------------------------------------------------
# Content extraction helpers
# ---------------------------------------------------------------------------

_JS_INDICATORS = [
    "javascript is required",
    "javascript must be enabled",
    "enable javascript",
    "requires javascript",
    "you need to enable javascript",
    "please enable javascript",
    "this page requires javascript",
]

def is_js_required(html: str) -> bool:
    """
    Heuristic: does this page require JavaScript to render its content?
    Two independent triggers — either one is sufficient:

    1. Keyword match: page explicitly says JS is required.
    2. Near-empty body: < 150 chars of visible text after stripping tags.
       React/Vue/SvelteKit apps typically render a single empty root div
       server-side, producing ~0-20 chars of visible text. Real documentation
       pages have at minimum a few sentences (150+ chars). Legitimate short
       pages (e.g. a one-line 404) may occasionally trigger this path, but
       Playwright will still render them correctly so false positives are safe.
    """
    soup = BeautifulSoup(html, "lxml")
    body = soup.find("body")
    text = body.get_text(separator=" ", strip=True) if body else ""
    if len(text) < 150:
        return True
    lower = html.lower()
    return any(ind in lower for ind in _JS_INDICATORS)


def extract_title(html: str) -> str:
    """Extract the best available title from HTML."""
    soup = BeautifulSoup(html, "lxml")
    if soup.title and soup.title.string:
        return soup.title.string.strip()
    h1 = soup.find("h1")
    if h1:
        return h1.get_text(strip=True)
    return ""


def extract_links(html: str, base_url: str) -> list[str]:
    """Extract all absolute <a href> links from HTML."""
    soup = BeautifulSoup(html, "lxml")
    links = []
    for tag in soup.find_all("a", href=True):
        href = tag["href"].strip()
        if not href or href.startswith("#"):
            continue
        full = urljoin(base_url, href)
        if is_crawlable_url(full):
            links.append(full)
    return links


def extract_youtube_ids(html: str) -> list[str]:
    """Extract YouTube video IDs from iframes, links, and embed tags."""
    patterns = [
        r"youtube\.com/embed/([A-Za-z0-9_-]{11})",
        r"youtube\.com/watch\?v=([A-Za-z0-9_-]{11})",
        r"youtu\.be/([A-Za-z0-9_-]{11})",
        r"youtube\.com/v/([A-Za-z0-9_-]{11})",
        r"youtube-nocookie\.com/embed/([A-Za-z0-9_-]{11})",
    ]
    ids = set()
    for pat in patterns:
        ids.update(re.findall(pat, html))
    return list(ids)


def extract_pdf_links(html: str, base_url: str) -> list[str]:
    """Extract links to PDF files."""
    soup = BeautifulSoup(html, "lxml")
    pdfs = []
    for tag in soup.find_all("a", href=True):
        href = tag["href"]
        if href.lower().endswith(".pdf"):
            pdfs.append(urljoin(base_url, href))
    return pdfs


# ---------------------------------------------------------------------------
# Fetch strategies
# ---------------------------------------------------------------------------

_REQUEST_HEADERS = {
    "User-Agent": (
        "GraphRAGBuilder/1.0 (open-source educational crawler; "
        "https://github.com/graphrag-builder)"
    ),
    "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


def fetch_static(url: str, session: requests.Session, timeout: int = 15) -> tuple[str | None, str]:
    """
    Fetch a URL with requests. Returns (html_content, status_message).
    status_message is "ok" on success, or an error description on failure.
    """
    try:
        resp = session.get(url, timeout=timeout, allow_redirects=True)
        resp.raise_for_status()
        content_type = resp.headers.get("content-type", "")
        if "text/html" not in content_type and "application/xhtml" not in content_type:
            return None, f"non-HTML content-type: {content_type}"
        return resp.text, "ok"
    except requests.exceptions.Timeout:
        return None, "timeout"
    except requests.exceptions.HTTPError as e:
        return None, f"HTTP {e.response.status_code}"
    except Exception as e:
        return None, str(e)


def fetch_playwright(url: str, wait_ms: int = 2000, timeout_ms: int = 30000) -> tuple[str | None, str]:
    """
    Fetch a URL using a headless Chromium browser via Playwright.
    Waits for network to settle (networkidle) before capturing HTML.
    Returns (html_content, status_message).
    """
    try:
        from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
    except ImportError:
        print("     Installing playwright...")
        os.system("pip install playwright --break-system-packages -q")
        os.system("playwright install chromium --with-deps 2>&1 | tail -5")
        from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent=_REQUEST_HEADERS["User-Agent"],
                java_script_enabled=True,
            )
            page = context.new_page()
            page.goto(url, timeout=timeout_ms, wait_until="networkidle")
            # Extra wait for dynamic rendering
            page.wait_for_timeout(wait_ms)
            html = page.content()
            browser.close()
            return html, "ok"
    except PWTimeout:
        return None, "playwright timeout"
    except Exception as e:
        return None, f"playwright error: {e}"


# ---------------------------------------------------------------------------
# SQLite state machine
# ---------------------------------------------------------------------------

class CrawlDB:
    """
    Tracks crawl state using an in-memory SQLite database, with JSON
    persistence to disk.

    Why in-memory? Some filesystems (Docker bind-mounts, certain Linux
    overlayfs configurations) reject SQLite's default journal file creation
    with a disk I/O error. Running in-memory avoids all locking/journaling
    issues. State is saved to <db_path>.json on every commit so it survives
    restarts.

    Status progression: crawled → extracted → embedded → graphed → complete
    """

    STATUSES = ("crawled", "extracted", "embedded", "graphed", "complete")

    def __init__(self, db_path: Path):
        # db_path is used as the base; we always write a .json sidecar
        # (never an actual .db file — see class docstring)
        self.json_path = db_path.with_suffix(".json")
        # Always in-memory; never write a .db file
        self.conn = sqlite3.connect(":memory:")
        self.conn.row_factory = sqlite3.Row
        self._init_schema()
        self._load_from_json()

    def _init_schema(self):
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS pages (
                url           TEXT    PRIMARY KEY,
                content_hash  TEXT    NOT NULL DEFAULT '',
                last_crawled  TEXT    NOT NULL DEFAULT '',
                title         TEXT    DEFAULT '',
                type          TEXT    DEFAULT 'html',
                status        TEXT    DEFAULT 'crawled',
                fetched_with  TEXT    DEFAULT 'requests',
                depth         INTEGER DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS crawl_meta (
                key   TEXT PRIMARY KEY,
                value TEXT
            );
        """)
        self.conn.commit()

    # ---- JSON persistence ----

    def _load_from_json(self):
        """Restore state from the JSON sidecar file if it exists."""
        if not self.json_path.exists():
            return
        try:
            with open(self.json_path) as f:
                data = json.load(f)
            for row in data.get("pages", []):
                self.conn.execute("""
                    INSERT OR REPLACE INTO pages
                        (url, content_hash, last_crawled, title, type,
                         status, fetched_with, depth)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (row["url"], row["content_hash"], row["last_crawled"],
                      row["title"], row["type"], row["status"],
                      row["fetched_with"], row["depth"]))
            for row in data.get("meta", []):
                self.conn.execute(
                    "INSERT OR REPLACE INTO crawl_meta (key, value) VALUES (?, ?)",
                    (row["key"], row["value"])
                )
            self.conn.commit()
        except Exception as e:
            print(f"  ⚠  Could not load crawl state: {e}")

    def _save_to_json(self):
        """Persist current in-memory state to the JSON sidecar file."""
        pages = [dict(r) for r in self.conn.execute("SELECT * FROM pages").fetchall()]
        meta = [dict(r) for r in self.conn.execute("SELECT * FROM crawl_meta").fetchall()]
        state = {"pages": pages, "meta": meta}
        with open(self.json_path, "w") as f:
            json.dump(state, f, indent=2)

    # ---- Public API ----

    def get_page(self, url: str) -> sqlite3.Row | None:
        return self.conn.execute(
            "SELECT * FROM pages WHERE url = ?", (url,)
        ).fetchone()

    def upsert_page(self, *, url, content_hash, title, status,
                    fetched_with, depth, page_type="html"):
        self.conn.execute("""
            INSERT INTO pages
                (url, content_hash, last_crawled, title, type, status, fetched_with, depth)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(url) DO UPDATE SET
                content_hash = excluded.content_hash,
                last_crawled = excluded.last_crawled,
                title        = excluded.title,
                type         = excluded.type,
                status       = excluded.status,
                fetched_with = excluded.fetched_with
        """, (url, content_hash, datetime.now().isoformat(),
              title, page_type, status, fetched_with, depth))
        self.conn.commit()
        self._save_to_json()

    def set_meta(self, key: str, value):
        self.conn.execute("""
            INSERT INTO crawl_meta (key, value) VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET value = excluded.value
        """, (key, str(value)))
        self.conn.commit()
        self._save_to_json()

    def update_page_status(self, url: str, status: str):
        """Used by later phases (extract, embed, graph) to advance status."""
        self.conn.execute(
            "UPDATE pages SET status = ? WHERE url = ?", (status, url)
        )
        self.conn.commit()
        self._save_to_json()

    def pages_with_status(self, status: str) -> list[sqlite3.Row]:
        return self.conn.execute(
            "SELECT * FROM pages WHERE status = ?", (status,)
        ).fetchall()

    def summary(self) -> dict:
        rows = self.conn.execute(
            "SELECT status, COUNT(*) as n FROM pages GROUP BY status"
        ).fetchall()
        return {r["status"]: r["n"] for r in rows}

    def close(self):
        self._save_to_json()
        self.conn.close()


# ---------------------------------------------------------------------------
# Main crawl function
# ---------------------------------------------------------------------------

def crawl(
    seed_url: str,
    max_depth: int = 3,
    output_dir: str = "./output",
    incremental: bool = True,
    rate_limit: float = 0.5,
) -> Path:
    """
    BFS crawl from seed_url up to max_depth hops.
    Returns the output package path (e.g. ./output/strudel-cc-mcp/).
    """
    parsed = urlparse(seed_url)
    base_domain = parsed.netloc.lstrip("www.")
    slug = url_to_slug(seed_url)

    # --- Output directories ---
    output_path = Path(output_dir) / f"{slug}-mcp"
    raw_dir = output_path / "raw_content"
    raw_dir.mkdir(parents=True, exist_ok=True)

    # --- SQLite ---
    db = CrawlDB(output_path / "crawl.db")
    db.set_meta("seed_url", seed_url)
    db.set_meta("max_depth", max_depth)
    db.set_meta("crawl_started", datetime.now().isoformat())

    # --- robots.txt ---
    rp = urllib.robotparser.RobotFileParser()
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    try:
        rp.set_url(robots_url)
        rp.read()
        print(f"  ✓  robots.txt loaded from {robots_url}")
    except Exception:
        rp = None
        print(f"  ⚠  robots.txt unavailable, proceeding without restrictions")

    # --- HTTP session ---
    session = requests.Session()
    session.headers.update(_REQUEST_HEADERS)

    # --- BFS state ---
    queue: deque[tuple[str, int]] = deque([(normalize_url(seed_url), 0)])
    visited: set[str] = set()
    stats = {
        "crawled": 0,
        "skipped_unchanged": 0,
        "skipped_robots": 0,
        "skipped_offsite": 0,
        "failed": 0,
        "js_fallbacks": 0,
    }

    print(f"\n{'━'*62}")
    print(f"  GraphRAG Builder — Crawler  (M1)")
    print(f"{'━'*62}")
    print(f"  Seed:    {seed_url}")
    print(f"  Domain:  {base_domain}")
    print(f"  Depth:   {max_depth}")
    print(f"  Output:  {output_path}")
    print(f"  Mode:    {'incremental (skip unchanged)' if incremental else 'full re-crawl'}")
    print(f"{'━'*62}\n")

    while queue:
        url, depth = queue.popleft()

        if url in visited:
            continue
        visited.add(url)

        if depth > max_depth:
            continue

        # Off-site check
        if not same_domain(url, base_domain):
            stats["skipped_offsite"] += 1
            continue

        # robots.txt
        if rp and not rp.can_fetch("*", url):
            print(f"  [robots]  {url}")
            stats["skipped_robots"] += 1
            continue

        print(f"  [{depth}/{max_depth}]  {url}")

        # --- Fetch ---
        html, status_msg = fetch_static(url, session)
        fetched_with = "requests"

        if html is None:
            print(f"           ✗  {status_msg}")
            stats["failed"] += 1
            continue

        # JS detection → Playwright fallback
        if is_js_required(html):
            print(f"           ↻  JS detected → Playwright")
            html, status_msg = fetch_playwright(url)
            fetched_with = "playwright"
            stats["js_fallbacks"] += 1
            if html is None:
                print(f"           ✗  Playwright failed: {status_msg}")
                stats["failed"] += 1
                continue

        # --- Incremental hash check ---
        c_hash = content_hash(html)
        if incremental:
            existing = db.get_page(url)
            if existing and existing["content_hash"] == c_hash and existing["status"] == "complete":
                print(f"           ✓  unchanged — skipping")
                stats["skipped_unchanged"] += 1
                # Still enqueue links from the stored page so we don't miss neighbours
                raw_file = raw_dir / f"{url_to_hash(url)}.json"
                if raw_file.exists():
                    with open(raw_file) as f:
                        data = json.load(f)
                    for link in data.get("outgoing_links", []):
                        norm = normalize_url(link)
                        if norm not in visited and depth < max_depth:
                            queue.append((norm, depth + 1))
                continue

        # --- Extract metadata ---
        title = extract_title(html)
        youtube_ids = extract_youtube_ids(html)
        pdf_links = extract_pdf_links(html, url)
        raw_links = extract_links(html, url)
        outgoing = list({normalize_url(l) for l in raw_links if same_domain(l, base_domain)})

        # --- Save raw JSON ---
        raw_file = raw_dir / f"{url_to_hash(url)}.json"
        page_data = {
            "url": url,
            "type": "html",
            "title": title,
            "raw_html": html,
            "outgoing_links": outgoing,
            "youtube_ids": youtube_ids,
            "pdf_links": pdf_links,
            "depth": depth,
            "fetched_with": fetched_with,
            "crawled_at": datetime.now().isoformat(),
        }
        with open(raw_file, "w", encoding="utf-8") as f:
            json.dump(page_data, f, ensure_ascii=False, indent=2)

        # --- Update SQLite ---
        db.upsert_page(
            url=url,
            content_hash=c_hash,
            title=title,
            status="crawled",
            fetched_with=fetched_with,
            depth=depth,
        )
        stats["crawled"] += 1

        print(
            f"           ✓  \"{title or '(no title)'}\"  "
            f"links={len(outgoing)}  yt={len(youtube_ids)}  pdf={len(pdf_links)}"
            f"  [{fetched_with}]"
        )

        # Enqueue internal links
        if depth < max_depth:
            for link in outgoing:
                norm = normalize_url(link)
                if norm not in visited:
                    queue.append((norm, depth + 1))

        time.sleep(rate_limit)

    # --- Wrap up ---
    db.set_meta("crawl_finished", datetime.now().isoformat())
    db.set_meta("pages_crawled_total", stats["crawled"])
    summary = db.summary()
    db.close()

    print(f"\n{'━'*62}")
    print(f"  Crawl complete!")
    print(f"  Pages crawled:       {stats['crawled']}")
    print(f"  Skipped (unchanged): {stats['skipped_unchanged']}")
    print(f"  Skipped (robots):    {stats['skipped_robots']}")
    print(f"  JS fallbacks:        {stats['js_fallbacks']}")
    print(f"  Failed:              {stats['failed']}")
    print(f"  DB status summary:   {summary}")
    print(f"  Output:              {output_path}/raw_content/")
    print(f"{'━'*62}\n")

    return output_path


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="GraphRAG Builder — Web Crawler (M1)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python crawl.py --url https://strudel.cc/workshop/getting-started/
  python crawl.py --url https://fastapi.tiangolo.com/tutorial/ --max-depth 2
  python crawl.py --url https://docs.example.com --max-depth 4 --force
        """,
    )
    parser.add_argument("--url", required=True, help="Seed URL to start crawling from")
    parser.add_argument("--max-depth", type=int, default=3, metavar="N",
                        help="Max link-hops from seed URL (default: 3)")
    parser.add_argument("--output", default="./output", metavar="DIR",
                        help="Root output directory (default: ./output)")
    parser.add_argument("--force", action="store_true",
                        help="Ignore stored content hashes; re-crawl everything")
    parser.add_argument("--rate-limit", type=float, default=0.5, metavar="SEC",
                        help="Seconds between requests (default: 0.5)")

    args = parser.parse_args()

    crawl(
        seed_url=args.url,
        max_depth=args.max_depth,
        output_dir=args.output,
        incremental=not args.force,
        rate_limit=args.rate_limit,
    )


if __name__ == "__main__":
    main()
