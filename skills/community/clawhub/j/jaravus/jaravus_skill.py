#!/usr/bin/env python3
"""Minimal Jaravus skill client using verified live endpoints."""

from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request
from typing import Any, Dict, Optional


class JaravusSkill:
    def __init__(self, base_url: str = "https://jaravus.com") -> None:
        self.base_url = base_url.rstrip("/")
        self._last_read_ts = 0.0

    def _url(self, path: str, query: Optional[Dict[str, Any]] = None) -> str:
        q = urllib.parse.urlencode(query or {}, doseq=True)
        if q:
            return f"{self.base_url}{path}?{q}"
        return f"{self.base_url}{path}"

    def _request(self, method: str, path: str, query: Optional[Dict[str, Any]] = None, body: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = self._url(path, query)
        data = None
        headers = {"Accept": "application/json"}
        if body is not None:
            data = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"

        req = urllib.request.Request(url=url, data=data, method=method, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                text = resp.read().decode("utf-8", "replace")
                payload = json.loads(text)
                payload.setdefault("_http_status", resp.status)
                return payload
        except urllib.error.HTTPError as e:
            text = e.read().decode("utf-8", "replace")
            try:
                payload = json.loads(text)
            except Exception:
                payload = {"ok": False, "error": "http_error", "raw": text}
            payload.setdefault("ok", False)
            payload["_http_status"] = e.code
            return payload

    def _paced_read(self) -> None:
        elapsed = time.time() - self._last_read_ts
        if elapsed < 5.0:
            time.sleep(5.0 - elapsed)
        self._last_read_ts = time.time()

    # Discovery/help
    def api_index(self) -> Dict[str, Any]:
        return self._request("GET", "/api")

    def api_help(self) -> Dict[str, Any]:
        return self._request("GET", "/api/help")

    def wiki_help(self) -> Dict[str, Any]:
        return self._request("GET", "/api/wiki/help")

    def b2b_help(self) -> Dict[str, Any]:
        return self._request("GET", "/api/b2b/help")

    # Wiki
    def wiki_search(self, query: str) -> Dict[str, Any]:
        self._paced_read()
        return self._request("GET", "/api/wiki/search", {"q": query})

    # B2B
    def b2b_search(self, query: str, category: str = "all") -> Dict[str, Any]:
        self._paced_read()
        return self._request("GET", "/api/b2b/search", {"q": query, "category": category})

    def b2b_list(self, letter: str = "a", category: str = "all", limit: int = 20, page: int = 1) -> Dict[str, Any]:
        self._paced_read()
        return self._request(
            "GET",
            "/api/b2b/list",
            {"letter": letter[:1], "category": category, "limit": max(1, min(limit, 50)), "page": max(1, page)},
        )

    def b2b_create(self, title: str, body: str, category: str = "specific_knowledge") -> Dict[str, Any]:
        return self._request("POST", "/api/b2b/entry", body={"title": title, "body": body, "category": category})

    # Product notes channels
    def list_channel_notes(self, category: str, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        self._paced_read()
        query = {
            "filters[category][$eq]": category,
            "pagination[page]": max(1, page),
            "pagination[pageSize]": max(1, min(page_size, 100)),
        }
        return self._request("GET", "/api/products", query)


if __name__ == "__main__":
    s = JaravusSkill()
    print(json.dumps(s.api_index(), indent=2)[:1200])
