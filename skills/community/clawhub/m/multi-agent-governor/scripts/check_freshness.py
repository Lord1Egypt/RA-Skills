#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys

from _common import load_manifest, path_record


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify source and build artifact hashes.")
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--include-sources", action="store_true")
    args = parser.parse_args()

    _, manifest = load_manifest(args.manifest)
    expected = list(manifest["build"].get("artifacts", []))
    if args.include_sources:
        expected += manifest.get("sources", [])
    if not expected:
        parser.error("manifest has no artifacts to verify")

    results = []
    stale = False
    for record in expected:
        try:
            current = path_record(record["path"])
            matches = current["sha256"] == record["sha256"]
        except FileNotFoundError:
            current = None
            matches = False
        stale = stale or not matches
        results.append({
            "path": record["path"],
            "expected_sha256": record["sha256"],
            "current_sha256": current["sha256"] if current else None,
            "fresh": matches,
        })
    print(json.dumps({"build_id": manifest["build"].get("id"), "fresh": not stale, "results": results}, indent=2))
    if stale:
        sys.exit(1)


if __name__ == "__main__":
    main()
