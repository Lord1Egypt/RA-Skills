#!/usr/bin/env python3
"""Pull live workflow state from n8n and rewrite the template."""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from helpers.workspace import workspace_root
from helpers.config import load_yaml, load_env, get_config_value
from helpers.n8n_client import ensure_client
from helpers.dehydrate import dehydrate_data


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", default=None)
    parser.add_argument("--env", required=True)
    parser.add_argument("--workflow-key", required=True, dest="workflow_key")
    args = parser.parse_args()

    ws = workspace_root(args.workspace)
    load_env(args.env, ws)
    yaml_data = load_yaml(args.env, ws)
    try:
        wf_id = str(get_config_value(yaml_data, f"workflows.{args.workflow_key}.id"))
    except KeyError:
        print(f"ERROR: no workflow id for key '{args.workflow_key}' in env '{args.env}'", file=sys.stderr)
        sys.exit(1)

    client = ensure_client(args.env, ws)
    raw = client.get_workflow(wf_id)
    text = dehydrate_data(raw, args.env, ws, args.workflow_key)

    out_dir = ws / "n8n-workflows-template"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{args.workflow_key}.template.json"
    out_file.write_text(text)
    print(f"Resynced workflow '{args.workflow_key}' from env '{args.env}' → {out_file}")


if __name__ == "__main__":
    main()
