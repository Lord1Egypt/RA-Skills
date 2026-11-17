#!/usr/bin/env python3
"""Stage 0 step 4: coverage gate. No uploaded report may vanish from the final report.

Graded blocking, per the agreed design:
  - an `analyzable` report that no chapter analyses      -> hard block
  - a `partial` / `insufficient` report that is explicitly documented
    with reason + impact + remedy in the data gap chapter -> allowed through
  - a `partial` / `insufficient` report that is NOT documented -> hard block

Usage:
    python coverage_guard.py --inventory report-inventory.json \
        --chapter-plan chapter-plan.json --output coverage-gate.json \
        [--report-md report.md]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from artifact_contract import native_stage_identity,validate_stage_identity

ANALYSIS_KINDS = {"domain_analysis", "independent_observation"}


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def add(checks: list[dict], cid: str, ok: bool, detail: str) -> None:
    checks.append({"check_id": cid, "status": "pass" if ok else "fail", "detail": detail})


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Stage 0 step 4: coverage gate")
    ap.add_argument("--inventory", required=True)
    ap.add_argument("--chapter-plan", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--report-md", default=None,
                    help="final markdown report, checked for explicit mentions of every report id")
    args = ap.parse_args(argv)

    inv_p, plan_p = Path(args.inventory), Path(args.chapter_plan)
    if not inv_p.exists() or not plan_p.exists():
        print(json.dumps({"status": "input_missing",
                          "inventory": str(inv_p), "chapter_plan": str(plan_p)}, ensure_ascii=False))
        return 2

    inv = json.loads(inv_p.read_text(encoding="utf-8"))
    plan = json.loads(plan_p.read_text(encoding="utf-8"))
    version=validate_stage_identity(inv,"report_inventory",inv.get("team_version"),
                                    inv.get("run_id"),inv.get("client_scope"))
    validate_stage_identity(plan,"chapter_plan",version,inv.get("run_id"),inv.get("client_scope"))

    reports = {r["report_id"]: r for r in inv["reports"]}
    chapters = plan["chapters"]
    cov = plan["coverage_plan"]
    checks: list[dict] = []

    # 1. every chapter reference must exist in the inventory
    known = set(reports)
    dangling = sorted({rid for ch in chapters for rid in ch.get("source_report_ids", [])
                       if rid not in known})
    add(checks, "chapter_refs_exist", not dangling,
        "所有章节引用的报表编号均存在于清单" if not dangling else f"章节引用了不存在的报表：{dangling}")

    # 2. every analyzable report must be analysed by a real chapter
    analysed: set[str] = set()
    for ch in chapters:
        if ch["chapter_kind"] in ANALYSIS_KINDS:
            analysed.update(ch.get("source_report_ids", []))
    analyzable_ids = {rid for rid, r in reports.items() if r["verdict"] == "analyzable"}
    analyzable_uncovered = sorted(analyzable_ids - analysed)
    add(checks, "analyzable_all_covered", not analyzable_uncovered,
        "全部可用报表均被分析章节覆盖" if not analyzable_uncovered
        else f"以下可用报表没有任何分析章节覆盖，必须补章节后再交付：{analyzable_uncovered}")

    # weak reports must be documented with reason + impact + remedy
    weak_ids = {rid for rid, r in reports.items() if r["verdict"] != "analyzable"}
    gap_chapters = [ch for ch in chapters if ch["chapter_kind"] == "data_gap"]
    documented = {}
    for ch in gap_chapters:
        for g in ch.get("data_gaps", []):
            if g.get("reason") and g.get("impact") and g.get("remedy"):
                documented[g["report_id"]] = g

    # 3. a chapter needs at least one analyzable source, unless every one of its
    #    weak members is explicitly documented in the data gap chapter
    thin = []
    for ch in chapters:
        if ch["chapter_kind"] != "domain_analysis":
            continue
        srcs = ch.get("source_report_ids", [])
        if any(reports.get(rid, {}).get("verdict") == "analyzable" for rid in srcs):
            continue
        undocumented_members = [rid for rid in srcs if rid not in documented]
        if undocumented_members:
            thin.append({"chapter_id": ch["chapter_id"],
                         "undocumented_members": sorted(undocumented_members)})
    add(checks, "chapter_has_analyzable_source", not thin,
        "每个分析章节都有可用报表支撑，或已文档化全部缺口" if not thin
        else f"以下章节既无可用报表、缺口也未说明：{thin}")

    # 4. every weak report must be documented
    undocumented = sorted(weak_ids - set(documented))
    add(checks, "weak_reports_documented", not undocumented,
        "数据不足的报表均已写明原因、影响和补数要求" if not undocumented
        else f"以下数据不足的报表未在数据缺口章节显式说明：{undocumented}")

    # 5. data overview must list every report
    overview = next((ch for ch in chapters if ch["chapter_kind"] == "data_overview"), None)
    if overview is None:
        add(checks, "overview_chapter_exists", False, "缺少数据概览章节")
    else:
        missing = sorted(known - set(overview.get("source_report_ids", [])))
        add(checks, "overview_lists_all_reports", not missing,
            "数据概览覆盖全部报表" if not missing else f"数据概览遗漏报表：{missing}")

    # 6. coverage plan self-consistency
    uncovered = cov.get("uncovered_report_ids", [])
    add(checks, "coverage_plan_complete", not uncovered,
        "覆盖计划无遗漏" if not uncovered else f"覆盖计划存在未覆盖报表：{uncovered}")

    # 7. final markdown must explicitly mention every report
    if args.report_md:
        md_p = Path(args.report_md)
        if not md_p.exists():
            add(checks, "final_report_mentions_all", False, f"最终报告文件不存在：{md_p}")
        else:
            text = md_p.read_text(encoding="utf-8", errors="ignore")
            silent = []
            for rid, r in reports.items():
                if rid in text or r["file_name"] in text:
                    continue
                silent.append(rid)
            add(checks, "final_report_mentions_all", not silent,
                "最终报告逐份提及了所有报表" if not silent
                else f"最终报告未提及以下报表，读者无法判断其去向：{silent}")
    else:
        checks.append({"check_id": "final_report_mentions_all", "status": "skipped",
                       "detail": "未提供最终报告文本，本项在交付前由团长补充校验"})

    blocking = [c for c in checks if c["status"] == "fail"]
    if blocking:
        status = "coverage_blocked"
    elif weak_ids:
        status = "coverage_passed_with_gaps"
    else:
        status = "coverage_passed"

    gate = {
        **native_stage_identity("coverage_guard", version),
        "run_id": inv.get("run_id", ""),
        "client_scope": inv.get("client_scope", ""),
        "team_version": version,
        "generated_at": now_iso(),
        "status": status,
        "inventory_sha256_ref": hashlib.sha256(inv_p.read_bytes()).hexdigest(),
        "chapter_plan_sha256_ref": hashlib.sha256(plan_p.read_bytes()).hexdigest(),
        "stats": {
            "total_reports": len(reports),
            "analyzable": len(analyzable_ids),
            "partial": sum(1 for r in reports.values() if r["verdict"] == "partial"),
            "insufficient": sum(1 for r in reports.values() if r["verdict"] == "insufficient"),
            "chapters": len(chapters),
            "coverage_rate": cov.get("coverage_rate", 0.0),
        },
        "analyzable_uncovered": analyzable_uncovered,
        "undocumented_weak_reports": undocumented,
        "documented_gaps": [{"report_id": k, "reason": v["reason"]} for k, v in sorted(documented.items())],
        "checks": checks,
        "blocking_failures": [c["check_id"] for c in blocking],
        "remedy": ("补齐上述缺口后重跑本闸门；在 status 变为 coverage_passed 或 "
                   "coverage_passed_with_gaps 之前不得交付报告" if blocking else ""),
    }
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(gate, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"status": status, "blocking_failures": gate["blocking_failures"],
                      "analyzable_uncovered": analyzable_uncovered,
                      "undocumented_weak_reports": undocumented,
                      "output": str(out.resolve())}, ensure_ascii=False))
    return 4 if blocking else 0


if __name__ == "__main__":
    sys.exit(main())
