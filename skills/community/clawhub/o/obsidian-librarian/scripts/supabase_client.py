#!/usr/bin/env python3
from __future__ import annotations

import urllib.parse
from typing import Any

from common import http_json_request, http_request


class SupabaseClient:
    def __init__(self, url: str, key: str) -> None:
        if not url or not key:
            raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set")
        self.base_url = url.rstrip("/")
        self.key = key
        self._headers = {
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal",
        }

    def rpc(self, function_name: str, params: dict[str, Any]) -> Any:
        url = f"{self.base_url}/rest/v1/rpc/{function_name}"
        return http_json_request(url, method="POST", headers=self._headers, json_body=params)

    def upsert(self, table: str, rows: list[dict[str, Any]], *, on_conflict: str) -> None:
        url = f"{self.base_url}/rest/v1/{table}"
        headers = {
            **self._headers,
            "Prefer": "resolution=merge-duplicates,return=minimal",
        }
        url += f"?on_conflict={urllib.parse.quote(on_conflict, safe=',')}"
        http_request(url, method="POST", headers=headers, json_body=rows)

    def select(self, table: str, *, columns: str = "*", filters: dict[str, str] | None = None) -> Any:
        url = f"{self.base_url}/rest/v1/{table}?select={urllib.parse.quote(columns, safe=',')}"
        for col, op in (filters or {}).items():
            url += f"&{urllib.parse.quote(col)}={urllib.parse.quote(op, safe='')}"
        return http_json_request(url, method="GET", headers=self._headers)

    def delete(self, table: str, *, filters: dict[str, str]) -> None:
        url = f"{self.base_url}/rest/v1/{table}"
        query_parts = [
            f"{urllib.parse.quote(col)}={urllib.parse.quote(op, safe='')}"
            for col, op in filters.items()
        ]
        if query_parts:
            url += "?" + "&".join(query_parts)
        http_request(url, method="DELETE", headers=self._headers)
