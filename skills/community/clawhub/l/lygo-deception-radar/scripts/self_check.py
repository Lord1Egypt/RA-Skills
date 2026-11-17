#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_radar_feed as b  # noqa: E402

def main() -> int:
    suite = Path(r"I:\E Drive\.grok\skills\lygo-ops-detector\tests\labeled_discourse_suite.json")
    samples = b.load_suite(suite if suite.is_file() else None)
    feed = b.build_feed(samples[:6] if samples else [])
    ok = feed.get("ok") is True and (feed.get("stats") or {}).get("samples", 0) >= 1
    print(json.dumps({"ok": ok, "signature": b.SIG, "stats": feed.get("stats"), "error": feed.get("error")}, indent=2))
    return 0 if ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
