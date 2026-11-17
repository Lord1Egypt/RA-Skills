#!/usr/bin/env python3
"""
scihub.py — Sci-Hub mirror connector for ocas-reach.

Resolves DOIs, titles, and keywords to academic paper PDFs via Sci-Hub mirrors.
Uses DNS-over-HTTPS fallback for ISP-blocked domains. Auto-rotates through mirrors
with per-mirror caching and temporary failure tracking.

Mirror list maintained from:
  - Debvex/Sci-Hub-MCP-Server (primary source)
  - https://www.sci-hub.pub/ (mirror directory)
  - https://sci-bot.ru/ (CITE_READER_URL)

Debounced mirror failures: 5-minute cooldown per mirror before retry.
"""

import json
import os
import re
import socket
import time
import logging
import urllib3
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger("ocas-reach.scihub")
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ── Mirror Registry ──────────────────────────────────────────────────────────
# Ordered by priority. First working mirror is used and cached.
MIRRORS = [
    "sci-hub.st",
    "sci-hub.su",
    "sci-hub.red",
    "sci-hub.ren",
    "sci-hub.ru",
    "sci-hub.box",
    "www.sci-hub.pub",
    "sci-hub.al",
    "sci-hub.mk",
    "sci-hub.ee",
]

# ── DNS-over-HTTPS Fallback ──────────────────────────────────────────────────
# Resolves domains via public DoH when ISP blocks Sci-Hub DNS.
_dns_cache: Dict[str, str] = {}
_dns_failure_until: Dict[str, float] = {}  # hostname → epoch cooldown

DOH_PROVIDERS = [
    "https://dns.google/resolve?name={host}&type=A",
    "https://cloudflare-dns.com/dns-query?name={host}&type=A",
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
]

_session_mirror: Optional[str] = None
_failure_cooldown = 300  # 5 minutes


def _pick_user_agent() -> str:
    import random
    return random.choice(USER_AGENTS)


def resolve_domain(hostname: str) -> str:
    """Resolve hostname with DoH fallback for ISP-blocked domains."""
    if hostname in _dns_cache:
        return _dns_cache[hostname]

    now = time.time()
    if hostname in _dns_failure_until and now < _dns_failure_until[hostname]:
        raise ConnectionError(f"DNS cooldown active for {hostname}")

    # Try normal DNS first
    try:
        addr = socket.getaddrinfo(hostname, 443, family=socket.AF_INET)[0][4][0]
        _dns_cache[hostname] = addr
        return addr
    except socket.gaierror:
        pass

    # Fall back to DNS-over-HTTPS
    for provider in DOH_PROVIDERS:
        try:
            url = provider.format(host=hostname)
            headers = {"Accept": "application/dns-json"}
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read())
                answers = data.get("Answer", [])
                for answer in answers:
                    if answer.get("type") == 1:  # A record
                        addr = answer["data"]
                        _dns_cache[hostname] = addr
                        logger.info(f"DoH resolved {hostname} → {addr}")
                        return addr
        except Exception as e:
            logger.debug(f"DoH provider failed for {hostname}: {e}")
            continue

    _dns_failure_until[hostname] = now + 60
    raise ConnectionError(f"Cannot resolve {hostname} via DNS or DoH")


def _get_working_mirror() -> str:
    """Return the first working mirror, with session-level caching."""
    global _session_mirror
    if _session_mirror:
        return _session_mirror

    now = time.time()
    for mirror in MIRRORS:
        if mirror in _dns_failure_until and now < _dns_failure_until[mirror]:
            continue
        try:
            resolve_domain(mirror)
            _session_mirror = mirror
            logger.info(f"Using Sci-Hub mirror: {mirror}")
            return mirror
        except ConnectionError:
            _dns_failure_until[mirror] = now + _failure_cooldown
            logger.warning(f"Mirror {mirror} unreachable, trying next")
            continue

    raise ConnectionError("All Sci-Hub mirrors are unreachable")


def _mark_mirror_failed(mirror: str):
    """Temporarily blacklist a mirror."""
    global _session_mirror
    _dns_failure_until[mirror] = time.time() + _failure_cooldown
    if _session_mirror == mirror:
        _session_mirror = None


