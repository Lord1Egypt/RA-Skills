"""Build a host-specific orchestration plan without claiming the host ran it."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from artifact_contract import native_analysis_identity


ROOT = Path(__file__).resolve().parents[1]
ROLES = ["data-analyst", "platform-ops", "content-live-growth", "ad-profit-optimizer", "delivery-review"]


def require(value, reason):
    if not value:
        raise ValueError(reason)


def build_plan(host, capabilities, run_id, client_scope, team_version):
    profiles = json.loads((ROOT / "config" / "host-profiles.json").read_text(encoding="utf-8"))
    require(host in ("workbuddy", "codex"), "host_invalid")
    require(isinstance(capabilities, list) and all(isinstance(item, str) and item for item in capabilities),
            "host_capabilities_invalid")
    observed = sorted(set(capabilities))
    profile = profiles[host]
    forbidden_hit = sorted(set(observed) & set(profile["forbidden_tools"]))
    require(not forbidden_hit, f"{host}_foreign_tool_forbidden:" + ",".join(forbidden_hit))

    if host == "workbuddy":
        require(profile["native_member_launcher"] in observed, "workbuddy_agent_tool_missing")
        require(profile["native_wait"] in observed, "workbuddy_wait_tool_missing")
        require(all(item in observed for item in profile["phase_management"]), "workbuddy_phase_tools_missing")
        if "TeamCreate" in observed:
            bootstrap = "teamcreate_direct"
        else:
            require(all(item in observed for item in profile["deferred_bootstrap"]),
                    "workbuddy_teamcreate_unavailable")
            bootstrap = "teamcreate_deferred"
        steps = [
            "TeamCreate 成功并取得真实 team_name 后才允许读取业务数据",
            "创建并由团长维护可见阶段任务",
            "用 Agent 启动四位分析专家并保留真实子任务 ID",
            "用 TaskOutput 等待真实终态并接收四份正式回传",
            "团长裁决并生成冻结报告候选稿",
            "用 Agent 启动 delivery-review 并等待真实复核回传",
            "完成质量、公域和 completion gate 后检查 TaskList 全部结束",
        ]
    else:
        require(all(item in observed for item in profile["required_tools"]), "codex_native_subagent_tools_missing")
        bootstrap = "codex_native_subagents"
        steps = [
            "确认 Codex 原生子代理容量，不创建 WorkBuddy Team",
            "用 spawn_agent 启动四位分析专家并保留原始 agent ID",
            "用 wait_agent 按原任务等待；观察超时不等于任务失败",
            "收齐四份正式回传后由主理人裁决并生成冻结报告候选稿",
            "用 spawn_agent 启动独立 delivery-review 并等待真实复核回传",
            "完成质量、公域和 completion gate 后再结束主任务",
        ]

    return {
        **native_analysis_identity("orchestration_plan", team_version),
        "run_id": run_id,
        "client_scope": client_scope,
        "team_version": team_version,
        "host": host,
        "bootstrap_mode": bootstrap,
        "member_launcher": profile["native_member_launcher"],
        "wait_tool": profile["native_wait"],
        "message_tool": profile["native_message"],
        "required_roles": ROLES,
        "observed_capabilities": observed,
        "forbidden_tools": profile["forbidden_tools"],
        "ordered_steps": steps,
        "runtime_evidence_required": True,
        "orchestration_completed": False,
        "status": "planned_not_executed",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="生成宿主专属多专家调度计划")
    parser.add_argument("--host", required=True, choices=("workbuddy", "codex"))
    parser.add_argument("--capability", action="append", default=[])
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--client-scope", required=True)
    parser.add_argument("--team-version", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    output = Path(args.output).resolve()
    try:
        plan = build_plan(args.host, args.capability, args.run_id, args.client_scope, args.team_version)
        require(not output.exists(), "host_plan_output_exists")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print("host_orchestration_blocked:" + str(exc))
        return 2
    print(json.dumps({"status": "PASS", "host": args.host, "output": str(output)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
