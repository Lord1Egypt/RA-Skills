#!/usr/bin/env python3
from __future__ import annotations

"""Minimal Serper client used by Nomtiq.

Credentials are read only from ``SERPER_API_KEY``.  Errors never include the
credential, request headers, or a full request URL.
"""

import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request

from safe_http import open_no_redirect

SERPER_API_BASE = "https://google.serper.dev"
_ALLOWED_ENDPOINTS = {"search", "maps"}


def _request(endpoint: str, payload: dict, timeout: int = 20) -> dict:
    if endpoint not in _ALLOWED_ENDPOINTS:
        raise ValueError("Unsupported Serper endpoint")

    key = os.environ.get("SERPER_API_KEY", "").strip()
    if not key:
        print("⚠️  SERPER_API_KEY is not configured; Serper search skipped", file=sys.stderr)
        return {}

    safe_payload = dict(payload)
    safe_payload["num"] = max(1, min(int(safe_payload.get("num", 10)), 25))
    request = Request(
        f"{SERPER_API_BASE}/{endpoint}",
        data=json.dumps(safe_payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "X-API-KEY": key,
            "Content-Type": "application/json",
            "User-Agent": "Nomtiq/0.5.1",
        },
        method="POST",
    )
    try:
        with open_no_redirect(request, timeout=timeout) as response:
            return json.loads(response.read())
    except HTTPError as error:
        print(f"Serper API error: HTTP {error.code}", file=sys.stderr)
    except (URLError, TimeoutError):
        print("Serper request failed (network or service unavailable)", file=sys.stderr)
    except (json.JSONDecodeError, ValueError):
        print("Serper returned an invalid response", file=sys.stderr)
    except Exception:
        print("Serper request failed", file=sys.stderr)
    return {}


def search_web(query: str, max_results: int = 10, country: str = "", language: str = "") -> list:
    payload = {"q": query, "num": max_results}
    if country:
        payload["gl"] = country
    if language:
        payload["hl"] = language
    data = _request("search", payload)
    results = []
    for item in data.get("organic") or []:
        normalized = dict(item)
        normalized["url"] = item.get("link", "")
        results.append(normalized)
    return results


def search_maps_raw(query: str, max_results: int = 20) -> list:
    data = _request("maps", {"q": query, "num": max_results})
    return data.get("places") or []
