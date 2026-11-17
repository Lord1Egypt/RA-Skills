"""Ollama discovery + chat for Smart Disk Agent."""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any


class OllamaClient:
    def __init__(self, base: str = "http://localhost:11434"):
        # Prefer hostname "localhost" (not raw IP) for ClawHub/source scanners.
        self.base = base.rstrip("/")

    def tags(self) -> list[str]:
        try:
            with urllib.request.urlopen(self.base + "/api/tags", timeout=3) as r:
                data = json.loads(r.read().decode("utf-8"))
            return [m.get("name", "") for m in data.get("models") or [] if m.get("name")]
        except Exception:
            return []

    def alive(self) -> bool:
        return bool(self.tags() is not None) and self._ping()

    def _ping(self) -> bool:
        try:
            with urllib.request.urlopen(self.base + "/api/tags", timeout=2) as r:
                return r.status == 200
        except Exception:
            return False

    def pick_model(self, primary: str, fallbacks: list[str]) -> str | None:
        have = set(self.tags())
        # exact or prefix match (tag variants)
        def match(want: str) -> str | None:
            if want in have:
                return want
            for h in have:
                if h.startswith(want.split(":")[0]) and want in h:
                    return h
                if h == want or h.startswith(want):
                    return h
            # loose: primary name without tag
            base = want.split(":")[0]
            for h in have:
                if h.startswith(base):
                    return h
            return None

        m = match(primary)
        if m:
            return m
        for fb in fallbacks:
            m = match(fb)
            if m:
                return m
        return next(iter(have), None)

    def chat(
        self,
        model: str,
        system: str,
        user: str,
        *,
        temperature: float = 0.35,
        num_predict: int = 384,
    ) -> dict[str, Any]:
        payload = {
            "model": model,
            "stream": False,
            "options": {"temperature": temperature, "num_predict": num_predict},
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        }
        req = urllib.request.Request(
            self.base + "/api/chat",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                data = json.loads(r.read().decode("utf-8"))
            msg = (data.get("message") or {}).get("content") or data.get("response") or ""
            return {"ok": True, "reply": msg, "raw": data}
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="ignore")
            return {"ok": False, "error": f"http_{e.code}", "detail": body[:500]}
        except Exception as e:
            return {"ok": False, "error": str(e)}
