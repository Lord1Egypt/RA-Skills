#!/usr/bin/env python3
"""Conservatively bootstrap a Junie-native .junie project layout."""
import argparse
import json
from pathlib import Path

DEFAULT_CONFIG = {
    "skill-default-locations": True,
    "command-default-locations": True,
    "agent-default-location": True,
    "model-default-locations": True,
    "mcp-default-locations": True,
    "auto-update": True,
}

AGENTS_TEMPLATE = """# Junie project guidance\n\nUse this file for persistent, project-specific instructions that Junie CLI should apply to tasks in this repo.\n\n- Prefer small, reviewable changes.\n- Explain any command that may mutate files before running it.\n- Keep secrets out of committed config.\n"""


def merge(base, patch):
    if isinstance(base, dict) and isinstance(patch, dict):
        result = dict(base)
        for key, value in patch.items():
            result[key] = merge(result[key], value) if key in result else value
        return result
    return patch


def read_object(path: Path) -> dict:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description="Bootstrap a Junie-native .junie layout without overwriting user content.")
    parser.add_argument("project", nargs="?", default=".", help="Project root to bootstrap. Defaults to current directory.")
    parser.add_argument("--model", help="Optional default model to add to .junie/config.json.")
    parser.add_argument("--guidelines-location", help="Optional guidelines-location value for .junie/config.json.")
    parser.add_argument("--config", help="Optional JSON object to merge into .junie/config.json.")
    parser.add_argument("--force-agents", action="store_true", help="Overwrite .junie/AGENTS.md with the default template.")
    args = parser.parse_args()

    root = Path(args.project).expanduser().resolve()
    junie_dir = root / ".junie"
    junie_dir.mkdir(parents=True, exist_ok=True)

    for name in ["skills", "commands", "agents", "models", "mcp", "rules"]:
        (junie_dir / name).mkdir(exist_ok=True)

    agents_path = junie_dir / "AGENTS.md"
    if args.force_agents or not agents_path.exists():
        agents_path.write_text(AGENTS_TEMPLATE, encoding="utf-8")

    patch = dict(DEFAULT_CONFIG)
    if args.model:
        patch["model"] = args.model
    if args.guidelines_location:
        patch["guidelines-location"] = args.guidelines_location
    if args.config:
        extra = json.loads(args.config)
        if not isinstance(extra, dict):
            raise ValueError("--config must be a JSON object")
        patch = merge(patch, extra)

    config_path = junie_dir / "config.json"
    existing = read_object(config_path)
    merged = merge(existing, patch)
    config_path.write_text(json.dumps(merged, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(junie_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
