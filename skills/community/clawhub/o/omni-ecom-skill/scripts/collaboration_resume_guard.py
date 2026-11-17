#!/usr/bin/env python3
"""Classify a partially completed run before any continuation is attempted."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from artifact_contract import validate_team_bootstrap_identity


DEFAULT_AGENTS = ("data-analyst", "platform-ops", "content-live-growth", "ad-profit-optimizer")


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def contains_any(root: Path, names: tuple[str, ...]) -> list[Path]:
    found: list[Path] = []
    for name in names:
        candidate = root / name
        if candidate.is_file():
            found.append(candidate)
    return found


def classify(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).expanduser().resolve()
    if not run_dir.is_dir():
        print(json.dumps({"status": "resume_blocked", "reason": "run_dir_missing"}, ensure_ascii=False))
        return 2
    bootstrap = run_dir / "team-bootstrap.json"
    if not bootstrap.is_file():
        print(json.dumps({"status": "resume_blocked", "reason": "team_bootstrap_missing", "phase": "bootstrap"}, ensure_ascii=False))
        return 2
    try:
        bootstrap_payload = read_json(bootstrap)
    except (OSError, json.JSONDecodeError):
        print(json.dumps({"status": "resume_blocked", "reason": "team_bootstrap_invalid", "phase": "bootstrap"}, ensure_ascii=False))
        return 2
    errors: list[str] = []
    try:
        validate_team_bootstrap_identity(bootstrap_payload,args.team_version,args.run_id,args.client_scope)
    except ValueError as exc:
        errors.append(str(exc))
    if bootstrap_payload.get("status") != "team_created":
        errors.append("team_bootstrap_not_verified")

    returns: dict[str, Path] = {}
    for path in run_dir.rglob("*.return.json"):
        try:
            payload = read_json(path)
        except (OSError, json.JSONDecodeError):
            continue
        agent_id = str(payload.get("agent_id", ""))
        if agent_id in args.expected_agents and payload.get("run_id") == args.run_id and payload.get("return_status") == "completed":
            if agent_id in returns:
                errors.append(f"duplicate_return:{agent_id}")
            returns[agent_id] = path

    sealed_agents: set[str] = set()
    for path in run_dir.rglob("*.sealed.json"):
        try:
            payload = read_json(path)
        except (OSError, json.JSONDecodeError):
            continue
        agent_id = str(payload.get("agent_id", ""))
        if agent_id in args.expected_agents and payload.get("run_id") == args.run_id:
            sealed_agents.add(agent_id)

    missing_returns = [agent for agent in args.expected_agents if agent not in returns]
    missing_sealed = [agent for agent in args.expected_agents if agent not in sealed_agents]
    report_files = contains_any(run_dir, ("report/report.json", "report.json"))
    pdf_files = contains_any(run_dir, ("report/report.pdf", "report.pdf"))
    pdf_receipts = contains_any(run_dir, ("report/pdf-delivery.json", "pdf-delivery.json"))
    manifest = contains_any(run_dir, ("review-manifest.json", "report/review-manifest.json"))
    completion = contains_any(run_dir, ("completion-receipt.json", "report/completion-receipt.json"))
    formal_complete = False
    for path in completion:
        try:
            if read_json(path).get("status") == "formal_delivery_complete":
                formal_complete = True
        except (OSError, json.JSONDecodeError):
            errors.append("completion_receipt_invalid")

    if errors:
        result = {"status": "resume_blocked", "reason": ";".join(errors), "phase": "integrity"}
        print(json.dumps(result, ensure_ascii=False))
        return 2
    if formal_complete:
        phase = "complete"
    elif manifest and pdf_files and pdf_receipts:
        phase = "review_pending"
    elif len(missing_returns) == 0 and len(missing_sealed) == 0:
        phase = "report_pending"
    elif returns:
        phase = "member_returns_pending"
    else:
        phase = "team_or_member_returns_pending"
    result = {
        "status": "resume_ready" if phase != "team_or_member_returns_pending" else "resume_waiting",
        "phase": phase,
        "run_id": args.run_id,
        "team_name": bootstrap_payload.get("team_name"),
        "completed_returns": sorted(returns),
        "missing_returns": missing_returns,
        "sealed_agents": sorted(sealed_agents),
        "missing_sealed": missing_sealed,
        "report_files": [path.name for path in report_files],
        "pdf_files": [path.name for path in pdf_files],
        "manifest_files": [path.name for path in manifest],
        "completion_files": [path.name for path in completion],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if phase in {"report_pending", "review_pending", "complete"} else 2


def main() -> int:
    parser = argparse.ArgumentParser(description="在续跑前判断已有专家团运行处于哪一阶段")
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--team-version", required=True)
    parser.add_argument("--client-scope", required=True)
    parser.add_argument("--expected-agents", default=",".join(DEFAULT_AGENTS))
    args = parser.parse_args()
    args.expected_agents = tuple(item.strip() for item in args.expected_agents.split(",") if item.strip())
    return classify(args)


if __name__ == "__main__":
    sys.exit(main())
