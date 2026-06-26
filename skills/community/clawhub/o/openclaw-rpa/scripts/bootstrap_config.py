#!/usr/bin/env python3
"""Create config.json from config.example.json if missing (default locale en-US)."""
import shutil
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
EXAMPLE = SKILL_DIR / "config.example.json"
CONFIG = SKILL_DIR / "config.json"


def main() -> int:
    if CONFIG.exists():
        print(f"OK — already exists: {CONFIG}")
        return 0
    if not EXAMPLE.exists():
        print(f"Missing {EXAMPLE}", file=sys.stderr)
        return 1
    shutil.copy(EXAMPLE, CONFIG)
    print(f"✅ Created {CONFIG} from {EXAMPLE.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
