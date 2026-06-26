#!/usr/bin/env python3
"""Insert a Queue Publish Execute Workflow node into a workflow's flow (XADD producer)."""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from helpers.workspace import workspace_root
# Reuse the lock helper's expression normaliser, static-scope extractor, and
# Execute Workflow node factory — they're key-agnostic. See note in
# create_queue.py about the future shared-helper extraction.
from helpers.add_lock_to_workflow import (
    _normalize_n8n_expression,
    _extract_static_scope,
    _make_execute_workflow_node,
)


_PUBLISH_NODE_NAME = "Queue Publish"
_DEFAULT_INSERTION_POINT = "auto"  # = after-trigger


def _auto_register_queue_scopes(workspace: Path, scope_expr: str) -> None:
    """Append the static literal stream name to every <env>.yml.queueScopes (idempotent).

    Parallel implementation of `_auto_register_lock_scopes` in
    `helpers/add_lock_to_workflow.py` — same logic, different YAML key. Flagged
    for refactor into a shared `_auto_register_scopes(workspace, expr, scope_key)`
    once we have a third caller.
    """
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


def _detect_trigger(nodes: list, connections: dict) -> dict:
    """Return the trigger node (the one node with no inbound connections)."""
    referenced: set[str] = set()
    for by_type in connections.values():
        for type_branches in by_type.values():
            for branch in type_branches:
                for c in branch:
                    referenced.add(c.get("node"))
    triggers = [n for n in nodes if n.get("name") not in referenced]
    if not triggers:
        raise SystemExit("Could not detect a trigger node (no node lacks inbound connections)")
    return triggers[0]


def _find_node_by_name(nodes: list, name: str) -> dict:
    """Return the node with the given name, or raise SystemExit."""
    matches = [n for n in nodes if n.get("name") == name]
    if not matches:
        existing = ", ".join(sorted(n.get("name", "") for n in nodes))
        raise SystemExit(f"Node '{name}' not found in workflow. Existing nodes: {existing}")
    if len(matches) > 1:
        # n8n normally enforces unique node names, but defend anyway.
        raise SystemExit(f"Ambiguous: {len(matches)} nodes named '{name}' in workflow")
    return matches[0]


def _find_terminals(nodes: list, connections: dict) -> list:
    """Return nodes with no outbound main connections (terminal nodes)."""
    terminals = []
    for n in nodes:
        name = n.get("name")
        out = connections.get(name, {}).get("main", [])
        # Has at least one non-empty branch?
        if not any(branch for branch in out):
            terminals.append(n)
    return terminals


def _downstream_names(connections: dict, start_name: str) -> set[str]:
    """BFS all node names reachable downstream from start_name (exclusive)."""
    seen: set[str] = set()
    queue = [start_name]
    while queue:
        cur = queue.pop(0)
        for branch in connections.get(cur, {}).get("main", []):
            for c in branch or []:
                nxt = c.get("node")
                if nxt and nxt not in seen:
                    seen.add(nxt)
                    queue.append(nxt)
    return seen


def _parse_insertion_point(insertion_point: str) -> tuple[str, str | None]:
    """Parse insertion-point arg into (mode, optional name).

    Modes: 'auto', 'after-trigger', 'before-terminal', 'after-named-node',
    'before-named-node'. The two named-node modes carry the target name after ':'.
    """
    if ":" in insertion_point:
        mode, _, name = insertion_point.partition(":")
        if mode not in ("after-named-node", "before-named-node"):
            raise SystemExit(
                f"--insertion-point '{insertion_point}': only after-named-node and "
                f"before-named-node accept a ':<node-name>' suffix"
            )
        if not name:
            raise SystemExit(f"--insertion-point '{insertion_point}' is missing the node name after ':'")
        return mode, name
    if insertion_point not in ("auto", "after-trigger", "before-terminal",
                                "after-named-node", "before-named-node"):
        raise SystemExit(f"--insertion-point '{insertion_point}' is not a recognised mode")
    if insertion_point in ("after-named-node", "before-named-node"):
        raise SystemExit(
            f"--insertion-point '{insertion_point}' requires a target: "
            f"pass '{insertion_point}:<node-name>' instead"
        )
    return insertion_point if insertion_point != "auto" else "after-trigger", None


