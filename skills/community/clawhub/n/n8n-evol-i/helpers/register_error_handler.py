#!/usr/bin/env python3
"""Wire a workflow's settings.errorWorkflow to point at an existing error-handler workflow."""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import yaml

from helpers.workspace import workspace_root


def _handler_exists(workspace: Path, handler_key: str) -> bool:
    cfg_dir = workspace / "n8n-config"
    if not cfg_dir.is_dir():
        return False
    for yml in cfg_dir.glob("*.yml"):
        if yml.stem in ("common", "deployment_order"):
            continue
        try:
            data = yaml.safe_load(yml.read_text()) or {}
            workflows = data.get("workflows") or {}
            if handler_key in workflows:
                return True
        except Exception:
            continue
    return False


def _update_error_source_map(workspace: Path, source_key: str, handler_key: str) -> None:
    """Append an entry to common.yml.error_source_to_handler if not present."""
    common = workspace / "n8n-config" / "common.yml"
    data: dict = {}
    if common.exists():
        data = yaml.safe_load(common.read_text()) or {}
    mapping = data.setdefault("error_source_to_handler", {}) or {}
    if mapping.get(source_key) != handler_key:
        mapping[source_key] = handler_key
        data["error_source_to_handler"] = mapping
        common.write_text(yaml.dump(data, default_flow_style=False, sort_keys=False))
        print(f"  Updated common.yml: error_source_to_handler.{source_key} = {handler_key}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", default=None)
    parser.add_argument("--workflow-key", required=True, dest="workflow_key")
    parser.add_argument("--handler-key", required=True, dest="handler_key")
    args = parser.parse_args()

    ws = workspace_root(args.workspace)
    if not _handler_exists(ws, args.handler_key):
        print(f"ERROR: handler '{args.handler_key}' not registered in any env YAML", file=sys.stderr)
        sys.exit(1)

    template = ws / "n8n-workflows-template" / f"{args.workflow_key}.template.json"
    if not template.exists():
        print(f"ERROR: template not found: {template}", file=sys.stderr)
        sys.exit(1)

    data = json.loads(template.read_text())
    settings = data.setdefault("settings", {})
    placeholder = "{{@env:workflows." + args.handler_key + ".id}}"
    settings["errorWorkflow"] = placeholder
    template.write_text(json.dumps(data, indent=2))
    print(f"  Wired {args.workflow_key}.settings.errorWorkflow → {placeholder}")

    _update_error_source_map(ws, args.workflow_key, args.handler_key)
    print(f"register-error-handler complete.")


if __name__ == "__main__":
    main()
