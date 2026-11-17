#!/usr/bin/env python3
"""Regression checks for analysis_depth_guard.py.

Covers: fully compliant L3 handoff passes, missing depth block fails,
description-only L1 submission fails at L2 bar, untethered baseline SHA fails,
weak self-check fails, BLOCKED data allows a documented downgrade,
and missing expected agent fails closed.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "analysis_depth_guard.py"

GOOD_DEPTH = {
    **__import__('artifact_contract').native_analysis_identity("depth_declaration","2.0.3"),
    "baseline_ack": {
        "baseline_sha256": "",  # filled at runtime
        "accepted": True,
        "deviations": [],
    },
    "depth_ladder": {
        "reached_level": "L3",
        "min_required_level": "L2",
        "level_evidence": {
            "L1": "本期 GMV 100000 元，较对比期 120000 元下降 16.7%，证据 E1/E2。",
            "L2": "按渠道拆为搜索 55%、推荐 30%、活动 15%；按商品拆为 TOP3 贡献 68%，证据 E3。",
            "L3": "下降主要由搜索渠道访客下滑驱动，替代解释为活动节奏错位，反证条件见 J1。",
            "L4": "未达到：缺退款与成本数据，无法给预算与利润决策。",
        },
    },
    "decomposition": [
        {
            "dimension": "渠道",
            "segments": [
                {"name": "搜索", "value": 55000, "share": "55%"},
                {"name": "推荐", "value": 30000, "share": "30%"},
                {"name": "活动", "value": 15000, "share": "15%"},
            ],
            "evidence_ids": ["E3"],
        }
    ],
    "minimum_analysis_set": [
        {"question": "核心指标变化多少", "status": "answered", "answer": "本期 GMV 100000 元，环比下降 16.7%，证据 E1/E2", "evidence_ids": ["E1"]},
        {"question": "变化集中在哪个渠道", "status": "answered", "answer": "集中在搜索渠道，占 GMV 的 55% 且降幅最大", "evidence_ids": ["E3"]},
        {"question": "是否受异常订单影响", "status": "answered", "answer": "已按 N1/N2 情景筛查，剔除后结论方向不被翻转", "evidence_ids": ["E4"]},
        {"question": "退款是否影响净销售", "status": "unanswerable", "blocker": "缺少退款明细导出，无法计算净销售与退款率"},
    ],
    "self_check": {
        "caliber_consistent": True,
        "denominator_comparable": True,
        "counterexample_considered": True,
        "sample_sufficient": True,
        "recomputable": True,
        "outlier_screened": True,
        "layered_fact_judgment_hypothesis": True,
    },
}

BODY = {
    **__import__('artifact_contract').native_handoff_identity("2.0.3"),
    "run_id": "run-2026-07-depth",
    "client_scope": "synthetic",
    "agent_id": "data-analyst",
    "agent_version": "2.0.3",
    "scope": {"platform": "tmall", "store": "s1", "period": "2026-07", "grain": "month"},
    "gate_status": "PASS",
    "status": "ready_for_review",
    "contribution_summary": "深度闸门样例",
    "facts": [{"id": "F1", "claim": "本期 GMV 100000 元", "evidence_ids": ["E1"]}],
    "judgments": [{
        "id": "J1", "claim": "下降由搜索渠道访客下滑驱动", "confidence": "medium",
        "evidence_ids": ["E3"], "counter_conditions": ["活动节奏错位时该结论不成立"],
    }],
    "hypotheses": [],
    "actions": [],
    "risks": [],
    "missing_data": ["退款明细"],
    "evidence_ledger": [
        {"id": "E1", "source": "raw.xlsx", "period": "2026-07", "metric": "GMV", "value": 100000, "status": "verified"}
    ],
}


def build(tmp: Path, name: str, depth: dict | None, body_extra: dict | None = None) -> Path:
    import copy

    payload = copy.deepcopy(BODY)
    if depth is not None:
        payload["analysis_depth"] = depth
    if body_extra:
        payload.update(body_extra)
    path = tmp / name
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    return path


def baseline_with(tmp: Path, digest: str) -> Path:
    payload = {
        **__import__('artifact_contract').native_baseline_identity("2.0.3"),
        "run_id": "run-2026-07-depth",
        "client_scope": "synthetic",
        "team_version": "2.0.3",
        "task_type": "monthly_report",
        "scope": {"platform": "tmall", "store": "s1", "period": "2026-07", "grain": "month"},
        "metric_contract": {
            "GMV": {"definition": "支付金额", "formula": "SUM(支付金额)",
                    "unit": "元", "denominator": "无"}
        },
        "authority_order": ["原始后台导出", "生意参谋", "截图", "转述"],
        "attribution_rules": {
            "refund_basis": "按原订单期间归属",
            "visitor_dedupe": "店铺去重",
            "paid_vs_organic": "以流量来源报表为准",
        },
        "known_conflicts": [],
        "issued_at": "2026-08-30T00:00:00Z",
    }
    path = tmp / "baseline-pack.json"
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    return path


def run(tmp: Path, pairs: list[str], baseline: Path | None, expect_agents: str | None = None) -> subprocess.CompletedProcess:
    cmd = [sys.executable, str(SCRIPT), "--output", str(tmp / "depth-guard.json"), "--pretty", "--min-level", "L2"]
    for pair in pairs:
        cmd += ["--handoff", pair]
    if baseline:
        cmd += ["--baseline", str(baseline)]
    if expect_agents:
        cmd += ["--expect-agents", expect_agents]
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")


def main() -> int:
    failures: list[str] = []

    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        base = baseline_with(tmp, "")
        base_sha = hashlib.sha256(base.read_bytes()).hexdigest()

        # Case 1: compliant L3 handoff must pass with baseline bound.
        import copy
        good = copy.deepcopy(GOOD_DEPTH)
        good["baseline_ack"]["baseline_sha256"] = base_sha
        p = build(tmp, "good.json", good)
        proc = run(tmp, [f"data-analyst={p}"], base)
        if proc.returncode != 0 or "depth_guard_passed" not in proc.stdout:
            failures.append(f"compliant_case_failed:{proc.stdout.strip()}{proc.stderr.strip()}")
        else:
            receipt=json.loads((tmp/'depth-guard.json').read_text(encoding='utf-8'))
            if receipt.get('contract_name')!='omni-ecom.analysis-depth-guard' or receipt.get('team_version')!='2.0.3':
                failures.append('depth_guard_v2_identity_missing')

        # Case 1b: a legacy depth declaration cannot pass under a current baseline.
        legacy_depth=copy.deepcopy(GOOD_DEPTH)
        for key in ('artifact_type','contract_name','contract_version','created_by_team_version','legacy_compatibility'):
            legacy_depth.pop(key)
        legacy_depth['schema_version']='1.0'; legacy_depth['baseline_ack']['baseline_sha256']=base_sha
        p_legacy=build(tmp,'legacy-depth.json',legacy_depth)
        proc=run(tmp,[f'data-analyst={p_legacy}'],base)
        if proc.returncode==0:
            failures.append('legacy_depth_declaration_not_blocked')

        # Case 2: missing depth block must be blocked.
        p = build(tmp, "no_depth.json", None)
        proc = run(tmp, [f"data-analyst={p}"], base)
        if proc.returncode == 0:
            failures.append("missing_depth_not_blocked")
        else:
            guard = json.loads((tmp / "depth-guard.json").read_text(encoding="utf-8"))
            if "depth_declaration_missing" not in guard["results"][0]["errors"]:
                failures.append("missing_depth_error_code_wrong")

        # Case 3: L1-only submission must fail at the L2 bar.
        shallow = copy.deepcopy(GOOD_DEPTH)
        shallow["baseline_ack"]["baseline_sha256"] = base_sha
        shallow["depth_ladder"]["reached_level"] = "L1"
        shallow["depth_ladder"]["level_evidence"]["L2"] = "待补"
        shallow.pop("decomposition", None)
        p = build(tmp, "shallow.json", shallow)
        proc = run(tmp, [f"data-analyst={p}"], base)
        if proc.returncode == 0:
            failures.append("shallow_l1_not_blocked")

        # Case 4: wrong baseline SHA must be blocked.
        wrong = copy.deepcopy(GOOD_DEPTH)
        wrong["baseline_ack"]["baseline_sha256"] = "f" * 64
        p = build(tmp, "wrong_sha.json", wrong)
        proc = run(tmp, [f"data-analyst={p}"], base)
        if proc.returncode == 0:
            failures.append("baseline_sha_mismatch_not_blocked")

        # Case 5: weak self-check (4 false) must be blocked.
        weak = copy.deepcopy(GOOD_DEPTH)
        weak["baseline_ack"]["baseline_sha256"] = base_sha
        for key in ("caliber_consistent", "denominator_comparable", "recomputable", "outlier_screened"):
            weak["self_check"][key] = False
        p = build(tmp, "weak.json", weak)
        proc = run(tmp, [f"data-analyst={p}"], base)
        if proc.returncode == 0:
            failures.append("weak_self_check_not_blocked")

        # Case 6: BLOCKED data with documented downgrade must pass.
        blocked_case = copy.deepcopy(GOOD_DEPTH)
        blocked_case["baseline_ack"]["baseline_sha256"] = base_sha
        blocked_case["depth_ladder"]["reached_level"] = "L1"
        blocked_case["depth_ladder"]["blocked_below"] = "退款与成本字段缺失，数据闸门 BLOCKED，仅交付清单与缺口"
        p = build(tmp, "blocked.json", blocked_case, {"gate_status": "BLOCKED", "judgments": []})
        proc = run(tmp, [f"data-analyst={p}"], base)
        if proc.returncode != 0:
            failures.append(f"blocked_downgrade_not_allowed:{proc.stdout.strip()}")

        # Case 7: missing expected agent must fail closed.
        good2 = copy.deepcopy(GOOD_DEPTH)
        good2["baseline_ack"]["baseline_sha256"] = base_sha
        p = build(tmp, "good2.json", good2)
        proc = run(tmp, [f"data-analyst={p}"], base, expect_agents="data-analyst,platform-ops")
        if proc.returncode == 0:
            failures.append("missing_expected_agent_not_blocked")

        # Case 8: an old baseline is history, not a current 2.0 analysis authority.
        legacy = json.loads(base.read_text(encoding="utf-8"))
        for key in ("artifact_type","contract_name","contract_version","created_by_team_version","legacy_compatibility"):
            legacy.pop(key)
        legacy["schema_version"]="1.0"
        base.write_text(json.dumps(legacy,ensure_ascii=False),encoding="utf-8")
        proc = run(tmp,[f"data-analyst={p}"],base)
        if proc.returncode == 0 or "baseline_identity_invalid" not in proc.stdout:
            failures.append("legacy_baseline_not_blocked")

    if failures:
        for item in failures:
            print(f"FAIL {item}")
        return 1
    print("analysis_depth_smoke_passed")
    return 0


class AnalysisDepthPipelineTests(unittest.TestCase):
    def test_analysis_depth_pipeline(self):
        self.assertEqual(main(),0)


if __name__ == "__main__":
    sys.exit(main())
