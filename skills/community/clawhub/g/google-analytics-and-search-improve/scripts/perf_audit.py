#!/usr/bin/env python3
from __future__ import annotations

"""Page performance & security audit tool.

Checks loading speed, compression, HSTS, HTML size, HTTP version,
and other technical SEO performance signals.

Usage:
    # Audit homepage
    python perf_audit.py --url "https://example.com/"

    # Audit multiple pages
    python perf_audit.py --url "https://example.com/" --pages "/about,/pricing"

    # Audit all pages from sitemap
    python perf_audit.py --url "https://example.com/" --sitemap

    # Output to file
    python perf_audit.py --url "https://example.com/" -o perf_report.json

Reads .env from: .skills-data/google-analytics-and-search-improve/.env
Env var: SITE_URL (fallback if --url not provided)
"""

import argparse
import json
import os
import re
import ssl
import sys
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

import utils  # noqa: F401  — triggers .env loading & warning suppression

try:
    import requests
except ImportError:
    print("Error: 'requests' package required. Install with: pip install requests", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

USER_AGENT = (
    "Mozilla/5.0 (compatible; PerfAuditBot/1.0; +https://github.com/skills/perf-audit)"
)
REQUEST_TIMEOUT = 20


def extract_sitemap_urls(sitemap_url: str) -> list[str]:
    try:
        resp = requests.get(sitemap_url, headers={"User-Agent": USER_AGENT},
                            timeout=REQUEST_TIMEOUT, allow_redirects=True)
        if resp.status_code != 200:
            return []
        content = resp.text
        urls = []
        if "<sitemapindex" in content.lower():
            sub_sitemaps = re.findall(r'<loc>\s*(.*?)\s*</loc>', content)
            for sub_url in sub_sitemaps:
                try:
                    sub_resp = requests.get(sub_url, headers={"User-Agent": USER_AGENT},
                                            timeout=REQUEST_TIMEOUT, allow_redirects=True)
                    if sub_resp.status_code == 200:
                        urls.extend(re.findall(r'<loc>\s*(.*?)\s*</loc>', sub_resp.text))
                except Exception:
                    pass
        else:
            urls = re.findall(r'<loc>\s*(.*?)\s*</loc>', content)
        return urls
    except Exception:
        return []


# ---------------------------------------------------------------------------
# Performance audit
# ---------------------------------------------------------------------------

def audit_page_performance(url: str) -> dict:
    """Measure performance metrics for a single page."""
    result = {
        "url": url,
        "status": None,
        "timing": {
            "dns_ms": None,
            "connect_ms": None,
            "tls_ms": None,
            "ttfb_ms": None,
            "download_ms": None,
            "total_ms": None,
        },
        "size": {
            "html_bytes": 0,
            "html_kb": 0,
            "transfer_bytes": 0,
            "transfer_kb": 0,
        },
        "compression": {
            "encoding": None,
            "is_compressed": False,
            "compression_ratio": None,
        },
        "headers": {
            "hsts": None,
            "hsts_ok": False,
            "content_type": None,
            "cache_control": None,
            "x_frame_options": None,
            "content_security_policy": False,
            "x_content_type_options": None,
            "server": None,
        },
        "https": {
            "is_https": url.startswith("https://"),
            "tls_version": None,
        },
        "redirect_count": 0,
        "issues": [],
        "checks": {},
    }

    try:
        # Make request with timing
        start_time = time.time()

        session = requests.Session()
        resp = session.get(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept-Encoding": "gzip, br, deflate",
            },
            timeout=REQUEST_TIMEOUT,
            allow_redirects=True,
        )
        total_time = time.time() - start_time

        result["status"] = resp.status_code
        result["redirect_count"] = len(resp.history)

        # Timing (approximate — for precise timing, curl is better)
        # We use elapsed from requests (excludes DNS in some cases)
        elapsed_ms = resp.elapsed.total_seconds() * 1000
        result["timing"]["total_ms"] = round(total_time * 1000, 1)
        result["timing"]["ttfb_ms"] = round(elapsed_ms, 1)

        # Size
        html_content = resp.text
        html_bytes = len(html_content.encode("utf-8"))
        result["size"]["html_bytes"] = html_bytes
        result["size"]["html_kb"] = round(html_bytes / 1024, 1)

        # Transfer size (compressed)
        transfer_bytes = len(resp.content)
        result["size"]["transfer_bytes"] = transfer_bytes
        result["size"]["transfer_kb"] = round(transfer_bytes / 1024, 1)

        # Compression
        encoding = resp.headers.get("Content-Encoding", "").lower()
        result["compression"]["encoding"] = encoding if encoding else "none"
        result["compression"]["is_compressed"] = encoding in ("gzip", "br", "deflate")
        if html_bytes > 0 and transfer_bytes > 0:
            result["compression"]["compression_ratio"] = round(transfer_bytes / html_bytes, 3)

        # Security headers
        headers = resp.headers
        hsts = headers.get("Strict-Transport-Security", "")
        result["headers"]["hsts"] = hsts if hsts else None
        result["headers"]["hsts_ok"] = bool(hsts) and "max-age=" in hsts.lower()
        result["headers"]["content_type"] = headers.get("Content-Type", "")
        result["headers"]["cache_control"] = headers.get("Cache-Control", "")
        result["headers"]["x_frame_options"] = headers.get("X-Frame-Options", "")
        result["headers"]["content_security_policy"] = bool(headers.get("Content-Security-Policy", ""))
        result["headers"]["x_content_type_options"] = headers.get("X-Content-Type-Options", "")
        result["headers"]["server"] = headers.get("Server", "")

        # TLS version
        if url.startswith("https://"):
            try:
                parsed = urlparse(url)
                hostname = parsed.hostname
                port = parsed.port or 443
                ctx = ssl.create_default_context()
                with ctx.wrap_socket(
                    __import__("socket").create_connection((hostname, port), timeout=5),
                    server_hostname=hostname,
                ) as ssock:
                    result["https"]["tls_version"] = ssock.version()
            except Exception:
                result["https"]["tls_version"] = "unknown"

        # --- Checks & Issues ---

        # Speed
        total_ms = result["timing"]["total_ms"]
        result["checks"]["fast_load"] = total_ms < 1000  # < 1s
        result["checks"]["very_fast_load"] = total_ms < 400  # < 0.4s (GEO target)

        if total_ms > 2000:
            result["issues"].append(f"Slow page load: {total_ms:.0f}ms (target < 400ms for GEO)")
        elif total_ms > 1000:
            result["issues"].append(f"Page load could be faster: {total_ms:.0f}ms (target < 400ms)")

        # Size
        result["checks"]["html_under_100kb"] = html_bytes < 102400
        if html_bytes > 102400:
            result["issues"].append(f"HTML too large: {result['size']['html_kb']}KB (target < 100KB)")

        # Compression
        result["checks"]["has_compression"] = result["compression"]["is_compressed"]
        result["checks"]["has_brotli"] = encoding == "br"
        if not result["compression"]["is_compressed"]:
            result["issues"].append("No compression detected — enable Brotli or gzip")
        elif encoding != "br":
            result["issues"].append(f"Using {encoding} compression — consider upgrading to Brotli (br)")

        # HSTS
        result["checks"]["has_hsts"] = result["headers"]["hsts_ok"]
        if not result["headers"]["hsts_ok"]:
            result["issues"].append("Missing or invalid HSTS header")

        # HTTPS
        result["checks"]["is_https"] = result["https"]["is_https"]
        if not result["https"]["is_https"]:
            result["issues"].append("Not using HTTPS — critical for SEO and trust")

        # Security headers
        result["checks"]["has_x_frame_options"] = bool(result["headers"]["x_frame_options"])
        result["checks"]["has_csp"] = result["headers"]["content_security_policy"]
        result["checks"]["has_x_content_type_options"] = bool(result["headers"]["x_content_type_options"])

        # Cache
        cache = result["headers"]["cache_control"]
        result["checks"]["has_cache_control"] = bool(cache)
        if not cache:
            result["issues"].append("No Cache-Control header — consider adding caching directives")

        # Redirects
        if result["redirect_count"] > 2:
            result["issues"].append(f"Too many redirects: {result['redirect_count']} (target ≤ 1)")

    except requests.exceptions.SSLError as exc:
        result["status"] = "ssl_error"
        result["issues"].append(f"SSL/TLS error: {exc}")
    except requests.exceptions.Timeout:
        result["status"] = "timeout"
        result["issues"].append(f"Request timed out after {REQUEST_TIMEOUT}s")
    except Exception as exc:
        result["status"] = "error"
        result["issues"].append(f"Request failed: {exc}")

    return result


