"""Demo1 CLI: run the lgd-engine gate on a case JSON.

Usage (from mvp/ directory):
    python -m demo1.change_gate --case demo1/cases/case01_red_pma_process.json
    python -m demo1.change_gate --all
    python -m demo1.change_gate --case demo1/cases_postmarket/pm01_class1_software.json --domain postmarket
    python -m demo1.change_gate --case demo1/cases_jurisdiction/supplier_swap.json --jurisdiction NMPA
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_MVP = _HERE.parent
if str(_MVP) not in sys.path:
    sys.path.insert(0, str(_MVP))

from lgd_engine.gate import GateEngine, GateReport           # noqa: E402
from lgd_engine.judges.judge_510k import Judge510kChange      # noqa: E402
from lgd_engine.judges.judge_postmarket import JudgePostmarket # noqa: E402
from lgd_engine.memory import LocalMemory                     # noqa: E402


_DOMAINS = {
    "510k": Judge510kChange,
    "postmarket": JudgePostmarket,
}


def _build_engine(domain: str = "510k") -> GateEngine:
    eng = GateEngine()
    eng.register(_DOMAINS[domain]())
    return eng


def run_case(case_path: Path, domain: str = "510k",
             jurisdiction: str | None = None,
             mem: LocalMemory | None = None,
             quiet: bool = False) -> GateReport:
    ctx = json.loads(case_path.read_text(encoding="utf-8"))
    expected = ctx.pop("expected_verdict", None)
    expected_fda = ctx.pop("expected_fda_verdict", None)
    expected_nmpa = ctx.pop("expected_nmpa_verdict", None)
    desensitized = ctx.pop("_desensitized_from", "")

    if jurisdiction:
        ctx["jurisdiction"] = jurisdiction

    eng = _build_engine(domain)
    t0 = time.perf_counter()
    report = eng.evaluate(ctx)
    dt_ms = (time.perf_counter() - t0) * 1000.0

    if mem is not None:
        mem.record({
            "time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "initiator": "demo1-cli",
            "subject": ctx.get("device_description", case_path.stem),
            "decision": report.verdict,
            "basis": "; ".join(r["rule"] for r in report.reasons),
            "status": "executed",
            "evidence_refs": [e["ref"] for e in report.evidence],
            "raw_ctx": ctx,
        })

    if not quiet:
        jur = ctx.get("jurisdiction", "FDA")
        print(f"\n[case] {case_path.name}  [domain={domain}] [jurisdiction={jur}]")
        if desensitized:
            print(f"[desensitized from] {desensitized}")
        print(f"[eval time] {dt_ms:.1f} ms")
        exp = expected
        if jurisdiction == "FDA" and expected_fda:
            exp = expected_fda
        elif jurisdiction == "NMPA" and expected_nmpa:
            exp = expected_nmpa
        if exp:
            mark = "OK" if report.verdict == exp else "MISMATCH"
            print(f"[expected verdict] {exp}  ->  got {report.verdict}  [{mark}]")
        print(report.pretty())
    return report


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="lgd-engine Demo1 CLI")
    p.add_argument("--case", type=str, help="path to a case JSON")
    p.add_argument("--all", action="store_true", help="run every case under cases/")
    p.add_argument("--domain", choices=list(_DOMAINS), default="510k")
    p.add_argument("--jurisdiction", default=None,
                   help="FDA | NMPA (overrides ctx.jurisdiction)")
    p.add_argument("--db", type=str,
                   default=str(_HERE / "demo1_memory.sqlite"))
    args = p.parse_args(argv)

    mem = LocalMemory(args.db)

    if args.all:
        root = _HERE / ("cases_postmarket" if args.domain == "postmarket" else "cases")
        cases = sorted(root.glob("*.json"))
        n_pass = 0
        for c in cases:
            rep = run_case(c, domain=args.domain,
                           jurisdiction=args.jurisdiction, mem=mem)
            ctx = json.loads(c.read_text(encoding="utf-8"))
            exp = ctx.get("expected_verdict")
            if exp and rep.verdict == exp:
                n_pass += 1
        print(f"\n[summary] {n_pass}/{len(cases)} cases match expected verdict "
              f"(domain={args.domain})")
        rc = 0 if n_pass == len(cases) else 1
        mem.close()
        return rc

    if not args.case:
        p.error("either --case PATH or --all is required")
    cp = Path(args.case)
    if not cp.is_absolute():
        cp = (Path.cwd() / cp).resolve()
    rep = run_case(cp, domain=args.domain,
                   jurisdiction=args.jurisdiction, mem=mem)
    mem.close()
    return {"go": 0, "hold": 1, "reject": 2}[rep.verdict]


if __name__ == "__main__":
    raise SystemExit(main())
