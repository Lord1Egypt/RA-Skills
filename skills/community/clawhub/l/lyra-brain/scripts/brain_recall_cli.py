#!/usr/bin/env python3
"""Recall from 3-brain graph (compact CLI)."""
import argparse
import json
import sys

from _lyra_core_paths import lyra_core_root


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("--mode", default="balanced")
    ap.add_argument("--limit", type=int, default=8)
    args = ap.parse_args()

    root = lyra_core_root()
    sys.path.insert(0, str(root / "modules"))
    import seals as seals_mod  # noqa: E402
    import lyra_brain  # noqa: E402

    idx = seals_mod.build_index()
    brain = lyra_brain.LyraThreeBrainMemory(base_dir=root, seal_index=idx, use_advanced=True)
    res = brain.recall(args.query, mode=args.mode, max_results=args.limit)
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()