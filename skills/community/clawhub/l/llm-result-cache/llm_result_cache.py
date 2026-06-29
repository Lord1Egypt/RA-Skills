"""
llm_result_cache.py — TTL-bounded local cache for expensive LLM/API calls.

The problem this solves: an agent that re-scores or re-analyzes the same
input (the same URL, the same document, the same competitor) across many
separate tasks pays for that LLM call every single time, even though the
input hasn't changed. This is a tiny, dependency-free disk cache that skips
the call entirely on a hit — keyed by whatever string you give it, with a
time-to-live and a bounded entry count so it can't grow unbounded.

Originally extracted from a production website-audit tool where competitor
sites kept recurring across many different clients' audits — caching by URL
cut a meaningful fraction of repeat LLM-scoring calls. Genericized here to
work with any JSON-serializable result, not just that one use case.

PUBLIC API
----------
ResultCache(cache_file, ttl_seconds=86400, max_entries=500)
    .get(key) -> dict | None
    .set(key, value: dict) -> None
    .clear() -> None

cached(cache, key_fn=None)  — decorator that wraps a function with the cache
"""
from __future__ import annotations

import json
import time
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Optional


class ResultCache:
    """A simple JSON-file-backed cache with TTL expiry and a size cap.

    Not for high-throughput/concurrent use — this is a single-process,
    occasional-write cache (reads the whole file, writes the whole file).
    Fine for the "save an LLM call when the same input recurs" use case;
    not a substitute for a real cache server under load."""

    def __init__(self, cache_file: str | Path, ttl_seconds: int = 86400, max_entries: int = 500):
        self.cache_file = Path(cache_file)
        self.ttl_seconds = ttl_seconds
        self.max_entries = max_entries

    def _load(self) -> dict[str, Any]:
        if self.cache_file.exists():
            try:
                return json.loads(self.cache_file.read_text())
            except Exception:
                # Corrupted cache file — treat as empty rather than crashing.
                # (This is a CACHE, not a source of truth, so losing it is
                # safe; a spend/audit ledger would need fail-closed handling
                # instead — see the ad-budget-governor skill for that case.)
                return {}
        return {}

    def _save(self, cache: dict[str, Any]) -> None:
        try:
            self.cache_file.write_text(json.dumps(cache, indent=2))
        except Exception:
            pass  # best-effort — a failed cache write should never break the caller

    def get(self, key: str) -> Optional[dict]:
        cache = self._load()
        entry = cache.get(key)
        if not entry:
            return None
        if time.time() - entry.get("cached_at", 0) > self.ttl_seconds:
            return None
        return entry.get("value")

    def set(self, key: str, value: dict) -> None:
        cache = self._load()
        cache[key] = {"cached_at": time.time(), "value": value}
        if len(cache) > self.max_entries:
            oldest_first = sorted(cache.items(), key=lambda kv: kv[1].get("cached_at", 0))
            cache = dict(oldest_first[-self.max_entries:])
        self._save(cache)

    def clear(self) -> None:
        self._save({})


def cached(cache: ResultCache, key_fn: Optional[Callable[..., str]] = None):
    """Decorator: wrap a function so repeat calls with the same key skip
    re-execution entirely. By default the cache key is the first positional
    argument as a string; pass key_fn(*args, **kwargs) -> str for anything
    more specific (e.g. normalize a URL, hash multiple inputs together)."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            key = key_fn(*args, **kwargs) if key_fn else str(args[0]) if args else ""
            hit = cache.get(key)
            if hit is not None:
                return hit
            result = fn(*args, **kwargs)
            if isinstance(result, dict):
                cache.set(key, result)
            return result
        return wrapper
    return decorator
