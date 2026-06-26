#!/usr/bin/env python3
from __future__ import annotations

"""GEO (Generative Engine Optimization) audit tool.

Checks AI-readability signals: llms.txt, robots.txt AI crawler rules,
content depth, question-style headings, HowTo schema, and more.

Usage:
    # Full GEO audit on a single page
    python geo_audit.py --url "https://example.com/"

    # Audit multiple pages
    python geo_audit.py --url "https://example.com/" --pages "/about,/pricing,/docs"

    # Audit all pages from sitemap
    python geo_audit.py --url "https://example.com/" --sitemap

    # Output to file
    python geo_audit.py --url "https://example.com/" -o geo_report.json

Reads .env from: .skills-data/google-analytics-and-search-improve/.env
Env var: SITE_URL (fallback if --url not provided)
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from urllib.parse import urljoin

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
    "Mozilla/5.0 (compatible; GEOAuditBot/1.0; +https://github.com/skills/geo-audit)"
)
REQUEST_TIMEOUT = 15

# Known AI crawlers and their User-Agent strings
AI_CRAWLERS = [
    "GPTBot",
    "ClaudeBot",
    "PerplexityBot",
    "Google-Extended",
    "Amazonbot",
    "anthropic-ai",
    "Bytespider",
    "CCBot",
    "cohere-ai",
]


def fetch(url: str) -> requests.Response:
    return requests.get(
        url,
        headers={"User-Agent": USER_AGENT, "Accept-Encoding": "gzip, br"},
        timeout=REQUEST_TIMEOUT,
        allow_redirects=True,
    )


def safe_fetch(url: str) -> requests.Response | None:
    try:
        return fetch(url)
    except Exception as exc:
        print(f"  ⚠️  Failed to fetch {url}: {exc}", file=sys.stderr)
        return None


def extract_sitemap_urls(sitemap_url: str) -> list[str]:
    resp = safe_fetch(sitemap_url)
    if not resp or resp.status_code != 200:
        return []
    content = resp.text
    urls = []
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
# llms.txt audit
# ---------------------------------------------------------------------------

def audit_llms_txt(base_url: str) -> dict:
    """Check presence and quality of llms.txt and llms-full.txt."""
    result = {
        "llms_txt": {"exists": False, "url": f"{base_url}/llms.txt", "lines": 0, "preview": ""},
        "llms_full_txt": {"exists": False, "url": f"{base_url}/llms-full.txt", "lines": 0, "preview": ""},
        "robots_txt_reference": False,
        "issues": [],
        "checks": {},
    }

    # llms.txt
    resp = safe_fetch(f"{base_url}/llms.txt")
    if resp and resp.status_code == 200 and len(resp.text.strip()) > 10:
        result["llms_txt"]["exists"] = True
        result["llms_txt"]["lines"] = len(resp.text.strip().splitlines())
        result["llms_txt"]["preview"] = "\n".join(resp.text.strip().splitlines()[:10])
    else:
        result["issues"].append("Missing /llms.txt — critical for AI engine discovery (P0)")

    # llms-full.txt
    resp = safe_fetch(f"{base_url}/llms-full.txt")
    if resp and resp.status_code == 200 and len(resp.text.strip()) > 10:
        result["llms_full_txt"]["exists"] = True
        result["llms_full_txt"]["lines"] = len(resp.text.strip().splitlines())
        result["llms_full_txt"]["preview"] = "\n".join(resp.text.strip().splitlines()[:10])
    else:
        result["issues"].append("Missing /llms-full.txt — recommended for comprehensive AI indexing")

    # Check robots.txt for llms.txt reference
    robots_resp = safe_fetch(f"{base_url}/robots.txt")
    if robots_resp and robots_resp.status_code == 200:
        if "llms" in robots_resp.text.lower():
            result["robots_txt_reference"] = True
        else:
            result["issues"].append("robots.txt does not reference llms.txt (add: Llms-txt: URL)")

    result["checks"]["has_llms_txt"] = result["llms_txt"]["exists"]
    result["checks"]["has_llms_full_txt"] = result["llms_full_txt"]["exists"]
    result["checks"]["robots_references_llms"] = result["robots_txt_reference"]

    return result


# ---------------------------------------------------------------------------
# robots.txt AI crawler audit
# ---------------------------------------------------------------------------

def audit_robots_ai_crawlers(base_url: str) -> dict:
    """Analyze robots.txt for AI crawler directives."""
    result = {
        "url": f"{base_url}/robots.txt",
        "exists": False,
        "content": "",
        "crawlers": {},
        "issues": [],
        "checks": {},
    }

    resp = safe_fetch(f"{base_url}/robots.txt")
    if not resp or resp.status_code != 200:
        result["issues"].append("robots.txt not found")
        return result

    result["exists"] = True
    content = resp.text
    result["content"] = content

    # Parse robots.txt for AI crawler rules
    lines = content.splitlines()
    current_agent = None
    agent_rules = {}

    for line in lines:
        line = line.strip()
        if line.startswith("#") or not line:
            continue
        if line.lower().startswith("user-agent:"):
            current_agent = line.split(":", 1)[1].strip()
            if current_agent not in agent_rules:
                agent_rules[current_agent] = []
        elif current_agent and (line.lower().startswith("allow:") or line.lower().startswith("disallow:")):
            agent_rules[current_agent] = agent_rules.get(current_agent, [])
            agent_rules[current_agent].append(line)

    # Check each known AI crawler
    for crawler in AI_CRAWLERS:
        status = "not_mentioned"
        if crawler in agent_rules:
            rules = agent_rules[crawler]
            has_allow = any("allow:" in r.lower() and "disallow:" not in r.lower() for r in rules)
            has_disallow = any("disallow:" in r.lower() for r in rules)
            if has_disallow and not has_allow:
                status = "blocked"
            elif has_allow:
                status = "allowed"
            else:
                status = "configured"
        elif "*" in agent_rules:
            # Falls under wildcard
            rules = agent_rules["*"]
            has_disallow_all = any("disallow: /" == r.lower().strip() for r in rules)
            if has_disallow_all:
                status = "blocked_by_wildcard"
            else:
                status = "allowed_by_wildcard"
        else:
            status = "allowed_by_default"

        result["crawlers"][crawler] = status

    # Generate issues
    blocked = [c for c, s in result["crawlers"].items() if "blocked" in s]
    not_mentioned = [c for c, s in result["crawlers"].items() if s in ("not_mentioned", "allowed_by_default", "allowed_by_wildcard")]

    if blocked:
        result["issues"].append(f"AI crawlers BLOCKED: {', '.join(blocked)}")
    if not_mentioned:
        result["issues"].append(
            f"AI crawlers not explicitly configured (recommended to add Allow rules): {', '.join(not_mentioned)}"
        )

    result["checks"]["no_ai_crawlers_blocked"] = len(blocked) == 0
    result["checks"]["ai_crawlers_explicitly_allowed"] = len(not_mentioned) == 0

    return result


# ---------------------------------------------------------------------------
# Content depth audit
# ---------------------------------------------------------------------------

def audit_content_depth(url: str, html: str) -> dict:
    """Analyze page content depth: word count, structure, intro summary, FAQ."""
    result = {
        "url": url,
        "word_count": 0,
        "has_intro_summary": False,
        "has_faq_section": False,
        "has_howto_content": False,
        "heading_count": 0,
        "question_headings": 0,
        "question_heading_ratio": 0,
        "content_sections": [],
        "issues": [],
        "checks": {},
    }

    # Strip scripts and styles
    clean = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    clean = re.sub(r'<style[^>]*>.*?</style>', '', clean, flags=re.DOTALL | re.IGNORECASE)
    # Remove nav, header, footer for main content estimation
    clean_main = re.sub(r'<(nav|header|footer)[^>]*>.*?</\1>', '', clean, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<[^>]+>', ' ', clean_main)
    text = re.sub(r'\s+', ' ', text).strip()

    cjk_chars = sum(1 for ch in text if '\u4e00' <= ch <= '\u9fff'
                    or '\u3400' <= ch <= '\u4dbf'
                    or '\U00020000' <= ch <= '\U0002a6df')
    non_cjk_text = re.sub(r'[\u4e00-\u9fff\u3400-\u4dbf]', ' ', text)
    en_words = len(non_cjk_text.split())

    is_cjk_dominant = cjk_chars > en_words
    result["cjk_chars"] = cjk_chars
    result["en_words"] = en_words
    result["is_cjk_dominant"] = is_cjk_dominant
    result["word_count"] = cjk_chars if is_cjk_dominant else en_words

    # Check for intro summary: a meaningful text block before the first <h2>.
    # Language-agnostic — checks length, not specific keywords.
    intro_text = ""
    h1_match = re.search(r'</h1>', clean_main, re.IGNORECASE)
    h2_match = re.search(r'<h2[\s>]', clean_main, re.IGNORECASE)
    if h1_match:
        start = h1_match.end()
        end = h2_match.start() if h2_match and h2_match.start() > start else start + 3000
        intro_html = clean_main[start:end]
        intro_text = re.sub(r'<[^>]+>', ' ', intro_html)
        intro_text = re.sub(r'\s+', ' ', intro_text).strip()

    if is_cjk_dominant:
        intro_len = sum(1 for ch in intro_text if '\u4e00' <= ch <= '\u9fff'
                        or '\u3400' <= ch <= '\u4dbf')
        result["has_intro_summary"] = intro_len >= 50
    else:
        result["has_intro_summary"] = len(intro_text.split()) >= 30

    # Check for FAQ section
    faq_signals = ["faq", "frequently asked", "common questions", "q&a",
                    "常见问题", "问答", "疑问解答"]
    html_lower = html.lower()
    result["has_faq_section"] = any(s in html_lower for s in faq_signals)

    # Check for HowTo content
    howto_signals = ["step 1", "step 2", "how to", "getting started", "tutorial",
                     "第一步", "第二步", "步骤", "教程", "使用方法", "操作指南"]
    result["has_howto_content"] = any(s in html_lower for s in howto_signals)

    # Heading analysis
    headings = re.findall(r'<(h[1-6])[^>]*>(.*?)</\1>', html, re.IGNORECASE | re.DOTALL)
    result["heading_count"] = len(headings)

    question_count = 0
    for _, heading_text in headings:
        cleaned = re.sub(r'<[^>]+>', '', heading_text).strip()
        if cleaned.rstrip().endswith("?") or cleaned.rstrip().endswith("？"):
            question_count += 1

    result["question_headings"] = question_count
    result["question_heading_ratio"] = (
        round(question_count / len(headings), 2) if headings else 0
    )

    # Check JSON-LD for FAQPage and HowTo
    faq_schema = '"FAQPage"' in html or "'FAQPage'" in html
    howto_schema = '"HowTo"' in html or "'HowTo'" in html
    result["checks"]["has_faq_schema"] = faq_schema
    result["checks"]["has_howto_schema"] = howto_schema

    # Issues — thresholds differ by dominant language
    if is_cjk_dominant:
        min_thin, min_target = 600, 1600
        unit = "CJK chars"
        target_label = "1600-2400 CJK chars"
    else:
        min_thin, min_target = 300, 800
        unit = "words"
        target_label = "800-1200 words"

    result["checks"]["word_count_sufficient"] = result["word_count"] >= min_target
    result["checks"]["has_intro_summary"] = result["has_intro_summary"]
    result["checks"]["has_faq_section"] = result["has_faq_section"]
    result["checks"]["has_question_headings"] = question_count > 0

    if result["word_count"] < min_thin:
        result["issues"].append(f"Very thin content ({result['word_count']} {unit}) — target {target_label}")
    elif result["word_count"] < min_target:
        result["issues"].append(f"Below content depth target ({result['word_count']} {unit}) — target {target_label}")

    if not result["has_intro_summary"]:
        result["issues"].append("No intro summary paragraph detected between H1 and first H2")

    if not result["has_faq_section"]:
        result["issues"].append("No FAQ section detected — adding FAQ improves GEO citations")

    if len(headings) > 3 and question_count == 0:
        result["issues"].append("No question-style headings found — AI engines prefer question format H2/H3")

    if result["has_faq_section"] and not faq_schema:
        result["issues"].append("FAQ content found but no FAQPage schema — add JSON-LD")

    if result["has_howto_content"] and not howto_schema:
        result["issues"].append("HowTo content found but no HowTo schema — add JSON-LD")

    return result


# ---------------------------------------------------------------------------
# Full page GEO audit
# ---------------------------------------------------------------------------

def audit_page_geo(url: str) -> dict:
    """Run GEO-focused audit on a single page."""
    resp = safe_fetch(url)
    if not resp or resp.status_code != 200:
        return {
            "url": url,
            "status": resp.status_code if resp else "error",
            "issues": [f"Failed to fetch page (status: {resp.status_code if resp else 'network error'})"],
            "checks": {},
        }

    html = resp.text
    content_result = audit_content_depth(url, html)
    return content_result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="GEO (Generative Engine Optimization) audit tool")
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

    # --- Site-level GEO checks ---
    print("Checking llms.txt...", file=sys.stderr)
    llms_result = audit_llms_txt(base_url)

    print("Checking robots.txt AI crawlers...", file=sys.stderr)
    robots_result = audit_robots_ai_crawlers(base_url)

    # --- Page-level content depth checks ---
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

    print(f"Auditing content depth on {len(page_urls)} page(s)...", file=sys.stderr)
    page_results = []
    for i, url in enumerate(page_urls, 1):
        print(f"  [{i}/{len(page_urls)}] {url}", file=sys.stderr)
        page_results.append(audit_page_geo(url))
        if i < len(page_urls):
            time.sleep(0.5)

    # --- Aggregate ---
    all_issues = []
    for issue in llms_result["issues"]:
        all_issues.append({"source": "llms.txt", "issue": issue})
    for issue in robots_result["issues"]:
        all_issues.append({"source": "robots.txt", "issue": issue})
    for pr in page_results:
        for issue in pr.get("issues", []):
            all_issues.append({"source": pr["url"], "issue": issue})

    # Aggregate checks
    site_checks = {}
    site_checks.update(llms_result["checks"])
    site_checks.update(robots_result["checks"])

    page_check_keys = set()
    for pr in page_results:
        page_check_keys.update(pr.get("checks", {}).keys())
    page_checks = {}
    for key in sorted(page_check_keys):
        values = [pr["checks"].get(key) for pr in page_results if key in pr.get("checks", {})]
        passed = sum(1 for v in values if v)
        page_checks[key] = {"passed": passed, "total": len(values)}

    result = {
        "tool": "geo_audit",
        "base_url": base_url,
        "pages_audited": len(page_results),
        "summary": {
            "total_issues": len(all_issues),
            "site_level_checks": site_checks,
            "page_level_checks": page_checks,
        },
        "llms_txt": llms_result,
        "robots_ai_crawlers": robots_result,
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
    print(f"GEO Audit Summary: {base_url}", file=sys.stderr)
    print(f"Pages audited: {len(page_results)}", file=sys.stderr)
    print(f"Total issues: {len(all_issues)}", file=sys.stderr)
    print(f"llms.txt: {'✅' if llms_result['llms_txt']['exists'] else '❌'}", file=sys.stderr)
    print(f"llms-full.txt: {'✅' if llms_result['llms_full_txt']['exists'] else '❌'}", file=sys.stderr)

    blocked = [c for c, s in robots_result["crawlers"].items() if "blocked" in s]
    if blocked:
        print(f"Blocked AI crawlers: ❌ {', '.join(blocked)}", file=sys.stderr)
    else:
        print(f"AI crawlers: ✅ None blocked", file=sys.stderr)

    if page_results:
        any_cjk = any(pr.get("is_cjk_dominant", False) for pr in page_results)
        avg_score = sum(pr.get("word_count", 0) for pr in page_results) / len(page_results)
        if any_cjk:
            print(f"Avg content depth: {avg_score:.0f} CJK chars/page (target: 1600-2400)", file=sys.stderr)
        else:
            print(f"Avg content depth: {avg_score:.0f} words/page (target: 800-1200)", file=sys.stderr)
    print(f"{'='*60}", file=sys.stderr)


if __name__ == "__main__":
    main()
