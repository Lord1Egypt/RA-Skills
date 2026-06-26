"""Hourly conditional report for the No.0 main agent.

Design: the main agent runs this on each cron tick. If nothing changed since
the previous tick, the script prints nothing and exits 0 — so the agent stays
silent. If there's a delta, it emits a concise summary the agent can relay.

Data sources (Core alone or Core+DLC):
  - ~/.openclaw/no0/change_log.json           (Core)  new tamper records
  - ~/.openclaw/no0/dlc/audit.csv             (DLC)   L4/L5 decisions + dedupes
  - ~/.openclaw/no0/dlc/pending_decisions/    (DLC)   outstanding L5 locks
  - ~/.openclaw/no0/events/pending/           (Core)  unconsumed events
  - ~/.openclaw/no0/events/expired/           (Core)  TTL-expired / over-cap

Cursor: ~/.openclaw/no0/hourly_cursor.json  (offsets into change_log + audit)

Usage:
  python3 hourly_report.py              # delta summary, silent if empty
  python3 hourly_report.py --json       # same but structured
  python3 hourly_report.py --reset      # rewind cursor to zero
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))
from i18n import t  # noqa: E402

NO0_ROOT = Path(os.path.expanduser("~/.openclaw/no0"))
CHANGE_LOG = NO0_ROOT / "change_log.json"
AUDIT_LOG = NO0_ROOT / "dlc" / "audit.csv"
PENDING_DECISIONS = NO0_ROOT / "dlc" / "pending_decisions"
PENDING_EVENTS = NO0_ROOT / "events" / "pending"
EXPIRED_EVENTS = NO0_ROOT / "events" / "expired"
CURSOR_FILE = NO0_ROOT / "hourly_cursor.json"


def _load_cursor() -> Dict[str, Any]:
    if not CURSOR_FILE.exists():
        return {"change_log_count": 0, "audit_rows": 0}
    try:
        return json.loads(CURSOR_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {"change_log_count": 0, "audit_rows": 0}


def _save_cursor(cursor: Dict[str, Any]) -> None:
    CURSOR_FILE.parent.mkdir(parents=True, exist_ok=True)
    CURSOR_FILE.write_text(json.dumps(cursor, ensure_ascii=False, indent=2), encoding="utf-8")


def _read_change_log() -> List[Dict[str, Any]]:
    if not CHANGE_LOG.exists():
        return []
    try:
        data = json.loads(CHANGE_LOG.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except Exception:
        return []


def _read_audit() -> List[Dict[str, str]]:
    if not AUDIT_LOG.exists():
        return []
    try:
        with AUDIT_LOG.open("r", encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh)
            return list(reader)
    except Exception:
        return []


def _count_files(directory: Path, recursive: bool = False) -> int:
    if not directory.exists():
        return 0
    pattern = "**/*" if recursive else "*"
    return sum(1 for p in directory.glob(pattern) if p.is_file())


def _read_locks() -> List[Dict[str, Any]]:
    if not PENDING_DECISIONS.exists():
        return []
    out: List[Dict[str, Any]] = []
    for lock in sorted(PENDING_DECISIONS.glob("*.lock")):
        try:
            payload = json.loads(lock.read_text(encoding="utf-8"))
        except Exception:
            payload = {"target_file": lock.stem, "severity": "unknown"}
        out.append(payload)
    return out


def build_report(reset: bool = False) -> Dict[str, Any]:
    cursor = {"change_log_count": 0, "audit_rows": 0} if reset else _load_cursor()

    change_rows = _read_change_log()
    audit_rows = _read_audit()

    new_change = max(0, len(change_rows) - int(cursor.get("change_log_count", 0)))
    new_audit = audit_rows[int(cursor.get("audit_rows", 0)):]

    # Severity breakdown in new audit rows
    pushed = 0
    deduped = 0
    rejected = 0
    for row in new_audit:
        action = row.get("action_taken", "")
        if action == "pushed_decision_request":
            pushed += 1
        elif action == "deduped_pending_decision":
            deduped += 1
        elif action == "rejected_schema_mismatch":
            rejected += 1

    locks = _read_locks()
    pending_events = _count_files(PENDING_EVENTS)
    expired_events = _count_files(EXPIRED_EVENTS, recursive=True)

    has_delta = bool(
        new_change
        or new_audit
        or locks
        or pending_events >= 50  # threshold warn
    )

    report = {
        "has_delta": has_delta,
        "new_change_records": new_change,
        "new_audit_rows": len(new_audit),
        "new_l5_decisions_pushed": pushed,
        "new_l5_deduped": deduped,
        "new_rejected_schema": rejected,
        "outstanding_locks": [
            {
                "target_file": lk.get("target_file"),
                "severity": lk.get("severity"),
                "pushed_at": lk.get("pushed_at"),
                "rule_hits": lk.get("rule_hits", []),
            }
            for lk in locks
        ],
        "pending_events": pending_events,
        "expired_events_all_time": expired_events,
    }

    # Advance cursor
    new_cursor = {
        "change_log_count": len(change_rows),
        "audit_rows": len(audit_rows),
    }
    _save_cursor(new_cursor)

    return report


def render_text(report: Dict[str, Any]) -> str:
    if not report["has_delta"]:
        return ""
    lines: List[str] = [t("report.header")]
    if report["new_change_records"]:
        lines.append(t("report.new_changes", n=report["new_change_records"]))
    if report["new_l5_decisions_pushed"]:
        lines.append(t("report.l5_pushed", n=report["new_l5_decisions_pushed"]))
    if report["new_l5_deduped"]:
        lines.append(t("report.l5_deduped", n=report["new_l5_deduped"]))
    if report["new_rejected_schema"]:
        lines.append(t("report.rejected_schema", n=report["new_rejected_schema"]))
    if report["outstanding_locks"]:
        lines.append(t("report.locks_header", n=len(report["outstanding_locks"])))
        for lk in report["outstanding_locks"]:
            rules = ", ".join(lk.get("rule_hits") or []) or t("report.no_rules")
            lines.append(f"      - {lk['target_file']} [{lk['severity']}] {rules}")
        lines.append(t("report.locks_hint"))
    if report["pending_events"] >= 50:
        lines.append(t("report.pending_backlog", n=report["pending_events"]))
    return "\n".join(lines)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="No.0 hourly conditional report")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text")
    parser.add_argument("--reset", action="store_true", help="Reset cursor to zero")
    args = parser.parse_args(argv)

    report = build_report(reset=args.reset)

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    text = render_text(report)
    if text:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
