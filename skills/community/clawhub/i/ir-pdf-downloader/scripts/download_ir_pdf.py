#!/usr/bin/env python3
"""
IR PDF Downloader — Production Script (v2.0)

Downloads annual reports and quarterly results PDFs from Cloudflare-protected
Investor Relations (IR) websites. Now works for ANY company's IR site.

Usage:
    python3 download_ir_pdf.py <url> [url ...]              # Single or multiple URLs
    python3 download_ir_pdf.py --list urls.txt              # Batch from text file
    python3 download_ir_pdf.py --input companies.csv        # Batch from CSV/JSON
    python3 download_ir_pdf.py --search-domain ir.baidu.com  # Search Wayback Machine
    python3 download_ir_pdf.py --list-known-ir               # List known IR domains
    python3 download_ir_pdf.py --search-domain ir.alibaba.com --download-found --download-year 2024
"""

import argparse
import csv
import json
import os
import re
import sys
import time
import urllib.parse
from pathlib import Path
from typing import Optional

try:
    import requests
except ImportError:
    print("ERROR: 'requests' module not found. Install with: pip3 install requests", file=sys.stderr)
    sys.exit(1)

# ─── Constants ────────────────────────────────────────────────────────────────

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)

DEFAULT_HEADERS = {
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
}

DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds
MIN_PDF_SIZE = 10_000  # bytes — anything smaller is likely an error page
PDF_MAGIC = b"%PDF-"

# ─── Known IR Domains for Chinese Stocks ─────────────────────────────────────

KNOWN_IR_DOMAINS = {
    "JD.com": {
        "domain": "ir.jd.com",
        "pattern": "*/static-files/*.pdf",
        "note": "UUID-style URLs, use --search-domain ir.jd.com",
    },
    "Alibaba": {
        "domain": "ir.alibabagroup.com",
        "pattern": "*/en-US/assets/pdf/annual-report/*.pdf",
        "note": "Also: annual reports at /en-US/press/press-releases/",
    },
    "Baidu": {
        "domain": "ir.baidu.com",
        "pattern": "*/static-files/*.pdf",
        "note": "UUID-style URLs, use --search-domain ir.baidu.com",
    },
    "Tencent": {
        "domain": "ir.tencent.com",
        "pattern": "*/static-files/*.pdf",
        "note": "Annual reports at ir.tencent.com",
    },
    "PDD Holdings": {
        "domain": "ir.pddgroup.com",
        "pattern": "*/static-files/*.pdf",
        "note": "Use --search-domain ir.pddgroup.com",
    },
    "NetEase": {
        "domain": "ir.163.com",
        "pattern": "*/static-files/*.pdf",
        "note": "Use --search-domain ir.163.com",
    },
    "Meituan": {
        "domain": "ir.meituan.com",
        "pattern": "*/static-files/*.pdf",
        "note": "Use --search-domain ir.meituan.com",
    },
    "Xiaomi": {
        "domain": "ir.xiaomi.com",
        "pattern": "*/static-files/*.pdf",
        "note": "Use --search-domain ir.xiaomi.com",
    },
    "NIO": {
        "domain": "ir.nio.cn",
        "pattern": "*/static-files/*.pdf",
        "note": "Use --search-domain ir.nio.cn",
    },
    "Li Auto": {
        "domain": "ir.lixiang.com",
        "pattern": "*/static-files/*.pdf",
        "note": "Use --search-domain ir.lixiang.com",
    },
    "Bilibili": {
        "domain": "ir.bilibili.com",
        "pattern": "*/static-files/*.pdf",
        "note": "Use --search-domain ir.bilibili.com",
    },
    "Trip.com": {
        "domain": "ir.trip.com",
        "pattern": "*/static-files/*.pdf",
        "note": "Use --search-domain ir.trip.com",
    },
    "Ke Holdings": {
        "domain": "ir.ke.com",
        "pattern": "*/static-files/*.pdf",
        "note": "Use --search-domain ir.ke.com",
    },
    "XPeng": {
        "domain": "ir.xpeng.com",
        "pattern": "*/static-files/*.pdf",
        "note": "Use --search-domain ir.xpeng.com",
    },
    "ByteDance": {
        "domain": "ir.bytedance.com",
        "pattern": "*/static-files/*.pdf",
        "note": "Use --search-domain ir.bytedance.com",
    },
}

# ─── Logging ──────────────────────────────────────────────────────────────────

