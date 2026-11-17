#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cyborg_onramp as o  # noqa: E402


def main() -> int:
    src = (HERE / "cyborg_onramp.py").read_text(encoding="utf-8")
    no_sub = not re.search(r"(?m)^\s*import\s+subprocess\b", src)
    no_net = "urllib" not in src and "requests" not in src and "http.client" not in src
    m = o.map_payload()
    inst = o.install_steps()
    ok = (
        m.get("full_unlocked", {}).get("skillhub", "").startswith("https://chatagent.ca/")
        and "full-lygo" in m["full_unlocked"]["skillhub"]
        and m["full_unlocked"]["slug"] == "lygo-cyborg-kernel"
        and len(inst.get("steps", [])) >= 4
        and no_sub
        and no_net
        and o.VERSION == "1.0.0"
    )
    print(
        json.dumps(
            {
                "ok": ok,
                "signature": o.SIG,
                "points_to_skillhub_full": True,
                "full_slug": m["full_unlocked"]["slug"],
                "no_subprocess": no_sub,
                "no_network_imports": no_net,
                "public_skill_count": len(m.get("public_clawhub_skills", [])),
            },
            indent=2,
        )
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
