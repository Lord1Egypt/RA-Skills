#!/usr/bin/env python3
from __future__ import annotations

"""SEO audit tool — checks JSON-LD, meta tags, headings, sitemap, Open Graph, etc.

Usage:
    # Audit a single page
    python seo_audit.py --url "https://example.com/"

    # Audit all pages from sitemap
    python seo_audit.py --url "https://example.com/" --sitemap

    # Audit specific pages (comma-separated)
    python seo_audit.py --url "https://example.com/" --pages "/about,/pricing,/docs"

    # Output to file
    python seo_audit.py --url "https://example.com/" --sitemap -o report.json

Reads .env from: .skills-data/google-analytics-and-search-improve/.env
Env var: SITE_URL (fallback if --url not provided)
"""

import argparse
import json
import os
import re
import sys
import time
from html.parser import HTMLParser
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
    "Mozilla/5.0 (compatible; SEOAuditBot/1.0; +https://github.com/skills/seo-audit)"
)
REQUEST_TIMEOUT = 15


def fetch(url: str, *, follow_redirects: bool = True) -> requests.Response:
    """Fetch a URL with standard headers."""
    return requests.get(
        url,
        headers={"User-Agent": USER_AGENT, "Accept-Encoding": "gzip, br"},
        timeout=REQUEST_TIMEOUT,
        allow_redirects=follow_redirects,
    )


def safe_fetch(url: str) -> requests.Response | None:
    """Fetch with error handling — returns None on failure."""
    try:
        return fetch(url)
    except Exception as exc:
        print(f"  ⚠️  Failed to fetch {url}: {exc}", file=sys.stderr)
        return None


# ---------------------------------------------------------------------------
# Extraction helpers
# ---------------------------------------------------------------------------

def extract_json_ld(html: str) -> list[dict]:
    """Extract all JSON-LD blocks from HTML."""
    pattern = re.compile(
        r'<script\s+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        re.DOTALL | re.IGNORECASE,
    )
    results = []
    for match in pattern.finditer(html):
        raw = match.group(1).strip()
        if not raw:
            continue
        try:
            data = json.loads(raw)
            # Handle @graph arrays
            if isinstance(data, dict) and "@graph" in data:
                for item in data["@graph"]:
                    results.append(item)
            elif isinstance(data, list):
                results.extend(data)
            else:
                results.append(data)
        except json.JSONDecodeError:
            results.append({"_parse_error": True, "_raw": raw[:200]})
    return results


