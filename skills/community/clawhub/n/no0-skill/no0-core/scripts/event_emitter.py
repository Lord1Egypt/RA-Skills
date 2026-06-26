"""Cognitive file tamper event emitter.

Writes Level 4/5 tamper events to ~/.openclaw/no0/events/pending/ so that
No.0-DLC-Internal Control (if installed) can consume them. Core stays
zero-dependency and never fails the main heartbeat loop if emission fails.

Spec: §3.1 event JSON schema.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

SCHEMA_VERSION = "1.0"
EVENT_SOURCE = "no0-core"
EMIT_MIN_LEVEL = 4

EVENTS_ROOT = Path(os.path.expanduser("~/.openclaw/no0/events"))
PENDING_DIR = EVENTS_ROOT / "pending"
EXPIRED_DIR = EVENTS_ROOT / "expired"

# Self-cleanup bounds — guards against unbounded growth when no DLC handler
# is draining pending/. Overridable via env for ops tuning or tests.
EVENT_MAX_AGE_SECONDS = int(os.environ.get("NO0_EVENT_MAX_AGE_SECONDS", 7 * 24 * 3600))
EVENT_MAX_PENDING = int(os.environ.get("NO0_EVENT_MAX_PENDING", 200))
EVENT_WARN_PENDING = int(os.environ.get("NO0_EVENT_WARN_PENDING", 50))

CRITICAL_RULE_GROUPS = {
    "安全机制绕过",
    "自动执行外部命令",
    "敏感信息外发",
    "破坏性清理与覆盖",
}


def _now_iso_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _make_event_id(timestamp_iso: str, file_name: str, new_hash: str) -> str:
    seed = f"{timestamp_iso}|{file_name}|{new_hash}".encode("utf-8")
    short = hashlib.md5(seed).hexdigest()[:6]
    return f"{timestamp_iso}_{short}"


def _build_dlc_request(level: int, rule_hits: Sequence[str], file_name: str) -> Dict[str, Any]:
    critical = any(hit in CRITICAL_RULE_GROUPS for hit in rule_hits)
    require_mfa = level >= 5 or critical
    require_authorization = level >= 4
    reason = (
        f"检测到 {file_name} 被篡改"
        + (f"，命中高危规则：{', '.join(rule_hits)}" if rule_hits else "")
        + "。建议审核并回滚。"
    )
    return {
        "require_authorization": require_authorization,
        "require_mfa": require_mfa,
        "reason_for_user": reason,
    }


def _truncate_preview(text: str, limit: int = 500) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + "..."


def build_event(
    *,
    event_payload: Dict[str, Any],
    level: int,
    reason: str,
    rule_hits: Sequence[str],
    added: int,
    removed: int,
    target_path: Optional[str] = None,
) -> Dict[str, Any]:
    file_name = str(event_payload.get("file_name", "")).strip() or "unknown"
    old_hash = str(event_payload.get("old_hash") or "")
    new_hash = str(event_payload.get("new_hash") or "")
    diff = event_payload.get("diff") if isinstance(event_payload.get("diff"), dict) else {}
    unified_diff = str(diff.get("unified_diff", "") if isinstance(diff, dict) else "")

    timestamp = _now_iso_utc()
    event_id = _make_event_id(timestamp, file_name, new_hash)

    return {
        "event_id": event_id,
        "event_type": "cognitive_file_tampering",
        "schema_version": SCHEMA_VERSION,
        "timestamp": timestamp,
        "source": EVENT_SOURCE,
        "severity": f"level_{level}",
        "severity_numeric": level,
        "target_file": file_name,
        "target_path": target_path or "",
        "baseline_hash": old_hash,
        "current_hash": new_hash,
        "rule_hits": list(rule_hits),
        "diff_summary": {
            "lines_added": added,
            "lines_removed": removed,
        },
        "diff_preview": _truncate_preview(unified_diff),
        "full_diff_path": "~/.openclaw/no0/change_log.json",
        "reason": reason,
        "suggested_action": "rollback_to_baseline",
        "dlc_request": _build_dlc_request(level, rule_hits, file_name),
    }


def _atomic_write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(prefix=".tmp_", suffix=".json", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp_path, path)
    except Exception:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


def _expire_file(path: Path) -> Optional[Path]:
    """Move a pending event to expired/<YYYY-MM-DD>/ so it doesn't clog Core."""
    try:
        day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        target_dir = EXPIRED_DIR / day
        target_dir.mkdir(parents=True, exist_ok=True)
        target = target_dir / path.name
        shutil.move(str(path), str(target))
        return target
    except Exception as exc:  # noqa: BLE001
        print(f"[no0-core] failed to expire {path.name}: {exc}", file=sys.stderr)
        return None


