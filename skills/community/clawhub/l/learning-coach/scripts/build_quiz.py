#!/usr/bin/env python3
"""Deprecated generator: use LLM protocol in SKILL.md.

This script only prints the required schema guidance so automation can route
quiz creation to the model and then validate with validate_quiz_json.py.
"""

from __future__ import annotations
import json


def main() -> int:
    guidance = {
        "status": "deprecated",
        "message": "Generate quiz JSON with LLM using references/quiz-schema.md, then run validate_quiz_json.py",
    }
    print(json.dumps(guidance, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
