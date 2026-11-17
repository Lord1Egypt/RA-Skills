#!/usr/bin/env python3
"""Self-check — no network required."""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import kickstart_cli as k  # noqa: E402


def main() -> int:
    checks = {
        "signature": k.SIG,
        "version": k.VERSION,
        "endpoints_https": all(e["url"].startswith("https://") for e in k.LATTICE_ENDPOINTS),
        "map_routes": len(k.ECOSYSTEM_MAP) >= 5,
        "mint_guide": False,
        "analyze_empty": False,
        "ok": False,
    }
    m = k.cmd_map()
    checks["map_ok"] = m.get("ok") is True
    mint = k.cmd_mint()
    checks["mint_guide"] = mint.get("ok") is True and len(mint.get("steps") or []) >= 4
    empty = k.cmd_analyze(text="")
    checks["analyze_empty"] = empty.get("ok") is False
    nxt = k.cmd_next()
    checks["roadmap"] = len(nxt.get("items") or []) >= 4
    checks["ok"] = all(
        [
            checks["endpoints_https"],
            checks["map_routes"],
            checks["map_ok"],
            checks["mint_guide"],
            checks["analyze_empty"],
            checks["roadmap"],
        ]
    )
    print(json.dumps(checks, indent=2))
    return 0 if checks["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
