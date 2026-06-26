"""
IMA API Key Preference Management
Version: 1.0.0

Manages per-API-key model preferences for video generation tasks.
Uses API key hash as identifier for preference storage.
"""

import hashlib
import json
import os
from datetime import datetime, timezone

from ima_constants import PREFS_PATH, ALLOWED_MODEL_IDS, normalize_model_id, to_user_facing_model_name


def _hash_api_key(api_key: str) -> str:
    """
    Generate a short hash from API key for storage.
    
    Args:
        api_key: IMA API key (e.g., 'ima_xxx...')
    
    Returns:
        Short hash string (first 12 chars of SHA256)
    """
    return hashlib.sha256(api_key.encode()).hexdigest()[:12]


def load_prefs() -> dict:
    """Load API key preferences from local JSON file."""
    try:
        with open(PREFS_PATH, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_pref(api_key: str, task_type: str, model_params: dict):
    """
    Save API key's preferred model for a specific task type.
    
    Args:
        api_key: IMA API key
        task_type: Task type (e.g., 'text_to_video')
        model_params: Model parameters including model_id, model_name, credit
    """
    os.makedirs(os.path.dirname(PREFS_PATH), exist_ok=True)
    prefs = load_prefs()
    key = f"key_{_hash_api_key(api_key)}"
    canonical_model_id = normalize_model_id(model_params.get("model_id")) or model_params.get("model_id")
    
    prefs.setdefault(key, {})[task_type] = {
        "model_id":    canonical_model_id,
        "model_name":  to_user_facing_model_name(
            model_params.get("model_name"),
            canonical_model_id,
        ),
        "credit":      model_params["credit"],
        "last_used":   datetime.now(timezone.utc).isoformat(),
    }
    
    with open(PREFS_PATH, "w", encoding="utf-8") as f:
        json.dump(prefs, f, ensure_ascii=False, indent=2)


def get_preferred_model_id(api_key: str, task_type: str) -> str | None:
    """
    Retrieve API key's preferred model_id for a task type.
    
    Args:
        api_key: IMA API key
        task_type: Task type (e.g., 'text_to_video')
    
    Returns:
        Canonical model_id if preference exists and is allowed, otherwise None
    """
    prefs = load_prefs()
    entry = (prefs.get(f"key_{_hash_api_key(api_key)}") or {}).get(task_type)
    if not entry:
        return None
    model_id = normalize_model_id(entry.get("model_id"))
    return model_id if model_id in ALLOWED_MODEL_IDS else None
