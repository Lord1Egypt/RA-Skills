#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ["SKILL.md", "LICENSE", "claw.json", "references/SECURITY.md"]
# rough secret-shape guards for package hygiene
BANNED = [
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"xai-[A-Za-z0-9]{20,}"),
    re.compile(r"0x[a-fA-F0-9]{40}"),
]


def main() -> int:
    missing = [p for p in REQUIRED if not (ROOT / p).is_file()]
    if missing:
        print("FAIL missing:", ", ".join(missing))
        return 1
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".md", ".json", ".py", ".txt", ""}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for pat in BANNED:
            if pat.search(text):
                print("FAIL possible secret pattern in", path.relative_to(ROOT))
                return 1
    print("OK lyra-open-claw public self_check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
