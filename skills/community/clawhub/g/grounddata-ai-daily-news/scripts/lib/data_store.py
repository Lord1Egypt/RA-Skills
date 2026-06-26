"""
data_store.py — L3 local cache management

Responsibilities:
- Cache dataset files by date+tier (json)
- TTL management (default 24h)
- Delivery log for ad impression tracking
"""

import json
import time
from pathlib import Path
from typing import Optional

from lib.runtime_paths import (
    get_dataset_cache_dir,
    get_delivery_log_path,
    get_legacy_dataset_cache_dir,
)

CACHE_DIR = get_dataset_cache_dir()
LEGACY_CACHE_DIR = get_legacy_dataset_cache_dir()
DELIVERY_LOG = get_delivery_log_path()


def _cache_path(date: str, tier: str) -> Path:
    safe_tier = tier.replace("/", "_")
    return CACHE_DIR / f"{date}_{safe_tier}.json"


def _legacy_cache_path(date: str, tier: str) -> Path:
    safe_tier = tier.replace("/", "_")
    return LEGACY_CACHE_DIR / f"{date}_{safe_tier}.json"


def get_cached(date: str, tier: str, ttl_seconds: int = 86400) -> Optional[str]:
    """Read from cache, return None if expired"""
    for path in (_cache_path(date, tier), _legacy_cache_path(date, tier)):
        if not path.exists():
            continue
        age = time.time() - path.stat().st_mtime
        if age > ttl_seconds:
            continue
        return path.read_text(encoding="utf-8")
    return None


def save_cached(date: str, tier: str, text: str):
    """Save decompressed text to cache"""
    path = _cache_path(date, tier)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def record_delivery(date: str, tier: str, record_count: int):
    """Record a delivery (for ad counting)"""
    log = _load_log()
    log.append({
        "date": date,
        "tier": tier,
        "record_count": record_count,
        "timestamp": time.time(),
    })
    _save_log(log)


def has_seen_ads() -> bool:
    """Check if ads have already been shown"""
    log = _load_log()
    return any(entry.get("ads_shown", False) for entry in log)


def mark_ads_shown():
    """Mark ads as shown"""
    log = _load_log()
    if log:
        log[-1]["ads_shown"] = True
        _save_log(log)


def _load_log() -> list:
    legacy_delivery_log = get_legacy_dataset_cache_dir() / "delivery_log.json"
    for path in (DELIVERY_LOG, legacy_delivery_log):
        if not path.exists():
            continue
        return json.loads(path.read_text(encoding="utf-8"))
    return []


def _save_log(log: list):
    DELIVERY_LOG.parent.mkdir(parents=True, exist_ok=True)
    DELIVERY_LOG.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")
