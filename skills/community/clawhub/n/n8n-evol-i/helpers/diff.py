#!/usr/bin/env python3
"""Diff a hydrated build vs the live workflow on n8n, ignoring volatile fields."""
import argparse
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent))

from helpers.workspace import workspace_root
from helpers.config import load_yaml, load_env, get_config_value
from helpers.n8n_client import ensure_client


_DIFF_IGNORE = frozenset({
    "id", "active", "versionId", "createdAt", "updatedAt",
    "tags", "shared", "isArchived", "triggerCount", "homeProject",
    "scopes", "meta", "usedCredentials", "sharedWithProjects",
    "pinData", "webhookId",
})


def _canon(data: Any) -> Any:
    """Strip volatile fields recursively from a workflow dict."""
    if isinstance(data, dict):
        return {k: _canon(v) for k, v in sorted(data.items()) if k not in _DIFF_IGNORE}
    if isinstance(data, list):
        return [_canon(item) for item in data]
    return data


def _diff(left: Any, right: Any, path: str = "") -> list[str]:
    """Yield human-readable diff lines for two structures."""
    out: list[str] = []
    if type(left) is not type(right):
        out.append(f"{path}: type {type(left).__name__} vs {type(right).__name__}")
        return out
    if isinstance(left, dict):
        for k in sorted(set(left) | set(right)):
            sub = f"{path}.{k}" if path else k
            if k not in left:
                out.append(f"{sub}: only on right ({right[k]!r})")
            elif k not in right:
                out.append(f"{sub}: only on left ({left[k]!r})")
            else:
                out.extend(_diff(left[k], right[k], sub))
    elif isinstance(left, list):
        if len(left) != len(right):
            out.append(f"{path}: length {len(left)} vs {len(right)}")
        else:
            for i, (l_item, r_item) in enumerate(zip(left, right)):
                out.extend(_diff(l_item, r_item, f"{path}[{i}]"))
    else:
        if left != right:
            out.append(f"{path}: {left!r} vs {right!r}")
    return out


def workflow_semantic_diff(left: dict, right: dict) -> list[str]:
    """Return human-readable diff lines between two workflow dicts."""
    return _diff(_canon(left), _canon(right))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", default=None)
    parser.add_argument("--env", required=True)
    parser.add_argument("--workflow-key", required=True, dest="workflow_key")
    args = parser.parse_args()

    ws = workspace_root(args.workspace)
    load_env(args.env, ws)
    yaml_data = load_yaml(args.env, ws)
    wf_id = str(get_config_value(yaml_data, f"workflows.{args.workflow_key}.id"))

    built = ws / "n8n-build" / args.env / f"{args.workflow_key}.generated.json"
    if not built.exists():
        print(f"ERROR: no built JSON at {built}; run hydrate first", file=sys.stderr)
        sys.exit(1)

    client = ensure_client(args.env, ws)
    live = client.get_workflow(wf_id)
    local = json.loads(built.read_text())

    lines = workflow_semantic_diff(local, live)
    if not lines:
        print("(empty diff)")
        sys.exit(0)
    for line in lines:
        print(line)
    sys.exit(1 if lines else 0)


if __name__ == "__main__":
    main()
