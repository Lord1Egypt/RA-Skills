from __future__ import annotations

import json

from config import DEFAULT_USER, STATE_FILE, canonical_user


def sanitize_state(data):
    if not isinstance(data, dict):
        return {"activeUser": DEFAULT_USER, "histories": {}}

    active_user = canonical_user(data.get("activeUser", DEFAULT_USER))
    raw_histories = data.get("histories", {})
    histories = {}

    if isinstance(raw_histories, dict):
        for raw_user, items in raw_histories.items():
            user = canonical_user(raw_user)
            if not isinstance(items, list):
                continue
            cleaned_items = []
            for item in items:
                if not isinstance(item, dict):
                    continue
                role = item.get("role")
                content = str(item.get("content") or "").strip()
                if role in {"user", "assistant"} and content:
                    cleaned_items.append({"role": role, "content": content})
            histories[user] = cleaned_items

    return {"activeUser": active_user, "histories": histories}


def load_state():
    if not STATE_FILE.exists():
        return {"activeUser": DEFAULT_USER, "histories": {}}
    try:
        return sanitize_state(json.loads(STATE_FILE.read_text(encoding="utf-8")))
    except Exception:
        return {"activeUser": DEFAULT_USER, "histories": {}}


def save_state(data):
    cleaned = sanitize_state(data)
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(cleaned, ensure_ascii=False, indent=2), encoding="utf-8")
