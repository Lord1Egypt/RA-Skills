#!/usr/bin/env python3
"""Create an immutable delivery-review return receipt from the reviewed result."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from review_guard import validate_manifest, validate_review_result


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task-card", required=True)
    args = parser.parse_args()
    card = load(Path(args.task_card).resolve())
    raw_path = Path(card["raw_review_result"]).resolve()
    return_path = Path(card["return_file"]).resolve()
    manifest_path = Path(card["manifest"]).resolve()
    if return_path.exists():
        raise ValueError("delivery_review_return_conflict")
    if card.get('review_analysis_file') and Path(card['review_analysis_file']).is_file():
        import copy
        analysis=load(Path(card['review_analysis_file']))
        allowed={'review_status','findings','required_changes','contribution_summary'}
        if not isinstance(analysis,dict) or set(analysis)!=allowed:
            raise ValueError('review_analysis_fields_invalid')
        raw=copy.deepcopy(card['raw_review_result_template'])
        raw.update(analysis)
        raw['returned_at']=datetime.now(timezone.utc).isoformat()
        # Validate before publishing a raw result. No default PASS or changed
        # manifest can ever turn the reviewer's own result into an approval.
        frozen=load(manifest_path)
        validate_manifest(frozen)
        from review_guard import changed_entries
        if any(changed_entries(frozen)) or frozen['manifest_sha256']!=card['manifest_sha256']:
            raise ValueError('review_frozen_files_changed')
        validate_review_result(raw,frozen)
        raw_path.parent.mkdir(parents=True,exist_ok=True)
        with raw_path.open('x',encoding='utf-8') as stream:
            json.dump(raw,stream,ensure_ascii=False,indent=2)
    raw = load(raw_path)
    manifest = load(manifest_path)
    if raw.get("agent_version") != card.get("team_version"):
        raise ValueError("delivery_review_agent_version_mismatch")
    if raw.get("client_scope") != card.get("client_scope"):
        raise ValueError("delivery_review_client_scope_mismatch")
    validate_manifest(manifest)
    validate_review_result(raw, manifest)
    if raw.get("run_id") != card.get("run_id") or raw.get("agent_id") != "delivery-review":
        raise ValueError("delivery_review_identity_mismatch")
    if raw.get("review_attempt_id") != card.get("attempt_id") or raw.get("report_revision") != card.get("report_revision"):
        raise ValueError("delivery_review_attempt_mismatch")
    digest = hashlib.sha256(raw_path.read_bytes()).hexdigest()
    receipt = {
        "run_id": card["run_id"],
        "agent_id": "delivery-review",
        "attempt_id": card["attempt_id"],
        "review_attempt_id": raw["review_attempt_id"],
        "report_revision": raw["report_revision"],
        "return_status": "completed",
        "returned_at": datetime.now(timezone.utc).isoformat(),
        "review_status": raw["review_status"],
        "reviewed_manifest_sha256": raw["reviewed_manifest_sha256"],
        "reviewed_artifacts": raw["reviewed_artifacts"],
        "contribution_summary": raw["contribution_summary"],
        "response": {"review_status": raw["review_status"], "required_changes": raw.get("required_changes", [])},
        "handoff_sha256": digest,
    }
    return_path.parent.mkdir(parents=True, exist_ok=True)
    with return_path.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")
    from return_communication import communication
    print(json.dumps({"status": "delivery_review_return_ready", "return_file": str(return_path), "handoff_sha256": digest,
                      **communication(card,receipt,return_path)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
