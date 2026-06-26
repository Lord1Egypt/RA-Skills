from __future__ import annotations

import requests

from config import CHANNEL, MODEL, OPENCLAW_BASE, OPENCLAW_TOKEN, canonical_user, user_slug
from prompts import get_prompt


def build_messages(user: str, history: list[dict] | None = None, message: str | None = None) -> list[dict]:
    user = canonical_user(user)
    messages = [{"role": "system", "content": get_prompt(user)}]

    for item in history or []:
        if not isinstance(item, dict):
            continue
        role = item.get("role")
        content = str(item.get("content") or "").strip()
        if role in {"system", "user", "assistant"} and content:
            messages.append({"role": role, "content": content})

    if message:
        messages.append({"role": "user", "content": message})

    return messages


def extract_reply(data: dict) -> str:
    try:
        choices = data.get("choices") or []
        if choices:
            message = choices[0].get("message") or {}
            content = message.get("content")
            if isinstance(content, str) and content.strip():
                return content.strip()
            if isinstance(content, list):
                parts = []
                for part in content:
                    if isinstance(part, dict) and part.get("text"):
                        parts.append(part["text"])
                joined = "\n".join(parts).strip()
                if joined:
                    return joined
    except Exception:
        pass

    error_message = data.get("error")
    if error_message:
        return f"OpenClaw error: {error_message}"

    return "OpenClaw returned no complete reply. The generation may have been interrupted."


def call_openclaw(user: str, message: str | None = None, history: list[dict] | None = None) -> str:
    user = canonical_user(user)

    headers = {
        "Content-Type": "application/json",
        "x-openclaw-message-channel": CHANNEL,
    }
    if OPENCLAW_TOKEN:
        headers["Authorization"] = f"Bearer {OPENCLAW_TOKEN}"

    payload = {
        "model": MODEL,
        "stream": False,
        "user": f"web-gateway:{user_slug(user)}",
        "messages": build_messages(user=user, history=history, message=message),
    }

    response = requests.post(
        f"{OPENCLAW_BASE}/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=180,
    )
    response.raise_for_status()
    return extract_reply(response.json())
