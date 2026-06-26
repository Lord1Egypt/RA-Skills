#!/usr/bin/env python3
"""Turn a workflow into a polling queue consumer (Schedule + Queue Pop + Has Message? + Queue Ack)."""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from helpers.workspace import workspace_root
# Reuse the lock helper's expression normaliser + Execute Workflow factory.
from helpers.add_lock_to_workflow import (
    _normalize_n8n_expression,
    _extract_static_scope,
    _make_execute_workflow_node,
)


_POP_NODE_NAME = "Queue Pop"
_ACK_NODE_NAME = "Queue Ack"
_IF_NODE_NAME = "Has Message?"
_SCHEDULE_NODE_NAME = "Schedule Trigger"
_SCHEDULE_TRIGGER_TYPE = "n8n-nodes-base.scheduleTrigger"


# ---------- copy of _auto_register from publish helper ----------
# Same logic as add_queue_publish_to_workflow._auto_register_queue_scopes;
# kept inline here so the consumer-wrap can stand alone.
def _auto_register_queue_scopes(workspace: Path, scope_expr: str) -> None:
    static = _extract_static_scope(scope_expr)
    if static is None:
        print(
            "  NOTE: --stream-expression is dynamic (depends on $json or runtime data). "
            "Active error-handler cleanup requires manual queueScopes maintenance — "
            "add the resolved stream names to <env>.yml.queueScopes by hand.",
            file=sys.stderr,
        )
        return
    config_dir = workspace / "n8n-config"
    if not config_dir.is_dir():
        return
    import yaml as _yaml
    for yml in sorted(config_dir.glob("*.yml")):
        if yml.stem in ("common", "deployment_order"):
            continue
        try:
            data = _yaml.safe_load(yml.read_text()) or {}
        except Exception:
            continue
        scopes = data.setdefault("queueScopes", [])
        if not isinstance(scopes, list):
            scopes = []
            data["queueScopes"] = scopes
        if static not in scopes:
            scopes.append(static)
            yml.write_text(_yaml.dump(data, default_flow_style=False, sort_keys=False))
            print(f"  Registered queueScopes += {static!r} in {yml.name}")


def _parse_schedule_interval(expr: str) -> dict:
    """Parse '30s' / '1m' / '5m' / '2h' / '1d' into a scheduleTrigger@1.3 interval[0] entry."""
    m = re.match(r"^\s*(\d+)\s*([smhdw])?\s*$", expr or "")
    if not m:
        raise ValueError(
            f"--schedule-interval must be like '30s', '5m', '1h', got {expr!r}"
        )
    n = int(m.group(1))
    unit = m.group(2) or "m"
    unit_map = {
        "s": ("seconds", "secondsInterval"),
        "m": ("minutes", "minutesInterval"),
        "h": ("hours", "hoursInterval"),
        "d": ("days", "daysInterval"),
        "w": ("weeks", "weeksInterval"),
    }
    field, interval_key = unit_map[unit]
    return {"field": field, interval_key: n}


def _make_schedule_trigger_node(name: str, position: list, interval_expr: str) -> dict:
    """Build a scheduleTrigger@1.3 node with rule.interval[0] populated."""
    interval = _parse_schedule_interval(interval_expr)
    return {
        "id": "{{@uuid:" + name.lower().replace(" ", "-") + "}}",
        "name": name,
        "type": _SCHEDULE_TRIGGER_TYPE,
        "typeVersion": 1.3,
        "position": position,
        "parameters": {
            "rule": {
                "interval": [interval],
            },
        },
    }