class Logger:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def _print(self, level: str, msg: str):
        ts = time.strftime("%H:%M:%S")
        print(f"[{ts}] [{level}] {msg}")

    def info(self, msg: str):
        self._print("INFO", msg)

    def warn(self, msg: str):
        self._print("WARN", msg)

    def error(self, msg: str):
        self._print("ERROR", msg)

    def debug(self, msg: str):
        if self.verbose:
            self._print("DEBUG", msg)

    def success(self, msg: str):
        self._print("OK", msg)


# ─── PDF Verification ──────────────────────────────────────────────────────────

def is_valid_pdf(data: bytes) -> bool:
    """Check PDF magic bytes at start of file."""
    return data[:5] == PDF_MAGIC


def verify_pdf(path: Path, min_size: int = MIN_PDF_SIZE) -> tuple[bool, str]:
    """
    Verify a downloaded file is a valid PDF.
    Returns (is_valid, reason).
    """
    if not path.exists():
        return False, f"File does not exist: {path}"

    size = path.stat().st_size
    if size < min_size:
        return False, f"File too small ({size:,} bytes), expected >={min_size:,} bytes"

    with open(path, "rb") as f:
        header = f.read(5)

    if header != PDF_MAGIC:
        return False, f"Invalid PDF magic bytes: {header!r} (expected {PDF_MAGIC!r})"

    return True, f"Valid PDF ({size:,} bytes)"


# ─── Filename Extraction ───────────────────────────────────────────────────────

def extract_filename_from_url(url: str) -> str:
    """Extract a meaningful filename from URL path."""
    parsed = urllib.parse.urlparse(url)
    path = parsed.path

    # Try to get the last path segment
    name = os.path.basename(path.rstrip("/"))
    if name.lower().endswith(".pdf"):
        return name

    # If UUID-style path, generate name from domain
    if len(name) > 30:  # UUID-like
        domain = parsed.netloc or "unknown"
        return f"{domain.replace('.', '_')}_report.pdf"

    return name + ".pdf" if name else "download.pdf"


def infer_referer(url: str) -> str:
    """Infer a valid Referer header from the URL."""
    parsed = urllib.parse.urlparse(url)
    netloc = parsed.netloc
    scheme = parsed.scheme or "https"
    # Use the IR root as referer
    return f"{scheme}://{netloc}/"


def infer_output_dir(url: str, output_dir: str | None) -> Path:
    """Determine output directory, optionally creating subdirs by domain."""
    if output_dir:
        base = Path(output_dir)
    else:
        base = Path("downloads")
    base.mkdir(parents=True, exist_ok=True)
    return base


# ─── Core Downloader ───────────────────────────────────────────────────────────

def download_from_url(
    url: str,
    output_path: Path | None = None,
    referer: str | None = None,
    timeout: int = DEFAULT_TIMEOUT,
    retries: int = MAX_RETRIES,
    verbose: bool = False,
    log: Logger | None = None,
) -> Path | None:
    """
    Generic PDF download for ANY IR website.
    Auto-detects Referer from URL domain.

    Returns the Path on success, None on failure.
    """
    if log is None:
        log = Logger(verbose=verbose)

    log.debug(f"Downloading: {url}")

    # Build headers — auto-detect Referer from URL
    resolved_referer = referer or infer_referer(url)
    headers = {
        **DEFAULT_HEADERS,
        "User-Agent": DEFAULT_USER_AGENT,
        "Referer": resolved_referer,
    }

    log.debug(f"Referer: {resolved_referer}")

    last_error = None
    for attempt in range(1, retries + 1):
        try:
            log.debug(f"Attempt {attempt}/{retries}")
            resp = requests.get(url, headers=headers, timeout=timeout, stream=True)

            if resp.status_code == 403:
                last_error = f"HTTP 403 Forbidden — IR site blocked. Check Referer (current: {resolved_referer})"
                log.warn(f"Attempt {attempt}: {last_error}")
            elif resp.status_code == 404:
                last_error = f"HTTP 404 Not Found — PDF URL does not exist: {url}"
                log.error(last_error)
                return None
            elif resp.status_code != 200:
                last_error = f"HTTP {resp.status_code} — unexpected response"
                log.warn(f"Attempt {attempt}: {last_error}")
            else:
                data = b"".join(resp.iter_content(chunk_size=65536))
                content_type = resp.headers.get("Content-Type", "")
                log.debug(f"Content-Type: {content_type}, Size: {len(data):,} bytes")

                if len(data) < MIN_PDF_SIZE:
                    last_error = f"Downloaded file too small ({len(data):,} bytes) — likely error/challenge page"
                    log.warn(f"Attempt {attempt}: {last_error}")
                else:
                    if output_path is None:
                        fname = extract_filename_from_url(url)
                        out_dir = infer_output_dir(url, None)
                        output_path = out_dir / fname

                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(output_path, "wb") as f:
                        f.write(data)

                    valid, reason = verify_pdf(output_path)
                    if not valid:
                        output_path.unlink(missing_ok=True)
                        last_error = f"PDF verification failed: {reason}"
                        log.warn(f"Attempt {attempt}: {last_error}")
                    else:
                        log.success(f"Downloaded {len(data):,} bytes → {output_path}")
                        return output_path

        except requests.exceptions.Timeout:
            last_error = f"Request timed out after {timeout}s"
            log.warn(f"Attempt {attempt}: {last_error}")
        except requests.exceptions.ConnectionError as e:
            last_error = f"Connection error: {e}"
            log.warn(f"Attempt {attempt}: {last_error}")
        except requests.exceptions.RequestException as e:
            last_error = f"Request failed: {e}"
            log.warn(f"Attempt {attempt}: {last_error}")

        if attempt < retries:
            log.debug(f"Retrying in {RETRY_DELAY}s...")
            time.sleep(RETRY_DELAY)

    log.error(f"All {retries} attempts failed. Last error: {last_error}")
    return None


