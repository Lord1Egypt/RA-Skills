#!/usr/bin/env python3
"""Stop n8n executions matching a status filter (and optional --workflow-key scope).

Two-phase:
  1. GET /api/v1/executions per workflow (list candidates) so the caller sees what would be stopped.
  2. POST /api/v1/executions/stop with the matching status set (and workflowId if scoped).

Without `--force`, the helper prints the candidate list and exits 0 with
"Rerun with --force to stop these executions." — never prompts interactively
(agents run non-TTY).

`--status running,waiting,queued` is a comma-separated list. n8n's POST stop endpoint
accepts a status array; the helper passes it through verbatim.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from helpers.workspace import workspace_root
from helpers.config import load_yaml, load_env, get_config_value
from helpers.n8n_client import ensure_client, N8nClient


_STATUS_CHOICES = ("error", "success", "running", "canceled", "waiting", "crashed", "queued")
_DEFAULT_STATUSES = "running,waiting,queued"


def _parse_status_list(raw: str) -> list[str]:
    """Split a comma-separated status list and validate each entry."""
    parts = [p.strip() for p in (raw or "").split(",") if p.strip()]
    bad = [p for p in parts if p not in _STATUS_CHOICES]
    if bad:
        raise SystemExit(f"Unknown status value(s): {bad}. Choices: {list(_STATUS_CHOICES)}")
    return parts


def _resolve_workflow_id(yaml_data: dict, workflow_key: str) -> str:
    return str(get_config_value(yaml_data, f"workflows.{workflow_key}.id"))


def _list_workflow_ids(client: N8nClient) -> list[str]:
    return [str(wf.get("id")) for wf in client.list_workflows() if wf.get("id")]


def _list_candidates(client: N8nClient, workflow_ids: list[str], statuses: list[str]) -> list[dict]:
    """Per-workflow GET /executions for each requested status; flatten and return rows."""
    out: list[dict] = []
    for wid in workflow_ids:
        for status in statuses:
            cursor = None
            while True:
                params: dict = {"workflowId": wid, "status": status, "limit": 250}
                if cursor:
                    params["cursor"] = cursor
                resp = client.get("executions", params=params)
                rows = resp.get("data") or []
                out.extend(rows)
                cursor = resp.get("nextCursor")
                if not cursor:
                    break
    return out


def _summarize(candidates: list[dict]) -> dict:
    """Group candidates by status for the dry-run output."""
    by_status: dict = {}
    for row in candidates:
        st = row.get("status", "unknown")
        by_status.setdefault(st, []).append(row.get("id"))
    return {"total": len(candidates), "by_status": {k: sorted(v) for k, v in sorted(by_status.items())}}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", default=None)
    parser.add_argument("--env", required=True)
    parser.add_argument("--workflow-key", default=None, dest="workflow_key",
                        help="Yaml key; if omitted, scope is the whole env (every workflow).")
    parser.add_argument("--status", default=_DEFAULT_STATUSES,
                        help=f"Comma-separated statuses to stop. Default: {_DEFAULT_STATUSES}")
    parser.add_argument("--force", action="store_true",
                        help="Actually issue the POST /executions/stop. Without --force, exit 0 with the candidate list.")
    args = parser.parse_args()

    ws = workspace_root(args.workspace)
    yaml_data = load_yaml(args.env, ws)
    load_env(args.env, ws)
    client = ensure_client(args.env, ws)

    statuses = _parse_status_list(args.status)
    if args.workflow_key:
        workflow_ids = [_resolve_workflow_id(yaml_data, args.workflow_key)]
    else:
        workflow_ids = _list_workflow_ids(client)

    candidates = _list_candidates(client, workflow_ids, statuses)
    summary = _summarize(candidates)

    if not args.force:
        result = {
            "dry_run": True,
            "candidates": summary,
            "message": "Rerun with --force to stop these executions.",
        }
        print(json.dumps(result, indent=2))
        return

    if not candidates:
        print(json.dumps({"stopped": [], "message": "No candidates matched."}, indent=2))
        return

    body: dict = {"status": statuses}
    if args.workflow_key:
        body["workflowId"] = workflow_ids[0]

    resp = client.post("executions/stop", body)
    result = {
        "stopped": summary,
        "n8n_response": resp,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
