#!/usr/bin/env python3
"""Insert a rate-limit gate around a workflow's main flow."""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from helpers.workspace import workspace_root


_RATE_LIMIT_NODE_NAME = "Rate Limit"
_IF_NODE_NAME = "Rate Limit Allowed?"
_DENIED_PASSTHROUGH_NAME = "Rate Limit Denied"
_DENIED_STOP_NAME = "Rate Limit Stop"

_VALID_ON_DENIED = ("passthrough", "stop", "error")


def _make_rate_limit_node(
    name: str,
    target_workflow_placeholder: str,
    position: list,
    scope_expr: str,
    limit: int,
    window_seconds: int,
) -> dict:
    return {
        "id": "{{@uuid:" + name.lower().replace(" ", "-") + "}}",
        "name": name,
        "type": "n8n-nodes-base.executeWorkflow",
        "typeVersion": 1.2,
        "position": position,
        "parameters": {
            "source": "database",
            "workflowId": {
                "__rl": True,
                "value": target_workflow_placeholder,
                "mode": "id",
            },
            "workflowInputs": {
                "mappingMode": "defineBelow",
                "value": {
                    "scope": scope_expr,
                    "limit": limit,
                    "windowSeconds": window_seconds,
                },
                "matchingColumns": [],
                "schema": [],
            },
            "options": {},
        },
    }


def _make_if_node(name: str, position: list) -> dict:
    return {
        "id": "{{@uuid:" + name.lower().replace(" ", "-").replace("?", "") + "}}",
        "name": name,
        "type": "n8n-nodes-base.if",
        "typeVersion": 2,
        "position": position,
        "parameters": {
            "conditions": {
                "options": {
                    "caseSensitive": True,
                    "leftValue": "",
                    "typeValidation": "strict",
                },
                "conditions": [
                    {
                        "id": "{{@uuid:" + name.lower().replace(" ", "-").replace("?", "") + "-cond}}",
                        "leftValue": "={{ $json.allowed === true }}",
                        "rightValue": True,
                        "operator": {
                            "type": "boolean",
                            "operation": "true",
                            "singleValue": True,
                        },
                    },
                ],
                "combinator": "and",
            },
            "options": {},
        },
    }


def _make_denied_passthrough_node(name: str, position: list, scope_expr: str) -> dict:
    return {
        "id": "{{@uuid:" + name.lower().replace(" ", "-") + "}}",
        "name": name,
        "type": "n8n-nodes-base.set",
        "typeVersion": 3.4,
        "position": position,
        "parameters": {
            "assignments": {
                "assignments": [
                    {
                        "id": "{{@uuid:" + name.lower().replace(" ", "-") + "-allowed}}",
                        "name": "allowed",
                        "value": False,
                        "type": "boolean",
                    },
                    {
                        "id": "{{@uuid:" + name.lower().replace(" ", "-") + "-scope}}",
                        "name": "scope",
                        "value": "={{ $json.scope }}",
                        "type": "string",
                    },
                    {
                        "id": "{{@uuid:" + name.lower().replace(" ", "-") + "-count}}",
                        "name": "count",
                        "value": "={{ $json.count }}",
                        "type": "number",
                    },
                    {
                        "id": "{{@uuid:" + name.lower().replace(" ", "-") + "-limit}}",
                        "name": "limit",
                        "value": "={{ $json.limit }}",
                        "type": "number",
                    },
                ],
            },
            "options": {},
        },
    }


def _make_denied_stop_node(name: str, position: list) -> dict:
    return {
        "id": "{{@uuid:" + name.lower().replace(" ", "-") + "}}",
        "name": name,
        "type": "n8n-nodes-base.stopAndError",
        "typeVersion": 1,
        "position": position,
        "parameters": {
            "errorMessage": "Rate limit exceeded for scope={{ $json.scope }} (count={{ $json.count }}, limit={{ $json.limit }})",
            "options": {},
        },
    }


