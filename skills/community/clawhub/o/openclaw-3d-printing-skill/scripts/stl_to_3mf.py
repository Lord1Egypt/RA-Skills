#!/usr/bin/env python3
"""Convert STL files to 3MF for slicers that prefer 3MF containers."""

from __future__ import annotations

import argparse
import os
import sys

from mesh_io import load_mesh


def convert(stl_path: str, out_path: str | None = None) -> str:
    if out_path is None:
        out_path = os.path.splitext(stl_path)[0] + ".3mf"
    mesh = load_mesh(stl_path)
    mesh.export(out_path)
    return out_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert STL files to 3MF")
    parser.add_argument("stl_files", nargs="+", help="Input STL file(s)")
    parser.add_argument("--out", help="Optional output path for a single input STL")
    args = parser.parse_args()

    if args.out and len(args.stl_files) > 1:
        print("ERROR: --out only works with one input file", file=sys.stderr)
        return 2

    for stl_path in args.stl_files:
        if not os.path.exists(stl_path):
            print(f"ERROR: {stl_path} not found", file=sys.stderr)
            return 1
        try:
            out_path = convert(stl_path, args.out)
        except Exception as exc:  # pragma: no cover - runtime dependency path
            print(f"ERROR: {stl_path}: {exc}", file=sys.stderr)
            return 1
        print(f"{stl_path} -> {out_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