def _make_if_has_message(name: str, position: list) -> dict:
    """If gate: route on whether the Queue Pop returned a usable message."""
    base_id = name.lower().replace(" ", "-").replace("?", "")
    return {
        "id": "{{@uuid:" + base_id + "}}",
        "name": name,
        "type": "n8n-nodes-base.if",
        "typeVersion": 2.2,
        "position": position,
        "parameters": {
            "conditions": {
                "options": {
                    "caseSensitive": True,
                    "leftValue": "",
                    "typeValidation": "strict",
                    "version": 2,
                },
                "conditions": [
                    {
                        "id": "{{@uuid:" + base_id + "-cond}}",
                        "leftValue": "={{ $json.empty !== true && $json.at_capacity !== true && $json.dlq_routed !== true }}",
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


_TRIGGER_TYPE_HINTS = (
    "trigger",  # any *Trigger / *trigger node type
    "webhook",
    "formtrigger",
    "emailreadimap",
    "rssfeedread",
)


def _is_trigger_node(node: dict) -> bool:
    t = (node.get("type") or "").lower()
    return any(hint in t for hint in _TRIGGER_TYPE_HINTS)


def _detect_trigger(template: dict) -> tuple[dict | None, str | None]:
    """Find the (sole) trigger node — by type, not by graph-position.

    A node is a trigger only if its type matches a known trigger shape
    (anything with 'trigger' or 'webhook' in the type). This prevents a stray
    main-flow node (e.g. an orphan Set with no inbound edges) from being
    mistaken for a trigger and incorrectly treated as one.
    """
    nodes = template.get("nodes", [])
    triggers = [n for n in nodes if _is_trigger_node(n)]
    if not triggers:
        return (None, None)
    trigger = triggers[0]
    return (trigger, trigger.get("name"))


def _insert_consumer(
    template: dict,
    *,
    stream_expr: str,
    group_expr: str | None,
    consumer_expr: str | None,
    max_concurrency: int,
    max_retries: int,
    dlq_enabled: bool,
    batch_size: int,
    claim_idle_ms: int,
    schedule_interval: str,
    ack_on_success_expression: str,
    remove_existing_trigger: bool,
) -> dict:
    """Splice Schedule? + Queue Pop + Has Message? + (existing flow) + Queue Ack."""
    nodes = template.setdefault("nodes", [])
    connections = template.setdefault("connections", {})

    if any(n.get("name") == _POP_NODE_NAME for n in nodes):
        raise SystemExit(f"Workflow already has a '{_POP_NODE_NAME}' node; refusing to add again")

    trigger, trigger_name = _detect_trigger(template)

    # Capture the existing "main flow head" before any mutation: when we
    # install/reuse a trigger, Pop+If's true-branch must route into whatever
    # was downstream of the original trigger (or, if there was none, the
    # left-most existing main-flow node).
    pre_existing_first_branch: list[dict] = []
    if trigger is not None and trigger_name in connections:
        out = connections.get(trigger_name, {}).get("main", [[]])
        pre_existing_first_branch = out[0] if out else []
    elif trigger is None and nodes:
        # No trigger — pick the orphan node with the smallest x as the head.
        leftmost = min(nodes, key=lambda n: (n.get("position") or [0, 0])[0])
        pre_existing_first_branch = [{"node": leftmost["name"], "type": "main", "index": 0}]

    # Decide whether to insert a Schedule Trigger or reuse an existing one.
    inserted_schedule = False
    if trigger is not None and trigger.get("type") == _SCHEDULE_TRIGGER_TYPE:
        # Reuse the existing schedule trigger.
        schedule = trigger
        schedule_name = trigger_name
        anchor_x = (trigger.get("position") or [240, 300])[0]
        anchor_y = (trigger.get("position") or [240, 300])[1]
    else:
        # Need to install one. If a non-schedule trigger exists, refuse unless
        # the caller explicitly opted into removing it.
        if trigger is not None and not remove_existing_trigger:
            raise SystemExit(
                f"Workflow already has a non-schedule trigger '{trigger_name}' "
                f"(type={trigger.get('type')}). Pass --remove-existing-trigger to "
                "replace it with a schedule trigger, or remove the trigger by hand first."
            )
        if trigger is not None and remove_existing_trigger:
            # Drop the existing trigger and any connections from it.
            nodes.remove(trigger)
            if trigger_name in connections:
                del connections[trigger_name]
            old_trigger_pos = trigger.get("position") or [240, 300]
            anchor_x = old_trigger_pos[0]
            anchor_y = old_trigger_pos[1]
        else:
            # No trigger at all (or just user-flow nodes); place the schedule
            # at a default position and right-shift downstream.
            anchor_x = 240
            anchor_y = 300

        schedule_pos = [anchor_x, anchor_y]
        schedule = _make_schedule_trigger_node(_SCHEDULE_NODE_NAME, schedule_pos, schedule_interval)
        schedule_name = _SCHEDULE_NODE_NAME
        nodes.append(schedule)
        inserted_schedule = True

    # Compute right-shift: schedule (220 if inserted) + pop (220) + if (220) = up to 660.
    # If schedule was reused, shift starts after schedule's x; we still add 660
    # to make room for Pop + If + Ack downstream of schedule. Actually simpler:
    # always shift original non-schedule nodes by 660 px (Pop + If + Ack
    # occupy three slots). When a schedule was inserted, those nodes also need
    # to make room for the schedule trigger itself, but the schedule sits at
    # the original trigger position so existing nodes keep their relative
    # offset — the +660 covers Pop + If + Ack only.
    shift_amount = 3 * 220  # 660
    pop_x = anchor_x + 220
    if_x = anchor_x + 440
    ack_x = anchor_x + 660 + 220  # leave room for the user's main flow between If-true and Ack

    # Right-shift every existing node except schedule by shift_amount; if no
    # schedule was inserted, also leave the schedule node alone.
    for n in nodes:
        if n is schedule:
            continue
        pos = n.get("position") or [0, 0]
        n["position"] = [pos[0] + shift_amount, pos[1]]

    # The "main flow head" — what should run after Pop returns a usable
    # message. Captured before mutation above; falls back to current schedule
    # outbound if nothing pre-existed.
    first_branch = pre_existing_first_branch or (
        connections.get(schedule_name, {}).get("main", [[]])[0]
        if connections.get(schedule_name, {}).get("main") else []
    )

    # Build Pop + If + Ack nodes.
    norm_stream, _ = _normalize_n8n_expression(stream_expr)
    norm_group = _normalize_n8n_expression(group_expr)[0] if group_expr else None
    norm_consumer = _normalize_n8n_expression(consumer_expr)[0] if consumer_expr else None
    norm_ack_success = _normalize_n8n_expression(ack_on_success_expression)[0]

    pop_inputs = {
        "stream": norm_stream,
        "group": norm_group if norm_group is not None else norm_stream,  # reasonable default
        "consumer": norm_consumer if norm_consumer is not None else "={{ $workflow.name + '-' + $execution.id }}",
        "max_concurrency": max_concurrency,
        "max_retries": max_retries,
        "dlq_enabled": dlq_enabled,
        "batch_size": batch_size,
        "claim_idle_ms": claim_idle_ms,
        # Pass the caller's execution id through so queue_pop's permit sidecar
        # records the PARENT consumer execution, not the queue_pop sub-workflow
        # execution. Without this, error_handler_queue_cleanup's ownership filter
        # never matches and orphan permits leak forever (DEFECT-3).
        "caller_execution_id": "={{ $execution.id }}",
    }
    pop_node = _make_execute_workflow_node(
        _POP_NODE_NAME,
        "{{@env:workflows.queue_pop.id}}",
        [pop_x, anchor_y],
        pop_inputs,
    )
    if_node = _make_if_has_message(_IF_NODE_NAME, [if_x, anchor_y])

    ack_inputs = {
        "stream": "={{ $('Queue Pop').first().json.stream }}",
        "group": "={{ $('Queue Pop').first().json.group }}",
        "message_id": "={{ $('Queue Pop').first().json.message_id }}",
        "success": norm_ack_success,
    }
    ack_node = _make_execute_workflow_node(
        _ACK_NODE_NAME,
        "{{@env:workflows.queue_ack.id}}",
        [ack_x + (shift_amount if not inserted_schedule else 0), anchor_y],
        ack_inputs,
    )

    nodes.append(pop_node)
    nodes.append(if_node)
    nodes.append(ack_node)

    # Wire: schedule → Pop → If
    connections[schedule_name] = {"main": [[{"node": _POP_NODE_NAME, "type": "main", "index": 0}]]}
    connections[_POP_NODE_NAME] = {"main": [[{"node": _IF_NODE_NAME, "type": "main", "index": 0}]]}

    # If has a message, route into the original first-downstream of the
    # original trigger; the no-message branch is a no-op (terminate iter).
    # Find terminal nodes of the user's flow (those with no outbound) and
    # route them all into Queue Ack.
    if first_branch:
        connections[_IF_NODE_NAME] = {"main": [first_branch, []]}
    else:
        # No existing main flow — wire If-true straight to Queue Ack.
        connections[_IF_NODE_NAME] = {"main": [[{"node": _ACK_NODE_NAME, "type": "main", "index": 0}], []]}

    outbound_names = set(connections.keys())
    skip = {schedule_name, _POP_NODE_NAME, _IF_NODE_NAME, _ACK_NODE_NAME}
    terminals = [n["name"] for n in nodes if n["name"] not in outbound_names and n["name"] not in skip]
    for t in terminals:
        connections[t] = {"main": [[{"node": _ACK_NODE_NAME, "type": "main", "index": 0}]]}

    return template


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", default=None)
    parser.add_argument("--workflow-key", required=True, dest="workflow_key")
    parser.add_argument("--stream-expression", required=True, dest="stream_expression")
    parser.add_argument("--group-expression", default=None, dest="group_expression")
    parser.add_argument("--consumer-expression", default=None, dest="consumer_expression")
    parser.add_argument("--max-concurrency", type=int, default=1, dest="max_concurrency")
    parser.add_argument("--max-retries", type=int, default=3, dest="max_retries")
    parser.add_argument("--dlq-enabled", action="store_true", dest="dlq_enabled")
    parser.add_argument("--no-dlq-enabled", action="store_false", dest="dlq_enabled")
    parser.set_defaults(dlq_enabled=False)
    parser.add_argument("--batch-size", type=int, default=1, dest="batch_size")
    parser.add_argument("--claim-idle-ms", type=int, default=60000, dest="claim_idle_ms")
    parser.add_argument("--schedule-interval", default="30s", dest="schedule_interval")
    parser.add_argument("--cleanup-on-error", action="store_true", dest="cleanup_on_error")
    parser.add_argument(
        "--ack-on-success-expression", default="={{ true }}",
        dest="ack_on_success_expression",
    )
    parser.add_argument(
        "--remove-existing-trigger", action="store_true",
        dest="remove_existing_trigger",
        help="Replace the workflow's existing non-schedule trigger with a schedule trigger.",
    )
    args = parser.parse_args()

    ws = workspace_root(args.workspace)

    for prim in ("queue_pop", "queue_ack"):
        if not (ws / "n8n-workflows-template" / f"{prim}.template.json").exists():
            print(
                f"ERROR: primitive '{prim}' not found in workspace. Run create-queue first.",
                file=sys.stderr,
            )
            sys.exit(1)

    template_path = ws / "n8n-workflows-template" / f"{args.workflow_key}.template.json"
    if not template_path.exists():
        print(f"ERROR: workflow template not found: {template_path}", file=sys.stderr)
        sys.exit(1)

    template = json.loads(template_path.read_text())
    template = _insert_consumer(
        template,
        stream_expr=args.stream_expression,
        group_expr=args.group_expression,
        consumer_expr=args.consumer_expression,
        max_concurrency=args.max_concurrency,
        max_retries=args.max_retries,
        dlq_enabled=args.dlq_enabled,
        batch_size=args.batch_size,
        claim_idle_ms=args.claim_idle_ms,
        schedule_interval=args.schedule_interval,
        ack_on_success_expression=args.ack_on_success_expression,
        remove_existing_trigger=args.remove_existing_trigger,
    )
    template_path.write_text(json.dumps(template, indent=2))
    print(f"  Inserted Queue Pop + Has Message? + Queue Ack in {template_path}")

    _auto_register_queue_scopes(ws, args.stream_expression)

    if args.cleanup_on_error:
        import subprocess
        cmd = [
            sys.executable,
            str(Path(__file__).parent / "register_error_handler.py"),
            "--workspace", str(ws),
            "--workflow-key", args.workflow_key,
            "--handler-key", "error_handler_queue_cleanup",
        ]
        r = subprocess.run(cmd, capture_output=True, text=True)
        print(r.stdout)
        if r.returncode != 0:
            print(r.stderr, file=sys.stderr)
            sys.exit(r.returncode)
    print("add-queue-consumer-to-workflow complete.")


if __name__ == "__main__":
    main()
