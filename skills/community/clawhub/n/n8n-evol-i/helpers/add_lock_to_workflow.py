#!/usr/bin/env python3
"""Insert lock acquire / release Execute Workflow nodes around a workflow's main flow."""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from helpers.workspace import workspace_root


_LOCK_ACQUIRE_NODE_NAME = "Lock Acquire"
_LOCK_RELEASE_NODE_NAME = "Lock Release"
_DEFAULT_TTL_SECONDS = 86400  # 24h — Redis-side EXPIRE on the lock key
_DEFAULT_MAX_WAIT_SECONDS = 86400  # 24h — wait-loop deadline; effectively unbounded by default


def _normalize_n8n_expression(expr) -> tuple[str, bool]:
    """Normalize a user-supplied n8n expression for executeWorkflow defineBelow inputs.

    n8n's `executeWorkflow@1.2` in `defineBelow` mode requires the canonical
    `={{ <js> }}` form for expression evaluation. The bare `=<js>` prefix is
    treated as a literal string and silently degrades — e.g. `--scope-expression
    "='foo-' + $json.x"` becomes the literal scope `'foo-' + $json.x`, so every
    caller hits the same lock regardless of payload. Skill MD historically
    documented both forms inconsistently; finding #15 from the deep-dive.

    Input shapes:
      (a) `={{ <js> }}`   — already canonical; pass through, no warning.
      (b) `=<js>` (bare)  — wrap into `={{ <js> }}`; emit a one-shot deprecation
                           warning the first time normalization happens.
      (c) `<literal>`     — no leading `=`; treat as a static scope and wrap as
                           `={{ "<literal>" }}` (escaped) so the deployed
                           workflow consistently uses the canonical form.
      (d) `""` / `None`   — reject with a clear error pointing to the canonical
                           form. Avoids silent empty-scope-string bugs from
                           unset env vars.

    Returns `(normalized, was_normalized)`. `was_normalized=True` only for (b)
    and (c), so the caller can emit the deprecation/auto-wrap notice once.
    """
    if expr is None or (isinstance(expr, str) and expr.strip() == ""):
        raise ValueError(
            "--scope-expression must be a non-empty string. Use "
            "'={{ $execution.id }}' for a per-execution scope, "
            "'={{ \"foo-\" + $json.fileId }}' for a per-resource scope, "
            "or pass a literal scope like 'global'."
        )
    s = str(expr)
    if s.startswith("={{") and s.rstrip().endswith("}}"):
        return (s, False)
    if s.startswith("="):
        return ("={{ " + s[1:].strip() + " }}", True)
    # Pure literal — wrap as a JS string expression so the field always uses
    # the canonical `={{ ... }}` form on the wire.
    return ('={{ ' + json.dumps(s) + ' }}', True)


def _make_execute_workflow_node(
    name: str,
    target_workflow_placeholder: str,
    position: list,
    inputs: dict,
) -> dict:
    """Build an Execute Workflow node with `inputs` mapped into workflowInputs.value."""
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
                "value": inputs,
                "matchingColumns": [],
                "schema": [],
            },
            "options": {},
        },
    }


