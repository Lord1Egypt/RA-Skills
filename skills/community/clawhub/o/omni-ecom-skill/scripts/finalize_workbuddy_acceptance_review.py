#!/usr/bin/env python3
"""Bind one real native-host reviewer and finish the candidate-only acceptance chain."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from host_runtime import Runtime


def write_new(path: Path, payload: dict) -> None:
    if path.exists(): raise ValueError(f"review_finalize_conflict:{path.name}")
    path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run(command: list[str]) -> None:
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if result.returncode: raise ValueError("review_finalize_command_failed:" + (result.stdout + result.stderr)[-1200:])


def finalize(run_dir: Path, plugin_dir: Path, task_id: str, host: str = "workbuddy", attempt_number: int = 1) -> dict:
    run_dir = run_dir.resolve(); plugin_dir = plugin_dir.resolve()
    if host not in {"workbuddy", "codex"}: raise ValueError("review_host_invalid")
    pattern = r"agent-[0-9A-Za-z_-]+" if host == "workbuddy" else r"(?:[0-9A-Za-z][0-9A-Za-z_-]{2,127}|(?:/[0-9A-Za-z_-]+){2,8})"
    if not re.fullmatch(pattern, task_id): raise ValueError("review_task_id_invalid")
    identity_name = "team-bootstrap.json" if host == "workbuddy" else "host-orchestration-plan.json"
    if attempt_number not in (1, 2): raise ValueError("review_retry_exhausted")
    bootstrap = json.loads((run_dir / identity_name).read_text(encoding="utf-8-sig"))
    revision = json.loads((run_dir/'report.json').read_text(encoding='utf-8-sig'))['report_revision']
    attempt = f"delivery-review-{revision.lower()}-a{attempt_number}"
    if bootstrap.get("host") != host: raise ValueError("review_host_identity_mismatch")
    raw = run_dir / "review" / revision / f"{attempt}.return.json"; ret = run_dir / "agent-returns" / "delivery-review" / f"a{attempt_number}.return.json"
    if not raw.is_file() or not ret.is_file(): raise ValueError("delivery_review_return_missing")
    raw_payload = json.loads(raw.read_text(encoding="utf-8-sig"))
    if raw_payload.get("review_status") != "passed" or raw_payload.get("required_changes"):
        raise ValueError("candidate_review_not_passed")
    runtime = Runtime(run_dir, bootstrap["run_id"], bootstrap["client_scope"])
    try:
        stem = "delivery-review" if attempt_number == 1 else "delivery-review-a2"
        started = run_dir / "observations" / f"{stem}.started.json"; completed = run_dir / "observations" / f"{stem}.completed.json"
        common = {"run_id": bootstrap["run_id"], "client_scope": bootstrap["client_scope"], "host": host, "task_id": task_id, "evidence_kind": "native_host_task_id_observed_by_team_lead"}
        write_new(started, {**common, "state": "created", "observed_at": datetime.now(timezone.utc).isoformat()})
        runtime.start("delivery-review", host, task_id, attempt, str(started.relative_to(run_dir)), "review-manifest.json")
        write_new(completed, {**common, "state": "completed", "observed_at": datetime.now(timezone.utc).isoformat()})
        runtime.accept("delivery-review", host, task_id, attempt, str(raw.relative_to(run_dir)), str(ret.relative_to(run_dir)), str(completed.relative_to(run_dir)), "sealed/delivery-review.json")
    finally: runtime.close()
    scripts = plugin_dir / "scripts"; manifest = run_dir / "review-manifest.json"; attestation = run_dir / "review" / revision / f"{attempt}.attestation.json"; release = run_dir / "release-receipt.json"
    run([sys.executable, str(scripts / "review_guard.py"), "attest-result", "--manifest", str(manifest), "--review-result", str(raw), "--agent-task-id", task_id, "--review-attempt-id", attempt, "--output", str(attestation)])
    run([sys.executable, str(scripts / "review_guard.py"), "verify", "--manifest", str(manifest), "--attestation", str(attestation), "--receipt", str(release)])
    public = run_dir / "public-output-receipt.json"
    run([sys.executable, str(scripts / "public_output_guard.py"), "--file", str(run_dir / "report.json"), "--file", str(run_dir / "report.md"), "--file", str(run_dir / "report.pdf"), "--team-version", bootstrap["team_version"], "--output", str(public)])
    candidate_mode = "-candidate." in bootstrap["team_version"]
    completion = run_dir / ("candidate-acceptance-receipt.json" if candidate_mode else "completion-receipt.json")
    command = [sys.executable, str(scripts / "completion_gate.py"), "--report-dir", str(run_dir), "--public-guard-receipt", str(public), "--manifest", str(manifest), "--attestation", str(attestation), "--release-receipt", str(release), "--claim-receipt", str(run_dir / "claim-receipt.json"), "--output", str(completion)]
    if candidate_mode:
        command.append("--candidate-acceptance")
    run(command)
    completion_result = json.loads(completion.read_text(encoding="utf-8-sig"))
    completion_status = "candidate_pipeline_complete" if candidate_mode else "formal_delivery_complete"
    if completion_result.get("status") != completion_status:
        raise ValueError("acceptance_completion_status_mismatch")
    analysis_ids = json.loads((run_dir / "analysis-binding-receipt.json").read_text(encoding="utf-8-sig"))["task_ids"]
    all_ids = {**analysis_ids, "delivery-review": task_id}
    final_lines = [
        f"专家团版本：v{bootstrap['team_version']}",
        f"run_id：{bootstrap['run_id']}",
        f"team_name：{bootstrap['team_name']}" if host == "workbuddy" else "host：codex",
        f"状态：{completion_status}",
    ] + [f"{role}：{all_ids[role]}" for role in ("data-analyst", "platform-ops", "content-live-growth", "ad-profit-optimizer", "delivery-review")]
    result = {"status": completion_status, "run_id": bootstrap["run_id"], "host": host, "team_name": bootstrap.get("team_name"), "review_task_id": task_id, "agent_task_ids": all_ids, "required_final_summary": "\n".join(final_lines), "completion_receipt": str(completion)}
    if candidate_mode:
        result["candidate_receipt"] = str(completion)
    write_new(run_dir / "acceptance-finalize-receipt.json", result); return result


def main() -> int:
    p=argparse.ArgumentParser(description=__doc__); p.add_argument("--run-dir",required=True); p.add_argument("--plugin-dir",required=True); p.add_argument("--task-id",required=True); p.add_argument("--host",choices=("workbuddy","codex"),default="workbuddy")
    p.add_argument("--attempt-number", type=int, choices=(1, 2), default=1)
    a=p.parse_args(); print(json.dumps(finalize(Path(a.run_dir),Path(a.plugin_dir),a.task_id,a.host,a.attempt_number),ensure_ascii=False)); return 0


if __name__ == "__main__": raise SystemExit(main())
