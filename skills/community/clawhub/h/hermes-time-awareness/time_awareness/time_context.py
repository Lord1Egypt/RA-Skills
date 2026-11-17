"""
Time context builder for Hermes Agent.

Generates a compact context block injected into the user message before
each LLM call via the ``pre_llm_call`` plugin hook.

Features:
  - Current time with timezone (IANA name + UTC offset)
  - Elapsed time since last user message (idle detection)
  - Session elapsed time

Design constraints:
  - Ephemeral only: rides the API copy of the user message, never persisted
  - Prompt-cache safe: does not touch the system prompt
  - Zero dependencies: stdlib only (``datetime``, ``threading``, ``zoneinfo``)
  - Never throws: any error returns empty string
"""

from __future__ import annotations

import threading
from datetime import datetime, timezone
from typing import Any, Optional

# ── Timezone resolution ──────────────────────────────────────────────
# Priority: hermes_time module > HERMES_TIMEZONE env > config.yaml > system local

_tz_str: str = ""
_tz_resolved = False


def _resolve_timezone() -> str:
    """Resolve timezone string. Cached after first call."""
    global _tz_str, _tz_resolved
    if _tz_resolved:
        return _tz_str
    _tz_resolved = True

    # 1. Try hermes_time (Hermes's own resolver)
    try:
        import hermes_time  # type: ignore
        resolved = (hermes_time._resolve_timezone_name() or "").strip()
        if resolved:
            _tz_str = resolved
            return _tz_str
    except Exception:
        pass

    # 2. HERMES_TIMEZONE env
    import os
    tz_env = os.environ.get("HERMES_TIMEZONE", "").strip()
    if tz_env:
        _tz_str = tz_env
        return _tz_str

    # 3. config.yaml: timezone field
    try:
        import yaml  # Hermes runtime dependency
        from pathlib import Path
        cfg_path = Path(
            os.environ.get("HERMES_HOME", Path.home() / ".hermes")
        ) / "config.yaml"
        if cfg_path.exists():
            loaded = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
            tz_cfg = loaded.get("timezone", "")
            if isinstance(tz_cfg, str) and tz_cfg.strip():
                _tz_str = tz_cfg.strip()
                return _tz_str
    except Exception:
        pass

    # 4. System local (fallback)
    return ""


# ── Elapsed time tracking ────────────────────────────────────────────

_last_user_ts_lock = threading.Lock()
_last_user_ts: dict[str, float] = {}  # session_id -> unix timestamp


def record_user_message(session_id: str, ts: Optional[float] = None) -> None:
    """Record when a user message was received. Called by the hook."""
    import time
    with _last_user_ts_lock:
        _last_user_ts[session_id] = ts or time.time()


def _get_idle_seconds(session_id: str, conversation_history: Any) -> Optional[float]:
    """Compute seconds since the last user message.

    Sources (in priority order):
      1. Timestamp from conversation_history[-2] (the previous message)
      2. In-process record from record_user_message()
    """
    import time

    # Try conversation history first (cross-process accurate)
    if conversation_history and len(conversation_history) >= 2:
        prev = conversation_history[-2] if len(conversation_history) >= 2 else None
        if prev and isinstance(prev, dict):
            ts_raw = prev.get("timestamp")
            if ts_raw is not None:
                try:
                    if isinstance(ts_raw, (int, float)):
                        prev_ts = float(ts_raw)
                    elif isinstance(ts_raw, str):
                        from datetime import datetime as _dt
                        prev_ts = _dt.fromisoformat(ts_raw).timestamp()
                    else:
                        prev_ts = None
                    if prev_ts and prev_ts > 0:
                        elapsed = time.time() - prev_ts
                        if elapsed > 0:
                            return elapsed
                except Exception:
                    pass

    # Fallback: in-process record
    with _last_user_ts_lock:
        prev_ts = _last_user_ts.get(session_id)
    if prev_ts:
        elapsed = time.time() - prev_ts
        if elapsed > 0:
            return elapsed

    return None


# ── Formatting ───────────────────────────────────────────────────────

_WEEKDAYS_EN = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def _format_elapsed(seconds: float) -> str:
    """Format elapsed seconds into a compact human-readable string."""
    if seconds < 60:
        return "just now"
    mins = int(seconds // 60)
    if mins < 60:
        return f"{mins}m"
    hours = mins // 60
    remaining_mins = mins % 60
    if hours < 24:
        return f"{hours}h{remaining_mins}m" if remaining_mins else f"{hours}h"
    days = hours // 24
    remaining_hours = hours % 24
    return f"{days}d{remaining_hours}h" if remaining_hours else f"{days}d"


def format_time_context(
    session_id: str = "",
    conversation_history: Any = None,
    is_first_turn: bool = False,
) -> str:
    """Build the time context block.

    Returns a string like:
        [time: 2026-08-29 18:00 AEST +10:00 Sat]
    or with idle info:
        [time: 2026-08-29 18:00 AEST +10:00 Sat | idle: 47m]

    Returns empty string on any error.
    """
    try:
        # Resolve timezone
        tz_label = ""
        tz_offset = ""
        tz_name = _resolve_timezone()

        try:
            if tz_name:
                from zoneinfo import ZoneInfo
                now = datetime.now(ZoneInfo(tz_name))
                tz_label = tz_name
            else:
                now = datetime.now().astimezone()
        except Exception:
            now = datetime.now().astimezone()

        # Format offset
        offset_str = now.strftime("%z")  # e.g. "+1000"
        if offset_str:
            tz_offset = f"{offset_str[:3]}:{offset_str[3:]}"

        weekday = _WEEKDAYS_EN[now.weekday()]
        tz_display = tz_label or now.strftime("%Z") or tz_offset

        parts = [
            f"time: {now.strftime('%Y-%m-%d %H:%M')} {tz_display} {tz_offset} {weekday}"
        ]

        # Idle detection (skip on first turn)
        if not is_first_turn and session_id:
            idle = _get_idle_seconds(session_id, conversation_history)
            if idle is not None and idle >= 60:
                parts.append(f"idle: {_format_elapsed(idle)}")

        return "[" + " | ".join(parts) + "]"

    except Exception:
        return ""