def _insert_lock(
    template: dict,
    scope_expr: str,
    ttl_seconds: int = _DEFAULT_TTL_SECONDS,
    max_wait_seconds: int = _DEFAULT_MAX_WAIT_SECONDS,
    fail_fast: bool = False,
) -> dict:
    """Splice in two Execute Workflow nodes, one before the main flow, one after."""
    nodes = template.setdefault("nodes", [])
    connections = template.setdefault("connections", {})

    if any(n.get("name") == _LOCK_ACQUIRE_NODE_NAME for n in nodes):
        raise SystemExit(f"Workflow already has a '{_LOCK_ACQUIRE_NODE_NAME}' node; refusing to add again")

    # Find the trigger (a node with no inbound connection — i.e. nobody references it)
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

    # Existing trigger's outbound connections
    trigger_out = connections.get(trigger_name, {}).get("main", [[]])
    first_branch = trigger_out[0] if trigger_out else []

    trigger_pos = trigger.get("position") or [240, 300]
    acquire_pos = [trigger_pos[0] + 220, trigger_pos[1]]

    # Push every other node 440 right (220 for acquire + 220 for spacing) so we have room
    for n in nodes:
        if n is trigger:
            continue
        pos = n.get("position") or [0, 0]
        n["position"] = [pos[0] + 440, pos[1]]

    # Normalize the user's scope expression to the canonical n8n form.
    normalized_scope, was_normalized = _normalize_n8n_expression(scope_expr)
    if was_normalized:
        print(
            f"WARNING: --scope-expression normalized to canonical form: {normalized_scope!r}. "
            "Bare '=<expr>' or literal scopes are auto-wrapped to '={{{{ <expr> }}}}'. "
            "Update calls to pass the canonical form directly to silence this warning.",
            file=sys.stderr,
        )

    # Acquire input contract — task-13 INCR + sidecar-meta primitive takes 8
    # fields. lock_id is a per-acquire UUID minted in Build Lock Context if not
    # supplied; we let the primitive default it. workflow_id/name flow through
    # so the meta sidecar carries identity for ownership-checked release and
    # active error-handler cleanup.
    acquire_inputs = {
        "scope": normalized_scope,
        "ttl_seconds": ttl_seconds,
        "execution_id": "={{ $execution.id }}",
        "wait_till_lock_released": not fail_fast,
        "max_wait_seconds": max_wait_seconds,
        "lock_id": "={{ $execution.id }}",
        "workflow_id": "={{ $workflow.id }}",
        "workflow_name": "={{ $workflow.name }}",
    }
    acquire = _make_execute_workflow_node(
        _LOCK_ACQUIRE_NODE_NAME,
        "{{@env:workflows.lock_acquisition.id}}",
        acquire_pos,
        acquire_inputs,
    )

    # Release input contract — task-13 ownership-checked: pass scope + lock_id.
    # The release primitive GETs the meta sidecar, compares lock_id, and DELs
    # only on match. lock_id matches what acquire used ($execution.id by default).
    release_pos = [trigger_pos[0] + 880, trigger_pos[1]]
    release_inputs = {
        "scope": normalized_scope,
        "lock_id": "={{ $execution.id }}",
    }
    release = _make_execute_workflow_node(
        _LOCK_RELEASE_NODE_NAME,
        "{{@env:workflows.lock_release.id}}",
        release_pos,
        release_inputs,
    )

    nodes.append(acquire)
    nodes.append(release)

    # Wire: trigger → acquire → (whatever was first) ... → release
    connections[trigger_name] = {"main": [[{"node": _LOCK_ACQUIRE_NODE_NAME, "type": "main", "index": 0}]]}
    connections[_LOCK_ACQUIRE_NODE_NAME] = {"main": [first_branch]} if first_branch else {"main": [[]]}

    # Find terminal node(s): nodes that have no outbound connection
    outbound_names = set(connections.keys())
    terminals = [n["name"] for n in nodes if n["name"] not in outbound_names and n["name"] not in (_LOCK_ACQUIRE_NODE_NAME, _LOCK_RELEASE_NODE_NAME, trigger_name)]
    if terminals:
        for t in terminals:
            connections[t] = {"main": [[{"node": _LOCK_RELEASE_NODE_NAME, "type": "main", "index": 0}]]}
    else:
        # No real downstream content — wire acquire directly to release
        connections[_LOCK_ACQUIRE_NODE_NAME] = {"main": [[{"node": _LOCK_RELEASE_NODE_NAME, "type": "main", "index": 0}]]}

    return template


def _extract_static_scope(scope_expr: str) -> str | None:
    """Return the static literal scope from a normalized expression, or None.

    Recognized static patterns:
      - Pure literals (no leading `=`): `"global"` → `"global"`.
      - Quoted literals inside `={{ "..." }}` or `={{ '...' }}`: `={{ "foo" }}` → `"foo"`.
    Anything else (template literals with `${...}`, `+ $json...`, function calls)
    is treated as dynamic and returns None.
    """
    if not scope_expr:
        return None
    s = scope_expr.strip()
    if not s.startswith("="):
        # pure literal (post-normalize this gets wrapped, but we handle pre-wrap too)
        return s
    # ={{ <expr> }} canonical form
    inner_match = re.match(r"^=\{\{\s*(.+?)\s*\}\}$", s, re.DOTALL)
    if not inner_match:
        return None
    inner = inner_match.group(1).strip()
    # Match a single-quoted or double-quoted string with NO concatenation / interpolation
    quote_match = re.match(r'^([\'"])(.*)\1$', inner, re.DOTALL)
    if not quote_match:
        return None
    literal = quote_match.group(2)
    # Reject if backticks/template-literals appear — those imply interpolation
    if "${" in literal:
        return None
    return literal


