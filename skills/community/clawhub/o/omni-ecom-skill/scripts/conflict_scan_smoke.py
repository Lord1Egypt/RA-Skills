#!/usr/bin/env python3
"""Regression checks for conflict_scan.py.

Covers: clean scan, numeric hard conflict, direction hard conflict,
caliber conflict via baseline deviation, missing handoff fail-closed,
and run_id mismatch fail-closed.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "conflict_scan.py"

BASE_EVIDENCE = [
    {"id": "E1", "source": "raw.xlsx", "period": "2026-07", "metric": "GMV", "value": 100000, "status": "verified"}
]


def write_handoff(path: Path, agent_id: str, extra: dict) -> None:
    payload = {
        **__import__('artifact_contract').native_handoff_identity("2.0.3-candidate.1"),
        "run_id": "run-2026-07-smoke",
        "client_scope": "synthetic",
        "agent_id": agent_id,
        "agent_version": "2.0.3-candidate.1",
        "scope": {"platform": "tmall", "store": "s1", "period": "2026-07", "grain": "month"},
        "gate_status": "PASS",
        "status": "ready_for_review",
        "contribution_summary": "基线成员",
        "facts": [{"id": "F1", "claim": "GMV 为 100000", "evidence_ids": ["E1"]}],
        "judgments": [],
        "hypotheses": [],
        "actions": [],
        "risks": [],
        "missing_data": [],
        "evidence_ledger": BASE_EVIDENCE,
    }
    payload.update(extra)
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


def run(tmp: Path, pairs: list[str], run_id: str | None = "run-2026-07-smoke",
        baseline: Path | None = None) -> subprocess.CompletedProcess:
    cmd = [sys.executable, str(SCRIPT), "--output", str(tmp / "conflict-scan.json"), "--pretty"]
    for pair in pairs:
        cmd += ["--handoff", pair]
    if run_id:
        cmd += ["--run-id", run_id]
    baseline=baseline or (tmp/'baseline-pack.json')
    cmd += ["--baseline", str(baseline)]
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")


def main() -> int:
    failures: list[str] = []

    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)

        # Case 1: clean scan - identical numbers, no opposing claims.
        a = tmp / "a.json"
        b = tmp / "b.json"
        write_handoff(a, "data-analyst", {})
        write_handoff(b, "platform-ops", {})
        baseline={**__import__('artifact_contract').native_baseline_identity('2.0.3-candidate.1'),
                  'run_id':'run-2026-07-smoke','client_scope':'synthetic','team_version':'2.0.3-candidate.1',
                  'task_type':'monthly_report','scope':{'platform':'tmall','store':'s1','period':'2026-07','grain':'month'},
                  'metric_contract':{},'authority_order':['原始后台导出'],
                  'attribution_rules':{'refund_basis':'原订单期','visitor_dedupe':'店铺去重','paid_vs_organic':'来源报表'},
                  'known_conflicts':[],'issued_at':'2026-09-08T00:00:00Z'}
        baseline_path=tmp/'baseline-pack.json'
        baseline_path.write_text(json.dumps(baseline,ensure_ascii=False),encoding='utf-8')
        proc = run(tmp, [f"data-analyst={a}", f"platform-ops={b}"],baseline=baseline_path)
        if proc.returncode != 0 or "conflict_scan_clean" not in proc.stdout:
            failures.append(f"clean_case_failed:{proc.stdout.strip()}{proc.stderr.strip()}")
        else:
            scan=json.loads((tmp/'conflict-scan.json').read_text(encoding='utf-8'))
            if scan.get('contract_name')!='omni-ecom.conflict-scan' or scan.get('team_version')!='2.0.3-candidate.1':
                failures.append('conflict_scan_v2_identity_missing')

        # Case 2: numeric hard conflict on a core metric.
        write_handoff(
            a, "data-analyst",
            {"evidence_ledger": [
                {"id": "E1", "source": "raw.xlsx", "period": "2026-07", "metric": "GMV", "value": 100000, "status": "verified"}
            ]},
        )
        write_handoff(
            b, "platform-ops",
            {"evidence_ledger": [
                {"id": "E2", "source": "raw.xlsx", "period": "2026-07", "metric": "GMV", "value": 250000, "status": "verified"}
            ]},
        )
        proc = run(tmp, [f"data-analyst={a}", f"platform-ops={b}"])
        if "conflict_scan_hard_blocked" not in proc.stdout:
            failures.append(f"numeric_case_failed:{proc.stdout.strip()}")
        else:
            scan = json.loads((tmp / "conflict-scan.json").read_text(encoding="utf-8"))
            if not any(c["type"] == "numeric" and c["lead_recomputation_required"] for c in scan["conflicts"]):
                failures.append("numeric_case_missing_lead_recomputation")

        # Case 3: direction conflict - one says conversion up, other says collapsed.
        write_handoff(a, "data-analyst", {
            "evidence_ledger": BASE_EVIDENCE,
            "judgments": [{"id": "J1", "claim": "转化率同比上升，流量质量改善",
                           "confidence": "medium", "evidence_ids": ["E1"], "counter_conditions": ["样本不足"]}],
        })
        write_handoff(b, "platform-ops", {
            "evidence_ledger": BASE_EVIDENCE,
            "judgments": [{"id": "J2", "claim": "转化率崩塌，承接链路恶化",
                           "confidence": "high", "evidence_ids": ["E1"], "counter_conditions": ["口径变化"]}],
        })
        proc = run(tmp, [f"data-analyst={a}", f"platform-ops={b}"])
        if "conflict_scan_hard_blocked" not in proc.stdout:
            failures.append(f"direction_case_failed:{proc.stdout.strip()}")
        else:
            scan = json.loads((tmp / "conflict-scan.json").read_text(encoding="utf-8"))
            if not any(c["type"] == "direction" for c in scan["conflicts"]):
                failures.append("direction_case_not_detected")

        # Case 4: caliber conflict via baseline deviation on 访客数.
        write_handoff(a, "data-analyst", {
            "evidence_ledger": [
                {"id": "E3", "source": "raw.xlsx", "period": "2026-07", "metric": "访客数", "value": 5000, "status": "verified"}
            ],
            "analysis_depth": {"baseline_ack": {"baseline_sha256": "0" * 64, "accepted": False,
                                                "deviations": [{"item": "访客数去重", "reason": "使用店铺去重口径"}]}},
        })
        write_handoff(b, "platform-ops", {
            "evidence_ledger": [
                {"id": "E4", "source": "raw.xlsx", "period": "2026-07", "metric": "访客数", "value": 9000, "status": "verified"}
            ],
            "analysis_depth": {"baseline_ack": {"baseline_sha256": "0" * 64, "accepted": False,
                                                "deviations": [{"item": "访客数去重", "reason": "SPU 访客加总"}]}},
        })
        proc = run(tmp, [f"data-analyst={a}", f"platform-ops={b}"])
        if "conflict_scan_hard_blocked" not in proc.stdout:
            failures.append(f"caliber_case_failed:{proc.stdout.strip()}")

        # Case 5: missing handoff must fail closed.
        proc = run(tmp, [f"data-analyst={tmp / 'nope.json'}"])
        if proc.returncode == 0:
            failures.append("missing_handoff_not_blocked")

        # Case 6: run_id mismatch must fail closed.
        write_handoff(a, "data-analyst", {"run_id": "other-run"})
        proc = run(tmp, [f"data-analyst={a}"])
        if proc.returncode == 0:
            failures.append("run_id_mismatch_not_blocked")

        # Case 7: legacy baseline cannot be used for a current scan.
        write_handoff(a,"data-analyst",{})
        legacy=dict(baseline); legacy['schema_version']='1.0'
        for key in ('artifact_type','contract_name','contract_version','created_by_team_version','legacy_compatibility'):
            legacy.pop(key)
        baseline_path.write_text(json.dumps(legacy,ensure_ascii=False),encoding='utf-8')
        proc=run(tmp,[f"data-analyst={a}"],baseline=baseline_path)
        if proc.returncode==0 or 'baseline_identity_invalid' not in proc.stdout:
            failures.append('legacy_baseline_scan_not_blocked')

    if failures:
        for item in failures:
            print(f"FAIL {item}")
        return 1
    print("conflict_scan_smoke_passed")
    return 0


class ConflictScanPipelineTests(unittest.TestCase):
    def test_conflict_scan_pipeline(self):
        self.assertEqual(main(),0)


if __name__ == "__main__":
    sys.exit(main())
