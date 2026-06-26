from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from runtime_support import (
    build_state_layer,
    build_tool_layer,
    evaluate_constraints,
    load_json_file,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate 3-layer capabilities against delivery constraints")
    parser.add_argument("--request", type=Path, help="Optional, structured request JSON file")
    parser.add_argument("--workflow-policy", type=Path, help="Workflow policy JSON file")
    parser.add_argument("--tool-config", type=Path, help="Tool config JSON file")
    parser.add_argument("--state-policy", type=Path, help="State policy JSON file")
    parser.add_argument("--constraint-policy", type=Path, help="Constraint policy JSON file")
    parser.add_argument("--output", type=Path, help="Optional, output JSON file")
    return parser.parse_args()


def skill_root_from_script(script_path: Path) -> Path:
    return script_path.resolve().parents[1]


def resolve_layer_path(skill_root: Path, configured: Any, fallback: str) -> Path:
    candidate = configured if isinstance(configured, str) and configured else fallback
    return (skill_root / candidate).resolve()


def main() -> int:
    args = parse_args()
    skill_root = skill_root_from_script(Path(__file__))
    workflow_policy_path = args.workflow_policy.resolve() if args.workflow_policy else skill_root / "policies" / "workflow-policy.json"
    workflow_policy = load_json_file(workflow_policy_path)
    tool_config_path = args.tool_config.resolve() if args.tool_config else resolve_layer_path(skill_root, workflow_policy.get("default_tool_config"), "tool/tool-config.json")
    state_policy_path = args.state_policy.resolve() if args.state_policy else resolve_layer_path(skill_root, workflow_policy.get("default_state_policy"), "state/state-policy.json")
    constraint_policy_path = args.constraint_policy.resolve() if args.constraint_policy else resolve_layer_path(skill_root, workflow_policy.get("default_constraint_policy"), "policy/constraint-policy.json")
    request = load_json_file(args.request.resolve()) if args.request else {}

    tool_config = load_json_file(tool_config_path)
    state_policy = load_json_file(state_policy_path)
    constraint_policy = load_json_file(constraint_policy_path)
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

    rendered = json.dumps(
        {
            "workflow_policy": workflow_policy_path.name,
            "tool_config": tool_config_path.name,
            "state_policy": state_policy_path.name,
            "constraint_policy": constraint_policy_path.name,
            "result": policy_layer,
        },
        ensure_ascii=False,
        indent=2,
    )
    if args.output:
        args.output.resolve().write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    return 1 if policy_layer["blocked"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
