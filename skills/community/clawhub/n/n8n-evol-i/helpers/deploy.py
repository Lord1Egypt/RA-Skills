#!/usr/bin/env python3
"""Hydrate, PUT to n8n, and (by default) activate a workflow."""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from helpers.workspace import workspace_root
from helpers.config import load_yaml, load_env, get_config_value
from helpers.n8n_client import ensure_client, redact_for_debug
from helpers.validate import validate_workflow_json


_PUT_FIELDS = ("name", "nodes", "connections", "settings", "staticData")

# Triggers that can stand alone (and thus support the /activate endpoint).
# Sub-workflow triggers (executeWorkflowTrigger, errorTrigger) cannot be activated alone.
_ACTIVATABLE_TRIGGER_TYPES = (
    "n8n-nodes-base.webhook",
    "n8n-nodes-base.scheduleTrigger",
    "n8n-nodes-base.cron",
    "n8n-nodes-base.formTrigger",
    "n8n-nodes-base.emailReadImap",
    "n8n-nodes-base.manualTrigger",
    "n8n-nodes-base.errorTrigger",  # Error Trigger workflows DO need activation
)


def _filter_for_put(data: dict) -> dict:
    """n8n's PUT /workflows/{id} accepts only certain fields; drop the rest."""
    return {k: data[k] for k in _PUT_FIELDS if k in data}


def _has_activatable_trigger(workflow: dict) -> bool:
    """A workflow with only ExecuteWorkflowTrigger cannot be activated."""
    for node in workflow.get("nodes", []):
        ntype = node.get("type", "")
        if ntype in _ACTIVATABLE_TRIGGER_TYPES:
            return True
        # Heuristic: any node whose type ends in 'Trigger' BUT isn't a sub-workflow trigger
        if ntype.endswith("Trigger") and ntype != "n8n-nodes-base.executeWorkflowTrigger":
            return True
    return False


def _resolve_workflow_id(env_name: str, workflow_key: str, workspace: Path) -> str:
    data = load_yaml(env_name, workspace)
    try:
        return str(get_config_value(data, f"workflows.{workflow_key}.id"))
    except KeyError:
        raise SystemExit(f"No workflow id for key '{workflow_key}' in env '{env_name}'.")


def _write_debug(env_name: str, workflow_key: str, payload: dict, response, stage: str) -> None:
    debug_dir = Path.home() / ".cache" / "n8n-evol-I" / "debug" / str(os.getpid())
    debug_dir.mkdir(parents=True, exist_ok=True)
    seq = len(list(debug_dir.glob(f"deploy-*.json"))) + 1
    out = debug_dir / f"deploy-{seq:03d}.json"
    blob = {
        "env": env_name,
        "workflow_key": workflow_key,
        "stage": stage,
        "payload": redact_for_debug(payload),
        "response": redact_for_debug(response if isinstance(response, (dict, list)) else str(response)),
    }
    out.write_text(json.dumps(blob, indent=2))
    out.chmod(0o600)
    print(f"  Debug artifact: {out}", file=sys.stderr)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", default=None)
    parser.add_argument("--env", required=True)
    parser.add_argument("--workflow-key", required=True, dest="workflow_key")
    parser.add_argument("--no-activate", action="store_true")
    parser.add_argument("--rehydrate", action="store_true", help="Re-hydrate before deploy even if generated JSON exists")
    parser.add_argument("--debug", action="store_true", help="Dump redacted pre/post hydration + request/response")
    args = parser.parse_args()

    ws = workspace_root(args.workspace)

    template_path = ws / "n8n-workflows-template" / f"{args.workflow_key}.template.json"
    if not template_path.exists():
        print(f"ERROR: template not found: {template_path}", file=sys.stderr)
        sys.exit(1)
    template_text = template_path.read_text(encoding="utf-8")
    valid, errors = validate_workflow_json(template_text, source="template", workspace=ws)
    if not valid:
        print("ERROR: template validation failed (deploy aborted):", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)

    generated = ws / "n8n-build" / args.env / f"{args.workflow_key}.generated.json"

    if args.rehydrate or not generated.exists():
        # Compose with hydrate.py as a subprocess
        cmd = [
            sys.executable,
            str(Path(__file__).parent / "hydrate.py"),
            "--workspace", str(ws),
            "--env", args.env,
            "--workflow-key", args.workflow_key,
        ]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stdout, file=sys.stderr)
            print(r.stderr, file=sys.stderr)
            sys.exit(r.returncode)

    if not generated.exists():
        print(f"ERROR: generated file missing after hydrate: {generated}", file=sys.stderr)
        sys.exit(1)

    payload_full = json.loads(generated.read_text())
    payload = _filter_for_put(payload_full)

    load_env(args.env, ws)
    wf_id = _resolve_workflow_id(args.env, args.workflow_key, ws)
    client = ensure_client(args.env, ws)

    resp = client.put(f"workflows/{wf_id}", payload)
    if args.debug:
        _write_debug(args.env, args.workflow_key, payload, resp, "put")
    print(f"Deployed workflow '{args.workflow_key}' (id={wf_id}) on env '{args.env}'")

    if not args.no_activate:
        try:
            act_resp = client.post(f"workflows/{wf_id}/activate")
            if args.debug:
                _write_debug(args.env, args.workflow_key, {}, act_resp, "activate")
            print(f"Activated workflow '{args.workflow_key}'")
        except Exception as e:
            # The PUT (deploy) succeeded — only the trigger flip failed. Common
            # causes: a sub-workflow target isn't yet activated (n8n Cloud
            # rejects with "Cannot publish workflow: Node X references workflow
            # Y which is not published"), invalid credential ref, etc.
            #
            # Severity policy (per task #9 deploy_all decision): exit code 2
            # signals "deployed-but-not-activated" — distinct from PUT failure
            # (1). deploy_all treats 2 as warn-and-continue by default and 1
            # as tier-stop. Use --strict-activate on deploy_all to escalate 2
            # to fail-fast.
            print(f"WARNING: activate failed for '{args.workflow_key}': {e}", file=sys.stderr)
            sys.exit(2)


if __name__ == "__main__":
    main()
