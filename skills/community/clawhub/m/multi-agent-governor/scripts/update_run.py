#!/usr/bin/env python3
from __future__ import annotations

import argparse

from _common import load_manifest, now_iso, path_record, save_json


FINAL_AGENT_STATUSES = {"completed", "errored", "closed", "cancelled"}


def main() -> None:
    parser = argparse.ArgumentParser(description="Update run agents, sessions, builds, and completion state.")
    parser.add_argument("action", choices=["agent-start", "agent-finish", "session-start", "session-finish", "build", "finish"])
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--lane-id")
    parser.add_argument("--thread-id")
    parser.add_argument("--nickname")
    parser.add_argument("--agent-status", choices=sorted(FINAL_AGENT_STATUSES))
    parser.add_argument("--session-id")
    parser.add_argument("--label")
    parser.add_argument("--exit-code", type=int)
    parser.add_argument("--artifact", action="append", default=[])
    parser.add_argument("--run-status", choices=["complete", "blocked"])
    args = parser.parse_args()

    manifest_path, manifest = load_manifest(args.manifest)

    if args.action == "agent-start":
        if not args.lane_id or not args.thread_id:
            parser.error("agent-start requires --lane-id and --thread-id")
        lane = next((lane for lane in manifest["lanes"] if lane["lane_id"] == args.lane_id), None)
        if not lane:
            parser.error(f"unknown lane: {args.lane_id}")
        if len(manifest["agents"]) >= manifest["limits"]["total_agents"]:
            parser.error("total agent limit reached")
        if any(agent["thread_id"] == args.thread_id for agent in manifest["agents"]):
            parser.error(f"agent already registered: {args.thread_id}")
        active_agents = [agent for agent in manifest["agents"] if agent["status"] == "running"]
        if len(active_agents) >= manifest["limits"]["max_concurrent"]:
            parser.error("concurrent agent limit reached")
        if lane["status"] != "planned":
            parser.error(f"lane is not available to start: {args.lane_id}")
        lane["status"] = "running"
        manifest["agents"].append({
            "lane_id": args.lane_id,
            "role": lane["role"],
            "thread_id": args.thread_id,
            "nickname": args.nickname,
            "status": "running",
            "started_at": now_iso(),
            "completed_at": None,
        })

    elif args.action == "agent-finish":
        if not args.thread_id or not args.agent_status:
            parser.error("agent-finish requires --thread-id and --agent-status")
        agent = next((agent for agent in manifest["agents"] if agent["thread_id"] == args.thread_id), None)
        if not agent:
            parser.error(f"unknown agent: {args.thread_id}")
        agent["status"] = args.agent_status
        agent["completed_at"] = now_iso()
        lane = next(lane for lane in manifest["lanes"] if lane["lane_id"] == agent["lane_id"])
        lane["status"] = args.agent_status

    elif args.action == "session-start":
        if not args.session_id or not args.label:
            parser.error("session-start requires --session-id and --label")
        if any(session["session_id"] == args.session_id for session in manifest["sessions"]):
            parser.error(f"session already registered: {args.session_id}")
        manifest["sessions"].append({
            "session_id": args.session_id,
            "label": args.label,
            "status": "running",
            "started_at": now_iso(),
            "completed_at": None,
            "exit_code": None,
        })

    elif args.action == "session-finish":
        if not args.session_id or args.exit_code is None:
            parser.error("session-finish requires --session-id and --exit-code")
        session = next((session for session in manifest["sessions"] if session["session_id"] == args.session_id), None)
        if not session:
            parser.error(f"unknown session: {args.session_id}")
        session["status"] = "completed" if args.exit_code == 0 else "errored"
        session["completed_at"] = now_iso()
        session["exit_code"] = args.exit_code

    elif args.action == "build":
        if not args.artifact:
            parser.error("build requires at least one --artifact")
        sequence = int(manifest["build"].get("sequence", 0)) + 1
        manifest["build"] = {
            "sequence": sequence,
            "id": f"{manifest['run_id']}-b{sequence:02d}",
            "artifacts": [path_record(value) for value in args.artifact],
            "created_at": now_iso(),
        }

    elif args.action == "finish":
        status = args.run_status or "complete"
        active_agents = [agent for agent in manifest["agents"] if agent["status"] not in FINAL_AGENT_STATUSES]
        active_sessions = [session for session in manifest["sessions"] if session["status"] == "running"]
        if active_agents or active_sessions:
            parser.error(f"cannot finish with {len(active_agents)} active agents and {len(active_sessions)} active sessions")
        manifest["status"] = status
        manifest["completed_at"] = now_iso()

    save_json(manifest_path, manifest)
    print(manifest_path)


if __name__ == "__main__":
    main()
