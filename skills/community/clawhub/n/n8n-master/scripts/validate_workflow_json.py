#!/usr/bin/env python3
"""Validate the basic shape of an n8n workflow JSON file."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REQUIRED_TOP_LEVEL = {"name", "nodes", "connections", "settings", "active"}
REQUIRED_NODE_FIELDS = {"name", "type", "parameters", "position"}


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        workflow = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - CLI should report parse errors plainly.
        return [f"Could not read JSON: {exc}"]

    if not isinstance(workflow, dict):
        return ["Workflow must be a JSON object."]

    missing = REQUIRED_TOP_LEVEL - set(workflow)
    if missing:
        errors.append(f"Missing top-level keys: {', '.join(sorted(missing))}")

    nodes = workflow.get("nodes")
    if not isinstance(nodes, list):
        errors.append("`nodes` must be an array.")
        return errors

    names: set[str] = set()
    for index, node in enumerate(nodes):
        if not isinstance(node, dict):
            errors.append(f"Node #{index} must be an object.")
            continue
        missing_node = REQUIRED_NODE_FIELDS - set(node)
        if missing_node:
            errors.append(
                f"Node #{index} missing fields: {', '.join(sorted(missing_node))}"
            )
        name = node.get("name")
        if isinstance(name, str):
            if name in names:
                errors.append(f"Duplicate node name: {name}")
            names.add(name)
        if "position" in node:
            pos = node["position"]
            if not (
                isinstance(pos, list)
                and len(pos) == 2
                and all(isinstance(value, (int, float)) for value in pos)
            ):
                errors.append(f"Node {name or index} has invalid position.")

    if workflow.get("active") is not False:
        errors.append("Recommended: `active` should be false for generated imports.")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workflow_json", type=Path)
    args = parser.parse_args()

    errors = validate(args.workflow_json)
    if errors:
        print("Invalid n8n workflow JSON:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Valid basic n8n workflow JSON shape.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

