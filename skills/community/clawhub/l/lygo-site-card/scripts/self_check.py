#!/usr/bin/env python3
"""Self-check — no network required."""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import site_card as s  # noqa: E402

FIXTURE = b"""<!doctype html><html><head>
<title>LYGO Site Card fixture</title>
<meta name="description" content="Local parse only.">
<link rel="canonical" href="/lattice/">
<meta name="referrer" content="strict-origin-when-cross-origin">
<script type="application/ld+json">{"@type":"WebPage","name":"fixture"}</script>
</head><body><p>ok</p></body></html>"""


def main() -> int:
    checks: dict = {
        "signature": s.SIG,
        "version": s.VERSION,
        "https_ok": s.https_only("https://chatagent.ca/lattice/"),
        "http_blocked": not s.https_only("http://chatagent.ca/"),
        "userinfo_blocked": not s.https_only("https://user:pass@chatagent.ca/"),
        "parse": False,
        "yield_local": None,
        "ok": False,
    }
    tmp = HERE.parent / "tests"
    tmp.mkdir(exist_ok=True)
    f = tmp / "fixture.html"
    f.write_bytes(FIXTURE)
    card = s.cmd_card(None, str(f), False)
    checks["parse"] = (
        card.get("ok") is True
        and card.get("title") == "LYGO Site Card fixture"
        and card.get("description") == "Local parse only."
        and "WebPage" in (card.get("json_ld_types") or [])
    )
    checks["yield_local"] = card.get("yield")
    checks["meta_referrer"] = (card.get("html_equiv") or {}).get("referrer") == "strict-origin-when-cross-origin"
    checks["local_aligned"] = card.get("yield") == "ALIGNED"
    checks["local_not_forged"] = card.get("source") == "local_file" and card.get("live_star_chart_write") is False
    checks["blocked_host_fn"] = s.allowed_url("https://127.0.0.1/") is False
    checks["ok"] = all(
        [
            checks["https_ok"],
            checks["http_blocked"],
            checks["userinfo_blocked"],
            checks["parse"],
            checks["meta_referrer"],
            checks["local_aligned"],
            checks["local_not_forged"],
            checks["blocked_host_fn"],
        ]
    )
    print(json.dumps(checks, indent=2))
    return 0 if checks["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
