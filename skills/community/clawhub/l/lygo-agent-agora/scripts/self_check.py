#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import agora_onboard as o  # noqa: E402


def main() -> int:
    src = (HERE / "agora_onboard.py").read_text(encoding="utf-8")
    no_sub = not re.search(r"(?m)^\s*import\s+subprocess\b", src)
    no_net = "urllib" not in src and "requests" not in src and "http.client" not in src
    m = o.map_payload()
    on = o.onboard()
    d = o.expand_draft("demo-cap", "clawhub", "lygo-continuum", "")
    ok = (
        m["options"]["skillhub_full"]["url"].endswith("#full-lygo")
        and m["options"]["clawhub_tentacles"]["publisher"].startswith("https://clawhub.ai/")
        and len(m["options"]["clawhub_tentacles"]["stack"]) >= 8
        and len(on.get("tracks", [])) >= 3
        and d.get("ok") is True
        and d.get("live_write") is False
        and no_sub
        and no_net
        and o.VERSION == "1.0.1"
        and len(o.FULL_ZIP_SHA256) == 64
    )
    print(
        json.dumps(
            {
                "ok": ok,
                "signature": o.SIG,
                "no_subprocess": no_sub,
                "no_network_imports": no_net,
                "clawhub_skills": len(m["options"]["clawhub_tentacles"]["stack"]),
                "draft_dry_run": d.get("dry_run"),
            },
            indent=2,
        )
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
