#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
from pathlib import Path


def fail(msg: str) -> int:
    print(f"INVALID: {msg}")
    return 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True)
    args = ap.parse_args()

    data = json.loads(Path(args.file).read_text(encoding="utf-8"))
    for key in ["summary", "question_results", "overall_percent", "level", "next_actions"]:
        if key not in data:
            return fail(f"missing '{key}'")
    if not isinstance(data["question_results"], list):
        return fail("question_results must be a list")
    pct = data["overall_percent"]
    if not isinstance(pct, (int, float)) or pct < 0 or pct > 100:
        return fail("overall_percent must be 0..100")
    print("VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
