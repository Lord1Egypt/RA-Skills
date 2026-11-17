#!/usr/bin/env python3
"""Reserve a native launch before execution; reservations are NOT host evidence.

Only omni-ecom team calls are in scope. No model names or automatic retries.
Reservations share the run database but never count as member_started/returned.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from run_journal import Journal, ROLES, utc_now


def reserve(event: dict) -> str:
    if event.get("tool_name") not in {"Agent", "Task"}:
        return "unrelated"
    args = event.get("tool_input", {})
    prompt = str(args.get("prompt", ""))
    scoped = (str(args.get("team_name", "")).startswith("omni-ecom-")
              or str(args.get("subagent_type", "")).startswith("omni-ecom:")
              or ("omni-ecom" in prompt and "task-cards" in prompt))
    if not scoped:
        return "unrelated"
    normalized = prompt.replace("\\", "/")
    normalized = re.sub(r"/+", "/", normalized)
    paths = re.findall(r"[A-Za-z]:/[^\n\r\"<>]*?\.json|(?<![A-Za-z:])/(?:[^\n\r\"<>]*?/)?task-cards/[^\n\r\"<>]*?\.json", normalized)
    cards = [Path(p).resolve() for p in paths if "/task-cards/" in p and Path(p).is_file()]
    if len(cards) != 1:
        raise ValueError("dispatch_requires_one_existing_task_card")
    path = cards[0]
    card = json.loads(path.read_text(encoding="utf-8-sig"))
    root = next((p.parent for p in path.parents if p.name == "task-cards"), None)
    if root is None:
        raise ValueError("dispatch_card_outside_run")
    bootstrap = json.loads((root / "team-bootstrap.json").read_text(encoding="utf-8-sig"))
    for key in ("run_id", "client_scope", "team_version", "host"):
        if not card.get(key) or card[key] != bootstrap.get(key):
            raise ValueError("dispatch_card_identity_mismatch:" + key)
    if card["host"] != "workbuddy" or args.get("team_name") != bootstrap.get("team_name"):
        raise ValueError("dispatch_team_mismatch")
    role = card.get("agent_id")
    subtype = str(args.get("subagent_type", "")).split(":")[-1]
    if role not in ROLES or subtype != role:
        raise ValueError("dispatch_role_mismatch")
    attempt = card.get("attempt_id", "")
    valid_attempt = bool(re.fullmatch(r"delivery-review-r[1-9][0-9]*-a[12]", attempt)) if role == "delivery-review" else attempt in {"a1", "a2"}
    if not valid_attempt:
        raise ValueError("dispatch_attempt_invalid")
    journal = Journal(root / "run-journal.sqlite", existing_only=True)
    try:
        with journal.transaction():
            rows = journal.events(card["run_id"], card["client_scope"])
            identity = journal.db.execute("SELECT team_version FROM runs WHERE run_id=?", (card["run_id"],)).fetchone()
            if identity[0] != card["team_version"]:
                raise ValueError("dispatch_journal_version_mismatch")
            members = [r for r in rows if r["payload"].get("role") == role]
            if any(r["kind"] == "member_returned" for r in members):
                raise ValueError("dispatch_member_already_returned")
            started = [r for r in members if r["kind"] == "member_started"]
            terminal = {r["payload"]["attempt_id"] for r in members if r["kind"] in {"member_failed", "member_rejected"}}
            if any(r["payload"]["attempt_id"] not in terminal for r in started):
                raise ValueError("dispatch_member_still_running")
            if attempt.endswith("a2") and attempt[:-1] + "1" not in terminal:
                raise ValueError("dispatch_retry_requires_recorded_terminal_failure")
            journal.db.execute("CREATE TABLE IF NOT EXISTS dispatch_reservations (run_id TEXT, role TEXT, attempt_id TEXT, card_path TEXT, session_id TEXT, reserved_at TEXT, PRIMARY KEY(run_id,role,attempt_id))")
            existing = journal.db.execute("SELECT 1 FROM dispatch_reservations WHERE run_id=? AND role=? AND attempt_id=?", (card["run_id"], role, attempt)).fetchone()
            if existing or any(r["payload"]["attempt_id"] == attempt for r in started):
                raise ValueError("dispatch_duplicate_blocked: wait for the original task; do not rename or relaunch it")
            journal.db.execute("INSERT INTO dispatch_reservations VALUES (?,?,?,?,?,?)", (card["run_id"], role, attempt, str(path), str(event.get("session_id", "")), utc_now()))
    finally:
        journal.close()
    return "reserved_not_started"


def main() -> int:
    try:
        reserve(json.load(sys.stdin))
        return 0  # Do not bypass the host's normal permission system.
    except Exception as exc:
        print("omni-ecom dispatch blocked: " + str(exc))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