def _auto_register_lock_scopes(workspace: Path, scope_expr: str) -> None:
    """Append the static literal scope to every <env>.yml.lockScopes (idempotent)."""
    import re as _re  # local alias to keep this fn dependency-tight
    static = _extract_static_scope(scope_expr)
    if static is None:
        print(
            "  NOTE: --scope-expression is dynamic (depends on $json or runtime data). "
            "Active error-handler cleanup requires manual lockScopes maintenance — "
            "add the resolved scope strings to <env>.yml.lockScopes by hand.",
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
        scopes = data.setdefault("lockScopes", [])
        if not isinstance(scopes, list):
            scopes = []
            data["lockScopes"] = scopes
        if static not in scopes:
            scopes.append(static)
            yml.write_text(_yaml.dump(data, default_flow_style=False, sort_keys=False))
            print(f"  Registered lockScopes += {static!r} in {yml.name}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", default=None)
    parser.add_argument("--workflow-key", required=True, dest="workflow_key")
    parser.add_argument("--lock-on-error", action="store_true", dest="lock_on_error")
    parser.add_argument("--scope-expression", default="={{ $execution.id }}", dest="scope_expression")
    parser.add_argument(
        "--ttl-seconds",
        type=int,
        default=_DEFAULT_TTL_SECONDS,
        dest="ttl_seconds",
        help="Lock TTL in seconds (default 86400 = 24h). Set on Redis at acquire; bounds leak on crash.",
    )
    parser.add_argument(
        "--max-wait-seconds",
        type=int,
        default=_DEFAULT_MAX_WAIT_SECONDS,
        dest="max_wait_seconds",
        help="Wait-loop deadline in seconds (default 86400 = 24h). Override per-workflow if you need fail-fast-ish semantics for time-sensitive callers (e.g. webhooks).",
    )
    parser.add_argument(
        "--fail-fast",
        action="store_true",
        dest="fail_fast",
        help="Pass wait_till_lock_released=false; Stop and Error immediately if lock is held instead of waiting.",
    )
    args = parser.parse_args()

    ws = workspace_root(args.workspace)

    # Sanity: lock primitives must already exist in the workspace
    for prim in ("lock_acquisition", "lock_release"):
        if not (ws / "n8n-workflows-template" / f"{prim}.template.json").exists():
            print(f"ERROR: primitive '{prim}' not found in workspace. Run create-lock first.", file=sys.stderr)
            sys.exit(1)

    template_path = ws / "n8n-workflows-template" / f"{args.workflow_key}.template.json"
    if not template_path.exists():
        print(f"ERROR: workflow template not found: {template_path}", file=sys.stderr)
        sys.exit(1)

    template = json.loads(template_path.read_text())
    template = _insert_lock(
        template,
        args.scope_expression,
        ttl_seconds=args.ttl_seconds,
        max_wait_seconds=args.max_wait_seconds,
        fail_fast=args.fail_fast,
    )
    template_path.write_text(json.dumps(template, indent=2))
    print(f"  Inserted lock acquire/release in {template_path}")

    # Auto-register the static portion of the scope in <env>.yml.lockScopes so
    # the active error-handler cleanup can iterate it and DEL only the failed
    # execution's lock keys. Only static literals are appended — dynamic
    # expressions (anything containing $json or other runtime refs) are skipped
    # because there's no way to enumerate them from a static config.
    _auto_register_lock_scopes(ws, args.scope_expression)

    if args.lock_on_error:
        import subprocess
        cmd = [
            sys.executable,
            str(Path(__file__).parent / "register_error_handler.py"),
            "--workspace", str(ws),
            "--workflow-key", args.workflow_key,
            "--handler-key", "error_handler_lock_cleanup",
        ]
        r = subprocess.run(cmd, capture_output=True, text=True)
        print(r.stdout)
        if r.returncode != 0:
            print(r.stderr, file=sys.stderr)
            sys.exit(r.returncode)
    print("add-lock-to-workflow complete.")


if __name__ == "__main__":
    main()
