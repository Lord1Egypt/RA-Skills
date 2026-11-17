#!/usr/bin/env python3
"""Bind four real native-host task ids to completed a1 returns and prepare report inputs."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from host_runtime import ROLES, Runtime


TASK_ID = re.compile(r"^agent-[0-9A-Za-z_-]+$")
CODEX_TASK_ID = re.compile(r"^(?:[0-9A-Za-z][0-9A-Za-z_-]{2,127}|(?:/[0-9A-Za-z_-]+){2,8})$")


def write_new(path: Path, payload: dict) -> None:
    if path.exists():
        raise ValueError(f"analysis_binding_conflict:{path.name}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def replace_uncommitted_start(path: Path, run_id: str, client_scope: str, host: str) -> None:
    """Remove only a start observation left behind before the journal accepted any event."""
    if not path.exists():
        return
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    safe = (payload.get("run_id") == run_id and payload.get("client_scope") == client_scope
            and payload.get("host") == host and payload.get("state") == "created")
    if not safe:
        raise ValueError(f"analysis_binding_conflict:{path.name}")
    path.unlink()


def load_identity(run_dir: Path, host: str) -> dict:
    name = "team-bootstrap.json" if host == "workbuddy" else "host-orchestration-plan.json"
    payload = json.loads((run_dir / name).read_text(encoding="utf-8-sig"))
    if payload.get("host") != host:
        raise ValueError("analysis_host_identity_mismatch")
    return payload


def bind(run_dir: Path, mappings: list[str], host: str = "workbuddy") -> dict:
    run_dir = run_dir.resolve()
    if host not in {"workbuddy", "codex"}:
        raise ValueError("analysis_host_invalid")
    identity = load_identity(run_dir, host)
    run_id = identity["run_id"]; client_scope = identity["client_scope"]
    task_id_pattern = TASK_ID if host == "workbuddy" else CODEX_TASK_ID
    pairs = {}
    for item in mappings:
        role, sep, task_id = item.partition("=")
        if not sep or role not in ROLES or not task_id_pattern.fullmatch(task_id):
            raise ValueError("analysis_task_mapping_invalid")
        pairs[role] = task_id
    if set(pairs) != set(ROLES) or len(set(pairs.values())) != 4:
        raise ValueError("analysis_task_mapping_incomplete_or_duplicate")
    runtime = Runtime(run_dir, run_id, client_scope)
    sealed = {}
    try:
        if runtime.status()["events"]:
            raise ValueError("analysis_binding_already_started")
        for role in ROLES:
            task_id = pairs[role]
            raw = run_dir / "raw-handoffs" / f"handoff-{role}-a1.json"
            ret = run_dir / "agent-returns" / role / "a1.return.json"
            if not raw.is_file() or not ret.is_file():
                raise ValueError(f"analysis_return_missing:{role}")
            started = run_dir / "observations" / f"{role}.started.json"
            completed = run_dir / "observations" / f"{role}.completed.json"
            common = {"run_id": run_id, "client_scope": client_scope, "host": host, "task_id": task_id, "evidence_kind": "native_host_task_id_observed_by_team_lead"}
            replace_uncommitted_start(started, run_id, client_scope, host)
            write_new(started, {**common, "state": "created", "observed_at": datetime.now(timezone.utc).isoformat()})
            runtime.start(role, host, task_id, "a1", str(started.relative_to(run_dir)))
            write_new(completed, {**common, "state": "completed", "observed_at": datetime.now(timezone.utc).isoformat()})
            target = f"sealed/{role}-a1.json"
            runtime.accept(role, host, task_id, "a1", str(raw.relative_to(run_dir)), str(ret.relative_to(run_dir)), str(completed.relative_to(run_dir)), target)
            sealed[role] = target
        write_new(run_dir / "quality-inputs.json", {"run_id": run_id, "client_scope": client_scope, "report_revision": "R1", "inventory": "report-inventory.json", "chapter_plan": "chapter-plan.json", "baseline": "baseline-pack.json", "run_scope": "run-scope.json", "handoffs": sealed})
        result = {"status": "analysis_returns_bound", "run_id": run_id, "host": host, "task_ids": pairs, "sealed_handoffs": sealed}
        write_new(run_dir / "analysis-binding-receipt.json", result)
        return result
    finally:
        runtime.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--task", action="append", required=True)
    parser.add_argument("--host", choices=("workbuddy", "codex"), default="workbuddy")
    args = parser.parse_args()
    print(json.dumps(bind(Path(args.run_dir), args.task, args.host), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
