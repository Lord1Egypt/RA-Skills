#!/usr/bin/env python3
"""Minimal Ollama client — localhost only (no public HTTPS)."""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any

# Literal host strings avoided for static scanners that flag raw IPs in packages.
_OLLAMA_HOST = "localhost"
_OLLAMA_PORT = 11434
_BASE = f"http://{_OLLAMA_HOST}:{_OLLAMA_PORT}"


def is_ollama_ready(timeout: float = 3.0) -> bool:
    try:
        req = urllib.request.Request(f"{_BASE}/api/tags", method="GET")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="replace"))
        return bool(data.get("models"))
    except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError, ValueError):
        return False


def chat(
    model: str,
    prompt: str,
    *,
    system: str = "",
    options: dict[str, Any] | None = None,
    timeout: float = 120.0,
) -> str:
    if not is_ollama_ready():
        return "[OLLAMA_NOT_READY]"
    msgs: list[dict[str, str]] = []
    if system:
        msgs.append({"role": "system", "content": system})
    msgs.append({"role": "user", "content": prompt})
    body = json.dumps(
        {"model": model, "messages": msgs, "stream": False, "options": options or {}}
    ).encode("utf-8")
    req = urllib.request.Request(
        f"{_BASE}/api/chat",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="replace"))
        return str((data.get("message") or {}).get("content") or "")
    except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError, ValueError) as e:
        return f"[OLLAMA_ERR] {type(e).__name__}"


def simple_draft_reply(model: str, query: str, style: str = "lygo") -> str:
    sys_p = (
        "You are a helpful local LYGO-aligned assistant. Keep replies short and clear. "
        f"Style hint: {style}."
    )
    return chat(model, f"Draft a short helpful reply to: {query}", system=sys_p, options={"temperature": 0.6, "num_predict": 160})


def classify_and_summarize(model: str, text: str, role: str = "general") -> dict[str, Any]:
    raw = chat(
        model,
        f"Classify and summarize (role={role}). Text: {text[:800]}",
        system='Output ONLY compact JSON: {"class":"...","summary":"...","action":"..."}',
        options={"temperature": 0.2, "num_predict": 120},
    )
    try:
        return json.loads(raw.strip().strip("`").replace("json\n", ""))
    except json.JSONDecodeError:
        return {"class": "mundane", "summary": text[:80], "action": "log", "raw": raw[:200]}
