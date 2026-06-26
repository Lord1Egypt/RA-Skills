#!/usr/bin/env python3
"""Rebuild the local persona index from persona directories.

Usage:
    python3 rebuild-index.py <personas_dir>

Scans each subdirectory of <personas_dir> for persona.json,
reads it, tags it as local, and writes index.json.
"""

import json
import os
import sys


def main():
    if len(sys.argv) < 2:
        print("Usage: rebuild-index.py <personas_dir>", file=sys.stderr)
        sys.exit(1)

    personas_dir = os.path.expanduser(sys.argv[1])
    if not os.path.isdir(personas_dir):
        print(f"Not a directory: {personas_dir}", file=sys.stderr)
        sys.exit(1)

    personas = []
    for entry in sorted(os.listdir(personas_dir)):
        entry_path = os.path.join(personas_dir, entry)
        if not os.path.isdir(entry_path):
            continue
        if entry.startswith("_") or entry.startswith("."):
            continue

        meta_path = os.path.join(entry_path, "persona.json")
        if not os.path.isfile(meta_path):
            print(f"  skip {entry}/ (no persona.json)", file=sys.stderr)
            continue

        try:
            with open(meta_path, "r") as f:
                meta = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            print(f"  skip {entry}/ ({e})", file=sys.stderr)
            continue

        # Verify minimum fields
        if "handle" not in meta or "name" not in meta:
            print(f"  skip {entry}/ (missing handle or name)", file=sys.stderr)
            continue

        # Check which files exist
        files = {}
        for fname in ["SOUL.md", "IDENTITY.md", "avatar.png"]:
            fpath = os.path.join(entry_path, fname)
            if os.path.isfile(fpath):
                files[fname.split(".")[0].lower()] = fname

        meta["local"] = True
        meta["files_present"] = files
        personas.append(meta)

    index = {
        "total": len(personas),
        "personas": personas,
    }

    index_path = os.path.join(personas_dir, "index.json")
    with open(index_path, "w") as f:
        json.dump(index, f, indent=2)

    print(f"Wrote {len(personas)} personas to {index_path}")


if __name__ == "__main__":
    main()