# Alias for backwards compatibility
def download_pdf(*args, **kwargs) -> Path | None:
    return download_from_url(*args, **kwargs)


# ─── Wayback Machine CDX Search ─────────────────────────────────────────────────

def search_wayback_cdx(
    domain: str,
    verbose: bool = False,
    log: Logger | None = None,
    filter_year: int | None = None,
) -> list[dict]:
    """
    Search Wayback Machine CDX API for ALL PDF URLs under a domain.
    Returns list of dicts with keys: url, timestamp, statuscode.
    """
    if log is None:
        log = Logger(verbose=verbose)

    log.info(f"Searching Wayback Machine CDX for PDFs under: {domain}")

    # CDX API: find ALL PDF files anywhere under the domain (not just static-files)
    # We use from:*/to:* to get all time periods
    # Match: *://{domain}/*/*.pdf  OR  *://{domain}/*.pdf
    # The CDX API uses URL pattern matching
    url_patterns = [
        f"*{domain}*/*.pdf",
        f"*{domain}*/**/*.pdf",
    ]

    all_rows = []

    for pattern in url_patterns:
        encoded = urllib.parse.quote(pattern, safe="")
        cdx_url = (
            f"https://web.archive.org/cdx/search/cdx"
            f"?url={encoded}"
            f"&output=json"
            f"&limit=200"
            f"&fl=original,statuscode,mimetype,timestamp"
            f"&filter=statuscode:200"
            f"&filter=mimetype:application/pdf"
            f"&collapse=original"  # Deduplicate by URL
        )

        log.debug(f"CDX query: {pattern}")
        log.debug(f"URL: {cdx_url}")

        try:
            resp = requests.get(
                cdx_url,
                headers={"User-Agent": DEFAULT_USER_AGENT},
                timeout=20,
            )
            resp.raise_for_status()
            data = resp.json()

            if data and len(data) > 1:
                # First row is header
                header = data[0]
                rows = data[1:]
                for row in rows:
                    if len(row) >= 4:
                        url, status, mimetype, timestamp = row[0], row[1], row[2], row[3]
                        # Filter by year if requested
                        if filter_year:
                            ts_year = timestamp[:4]
                            if str(filter_year) != ts_year:
                                continue
                        all_rows.append({
                            "url": url,
                            "timestamp": timestamp,
                            "statuscode": status,
                            "domain": domain,
                        })
        except requests.exceptions.RequestException as e:
            log.warn(f"CDX request failed for pattern '{pattern}': {e}")
        except json.JSONDecodeError:
            log.warn(f"Failed to parse CDX response for pattern '{pattern}'")

    # Deduplicate by URL
    seen = set()
    unique = []
    for item in all_rows:
        if item["url"] not in seen:
            seen.add(item["url"])
            unique.append(item)

    log.info(f"Found {len(unique)} unique PDF URL(s)" + (f" from year {filter_year}" if filter_year else ""))
    return unique


def wayback_search_to_urls(results: list[dict]) -> list[str]:
    """Extract just the URLs from CDX search results."""
    return [r["url"] for r in results]


def print_wayback_results(results: list[dict], log: Logger):
    """Print CDX results in a readable format."""
    if not results:
        log.warn("No PDFs found.")
        return

    log.info(f"Found {len(results)} PDF URL(s):")
    print()
    for i, r in enumerate(results, 1):
        ts = r.get("timestamp", "unknown")
        year = ts[:4] if ts and len(ts) >= 4 else "?"
        print(f"  [{i}] {year}  {r['url']}")
    print()


