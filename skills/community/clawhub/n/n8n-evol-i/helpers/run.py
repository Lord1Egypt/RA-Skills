#!/usr/bin/env python3
"""Fire a workflow's webhook (or its paired error-source) and poll for terminal status."""
import argparse
import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import requests

from helpers.workspace import workspace_root
from helpers.config import load_yaml, load_env, load_common, get_config_value
from helpers.n8n_client import ensure_client


def _find_webhook_path(workflow: dict) -> str | None:
    """Find the first webhook node in a workflow; return its path or None."""
    for node in workflow.get("nodes", []):
        if str(node.get("type", "")).endswith(".webhook"):
            params = node.get("parameters") or {}
            return params.get("path")
    return None


def _fire_webhook_and_poll(workspace: Path, env_name: str, workflow_key: str, payload: dict, timeout: int) -> dict:
    """POST to the workflow's webhook, then poll executions for the terminal result."""
    yaml_data = load_yaml(env_name, workspace)
    wf_id = str(get_config_value(yaml_data, f"workflows.{workflow_key}.id"))
    instance = yaml_data.get("n8n", {}).get("instanceName", "")
    base_url = instance if instance.startswith("http") else f"https://{instance.rstrip('/')}"

    client = ensure_client(env_name, workspace)
    workflow = client.get_workflow(wf_id)
    path = _find_webhook_path(workflow)
    if not path:
        raise SystemExit(f"Workflow '{workflow_key}' has no webhook node; cannot fire directly")

    fire_started_at = time.time()
    webhook_url = f"{base_url}/webhook/{path}"
    test_url = f"{base_url}/webhook-test/{path}"

    fired = False
    last_err = None
    for url in (webhook_url, test_url):
        try:
            r = requests.post(url, json=payload, timeout=timeout)
            if r.status_code < 500:
                fired = True
                break
            last_err = f"{url} → {r.status_code} {r.text[:200]}"
        except Exception as e:
            last_err = f"{url} → {e}"
    if not fired:
        raise SystemExit(f"Could not fire webhook for '{workflow_key}': {last_err}")

    return _poll_for_execution(client, wf_id, fire_started_at, timeout)


def _fire_via_error_source(workspace: Path, env_name: str, handler_key: str, payload: dict, timeout: int) -> dict:
    """Indirect dispatch: find the source workflow paired with the handler, fire it, poll the handler."""
    common = load_common(workspace)
    mapping = common.get("error_source_to_handler") or {}
    source_key = next((s for s, h in mapping.items() if h == handler_key), None)
    if not source_key:
        raise SystemExit(
            f"No source workflow paired with handler '{handler_key}' in n8n-config/common.yml.\n"
            f"Use register-workflow-to-error-handler to set up the pairing."
        )
    yaml_data = load_yaml(env_name, workspace)
    handler_id = str(get_config_value(yaml_data, f"workflows.{handler_key}.id"))

    fire_started_at = time.time()
    # Fire the source workflow (which is supposed to error and route to handler)
    try:
        _fire_webhook_and_poll(workspace, env_name, source_key, payload, timeout)
    except SystemExit:
        pass  # source workflow erroring is the expected dispatch path
    # Poll the handler's executions
    client = ensure_client(env_name, workspace)
    return _poll_for_execution(client, handler_id, fire_started_at, timeout)


def _poll_for_execution(client, workflow_id: str, started_at: float, timeout: int) -> dict:
    """Poll /executions for a terminal record with `workflowId == workflow_id` started after started_at."""
    deadline = started_at + timeout
    last_id = None
    while time.time() < deadline:
        try:
            execs = client.get("executions", params={"workflowId": workflow_id, "limit": 5})
            data = execs.get("data") or []
            for ex in data:
                # Match started after our fire
                started_at_str = ex.get("startedAt") or ""
                # Best-effort: parse ISO 8601
                try:
                    from datetime import datetime
                    ts = datetime.fromisoformat(started_at_str.replace("Z", "+00:00")).timestamp()
                except Exception:
                    ts = started_at  # fall back to "any execution"
                if ts >= started_at - 1:
                    if ex.get("finished"):
                        # Get full execution
                        full = client.get(f"executions/{ex['id']}", params={"includeData": "true"})
                        return full
                    last_id = ex.get("id")
        except Exception:
            pass
        time.sleep(1)
    raise SystemExit(f"Timeout waiting for terminal execution of workflow {workflow_id} (last seen={last_id})")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", default=None)
    parser.add_argument("--env", required=True)
    parser.add_argument("--workflow-key", required=True, dest="workflow_key")
    parser.add_argument("--payload", default="{}", help="JSON payload to POST to the webhook")
    parser.add_argument("--expect-status", default=None, dest="expect_status",
                        choices=("success", "error", "canceled", None))
    parser.add_argument("--timeout", type=int, default=30)
    args = parser.parse_args()

    ws = workspace_root(args.workspace)
    load_env(args.env, ws)
    payload = json.loads(args.payload)

    common = load_common(ws)
    mapping = common.get("error_source_to_handler") or {}

    if args.workflow_key in mapping.values():
        # Indirect dispatch — workflow_key is a handler
        ex = _fire_via_error_source(ws, args.env, args.workflow_key, payload, args.timeout)
    else:
        ex = _fire_webhook_and_poll(ws, args.env, args.workflow_key, payload, args.timeout)

    status = ex.get("status") or ("error" if ex.get("stoppedAt") and not ex.get("finished") else "success")
    print(json.dumps({"id": ex.get("id"), "status": status, "finished": ex.get("finished")}, indent=2))

    if args.expect_status and status != args.expect_status:
        print(f"FAIL: expected status='{args.expect_status}', got '{status}'", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
