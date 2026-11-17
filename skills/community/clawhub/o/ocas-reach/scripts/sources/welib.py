#!/usr/bin/env python3
"""
welib.py — Free books and papers library via WeLib API.

Searches and retrieves books and academic papers from welib.org.
Aggregates 43M books + 98M papers with direct download links.

⚠️ WeLib is behind Cloudflare. API calls from server-side may be blocked.
If blocked, fail gracefully with a clear error message.
"""

import json
import urllib.request
import urllib.parse
import urllib.error
import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger("ocas-reach.welib")

BASE_URL = "https://welib.org/api/v1"


def _fetch(path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Fetch from WeLib API with Cloudflare awareness."""
    url = f"{BASE_URL}/{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "application/json",
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        if e.code == 403:
            return {"error": "cloudflare_blocked", "detail": "WeLib Cloudflare protection blocked this request. Try using the browser tool or a residential proxy."}
        if e.code == 429:
            return {"error": "rate_limited", "detail": "WeLib rate limit exceeded. Wait before retrying."}
        return {"error": f"HTTP {e.code}", "detail": str(e)}
    except Exception as e:
        if "cloudflare" in str(e).lower() or "captcha" in str(e).lower():
            return {"error": "cloudflare_blocked", "detail": "WeLib Cloudflare protection may be blocking this request."}
        return {"error": str(e)}


def action_search(params: Dict[str, Any]) -> Dict[str, Any]:
    """Search for books and papers."""
    query = params.get("q", "")
    if not query:
        return {"error": "Missing 'q' param"}

    api_params = {
        "q": query,
        "type": params.get("type", "all"),
        "limit": params.get("limit", 10),
    }
    if "offset" in params:
        api_params["offset"] = params["offset"]

    result = _fetch("search", api_params)
    if "error" in result:
        return result

    # Normalize response shape
    items = result.get("results", result.get("items", result.get("data", [])))
    total = result.get("total", len(items))

    return {
        "status": "success",
        "results": items[:api_params["limit"]],
        "total": total,
        "offset": params.get("offset", 0),
        "limit": api_params["limit"],
    }


def action_detail(params: Dict[str, Any]) -> Dict[str, Any]:
    """Get item details by ID."""
    item_id = params.get("id", "")
    if not item_id:
        return {"error": "Missing 'id' param"}

    item_type = params.get("type", "book")
    result = _fetch(f"{item_type}/{item_id}")

    if "error" in result:
        return result

    return {"status": "success", "item": result}


ACTIONS = {
    "search": action_search,
    "detail": action_detail,
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
        logger.error(f"welib.{action} failed: {e}", exc_info=True)
        return {"status": "error", "error": str(e)}
