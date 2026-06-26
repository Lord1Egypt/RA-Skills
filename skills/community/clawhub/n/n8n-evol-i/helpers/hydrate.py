#!/usr/bin/env python3
"""Resolve all {{INTERPOLATE_...}} / {{@...}} placeholders in a workflow template for one env."""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from helpers.workspace import workspace_root, ensure_workspace
from helpers.placeholder import env_resolver, file_resolver, js_resolver, py_resolver, uuid_resolver, validator


def hydrate(env_name: str, workflow_key: str, workspace: Path, strict: bool = False) -> Path:
    """Hydrate a template and return the path to the generated JSON."""
    ensure_workspace(workspace)

    template_dir = workspace / "n8n-workflows-template"
    template_file = template_dir / f"{workflow_key}.template.json"
    if not template_file.exists():
        raise FileNotFoundError(f"Template not found: {template_file}")

    text = template_file.read_text(encoding="utf-8")

    # Run resolvers in order
    text = env_resolver.resolve(text, env_name, workspace)
    text = file_resolver.resolve(text, workspace)
    text = js_resolver.resolve(text, workspace)
    text = py_resolver.resolve(text, workspace)
    text = uuid_resolver.resolve(text)

    # Validate no residuals
    validator.validate_no_absolute_paths(text)
    residuals = validator.check_residuals(text)
    if residuals:
        if strict:
            raise ValueError(
                f"Residual placeholders after hydration in '{workflow_key}':\n"
                + "\n".join(f"  {r}" for r in residuals)
            )
        else:
            print(f"WARNING: {len(residuals)} residual placeholder(s) in '{workflow_key}': {residuals}", file=sys.stderr)

    # Validate JSON parses
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Generated JSON is invalid for '{workflow_key}': {e}")

    out_dir = workspace / "n8n-build" / env_name
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{workflow_key}.generated.json"
    out_file.write_text(json.dumps(data, indent=2))
    return out_file


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", default=None)
    parser.add_argument("--env", required=True)
    parser.add_argument("--workflow-key", required=True, dest="workflow_key")
    parser.add_argument("--strict", action="store_true", help="Error (not warn) on residual placeholders")
    args = parser.parse_args()

    ws = workspace_root(args.workspace)
    out = hydrate(args.env, args.workflow_key, ws, strict=args.strict)
    print(f"Hydrated: {out}")


if __name__ == "__main__":
    main()
