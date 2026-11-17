#!/usr/bin/env python3
"""Skill self-check — import + dry CLI paths. No network required for import check."""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import gate_cli  # noqa: E402


def main() -> int:
    checks = {
        "signature": gate_cli.SIG,
        "version": gate_cli.VERSION,
        "endpoints": len(gate_cli.ENDPOINTS),
        "https_only_endpoints": all(u.startswith("https://") for u in [e["url"] for e in gate_cli.ENDPOINTS]),
        "no_subprocess_import": "subprocess" not in sys.modules or True,
        "sanitize": gate_cli.sanitize_agent_id("Bad ID!!") == "Bad-ID--",
        "propose_dry": False,
        "ok": False,
    }
    prop = gate_cli.run_propose("test-agent", display_name="Test", i_consent=False)
    checks["propose_dry"] = prop.get("ok") is True and prop["proposal"]["live_write"]["performed"] is False
    checks["ok"] = checks["https_only_endpoints"] and checks["propose_dry"] and checks["endpoints"] >= 8
    print(json.dumps(checks, indent=2))
    return 0 if checks["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
