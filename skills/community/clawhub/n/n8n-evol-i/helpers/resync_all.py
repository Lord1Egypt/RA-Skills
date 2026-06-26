#!/usr/bin/env python3
"""Resync every workflow registered in an env's YAML."""
import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from helpers.workspace import workspace_root
from helpers.config import load_yaml


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", default=None)
    parser.add_argument("--env", required=True)
    args = parser.parse_args()

    ws = workspace_root(args.workspace)
    yaml_data = load_yaml(args.env, ws)
    workflows = yaml_data.get("workflows") or {}
    helpers = Path(__file__).parent

    failures: list[tuple[str, int]] = []
    for key in sorted(workflows.keys()):
        cmd = [sys.executable, str(helpers / "resync.py"),
               "--workspace", str(ws), "--env", args.env, "--workflow-key", key]
        r = subprocess.run(cmd)
        if r.returncode != 0:
            failures.append((key, r.returncode))

    if failures:
        print(f"resync_all complete with {len(failures)} failure(s): {failures}", file=sys.stderr)
        sys.exit(1)
    print("resync_all complete.")


if __name__ == "__main__":
    main()