def _insert_rate_limit(
    template: dict,
    scope_expr: str,
    limit: int,
    window_seconds: int,
    on_denied: str = "passthrough",
) -> dict:
    if on_denied not in _VALID_ON_DENIED:
        raise SystemExit(f"--on-denied must be one of {_VALID_ON_DENIED}; got {on_denied!r}")

    # Reuse the lock helper's normalizer — same n8n expression-form constraints
    # apply to executeWorkflow defineBelow inputs in this primitive.
    from helpers.add_lock_to_workflow import _normalize_n8n_expression
    scope_expr, was_normalized = _normalize_n8n_expression(scope_expr)
    if was_normalized:
        print(
            f"WARNING: --scope-expression normalized to canonical form: {scope_expr!r}. "
            "Bare '=<expr>' or literal scopes are auto-wrapped to '={{{{ <expr> }}}}'.",
            file=sys.stderr,
        )

    nodes = template.setdefault("nodes", [])
    connections = template.setdefault("connections", {})

    if any(n.get("name") == _RATE_LIMIT_NODE_NAME for n in nodes):
        raise SystemExit(f"Workflow already has a '{_RATE_LIMIT_NODE_NAME}' node; refusing to add again")

    # Find the trigger (a node with no inbound connection)
    referenced: set[str] = set()
    for src_name, by_type in connections.items():
        for type_branches in by_type.values():
            for branch in type_branches:
                for c in branch:
                    referenced.add(c.get("node"))
    triggers = [n for n in nodes if n.get("name") not in referenced]
    if not triggers:
        raise SystemExit("Could not detect a trigger node (no node lacks inbound connections)")
    trigger = triggers[0]
    trigger_name = trigger["name"]

    trigger_out = connections.get(trigger_name, {}).get("main", [[]])
    first_branch = trigger_out[0] if trigger_out else []

    trigger_pos = trigger.get("position") or [240, 300]
    rl_pos = [trigger_pos[0] + 220, trigger_pos[1]]
    if_pos = [trigger_pos[0] + 440, trigger_pos[1]]
    denied_pos = [trigger_pos[0] + 660, trigger_pos[1] + 160]

    # Push every other node 660 right (220 for rate-limit + 220 for if + 220 spacing)
    for n in nodes:
        if n is trigger:
            continue
        pos = n.get("position") or [0, 0]
        n["position"] = [pos[0] + 660, pos[1]]

    rl_node = _make_rate_limit_node(
        _RATE_LIMIT_NODE_NAME,
        "{{@env:workflows.rate_limit_check.id}}",
        rl_pos,
        scope_expr,
        limit,
        window_seconds,
    )
    if_node = _make_if_node(_IF_NODE_NAME, if_pos)
    nodes.append(rl_node)
    nodes.append(if_node)

    if on_denied == "passthrough":
        denied_node = _make_denied_passthrough_node(_DENIED_PASSTHROUGH_NAME, denied_pos, scope_expr)
        denied_name = _DENIED_PASSTHROUGH_NAME
    else:
        # `stop` and `error` both map to stopAndError (errors trigger errorWorkflow if configured)
        denied_node = _make_denied_stop_node(_DENIED_STOP_NAME, denied_pos)
        denied_name = _DENIED_STOP_NAME
    nodes.append(denied_node)

    # Wire: trigger → rate_limit → if → (allowed: original first_branch | denied: denied_node)
    connections[trigger_name] = {"main": [[{"node": _RATE_LIMIT_NODE_NAME, "type": "main", "index": 0}]]}
    connections[_RATE_LIMIT_NODE_NAME] = {"main": [[{"node": _IF_NODE_NAME, "type": "main", "index": 0}]]}
    connections[_IF_NODE_NAME] = {
        "main": [
            first_branch,
            [{"node": denied_name, "type": "main", "index": 0}],
        ],
    }

    return template


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", default=None)
    parser.add_argument("--workflow-key", required=True, dest="workflow_key")
    parser.add_argument("--limit", type=int, required=True)
    parser.add_argument("--window-seconds", type=int, required=True, dest="window_seconds")
    parser.add_argument(
        "--scope-expression",
        default="={{ $execution.id }}",
        dest="scope_expression",
    )
    parser.add_argument(
        "--on-denied",
        choices=_VALID_ON_DENIED,
        default="passthrough",
        dest="on_denied",
    )
    args = parser.parse_args()

    ws = workspace_root(args.workspace)

    if not (ws / "n8n-workflows-template" / "rate_limit_check.template.json").exists():
        print(
            "ERROR: primitive 'rate_limit_check' not found in workspace. "
            "Run create-lock --include-rate-limit first.",
            file=sys.stderr,
        )
        sys.exit(1)

    template_path = ws / "n8n-workflows-template" / f"{args.workflow_key}.template.json"
    if not template_path.exists():
        print(f"ERROR: workflow template not found: {template_path}", file=sys.stderr)
        sys.exit(1)

    template = json.loads(template_path.read_text())
    template = _insert_rate_limit(
        template,
        args.scope_expression,
        args.limit,
        args.window_seconds,
        on_denied=args.on_denied,
    )
    template_path.write_text(json.dumps(template, indent=2))
    print(f"  Inserted rate-limit gate in {template_path} (on-denied={args.on_denied})")
    print("add-rate-limit-to-workflow complete.")


if __name__ == "__main__":
    main()
