#!/usr/bin/env python3
"""Minimal HTTP client (stdlib only). Raises SkillHttpError on failure."""

import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

__all__ = ["SkillHttpClient", "SkillHttpError"]


class SkillHttpError(Exception):
    def __init__(self, message: str, status_code: int = 0, body: str = ""):
        super().__init__(message)
        self.status_code = status_code
        self.body = body

    def __str__(self):
        return f"[HTTP {self.status_code}] {super().__str__()}" if self.status_code else super().__str__()


class SkillHttpClient:
    def __init__(self, auth_token: str, timeout: int = 60):
        self._auth_token = auth_token
        self._timeout = timeout

    def _headers(self) -> dict:
        return {
            "auth-token":   self._auth_token,
            "Content-Type": "application/json; charset=utf-8",
            "Accept":       "application/json",
        }

    def _send(self, req: urllib.request.Request) -> dict:
        try:
            with urllib.request.urlopen(req, timeout=self._timeout) as r:
                raw = r.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            body = ""
            try: body = e.read().decode("utf-8")
            except Exception: pass
            raise SkillHttpError(f"{req.get_method()} {req.full_url} 失败: {e.reason}",
                                 status_code=e.code, body=body) from e
        except urllib.error.URLError as e:
            raise SkillHttpError(f"网络错误: {e.reason}") from e
        except TimeoutError as e:
            raise SkillHttpError(f"请求超时 (>{self._timeout}s)") from e
        try:
            return json.loads(raw)
        except json.JSONDecodeError as e:
            raise SkillHttpError(f"响应非 JSON: {raw[:200]}") from e

    def get(self, url: str, params: dict[str, Any] | None = None) -> dict:
        if params:
            qs  = "&".join(f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items())
            url = f"{url}{'&' if '?' in url else '?'}{qs}"
        return self._send(urllib.request.Request(url, headers=self._headers(), method="GET"))

    def post(self, url: str, body: dict | None = None) -> dict:
        data = json.dumps(body or {}, ensure_ascii=False).encode("utf-8")
        return self._send(urllib.request.Request(url, data=data, headers=self._headers(), method="POST"))
