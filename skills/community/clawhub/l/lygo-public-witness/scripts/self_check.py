#!/usr/bin/env python3
"""Import + dry CLI paths. Network not required."""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import witness_cli as w  # noqa: E402


def main() -> int:
    checks = {
        "signature": w.SIG,
        "version": w.VERSION,
        "canon_https": all(e["url"].startswith("https://") for e in w.CANON),
        "ref_https": all(e["url"].startswith("https://") for e in w.REFERENCE),
        "allowlist_self": all(w.allowlisted(e["url"], w.CANON) for e in w.CANON),
        "https_only_fn": w.https_only("https://chatagent.ca/witness/") and not w.https_only("http://evil"),
        "propose_dry": False,
        "doctrine": False,
        "ok": False,
    }
    d = w.cmd_doctrine(type("A", (), {})())
    checks["doctrine"] = d.get("public_is") == "REFERENCE" and d.get("lattice_is") == "CANON"
    ns = type("A", (), {"agent_id": "t", "display_name": "t", "i_consent": True, "write": None})()
    prop = w.cmd_propose(ns)
    checks["propose_dry"] = prop.get("ok") is True and prop["live_write"]["performed"] is False
    checks["ok"] = (
        checks["canon_https"]
        and checks["ref_https"]
        and checks["allowlist_self"]
        and checks["https_only_fn"]
        and checks["propose_dry"]
        and checks["doctrine"]
        and "subprocess" not in sys.modules
    )
    print(json.dumps(checks, indent=2))
    return 0 if checks["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
