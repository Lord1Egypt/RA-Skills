#!/usr/bin/env python3
"""Set openclaw-rpa skill locale (zh-CN | en-US)."""
import json
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
CONFIG = SKILL_DIR / "config.json"
EXAMPLE = SKILL_DIR / "config.example.json"
VALID = {"zh-CN", "en-US"}


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <zh-CN|en-US>", file=sys.stderr)
        return 1
    loc = sys.argv[1].strip()
    if loc not in VALID:
        print(f"Invalid locale: {loc!r}. Use: {VALID}", file=sys.stderr)
        return 1
    if not CONFIG.exists() and EXAMPLE.exists():
        import shutil

        shutil.copy(EXAMPLE, CONFIG)
        print(f"Created {CONFIG} from {EXAMPLE.name}")
    data = {}
    if CONFIG.exists():
        try:
            data = json.loads(CONFIG.read_text(encoding="utf-8"))
        except Exception:
            pass
    data["locale"] = loc
    if "_comment" in data:
        pass
    else:
        data["_comment"] = "Supported: zh-CN | en-US"
    CONFIG.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"✅ locale set to {loc} → {CONFIG}")
    print("   Restart the OpenClaw session or re-read SKILL.md / locale file for the agent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
