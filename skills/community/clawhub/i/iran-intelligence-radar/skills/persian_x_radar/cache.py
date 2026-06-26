from __future__ import annotations

from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
from typing import Dict, Optional


CACHE_FILE = Path(__file__).resolve().with_name("charge_cache.json")


def _read_cache() -> Dict[str, str]:
    if not CACHE_FILE.exists():
        return {}
    try:
        with CACHE_FILE.open("r", encoding="utf-8") as f:
            raw = json.load(f)
        return {str(k): str(v) for k, v in raw.items()}
    except (json.JSONDecodeError, OSError, ValueError):
        return {}


def _write_cache(cache: Dict[str, str]) -> None:
    with CACHE_FILE.open("w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


def get_last_charge_timestamp(user_id: str) -> Optional[datetime]:
    cache = _read_cache()
    ts = cache.get(user_id)
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts)
    except ValueError:
        return None


def has_recent_charge(user_id: str, cooldown_minutes: int) -> bool:
    last_ts = get_last_charge_timestamp(user_id)
    if last_ts is None:
        return False
    now = datetime.now(timezone.utc)
    if last_ts.tzinfo is None:
        last_ts = last_ts.replace(tzinfo=timezone.utc)
    return now - last_ts <= timedelta(minutes=cooldown_minutes)


def record_charge(user_id: str) -> None:
    cache = _read_cache()
    cache[user_id] = datetime.now(timezone.utc).isoformat()
    _write_cache(cache)
