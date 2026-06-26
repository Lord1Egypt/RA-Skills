#!/usr/bin/env python3
"""Shared in-memory and optional disk cache for NBA_TR."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
import threading
import time
from pathlib import Path
from typing import Any, Callable

from nba_common import NBAReportError

MEMORY_LOCK = threading.Lock()
MEMORY_CACHE: dict[tuple[str, str], dict[str, Any]] = {}

DEFAULT_DISK_NAMESPACES = {
    "espn:scoreboard",
    "espn:summary",
    "espn:team_roster",
    "espn:team_schedule",
    "espn:team_statistics",
    "nba:game_story",
    "nba:league_schedule",
    "nba:scoreboard",
    "nba:play_by_play",
    "nba:boxscore",
    "nba:team_roster",
}


def disk_cache_enabled() -> bool:
    return False


def cache_root() -> Path:
    return Path(tempfile.gettempdir()) / "nba_tr_cache"


def _cache_key(namespace: str, key: str) -> tuple[str, str]:
    return namespace, key


def _serialize_payload(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))


def _cache_path(namespace: str, key: str) -> Path:
    digest = hashlib.sha256(f"{namespace}:{key}".encode("utf-8")).hexdigest()
    return cache_root() / namespace.replace(":", "_") / f"{digest}.json"


def _read_disk_entry(path: Path) -> dict[str, Any] | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _write_disk_entry(path: Path, entry: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        dir=path.parent,
        prefix=f"{path.stem}.",
        suffix=".tmp",
        delete=False,
    ) as tmp_file:
        tmp_path = Path(tmp_file.name)
        tmp_file.write(json.dumps(entry, ensure_ascii=False))
        tmp_file.flush()
        os.fsync(tmp_file.fileno())
    try:
        tmp_path.replace(path)
    finally:
        tmp_path.unlink(missing_ok=True)


def _trim_oversized_entry(entry: dict[str, Any], max_payload_bytes: int) -> dict[str, Any]:
    payload_text = _serialize_payload(entry.get("payload"))
    if len(payload_text.encode("utf-8")) <= max_payload_bytes:
        return entry
    raise NBAReportError("缓存对象超过大小上限。", kind="invalid_cache_entry")


def cached_json_fetch(
    *,
    namespace: str,
    key: str,
    ttl_seconds: int,
    fetcher: Callable[[], Any],
    allow_stale: bool = True,
    max_payload_bytes: int = 2_000_000,
    use_disk: bool | None = None,
) -> tuple[Any, str]:
    now = time.time()
    cache_key = _cache_key(namespace, key)
    disk_allowed = disk_cache_enabled() if use_disk is None else use_disk

    with MEMORY_LOCK:
        memory_entry = MEMORY_CACHE.get(cache_key)
    if memory_entry and memory_entry.get("expiresAt", 0) >= now:
        return memory_entry.get("payload"), "fresh"

    disk_path = _cache_path(namespace, key)
    disk_entry = None
    if disk_allowed and namespace in DEFAULT_DISK_NAMESPACES:
        disk_entry = _read_disk_entry(disk_path)
        if disk_entry and disk_entry.get("expiresAt", 0) >= now:
            with MEMORY_LOCK:
                MEMORY_CACHE[cache_key] = disk_entry
            return disk_entry.get("payload"), "fresh"

    try:
        payload = fetcher()
    except Exception as exc:
        stale_entry = memory_entry or disk_entry
        if allow_stale and stale_entry and stale_entry.get("payload") is not None:
            return stale_entry.get("payload"), "stale"
        if isinstance(exc, NBAReportError):
            raise
        raise NBAReportError(str(exc), kind="request_failed") from exc

    entry = _trim_oversized_entry(
        {
            "namespace": namespace,
            "key": key,
            "storedAt": now,
            "expiresAt": now + max(ttl_seconds, 0),
            "payload": payload,
        },
        max_payload_bytes=max_payload_bytes,
    )

    with MEMORY_LOCK:
        MEMORY_CACHE[cache_key] = entry
    if disk_allowed and namespace in DEFAULT_DISK_NAMESPACES:
        _write_disk_entry(disk_path, entry)
    return payload, "fresh"


def clear_memory_cache() -> None:
    with MEMORY_LOCK:
        MEMORY_CACHE.clear()
