#!/usr/bin/env python3
"""
verify_claim.py — Multi-source cross-validation for factual claims
Part of openclaw-free-web-search skill v4.0

# SECURITY MANIFEST
# external_endpoints:
#   - local SearXNG (default: http://127.0.0.1:18080)
#   - public SearXNG fallback instances (read-only search)
#   - target URLs found in search results (read-only fetch)
# data_stored: none
# data_sent_to_llm: none
# pii_handling: no PII collected or transmitted
# network_access: outbound HTTP only (no listening ports)

Usage:
    python3 verify_claim.py --claim "Claude 3.7 was released on Feb 24 2025"
    python3 verify_claim.py --claim "..." --sources 7 --searxng-url http://127.0.0.1:18080
    python3 verify_claim.py --claim "..." --json   # machine-readable output
"""

import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from typing import Optional

# ─── Scrapling import (graceful fallback) ────────────────────────────────────
SCRAPLING_AVAILABLE = False
STEALTHY_AVAILABLE = False
try:
    from scrapling.fetchers import Fetcher as ScraplingFetcher
    SCRAPLING_AVAILABLE = True
    try:
        from scrapling.fetchers import StealthyFetcher
        STEALTHY_AVAILABLE = True
    except ImportError:
        pass
except ImportError:
    pass

# ─── Constants ────────────────────────────────────────────────────────────────
DEFAULT_SEARXNG = "http://127.0.0.1:18080"
PUBLIC_SEARXNG_INSTANCES = [
    "https://search.mdosch.de",
    "https://paulgo.io",
    "https://opnxng.com",
    "https://searx.tiekoetter.com",
]

BROWSER_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36"
)

# Domain authority tiers (higher = more authoritative)
HIGH_AUTHORITY_DOMAINS = {
    "wikipedia.org", "britannica.com",
    "reuters.com", "apnews.com", "bbc.com", "bbc.co.uk",
    "theguardian.com", "nytimes.com", "washingtonpost.com",
    "techcrunch.com", "theverge.com", "wired.com", "arstechnica.com",
    "nature.com", "science.org", "pubmed.ncbi.nlm.nih.gov",
    "anthropic.com", "openai.com", "google.com", "microsoft.com",
    "github.com", "stackoverflow.com",
    "gov", "edu",  # TLD suffixes
}
MEDIUM_AUTHORITY_DOMAINS = {
    "medium.com", "substack.com", "dev.to", "hackernews.com",
    "reddit.com", "quora.com", "linkedin.com",
    "zdnet.com", "cnet.com", "engadget.com", "venturebeat.com",
    "towardsdatascience.com", "analyticsvidhya.com",
}

VERDICT_LEVELS = [
    (0.75, "VERIFIED",      "✅"),
    (0.55, "LIKELY_TRUE",   "🟢"),
    (0.35, "UNCERTAIN",     "🟡"),
    (0.15, "LIKELY_FALSE",  "🔴"),
    (0.00, "UNVERIFIABLE",  "⬜"),
]

# ─── Utility helpers ──────────────────────────────────────────────────────────

def _domain_from_url(url: str) -> str:
    try:
        return urllib.parse.urlparse(url).netloc.lower().lstrip("www.")
    except Exception:
        return ""


def _domain_authority(domain: str) -> tuple[str, float]:
    """Return (tier_label, score 0-1)."""
    if not domain:
        return "LOW", 0.2
    # Check TLD suffixes
    for suffix in (".gov", ".edu"):
        if domain.endswith(suffix):
            return "HIGH", 1.0
    if domain in HIGH_AUTHORITY_DOMAINS:
        return "HIGH", 1.0
    # Partial match (e.g. sub.wikipedia.org)
    for hd in HIGH_AUTHORITY_DOMAINS:
        if domain.endswith("." + hd) or domain == hd:
            return "HIGH", 1.0
    if domain in MEDIUM_AUTHORITY_DOMAINS:
        return "MEDIUM", 0.55
    for md in MEDIUM_AUTHORITY_DOMAINS:
        if domain.endswith("." + md):
            return "MEDIUM", 0.55
    return "LOW", 0.25