def _enumerate_pending() -> List[Tuple[Path, float]]:
    if not PENDING_DIR.exists():
        return []
    out: List[Tuple[Path, float]] = []
    for entry in PENDING_DIR.iterdir():
        if not entry.is_file() or entry.name.startswith(".tmp_") or entry.suffix != ".json":
            continue
        try:
            mtime = entry.stat().st_mtime
        except OSError:
            continue
        out.append((entry, mtime))
    out.sort(key=lambda item: item[1])
    return out


def _self_cleanup_pending() -> Dict[str, int]:
    """Expire events that are too old or overflow the pending cap.

    Called opportunistically from emit_tamper_event so Core keeps its own
    house even when no DLC consumer is running. Fail-soft.
    """
    stats = {"scanned": 0, "expired_age": 0, "expired_cap": 0}
    try:
        items = _enumerate_pending()
        stats["scanned"] = len(items)
        now = time.time()

        for path, mtime in items:
            if now - mtime > EVENT_MAX_AGE_SECONDS:
                if _expire_file(path) is not None:
                    stats["expired_age"] += 1

        items = _enumerate_pending()
        overflow = len(items) - EVENT_MAX_PENDING
        if overflow > 0:
            for path, _mt in items[:overflow]:
                if _expire_file(path) is not None:
                    stats["expired_cap"] += 1
    except Exception as exc:  # noqa: BLE001
        print(f"[no0-core] pending self-cleanup error: {exc}", file=sys.stderr)
    return stats


def pending_summary() -> Dict[str, Any]:
    """Cheap stat for `./no0 status`: count + warn threshold + oldest age."""
    items = _enumerate_pending()
    oldest_age_s: Optional[float] = None
    if items:
        oldest_age_s = time.time() - items[0][1]
    return {
        "pending_count": len(items),
        "warn_threshold": EVENT_WARN_PENDING,
        "cap": EVENT_MAX_PENDING,
        "oldest_age_seconds": oldest_age_s,
        "max_age_seconds": EVENT_MAX_AGE_SECONDS,
        "warn": len(items) >= EVENT_WARN_PENDING,
    }


def _core_direct_push(event: Dict[str, Any]) -> None:
    """Optional fallback push for Core-only installs (no DLC handler).

    Opt-in via NO0_CORE_DIRECT_PUSH=1 — users with DLC installed should leave
    this unset so the DLC handler owns L5 notifications and Core doesn't
    double-push. No-op if openclaw CLI is absent or severity < 5.
    """
    if os.environ.get("NO0_CORE_DIRECT_PUSH", "") != "1":
        return
    if event.get("severity_numeric") != 5:
        return
    if shutil.which("openclaw") is None:
        return
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from i18n import t as _t  # local import keeps Core zero-dep at module load
    target = event.get("target_file", "?")
    rule_hits = ", ".join(event.get("rule_hits", []) or []) or _t("core_push.none")
    text = (
        _t("core_push.header") + "\n"
        + _t("core_push.file", name=target) + "\n"
        + _t("core_push.time", ts=event.get("timestamp", "")) + "\n"
        + _t("core_push.rules", rules=rule_hits) + "\n"
        + _t("core_push.inspect", name=target)
    )
    try:
        subprocess.run(
            ["openclaw", "system", "event", "--mode", "now", "--text", text],
            capture_output=True,
            timeout=10,
        )
    except Exception as exc:  # noqa: BLE001
        print(f"[no0-core] direct push failed: {exc}", file=sys.stderr)


def emit_tamper_event(
    *,
    event_payload: Dict[str, Any],
    level: int,
    reason: str,
    rule_hits: Sequence[str],
    added: int,
    removed: int,
    target_path: Optional[str] = None,
) -> Optional[Path]:
    """Emit a tamper event to pending/. Returns path on success, None on skip/failure.

    Fail-soft: any exception is caught and logged to stderr so the Core loop
    is never disrupted by DLC-facing emission issues.
    """
    if level is None or level < EMIT_MIN_LEVEL:
        return None
    try:
        event = build_event(
            event_payload=event_payload,
            level=level,
            reason=reason,
            rule_hits=rule_hits,
            added=added,
            removed=removed,
            target_path=target_path,
        )
        dest = PENDING_DIR / f"{event['event_id']}.json"
        _atomic_write(dest, event)
        _self_cleanup_pending()
        _core_direct_push(event)
        return dest
    except Exception as exc:  # noqa: BLE001
        print(f"[no0-core] event emission failed: {exc}", file=sys.stderr)
        return None
