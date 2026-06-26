from __future__ import annotations

import json
import os
from datetime import datetime, timezone

from ima_runtime.shared.config import PREFS_PATH


def load_prefs() -> dict:
    try:
        with open(PREFS_PATH, encoding="utf-8") as handle:
            return json.load(handle)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_pref(user_id: str, task_type: str, model_params: dict) -> None:
    os.makedirs(os.path.dirname(PREFS_PATH), exist_ok=True)
    prefs = load_prefs()
    key = f"user_{user_id}"
    prefs.setdefault(key, {})[task_type] = {
        "model_id": model_params["model_id"],
        "model_name": model_params["model_name"],
        "credit": model_params["credit"],
        "last_used": datetime.now(timezone.utc).isoformat(),
    }
    with open(PREFS_PATH, "w", encoding="utf-8") as handle:
        json.dump(prefs, handle, ensure_ascii=False, indent=2)


def get_preferred_model_id(user_id: str, task_type: str) -> str | None:
    prefs = load_prefs()
    entry = (prefs.get(f"user_{user_id}") or {}).get(task_type)
    return entry.get("model_id") if entry else None