def _recency_score(date_str: str) -> float:
    """Score 0-1 based on how recent the source is."""
    if not date_str:
        return 0.4  # unknown → neutral
    try:
        # Try common formats
        for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%SZ",
                    "%B %d, %Y", "%b %d, %Y", "%d %B %Y"):
            try:
                dt = datetime.strptime(date_str[:len(fmt) + 4].strip(), fmt)
                break
            except ValueError:
                continue
        else:
            return 0.4
        now = datetime.now()
        days_old = (now - dt).days
        if days_old < 0:
            return 0.5
        if days_old <= 30:
            return 1.0
        if days_old <= 180:
            return 0.85
        if days_old <= 365:
            return 0.70
        if days_old <= 730:
            return 0.55
        return 0.35
    except Exception:
        return 0.4


def _extract_keywords(claim: str) -> list[str]:
    """Extract meaningful keywords from a claim for sentence matching."""
    stopwords = {
        "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "will", "would", "could",
        "should", "may", "might", "shall", "can", "need", "dare", "ought",
        "used", "to", "of", "in", "on", "at", "by", "for", "with", "about",
        "against", "between", "into", "through", "during", "before", "after",
        "above", "below", "from", "up", "down", "out", "off", "over", "under",
        "again", "further", "then", "once", "and", "but", "or", "nor", "so",
        "yet", "both", "either", "neither", "not", "only", "own", "same",
        "than", "too", "very", "just", "that", "this", "these", "those",
    }
    words = re.findall(r"\b[a-zA-Z0-9][a-zA-Z0-9\-\.]*\b", claim.lower())
    return [w for w in words if w not in stopwords and len(w) > 2]


