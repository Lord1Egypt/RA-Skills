"""lgd_engine.cli — console entry point (pyproject: lgd-gate = lgd_engine.cli:main).

Thin CLI over the judgment core. Mirrors demo1.change_gate without depending on
the demo layer; exit codes follow the release-gate convention: 0=go, 1=hold, 2=reject.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .gate import GateEngine
from .judges.judge_510k import Judge510kChange
from .judges.judge_postmarket import JudgePostmarket

_DOMAINS = {
    "510k": Judge510kChange,
    "postmarket": JudgePostmarket,
}
_STRIP_KEYS = ("expected_verdict", "expected_fda_verdict",
               "expected_nmpa_verdict", "_desensitized_from")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="lgd-gate",
        description="LGD Engine judgment core — go / hold / reject from a change context.",
    )
    ap.add_argument("--case", type=str, required=True,
                    help="path to a case JSON (change context; expected_* keys are stripped)")
    ap.add_argument("--domain", choices=list(_DOMAINS), default="510k",
                    help="judge family to run (default 510k)")
    ap.add_argument("--jurisdiction", choices=["FDA", "NMPA"], default=None,
                    help="override the jurisdiction in the case JSON")
    args = ap.parse_args(argv)

    ctx = json.loads(Path(args.case).read_text(encoding="utf-8"))
    for k in _STRIP_KEYS:
        ctx.pop(k, None)
    if args.jurisdiction:
        ctx["jurisdiction"] = args.jurisdiction

    eng = GateEngine()
    eng.register(_DOMAINS[args.domain]())
    report = eng.evaluate(ctx)
    print(report.pretty())
    return {"go": 0, "hold": 1, "reject": 2}.get(report.verdict, 1)


if __name__ == "__main__":
    raise SystemExit(main())