def _fetch_url(url: str, timeout: int = 30) -> bytes:
    """Fetch a URL with proper headers and timeout."""
    headers = {
        "User-Agent": _pick_user_agent(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        import ssl
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        resp = urllib.request.urlopen(req, timeout=timeout, context=ctx)
        return resp.read()
    except Exception as e:
        raise ConnectionError(f"HTTP fetch failed for {url}: {e}")


def _extract_pdf_url_from_html(html: str, base_url: str) -> Optional[str]:
    """Extract PDF URL from Sci-Hub HTML page."""
    # Pattern 1: <meta name="citation_pdf_url" content="...">
    meta_match = re.search(
        r'<meta[^>]*name=["\']citation_pdf_url["\'][^>]*content=["\']([^"\']*)["\']',
        html,
    )
    if meta_match:
        pdf_path = meta_match.group(1)
        if pdf_path.startswith("/"):
            return f"https://{urllib.parse.urlparse(base_url).netloc}{pdf_path}"
        return pdf_path

    # Pattern 2: <iframe id="pdf" src="...">
    iframe_match = re.search(r'<iframe[^>]*id=["\']pdf["\'][^>]*src=["\']([^"\']*)["\']', html)
    if iframe_match:
        return iframe_match.group(1)

    # Pattern 3: direct embed/PDF links
    embed_match = re.search(r'(https?://[^\s"\'<>]+\.pdf)', html)
    if embed_match:
        return embed_match.group(1)

    return None


def _crossref_resolve_title(title: str) -> Optional[Dict[str, Any]]:
    """Resolve a title to DOI via CrossRef."""
    try:
        url = f"https://api.crossref.org/works?query.title={urllib.parse.quote(title)}&rows=1"
        data = json.loads(_fetch_url(url, timeout=15))
        items = data.get("message", {}).get("items", [])
        if items:
            item = items[0]
            return {
                "doi": item.get("DOI", ""),
                "title": item.get("title", [title])[0] if isinstance(item.get("title"), list) else item.get("title", title),
                "author": ", ".join(
                    f"{a.get('given', '')} {a.get('family', '')}".strip()
                    for a in item.get("author", [])
                ),
                "year": str(
                    (item.get("published-print", {}) or item.get("published-online", {})).get(
                        "date-parts", [[None]]
                    )[0][0] or ""
                ) if (item.get("published-print", {}) or item.get("published-online", {})).get(
                    "date-parts", [[None]]
                )[0][0] else "",
            }
    except Exception as e:
        logger.warning(f"CrossRef title lookup failed: {e}")
    return None


def _crossref_search_keyword(keyword: str, num_results: int = 10) -> List[Dict[str, Any]]:
    """Search papers by keyword via CrossRef."""
    try:
        url = f"https://api.crossref.org/works?query={urllib.parse.quote(keyword)}&rows={num_results}"
        data = json.loads(_fetch_url(url, timeout=15))
        items = data.get("message", {}).get("items", [])
        results = []
        for item in items:
            results.append({
                "doi": item.get("DOI", ""),
                "title": item.get("title", [""])[0] if isinstance(item.get("title"), list) else item.get("title", ""),
                "author": ", ".join(
                    f"{a.get('given', '')} {a.get('family', '')}".strip()
                    for a in item.get("author", [])
                ),
                "year": str(
                    (item.get("published-print", {}) or item.get("published-online", {})).get(
                        "date-parts", [[None]]
                    )[0][0] or ""
                ) if (item.get("published-print", {}) or item.get("published-online", {})).get(
                    "date-parts", [[None]]
                )[0][0] else "",
            })
        return results
    except Exception as e:
        logger.warning(f"CrossRef keyword search failed: {e}")
        return []


def search_by_doi(doi: str) -> Dict[str, Any]:
    """Search for a paper by DOI. Returns metadata + PDF URL."""
    for mirror in MIRRORS:
        if mirror in _dns_failure_until and time.time() < _dns_failure_until[mirror]:
            continue
        try:
            url = f"https://{mirror}/{doi}"
            html = _fetch_url(url, timeout=30).decode("utf-8", errors="replace")

            if not html or len(html) < 100:
                raise ValueError("Empty or too-short response")

            pdf_url = _extract_pdf_url_from_html(html, url)

            # Extract title from HTML
            title_match = re.search(r'<title>([^<]+)</title>', html)
            title = title_match.group(1).strip() if title_match else doi

            result = {
                "doi": doi,
                "title": title,
                "pdf_url": pdf_url,
                "mirror_used": mirror,
                "status": "success" if pdf_url else "no_pdf",
            }

            if not pdf_url:
                result["error"] = "Could not extract PDF URL from page"

            global _session_mirror
            _session_mirror = mirror
            return result

        except Exception as e:
            logger.warning(f"Mirror {mirror} failed for DOI {doi}: {e}")
            _mark_mirror_failed(mirror)
            continue

    return {"doi": doi, "status": "error", "error": "All mirrors failed"}


def search_by_title(title: str) -> Dict[str, Any]:
    """Search for a paper by title via CrossRef → Sci-Hub."""
    crossref = _crossref_resolve_title(title)
    if not crossref or not crossref.get("doi"):
        return {"title": title, "status": "error", "error": "Could not resolve title to DOI via CrossRef"}

    result = search_by_doi(crossref["doi"])
    # Enrich with CrossRef metadata
    if result.get("status") == "success":
        result.setdefault("title", crossref.get("title", title))
        result.setdefault("author", crossref.get("author", ""))
        result.setdefault("year", crossref.get("year", ""))
        result["doi"] = crossref["doi"]

    return result


def search_by_keyword(keyword: str, num_results: int = 10) -> List[Dict[str, Any]]:
    """Search for papers by keyword via CrossRef, then resolve DOI to Sci-Hub."""
    papers = _crossref_search_keyword(keyword, num_results)
    results = []
    for paper in papers[:num_results]:
        if not paper.get("doi"):
            results.append({**paper, "status": "no_doi"})
            continue
        scihub_result = search_by_doi(paper["doi"])
        if scihub_result.get("status") == "success":
            results.append(scihub_result)
        else:
            results.append({**paper, "status": "scihub_unavailable"})
    return results


def download_pdf(pdf_url: str, output_path: str) -> Dict[str, Any]:
    """Download a PDF from a Sci-Hub URL to a local path."""
    for mirror in MIRRORS:
        if mirror in _dns_failure_until and time.time() < _dns_failure_until[mirror]:
            continue
        try:
            content = _fetch_url(pdf_url, timeout=60)

            # Validate PDF
            if not content.startswith(b"%PDF"):
                # Maybe the URL redirected to a different domain — try direct mirror
                mirror_url = f"https://{mirror}/{pdf_url.split('.org/')[-1]}" if ".org/" in pdf_url else None
                if mirror_url:
                    content = _fetch_url(mirror_url, timeout=60)

                if not content.startswith(b"%PDF"):
                    _mark_mirror_failed(mirror)
                    continue

            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(content)

            global _session_mirror
            _session_mirror = mirror

            return {
                "status": "success",
                "output_path": output_path,
                "bytes": len(content),
                "mirror_used": mirror,
            }

        except Exception as e:
            logger.warning(f"Download failed via {mirror}: {e}")
            _mark_mirror_failed(mirror)
            continue

    return {"status": "error", "error": "All mirrors failed", "output_path": output_path}


# ── CLI entry point (for reach.py custom module routing) ────────────────────

def action_search_doi(params: Dict[str, Any]) -> Dict[str, Any]:
    return search_by_doi(params["doi"])


def action_search_title(params: Dict[str, Any]) -> Dict[str, Any]:
    return search_by_title(params["title"])


def action_search_keyword(params: Dict[str, Any]) -> List[Dict[str, Any]]:
    return search_by_keyword(params["keyword"], params.get("num_results", 10))


def action_download_pdf(params: Dict[str, Any]) -> Dict[str, Any]:
    return download_pdf(params["pdf_url"], params["output_path"])


ACTIONS = {
    "search_doi": action_search_doi,
    "search_title": action_search_title,
    "search_keyword": action_search_keyword,
    "download_pdf": action_download_pdf,
}


def run(action: str, params_json: str) -> Any:
    """Entry point for reach.py custom module routing."""
    params = json.loads(params_json)
    fn = ACTIONS.get(action)
    if not fn:
        return {"status": "error", "error": f"Unknown action: {action}"}
    try:
        return fn(params)
    except Exception as e:
        logger.error(f"scihub.{action} failed: {e}", exc_info=True)
        return {"status": "error", "error": str(e)}
