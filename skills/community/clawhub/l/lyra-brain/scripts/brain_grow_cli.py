#!/usr/bin/env python3
"""Grow one compact memory line into 3-brain graph. Requires --i-consent (v2.1.0)."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from _lyra_core_paths import lyra_core_root

_SECRETISH = re.compile(
    r"(?i)(api[_-]?key|secret|password|token|private[_-]?key|moltx_sk_|sk-|xai-|nvapi-)\s*[:=]"
)


def main() -> int:
    ap = argparse.ArgumentParser(description="Grow into LYRA graph (persistent; consent required)")
    ap.add_argument(
        "--i-consent",
        action="store_true",
        help="Required: confirm persistent graph/memory write under LYRA_CORE_ROOT",
    )
    ap.add_argument("text", nargs="?", help="Snip to grow (or --file)")
    ap.add_argument("--file", help="Read snip from file")
    ap.add_argument("--source", default="lyra-brain-skill", help="grow() source tag")
    args = ap.parse_args()

    if not args.i_consent:
        print(
            "REFUSED: graph grow requires --i-consent "
            "(writes under LYRA_CORE_ROOT — persistent storage).",
            file=sys.stderr,
        )
        return 2

    text = args.text
    if args.file:
        text = Path(args.file).read_text(encoding="utf-8").strip()
    if not text:
        ap.error("Provide text or --file")

    if _SECRETISH.search(text):
        print("REFUSED: text looks like it contains credentials.", file=sys.stderr)
        return 2

    root = lyra_core_root()
    sys.path.insert(0, str(root / "modules"))
    import seals as seals_mod  # noqa: E402
    import lyra_brain  # noqa: E402

    idx = seals_mod.build_index()
    brain = lyra_brain.LyraThreeBrainMemory(base_dir=root, seal_index=idx, use_advanced=True)
    nid = brain.grow(text[:2000], source=args.source)
    print(nid)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
