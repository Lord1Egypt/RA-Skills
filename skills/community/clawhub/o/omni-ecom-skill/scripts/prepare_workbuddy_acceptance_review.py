#!/usr/bin/env python3
"""Freeze the acceptance report and create one native-host delivery-review task card."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from artifact_contract import native_receipt_identity
from run_journal import Journal
from review_guard import validate_manifest, changed_entries


def prepare(run_dir: Path, plugin_dir: Path, host: str = "workbuddy", attempt_number: int = 1) -> dict:
    run_dir = run_dir.resolve(); plugin_dir = plugin_dir.resolve()
    if host not in {"workbuddy", "codex"}: raise ValueError("review_host_invalid")
    identity_name = "team-bootstrap.json" if host == "workbuddy" else "host-orchestration-plan.json"
    bootstrap = json.loads((run_dir / identity_name).read_text(encoding="utf-8-sig"))
    if bootstrap.get("host") != host: raise ValueError("review_host_identity_mismatch")
    manifest = run_dir / "review-manifest.json"
    revision = json.loads((run_dir/'report.json').read_text(encoding='utf-8-sig'))['report_revision']
    if attempt_number not in (1, 2): raise ValueError("review_retry_exhausted")
    if manifest.exists() and attempt_number == 1:
        raise ValueError("review_manifest_already_exists")
    if attempt_number == 2:
        journal = Journal(run_dir / "run-journal.sqlite", read_only=True)
        try:
            events = journal.events(bootstrap["run_id"], bootstrap["client_scope"])
        finally: journal.close()
        reviews = [e for e in events if e["payload"].get("role") == "delivery-review" and e["kind"].startswith("member_")]
        if not reviews or reviews[-1]["kind"] not in ("member_failed", "member_rejected") or reviews[-1]["payload"].get("attempt_id") != "delivery-review-r1-a1":
            raise ValueError("review_retry_requires_terminal_a1")
        if manifest.exists():
            payload = json.loads(manifest.read_text(encoding="utf-8-sig"))
            validate_manifest(payload)
            if any(changed_entries(payload)): raise ValueError("review_frozen_files_changed")
            if payload.get('report_revision')!=revision:raise ValueError('review_new_revision_requires_new_directory')
    artifacts = ["report.md", "report.json", "report.pdf", "pdf-delivery.json", "depth-guard.json", "conflict-scan.json"]
    sources = ["team-lead-handoff.json", *[f"sealed/{role}-a1.json" for role in ("data-analyst", "platform-ops", "content-live-growth", "ad-profit-optimizer")]]
    command = [sys.executable, str(plugin_dir / "scripts" / "review_guard.py"), "prepare", "--run-id", bootstrap["run_id"], "--client-scope", bootstrap["client_scope"], "--team-version", bootstrap["team_version"], "--report-revision", revision]
    for name in artifacts:
        command.extend(["--artifact", str(run_dir / name)])
    for name in sources:
        command.extend(["--source", str(run_dir / name)])
    command.extend(["--output", str(manifest)])
    if not manifest.exists():
        completed = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if completed.returncode:
            raise ValueError("review_manifest_prepare_failed:" + (completed.stdout + completed.stderr)[-1000:])
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    attempt = f"delivery-review-{revision.lower()}-a{attempt_number}"
    raw_result = run_dir / "review" / revision / f"{attempt}.return.json"
    latch = run_dir / "agent-returns" / "delivery-review" / f"a{attempt_number}.return.json"
    card_path = run_dir / "task-cards" / "review" / f"{attempt}.json"
    if any(p.exists() for p in (latch, card_path, raw_result)): raise ValueError("review_attempt_already_exists")
    card_path.parent.mkdir(parents=True, exist_ok=True)
    card = {
        "schema_version": "2.0", "artifact_type": "delivery_review_task_card", "immutable_after_launch": True,
        "run_id": bootstrap["run_id"], "client_scope": bootstrap["client_scope"], "team_version": bootstrap["team_version"], "host": host,
        "agent_id": "delivery-review", "attempt_id": attempt, "report_revision": revision,
        "raw_result_identity": {
            **native_receipt_identity("review_result", bootstrap["team_version"]),
            "run_id": bootstrap["run_id"], "client_scope": bootstrap["client_scope"],
            "agent_id": "delivery-review", "agent_version": bootstrap["team_version"],
            "review_attempt_id": attempt, "report_revision": revision,
        },
        "raw_result_schema": str(plugin_dir / "schemas" / "review-result.schema.json"),
        "manifest": str(manifest), "manifest_sha256": payload["manifest_sha256"], "raw_review_result": str(raw_result), "return_file": str(latch),
        "return_command": f'python -B "{plugin_dir / "scripts" / "write_delivery_review_return.py"}" --task-card "{card_path}"',
        "required_result": {"review_status": "passed_or_conditional_pass_or_rejected", "send_message_recipient": "team-lead", "send_message_count": 1, "return_fields": ["run_id", "agent_id", "attempt_id", "review_attempt_id", "report_revision", "return_status", "returned_at", "review_status", "reviewed_manifest_sha256", "reviewed_artifacts", "contribution_summary", "response", "handoff_sha256"]},
        "rules": ["独立复核 manifest 中全部冻结文件，不得修改任何报告或来源", "raw review result 必须使用 omni-ecom.review-result@2.0 且 reviewed_manifest_sha256 与卡片一致", "写完 raw review result 后必须原样执行 return_command 一次；禁止手写、补写或覆盖 return_file", "review_status 只能为 passed、conditional_pass 或 rejected；候选验收只有 passed 且 required_changes 为空才可完成", "return_command 成功后只向 team-lead 回传一次并结束"],
    }
    card['input_verification_command'] = f'python -B "{plugin_dir / "scripts" / "check_review_inputs.py"}" --task-card "{card_path}"'
    from review_task_card import add_format
    add_format(card,payload,plugin_dir)
    card_path.write_text(json.dumps(card, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    review_return_dir = (run_dir / "agent-returns").as_posix()
    result = {"status": "delivery_review_ready", "run_id": bootstrap["run_id"], "host": host, "review_attempt_id": attempt, "card_path": str(card_path), "launch_prompt": f"读取并严格执行复核任务卡：{card_path}。独立复核冻结报告，只向 team-lead 回传一次，然后结束。", "wait_command": f'python -B "{plugin_dir / "scripts" / "wait_for_agent_returns.py"}" --return-dir "{review_return_dir}" --run-id {bootstrap["run_id"]} --expected delivery-review --contract delivery_review --return-file delivery-review=delivery-review/a1.return.json --timeout 600', "finalize_command_template": f'python -B "{plugin_dir / "scripts" / "finalize_workbuddy_acceptance_review.py"}" --run-dir "{run_dir}" --plugin-dir "{plugin_dir}" --host {host} --task-id <真实review_task_id>'}
    if host=='workbuddy':
        result['dispatch_parameters']={'team_name':bootstrap['team_name'],'name':'delivery-review',
            'subagent_type':'delivery-review','prompt':result['launch_prompt']}
    if attempt_number == 2:
        result["wait_command"] = result["wait_command"].replace("delivery-review/a1.return.json", "delivery-review/a2.return.json")
        result["finalize_command_template"] += " --attempt-number 2"
    launch_name = "review-launch-manifest.json" if attempt_number == 1 else "review-launch-manifest-a2.json"
    (run_dir / launch_name).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--run-dir", required=True); parser.add_argument("--plugin-dir", required=True); parser.add_argument("--host", choices=("workbuddy", "codex"), default="workbuddy")
    parser.add_argument("--attempt-number", type=int, choices=(1, 2), default=1)
    args = parser.parse_args(); print(json.dumps(prepare(Path(args.run_dir), Path(args.plugin_dir), args.host, args.attempt_number), ensure_ascii=False)); return 0


if __name__ == "__main__":
    raise SystemExit(main())
