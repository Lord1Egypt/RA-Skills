#!/usr/bin/env python3
"""This Skill has no local workflow helper; use the host's live Apify tool schema."""

import sys


def main() -> int:
    sys.stderr.write(
        "No local workflow helper is defined for this Skill. "
        "Follow references/workflow.md and the host's live Apify tool schema.\n"
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
