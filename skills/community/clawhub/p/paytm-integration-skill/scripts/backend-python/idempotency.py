"""Minimal in-process idempotency cache for the reference create endpoints.

PRODUCTION NOTE: this is in-memory and per-process - fine for the demo, NOT
fine for a real merchant deployment. Replace with Redis / DynamoDB / a DB row
keyed on (idempotency_key -> {status, body, created_at}) before going live.
The interface here is deliberately small so the swap is straightforward.
"""
import threading
import time
from typing import Optional

TTL_SECONDS = 24 * 60 * 60
MAX_ENTRIES = 10_000

_cache: dict = {}                      # key -> (status, body, created_at)
_lock = threading.Lock()


def _prune_locked():
    if len(_cache) <= MAX_ENTRIES:
        return
    cutoff = time.time() - TTL_SECONDS
    for k in list(_cache.keys()):
        if _cache[k][2] < cutoff:
            del _cache[k]
        if len(_cache) <= MAX_ENTRIES:
            break


def get_cached(key: Optional[str]):
    if not key:
        return None
    with _lock:
        entry = _cache.get(key)
        if not entry:
            return None
        if time.time() - entry[2] > TTL_SECONDS:
            del _cache[key]
            return None
        status, body, _ = entry
        return status, body


def set_cached(key: Optional[str], status: int, body) -> None:
    if not key:
        return
    with _lock:
        _prune_locked()
        _cache[key] = (status, body, time.time())


def read_key(headers, body) -> Optional[str]:
    """Header `Idempotency-Key` is the convention; some clients pass
    `idempotencyKey` in the JSON body - accept both for ergonomics."""
    h = headers.get("Idempotency-Key") or headers.get("idempotency-key")
    if isinstance(h, str) and h.strip():
        return h.strip()
    if isinstance(body, dict):
        b = body.get("idempotencyKey")
        if isinstance(b, str) and b.strip():
            return b.strip()
    return None