# ---------------------------------------------------------------------------
# CDN detection
# ---------------------------------------------------------------------------

def detect_cdn(headers: dict) -> str | None:
    """Try to detect CDN from response headers."""
    server = headers.get("server", "").lower()
    via = headers.get("via", "").lower()
    cf_ray = headers.get("cf-ray", "")
    x_cache = headers.get("x-cache", "").lower()
    x_served_by = headers.get("x-served-by", "").lower()

    if cf_ray or "cloudflare" in server:
        return "Cloudflare"
    if "fastly" in via or "fastly" in x_served_by:
        return "Fastly"
    if "cloudfront" in via or "cloudfront" in x_cache:
        return "CloudFront (AWS)"
    if "akamai" in server or "akamai" in x_cache:
        return "Akamai"
    if "vercel" in server or "vercel" in x_cache:
        return "Vercel"
    if "netlify" in server:
        return "Netlify"
    if "bunny" in server.lower() or "bunnycdn" in server.lower():
        return "BunnyCDN"
    return None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Page performance & security audit tool")
    parser.add_argument("--url", default=os.environ.get("SITE_URL"),
                        help="Base URL of the site (or set SITE_URL env)")
    parser.add_argument("--sitemap", action="store_true",
                        help="Audit all pages from sitemap.xml")
    parser.add_argument("--pages", help="Comma-separated page paths to audit")
    parser.add_argument("--max-pages", type=int, default=20,
                        help="Max pages to audit from sitemap (default: 20)")
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")

    args = parser.parse_args()

    if not args.url:
        print("Error: --url required or set SITE_URL", file=sys.stderr)
        sys.exit(1)

    base_url = args.url.rstrip("/")
    if not base_url.startswith("http"):
        base_url = f"https://{base_url}"

    # Determine pages
    page_urls = []
    if args.pages:
        for path in args.pages.split(","):
            path = path.strip()
            if not path.startswith("/"):
                path = f"/{path}"
            page_urls.append(f"{base_url}{path}")
    elif args.sitemap:
        sitemap_url = f"{base_url}/sitemap.xml"
        print(f"Fetching sitemap: {sitemap_url}", file=sys.stderr)
        page_urls = extract_sitemap_urls(sitemap_url)
        if not page_urls:
            print("Warning: No URLs in sitemap, falling back to homepage", file=sys.stderr)
            page_urls = [f"{base_url}/"]
        else:
            print(f"Found {len(page_urls)} pages in sitemap", file=sys.stderr)
            if len(page_urls) > args.max_pages:
                print(f"Limiting to first {args.max_pages} pages", file=sys.stderr)
                page_urls = page_urls[:args.max_pages]
    else:
        page_urls = [f"{base_url}/"]

    print(f"Auditing performance on {len(page_urls)} page(s)...", file=sys.stderr)

    page_results = []
    for i, url in enumerate(page_urls, 1):
        print(f"  [{i}/{len(page_urls)}] {url}", file=sys.stderr)
        pr = audit_page_performance(url)

        # CDN detection (from first page's headers)
        if isinstance(pr.get("headers"), dict) and i == 1:
            # Refetch headers for CDN detection
            try:
                head_resp = requests.head(url, headers={"User-Agent": USER_AGENT},
                                          timeout=10, allow_redirects=True)
                cdn = detect_cdn(dict(head_resp.headers))
            except Exception:
                cdn = None
        else:
            cdn = None

        if cdn:
            pr["cdn_detected"] = cdn
        page_results.append(pr)
        if i < len(page_urls):
            time.sleep(0.5)

    # Aggregate
    all_issues = []
    for pr in page_results:
        for issue in pr["issues"]:
            all_issues.append({"url": pr["url"], "issue": issue})

    # Stats
    load_times = [pr["timing"]["total_ms"] for pr in page_results
                  if pr["timing"]["total_ms"] is not None]
    html_sizes = [pr["size"]["html_kb"] for pr in page_results
                  if pr["size"]["html_kb"] > 0]

    stats = {}
    if load_times:
        stats["avg_load_ms"] = round(sum(load_times) / len(load_times), 1)
        stats["min_load_ms"] = round(min(load_times), 1)
        stats["max_load_ms"] = round(max(load_times), 1)
        stats["pages_under_400ms"] = sum(1 for t in load_times if t < 400)
        stats["pages_under_1000ms"] = sum(1 for t in load_times if t < 1000)
    if html_sizes:
        stats["avg_html_kb"] = round(sum(html_sizes) / len(html_sizes), 1)
        stats["max_html_kb"] = round(max(html_sizes), 1)

    # Aggregate checks
    check_keys = set()
    for pr in page_results:
        check_keys.update(pr.get("checks", {}).keys())
    agg_checks = {}
    for key in sorted(check_keys):
        values = [pr["checks"].get(key) for pr in page_results if key in pr.get("checks", {})]
        passed = sum(1 for v in values if v)
        agg_checks[key] = {"passed": passed, "total": len(values)}

    # CDN info
    cdns = [pr.get("cdn_detected") for pr in page_results if pr.get("cdn_detected")]
    cdn_detected = cdns[0] if cdns else None

    result = {
        "tool": "perf_audit",
        "base_url": base_url,
        "pages_audited": len(page_results),
        "cdn_detected": cdn_detected,
        "summary": {
            "total_issues": len(all_issues),
            "stats": stats,
            "checks": agg_checks,
        },
        "issues": all_issues,
        "pages": page_results,
    }

    output = json.dumps(result, indent=2, ensure_ascii=False, default=str)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"\nOutput written to {args.output}", file=sys.stderr)
    else:
        print(output)

    # Quick summary
    print(f"\n{'='*60}", file=sys.stderr)
    print(f"Performance Audit Summary: {base_url}", file=sys.stderr)
    print(f"Pages audited: {len(page_results)}", file=sys.stderr)
    print(f"Total issues: {len(all_issues)}", file=sys.stderr)
    if stats.get("avg_load_ms"):
        print(f"Avg load time: {stats['avg_load_ms']:.0f}ms", file=sys.stderr)
        geo_pass = stats.get("pages_under_400ms", 0)
        print(f"Pages under 400ms (GEO target): {geo_pass}/{len(page_results)}", file=sys.stderr)
    if stats.get("avg_html_kb"):
        print(f"Avg HTML size: {stats['avg_html_kb']:.1f}KB", file=sys.stderr)
    if cdn_detected:
        print(f"CDN: {cdn_detected}", file=sys.stderr)
    else:
        print(f"CDN: ❌ Not detected", file=sys.stderr)
    print(f"{'='*60}", file=sys.stderr)


if __name__ == "__main__":
    main()
