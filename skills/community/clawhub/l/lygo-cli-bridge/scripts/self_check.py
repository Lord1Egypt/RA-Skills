#!/usr/bin/env python3
"""Self-check for lygo-cli-bridge — no network required for core paths."""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import lygo_cli as cli  # noqa: E402


def main() -> int:
    ver = cli.cmd_version()
    mp = cli.cmd_map()
    nxt = cli.cmd_next()
    # analyze may need ops-detector; treat as soft if missing
    an = cli.cmd_analyze(text="It's on you to prove it. Tons of evidence out there.")
    mint_guide = cli.cmd_mint()
    ok = (
        ver.get("ok")
        and mp.get("ok")
        and nxt.get("ok")
        and mint_guide.get("ok")
        and ver.get("signature") == cli.SIG
        and len(cli.LATTICE_ENDPOINTS) >= 4
        and all(e["url"].startswith("https://") for e in cli.LATTICE_ENDPOINTS)
    )
    # analyze ok if detector present OR honest missing error
    analyze_ok = an.get("ok") is True or an.get("error") == "ops_detector_missing"
    report = {
        "ok": ok and analyze_ok,
        "signature": cli.SIG,
        "version": cli.VERSION,
        "version_cmd": ver.get("ok"),
        "map_routes": len(mp.get("routes") or []),
        "analyze": {"ok": an.get("ok"), "error": an.get("error"), "level": (an.get("result") or {}).get("level")},
        "mint_guide": mint_guide.get("ok"),
        "https_only": all(e["url"].startswith("https://") for e in cli.LATTICE_ENDPOINTS),
        "no_subprocess_in_source": "subprocess" not in Path(HERE / "lygo_cli.py").read_text(encoding="utf-8"),
    }
    print(json.dumps(report, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
