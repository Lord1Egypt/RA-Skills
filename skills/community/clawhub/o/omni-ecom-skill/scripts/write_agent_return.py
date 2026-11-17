#!/usr/bin/env python3
"""Create an immutable member return receipt from its task card and raw handoff."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task-card", required=True)
    args = parser.parse_args()
    card_path = Path(args.task_card).resolve()
    card = load(card_path)
    paths = card.get("paths", {})
    raw_path = Path(paths.get("raw_handoff", "")).resolve()
    return_path = Path(paths.get("return_file", "")).resolve()
    if return_path.exists():
        raise ValueError("member_return_conflict")
    if not raw_path.is_file():
        raise ValueError("raw_handoff_missing")
    raw = load(raw_path)
    if card.get('analysis_question_contract'):
        from role_analysis_contract import check_questions
        depth=raw.get('analysis_depth',{})
        if depth.get('question_contract')!=card['analysis_question_contract']:
            raise ValueError('minimum_analysis_contract_mismatch')
        check_questions(card['agent_id'],depth)
    if any(raw.get(key) != card.get(key) for key in ("run_id", "agent_id", "attempt_id")):
        raise ValueError("raw_handoff_task_card_mismatch")
    if raw.get("client_scope") != card.get("client_scope") or raw.get("agent_version") != card.get("team_version"):
        raise ValueError("raw_handoff_scope_or_version_mismatch")
    validator_root = Path(paths.get("validate_handoff", "")).resolve().parent
    sys.path.insert(0, str(validator_root))
    from validate_handoff import validate
    errors = validate(raw)
    if errors:
        raise ValueError("raw_handoff_contract_invalid:" + ",".join(errors))
    digest = hashlib.sha256(raw_path.read_bytes()).hexdigest()
    summary = str(raw.get("contribution_summary") or "").strip()
    if not summary:
        raise ValueError("contribution_summary_missing")
    receipt = {
        "run_id": card["run_id"],
        "agent_id": card["agent_id"],
        "attempt_id": card["attempt_id"],
        "return_status": "completed",
        "returned_at": datetime.now(timezone.utc).isoformat(),
        "contribution_summary": summary,
        "response": {"status": "completed", "raw_handoff": raw_path.name, "gate_status": raw.get("gate_status"), "handoff_status": raw.get("status")},
        "handoff_sha256": digest,
    }
    return_path.parent.mkdir(parents=True, exist_ok=True)
    with return_path.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")
    from return_communication import communication
    print(json.dumps({"status": "member_return_ready", "return_file": str(return_path), "handoff_sha256": digest,
                      **communication(card,receipt,return_path)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
