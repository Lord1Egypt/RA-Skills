#!/usr/bin/env python3
"""Local operator token for Smart Disk Agent HTTP API.

Token is generated on first boot and stored under data/ (never committed).
Not a cloud password wall — same-machine secret for unauth HTTP abuse resistance.
"""
from __future__ import annotations

import hmac
import secrets
from pathlib import Path
from typing import Any


class LocalTokenAuth:
    def __init__(self, root: Path, cfg: dict[str, Any]):
        auth = cfg.get("auth") or {}
        self.required = bool(auth.get("required", True))
        rel = str(auth.get("token_file") or "data/.sda_local_token")
        self.path = (root / rel).resolve()
        # stay inside package root
        if root.resolve() not in self.path.parents and self.path != root.resolve():
            self.path = root / "data" / ".sda_local_token"
        self.header_name = str(auth.get("header") or "X-SDA-Token")
        self._token: str | None = None
        if self.required:
            self._token = self.ensure_token()

    def ensure_token(self) -> str:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if self.path.is_file():
            t = self.path.read_text(encoding="utf-8").strip()
            if len(t) >= 16:
                return t
        t = secrets.token_urlsafe(24)
        self.path.write_text(t + "\n", encoding="utf-8")
        try:
            self.path.chmod(0o600)
        except OSError:
            pass
        return t

    @property
    def token(self) -> str | None:
        return self._token

    def extract(self, headers: Any, query: str = "") -> str | None:
        # Header preferred
        h = headers.get(self.header_name) or headers.get(self.header_name.lower())
        if h:
            return str(h).strip()
        auth = headers.get("Authorization") or headers.get("authorization")
        if auth:
            a = str(auth).strip()
            if a.lower().startswith("bearer "):
                return a[7:].strip()
            return a
        # Query ?t= for one-shot browser open only (portal strips after load)
        if query:
            from urllib.parse import parse_qs

            q = parse_qs(query.lstrip("?"))
            if q.get("t"):
                return q["t"][0]
            if q.get("token"):
                return q["token"][0]
        return None

    def ok(self, provided: str | None) -> bool:
        if not self.required:
            return True
        if not provided or not self._token:
            return False
        return hmac.compare_digest(provided, self._token)

    def public_info(self) -> dict[str, Any]:
        return {
            "auth_required": self.required,
            "auth_mode": "local_token" if self.required else "open_loopback",
            "header": self.header_name,
            "token_file": str(self.path.name),
            "password_gate": False,  # not a remote/vendor password wall
            "local_token": self.required,
        }
