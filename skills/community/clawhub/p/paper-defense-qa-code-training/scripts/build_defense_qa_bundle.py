#!/usr/bin/env python3
"""Build a zip bundle for a paper-defense Q&A directory.

Usage:
  python scripts/build_defense_qa_bundle.py --root ./paper_defense_bundle --output ./paper_defense_bundle.zip
"""

from __future__ import annotations

import argparse
import zipfile
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="paper_defense_bundle")
    parser.add_argument("--output", default="paper_defense_bundle.zip")
    args = parser.parse_args()

    root = Path(args.root)
    output = Path(args.output)
    if not root.exists():
        raise SystemExit(f"Root does not exist: {root}")

    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(root.rglob("*")):
            if path.is_file():
                zf.write(path, path.relative_to(root.parent if root.parent != Path("") else root))

    print(f"Wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
