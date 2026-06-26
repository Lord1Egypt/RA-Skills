#!/usr/bin/env python3
"""
Provider Health Registry — Proactive Health-Based Routing

Tracks per-provider state so the router can make intelligent decisions
BEFORE sending a request, not after it blows up.

State tracked per provider:
  - last_429_at: timestamp of most recent rate-limit error
  - consecutive_429s: how many in a row
  - active_sessions: count of currently running spawns/crons
  - cooldown_until: epoch timestamp, skip provider until this time
  - total_failures: lifetime failure counter

Used by spawn_helper.py to skip degraded providers proactively.

Storage: ~/.openclaw/workspace/memory/provider-health.json
"""

from __future__ import annotations

import json
import os
import time
import fcntl
from pathlib import Path
from typing import Any

HEALTH_FILE = Path(__file__).parent.parent.parent.parent / ".openclaw" / "workspace" / "memory" / "provider-health.json"
# Fallback to relative path
if not HEALTH_FILE.parent.exists():
    HEALTH_FILE = Path(__file__).parent.parent / "provider-health.json"

# How long to cool down after N consecutive 429s (seconds)
COOLDOWN_SCHEDULE = {
    1: 60,       # 1st 429 → 1 min cooldown
    2: 300,      # 2nd → 5 min
    3: 900,      # 3rd → 15 min
    4: 3600,     # 4th → 1 hour
}
MAX_COOLDOWN = 3600 * 4  # 4 hours max

# Max concurrent sessions per provider before routing elsewhere
MAX_CONCURRENT_PER_PROVIDER = 1


def _load() -> dict[str, Any]:
    if not HEALTH_FILE.exists():
        return {}
    try:
        with open(HEALTH_FILE) as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def _save(data: dict[str, Any]) -> None:
    HEALTH_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = HEALTH_FILE.with_suffix(".tmp")
    with open(tmp, "w") as f:
        json.dump(data, f, indent=2)
    tmp.replace(HEALTH_FILE)


def _provider_key(model_id: str) -> str:
    """Extract provider prefix from model_id like 'anthropic-proxy-1/claude-sonnet-4-6'."""
    return model_id.split("/")[0] if "/" in model_id else model_id


def record_429(model_id: str) -> None:
    """Call this when a provider returns 429. Updates cooldown."""
    data = _load()
    key = _provider_key(model_id)
    now = time.time()

    entry = data.get(key, {})
    consecutive = entry.get("consecutive_429s", 0) + 1
    cooldown_secs = COOLDOWN_SCHEDULE.get(consecutive, MAX_COOLDOWN)
    cooldown_until = now + cooldown_secs

    entry.update({
        "last_429_at": now,
        "consecutive_429s": consecutive,
        "cooldown_until": cooldown_until,
        "total_failures": entry.get("total_failures", 0) + 1,
        "last_updated": now,
    })
    data[key] = entry
    _save(data)


def record_success(model_id: str) -> None:
    """Call this on successful response. Resets consecutive 429 counter."""
    data = _load()
    key = _provider_key(model_id)
    now = time.time()

    entry = data.get(key, {})
    entry.update({
        "consecutive_429s": 0,
        "cooldown_until": 0,
        "last_success_at": now,
        "last_updated": now,
    })
    data[key] = entry
    _save(data)


def session_start(model_id: str) -> None:
    """Call when a spawn/session begins on this provider."""
    data = _load()
    key = _provider_key(model_id)
    now = time.time()

    entry = data.get(key, {})
    active = entry.get("active_sessions", 0) + 1
    entry.update({
        "active_sessions": active,
        "last_updated": now,
    })
    data[key] = entry
    _save(data)


def session_end(model_id: str) -> None:
    """Call when a spawn/session finishes on this provider."""
    data = _load()
    key = _provider_key(model_id)
    now = time.time()

    entry = data.get(key, {})
    active = max(0, entry.get("active_sessions", 1) - 1)
    entry.update({
        "active_sessions": active,
        "last_updated": now,
    })
    data[key] = entry
    _save(data)


def is_healthy(model_id: str, check_concurrency: bool = True) -> tuple[bool, str]:
    """
    Returns (is_healthy, reason).
    Use before routing to proactively skip degraded providers.
    """
    data = _load()
    key = _provider_key(model_id)
    entry = data.get(key, {})
    now = time.time()

    # Check cooldown
    cooldown_until = entry.get("cooldown_until", 0)
    if cooldown_until > now:
        remaining = int(cooldown_until - now)
        return False, f"rate-limited, cooldown {remaining}s remaining"

    # Check concurrency
    if check_concurrency:
        active = entry.get("active_sessions", 0)
        if active >= MAX_CONCURRENT_PER_PROVIDER:
            return False, f"{active} active session(s) on this provider — concurrent limit reached"

    return True, "ok"


def get_status(provider_key: str | None = None) -> dict[str, Any]:
    """Get health status for one or all providers."""
    data = _load()
    now = time.time()

    def _enrich(key: str, entry: dict) -> dict:
        cooldown_until = entry.get("cooldown_until", 0)
        in_cooldown = cooldown_until > now
        return {
            **entry,
            "provider": key,
            "in_cooldown": in_cooldown,
            "cooldown_remaining_s": max(0, int(cooldown_until - now)) if in_cooldown else 0,
            "healthy": not in_cooldown and entry.get("active_sessions", 0) < MAX_CONCURRENT_PER_PROVIDER,
        }

    if provider_key:
        entry = data.get(provider_key, {})
        return _enrich(provider_key, entry)

    return {k: _enrich(k, v) for k, v in data.items()}


def pick_healthy(candidates: list[str], check_concurrency: bool = True) -> str | None:
    """
    Given an ordered list of model_ids, return the first one that is healthy.
    Returns None if all are degraded.
    """
    for model_id in candidates:
        healthy, _ = is_healthy(model_id, check_concurrency=check_concurrency)
        if healthy:
            return model_id
    return None


if __name__ == "__main__":
    import sys

    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"

    if cmd == "status":
        status = get_status()
        if not status:
            print("No provider health data yet.")
        else:
            for key, info in status.items():
                icon = "🟢" if info["healthy"] else "🔴"
                cooldown = f" (cooldown {info['cooldown_remaining_s']}s)" if info["in_cooldown"] else ""
                active = info.get("active_sessions", 0)
                fails = info.get("total_failures", 0)
                print(f"{icon} {key}: active={active} failures={fails}{cooldown}")

    elif cmd == "record-429" and len(sys.argv) > 2:
        record_429(sys.argv[2])
        print(f"Recorded 429 for {sys.argv[2]}")

    elif cmd == "record-success" and len(sys.argv) > 2:
        record_success(sys.argv[2])
        print(f"Recorded success for {sys.argv[2]}")

    elif cmd == "session-start" and len(sys.argv) > 2:
        session_start(sys.argv[2])
        print(f"Session started on {sys.argv[2]}")

    elif cmd == "session-end" and len(sys.argv) > 2:
        session_end(sys.argv[2])
        print(f"Session ended on {sys.argv[2]}")

    elif cmd == "is-healthy" and len(sys.argv) > 2:
        healthy, reason = is_healthy(sys.argv[2])
        print(f"{'healthy' if healthy else 'DEGRADED'}: {reason}")
        sys.exit(0 if healthy else 1)

    elif cmd == "pick" and len(sys.argv) > 2:
        candidates = sys.argv[2:]
        chosen = pick_healthy(candidates)
        print(chosen or "NONE")

    else:
        print("Usage: provider_health.py <status|record-429|record-success|session-start|session-end|is-healthy|pick> [model_id...]")
