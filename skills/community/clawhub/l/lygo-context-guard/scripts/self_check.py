#!/usr/bin/env python3
"""Self-check for lygo-context-guard."""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import context_guard as g  # noqa: E402


def main() -> int:
    demo = g.cmd_demo()
    leaky = "api_key=REDACTED-SECRET password: hunter22secret"
    red = g.redact_secrets(leaky)
    est = g.estimate_tokens("hello world " * 100)
    over = g.budget_check(99999, 100)
    under = g.budget_check(10, 100)
    big = "line same\n" * 50 + ("x" * 5000)
    comp = g.compact_text(big, max_chars=1000)

    ok = (
        demo.get("ok")
        and red["total_hits"] >= 1
        and "[REDACTED" in red["redacted"]
        and est["tokens_estimate"] > 0
        and over["over_budget"] is True
        and under["ok"] is True
        and comp["ok"]
        and len(comp["text"]) < len(big)
        and g.SIG.startswith("Delta9")
        and "subprocess" not in Path(HERE / "context_guard.py").read_text(encoding="utf-8")
        or "import subprocess" not in Path(HERE / "context_guard.py").read_text(encoding="utf-8")
    )
    # fix ok logic - no subprocess import
    src = Path(HERE / "context_guard.py").read_text(encoding="utf-8")
    no_sub = "import subprocess" not in src
    ok = (
        bool(demo.get("ok"))
        and red["total_hits"] >= 1
        and "[REDACTED" in red["redacted"]
        and est["tokens_estimate"] > 0
        and over["over_budget"] is True
        and under["ok"] is True
        and comp["ok"]
        and len(comp["text"]) < len(big)
        and no_sub
    )
    report = {
        "ok": ok,
        "signature": g.SIG,
        "version": g.VERSION,
        "demo_saved": demo.get("compact", {}).get("tokens_saved_estimate"),
        "redact_hits": red["total_hits"],
        "est_tokens": est["tokens_estimate"],
        "no_subprocess": no_sub,
    }
    print(json.dumps(report, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
