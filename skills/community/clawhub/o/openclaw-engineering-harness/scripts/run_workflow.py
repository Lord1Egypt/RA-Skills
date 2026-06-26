from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from runtime_support import (
    audit_directory,
    build_state_layer,
    build_tool_layer,
    evaluate_constraints,
    load_json_file,
    phase_name_map,
    summarize_present_fields,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate minimal engineering loop plan based on policy")
    parser.add_argument("--request", type=Path, help="Structured request JSON file")
    parser.add_argument("--policy", type=Path, help="Workflow policy JSON file")
    parser.add_argument("--tool-config", type=Path, help="Tool config JSON file")
    parser.add_argument("--state-policy", type=Path, help="State policy JSON file")
    parser.add_argument("--constraint-policy", type=Path, help="Constraint policy JSON file")
    parser.add_argument("--audit-path", type=Path, help="Optional, append directory audit execution")
    parser.add_argument("--output", type=Path, help="Optional, write result JSON")
    return parser.parse_args()

def build_plan(request: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    required_fields = [item for item in policy.get("required_fields", []) if isinstance(item, str)]
    missing_fields = [field for field in required_fields if request.get(field) in (None, "", [], {})]
    phase_checks = policy.get("phase_checks", {})
    if not isinstance(phase_checks, dict):
        raise ValueError("phase_checks must be an object")
    phase_order = [item for item in policy.get("phase_order", []) if isinstance(item, str)]
    phase_display = phase_name_map(policy)
    phases: list[dict[str, Any]] = []
    phase_missing_fields: list[str] = []
    for phase_key in phase_order:
        required_by_phase = [item for item in phase_checks.get(phase_key, []) if isinstance(item, str)]
        missing_by_phase = [field for field in required_by_phase if request.get(field) in (None, "", [], {})]
        for field in missing_by_phase:
            if field not in phase_missing_fields:
                phase_missing_fields.append(field)
        phases.append(
            {
                "id": phase_key,
                "title": phase_display.get(phase_key, phase_key),
                "required_inputs": required_by_phase,
                "present_inputs": summarize_present_fields(request, required_by_phase),
                "missing_inputs": missing_by_phase,
                "ready": not missing_by_phase,
            }
        )
    return {
        "ready": not missing_fields and not phase_missing_fields,
        "missing_fields": missing_fields,
        "phase_missing_fields": phase_missing_fields,
        "request_fields": sorted(request.keys()),
        "phases": phases,
    }


def default_policy_path(script_path: Path) -> Path:
    return script_path.resolve().parents[1] / "policies" / "workflow-policy.json"


def resolve_layer_path(skill_root: Path, configured: Any, fallback: str) -> Path:
    candidate = configured if isinstance(configured, str) and configured else fallback
    return (skill_root / candidate).resolve()



def main() -> int:
    args = parse_args()
    policy_path = args.policy.resolve() if args.policy else default_policy_path(Path(__file__))
    skill_root = policy_path.parent.parent
    workflow_policy = load_json_file(policy_path)
    request = load_json_file(args.request.resolve()) if args.request else {}

    tool_config_path = args.tool_config.resolve() if args.tool_config else resolve_layer_path(skill_root, workflow_policy.get("default_tool_config"), "tool/tool-config.json")
    state_policy_path = args.state_policy.resolve() if args.state_policy else resolve_layer_path(skill_root, workflow_policy.get("default_state_policy"), "state/state-policy.json")
    constraint_policy_path = args.constraint_policy.resolve() if args.constraint_policy else resolve_layer_path(skill_root, workflow_policy.get("default_constraint_policy"), "policy/constraint-policy.json")

    tool_config = load_json_file(tool_config_path)
    state_policy = load_json_file(state_policy_path)
    constraint_policy = load_json_file(constraint_policy_path)

    workflow_result = build_plan(request, workflow_policy)
    tool_layer = build_tool_layer(request, workflow_policy, tool_config)
    state_layer = build_state_layer(request, workflow_policy, state_policy)
    policy_layer = evaluate_constraints(
        {
            "request": request,
            "workflow_policy": workflow_policy,
            "tool_config": tool_config,
            "state_policy": state_policy,
            "policy": constraint_policy,
            "tool_layer": tool_layer,
            "state_layer": state_layer,
        },
        constraint_policy,
    )

    overall_ready = workflow_result["ready"] and tool_layer["ready"] and not policy_layer["blocked"]
    result: dict[str, Any] = {
        "workflow_policy": policy_path.name,
        "tool_config": tool_config_path.name,
        "state_policy": state_policy_path.name,
        "constraint_policy": constraint_policy_path.name,
        "ready": overall_ready,
        "result": workflow_result,
        "layers": {
            "tool": tool_layer,
            "state": state_layer,
            "policy": policy_layer,
        },
    }
    if args.audit_path:
        audit_policy_name = str(workflow_policy.get("default_audit_policy", "export-audit-policy.json"))
        audit_policy_path = policy_path.parent / audit_policy_name
        audit_policy = load_json_file(audit_policy_path)
        result["audit"] = audit_directory(args.audit_path.resolve(), audit_policy)

    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.resolve().write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)

    audit_blocked = bool(result.get("audit", {}).get("blocked"))
    return 0 if result["ready"] and not audit_blocked else 1


if __name__ == "__main__":
    raise SystemExit(main())