def _insert_publish(
    template: dict,
    stream_expr: str,
    max_len: int | None = None,
    approximate: bool = True,
    insertion_point: str = _DEFAULT_INSERTION_POINT,
) -> dict:
    """Splice a single Queue Publish Execute Workflow node at the chosen point.

    Wiring is mode-dependent; position math is intentionally simple — the user
    can re-tidy with tidy-workflow afterward. Correctness over canvas aesthetics.
    """
    nodes = template.setdefault("nodes", [])
    connections = template.setdefault("connections", {})

    if any(n.get("name") == _PUBLISH_NODE_NAME for n in nodes):
        raise SystemExit(f"Workflow already has a '{_PUBLISH_NODE_NAME}' node; refusing to add again")

    mode, target_name = _parse_insertion_point(insertion_point)

    # Resolve the anchor node (the node we're inserting after/before) per mode.
    if mode == "after-trigger":
        anchor = _detect_trigger(nodes, connections)
        place_after = True
    elif mode == "before-terminal":
        terminals = _find_terminals(nodes, connections)
        if not terminals:
            raise SystemExit("--insertion-point before-terminal: no terminal node found "
                             "(every node has outbound connections — is this a complete workflow?)")
        if len(terminals) > 1:
            names = ", ".join(t.get("name") for t in terminals)
            raise SystemExit(
                f"--insertion-point before-terminal: {len(terminals)} terminal nodes found "
                f"({names}). Disambiguate with --insertion-point before-named-node:<name>."
            )
        anchor = terminals[0]
        place_after = False
    elif mode == "after-named-node":
        anchor = _find_node_by_name(nodes, target_name)
        place_after = True
    elif mode == "before-named-node":
        anchor = _find_node_by_name(nodes, target_name)
        place_after = False
    else:
        raise SystemExit(f"Internal: unhandled insertion mode {mode!r}")

    anchor_name = anchor["name"]
    anchor_pos = anchor.get("position") or [240, 300]

    normalized_stream, was_normalized = _normalize_n8n_expression(stream_expr)
    if was_normalized:
        print(
            f"WARNING: --stream-expression normalized to canonical form: {normalized_stream!r}. "
            "Bare '=<expr>' or literal streams are auto-wrapped to '={{{{ <expr> }}}}'. "
            "Update calls to pass the canonical form directly to silence this warning.",
            file=sys.stderr,
        )

    publish_inputs: dict = {
        "stream": normalized_stream,
        "payload": "={{ $json }}",
        "max_len": max_len if max_len is not None else None,
        "approximate": approximate,
    }

    if place_after:
        # Insert AFTER anchor: splice between anchor and its current downstream.
        publish_pos = [anchor_pos[0] + 220, anchor_pos[1]]
        # Shift downstream of anchor right by 220 to make room.
        downstream = _downstream_names(connections, anchor_name)
        for n in nodes:
            if n.get("name") in downstream:
                pos = n.get("position") or [0, 0]
                n["position"] = [pos[0] + 220, pos[1]]
        publish = _make_execute_workflow_node(
            _PUBLISH_NODE_NAME,
            "{{@env:workflows.queue_publish.id}}",
            publish_pos,
            publish_inputs,
        )
        nodes.append(publish)
        # Re-wire: anchor's old main[0] outputs flow through Publish.
        anchor_out = connections.get(anchor_name, {}).get("main", [[]])
        first_branch = anchor_out[0] if anchor_out else []
        connections[anchor_name] = {"main": [[{"node": _PUBLISH_NODE_NAME, "type": "main", "index": 0}]]}
        connections[_PUBLISH_NODE_NAME] = {"main": [first_branch]} if first_branch else {"main": [[]]}
    else:
        # Insert BEFORE anchor: redirect anchor's inbound edges through Publish.
        publish_pos = [anchor_pos[0], anchor_pos[1]]
        # Shift anchor and its downstream right by 220.
        downstream = _downstream_names(connections, anchor_name) | {anchor_name}
        for n in nodes:
            if n.get("name") in downstream:
                pos = n.get("position") or [0, 0]
                n["position"] = [pos[0] + 220, pos[1]]
        publish = _make_execute_workflow_node(
            _PUBLISH_NODE_NAME,
            "{{@env:workflows.queue_publish.id}}",
            publish_pos,
            publish_inputs,
        )
        nodes.append(publish)
        # Find every inbound edge pointing at anchor, redirect to Publish.
        inbound_count = 0
        for src_name, by_type in connections.items():
            if src_name == _PUBLISH_NODE_NAME:
                continue
            for branches in by_type.values():
                for branch in branches:
                    for c in branch or []:
                        if c.get("node") == anchor_name:
                            c["node"] = _PUBLISH_NODE_NAME
                            inbound_count += 1
        # Wire Publish → anchor
        connections[_PUBLISH_NODE_NAME] = {
            "main": [[{"node": anchor_name, "type": "main", "index": 0}]]
        }
        if inbound_count == 0 and mode == "before-named-node":
            # Anchor had no inbound edges — it's effectively a trigger. Warn.
            print(
                f"WARNING: '{anchor_name}' has no inbound connections — Queue Publish was "
                "inserted but has no upstream. Did you mean --insertion-point after-trigger?",
                file=sys.stderr,
            )

    return template


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", default=None)
    parser.add_argument("--workflow-key", required=True, dest="workflow_key")
    parser.add_argument("--stream-expression", required=True, dest="stream_expression")
    parser.add_argument("--max-len", type=int, default=None, dest="max_len")
    parser.add_argument(
        "--approximate", action="store_true", dest="approximate", default=True,
        help="Use 'MAXLEN ~' (approximate trimming, default)",
    )
    parser.add_argument(
        "--no-approximate", action="store_false", dest="approximate",
        help="Use exact MAXLEN trimming (more expensive)",
    )
    parser.add_argument(
        "--insertion-point", default=_DEFAULT_INSERTION_POINT, dest="insertion_point",
        help="Where to splice the publish node. Accepted values: "
             "'auto' (= after-trigger), 'after-trigger', 'before-terminal' (errors if multiple terminals), "
             "'after-named-node:<node-name>', 'before-named-node:<node-name>'.",
    )
    args = parser.parse_args()

    ws = workspace_root(args.workspace)

    if not (ws / "n8n-workflows-template" / "queue_publish.template.json").exists():
        print(
            "ERROR: primitive 'queue_publish' not found in workspace. Run create-queue first.",
            file=sys.stderr,
        )
        sys.exit(1)

    template_path = ws / "n8n-workflows-template" / f"{args.workflow_key}.template.json"
    if not template_path.exists():
        print(f"ERROR: workflow template not found: {template_path}", file=sys.stderr)
        sys.exit(1)

    template = json.loads(template_path.read_text())
    template = _insert_publish(
        template,
        args.stream_expression,
        max_len=args.max_len,
        approximate=args.approximate,
        insertion_point=args.insertion_point,
    )
    template_path.write_text(json.dumps(template, indent=2))
    print(f"  Inserted Queue Publish in {template_path}")

    _auto_register_queue_scopes(ws, args.stream_expression)
    print("add-queue-publish-to-workflow complete.")


if __name__ == "__main__":
    main()
