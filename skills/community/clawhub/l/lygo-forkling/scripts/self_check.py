#!/usr/bin/env python3
"""Offline self-check for Forkling."""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import forkling as f  # noqa: E402


def main() -> int:
    if f.STATE.exists():
        shutil.rmtree(f.STATE)
    checks = {"signature": f.SIG, "birth": False, "loop": False, "propose_dry": False, "ok": False}
    b = f.birth(True)
    checks["birth"] = b.get("ok") is True and (f.FORK / "identity.json").is_file()
    lp = f.loop(4, True)
    checks["loop"] = lp.get("ok") is True and int(lp.get("last_generation") or 0) == 4
    pr = f.propose()
    checks["propose_dry"] = pr.get("live_write") is False and pr.get("node", {}).get("id") == f.AGENT_ID
    ident = json.loads((f.FORK / "identity.json").read_text(encoding="utf-8"))
    checks["parent_pin"] = ident.get("parent_node") == f.PARENT_NODE
    checks["not_lightfather"] = ident.get("replaces_lightfather") is False
    checks["ok"] = all(
        [checks["birth"], checks["loop"], checks["propose_dry"], checks["parent_pin"], checks["not_lightfather"]]
    )
    print(json.dumps(checks, indent=2))
    return 0 if checks["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
