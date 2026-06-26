#!/usr/bin/env python3
"""Compatibility wrapper for write_starter_profile.py."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from write_starter_profile import ROLE_DATA, write_bundle


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--kind", default="generic", choices=sorted(ROLE_DATA.keys()))
    args = parser.parse_args()

    workspace = Path(args.workspace)
    workspace.mkdir(parents=True, exist_ok=True)
    written = write_bundle(workspace, args.name, args.kind)
    print(
        json.dumps(
            {
                "note": "Compatibility wrapper: this command now writes the full starter profile bundle.",
                "written_files": [str(path) for path in written],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
