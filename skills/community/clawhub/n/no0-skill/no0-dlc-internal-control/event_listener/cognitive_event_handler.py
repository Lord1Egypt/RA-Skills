"""DLC-side handler for cognitive_file_tampering events.

Watches ~/.openclaw/no0/events/pending/, applies severity policy, writes an
audit row, and archives to processed/<YYYY-MM-DD>/.

Severity policy (v0.3.0):
  - L5  → fetch Core's version list, push an immediate alert via
          `openclaw system event --mode now`, drop a pending_decision lock,
          await a human decision. No auto-rollback.
  - L4  → log only; the hourly cron report picks it up.
  - <4  → shouldn't be emitted by Core; logged defensively.

Schema-version mismatch or unreadable events are archived with a rejection
reason in audit.csv and never trigger pushes or rollbacks.

Polling is 5 s by default (spec §3.2). FSEvents/inotify is deferred.

Set NO0_DLC_DISABLE_PUSH=1 to suppress outbound `openclaw system event`
calls — used by the integration test, and useful for dry-run installs.

Invocation:
    python3 cognitive_event_handler.py              # run forever
    python3 cognitive_event_handler.py --once       # one sweep, then exit
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import shutil
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from i18n import t  # noqa: E402

SUPPORTED_SCHEMA_MAJOR = "1"

EVENTS_ROOT = Path(os.path.expanduser("~/.openclaw/no0/events"))
PENDING_DIR = EVENTS_ROOT / "pending"
PROCESSED_DIR = EVENTS_ROOT / "processed"

DLC_RUNTIME_DIR = Path(os.path.expanduser("~/.openclaw/no0/dlc"))
AUDIT_LOG_PATH = DLC_RUNTIME_DIR / "audit.csv"
PENDING_DECISIONS_DIR = DLC_RUNTIME_DIR / "pending_decisions"
PUSH_FAILURES_LOG = DLC_RUNTIME_DIR / "push_failures.log"

PUSH_TIMEOUT_SEC = 10
VERSIONS_TIMEOUT_SEC = 10
PUSH_MAX_RETRIES = 5

AUDIT_HEADER = [
    "audit_timestamp",
    "event_id",
    "event_timestamp",
    "severity",
    "target_file",
    "rule_hits",
    "action_taken",
    "action_result",
    "require_mfa",
    "require_authorization",
    "schema_version",
]


def _log(msg: str) -> None:
    print(f"[dlc-handler] {msg}", flush=True)


def _now_iso_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _ensure_runtime() -> None:
    DLC_RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    PENDING_DECISIONS_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def _push_disabled() -> bool:
    return os.environ.get("NO0_DLC_DISABLE_PUSH", "") == "1"


def _append_audit(row: Dict[str, Any]) -> None:
    _ensure_runtime()
    new_file = not AUDIT_LOG_PATH.exists()
    with AUDIT_LOG_PATH.open("a", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=AUDIT_HEADER)
        if new_file:
            writer.writeheader()
        writer.writerow({k: row.get(k, "") for k in AUDIT_HEADER})


def _archive(event_path: Path, event_id: str) -> Path:
    day_dir = PROCESSED_DIR / _today()
    day_dir.mkdir(parents=True, exist_ok=True)
    dest = day_dir / f"{event_id}.json"
    shutil.move(str(event_path), str(dest))
    return dest


def _schema_ok(event: Dict[str, Any]) -> bool:
    version = str(event.get("schema_version", ""))
    major = version.split(".", 1)[0] if version else ""
    return major == SUPPORTED_SCHEMA_MAJOR


def _locate_no0_dispatcher() -> Optional[Path]:
    here = Path(__file__).resolve()
    for parent in [here.parent, *here.parents]:
        candidate = parent.parent / "no0"
        if candidate.exists() and os.access(candidate, os.X_OK):
            return candidate
    return None


def _lock_path(target_file: str) -> Path:
    basename = Path(target_file).name if target_file else "unknown"
    return PENDING_DECISIONS_DIR / f"{basename}.lock"


def _fetch_versions(target_file: str) -> str:
    """Ask Core for the version list of `target_file`. Stdout verbatim, or ''."""
    if not target_file:
        return ""
    no0_bin = _locate_no0_dispatcher()
    if no0_bin is None:
        return ""
    try:
        result = subprocess.run(
            [str(no0_bin), "versions", Path(target_file).name],
            capture_output=True,
            text=True,
            timeout=VERSIONS_TIMEOUT_SEC,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:  # noqa: BLE001
        pass
    return ""


def _push_l5_alert(event: Dict[str, Any], versions_blob: str, lock: Path) -> str:
    """Fire `openclaw system event --mode now`. Returns a short status label."""
    if _push_disabled():
        return "push_skipped_env"
    if shutil.which("openclaw") is None:
        return "push_failed_no_cli"

    target = event.get("target_file", "<unknown>")
    rule_hits = ", ".join(event.get("rule_hits", []) or []) or t("push.none")
    ts = event.get("timestamp", _now_iso_utc())
    versions_section = versions_blob or t("push.versions_unavailable")
    text = (
        t("push.header") + "\n"
        + t("push.file", name=target) + "\n"
        + t("push.time", ts=ts) + "\n"
        + t("push.rules", rules=rule_hits) + "\n\n"
        + t("push.versions_label") + "\n"
        + f"{versions_section}\n\n"
        + t("push.prompt") + "\n"
        + t("push.cleanup", lock=lock)
    )
    try:
        result = subprocess.run(
            ["openclaw", "system", "event", "--mode", "now", "--text", text],
            capture_output=True,
            text=True,
            timeout=PUSH_TIMEOUT_SEC,
        )
        if result.returncode == 0:
            return "pushed_ok"
        return f"push_failed_rc{result.returncode}"
    except subprocess.TimeoutExpired:
        return "push_timeout"
    except Exception as exc:  # noqa: BLE001
        return f"push_error_{type(exc).__name__}"


def _push_succeeded(status: str) -> bool:
    return status == "pushed_ok" or status == "push_skipped_env"


def _record_push_failure(event: Dict[str, Any], lock: Path, reason: str) -> None:
    """Append a JSONL entry so retries + visibility surfaces elsewhere."""
    PUSH_FAILURES_LOG.parent.mkdir(parents=True, exist_ok=True)
    row = {
        "recorded_at": _now_iso_utc(),
        "event_id": event.get("event_id"),
        "target_file": event.get("target_file"),
        "severity": event.get("severity"),
        "lock": str(lock),
        "reason": reason,
        "retry_count": 0,
    }
    with PUSH_FAILURES_LOG.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def _load_push_failures() -> list:
    if not PUSH_FAILURES_LOG.exists():
        return []
    rows = []
    for line in PUSH_FAILURES_LOG.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except Exception:
            continue
    return rows


def _rewrite_push_failures(rows: list) -> None:
    if not rows:
        if PUSH_FAILURES_LOG.exists():
            PUSH_FAILURES_LOG.unlink()
        return
    PUSH_FAILURES_LOG.parent.mkdir(parents=True, exist_ok=True)
    with PUSH_FAILURES_LOG.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def retry_push_failures() -> Dict[str, int]:
    """Re-attempt pushes for prior failures whose lock still exists.

    Drops entries whose lock is gone (user resolved via decide) or whose
    retry_count exceeds the cap. Called at handler startup + before each sweep.
    """
    stats = {"retried": 0, "recovered": 0, "still_failing": 0, "dropped": 0}
    rows = _load_push_failures()
    if not rows:
        return stats

    survivors: list = []
    for row in rows:
        lock_path = Path(row.get("lock", ""))
        if not lock_path.exists():
            stats["dropped"] += 1
            continue
        if row.get("retry_count", 0) >= PUSH_MAX_RETRIES:
            stats["dropped"] += 1
            continue
        try:
            lock_payload = json.loads(lock_path.read_text(encoding="utf-8"))
        except Exception:
            stats["dropped"] += 1
            continue

        synthetic_event = {
            "event_id": lock_payload.get("event_id"),
            "target_file": lock_payload.get("target_file"),
            "timestamp": lock_payload.get("pushed_at"),
            "rule_hits": lock_payload.get("rule_hits", []),
            "severity": lock_payload.get("severity"),
        }
        status = _push_l5_alert(synthetic_event, lock_payload.get("versions_blob", ""), lock_path)
        stats["retried"] += 1
        if _push_succeeded(status):
            stats["recovered"] += 1
            continue
        row["retry_count"] = int(row.get("retry_count", 0)) + 1
        row["last_attempt_at"] = _now_iso_utc()
        row["last_reason"] = status
        survivors.append(row)
        stats["still_failing"] += 1

    _rewrite_push_failures(survivors)
    return stats


def _write_lock(event: Dict[str, Any], versions_blob: str) -> Path:
    lock = _lock_path(str(event.get("target_file", "")))
    payload = {
        "event_id": event.get("event_id"),
        "target_file": event.get("target_file"),
        "severity": event.get("severity"),
        "severity_numeric": event.get("severity_numeric"),
        "pushed_at": _now_iso_utc(),
        "rule_hits": event.get("rule_hits", []),
        "versions_blob": versions_blob,
    }
    lock.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return lock


def handle_event(event_path: Path) -> None:
    try:
        event = json.loads(event_path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        _log(f"skipping unreadable event {event_path.name}: {exc}")
        return

    if not isinstance(event, dict):
        _log(f"skipping non-object event {event_path.name}")
        return

    event_id = str(event.get("event_id", event_path.stem))

    if not _schema_ok(event):
        _append_audit({
            "audit_timestamp": _now_iso_utc(),
            "event_id": event_id,
            "event_timestamp": event.get("timestamp", ""),
            "severity": event.get("severity", ""),
            "target_file": event.get("target_file", ""),
            "rule_hits": ";".join(event.get("rule_hits", []) or []),
            "action_taken": "rejected_schema_mismatch",
            "action_result": f"schema={event.get('schema_version')}",
            "require_mfa": "",
            "require_authorization": "",
            "schema_version": str(event.get("schema_version", "")),
        })
        _archive(event_path, event_id)
        return

    dlc_request = event.get("dlc_request", {}) if isinstance(event.get("dlc_request"), dict) else {}
    severity_numeric = event.get("severity_numeric")
    target_file = str(event.get("target_file", ""))

    action_taken = "logged_only"
    action_result = ""

    if severity_numeric == 5:
        lock = _lock_path(target_file)
        if lock.exists():
            action_taken = "deduped_pending_decision"
            action_result = f"existing_lock={lock.name}"
        else:
            versions_blob = _fetch_versions(target_file)
            lock = _write_lock(event, versions_blob)
            push_status = _push_l5_alert(event, versions_blob, lock)
            versions_flag = "available" if versions_blob else "unavailable"
            action_taken = "pushed_decision_request"
            action_result = f"push={push_status};versions={versions_flag};lock={lock.name}"
            if not _push_succeeded(push_status):
                _record_push_failure(event, lock, push_status)
    elif severity_numeric == 4:
        action_result = "pending_hourly_report"

    _append_audit({
        "audit_timestamp": _now_iso_utc(),
        "event_id": event_id,
        "event_timestamp": event.get("timestamp", ""),
        "severity": event.get("severity", ""),
        "target_file": event.get("target_file", ""),
        "rule_hits": ";".join(event.get("rule_hits", []) or []),
        "action_taken": action_taken,
        "action_result": action_result,
        "require_mfa": str(bool(dlc_request.get("require_mfa"))),
        "require_authorization": str(bool(dlc_request.get("require_authorization"))),
        "schema_version": str(event.get("schema_version", "")),
    })
    _archive(event_path, event_id)
    _log(f"handled {event_id}: {action_taken} / {action_result}")


def sweep_pending() -> int:
    retry_stats = retry_push_failures()
    if retry_stats["retried"]:
        _log(
            f"push-failure retry: attempted={retry_stats['retried']} "
            f"recovered={retry_stats['recovered']} still_failing={retry_stats['still_failing']} "
            f"dropped={retry_stats['dropped']}"
        )
    if not PENDING_DIR.exists():
        return 0
    handled = 0
    for entry in sorted(PENDING_DIR.iterdir()):
        if not entry.is_file() or entry.name.startswith(".tmp_") or entry.suffix != ".json":
            continue
        handle_event(entry)
        handled += 1
    return handled


def run_forever(interval_seconds: float = 5.0) -> None:
    _ensure_runtime()
    _log(f"polling {PENDING_DIR} every {interval_seconds}s")
    stop = {"flag": False}

    def _handler(signum, _frame):  # noqa: ARG001
        _log(f"received signal {signum}, exiting after current sweep")
        stop["flag"] = True

    signal.signal(signal.SIGINT, _handler)
    signal.signal(signal.SIGTERM, _handler)

    while not stop["flag"]:
        sweep_pending()
        for _ in range(int(interval_seconds * 10)):
            if stop["flag"]:
                break
            time.sleep(0.1)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="DLC cognitive event handler")
    parser.add_argument("--once", action="store_true", help="Single sweep, then exit")
    parser.add_argument("--interval", type=float, default=5.0, help="Poll interval seconds")
    parser.add_argument(
        "--install-daemon",
        action="store_true",
        help="TODO: install a launchd/systemd daemon (deferred)",
    )
    args = parser.parse_args(argv)

    if args.install_daemon:
        _log("TODO: daemon install not implemented in v0.3.0 — run manually or via cron")
        return 0

    _ensure_runtime()
    if args.once:
        handled = sweep_pending()
        _log(f"single sweep complete: handled={handled}")
        return 0

    run_forever(args.interval)
    return 0


if __name__ == "__main__":
    sys.exit(main())
