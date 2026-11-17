#!/usr/bin/env python3
"""
unpaywall.py — Open Access paper lookup via Unpaywall API.

Resolves DOIs to open-access PDF URLs. Checks OA status of academic papers.
Uses CrossRef for title/keyword search.

API: https://api.unpaywall.org/v2/{doi}?email={email}
"""

import json
import os
import urllib.request
import urllib.parse
import urllib.error
import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger("ocas-reach.unpaywall")

BASE_URL = "https://api.unpaywall.org/v2"
EMAIL = "os.environ.get("OCAS_AGENT_EMAIL", "agent@example.com")"


def _fetch(path_or_doi: str, params: Optional[Dict] = None) -> Dict[str, Any]:
    """Fetch from Unpaywall API."""
    url = f"{BASE_URL}/{path_or_doi}?email={EMAIL}"
    if params:
        url += "&" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "ocas-reach/3.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {"error": "not_found", "doi": path_or_doi}
        raise
    except Exception as e:
        return {"error": str(e)}


def _extract_result(data: Dict[str, Any]) -> Dict[str, Any]:
    """Extract clean result from Unpaywall response."""
    best = data.get("best_oa_location") or {}
    return {
        "doi": data.get("doi", ""),
        "title": data.get("title", ""),
        "is_oa": data.get("is_oa", False),
        "oa_status": data.get("oa_status", ""),
        "journal_name": data.get("journal_name", ""),
        "year": data.get("year", ""),
        "best_oa_url": best.get("url", ""),
        "best_oa_pdf": best.get("url_for_pdf", ""),
        "best_oa_host_type": best.get("host_type", ""),
        "best_oa_license": best.get("license", ""),
        "best_oa_version": best.get("version", ""),
        "oa_locations_count": len(data.get("oa_locations", [])),
        "publisher": data.get("publisher", ""),
        "z_authors": _format_authors(data.get("z_authors", [])),
    }


def _format_authors(authors: List) -> str:
    """Format author list."""
    parts = []
    for a in authors[:5]:
        name = a.get("raw_author_name", "")
        if name:
            parts.append(name)
    result = ", ".join(parts)
    if len(authors) > 5:
        result += f" +{len(authors)-5} more"
    return result


def action_doi(params: Dict[str, Any]) -> Dict[str, Any]:
    """Look up a paper by DOI."""
    doi = params.get("doi", "")
    if not doi:
        return {"error": "Missing 'doi' param"}
    data = _fetch(doi)
    if "error" in data:
        return data
    return {"status": "success", **_extract_result(data)}


def action_search(params: Dict[str, Any]) -> Dict[str, Any]:
    """Search for papers by title/keyword via CrossRef, then check OA status."""
    query = params.get("query", "")
    is_oa = params.get("is_oa", None)
    if not query:
        return {"error": "Missing 'query' param"}

    # Search via CrossRef
    cr_url = f"https://api.crossref.org/works?query={urllib.parse.quote(query)}&rows=10"
    if is_oa:
        cr_url += "&filter=has-full-text:true"

    req = urllib.request.Request(cr_url, headers={"User-Agent": "ocas-reach/3.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            cr_data = json.loads(resp.read())
    except Exception as e:
        return {"error": f"CrossRef search failed: {e}"}

    items = cr_data.get("message", {}).get("items", [])
    results = []
    for item in items[:10]:
        doi = item.get("DOI", "")
        if not doi:
            continue
        # Check OA status via Unpaywall
        data = _fetch(doi)
        if "error" in data:
            results.append({
                "doi": doi,
                "title": (item.get("title", [""]) or [""])[0],
                "is_oa": None,
                "status": "lookup_failed",
            })
        else:
            extracted = _extract_result(data)
            if is_oa is None or extracted.get("is_oa") == is_oa:
                results.append(extracted)

    return {"status": "success", "results": results, "total_crossref": len(items)}


ACTIONS = {
    "doi": action_doi,
    "search": action_search,
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
        logger.error(f"unpaywall.{action} failed: {e}", exc_info=True)
        return {"status": "error", "error": str(e)}
