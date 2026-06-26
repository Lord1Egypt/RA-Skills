#!/usr/bin/env python3
"""Deprecated grader: use LLM rubric grading protocol in SKILL.md.

This script only prints guidance for model-based grading and JSON validation.
"""

from __future__ import annotations
import json


def main() -> int:
    guidance = {
        "status": "deprecated",
        "message": "Grade with LLM using references/grading-schema.md, then run validate_grading_json.py",
    }
    print(json.dumps(guidance, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
