#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ["SKILL.md", "LICENSE", "claw.json", "references/SECURITY.md"]


def main() -> int:
    missing = [p for p in REQUIRED if not (ROOT / p).is_file()]
    if missing:
        print("FAIL missing:", ", ".join(missing))
        return 1
    print("OK lygo-pc-lattice-hardening self_check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
