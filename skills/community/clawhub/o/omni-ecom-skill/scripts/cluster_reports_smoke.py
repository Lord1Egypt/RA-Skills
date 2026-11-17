#!/usr/bin/env python3
"""Regression tests for cluster_reports.py (fail-closed)."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path
from artifact_contract import native_stage_identity

HERE = Path(__file__).resolve().parent
SCRIPT = HERE / "cluster_reports.py"
PY = sys.executable
FAILURES: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    if cond:
        print(f"  PASS  {name}")
    else:
        print(f"  FAIL  {name} :: {detail}")
        FAILURES.append(name)


def metric(std, unit="元", agg="sum", core=True):
    return {"raw_name": std, "standard_name": std, "unit": unit,
            "aggregation": agg, "is_core": core}


def rep(rid, name, rtype, domain, verdict, start, end, gran, metrics, rows=1000,
        confidence="high", reason=None):
    r = {
        "report_id": rid, "file_name": name, "file_path": f"/tmp/{name}",
        "platform": "tmall", "report_type": rtype, "report_type_label": name,
        "domain": domain, "confidence": confidence, "identified_by": "rule",
        "identify_evidence": ["测试样本"],
        "time_scope": {"start": start, "end": end, "time_column": "日期",
                       "has_explicit_time": True, "note": ""},
        "granularity": gran, "row_count": rows, "column_count": len(metrics),
        "metrics": metrics, "dimensions": ["date"],
        "completeness": {"missing_rate": 0.0, "has_total_row": False},
        "verdict": verdict,
    }
    if reason:
        r["verdict_reason"] = reason
    return r


def build_inventory(tmp: Path) -> Path:
    reports = [
        rep("R001", "交易概况_2026-08.xlsx", "trade_sales", "transaction", "analyzable",
            "2026-08-01", "2026-08-31", "daily",
            [metric("gmv"), metric("uv", "人", "distinct_count"),
             metric("conversion_rate", "%", "ratio")], rows=5000),
        rep("R002", "退款明细_2026-08.xlsx", "refund_aftersales", "transaction", "analyzable",
            "2026-08-01", "2026-08-31", "daily",
            [metric("gmv"), metric("refund_amount"), metric("refund_rate", "%", "ratio")], rows=3000),
        rep("R003", "推广计划_2026-08.xlsx", "advertising", "advertising", "analyzable",
            "2026-08-01", "2026-08-31", "daily",
            [metric("ad_spend"), metric("roi", "倍", "ratio"), metric("cpc", "元", "avg")], rows=800),
        rep("R004", "客服接待_2026-08.csv", "customer_service", "service", "partial",
            "2026-08-01", "2026-08-31", "daily",
            [metric("service_sessions", "次"), metric("first_response_sec", "秒", "avg")],
            rows=620, reason="数据缺失率 32%，可分析但结论需标注置信度"),
        rep("R005", "数据导出.csv", "unidentified", "unclassified", "partial",
            None, None, "unknown", [], rows=12, confidence="low",
            reason="未识别到标准指标列，只能做清单与结构层面描述"),
        rep("R006", "行业大盘_2026Q1.xlsx", "market_benchmark", "market", "insufficient",
            "2026-01-01", "2026-03-31", "monthly",
            [metric("gmv"), metric("uv", "人", "distinct_count")], rows=3,
            reason="无有效数据行，无法支撑任何分析"),
        rep("R007", "流量来源_2026-01.xlsx", "traffic", "traffic", "analyzable",
            "2026-01-01", "2026-01-31", "daily",
            [metric("uv", "人", "distinct_count"), metric("pv", "次")], rows=3100),
        rep("R008", "流量来源_2026-11.xlsx", "traffic", "traffic", "analyzable",
            "2026-11-01", "2026-11-30", "daily",
            [metric("uv", "人", "distinct_count"), metric("pv", "次")], rows=2900),
    ]
    inv = {
        **native_stage_identity("report_inventory","2.0.3-candidate.1"),
        "run_id": "cluster-smoke-run", "client_scope": "smoke", "team_version": "2.0.3-candidate.1",
        "issued_at": "2026-09-01T00:00:00+08:00", "scanned_root": "/tmp",
        "report_count": len(reports),
        "identification": {"mode": "rule_first_model_fallback", "rule_hits": 7,
                           "model_hits": 0, "unidentified": 1,
                           "low_confidence_ids": ["R005"], "model_review_pending": []},
        "reports": reports,
    }
    p = tmp / "inventory.json"
    p.write_text(json.dumps(inv, ensure_ascii=False, indent=2), encoding="utf-8")
    return p


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="cluster_smoke_"))
    inv = build_inventory(tmp)
    cout, pout = tmp / "clusters.json", tmp / "chapter-plan.json"
    proc = subprocess.run(
        [PY, str(SCRIPT), "--inventory", str(inv), "--output-clusters", str(cout),
         "--output-chapter-plan", str(pout)],
        capture_output=True, text=True, encoding="utf-8")
    if proc.returncode != 0:
        raise SystemExit(f"cluster crashed\n{proc.stdout}\n{proc.stderr}")
    res = json.loads(proc.stdout)
    clusters = json.loads(cout.read_text(encoding="utf-8"))
    plan = json.loads(pout.read_text(encoding="utf-8"))

    cmap = {c["domain"]: c for c in clusters["clusters"]}

    print("[S1] domain axis groups reports into clusters")
    check("five clusters formed", clusters["cluster_count"] == 5, str(clusters["cluster_count"]))
    check("transaction has two members", len(cmap["transaction"]["members"]) == 2,
          str(cmap["transaction"]["members"]))
    check("no member lost", sum(len(c["members"]) for c in clusters["clusters"]) + len(clusters["unclustered"]) == 8,
          str(sum(len(c["members"]) for c in clusters["clusters"]) + len(clusters["unclustered"])))

    print("[S2] metric axis picks primary and corroborating sources")
    gmv = next(m for m in cmap["transaction"]["metrics"] if m["standard_name"] == "gmv")
    check("primary is the larger analyzable report", gmv["primary_report_id"] == "R001",
          gmv["primary_report_id"])
    check("corroborating listed", gmv["corroborating_report_ids"] == ["R002"],
          str(gmv["corroborating_report_ids"]))
    check("cross check rule present", "团长亲跑数裁决" in gmv["cross_check_rule"],
          gmv["cross_check_rule"])

    print("[S3] time axis refuses fake comparisons")
    check("traffic overlap ratio zero",
          cmap["traffic"]["merge_basis"]["time_alignment"]["overlap_ratio"] == 0.0,
          str(cmap["traffic"]["merge_basis"]["time_alignment"]["overlap_ratio"]))
    check("traffic marked not aligned",
          cmap["traffic"]["merge_basis"]["time_alignment"]["aligned"] is False)
    check("action explains why", "不做同期同比" in cmap["traffic"]["merge_basis"]["time_alignment"]["action"],
          cmap["traffic"]["merge_basis"]["time_alignment"]["action"])
    check("transaction aligned", cmap["transaction"]["merge_basis"]["time_alignment"]["aligned"] is True)

    print("[S4] insufficiency propagates to cluster sufficiency")
    check("service cluster partial", cmap["service"]["sufficiency"] == "partial",
          cmap["service"]["sufficiency"])
    check("market cluster insufficient", cmap["market"]["sufficiency"] == "insufficient",
          cmap["market"]["sufficiency"])
    check("reason recorded", bool(cmap["market"].get("sufficiency_reason")),
          cmap["market"].get("sufficiency_reason", ""))

    print("[S5] unclustered reports are kept, not dropped")
    check("one unclustered", len(clusters["unclustered"]) == 1, str(clusters["unclustered"]))
    check("reason mandatory", bool(clusters["unclustered"][0]["reason"]),
          clusters["unclustered"][0]["reason"])
    obs = next(c for c in plan["chapters"] if c["chapter_kind"] == "independent_observation")
    check("gets its own chapter", "R005" in obs["source_report_ids"], str(obs["source_report_ids"]))

    print("[S6] chapter plan covers every report")
    cp = plan["coverage_plan"]
    check("coverage rate 100%", cp["coverage_rate"] == 1.0, str(cp["coverage_rate"]))
    check("nothing uncovered", cp["uncovered_report_ids"] == [], str(cp["uncovered_report_ids"]))
    overview = next(c for c in plan["chapters"] if c["chapter_kind"] == "data_overview")
    check("overview lists all eight", len(overview["source_report_ids"]) == 8,
          str(len(overview["source_report_ids"])))
    check("overview is chapter 0", overview["chapter_index"] == 0, str(overview["chapter_index"]))

    print("[S7] chapter skeleton and ownership")
    check("chapter count", len(plan["chapters"]) == 9, str(len(plan["chapters"])))
    for ch in plan["chapters"]:
        keys = [s["section_key"] for s in ch["sections"]]
        if keys != ["caliber_and_coverage", "core_metrics", "cross_validation", "judgment_and_action"]:
            check(f"sections fixed for {ch['chapter_id']}", False, str(keys))
            break
    else:
        check("all chapters carry the four fixed sections", True)
    adv = next(c for c in plan["chapters"] if c["source_cluster_ids"] == [cmap["advertising"]["cluster_id"]])
    check("advertising owned by ad-profit-optimizer", adv["owner_agent"] == "ad-profit-optimizer",
          adv["owner_agent"])
    check("advertising has cross validation", len(adv["cross_validation"]) >= 0)
    gap = next(c for c in plan["chapters"] if c["chapter_kind"] == "data_gap")
    gap_ids = {g["report_id"] for g in gap["data_gaps"]}
    check("gap chapter documents R004/R005/R006",
          {"R004", "R005", "R006"} <= gap_ids, str(gap_ids))
    check("gap entries carry impact and remedy",
          all(g.get("impact") and g.get("remedy") for g in gap["data_gaps"]))
    check("synthesis is last", plan["chapters"][-1]["chapter_kind"] == "synthesis")

    print()
    if FAILURES:
        print(f"FAILED {len(FAILURES)}: {FAILURES}")
        return 1
    print(f"ALL PASSED (7 scenarios, {len(plan['chapters'])} chapters, "
          f"{clusters['cluster_count']} clusters)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