def _classify_stance(text_lower: str, keywords: list[str], claim_lower: str) -> str:
    """
    Classify whether a text excerpt AGREES, CONTRADICTS, or is NEUTRAL
    with respect to the claim.
    """
    # Contradiction signals
    contradiction_phrases = [
        "not ", "never ", "false", "incorrect", "wrong", "debunked",
        "misleading", "inaccurate", "no evidence", "contrary to",
        "actually ", "in fact, ", "however,", "but actually",
        "correction:", "update:", "erratum",
    ]
    # Agreement signals
    agreement_phrases = [
        "confirmed", "announced", "released", "launched", "published",
        "according to", "reports that", "states that", "reveals that",
        "officially", "as of", "on ", "in ", "at ",
    ]

    keyword_hits = sum(1 for kw in keywords if kw in text_lower)
    if keyword_hits < max(1, len(keywords) // 3):
        return "NEUTRAL"

    contra_hits = sum(1 for p in contradiction_phrases if p in text_lower)
    agree_hits = sum(1 for p in agreement_phrases if p in text_lower)

    if contra_hits > agree_hits and contra_hits >= 2:
        return "CONTRADICT"
    if agree_hits >= 1 or keyword_hits >= len(keywords) // 2:
        return "AGREE"
    return "NEUTRAL"


def _extract_relevant_sentences(full_text: str, keywords: list[str], max_chars: int = 300) -> str:
    """Find the most relevant sentence(s) from a page for the claim."""
    sentences = re.split(r"(?<=[.!?])\s+", full_text)
    scored = []
    for sent in sentences:
        sl = sent.lower()
        score = sum(1 for kw in keywords if kw in sl)
        if score > 0:
            scored.append((score, sent.strip()))
    scored.sort(key=lambda x: -x[0])
    result = ""
    for _, sent in scored[:3]:
        if len(result) + len(sent) < max_chars:
            result += sent + " "
        else:
            break
    return result.strip() or "(no relevant excerpt found)"


# ─── Fetching helpers ─────────────────────────────────────────────────────────

def _fetch_with_stdlib(url: str, timeout: int = 12) -> Optional[str]:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": BROWSER_UA})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read(1024 * 200)  # max 200KB
            charset = resp.headers.get_content_charset() or "utf-8"
            return raw.decode(charset, errors="replace")
    except Exception:
        return None


def _fetch_page_text(url: str) -> tuple[str, str]:
    """
    Fetch a URL and return (plain_text, fetcher_name_used).
    Tries Scrapling first, falls back to stdlib.
    """
    # Try Scrapling Fetcher (TLS fingerprint spoofing)
    if SCRAPLING_AVAILABLE:
        try:
            page = ScraplingFetcher().get(url, timeout=15)
            if page and page.status == 200:
                text = page.get_all_text(separator=" ", ignore_tags=("script", "style", "nav", "footer"))
                if text and len(text) > 100:
                    return text, "Fetcher"
        except Exception:
            pass

    # Try StealthyFetcher (Cloudflare bypass)
    if STEALTHY_AVAILABLE:
        try:
            page = StealthyFetcher().fetch(url, headless=True, network_idle=True)
            if page and page.status == 200:
                text = page.get_all_text(separator=" ", ignore_tags=("script", "style", "nav", "footer"))
                if text and len(text) > 100:
                    return text, "StealthyFetcher"
        except Exception:
            pass

    # Stdlib fallback
    html = _fetch_with_stdlib(url)
    if html:
        # Strip HTML tags
        text = re.sub(r"<[^>]+>", " ", html)
        text = re.sub(r"\s+", " ", text).strip()
        if len(text) > 100:
            return text, "stdlib"

    return "", "failed"


# ─── Search helpers ───────────────────────────────────────────────────────────

def _search_searxng(query: str, searxng_url: str, num: int = 5) -> list[dict]:
    """Query SearXNG and return list of {url, title, snippet, publishedDate}."""
    params = urllib.parse.urlencode({
        "q": query,
        "format": "json",
        "language": "en",
        "time_range": "",
        "safesearch": "0",
        "categories": "general",
    })
    full_url = f"{searxng_url}/search?{params}"
    try:
        req = urllib.request.Request(full_url, headers={"User-Agent": BROWSER_UA})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            results = data.get("results", [])[:num]
            return [
                {
                    "url": r.get("url", ""),
                    "title": (r.get("title") or "").strip(),
                    "snippet": (r.get("content") or "").strip(),
                    "publishedDate": (r.get("publishedDate") or "").strip(),
                }
                for r in results if r.get("url")
            ]
    except Exception:
        return []


def _find_working_searxng(searxng_url: str) -> str:
    """Try local first, then public fallbacks. Return working URL."""
    for url in [searxng_url] + PUBLIC_SEARXNG_INSTANCES:
        try:
            req = urllib.request.Request(
                f"{url}/search?q=test&format=json",
                headers={"User-Agent": BROWSER_UA}
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                if resp.status == 200:
                    return url
        except Exception:
            continue
    return ""


def _expand_queries(claim: str) -> list[str]:
    """Generate 3 search query variants from a claim."""
    q1 = claim
    # Variant 2: add "fact check"
    q2 = f'fact check: {claim}'
    # Variant 3: extract key noun phrase (first 8 words)
    words = claim.split()
    q3 = " ".join(words[:8]) + (" site:wikipedia.org OR site:reuters.com OR site:bbc.com" if len(words) > 4 else "")
    return [q1, q2, q3]


# ─── Core verification logic ──────────────────────────────────────────────────

def _analyze_source(item: dict, keywords: list[str], claim_lower: str) -> dict:
    """Fetch and analyze a single source. Returns evidence dict."""
    url = item["url"]
    domain = _domain_from_url(url)
    authority_label, authority_score = _domain_authority(domain)
    recency = _recency_score(item.get("publishedDate", ""))

    # Use snippet first (fast, no network)
    snippet = item.get("snippet", "")
    snippet_stance = _classify_stance(snippet.lower(), keywords, claim_lower)

    # Only fetch full page if snippet is NEUTRAL or insufficient
    fetcher_used = "snippet_only"
    excerpt = snippet[:300] if snippet else ""
    full_text = ""

    if snippet_stance == "NEUTRAL" or len(snippet) < 80:
        full_text, fetcher_used = _fetch_page_text(url)
        if full_text:
            excerpt = _extract_relevant_sentences(full_text, keywords)
            stance = _classify_stance(full_text.lower(), keywords, claim_lower)
        else:
            stance = snippet_stance
    else:
        stance = snippet_stance

    # Partial score (cross_agreement added later)
    partial_score = (
        authority_score * 0.30 +
        (1.0 if stance == "AGREE" else 0.0 if stance == "NEUTRAL" else -0.5) * 0.35 +
        recency * 0.20
    )

    return {
        "url": url,
        "domain": domain,
        "authority": authority_label,
        "authority_score": round(authority_score, 2),
        "stance": stance,
        "excerpt": excerpt[:300],
        "published_date": item.get("publishedDate", ""),
        "recency_score": round(recency, 2),
        "partial_score": round(partial_score, 3),
        "fetcher_used": fetcher_used,
    }


def verify_claim(
    claim: str,
    num_sources: int = 5,
    searxng_url: str = DEFAULT_SEARXNG,
    direct_urls: Optional[list] = None,
) -> dict:
    """
    Main entry point. Returns a structured verification result dict.
    If direct_urls is provided, skip SearXNG search and verify those URLs directly.
    """
    print(f"\n🔍 Verifying: \"{claim}\"", file=sys.stderr)
    print(f"   Sources target: {num_sources}", file=sys.stderr)

    all_results: list[dict] = []

    # ── Mode A: Direct URL list (no SearXNG needed) ──
    if direct_urls:
        print(f"   Mode: Direct URL verification ({len(direct_urls)} URLs)", file=sys.stderr)
        for url in direct_urls[:num_sources]:
            all_results.append({"url": url, "title": "", "snippet": "", "publishedDate": ""})
    else:
        # ── Mode B: SearXNG search ──
        print("   Finding SearXNG instance...", file=sys.stderr)
        working_searxng = _find_working_searxng(searxng_url)
        if not working_searxng:
            print("   ⚠️  No SearXNG instance available.", file=sys.stderr)
            print("   💡 Tip: Start local SearXNG with ./start_local_search.sh", file=sys.stderr)
            print("   💡 Or pass known URLs directly: --urls url1 url2 ...", file=sys.stderr)
            return {
                "claim": claim,
                "verdict": "UNVERIFIABLE",
                "confidence": 0.0,
                "error": "No SearXNG instance available. Start local SearXNG or use --urls to provide sources directly.",
                "sources_checked": 0,
            }
        print(f"   Using: {working_searxng}", file=sys.stderr)

        queries = _expand_queries(claim)
        per_query = max(2, num_sources // len(queries) + 1)
        seen_urls: set[str] = set()

        for q in queries:
            results = _search_searxng(q, working_searxng, num=per_query)
            for r in results:
                if r["url"] not in seen_urls:
                    seen_urls.add(r["url"])
                    all_results.append(r)

        all_results = all_results[:num_sources]

    print(f"   Collected {len(all_results)} unique sources to analyze...", file=sys.stderr)

    if not all_results:
        return {
            "claim": claim,
            "verdict": "UNVERIFIABLE",
            "confidence": 0.0,
            "error": "No search results found for this claim.",
            "sources_checked": 0,
        }

    # 3. Analyze sources in parallel
    keywords = _extract_keywords(claim)
    claim_lower = claim.lower()
    evidence = []

    with ThreadPoolExecutor(max_workers=min(5, len(all_results))) as pool:
        futures = {pool.submit(_analyze_source, item, keywords, claim_lower): item for item in all_results}
        for i, future in enumerate(as_completed(futures), 1):
            try:
                result = future.result(timeout=30)
                evidence.append(result)
                stance_icon = {"AGREE": "✅", "CONTRADICT": "❌", "NEUTRAL": "➖"}.get(result["stance"], "?")
                print(f"   [{i}/{len(all_results)}] {stance_icon} {result['domain']} ({result['authority']})", file=sys.stderr)
            except Exception as e:
                print(f"   [{i}/{len(all_results)}] ⚠️  source failed: {e}", file=sys.stderr)

    if not evidence:
        return {
            "claim": claim,
            "verdict": "UNVERIFIABLE",
            "confidence": 0.0,
            "error": "All source fetches failed.",
            "sources_checked": 0,
        }

    # 4. Compute cross_agreement weight
    stances = [e["stance"] for e in evidence]
    agree_count = stances.count("AGREE")
    contra_count = stances.count("CONTRADICT")
    neutral_count = stances.count("NEUTRAL")
    total = len(evidence)

    for e in evidence:
        if e["stance"] == "AGREE":
            cross_score = agree_count / total
        elif e["stance"] == "CONTRADICT":
            cross_score = contra_count / total
        else:
            cross_score = 0.5
        e["score"] = round(
            e["partial_score"] + cross_score * 0.15,
            3
        )

    # 5. Compute final confidence
    # Weight by authority: HIGH sources count 3x, MEDIUM 2x, LOW 1x
    authority_weights = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}
    weighted_agree = sum(
        authority_weights.get(e["authority"], 1)
        for e in evidence if e["stance"] == "AGREE"
    )
    weighted_contra = sum(
        authority_weights.get(e["authority"], 1)
        for e in evidence if e["stance"] == "CONTRADICT"
    )
    weighted_total = sum(authority_weights.get(e["authority"], 1) for e in evidence)

    if weighted_total == 0:
        confidence = 0.0
    else:
        raw_confidence = weighted_agree / weighted_total
        # Penalize if contradictions exist
        if weighted_contra > 0:
            penalty = min(0.3, weighted_contra / weighted_total * 0.5)
            raw_confidence = max(0.0, raw_confidence - penalty)
        confidence = round(raw_confidence, 3)

    # 6. Determine verdict
    verdict = "UNVERIFIABLE"
    verdict_icon = "⬜"
    for threshold, label, icon in VERDICT_LEVELS:
        if confidence >= threshold:
            verdict = label
            verdict_icon = icon
            break

    # 7. Build summary
    summary_parts = []
    if agree_count > 0:
        summary_parts.append(f"{agree_count} source(s) support the claim")
    if contra_count > 0:
        summary_parts.append(f"{contra_count} source(s) contradict it")
    if neutral_count > 0:
        summary_parts.append(f"{neutral_count} source(s) are neutral")
    high_auth_agree = [e for e in evidence if e["stance"] == "AGREE" and e["authority"] == "HIGH"]
    if high_auth_agree:
        summary_parts.append(f"including {len(high_auth_agree)} high-authority source(s)")
    summary = ". ".join(summary_parts) + "." if summary_parts else "Insufficient evidence."

    # Sort evidence by score descending
    evidence.sort(key=lambda x: -x.get("score", 0))

    return {
        "claim": claim,
        "verdict": verdict,
        "verdict_icon": verdict_icon,
        "confidence": confidence,
        "sources_checked": total,
        "sources_agreeing": agree_count,
        "sources_contradicting": contra_count,
        "sources_neutral": neutral_count,
        "summary": summary,
        "evidence": evidence,
        "searxng_used": working_searxng if not direct_urls else "direct-url-mode",
        "scrapling_mode": (
            "FULL (Scrapling + StealthyFetcher)" if STEALTHY_AVAILABLE else
            "PARTIAL (Scrapling Fetcher only)" if SCRAPLING_AVAILABLE else
            "DEGRADED (stdlib urllib only)"
        ),
    }


# ─── CLI ──────────────────────────────────────────────────────────────────────

def _print_human_readable(result: dict) -> None:
    print("\n" + "=" * 60)
    print(f"  CLAIM  : {result['claim']}")
    print(f"  VERDICT: {result.get('verdict_icon', '')} {result['verdict']}")
    print(f"  CONFIDENCE: {result['confidence']:.0%}")
    print(f"  SOURCES: {result['sources_checked']} checked  "
          f"({result.get('sources_agreeing', 0)} agree / "
          f"{result.get('sources_contradicting', 0)} contradict / "
          f"{result.get('sources_neutral', 0)} neutral)")
    print(f"  SUMMARY: {result.get('summary', '')}")
    print(f"  MODE   : {result.get('scrapling_mode', 'unknown')}")
    print("-" * 60)

    for i, ev in enumerate(result.get("evidence", []), 1):
        stance_icon = {"AGREE": "✅", "CONTRADICT": "❌", "NEUTRAL": "➖"}.get(ev["stance"], "?")
        print(f"\n  [{i}] {stance_icon} {ev['domain']}  [{ev['authority']}]  score={ev.get('score', 0):.2f}")
        print(f"       {ev['url'][:80]}")
        if ev.get("published_date"):
            print(f"       Published: {ev['published_date']}")
        if ev.get("excerpt"):
            print(f"       Excerpt: \"{ev['excerpt'][:200]}\"")

    print("=" * 60 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Verify a factual claim using multi-source cross-validation"
    )
    parser.add_argument("--claim", required=True, help="The factual claim to verify")
    parser.add_argument("--sources", type=int, default=5,
                        help="Number of sources to check (default: 5, max recommended: 10)")
    parser.add_argument("--searxng-url", default=DEFAULT_SEARXNG,
                        help=f"SearXNG base URL (default: {DEFAULT_SEARXNG})")
    parser.add_argument("--urls", nargs="+", default=None,
                        help="Skip SearXNG search and verify these URLs directly (space-separated)")
    parser.add_argument("--json", action="store_true",
                        help="Output raw JSON (machine-readable)")
    args = parser.parse_args()

    if not SCRAPLING_AVAILABLE:
        print(
            "\n⚠️  WARNING: Scrapling not installed. Running in DEGRADED mode.\n"
            "   Install with: pip install scrapling[all] && python -m playwright install chromium\n",
            file=sys.stderr
        )

    result = verify_claim(
        claim=args.claim,
        num_sources=args.sources,
        searxng_url=args.searxng_url,
        direct_urls=args.urls,
    )

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        _print_human_readable(result)


if __name__ == "__main__":
    main()