# ─── Batch Download from CSV/JSON ───────────────────────────────────────────────

def load_input_file(path: str, log: Logger) -> list[dict]:
    """
    Load company data from CSV or JSON.
    CSV columns: company, url, out_dir (all optional except url)
    JSON: list of {company, url, out_dir} objects
    """
    path_obj = Path(path)
    if not path_obj.exists():
        log.error(f"Input file not found: {path}")
        sys.exit(1)

    ext = path_obj.suffix.lower()
    entries = []

    if ext == ".json":
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            entries = data
        else:
            log.error("JSON must be a list of objects with 'url' field")
            sys.exit(1)
    elif ext in (".csv", ".tsv"):
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("url", "").strip():
                    entries.append({
                        "company": row.get("company", "").strip(),
                        "url": row.get("url", "").strip(),
                        "out_dir": row.get("out_dir", "").strip(),
                    })
    else:
        log.error(f"Unsupported file type: {ext} (use .csv or .json)")
        sys.exit(1)

    log.info(f"Loaded {len(entries)} entry(ies) from {path}")
    return entries


def batch_from_input(
    entries: list[dict],
    verbose: bool = False,
    delay: float = 1.0,
    filter_year: int | None = None,
) -> dict:
    """
    Download PDFs from a list of {company, url, out_dir} entries.
    Returns {url: Path_or_None}.
    """
    log = Logger(verbose=verbose)
    results = {}

    for i, entry in enumerate(entries, 1):
        url = entry["url"]
        company = entry.get("company", "") or "unknown"
        out_dir = entry.get("out_dir", "") or None

        log.info(f"[{i}/{len(entries)}] {company}: {url}")
        path = download_from_url(
            url,
            output_path=None,
            referer=None,
            verbose=verbose,
            log=log,
        )
        results[url] = path

        if delay > 0 and i < len(entries):
            time.sleep(delay)

    succeeded = sum(1 for v in results.values() if v is not None)
    log.info(f"Batch complete: {succeeded}/{len(entries)} succeeded")
    return results


