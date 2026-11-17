#!/usr/bin/env python3
"""Create a race-safe immutable handoff bound to one real Agent task."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--handoff", required=True)
    parser.add_argument("--return-file", required=True)
    parser.add_argument("--agent-task-id", required=True)
    parser.add_argument("--attempt-id", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    handoff_path = Path(args.handoff).resolve()
    return_path = Path(args.return_file).resolve()
    output_path = Path(args.output).resolve()
    if output_path.exists():
        raise ValueError("sealed_handoff_already_exists")
    if not args.agent_task_id.startswith("agent-"):
        raise ValueError("invalid_agent_task_id")
    if not args.attempt_id.strip():
        raise ValueError("invalid_attempt_id")

    handoff = read_json(handoff_path)
    receipt = read_json(return_path)
    digest = sha256(handoff_path)
    if receipt.get("return_status") != "completed":
        raise ValueError("agent_return_incomplete")
    if receipt.get("run_id") != handoff.get("run_id") or receipt.get("agent_id") != handoff.get("agent_id"):
        raise ValueError("handoff_return_identity_mismatch")
    if receipt.get("handoff_sha256") != digest:
        raise ValueError("handoff_return_sha256_mismatch")

    sealed = dict(handoff)
    sealed.update({
        "agent_task_id": args.agent_task_id,
        "agent_attempt_id": args.attempt_id,
        "agent_return_status": "completed",
        "agent_returned_at": receipt.get("returned_at"),
        "agent_return_file": return_path.name,
        "agent_return_sha256": sha256(return_path),
        "raw_handoff_file": handoff_path.name,
        "raw_handoff_sha256": digest,
        "sealed_at": datetime.now(timezone.utc).isoformat(),
    })
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(sealed, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": "sealed_handoff_created",
        "agent_id": sealed.get("agent_id"),
        "agent_task_id": args.agent_task_id,
        "attempt_id": args.attempt_id,
        "output": str(output_path),
        "sha256": sha256(output_path),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
