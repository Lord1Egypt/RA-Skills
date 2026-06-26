#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


def main():
    if len(sys.argv) != 3:
        print("Usage: canonicalize_deduped.py <deduped.json> <out.jsonl>", file=sys.stderr)
        sys.exit(2)

    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    out = Path(sys.argv[2])
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for group in data:
            f.write(json.dumps(group["canonical"], ensure_ascii=False) + "\n")
    print(f"Wrote canonical JSONL -> {out}")


if __name__ == "__main__":
    main()
