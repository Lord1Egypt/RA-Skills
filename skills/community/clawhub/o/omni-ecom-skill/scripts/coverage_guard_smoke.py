#!/usr/bin/env python3
"""Regression tests for coverage_guard.py (fail-closed, graded blocking)."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path
from artifact_contract import native_stage_identity

HERE = Path(__file__).resolve().parent
CLUSTER = HERE / "cluster_reports.py"
GUARD = HERE / "coverage_guard.py"
PY = sys.executable
FAILURES: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    if cond:
        print(f"  PASS  {name}")
    else:
        print(f"  FAIL  {name} :: {detail}")
        FAILURES.append(name)


def metric(std, unit="元", agg="sum"):
    return {"raw_name": std, "standard_name": std, "unit": unit,
            "aggregation": agg, "is_core": True}


def rep(rid, name, rtype, domain, verdict, reason=None):
    r = {
        "report_id": rid, "file_name": name, "file_path": f"/tmp/{name}",
        "platform": "tmall", "report_type": rtype, "report_type_label": name,
        "domain": domain, "confidence": "high", "identified_by": "rule",
        "identify_evidence": ["测试样本"],
        "time_scope": {"start": "2026-08-01", "end": "2026-08-31",
                       "time_column": "日期", "has_explicit_time": True, "note": ""},
        "granularity": "daily", "row_count": 1000, "column_count": 3,
        "metrics": [metric("gmv")], "dimensions": ["date"],
        "completeness": {"missing_rate": 0.0, "has_total_row": False},
        "verdict": verdict,
    }
    if reason:
        r["verdict_reason"] = reason
    return r


def make_inventory(reports) -> dict:
    return {
        **native_stage_identity("report_inventory","2.0.3"),
        "run_id": "coverage-smoke-run", "client_scope": "smoke", "team_version": "2.0.3",
        "issued_at": "2026-09-01T00:00:00+08:00", "scanned_root": "/tmp",
        "report_count": len(reports),
        "identification": {"mode": "rule_first_model_fallback", "rule_hits": len(reports),
                           "model_hits": 0, "unidentified": 0,
                           "low_confidence_ids": [], "model_review_pending": []},
        "reports": reports,
    }


def run_pipeline(tmp: Path, inv: dict, tag: str):
    ipath = tmp / f"inv-{tag}.json"
    ipath.write_text(json.dumps(inv, ensure_ascii=False, indent=2), encoding="utf-8")
    cpath, ppath = tmp / f"clusters-{tag}.json", tmp / f"plan-{tag}.json"
    subprocess.run([PY, str(CLUSTER), "--inventory", str(ipath), "--output-clusters", str(cpath),
                    "--output-chapter-plan", str(ppath)],
                   capture_output=True, text=True, encoding="utf-8", check=True)
    return ipath, cpath, ppath


def guard(tmp: Path, ipath: Path, ppath: Path, tag: str, md: Path | None = None) -> tuple[dict, int]:
    out = tmp / f"gate-{tag}.json"
    cmd = [PY, str(GUARD), "--inventory", str(ipath), "--chapter-plan", str(ppath),
           "--output", str(out)]
    if md:
        cmd += ["--report-md", str(md)]
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if out.exists():
        return json.loads(out.read_text(encoding="utf-8")), proc.returncode
    return {"status": "no_output", "checks": [], "blocking_failures": []}, proc.returncode


def cstatus(gate: dict, cid: str) -> str:
    for c in gate["checks"]:
        if c["check_id"] == cid:
            return c["status"]
    return "missing"


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="coverage_smoke_"))

    print("[S1] clean run with only analyzable reports")
    inv = make_inventory([
        rep("R001", "交易概况.xlsx", "trade_sales", "transaction", "analyzable"),
        rep("R002", "推广计划.xlsx", "advertising", "advertising", "analyzable"),
    ])
    i, _c, p = run_pipeline(tmp, inv, "clean")
    gate, rc = guard(tmp, i, p, "clean")
    check("status passed", gate["status"] == "coverage_passed", gate["status"])
    check("exit code zero", rc == 0, str(rc))
    check("no blocking failures", gate["blocking_failures"] == [], str(gate["blocking_failures"]))

    print("[S2] documented weak reports pass with gaps")
    inv = make_inventory([
        rep("R001", "交易概况.xlsx", "trade_sales", "transaction", "analyzable"),
        rep("R002", "行业大盘.xlsx", "market_benchmark", "market", "insufficient",
            "无有效数据行，无法支撑任何分析"),
    ])
    i, _c, p = run_pipeline(tmp, inv, "weak")
    gate, rc = guard(tmp, i, p, "weak")
    check("status passed_with_gaps", gate["status"] == "coverage_passed_with_gaps", gate["status"])
    check("exit code zero", rc == 0, str(rc))
    check("gap documented", cstatus(gate, "weak_reports_documented") == "pass",
          cstatus(gate, "weak_reports_documented"))
    check("gap listed with reason", any(g["report_id"] == "R002" for g in gate["documented_gaps"]),
          str(gate["documented_gaps"]))

    print("[S3] analyzable report with no chapter is a hard block")
    inv = make_inventory([
        rep("R001", "交易概况.xlsx", "trade_sales", "transaction", "analyzable"),
        rep("R002", "推广计划.xlsx", "advertising", "advertising", "analyzable"),
    ])
    i, _c, p = run_pipeline(tmp, inv, "drop")
    plan = json.loads(p.read_text(encoding="utf-8"))
    for ch in plan["chapters"]:
        if ch["chapter_kind"] == "domain_analysis" and "R002" in ch["source_report_ids"]:
            ch["source_report_ids"] = [r for r in ch["source_report_ids"] if r != "R002"]
    p2 = tmp / "plan-drop-tampered.json"
    p2.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    gate, rc = guard(tmp, i, p2, "drop")
    check("status blocked", gate["status"] == "coverage_blocked", gate["status"])
    check("exit code 4", rc == 4, str(rc))
    check("analyzable_uncovered surfaced", gate["analyzable_uncovered"] == ["R002"],
          str(gate["analyzable_uncovered"]))
    check("blocking failure named", "analyzable_all_covered" in gate["blocking_failures"],
          str(gate["blocking_failures"]))

    print("[S4] undocumented weak report is also a hard block")
    inv = make_inventory([
        rep("R001", "交易概况.xlsx", "trade_sales", "transaction", "analyzable"),
        rep("R002", "行业大盘.xlsx", "market_benchmark", "market", "insufficient",
            "无有效数据行，无法支撑任何分析"),
    ])
    i, _c, p = run_pipeline(tmp, inv, "undoc")
    plan = json.loads(p.read_text(encoding="utf-8"))
    for ch in plan["chapters"]:
        if ch["chapter_kind"] == "data_gap":
            ch["data_gaps"] = []
    p2 = tmp / "plan-undoc-tampered.json"
    p2.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    gate, rc = guard(tmp, i, p2, "undoc")
    check("status blocked", gate["status"] == "coverage_blocked", gate["status"])
    check("undocumented surfaced", gate["undocumented_weak_reports"] == ["R002"],
          str(gate["undocumented_weak_reports"]))
    check("remedy text present", bool(gate["remedy"]))

    print("[S5] overview chapter must list everything")
    inv = make_inventory([
        rep("R001", "交易概况.xlsx", "trade_sales", "transaction", "analyzable"),
        rep("R002", "推广计划.xlsx", "advertising", "advertising", "analyzable"),
    ])
    i, _c, p = run_pipeline(tmp, inv, "overview")
    plan = json.loads(p.read_text(encoding="utf-8"))
    for ch in plan["chapters"]:
        if ch["chapter_kind"] == "data_overview":
            ch["source_report_ids"] = ["R001"]
    p2 = tmp / "plan-overview-tampered.json"
    p2.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    gate, rc = guard(tmp, i, p2, "overview")
    check("overview check fails", cstatus(gate, "overview_lists_all_reports") == "fail",
          cstatus(gate, "overview_lists_all_reports"))
    check("status blocked", gate["status"] == "coverage_blocked", gate["status"])

    print("[S6] final markdown must name every report")
    inv = make_inventory([
        rep("R001", "交易概况.xlsx", "trade_sales", "transaction", "analyzable"),
        rep("R002", "推广计划.xlsx", "advertising", "advertising", "analyzable"),
    ])
    i, _c, p = run_pipeline(tmp, inv, "md")
    md = tmp / "report-partial.md"
    md.write_text("# 报告\n本章分析 R001 交易概况.xlsx。\n", encoding="utf-8")
    gate, rc = guard(tmp, i, p, "md", md)
    check("silent report detected", cstatus(gate, "final_report_mentions_all") == "fail",
          cstatus(gate, "final_report_mentions_all"))
    md_full = tmp / "report-full.md"
    md_full.write_text("# 报告\n分析 R001 与 R002，两章分别覆盖。\n", encoding="utf-8")
    gate2, rc2 = guard(tmp, i, p, "md2", md_full)
    check("full report passes", gate2["status"] == "coverage_passed", gate2["status"])
    check("exit code zero", rc2 == 0, str(rc2))

    print("[S7] missing input is its own status")
    gate, rc = guard(tmp, tmp / "nope.json", tmp / "nope-plan.json", "missing")
    check("input missing status", gate["status"] == "no_output", gate["status"])
    check("exit code 2", rc == 2, str(rc))

    print()
    if FAILURES:
        print(f"FAILED {len(FAILURES)}: {FAILURES}")
        return 1
    print("ALL PASSED (7 scenarios)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
