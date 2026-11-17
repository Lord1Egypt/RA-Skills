# Copyright (c) 2026 Ming Fang — MIT (vendored from perplexity-skill drivers/webbridge.py)
"""Thin kimi-webbridge HTTP transport: read-only probes retry once, mutating calls never retry."""
from __future__ import annotations

from typing import Any

import httpx


class WebBridgeError(RuntimeError):
    def __init__(self, kind: str, message: str):
        super().__init__(f"webbridge[{kind}]: {message}")
        self.kind = kind


class WebBridgeDriver:
    def __init__(self, session: str, endpoint: str = "http://127.0.0.1:10086/command"):
        if not session:
            raise ValueError("session is required")
        self.session, self.endpoint = session, endpoint

    def call(self, action: str, *, mutating: bool = False, **args: Any) -> dict:
        payload = {"action": action, "args": args, "session": self.session}
        attempts = 1 if mutating else 2
        last: Exception | None = None
        for _ in range(attempts):
            try:
                r = httpx.post(self.endpoint, json=payload, timeout=60.0)
                data = r.json()
            except (httpx.HTTPError, ValueError) as e:  # network/parse
                last = e
                continue
            if data.get("ok"):
                return data.get("data", {})
            err = data.get("error", {})
            kind = str(err.get("code", "unknown"))
            if not mutating and kind in {"http_502", "timeout", "connect"}:
                continue
            raise WebBridgeError(kind, str(err.get("message", "")))
        raise WebBridgeError("connect", f"exhausted retries: {last}")

    def evaluate(self, code: str, *, mutating: bool = False) -> Any:
        data = self.call("evaluate", mutating=mutating, code=code)
        return data.get("value") if isinstance(data, dict) else data
