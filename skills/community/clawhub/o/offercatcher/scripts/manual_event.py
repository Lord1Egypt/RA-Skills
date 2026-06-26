#!/usr/bin/env python3
"""
OfferCatcher - 手动记录事件
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
REMINDERS_SCRIPT = REPO_ROOT / "scripts" / "apple_reminders_bridge.py"
STATE_PATH = Path.home() / ".openclaw" / "workspace" / "memory" / "offercatcher-state.json"
DEFAULT_LIST = os.environ.get("OFFERCATCHER_MANUAL_LIST", "OfferCatcher")
DEFAULT_ACCOUNT = os.environ.get("OFFERCATCHER_MANUAL_ACCOUNT", "iCloud")


def run_bridge(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(REMINDERS_SCRIPT), *cmd],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def format_due(value: str) -> str:
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S"):
        try:
            parsed = dt.datetime.strptime(value, fmt)
            return parsed.strftime("%Y-%m-%d %H:%M:%S" if fmt.endswith("%S") else "%Y-%m-%d %H:%M")
        except ValueError:
            continue
    raise SystemExit("unsupported --due format, use YYYY-MM-DD HH:MM or YYYY-MM-DD HH:MM:SS")


def parse_bridge_row(output: str) -> dict[str, str]:
    parts = output.strip().split("\t")
    return {
        "id": parts[0] if parts else "",
        "list": parts[1] if len(parts) > 1 else "",
        "title": parts[2] if len(parts) > 2 else "",
    }


def stable_hash(payload: dict[str, str]) -> str:
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:16]


def load_state(path: Path) -> dict:
    if not path.exists():
        return {
            "schemaVersion": 2,
            "list": DEFAULT_LIST,
            "account": DEFAULT_ACCOUNT,
            "source": "manual_event",
            "processed": {},
            "review": [],
        }
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    data.setdefault("processed", {})
    data.setdefault("review", [])
    data.setdefault("list", DEFAULT_LIST)
    data.setdefault("account", DEFAULT_ACCOUNT)
    return data


def write_state(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_manual_entry(args: argparse.Namespace, reminder: dict[str, str]) -> tuple[str, dict]:
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    due = format_due(args.due) if args.due else ""
    timing = {"type": "scheduled_start", "start": due} if due else {"type": "unknown", "observedAt": now}
    note = args.notes
    entry = {
        "eventId": "",
        "status": "active",
        "identityKey": stable_hash({"title": args.title, "due": due, "notes": note}),
        "sourceFamily": "manual",
        "company": "手动记录",
        "eventType": "manual_note",
        "role": "",
        "title": args.title,
        "note": note,
        "timing": timing,
        "links": [],
        "mainReminder": {
            "title": args.title,
            "due": due,
            "priority": args.priority,
        },
        "firstSeenAt": now,
        "updatedAt": now,
        "expiredAt": None,
        "cancelledAt": None,
        "reminder": {
            "id": reminder.get("id", ""),
            "list": args.list,
            "account": args.account,
            "lastSyncedFingerprint": "",
            "syncedAt": now,
        },
        "source": {
            "threadIds": [f"manual:{now}"],
            "subject": args.title,
            "subjects": [args.title],
            "sender": "manual",
            "lastSeenAt": now,
        },
    }
    entry["fingerprint"] = stable_hash(
        {
            "status": entry["status"],
            "title": entry["title"],
            "note": entry["note"],
            "timing": json.dumps(entry["timing"], ensure_ascii=False, sort_keys=True),
            "due": due,
        }
    )
    event_id = stable_hash({"title": args.title, "due": due, "createdAt": now, "kind": "manual"})
    entry["eventId"] = event_id
    entry["reminder"]["lastSyncedFingerprint"] = entry["fingerprint"]
    return event_id, entry


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a manual reminder event for Offer Radar")
    parser.add_argument("--title", required=True)
    parser.add_argument("--due")
    parser.add_argument("--notes", default="")
    parser.add_argument("--priority", default="high", choices=("none", "low", "medium", "high"))
    parser.add_argument("--list", default=DEFAULT_LIST)
    parser.add_argument("--account", default=DEFAULT_ACCOUNT)
    parser.add_argument("--output", default=str(STATE_PATH))
    args = parser.parse_args()

    cmd = [
        "add",
        "--title",
        args.title,
        "--list",
        args.list,
        "--account",
        args.account,
        "--priority",
        args.priority,
        "--notes",
        args.notes,
    ]
    if args.due:
        cmd.extend(["--due", format_due(args.due)])

    proc = run_bridge(cmd)
    if proc.returncode != 0:
        raise SystemExit(proc.stderr.strip() or proc.stdout.strip() or "create reminder failed")

    payload = parse_bridge_row(proc.stdout.strip())
    payload["due"] = args.due or ""
    payload["notes"] = args.notes
    payload["priority"] = args.priority
    output = Path(args.output).expanduser()
    state = load_state(output)
    event_id, entry = build_manual_entry(args, payload)
    state["processed"][event_id] = entry
    if state.get("source") and state.get("source") != "manual_event":
        state["source"] = "multi_source"
    else:
        state["source"] = "manual_event"
    write_state(output, state)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
