#!/usr/bin/env python3
"""Hello-world entry point for the Grupr OpenClaw skill.

Confirms the skill is installed correctly and reports configuration state.
Subsequent milestones add login.py, poll.py, start.py, stop.py.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

VERSION = "0.1.0"
SKILL_DIR = Path(__file__).resolve().parent.parent


def main() -> int:
    print(f"🐠 Grupr OpenClaw skill v{VERSION} — loaded")
    print(f"   skill dir: {SKILL_DIR}")

    token = os.environ.get("GRUPR_AGENT_TOKEN", "")
    if token:
        # Show only a hint, never the full token.
        hint = f"{token[:8]}…{token[-4:]}" if len(token) > 12 else "(short)"
        print(f"   GRUPR_AGENT_TOKEN: set ({hint})")
    else:
        env_file = SKILL_DIR / ".env"
        suffix = " — populated" if env_file.exists() else " — not yet created"
        print(f"   GRUPR_AGENT_TOKEN: not set (configure in milestone 2 — login)")
        print(f"   .env path:        {env_file}{suffix}")

    print(f"   python:           {sys.version.split()[0]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
