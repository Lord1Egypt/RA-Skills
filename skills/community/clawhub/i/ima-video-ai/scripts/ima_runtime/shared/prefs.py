from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from ima_runtime.shared.catalog import normalize_model_id
from ima_runtime.shared.config import PREFS_PATH


def load_prefs(*, prefs_path: Path | None = None) -> dict:
    path = Path(prefs_path or PREFS_PATH)
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_pref(user_id: str, task_type: str, model_params: dict, *, prefs_path: Path | None = None) -> None:
    path = Path(prefs_path or PREFS_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)
    loaded_prefs = load_prefs(prefs_path=path)
    users = loaded_prefs.get("users") if isinstance(loaded_prefs, dict) else None
    prefs = {"users": users if isinstance(users, dict) else {}}
    canonical_model_id = normalize_model_id(model_params.get("model_id")) or model_params.get("model_id")
    prefs["users"].setdefault(user_id, {})[task_type] = {
        "model_id": canonical_model_id,
        "model_name": model_params["model_name"],
        "credit": model_params["credit"],
        "last_used": datetime.now(timezone.utc).isoformat(),
    }
    path.write_text(json.dumps(prefs, ensure_ascii=False, indent=2), encoding="utf-8")


def get_preferred_model_id(user_id: str, task_type: str, *, prefs_path: Path | None = None) -> str | None:
    prefs = load_prefs(prefs_path=prefs_path)
    users = prefs.get("users") if isinstance(prefs, dict) else None
    if not isinstance(users, dict):
        return None
    user_prefs = users.get(user_id)
    if not isinstance(user_prefs, dict):
        return None
    entry = user_prefs.get(task_type)
    if not isinstance(entry, dict):
        return None
    return normalize_model_id(entry.get("model_id"))
