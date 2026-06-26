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
    for key in ["metadata", "questions", "answer_key", "grading_rubric", "feedback_rules"]:
        if key not in data:
            return fail(f"missing '{key}'")
    if not isinstance(data["questions"], list) or not data["questions"]:
        return fail("questions must be non-empty list")
    if len(data["answer_key"]) != len(data["questions"]):
        return fail("answer_key length must match questions")
    print("VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