def extract_meta_tags(html: str) -> dict:
    """Extract meta tags, title, canonical, hreflang, and OG tags."""
    result = {
        "title": None,
        "title_length": 0,
        "description": None,
        "description_length": 0,
        "canonical": None,
        "hreflang": [],
        "open_graph": {},
        "twitter": {},
        "robots": None,
        "viewport": None,
    }

    # Title
    m = re.search(r'<title[^>]*>([^<]*)</title>', html, re.IGNORECASE)
    if m:
        result["title"] = m.group(1).strip()
        result["title_length"] = len(result["title"])

    # Meta description
    m = re.search(
        r'<meta\s+[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)["\']',
        html, re.IGNORECASE,
    )
    if not m:
        m = re.search(
            r'<meta\s+[^>]*content=["\']([^"\']*)["\'][^>]*name=["\']description["\']',
            html, re.IGNORECASE,
        )
    if m:
        result["description"] = m.group(1).strip()
        result["description_length"] = len(result["description"])

    # Canonical
    m = re.search(r'<link\s+[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']*)["\']', html, re.IGNORECASE)
    if not m:
        m = re.search(r'<link\s+[^>]*href=["\']([^"\']*)["\'][^>]*rel=["\']canonical["\']', html, re.IGNORECASE)
    if m:
        result["canonical"] = m.group(1).strip()

    # Hreflang
    for hm in re.finditer(
        r'<link\s+[^>]*rel=["\']alternate["\'][^>]*hreflang=["\']([^"\']*)["\'][^>]*href=["\']([^"\']*)["\']',
        html, re.IGNORECASE,
    ):
        result["hreflang"].append({"lang": hm.group(1), "href": hm.group(2)})

    # Open Graph
    for og in re.finditer(
        r'<meta\s+[^>]*property=["\']og:([^"\']*)["\'][^>]*content=["\']([^"\']*)["\']',
        html, re.IGNORECASE,
    ):
        result["open_graph"][f"og:{og.group(1)}"] = og.group(2)
    # Also match reversed attribute order
    for og in re.finditer(
        r'<meta\s+[^>]*content=["\']([^"\']*)["\'][^>]*property=["\']og:([^"\']*)["\']',
        html, re.IGNORECASE,
    ):
        result["open_graph"][f"og:{og.group(2)}"] = og.group(1)

    # Twitter Card
    for tw in re.finditer(
        r'<meta\s+[^>]*(?:name|property)=["\']twitter:([^"\']*)["\'][^>]*content=["\']([^"\']*)["\']',
        html, re.IGNORECASE,
    ):
        result["twitter"][f"twitter:{tw.group(1)}"] = tw.group(2)
    for tw in re.finditer(
        r'<meta\s+[^>]*content=["\']([^"\']*)["\'][^>]*(?:name|property)=["\']twitter:([^"\']*)["\']',
        html, re.IGNORECASE,
    ):
        result["twitter"][f"twitter:{tw.group(2)}"] = tw.group(1)

    # Robots
    m = re.search(
        r'<meta\s+[^>]*name=["\']robots["\'][^>]*content=["\']([^"\']*)["\']',
        html, re.IGNORECASE,
    )
    if m:
        result["robots"] = m.group(1).strip()

    # Viewport
    m = re.search(
        r'<meta\s+[^>]*name=["\']viewport["\'][^>]*content=["\']([^"\']*)["\']',
        html, re.IGNORECASE,
    )
    if m:
        result["viewport"] = m.group(1).strip()

    return result


def extract_headings(html: str) -> list[dict]:
    """Extract all headings (h1-h6) from HTML."""
    headings = []
    for m in re.finditer(r'<(h[1-6])[^>]*>(.*?)</\1>', html, re.IGNORECASE | re.DOTALL):
        level = m.group(1).lower()
        text = re.sub(r'<[^>]+>', '', m.group(2)).strip()
        if text:
            headings.append({
                "level": level,
                "text": text,
                "is_question": text.rstrip().endswith("?"),
            })
    return headings


def extract_sitemap_urls(sitemap_url: str) -> list[str]:
    """Parse sitemap.xml and return all <loc> URLs. Handles sitemap index files."""
    resp = safe_fetch(sitemap_url)
    if not resp or resp.status_code != 200:
        return []

    content = resp.text
    urls = []

    # Check if it's a sitemap index
    if "<sitemapindex" in content.lower():
        sub_sitemaps = re.findall(r'<loc>\s*(.*?)\s*</loc>', content)
        for sub_url in sub_sitemaps:
            sub_resp = safe_fetch(sub_url)
            if sub_resp and sub_resp.status_code == 200:
                urls.extend(re.findall(r'<loc>\s*(.*?)\s*</loc>', sub_resp.text))
    else:
        urls = re.findall(r'<loc>\s*(.*?)\s*</loc>', content)

    return urls


# ---------------------------------------------------------------------------
# Audit functions
# ---------------------------------------------------------------------------

def audit_page(url: str) -> dict:
    """Run full SEO audit on a single page."""
    result = {
        "url": url,
        "status": None,
        "redirect_chain": [],
        "json_ld": {"blocks": [], "types": [], "count": 0, "issues": []},
        "meta": {},
        "headings": [],
        "heading_stats": {},
        "issues": [],
        "checks": {},
    }

    # Fetch with redirect tracking
    try:
        resp = requests.get(
            url,
            headers={"User-Agent": USER_AGENT},
            timeout=REQUEST_TIMEOUT,
            allow_redirects=True,
        )
        result["status"] = resp.status_code
        if resp.history:
            result["redirect_chain"] = [
                {"url": r.url, "status": r.status_code} for r in resp.history
            ]
    except Exception as exc:
        result["status"] = "error"
        result["issues"].append(f"Fetch error: {exc}")
        return result

    html = resp.text

    # --- JSON-LD ---
    ld_blocks = extract_json_ld(html)
    result["json_ld"]["blocks"] = ld_blocks
    result["json_ld"]["count"] = len(ld_blocks)
    result["json_ld"]["types"] = [
        b.get("@type", "unknown") for b in ld_blocks if isinstance(b, dict) and not b.get("_parse_error")
    ]

    # JSON-LD checks
    has_website = any(b.get("@type") == "WebSite" for b in ld_blocks if isinstance(b, dict))
    has_webpage = any(b.get("@type") == "WebPage" for b in ld_blocks if isinstance(b, dict))
    has_breadcrumb = any(b.get("@type") == "BreadcrumbList" for b in ld_blocks if isinstance(b, dict))
    has_faq = any(b.get("@type") == "FAQPage" for b in ld_blocks if isinstance(b, dict))
    has_howto = any(b.get("@type") == "HowTo" for b in ld_blocks if isinstance(b, dict))

    result["checks"]["has_json_ld"] = len(ld_blocks) > 0
    result["checks"]["has_website_schema"] = has_website
    result["checks"]["has_webpage_schema"] = has_webpage
    result["checks"]["has_breadcrumb_schema"] = has_breadcrumb
    result["checks"]["has_faq_schema"] = has_faq
    result["checks"]["has_howto_schema"] = has_howto

    if len(ld_blocks) == 0:
        result["json_ld"]["issues"].append("No JSON-LD blocks found")
    if not has_website:
        result["json_ld"]["issues"].append("Missing WebSite schema")
    if not has_webpage:
        result["json_ld"]["issues"].append("Missing WebPage schema")
    if not has_breadcrumb:
        result["json_ld"]["issues"].append("Missing BreadcrumbList schema")

    # Check for parse errors
    parse_errors = [b for b in ld_blocks if isinstance(b, dict) and b.get("_parse_error")]
    if parse_errors:
        result["json_ld"]["issues"].append(f"{len(parse_errors)} JSON-LD block(s) failed to parse")

    # --- Meta tags ---
    meta = extract_meta_tags(html)
    result["meta"] = meta

    # Meta checks
    result["checks"]["has_title"] = bool(meta["title"])
    result["checks"]["title_length_ok"] = 30 <= meta["title_length"] <= 60 if meta["title"] else False
    result["checks"]["has_description"] = bool(meta["description"])
    result["checks"]["description_length_ok"] = 70 <= meta["description_length"] <= 160 if meta["description"] else False
    result["checks"]["has_canonical"] = bool(meta["canonical"])
    result["checks"]["has_hreflang"] = len(meta["hreflang"]) > 0
    result["checks"]["has_og_title"] = "og:title" in meta["open_graph"]
    result["checks"]["has_og_description"] = "og:description" in meta["open_graph"]
    result["checks"]["has_og_image"] = "og:image" in meta["open_graph"]
    result["checks"]["has_twitter_card"] = bool(meta["twitter"])
    result["checks"]["has_viewport"] = bool(meta["viewport"])

    if not meta["title"]:
        result["issues"].append("Missing <title> tag")
    elif meta["title_length"] > 60:
        result["issues"].append(f"Title too long ({meta['title_length']} chars, max 60)")
    elif meta["title_length"] < 30:
        result["issues"].append(f"Title too short ({meta['title_length']} chars, min 30)")

    if not meta["description"]:
        result["issues"].append("Missing meta description")
    elif meta["description_length"] > 160:
        result["issues"].append(f"Description too long ({meta['description_length']} chars, max 160)")

    if not meta["canonical"]:
        result["issues"].append("Missing canonical URL")

    if "og:image" not in meta["open_graph"]:
        result["issues"].append("Missing og:image")

    # --- Headings ---
    headings = extract_headings(html)
    result["headings"] = headings

    h1_count = sum(1 for h in headings if h["level"] == "h1")
    question_headings = sum(1 for h in headings if h["is_question"])
    total_headings = len(headings)

    result["heading_stats"] = {
        "total": total_headings,
        "h1_count": h1_count,
        "question_style_count": question_headings,
        "question_ratio": round(question_headings / total_headings, 2) if total_headings > 0 else 0,
    }

    result["checks"]["has_h1"] = h1_count > 0
    result["checks"]["single_h1"] = h1_count == 1
    result["checks"]["has_question_headings"] = question_headings > 0

    if h1_count == 0:
        result["issues"].append("No H1 heading found")
    elif h1_count > 1:
        result["issues"].append(f"Multiple H1 headings found ({h1_count})")

    if total_headings > 3 and question_headings == 0:
        result["issues"].append("No question-style headings (H2/H3) — hurts GEO visibility")

    # --- SSR check ---
    html_size = len(html.encode("utf-8"))
    result["checks"]["html_size_bytes"] = html_size
    result["checks"]["ssr_likely_ok"] = html_size > 10000  # >10KB likely has real content

    if html_size < 500:
        result["issues"].append(f"HTML extremely small ({html_size} bytes) — possible empty shell / CSR-only")

    # --- Redirect check ---
    if result["redirect_chain"]:
        result["issues"].append(
            f"Redirect detected: {' → '.join(r['url'] for r in result['redirect_chain'])} → {url}"
        )

    return result


def audit_sitemap(base_url: str) -> dict:
    """Check sitemap.xml presence and structure."""
    sitemap_url = urljoin(base_url, "/sitemap.xml")
    result = {
        "url": sitemap_url,
        "exists": False,
        "page_count": 0,
        "has_lastmod": False,
        "declared_in_robots": False,
        "pages": [],
    }

    resp = safe_fetch(sitemap_url)
    if resp and resp.status_code == 200:
        result["exists"] = True
        urls = extract_sitemap_urls(sitemap_url)
        result["page_count"] = len(urls)
        result["pages"] = urls
        result["has_lastmod"] = "<lastmod>" in resp.text.lower()

    # Check robots.txt for sitemap declaration
    robots_resp = safe_fetch(urljoin(base_url, "/robots.txt"))
    if robots_resp and robots_resp.status_code == 200:
        result["declared_in_robots"] = "sitemap:" in robots_resp.text.lower()

    return result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="SEO audit tool for website pages")
    parser.add_argument("--url", default=os.environ.get("SITE_URL"),
                        help="Base URL of the site (or set SITE_URL env)")
    parser.add_argument("--sitemap", action="store_true",
                        help="Audit all pages from sitemap.xml")
    parser.add_argument("--pages", help="Comma-separated page paths to audit (e.g. /about,/pricing)")
    parser.add_argument("--max-pages", type=int, default=50,
                        help="Max pages to audit from sitemap (default: 50)")
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")

    args = parser.parse_args()

    if not args.url:
        print("Error: --url required or set SITE_URL", file=sys.stderr)
        sys.exit(1)

    base_url = args.url.rstrip("/")
    if not base_url.startswith("http"):
        base_url = f"https://{base_url}"

    # Determine pages to audit
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
            print("Warning: No URLs found in sitemap, falling back to homepage", file=sys.stderr)
            page_urls = [f"{base_url}/"]
        else:
            print(f"Found {len(page_urls)} pages in sitemap", file=sys.stderr)
            if len(page_urls) > args.max_pages:
                print(f"Limiting to first {args.max_pages} pages", file=sys.stderr)
                page_urls = page_urls[:args.max_pages]
    else:
        page_urls = [f"{base_url}/"]

    # Run audits
    print(f"Auditing {len(page_urls)} page(s)...", file=sys.stderr)

    page_results = []
    for i, url in enumerate(page_urls, 1):
        print(f"  [{i}/{len(page_urls)}] {url}", file=sys.stderr)
        page_results.append(audit_page(url))
        if i < len(page_urls):
            time.sleep(0.5)  # polite delay

    # Sitemap audit
    sitemap_result = audit_sitemap(base_url)

    # Aggregate summary
    all_issues = []
    all_checks = {}
    for pr in page_results:
        for issue in pr["issues"]:
            all_issues.append({"url": pr["url"], "issue": issue})
        for issue in pr["json_ld"].get("issues", []):
            all_issues.append({"url": pr["url"], "issue": f"[JSON-LD] {issue}"})

    # Aggregate pass/fail counts
    check_keys = set()
    for pr in page_results:
        check_keys.update(pr["checks"].keys())
    for key in sorted(check_keys):
        if key == "html_size_bytes":
            continue
        values = [pr["checks"].get(key) for pr in page_results if key in pr["checks"]]
        passed = sum(1 for v in values if v)
        all_checks[key] = {"passed": passed, "total": len(values)}

    result = {
        "tool": "seo_audit",
        "base_url": base_url,
        "pages_audited": len(page_results),
        "summary": {
            "total_issues": len(all_issues),
            "checks": all_checks,
        },
        "sitemap": sitemap_result,
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

    # Print quick summary to stderr
    print(f"\n{'='*60}", file=sys.stderr)
    print(f"SEO Audit Summary: {base_url}", file=sys.stderr)
    print(f"Pages audited: {len(page_results)}", file=sys.stderr)
    print(f"Total issues: {len(all_issues)}", file=sys.stderr)
    if sitemap_result["exists"]:
        print(f"Sitemap: ✅ {sitemap_result['page_count']} pages", file=sys.stderr)
    else:
        print(f"Sitemap: ❌ Not found", file=sys.stderr)
    print(f"{'='*60}", file=sys.stderr)


if __name__ == "__main__":
    main()
