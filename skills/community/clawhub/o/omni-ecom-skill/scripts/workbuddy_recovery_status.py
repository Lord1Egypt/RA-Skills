#!/usr/bin/env python3
"""Read actual native launch IDs and return files; never launch or change run state."""
import argparse
import json
import os
import re
from pathlib import Path
from wait_for_agent_returns import read_return


def inspect(run_dir: Path, home: Path | None = None) -> dict:
    run_dir = run_dir.resolve()
    root = home or Path.home()
    config_root=Path(os.environ.get('CODEBUDDY_CONFIG_DIR')) if home is None and os.environ.get('CODEBUDDY_CONFIG_DIR') else root/'.codebuddy'
    bootstrap = json.loads((run_dir / "team-bootstrap.json").read_text(encoding="utf-8-sig"))
    team = json.loads((config_root / "teams" / bootstrap["team_name"] / "config.json").read_text(encoding="utf-8-sig"))
    if team.get("name") != bootstrap["team_name"]:
        raise ValueError("recovery_team_mismatch")
    session = team.get("leadSessionId", "")
    if not re.fullmatch(r"[0-9a-fA-F-]{36}", session):
        raise ValueError("recovery_session_invalid")
    traces = list((config_root / "projects").glob(f"*/{session}.jsonl"))
    if len(traces) != 1:
        raise ValueError("recovery_native_trace_missing_or_ambiguous")
    calls = {}; launches = {}
    for line in traces[0].read_text(encoding="utf-8").splitlines():
        if not line.strip(): continue
        event = json.loads(line)
        if event.get("name") != "Agent": continue
        if event.get("type") == "function_call":
            args = event.get("arguments", {})
            if isinstance(args, str): args = json.loads(args)
            if args.get("team_name") == bootstrap["team_name"]:
                calls[event.get("callId")] = args
        elif event.get("type") == "function_call_result" and event.get("callId") in calls:
            args = calls[event["callId"]]
            text = json.dumps(event.get("output"), ensure_ascii=False)
            match = re.search(r"task_id:\s*(agent-[A-Za-z0-9_-]+)", text)
            if "Spawned successfully" in text and match:
                role = str(args.get("subagent_type", "")).split(":")[-1]
                launches.setdefault(role, []).append(match.group(1))
    roles = ("data-analyst", "platform-ops", "content-live-growth", "ad-profit-optimizer")
    returns = {}
    for role in roles:
        path = run_dir / "agent-returns" / role / "a1.return.json"
        ok, reason, _ = read_return(path, bootstrap["run_id"], role, "member", True)
        returns[role] = {"valid_return_file": ok, "return_state": reason, "native_task_ids": launches.get(role, [])}
    return {"status": "read_only_recovery_observation", "run_id": bootstrap["run_id"], "team_name": bootstrap["team_name"], "session_id": session, "native_trace": str(traces[0]), "members": returns, "review_native_task_ids": launches.get("delivery-review", []), "duplicate_native_launches": {role: ids for role, ids in launches.items() if len(ids) > 1}, "instruction": "Use these exact original task IDs to query the native host. A return file alone does not prove host completion. Wait timeout never authorizes duplicate dispatch. If interrupted, confirm native resumability before resuming the original ID; otherwise report the unresolved state."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True); parser.add_argument("--output")
    args = parser.parse_args()
    payload = json.dumps(inspect(Path(args.run_dir)), ensure_ascii=False, indent=2)
    if args.output:
        output = Path(args.output).resolve()
        if output.is_relative_to(Path(args.run_dir).resolve()):
            raise ValueError("recovery_snapshot_must_not_replace_run_evidence")
        output.write_text(payload + "\n", encoding="utf-8")
    print(payload)


if __name__ == "__main__": main()