# ─── CLI ───────────────────────────────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        prog="download_ir_pdf.py",
        description="Download IR PDFs (annual reports, quarterly results) from ANY IR website. "
                    "Auto-detects Referer from URL domain.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download a single PDF (auto-detects Referer from URL)
  python3 download_ir_pdf.py "https://ir.jd.com/static-files/..."

  # Batch from text file
  python3 download_ir_pdf.py --list urls.txt

  # Search Wayback Machine for PDFs on any IR domain
  python3 download_ir_pdf.py --search-domain ir.baidu.com

  # Search + download from specific year
  python3 download_ir_pdf.py --search-domain ir.alibaba.com --download-found --download-year 2024

  # Batch from CSV/JSON with company names and output dirs
  python3 download_ir_pdf.py --input companies.csv

  # List known Chinese stock IR domains
  python3 download_ir_pdf.py --list-known-ir
        """,
    )

    parser.add_argument("urls", nargs="*", help="One or more PDF URLs to download")
    parser.add_argument("--list", "-l", metavar="FILE",
                        help="Path to a text file with URLs (one per line)")
    parser.add_argument("--input", "-i", metavar="FILE",
                        help="CSV or JSON file with columns: company, url, out_dir")
    parser.add_argument(
        "--search-domain", "-s", metavar="DOMAIN",
        help="Search Wayback Machine CDX for PDFs under this domain (e.g. ir.baidu.com)"
    )
    parser.add_argument(
        "--search-wb", "-w", metavar="DOMAIN",
        help="Alias for --search-domain (Wayback Machine search)"
    )
    parser.add_argument("--download-found", "-d", action="store_true",
                        help="Download all PDFs found by --search-domain")
    parser.add_argument("--download-year", "-y", type=int, metavar="YEAR",
                        help="Only download PDFs from this year (e.g. 2024)")
    parser.add_argument("--list-known-ir", action="store_true",
                        help="List known IR domains for Chinese stocks and exit")
    parser.add_argument("--output", "-o", metavar="DIR",
                        help="Output directory (default: ./downloads/)")
    parser.add_argument("--referer", "-r", metavar="URL",
                        help="Custom Referer header (default: auto-detected from URL)")
    parser.add_argument("--timeout", "-t", type=int, default=DEFAULT_TIMEOUT,
                        help=f"Request timeout in seconds (default: {DEFAULT_TIMEOUT})")
    parser.add_argument("--retries", type=int, default=MAX_RETRIES,
                        help=f"Number of retry attempts (default: {MAX_RETRIES})")
    parser.add_argument("--delay", type=float, default=1.0,
                        help="Delay between downloads in batch mode (default: 1.0s)")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Enable verbose debug output")

    return parser.parse_args()


def read_url_list(path: str) -> list[str]:
    """Read URLs from a file, one per line, skipping blanks and comments."""
    urls = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                urls.append(line)
    return urls


def list_known_ir(log: Logger):
    """Print the known IR domains table."""
    log.info("Known Chinese Stock IR Domains:")
    print()
    print(f"{'Company':<20} {'Domain':<25} {'Pattern'}")
    print("-" * 80)
    for company, info in KNOWN_IR_DOMAINS.items():
        domain = info["domain"]
        pattern = info["pattern"]
        print(f"{company:<20} {domain:<25} {pattern}")
    print()
    print("Usage: python3 download_ir_pdf.py --search-domain <domain> --download-found")


def main():
    args = parse_args()
    log = Logger(verbose=args.verbose)

    # ── List known IR domains ─────────────────────────────────────────────────
    if args.list_known_ir:
        list_known_ir(log)
        return

    # ── Wayback Machine search mode ──────────────────────────────────────────
    search_domain = args.search_domain or args.search_wb

    if search_domain:
        domain = search_domain
        if not re.match(r"^[a-zA-Z0-9.\-]+$", domain):
            log.error(f"Invalid domain format: {domain}")
            sys.exit(1)

        results = search_wayback_cdx(
            domain,
            verbose=args.verbose,
            log=log,
            filter_year=args.download_year,
        )
        print_wayback_results(results, log)

        if not results:
            log.warn("No PDFs found.")
            sys.exit(0)

        if args.download_found:
            pdf_urls = wayback_search_to_urls(results)
            print(f"--- Downloading {len(pdf_urls)} PDF(s) ---\n")
            wb_referer = f"https://{domain}/"
            for i, url in enumerate(pdf_urls, 1):
                log.info(f"[{i}/{len(pdf_urls)}] {url}")
                download_from_url(
                    url,
                    output_path=None,
                    referer=wb_referer,
                    timeout=args.timeout,
                    retries=args.retries,
                    verbose=args.verbose,
                    log=log,
                )
                if args.delay > 0 and i < len(pdf_urls):
                    time.sleep(args.delay)
        else:
            print(f"(Use --download-found to download all {len(results)} PDFs)")
        return

    # ── Collect URLs ──────────────────────────────────────────────────────────
    urls = []
    if args.urls:
        urls = list(args.urls)
    elif args.list:
        path = Path(args.list)
        if not path.exists():
            log.error(f"URL list file not found: {path}")
            sys.exit(1)
        urls = read_url_list(str(path))
        log.info(f"Loaded {len(urls)} URL(s) from {path}")
    elif args.input:
        # Load from CSV/JSON and download
        entries = load_input_file(args.input, log)
        if not entries:
            log.error("No entries found in input file.")
            sys.exit(1)
        results = batch_from_input(
            entries,
            verbose=args.verbose,
            delay=args.delay,
            filter_year=args.download_year,
        )
        failed = [url for url, path in results.items() if path is None]
        if failed:
            log.warn(f"{len(failed)} download(s) failed:")
            for url in failed:
                log.warn(f"  FAILED: {url}")
            sys.exit(1)
        return
    else:
        log.error("No URLs provided. Use positional args, --list FILE, --input FILE, or --search-domain DOMAIN.")
        parser.print_help()
        sys.exit(1)

    if not urls:
        log.error("No URLs to download.")
        sys.exit(1)

    # ── Download ──────────────────────────────────────────────────────────────
    if len(urls) == 1:
        log.info(f"Downloading: {urls[0]}")
        result = download_from_url(
            urls[0],
            output_path=None,
            referer=args.referer,
            timeout=args.timeout,
            retries=args.retries,
            verbose=args.verbose,
            log=log,
        )
        if result is None:
            sys.exit(1)
    else:
        results = {}
        for i, url in enumerate(urls, 1):
            log.info(f"[{i}/{len(urls)}] {url}")
            path = download_from_url(
                url,
                output_path=None,
                referer=args.referer,
                timeout=args.timeout,
                retries=args.retries,
                verbose=args.verbose,
                log=log,
            )
            results[url] = path
            if args.delay > 0 and i < len(urls):
                time.sleep(args.delay)

        failed = [url for url, path in results.items() if path is None]
        if failed:
            log.warn(f"{len(failed)} download(s) failed:")
            for url in failed:
                log.warn(f"  FAILED: {url}")
            sys.exit(1)


if __name__ == "__main__":
    main()
