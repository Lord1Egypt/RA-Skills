#!/usr/bin/env python3
"""Deterministic smoke test for multi-agent collaboration visibility."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import copy
import contextlib
import io
import unittest
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from analysis_depth_smoke import GOOD_DEPTH, baseline_with
from analysis_depth_guard import check_handoff
from coverage_guard_smoke import make_inventory, rep, run_pipeline
from host_runtime import Runtime, sha
from quality_gate_smoke import write_scope_receipt


ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts" / "build_report_package.py"
WAITER = ROOT / "scripts" / "wait_for_agent_returns.py"
PUBLIC_GUARD = ROOT / "scripts" / "public_output_guard.py"
REVIEW_GUARD = ROOT / "scripts" / "review_guard.py"
COMPLETION_GATE = ROOT / "scripts" / "completion_gate.py"
UTF8_ENV = {
    **os.environ,
    "PYTHONUTF8": "1",
    "OMNI_ECOM_CLIENT_REGISTRY": str(ROOT / "config" / "client-brand-registry.json"),
}
TEAM_VERSION = json.loads((ROOT / "version-info.json").read_text(encoding="utf-8"))["team_version"]


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def handoff(agent_id: str, summary: str) -> dict[str, Any]:
    evidence_id = "E-" + agent_id
    visible_summary = summary + ("；覆盖 R001 交易.csv" if agent_id == "omni-ecom-team-lead" else "")
    return {
        **__import__('artifact_contract').native_handoff_identity(TEAM_VERSION),
        "run_id": "run-collaboration-smoke",
        "client_scope": "smoke-client",
        "agent_id": agent_id,
        "agent_version": TEAM_VERSION,
        "contribution_summary": summary,
        "scope": {"platform": "演示平台", "store": "脱敏店铺", "period": "2026-W01", "grain": "week"},
        "gate_status": "PASS",
        "status": "ready_for_review",
        "facts": [{"id": "F-" + agent_id, "claim": visible_summary, "evidence_ids": [evidence_id]}],
        "judgments": [],
        "hypotheses": [],
        "actions": [],
        "risks": [],
        "missing_data": [],
        "evidence_ledger": [{
            "id": evidence_id,
            "source": f"{agent_id}-source.json",
            "period": "2026-W01",
            "metric": "collaboration_smoke",
            "value": 1,
            "status": "verified",
        }],
    }


def main() -> int:
    checks: list[tuple[str, bool, str]] = []
    with tempfile.TemporaryDirectory(prefix="omni-ecom-collab-") as temp:
        work = Path(temp)
        files: dict[str, Path] = {}
        summaries = {
            "omni-ecom-team-lead": "完成任务拆解、冲突裁决和最终结论",
            "data-analyst": "完成数据质量闸门与指标复算",
            "platform-ops": "完成平台经营诊断",
            "content-live-growth": "完成内容与直播增长诊断",
            "ad-profit-optimizer": "完成投流与利润边界诊断",
            "delivery-review": "完成报告结构与交付复核",
        }
        for agent_id, summary in summaries.items():
            path = work / f"{agent_id}.json"
            write_json(path, handoff(agent_id, summary))
            files[agent_id] = path

        output = work / "complete"
        output.mkdir()
        inventory=make_inventory([rep('R001','交易.csv','trade_sales','transaction','analyzable')])
        inventory.update(**__import__('artifact_contract').native_stage_identity('report_inventory',TEAM_VERSION),
                         run_id='run-collaboration-smoke',client_scope='smoke-client',team_version=TEAM_VERSION)
        inv,clusters,chapter_plan=run_pipeline(output,inventory,'collaboration')
        baseline_path=baseline_with(output,'')
        baseline=json.loads(baseline_path.read_text(encoding='utf-8'))
        baseline.update(run_id='run-collaboration-smoke',client_scope='smoke-client',
                        team_version=TEAM_VERSION,created_by_team_version=TEAM_VERSION)
        baseline['scope'].update(platform='演示平台',store='脱敏店铺',period='2026-W01',grain='week')
        write_json(baseline_path,baseline)
        runtime=Runtime(output,'run-collaboration-smoke','smoke-client')
        runtime.init(TEAM_VERSION,'weekly_report')
        sealed={}
        for role in ('data-analyst','platform-ops','content-live-growth','ad-profit-optimizer'):
            body=json.loads(files[role].read_text(encoding='utf-8'))
            body['analysis_depth']=copy.deepcopy(GOOD_DEPTH)
            body['analysis_depth']['created_by_team_version']=TEAM_VERSION
            body['analysis_depth']['baseline_ack']['baseline_sha256']=sha(baseline_path)
            raw=output/f'raw/{role}.json'; write_json(raw,body)
            task_id="agent-" + role.replace("-", "_"); attempt='a1'
            started=output/f'observations/{role}.started.json'
            write_json(started,dict(run_id='run-collaboration-smoke',client_scope='smoke-client',host='codex',task_id=task_id,state='running',evidence_kind='synthetic_fixture'))
            runtime.start(role,'codex',task_id,attempt,str(started.relative_to(output)))
            returned_at=datetime.now(timezone.utc).isoformat()
            return_file=output/f'returns/{role}.return.json'
            write_json(return_file,dict(run_id='run-collaboration-smoke',agent_id=role,agent_task_id=task_id,attempt_id=attempt,return_status='completed',returned_at=returned_at,handoff_sha256=sha(raw),contribution_summary=summaries[role],response={'result':'ok'}))
            completed=output/f'observations/{role}.completed.json'
            write_json(completed,dict(run_id='run-collaboration-smoke',client_scope='smoke-client',host='codex',task_id=task_id,state='completed',evidence_kind='synthetic_fixture'))
            target=f'sealed/{role}.json'
            runtime.accept(role,'codex',task_id,attempt,str(raw.relative_to(output)),str(return_file.relative_to(output)),str(completed.relative_to(output)),target)
            sealed[role]=target
            files[role]=output/target
        runtime.close()
        depth_results=[check_handoff(role,files[role],json.loads(files[role].read_text(encoding='utf-8')),sha(baseline_path),'L2') for role in sealed]
        if any(item['status']!='passed' for item in depth_results):
            print(json.dumps({'status':'FAIL','reason':'synthetic_depth_setup_invalid','results':depth_results},ensure_ascii=False,indent=2))
            return 1
        canonical_files={role:json.loads(path.read_text(encoding='utf-8')) for role,path in files.items()}
        canonical_bytes={role:path.read_bytes() for role,path in files.items()}
        write_json(output/'quality-inputs.json',dict(run_id='run-collaboration-smoke',client_scope='smoke-client',report_revision='R1',inventory=inv.name,chapter_plan=chapter_plan.name,baseline=baseline_path.name,handoffs=sealed))
        claim_ledger = output / "claim-ledger.json"
        smoke_source = output / "smoke-source.csv"
        smoke_source.write_text("访客数,支付GMV,支付买家数,期间,平台,店铺,访客单位,金额单位,买家单位,访客价值单位,转化率单位\n100,1000,5,2026-W01,演示平台,脱敏店铺,人,元,人,元/人,%\n", encoding="utf-8")
        write_scope_receipt(output,dict(run_id='run-collaboration-smoke',client_scope='smoke-client',
                            team_version=TEAM_VERSION),[smoke_source])
        quality_config=json.loads((output/'quality-inputs.json').read_text(encoding='utf-8'))
        quality_config['run_scope']='run-scope.json'; write_json(output/'quality-inputs.json',quality_config)
        smoke_source_hash = __import__("hashlib").sha256(smoke_source.read_bytes()).hexdigest()
        write_json(claim_ledger, {
            **__import__('artifact_contract').native_claim_identity(TEAM_VERSION),
            "run_id": "run-collaboration-smoke",
            "client_scope": "smoke-client",
            "period": "2026-W01",
            "scope": {"platform": "演示平台", "store": "脱敏店铺"},
            "source_context_policy": "required",
            "claims": [
                {"claim_id": "C-visitors", "metric": "visitors", "value": 100, "unit": "人", "period": "2026-W01", "status": "verified", "source_ref": {"source_id": "traffic", "source_file": "smoke-source.csv", "sheet": "data", "range": "A2", "field": "访客数", "source_sha256": smoke_source_hash, "contexts": {"period":{"column":"D","field":"期间"},"platform":{"column":"E","field":"平台"},"store":{"column":"F","field":"店铺"},"unit":{"column":"G","field":"访客单位"}}}},
                {"claim_id": "C-gmv", "metric": "gmv", "value": 1000, "unit": "元", "period": "2026-W01", "status": "verified", "source_ref": {"source_id": "traffic", "source_file": "smoke-source.csv", "sheet": "data", "range": "B2", "field": "支付GMV", "source_sha256": smoke_source_hash, "contexts": {"period":{"column":"D","field":"期间"},"platform":{"column":"E","field":"平台"},"store":{"column":"F","field":"店铺"},"unit":{"column":"H","field":"金额单位"}}}},
                {"claim_id": "C-buyers", "metric": "paid_buyers", "value": 5, "unit": "人", "period": "2026-W01", "status": "verified", "source_ref": {"source_id": "traffic", "source_file": "smoke-source.csv", "sheet": "data", "range": "C2", "field": "支付买家数", "source_sha256": smoke_source_hash, "contexts": {"period":{"column":"D","field":"期间"},"platform":{"column":"E","field":"平台"},"store":{"column":"F","field":"店铺"},"unit":{"column":"I","field":"买家单位"}}}},
                {"claim_id": "C-uv-value", "metric": "uv_value", "value": 10, "unit": "元/人", "period": "2026-W01", "status": "derived", "source_ref": {"source_id": "traffic", "source_file": "smoke-source.csv", "sheet": "data", "range": "B2", "field": "支付GMV", "source_sha256": smoke_source_hash, "contexts": {"period":{"column":"D","field":"期间"},"platform":{"column":"E","field":"平台"},"store":{"column":"F","field":"店铺"},"unit":{"column":"J","field":"访客价值单位"}}}, "formula": {"name": "uv_value", "numerator": "gmv", "denominator": "visitors", "expression": "gmv / visitors"}, "inputs": ["C-gmv", "C-visitors"]},
                {"claim_id": "C-conversion", "metric": "conversion_rate", "value": 5, "unit": "%", "period": "2026-W01", "status": "derived", "source_ref": {"source_id": "traffic", "source_file": "smoke-source.csv", "sheet": "data", "range": "C2", "field": "支付买家数", "source_sha256": smoke_source_hash, "contexts": {"period":{"column":"D","field":"期间"},"platform":{"column":"E","field":"平台"},"store":{"column":"F","field":"店铺"},"unit":{"column":"K","field":"转化率单位"}}}, "formula": {"name": "conversion_rate", "numerator": "paid_buyers", "denominator": "visitors", "expression": "(paid_buyers / visitors) * 100"}, "inputs": ["C-buyers", "C-visitors"]}
            ]
        })
        command = [
            sys.executable,
            str(BUILDER),
            "--handoff", str(files["omni-ecom-team-lead"]),
            "--client-scope", "smoke-client",
            "--collaboration-mode", "comprehensive",
            "--task-type", "weekly_report",
            "--member-handoff", str(files["data-analyst"]),
            "--member-handoff", str(files["platform-ops"]),
            "--member-handoff", str(files["content-live-growth"]),
            "--member-handoff", str(files["ad-profit-optimizer"]),
            "--report-revision", "R1",
            "--claim-ledger", str(claim_ledger),
            "--output-dir", str(output),
        ]
        def retarget(target: Path) -> list[str]:
            target.mkdir(parents=True,exist_ok=True)
            (target/smoke_source.name).write_bytes(smoke_source.read_bytes())
            (target/claim_ledger.name).write_bytes(claim_ledger.read_bytes())
            result=list(command)
            result[result.index("--claim-ledger")+1]=str(target/claim_ledger.name)
            result[result.index("--output-dir")+1]=str(target)
            return result
        complete = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", env=UTF8_ENV)
        checks.append(("comprehensive_build", complete.returncode == 0, complete.stderr or complete.stdout))

        report_path = output / "report.json"
        report = json.loads(report_path.read_text(encoding="utf-8")) if report_path.is_file() else {}
        checks.append(("team_version", report.get("team_version") == TEAM_VERSION, str(report.get("team_version"))))
        checks.append(("weekly_task_profile", report.get("task_type") == "weekly_report" and report.get("task_profile", {}).get("period_grain") == "week", json.dumps(report.get("task_profile", {}), ensure_ascii=False)))
        pdf_receipt_path = output / "pdf-delivery.json"
        pdf_receipt = json.loads(pdf_receipt_path.read_text(encoding="utf-8")) if pdf_receipt_path.is_file() else {}
        checks.append((
            "default_chart_pdf",
            (output / "report.pdf").is_file()
            and pdf_receipt.get("status") == "pdf_render_verified"
            and int(pdf_receipt.get("chart_count", 0)) >= 3,
            json.dumps(pdf_receipt, ensure_ascii=False),
        ))
        participants = report.get("expert_participation", [])
        contributed = {item.get("agent_id") for item in participants if item.get("participation_status") == "contributed"}
        expected_draft = set(summaries) - {"delivery-review"}
        checks.append((
            "draft_role_visibility",
            len(participants) == 6 and contributed == expected_draft,
            f"roster={len(participants)}, contributed={sorted(contributed)}",
        ))
        pending_review = next((item for item in participants if item.get("agent_id") == "delivery-review"), {})
        checks.append(("delivery_review_visible_as_pending", pending_review.get("participation_status") == "pending_review", json.dumps(pending_review, ensure_ascii=False)))
        markdown = (output / "report.md").read_text(encoding="utf-8") if (output / "report.md").is_file() else ""
        checks.append(("markdown_review_candidate", "本次专家协作记录" in markdown and pending_review.get("participation_status") == "pending_review", "section/status"))
        task_ids = {
            task_id
            for item in participants
            if item.get("agent_id") != "omni-ecom-team-lead"
            for task_id in item.get("agent_task_ids", [])
        }
        checks.append(("four_analysis_task_ids", len(task_ids) == 4 and "Agent 子任务" in markdown, str(sorted(task_ids))))

        premature_review=copy.deepcopy(canonical_files["delivery-review"])
        premature_review.update(agent_task_id='agent-delivery_review_premature',agent_return_status='completed',
                                agent_returned_at='2026-08-11T12:00:00Z',agent_return_file='delivery-review.return.json',
                                agent_return_sha256='0'*64)
        write_json(files["delivery-review"],premature_review)
        review_before_command=retarget(work / "review-before-draft")
        review_before_command[review_before_command.index("--output-dir"):review_before_command.index("--output-dir")]=["--member-handoff",str(files["delivery-review"])]
        review_before_draft = subprocess.run(review_before_command, capture_output=True, text=True, encoding="utf-8", env=UTF8_ENV)
        review_before_text = review_before_draft.stdout + review_before_draft.stderr
        checks.append(("delivery_review_before_frozen_draft_blocks", review_before_draft.returncode != 0 and "review_order_invalid" in review_before_text, review_before_text))
        files["delivery-review"].write_bytes(canonical_bytes["delivery-review"])

        incomplete_output = work / "incomplete"
        incomplete_command=retarget(incomplete_output)
        while "--member-handoff" in incomplete_command:
            i=incomplete_command.index("--member-handoff"); del incomplete_command[i:i+2]
        incomplete = subprocess.run(incomplete_command, capture_output=True, text=True, encoding="utf-8", env=UTF8_ENV)
        incomplete_text = (incomplete.stderr or "") + (incomplete.stdout or "")
        blocked = incomplete.returncode != 0 and "collaboration_incomplete" in incomplete_text
        checks.append(("incomplete_collaboration_blocks", blocked, incomplete.stderr or incomplete.stdout))

        untraceable_payload = copy.deepcopy(canonical_files["data-analyst"])
        untraceable_payload.pop("agent_task_id", None)
        write_json(files["data-analyst"], untraceable_payload)
        untraceable_output = work / "untraceable"
        untraceable = subprocess.run(retarget(untraceable_output), capture_output=True, text=True, encoding="utf-8", env=UTF8_ENV)
        untraceable_text = (untraceable.stderr or "") + (untraceable.stdout or "")
        checks.append((
            "missing_agent_task_id_blocks",
            untraceable.returncode != 0 and "collaboration_untraceable" in untraceable_text,
            untraceable_text,
        ))

        unreturned_payload = copy.deepcopy(canonical_files["data-analyst"])
        unreturned_payload.pop("agent_return_status", None)
        write_json(files["data-analyst"], unreturned_payload)
        unreturned_output = work / "unreturned"
        unreturned = subprocess.run(retarget(unreturned_output), capture_output=True, text=True, encoding="utf-8", env=UTF8_ENV)
        unreturned_text = (unreturned.stderr or "") + (unreturned.stdout or "")
        checks.append((
            "missing_agent_return_blocks",
            unreturned.returncode != 0 and "collaboration_unreturned" in unreturned_text,
            unreturned_text,
        ))

        return_dir = work / "agent_returns"
        return_dir.mkdir()
        for agent_id in ("data-analyst", "platform-ops"):
            write_json(return_dir / f"{agent_id}.return.json", {
                "run_id": "run-collaboration-smoke",
                "agent_id": agent_id,
                "return_status": "completed",
                "returned_at": "2026-08-11T12:00:00Z",
                "contribution_summary": summaries[agent_id],
                "response": {"result": "ok"},
                "handoff_sha256": "a" * 64,
            })
        wait_ok = subprocess.run([
            sys.executable, str(WAITER),
            "--return-dir", str(return_dir),
            "--run-id", "run-collaboration-smoke",
            "--expected", "data-analyst,platform-ops",
            "--timeout", "2",
        ], capture_output=True, text=True, encoding="utf-8", env=UTF8_ENV)
        checks.append(("return_latch_releases", wait_ok.returncode == 0 and "all_agent_returns_received" in wait_ok.stdout, wait_ok.stdout + wait_ok.stderr))

        wait_timeout = subprocess.run([
            sys.executable, str(WAITER),
            "--return-dir", str(return_dir),
            "--run-id", "run-collaboration-smoke",
            "--expected", "data-analyst,delivery-review",
            "--timeout", "1",
            "--poll-seconds", "0.2",
        ], capture_output=True, text=True, encoding="utf-8", env=UTF8_ENV)
        checks.append(("return_latch_fails_closed", wait_timeout.returncode == 2 and "collaboration_wait_timeout" in wait_timeout.stdout, wait_timeout.stdout + wait_timeout.stderr))

        invalid_dir = work / "invalid_agent_returns"
        invalid_dir.mkdir()
        write_json(invalid_dir / "ad-profit-optimizer.return.json", {
            "run_id": "run-collaboration-smoke",
            "agent_id": "ad-profit-optimizer",
            "return_status": "completed",
            "returned_at": "2026-08-11T12:00:00Z",
            "response": {"result": "missing top-level contribution summary"},
        })
        wait_invalid = subprocess.run([
            sys.executable, str(WAITER),
            "--return-dir", str(invalid_dir),
            "--run-id", "run-collaboration-smoke",
            "--expected", "ad-profit-optimizer",
            "--timeout", "5",
            "--poll-seconds", "0.1",
            "--invalid-grace-seconds", "0",
        ], capture_output=True, text=True, encoding="utf-8", env=UTF8_ENV)
        checks.append((
            "invalid_terminal_return_fails_fast_for_new_attempt",
            wait_invalid.returncode == 4 and "agent_return_invalid" in wait_invalid.stdout and
            "contribution_summary_missing" in wait_invalid.stdout,
            wait_invalid.stdout + wait_invalid.stderr,
        ))

        wrong_hash_dir = work / "wrong_hash_agent_returns"
        wrong_hash_dir.mkdir()
        write_json(wrong_hash_dir / "data-analyst.return.json", {
            "run_id": "run-collaboration-smoke",
            "agent_id": "data-analyst",
            "return_status": "completed",
            "returned_at": "2026-08-11T12:00:00Z",
            "contribution_summary": summaries["data-analyst"],
            "response": {"result": "ok"},
            "raw_handoff_sha256": "a" * 64,
        })
        wait_wrong_hash = subprocess.run([
            sys.executable, str(WAITER),
            "--return-dir", str(wrong_hash_dir),
            "--run-id", "run-collaboration-smoke",
            "--expected", "data-analyst",
            "--timeout", "5",
            "--poll-seconds", "0.1",
            "--invalid-grace-seconds", "0",
        ], capture_output=True, text=True, encoding="utf-8", env=UTF8_ENV)
        checks.append((
            "return_latch_rejects_wrong_handoff_hash_field",
            wait_wrong_hash.returncode == 4 and "handoff_sha256_missing_or_invalid" in wait_wrong_hash.stdout,
            wait_wrong_hash.stdout + wait_wrong_hash.stderr,
        ))

        safe_public = work / "safe-public.md"
        current_client = "示例当前客户"
        safe_public.write_text(f"当前客户：{current_client}；采用品牌无关标准经营报告版式。", encoding="utf-8")
        guard_pass = subprocess.run([
            sys.executable, str(PUBLIC_GUARD), "--file", str(safe_public), "--allowed-term", current_client,
        ], capture_output=True, text=True, encoding="utf-8", env=UTF8_ENV)
        checks.append(("public_guard_allows_current_client", guard_pass.returncode == 0 and "public_output_guard_passed" in guard_pass.stdout, guard_pass.stdout + guard_pass.stderr))

        registry = json.loads((ROOT / "config" / "client-brand-registry.json").read_text(encoding="utf-8"))
        blocked_term = next(term for term in registry["registered_client_terms"] if term != current_client)
        leaked_public = work / "leaked-public.md"
        leaked_public.write_text(f"错误复用了其他客户：{blocked_term}", encoding="utf-8")
        guard_block = subprocess.run([
            sys.executable, str(PUBLIC_GUARD), "--file", str(leaked_public), "--allowed-term", current_client,
        ], capture_output=True, text=True, encoding="utf-8", env=UTF8_ENV)
        guard_text = guard_block.stdout + guard_block.stderr
        checks.append(("public_guard_blocks_cross_client_without_echo", guard_block.returncode == 2 and "client_scope_leak_blocked" in guard_text and blocked_term not in guard_text, guard_text))

        files["data-analyst"].write_bytes(canonical_bytes["data-analyst"])
        leaked_handoff = handoff("omni-ecom-team-lead", summaries["omni-ecom-team-lead"])
        leaked_handoff["facts"][0]["claim"] = f"错误引用其他客户 {blocked_term}"
        write_json(files["omni-ecom-team-lead"], leaked_handoff)
        integrated_block = subprocess.run(retarget(work / "integrated-leak"), capture_output=True, text=True, encoding="utf-8", env=UTF8_ENV)
        integrated_text = integrated_block.stdout + integrated_block.stderr
        checks.append(("report_builder_blocks_cross_client", integrated_block.returncode != 0 and "client_scope_leak_blocked" in integrated_text and blocked_term not in integrated_text, integrated_text))

        for agent_id in summaries:
            files[agent_id].write_bytes(canonical_bytes[agent_id])
        conflict = work / "conflict-resolution.md"
        conflict.write_text("冲突已按同平台、同期间、同口径裁决。", encoding="utf-8")

        missing_pdf_manifest = work / "missing-pdf-manifest.json"
        missing_pdf = subprocess.run([
            sys.executable, str(REVIEW_GUARD), "prepare",
            "--run-id", "run-collaboration-smoke",
            "--client-scope", "smoke-client",
            "--team-version", TEAM_VERSION,
            "--report-revision", "R1",
            "--artifact", str(output / "report.md"),
            "--artifact", str(output / "report.json"),
            "--artifact", str(output / "pdf-delivery.json"),
            "--artifact", str(conflict),
            "--source", str(files["omni-ecom-team-lead"]),
            "--output", str(missing_pdf_manifest),
        ], capture_output=True, text=True, encoding="utf-8", env=UTF8_ENV)
        missing_pdf_text = missing_pdf.stdout + missing_pdf.stderr
        checks.append(("missing_pdf_blocks_review", missing_pdf.returncode == 2 and "pdf_delivery_required" in missing_pdf_text, missing_pdf_text))

        if not (output / "pdf-delivery.json").is_file():
            print(json.dumps({"status": "FAIL", "reason": "initial_report_build_missing_pdf_receipt",
                              "builder_output": complete.stdout + complete.stderr}, ensure_ascii=False, indent=2))
            return 1
        original_pdf_receipt = (output / "pdf-delivery.json").read_text(encoding="utf-8")
        bad_pdf_receipt = json.loads(original_pdf_receipt)
        bad_pdf_receipt["chart_count"] = 2
        write_json(output / "pdf-delivery.json", bad_pdf_receipt)
        bad_pdf_manifest = work / "bad-pdf-manifest.json"
        bad_pdf = subprocess.run([
            sys.executable, str(REVIEW_GUARD), "prepare",
            "--run-id", "run-collaboration-smoke",
            "--client-scope", "smoke-client",
            "--team-version", TEAM_VERSION,
            "--report-revision", "R1",
            "--artifact", str(output / "report.md"),
            "--artifact", str(output / "report.json"),
            "--artifact", str(output / "report.pdf"),
            "--artifact", str(output / "pdf-delivery.json"),
            "--source", str(files["omni-ecom-team-lead"]),
            "--output", str(bad_pdf_manifest),
        ], capture_output=True, text=True, encoding="utf-8", env=UTF8_ENV)
        bad_pdf_text = bad_pdf.stdout + bad_pdf.stderr
        checks.append(("unverified_pdf_blocks_review", bad_pdf.returncode == 2 and "pdf_delivery_not_verified" in bad_pdf_text, bad_pdf_text))
        (output / "pdf-delivery.json").write_text(original_pdf_receipt, encoding="utf-8")

        mutable_return = work / "data-analyst.return.json"
        mutable_return.write_text(files["data-analyst"].read_text(encoding="utf-8"), encoding="utf-8")
        mutable_manifest = work / "mutable-source-manifest.json"
        mutable_review = subprocess.run([
            sys.executable, str(REVIEW_GUARD), "prepare",
            "--run-id", "run-collaboration-smoke",
            "--client-scope", "smoke-client",
            "--team-version", TEAM_VERSION,
            "--report-revision", "R1",
            "--artifact", str(output / "report.md"),
            "--artifact", str(output / "report.json"),
            "--artifact", str(output / "report.pdf"),
            "--artifact", str(output / "pdf-delivery.json"),
            "--source", str(mutable_return),
            "--output", str(mutable_manifest),
        ], capture_output=True, text=True, encoding="utf-8", env=UTF8_ENV)
        mutable_text = mutable_review.stdout + mutable_review.stderr
        checks.append(("mutable_return_source_blocks_freeze", mutable_review.returncode == 2 and "mutable_return_source_blocked" in mutable_text, mutable_text))

        manifest = output / "review-manifest.json"
        review_attempt_id = "delivery-review-r1-a1"
        attestation = output / "review" / "R1" / f"{review_attempt_id}.attestation.json"
        receipt = output / "release-receipt.json"
        prepare_review = subprocess.run([
            sys.executable, str(REVIEW_GUARD), "prepare",
            "--run-id", "run-collaboration-smoke",
            "--client-scope", "smoke-client",
            "--team-version", TEAM_VERSION,
            "--report-revision", "R1",
            "--artifact", str(output / "report.md"),
            "--artifact", str(output / "report.json"),
            "--artifact", str(output / "report.pdf"),
            "--artifact", str(output / "pdf-delivery.json"),
            "--artifact", str(conflict),
            *[value for agent_id in ("omni-ecom-team-lead", "data-analyst", "platform-ops", "content-live-growth", "ad-profit-optimizer") for value in ("--source", str(files[agent_id]))],
            "--output", str(manifest),
        ], capture_output=True, text=True, encoding="utf-8", env=UTF8_ENV)
        checks.append(("review_manifest_prepared", prepare_review.returncode == 0 and "review_manifest_prepared" in prepare_review.stdout, prepare_review.stdout + prepare_review.stderr))

        if not manifest.is_file():
            print(json.dumps({"status": "FAIL", "reason": "review_manifest_missing",
                              "review_output": prepare_review.stdout + prepare_review.stderr}, ensure_ascii=False, indent=2))
            return 1
        manifest_payload = json.loads(manifest.read_text(encoding="utf-8"))
        review_result = output / "review" / "R1" / f"{review_attempt_id}.return.json"
        result_attestation = attestation
        review_result.parent.mkdir(parents=True, exist_ok=True)
        write_json(review_result, {
            "schema_version": "2.0",
            "artifact_type": "review_result",
            "contract_name": "omni-ecom.review-result",
            "contract_version": "2.0",
            "created_by_team_version": TEAM_VERSION,
            "legacy_compatibility": {"read_only_import": ["omni-ecom.review-result@1.0"], "current_completion_authority": False},
            "run_id": "run-collaboration-smoke",
            "client_scope": "smoke-client",
            "agent_id": "delivery-review",
            "agent_version": TEAM_VERSION,
            "review_attempt_id": review_attempt_id,
            "report_revision": "R1",
            "return_status": "completed",
            "returned_at": "2099-08-13T00:00:00Z",
            "review_status": "passed",
            "reviewed_manifest_sha256": manifest_payload["manifest_sha256"],
            "reviewed_artifacts": [
                {"file": item["file"], "sha256": item["sha256"]}
                for item in manifest_payload["artifacts"]
            ],
            "findings": ["冻结报告、PDF 和来源一致"],
            "required_changes": [],
            "contribution_summary": "一次性独立复核通过",
        })

        review_runtime=Runtime(output,'run-collaboration-smoke','smoke-client')
        review_task_id='agent-delivery_review_result'
        started=output/'observations/delivery-review.started.json'
        write_json(started,dict(run_id='run-collaboration-smoke',client_scope='smoke-client',host='codex',task_id=review_task_id,state='running',evidence_kind='synthetic_fixture'))
        review_runtime.start('delivery-review','codex',review_task_id,review_attempt_id,str(started.relative_to(output)),str(manifest.relative_to(output)))
        review_return=output/'returns/delivery-review.return.json'
        write_json(review_return,dict(run_id='run-collaboration-smoke',agent_id='delivery-review',agent_task_id=review_task_id,attempt_id=review_attempt_id,return_status='completed',returned_at='2099-08-13T00:00:00Z',handoff_sha256=sha(review_result),contribution_summary='一次性独立复核通过',response={'review_status':'passed'}))
        completed=output/'observations/delivery-review.completed.json'
        write_json(completed,dict(run_id='run-collaboration-smoke',client_scope='smoke-client',host='codex',task_id=review_task_id,state='completed',evidence_kind='synthetic_fixture'))
        review_runtime.accept('delivery-review','codex',review_task_id,review_attempt_id,str(review_result.relative_to(output)),str(review_return.relative_to(output)),str(completed.relative_to(output)),'sealed/delivery-review.json')
        review_runtime.close()

        review_wait = subprocess.run([
            sys.executable, str(WAITER),
            "--return-dir", str(output),
            "--run-id", "run-collaboration-smoke",
            "--expected", "delivery-review",
            "--contract", "delivery_review",
            "--return-file", f"delivery-review=review/R1/{review_attempt_id}.return.json",
            "--timeout", "2",
        ], capture_output=True, text=True, encoding="utf-8", env=UTF8_ENV)
        checks.append(("delivery_review_latch_releases", review_wait.returncode == 0 and "all_agent_returns_received" in review_wait.stdout, review_wait.stdout + review_wait.stderr))

        wrong_attempt = subprocess.run([
            sys.executable, str(REVIEW_GUARD), "attest-result",
            "--manifest", str(manifest),
            "--review-result", str(review_result),
            "--agent-task-id", "agent-delivery_review_wrong_attempt",
            "--review-attempt-id", "delivery-review-r1-a2",
            "--output", str(work / "wrong-attempt.attestation.json"),
        ], capture_output=True, text=True, encoding="utf-8", env=UTF8_ENV)
        checks.append(("review_attempt_mismatch_blocks", wrong_attempt.returncode == 2 and "review_attempt_mismatch" in (wrong_attempt.stdout + wrong_attempt.stderr), wrong_attempt.stdout + wrong_attempt.stderr))

        attest_from_result = subprocess.run([
            sys.executable, str(REVIEW_GUARD), "attest-result",
            "--manifest", str(manifest),
            "--review-result", str(review_result),
            "--agent-task-id", review_task_id,
            "--review-attempt-id", review_attempt_id,
            "--output", str(result_attestation),
        ], capture_output=True, text=True, encoding="utf-8", env=UTF8_ENV)
        checks.append(("one_shot_review_result_attested", attest_from_result.returncode == 0 and "delivery_review_result_attested" in attest_from_result.stdout, attest_from_result.stdout + attest_from_result.stderr))

        freeform_attest = subprocess.run([
            sys.executable, str(REVIEW_GUARD), "attest",
            "--manifest", str(manifest),
            "--agent-task-id", "agent-delivery_review_r1",
            "--review-status", "passed",
            "--summary", "最终候选稿、裁决和来源复核通过",
            "--output", str(work / "freeform-attestation.json"),
        ], capture_output=True, text=True, encoding="utf-8", env=UTF8_ENV)
        checks.append(("freeform_attest_disabled", freeform_attest.returncode == 2 and "freeform_attest_disabled_use_attest_result" in (freeform_attest.stdout + freeform_attest.stderr), freeform_attest.stdout + freeform_attest.stderr))

        verify_pass = subprocess.run([
            sys.executable, str(REVIEW_GUARD), "verify",
            "--manifest", str(manifest),
            "--attestation", str(attestation),
            "--receipt", str(receipt),
        ], capture_output=True, text=True, encoding="utf-8", env=UTF8_ENV)
        checks.append(("review_release_verified", verify_pass.returncode == 0 and "review_release_verified" in verify_pass.stdout and receipt.is_file(), verify_pass.stdout + verify_pass.stderr))

        public_receipt = output / "public-output-receipt.json"
        public_check = subprocess.run([
            sys.executable, str(PUBLIC_GUARD),
            "--file", str(output / "report.json"),
            "--file", str(output / "report.md"),
            "--file", str(output / "report.pdf"),
            "--team-version", TEAM_VERSION,
            "--output", str(public_receipt),
        ], capture_output=True, text=True, encoding="utf-8", env=UTF8_ENV)
        checks.append(("public_guard_receipt_created", public_check.returncode == 0 and public_receipt.is_file(), public_check.stdout + public_check.stderr))

        blocked_completion = subprocess.run([
            sys.executable, str(COMPLETION_GATE),
            "--report-dir", str(output),
            "--public-guard-receipt", str(public_receipt),
            "--claim-receipt", str(output / "claim-receipt.json"),
            "--output", str(work / "blocked-completion-receipt.json"),
        ], capture_output=True, text=True, encoding="utf-8", env=UTF8_ENV)
        checks.append(("completion_without_review_stays_blocked", blocked_completion.returncode != 0 and not (work / "blocked-completion-receipt.json").exists(), blocked_completion.stdout + blocked_completion.stderr))

        completion_receipt = output / "completion-receipt.json"
        completion = subprocess.run([
            sys.executable, str(COMPLETION_GATE),
            "--report-dir", str(output),
            "--public-guard-receipt", str(public_receipt),
            "--manifest", str(manifest),
            "--attestation", str(result_attestation),
            "--release-receipt", str(receipt),
            "--claim-receipt", str(output / "claim-receipt.json"),
            "--output", str(completion_receipt),
        ], capture_output=True, text=True, encoding="utf-8", env=UTF8_ENV)
        is_candidate = "-candidate." in TEAM_VERSION
        if is_candidate:
            checks.append(("candidate_cannot_issue_formal_completion", completion.returncode == 2 and "candidate_version_not_release_ready" in (completion.stdout + completion.stderr) and not completion_receipt.exists(), completion.stdout + completion.stderr))
        else:
            value = json.loads(completion_receipt.read_text(encoding="utf-8")) if completion_receipt.exists() else {}
            checks.append(("formal_pipeline_completes", completion.returncode == 0 and value.get("status") == "formal_delivery_complete", completion.stdout + completion.stderr))

        candidate_receipt = output / "candidate-acceptance-receipt.json"
        candidate_completion = subprocess.run([
            sys.executable, str(COMPLETION_GATE),
            "--report-dir", str(output),
            "--public-guard-receipt", str(public_receipt),
            "--manifest", str(manifest),
            "--attestation", str(result_attestation),
            "--release-receipt", str(receipt),
            "--claim-receipt", str(output / "claim-receipt.json"),
            "--candidate-acceptance",
            "--output", str(candidate_receipt),
        ], capture_output=True, text=True, encoding="utf-8", env=UTF8_ENV)
        candidate_value = json.loads(candidate_receipt.read_text(encoding="utf-8")) if candidate_receipt.is_file() else {}
        candidate_ok = (candidate_completion.returncode == 0
                       and candidate_value.get("status") == "candidate_pipeline_complete"
                       and candidate_value.get("artifact_type") == "candidate_runtime_acceptance"
                       and candidate_value.get("legacy_compatibility", {}).get("current_completion_authority") is False
                       and not completion_receipt.exists())
        checks.append(("candidate_mode_isolated_from_formal_release",
                       candidate_ok if is_candidate else candidate_completion.returncode != 0 and not candidate_receipt.exists(),
                       candidate_completion.stdout + candidate_completion.stderr))

        original_report = (output / "report.md").read_text(encoding="utf-8")
        (output / "report.md").write_text(original_report + "\n复核后错误改稿\n", encoding="utf-8")
        stale_report = subprocess.run([
            sys.executable, str(REVIEW_GUARD), "verify", "--manifest", str(manifest), "--attestation", str(attestation),
        ], capture_output=True, text=True, encoding="utf-8", env=UTF8_ENV)
        stale_report_text = stale_report.stdout + stale_report.stderr
        checks.append(("report_edit_after_review_blocks", stale_report.returncode == 2 and "review_stale_blocked" in stale_report_text, stale_report_text))
        (output / "report.md").write_text(original_report, encoding="utf-8")

        original_pdf = (output / "report.pdf").read_bytes()
        (output / "report.pdf").write_bytes(original_pdf + b"stale")
        stale_pdf = subprocess.run([
            sys.executable, str(REVIEW_GUARD), "verify", "--manifest", str(manifest), "--attestation", str(attestation),
        ], capture_output=True, text=True, encoding="utf-8", env=UTF8_ENV)
        stale_pdf_text = stale_pdf.stdout + stale_pdf.stderr
        checks.append(("pdf_edit_after_review_blocks", stale_pdf.returncode == 2 and "review_stale_blocked" in stale_pdf_text, stale_pdf_text))
        (output / "report.pdf").write_bytes(original_pdf)

        original_source = files["data-analyst"].read_text(encoding="utf-8")
        files["data-analyst"].write_text(original_source + "\n", encoding="utf-8")
        stale_source = subprocess.run([
            sys.executable, str(REVIEW_GUARD), "verify", "--manifest", str(manifest), "--attestation", str(attestation),
        ], capture_output=True, text=True, encoding="utf-8", env=UTF8_ENV)
        stale_source_text = stale_source.stdout + stale_source.stderr
        checks.append(("source_change_after_review_blocks", stale_source.returncode == 2 and "review_stale_blocked" in stale_source_text, stale_source_text))
        files["data-analyst"].write_text(original_source, encoding="utf-8")

        conditional_attempt_id = "delivery-review-r1-conditional"
        conditional_result = work / "review" / "R1" / f"{conditional_attempt_id}.return.json"
        conditional = work / "review" / "R1" / f"{conditional_attempt_id}.attestation.json"
        write_json(conditional_result, {
            "schema_version": "2.0",
            "artifact_type": "review_result",
            "contract_name": "omni-ecom.review-result",
            "contract_version": "2.0",
            "created_by_team_version": TEAM_VERSION,
            "legacy_compatibility": {"read_only_import": ["omni-ecom.review-result@1.0"], "current_completion_authority": False},
            "run_id": "run-collaboration-smoke",
            "client_scope": "smoke-client",
            "agent_id": "delivery-review",
            "agent_version": TEAM_VERSION,
            "review_attempt_id": conditional_attempt_id,
            "report_revision": "R1",
            "return_status": "completed",
            "returned_at": "2099-08-13T00:00:00Z",
            "review_status": "conditional_pass",
            "reviewed_manifest_sha256": manifest_payload["manifest_sha256"],
            "reviewed_artifacts": [{"file": item["file"], "sha256": item["sha256"]} for item in manifest_payload["artifacts"]],
            "findings": ["行动负责人缺失"],
            "required_changes": ["补齐行动负责人"],
            "contribution_summary": "存在必改项",
        })
        attest_conditional = subprocess.run([
            sys.executable, str(REVIEW_GUARD), "attest-result",
            "--manifest", str(manifest),
            "--review-result", str(conditional_result),
            "--agent-task-id", "agent-delivery_review_conditional",
            "--review-attempt-id", conditional_attempt_id,
            "--output", str(conditional),
        ], capture_output=True, text=True, encoding="utf-8", env=UTF8_ENV)
        verify_conditional = subprocess.run([
            sys.executable, str(REVIEW_GUARD), "verify", "--manifest", str(manifest), "--attestation", str(conditional),
        ], capture_output=True, text=True, encoding="utf-8", env=UTF8_ENV)
        conditional_text = verify_conditional.stdout + verify_conditional.stderr
        checks.append(("conditional_pass_cannot_release", attest_conditional.returncode == 0 and verify_conditional.returncode == 2 and "review_not_passed_blocked" in conditional_text, conditional_text))

    failed = [item for item in checks if not item[1]]
    result = {
        "status": "PASS" if not failed else "FAIL",
        "total": len(checks),
        "passed": len(checks) - len(failed),
        "failed": len(failed),
        "checks": [{"name": name, "status": "PASS" if ok else "FAIL", "detail": detail.strip()} for name, ok, detail in checks],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failed else 1


class CollaborationPipelineTests(unittest.TestCase):
    def test_complete_candidate_multi_agent_report_pipeline(self):
        stream=io.StringIO()
        with contextlib.redirect_stdout(stream),contextlib.redirect_stderr(stream):
            code=main()
        self.assertEqual(code,0,stream.getvalue())


if __name__ == "__main__":
    raise SystemExit(main())
