#!/usr/bin/env python3
"""Unarchive a previously-archived workflow on its env's n8n instance.

Wraps `POST /api/v1/workflows/{id}/unarchive`. Without this, an archived
workflow rejects all PUT updates with `400 {"message":"Cannot update an
archived workflow."}`.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from helpers.workspace import workspace_root
from helpers.config import load_yaml, load_env, get_config_value
from helpers.n8n_client import ensure_client


def _resolve_workflow_id(env_name: str, workflow_key: str, workspace: Path) -> str:
    data = load_yaml(env_name, workspace)
    try:
        return str(get_config_value(data, f"workflows.{workflow_key}.id"))
    except KeyError:
        raise SystemExit(
            f"No workflow id for key '{workflow_key}' in env '{env_name}'."
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", default=None)
    parser.add_argument("--env", required=True)
    parser.add_argument("--workflow-key", required=True, dest="workflow_key")
    args = parser.parse_args()

    ws = workspace_root(args.workspace)
    load_env(args.env, ws)
    wf_id = _resolve_workflow_id(args.env, args.workflow_key, ws)
    client = ensure_client(args.env, ws)
    client.post(f"workflows/{wf_id}/unarchive")
    print(f"Unarchived workflow '{args.workflow_key}' (id={wf_id}) on env '{args.env}'")


if __name__ == "__main__":
    main()
