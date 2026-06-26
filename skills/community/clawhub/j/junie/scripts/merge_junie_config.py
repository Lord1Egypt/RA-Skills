#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path


def usage() -> None:
    print(
        "Usage: merge_junie_config.py <config-path> <json-patch>\n"
        "\n"
        "Example:\n"
        "  merge_junie_config.py ~/.junie/config.json '{\"model\":\"sonnet\",\"auto-update\":true}'\n"
    )


def merge(base, patch):
    if isinstance(base, dict) and isinstance(patch, dict):
        result = dict(base)
        for key, value in patch.items():
            if key in result:
                result[key] = merge(result[key], value)
            else:
                result[key] = value
        return result
    return patch


def main() -> int:
    if len(sys.argv) != 3:
        usage()
        return 2

    raw_path = os.path.expanduser(sys.argv[1])
    config_path = Path(raw_path)

    try:
        patch = json.loads(sys.argv[2])
    except json.JSONDecodeError as exc:
        print(f"Invalid JSON patch: {exc}", file=sys.stderr)
        return 2

    if not isinstance(patch, dict):
        print("Patch must be a JSON object", file=sys.stderr)
        return 2

    existing = {}
    if config_path.exists():
        try:
            existing = json.loads(config_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            print(f"Existing config is not valid JSON: {exc}", file=sys.stderr)
            return 1
        if not isinstance(existing, dict):
            print("Existing config must be a JSON object", file=sys.stderr)
            return 1

    merged = merge(existing, patch)

    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(merged, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(str(config_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
