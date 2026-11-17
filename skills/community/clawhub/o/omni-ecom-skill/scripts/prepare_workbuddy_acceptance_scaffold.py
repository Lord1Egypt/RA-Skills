#!/usr/bin/env python3
"""Create immutable, schema-valid artifacts for a no-client-data native-host acceptance."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from artifact_contract import (
    native_analysis_identity,
    native_baseline_identity,
    native_stage_identity,
    native_team_bootstrap_identity,
    native_claim_identity,
    native_handoff_identity,
    native_run_scope_identity,
    validate_baseline_identity,
    validate_stage_identity,
    validate_team_bootstrap_identity,
)
from host_runtime import Runtime
from prepare_agent_task_cards import analysis_cards


ACCEPTANCE_SCOPE = "runtime-acceptance-no-client-data"
ROLE_CHAPTERS = (
    ("data-analyst", "运行身份与回传证据核查", ["阶段任务完成状态", "成员回传计数", "回传凭证 SHA256 完整性"]),
    ("platform-ops", "调度与平台侧闸门证据核查", ["team-bootstrap 有效性", "launch-manifest 完整性", "阶段任务登记一致性"]),
    ("content-live-growth", "协作机制与回传链路核查", ["SendMessage 单次回传约束", "attempt_id=a1 一致性", "handoff 契约字段完整性"]),
    ("ad-profit-optimizer", "闸门脚本与成本边界核查", ["闸门脚本通过状态", "无经营数字约束遵守情况", "凭证链完整性"]),
)


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError("acceptance_lead_card_invalid")
    return value


def write_new(path: Path, payload: dict[str, Any]) -> None:
    if path.exists():
        raise ValueError(f"acceptance_scaffold_conflict:{path.name}")
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sections() -> list[dict[str, str]]:
    return [
        {"section_key": "caliber_and_coverage", "title": "口径与覆盖", "requirement": "写明本次无客户业务数据，只核查运行凭证和闸门产物。"},
        {"section_key": "core_metrics", "title": "核心指标", "requirement": "只列可从运行目录复核的验收事实，不得出现经营数字。"},
        {"section_key": "cross_validation", "title": "跨文件交叉验证", "requirement": "交叉核对运行证据文件身份、哈希与状态的一致性。"},
        {"section_key": "judgment_and_action", "title": "判断与行动", "requirement": "本次验收保持 judgments、hypotheses、actions 三个数组为空；不得写原因、导致、归因、建议或经营结论。"},
    ]


def chapter(index: int, title: str, kind: str, owner: str, metrics: list[str]) -> dict[str, Any]:
    item = {
        "chapter_index": index,
        "chapter_id": f"CH{index:02d}",
        "title": title,
        "chapter_kind": kind,
        "source_report_ids": [],
        "owner_agent": owner,
        "caliber": {"metric_definitions": [], "denominator": "不适用：无经营指标数据", "time_alignment": "单次运行，不适用同期同比"},
        "key_metrics": metrics,
        "sections": sections(),
    }
    if kind == "domain_analysis":
        item["cross_validation"] = []
    if kind == "data_gap":
        item["data_gaps"] = []
    return item


def prepare_scaffold(lead_card_path: Path, plugin_dir: Path) -> dict[str, Any]:
    lead_card_path = lead_card_path.resolve()
    plugin_dir = plugin_dir.resolve()
    card = load_json(lead_card_path)
    host = str(card.get("host") or "workbuddy")
    if host not in {"workbuddy", "codex"}:
        raise ValueError("acceptance_host_invalid")
    required = {
        "schema_version": "2.0",
        "artifact_type": f"{host}_acceptance_lead_card",
        "client_scope": ACCEPTANCE_SCOPE,
        "immutable_after_launch": True,
    }
    if any(card.get(key) != value for key, value in required.items()):
        raise ValueError("acceptance_lead_card_identity_invalid")
    version = str(card.get("version") or "")
    run_id = str(card.get("run_id") or "")
    team_name = str(card.get("team_name") or "")
    run_dir = Path(str(card.get("run_dir") or "")).resolve()
    if not version or not run_id or (host == "workbuddy" and not team_name) or not run_dir.is_relative_to(lead_card_path.parent):
        raise ValueError("acceptance_lead_card_scope_invalid")
    metadata_path = plugin_dir / "version-info.json"
    package_version = (load_json(metadata_path).get("team_version") if metadata_path.is_file()
                       else load_json(plugin_dir / ".codebuddy-plugin" / "plugin.json").get("version"))
    if package_version != version:
        raise ValueError("acceptance_plugin_version_mismatch")
    if run_dir.exists():
        raise ValueError("acceptance_run_already_exists")
    run_dir.mkdir(parents=True)
    issued_at = datetime.now(timezone.utc).isoformat()
    source_path = run_dir / "acceptance-source.csv"
    host_label = "WorkBuddy" if host == "workbuddy" else "Codex"
    source_path.write_text(
        "访客数,支付GMV,支付买家数,期间,平台,店铺,访客单位,金额单位,买家单位,访客价值单位,转化率单位\n"
        f"100,1000,5,2026-W36,{host_label}验收环境,无客户测试店铺,人,元,人,元/人,%\n",
        encoding="utf-8",
    )

    if host == "workbuddy":
        bootstrap = {
            **native_team_bootstrap_identity(version), "run_id": run_id, "client_scope": ACCEPTANCE_SCOPE,
            "team_version": version, "host": "workbuddy", "status": "team_created", "team_name": team_name,
            "host_mode": "interactive", "created_at": issued_at,
        }
        write_new(run_dir / "team-bootstrap.json", bootstrap)
        validate_team_bootstrap_identity(bootstrap, version, run_id, ACCEPTANCE_SCOPE)

    orchestration = {
        **native_analysis_identity("orchestration_plan", version), "run_id": run_id,
        "client_scope": ACCEPTANCE_SCOPE, "team_version": version, "host": host,
        "bootstrap_mode": "teamcreate_direct" if host == "workbuddy" else "codex_native_subagents",
        "member_launcher": "Agent" if host == "workbuddy" else "spawn_agent", "wait_tool": "TaskOutput" if host == "workbuddy" else "wait_agent",
        "message_tool": "SendMessage" if host == "workbuddy" else "send_message", "required_roles": [role for role, _, _ in ROLE_CHAPTERS] + ["delivery-review"],
        "observed_capabilities": ["Agent", "SendMessage", "TaskCreate", "TaskList", "TaskOutput", "TaskUpdate", "TeamCreate"] if host == "workbuddy" else ["spawn_agent", "wait_agent", "send_message"],
        "forbidden_tools": ["spawn_agent", "wait_agent", "send_message"] if host == "workbuddy" else ["TeamCreate", "TaskCreate", "TaskList", "TaskUpdate", "Agent", "TaskOutput", "SendMessage"],
        "ordered_steps": (["TeamCreate"] if host == "workbuddy" else []) + ["固定脚手架", "四位分析专家", "团长裁决与报告", "delivery-review", "候选完成门禁"],
        "runtime_evidence_required": True, "orchestration_completed": False, "status": "planned_not_executed",
    }
    write_new(run_dir / "host-orchestration-plan.json", orchestration)

    inventory = {
        **native_stage_identity("report_inventory", version), "team_version": version, "run_id": run_id,
        "client_scope": ACCEPTANCE_SCOPE, "issued_at": issued_at, "scanned_root": str(run_dir), "report_count": 0,
        "identification": {"mode": "rule_first_model_fallback", "type_taxonomy_version": "2.0", "domain_taxonomy_version": "2.0", "rule_hits": 0, "model_hits": 0, "unidentified": 0, "model_review_pending": []},
        "reports": [{
            "report_id": "R001", "file_name": source_path.name, "file_path": str(source_path), "file_ext": ".csv",
            "size_bytes": source_path.stat().st_size, "platform": "unknown", "report_type": "trade_sales", "domain": "transaction",
            "report_type_label": "透明验收测试数据（非客户经营数据）", "confidence": "high", "identified_by": "manual",
            "identify_evidence": ["固定验收程序生成，数值仅用于验证公式、图表和 PDF 链路"],
            "time_scope": {"start": "2026-08-31", "end": "2026-09-06", "time_column": "期间", "has_explicit_time": True, "note": "2026-W36"},
            "granularity": "snapshot", "row_count": 1, "column_count": 11,
            "metrics": [{"raw_name": "访客数", "standard_name": "visitors", "unit": "人", "aggregation": "sum", "is_core": True}, {"raw_name": "支付GMV", "standard_name": "gmv", "unit": "元", "aggregation": "sum", "is_core": True}, {"raw_name": "支付买家数", "standard_name": "paid_buyers", "unit": "人", "aggregation": "sum", "is_core": True}],
            "dimensions": ["期间", "平台", "店铺"], "completeness": {"missing_rate": 0.0, "empty_columns": 0, "has_total_row": False, "notes": "固定一行透明测试值"},
            "verdict": "analyzable", "analysis_potential": ["验证来源复算、派生公式、图表与 PDF，不用于经营判断"],
        }], "acceptance_note": "无客户业务数据；R001 是固定透明测试值，只用于验证报告与 PDF 链路，不得解释为真实经营表现。",
    }
    inventory["report_count"] = 1
    write_new(run_dir / "report-inventory.json", inventory)
    validate_stage_identity(inventory, "report_inventory", version, run_id, ACCEPTANCE_SCOPE)

    clusters = {
        **native_stage_identity("report_clusters", version), "team_version": version, "run_id": run_id,
        "client_scope": ACCEPTANCE_SCOPE, "inventory_sha256": sha256(run_dir / "report-inventory.json"), "issued_at": issued_at,
        "merge_rules": {"domain_axis": "按业务域归类", "time_axis": "期间重叠率低于80%不合并", "metric_axis": "按指标交集归类", "tie_break": "原始后台导出优先", "overlap_threshold": 0.8},
        "cluster_count": 1, "clusters": [{"cluster_id": "C01", "domain": "transaction", "label": "透明验收测试数据", "members": ["R001"], "merge_basis": {"domain": "固定验收数据", "time_alignment": {"aligned": True, "action": "仅验证单次流水线", "overlap_ratio": 1.0}, "metric_overlap": ["visitors", "gmv", "paid_buyers"]}, "time_scope": {"start": None, "end": None, "granularity": "snapshot", "aligned": True}, "metrics": [{"standard_name": "visitors", "unit": "人", "primary_report_id": "R001", "corroborating_report_ids": [], "cross_check_rule": "按原 CSV 单元格复算"}, {"standard_name": "gmv", "unit": "元", "primary_report_id": "R001", "corroborating_report_ids": [], "cross_check_rule": "按原 CSV 单元格复算"}, {"standard_name": "paid_buyers", "unit": "人", "primary_report_id": "R001", "corroborating_report_ids": [], "cross_check_rule": "按原 CSV 单元格复算"}], "sufficiency": "sufficient"}], "unclustered": [],
    }
    write_new(run_dir / "report-clusters.json", clusters)
    validate_stage_identity(clusters, "report_clusters", version, run_id, ACCEPTANCE_SCOPE)

    chapters = [chapter(0, "数据概览（验收范围声明）", "data_overview", "omni-ecom-team-lead", ["report_count=1（固定透明测试源）"])]
    chapters[0]["source_report_ids"] = ["R001"]
    chapters.extend(chapter(index, title, "domain_analysis", role, metrics) for index, (role, title, metrics) in enumerate(ROLE_CHAPTERS, 1))
    chapters[1]["source_report_ids"] = ["R001"]
    chapters[1]["source_cluster_ids"] = ["C01"]
    chapters.append(chapter(5, "验收缺口与限制", "data_gap", "omni-ecom-team-lead", ["未覆盖项清单"]))
    chapter_plan = {
        **native_stage_identity("chapter_plan", version), "team_version": version, "run_id": run_id,
        "client_scope": ACCEPTANCE_SCOPE, "cluster_sha256": sha256(run_dir / "report-clusters.json"), "issued_at": issued_at,
        "chapters": chapters, "coverage_plan": {"total_reports": 1, "covered_report_ids": ["R001"], "uncovered_report_ids": [], "coverage_rate": 1.0, "data_overview_chapter_id": "CH00", "data_gap_chapter_id": "CH05"},
    }
    write_new(run_dir / "chapter-plan.json", chapter_plan)
    validate_stage_identity(chapter_plan, "chapter_plan", version, run_id, ACCEPTANCE_SCOPE)

    baseline = {
        **native_baseline_identity(version), "run_id": run_id, "client_scope": ACCEPTANCE_SCOPE, "team_version": version,
        "task_type": "single_topic", "scope": {"platform": f"{host_label}验收环境", "store": "无客户测试店铺", "period": "2026-W36", "grain": "week"},
        "metric_contract": {"visitors": {"definition": "固定测试访客数", "formula": "CSV 访客数列求和", "unit": "人", "denominator": "不适用", "forbidden_usage": ["不得解释为真实客户访客"]}, "gmv": {"definition": "固定测试支付GMV", "formula": "CSV 支付GMV列求和", "unit": "元", "denominator": "不适用", "forbidden_usage": ["不得解释为真实客户销售额"]}, "paid_buyers": {"definition": "固定测试支付买家数", "formula": "CSV 支付买家数列求和", "unit": "人", "denominator": "不适用", "forbidden_usage": ["不得解释为真实客户买家"]}}, "authority_order": ["固定验收 CSV > 运行账本 host_runtime 记录 > 宿主工具真实返回 > 成员回执文字"],
        "attribution_rules": {"refund_basis": "不适用：本次验收无退款数据", "visitor_dedupe": "CSV 有固定测试访客数，仅用于复算；没有真实客户访客明细，不能认证真实访客去重。", "paid_vs_organic": "不适用：本次验收无流量来源数据", "cross_platform": "不适用：单宿主单次运行"},
        "shared_evidence_index": [{"evidence_id": "E-acc-bootstrap", "metric": "team_bootstrap_recorded" if host=='workbuddy' else "local_host_plan_prepared_not_native_execution", "value": team_name if host=='workbuddy' else "planned_not_executed", "status": "verified"}],
        "known_conflicts": [], "issued_at": issued_at,
        "forbidden_outputs": ["经营数字", "经营结论", "利润/预算/调价/库存建议", "未授权客户名称"],
    }
    write_new(run_dir / "baseline-pack.json", baseline)
    validate_baseline_identity(baseline, version, run_id, ACCEPTANCE_SCOPE)

    source_hash = sha256(source_path)
    claims = {
        **native_claim_identity(version), "run_id": run_id, "client_scope": ACCEPTANCE_SCOPE,
        "period": "2026-W36", "scope": {"platform": f"{host_label}验收环境", "store": "无客户测试店铺"},
        "source_context_policy": "required", "claims": [
            {"claim_id": "C-visitors", "metric": "visitors", "value": 100, "unit": "人", "period": "single-run-acceptance", "status": "verified", "source_ref": {"source_id": "acceptance", "source_file": source_path.name, "sheet": "data", "range": "A2", "field": "访客数", "source_sha256": source_hash, "contexts": {"period": {"column": "D", "field": "期间"}, "platform": {"column": "E", "field": "平台"}, "store": {"column": "F", "field": "店铺"}, "unit": {"column": "G", "field": "访客单位"}}}},
            {"claim_id": "C-gmv", "metric": "gmv", "value": 1000, "unit": "元", "period": "single-run-acceptance", "status": "verified", "source_ref": {"source_id": "acceptance", "source_file": source_path.name, "sheet": "data", "range": "B2", "field": "支付GMV", "source_sha256": source_hash, "contexts": {"period": {"column": "D", "field": "期间"}, "platform": {"column": "E", "field": "平台"}, "store": {"column": "F", "field": "店铺"}, "unit": {"column": "H", "field": "金额单位"}}}},
            {"claim_id": "C-buyers", "metric": "paid_buyers", "value": 5, "unit": "人", "period": "single-run-acceptance", "status": "verified", "source_ref": {"source_id": "acceptance", "source_file": source_path.name, "sheet": "data", "range": "C2", "field": "支付买家数", "source_sha256": source_hash, "contexts": {"period": {"column": "D", "field": "期间"}, "platform": {"column": "E", "field": "平台"}, "store": {"column": "F", "field": "店铺"}, "unit": {"column": "I", "field": "买家单位"}}}},
            {"claim_id": "C-uv-value", "metric": "uv_value", "value": 10, "unit": "元/人", "period": "single-run-acceptance", "status": "derived", "source_ref": {"source_id": "acceptance", "source_file": source_path.name, "sheet": "data", "range": "B2", "field": "支付GMV", "source_sha256": source_hash, "contexts": {"period": {"column": "D", "field": "期间"}, "platform": {"column": "E", "field": "平台"}, "store": {"column": "F", "field": "店铺"}, "unit": {"column": "J", "field": "访客价值单位"}}}, "formula": {"name": "uv_value", "numerator": "gmv", "denominator": "visitors", "expression": "gmv / visitors"}, "inputs": ["C-gmv", "C-visitors"]},
            {"claim_id": "C-conversion", "metric": "conversion_rate", "value": 5, "unit": "%", "period": "single-run-acceptance", "status": "derived", "source_ref": {"source_id": "acceptance", "source_file": source_path.name, "sheet": "data", "range": "C2", "field": "支付买家数", "source_sha256": source_hash, "contexts": {"period": {"column": "D", "field": "期间"}, "platform": {"column": "E", "field": "平台"}, "store": {"column": "F", "field": "店铺"}, "unit": {"column": "K", "field": "转化率单位"}}}, "formula": {"name": "conversion_rate", "numerator": "paid_buyers", "denominator": "visitors", "expression": "(paid_buyers / visitors) * 100"}, "inputs": ["C-buyers", "C-visitors"]},
        ],
    }
    for claim_row in claims["claims"]:
        claim_row["period"] = "2026-W36"
    write_new(run_dir / "claim-ledger.json", claims)
    run_scope = {**native_run_scope_identity(version), "run_id": run_id, "client_scope": ACCEPTANCE_SCOPE, "team_version": version, "status": "scope_verified", "allowed_roots": ["."], "input_paths": [source_path.name], "files": [{"file": source_path.name, "sha256": source_hash, "size_bytes": source_path.stat().st_size}], "scanned_files": 1, "errors": []}
    write_new(run_dir / "run-scope.json", run_scope)
    lead_handoff = {**native_handoff_identity(version), "run_id": run_id, "client_scope": ACCEPTANCE_SCOPE, "agent_id": "omni-ecom-team-lead", "agent_version": version, "contribution_summary": "已准备无客户验收范围与固定口径；真实派工和回传由宿主证据核对，未执行的裁决不记为完成", "scope": baseline["scope"], "gate_status": "PASS", "status": "ready_for_review", "facts": [{"id": "F-lead-scope", "claim": "R001 acceptance-source.csv 是透明固定测试源，不是客户经营数据；仅用于验证来源复算、图表与 PDF。", "evidence_ids": ["E-lead-scope"]}], "judgments": [], "hypotheses": [], "actions": [], "risks": ["固定测试值不得解释为真实经营表现"], "missing_data": ["本轮未使用客户业务数据"], "evidence_ledger": [{"id": "E-lead-scope", "source": source_path.name, "period": "single-run-acceptance", "metric": "acceptance_scope", "value": 1, "status": "verified"}]}
    lead_handoff["evidence_ledger"][0]["period"] = "2026-W36"
    write_new(run_dir / "team-lead-handoff.json", lead_handoff)
    # These fixed probe values are already source-bound in claim-ledger.json;
    # expose them to the same KPI/chart validator used for customer exports.
    write_new(run_dir / 'acceptance-metrics.json', {
        'gate_status': 'PASS', 'source': source_path.name,
        'rows': [{'period': '2026-W36', 'inputs': {'gmv': 1000, 'visitors': 100,
                  'buyers': 5}, 'metrics': {'uv_value': 10, 'conversion_rate': .05}}]})

    runtime = Runtime(run_dir, run_id, ACCEPTANCE_SCOPE)
    try:
        runtime.init(version, "single_topic")
    finally:
        runtime.close()
    cards = analysis_cards(SimpleNamespace(run_dir=str(run_dir), plugin_dir=str(plugin_dir), baseline=None, chapter_plan=None, inventory=None, attempt="a1", host=host, output=None, pretty=False))
    q = lambda value: f'"{value}"'
    scripts = plugin_dir / "scripts"
    sealed_args = " ".join(f'--member-handoff {q(run_dir / "sealed" / (role + "-a1.json"))}' for role, _, _ in ROLE_CHAPTERS)
    return_dir = run_dir / "agent-returns"
    wait_return_args = " ".join(
        f'--return-file {role}={role}/a1.return.json' for role, _, _ in ROLE_CHAPTERS
    )
    wait_command = (
        f'python -B {q(scripts / "wait_for_agent_returns.py")} '
        f'--return-dir {q(return_dir)} --run-id {run_id} '
        '--expected data-analyst,platform-ops,content-live-growth,ad-profit-optimizer '
        f'--contract member {wait_return_args} --timeout 600'
    )
    after_binding_commands = [
        f'python -B {q(scripts / "analysis_depth_guard.py")} ' + " ".join(f'--handoff {role}={q(run_dir / "sealed" / (role + "-a1.json"))}' for role, _, _ in ROLE_CHAPTERS) + f' --baseline {q(run_dir / "baseline-pack.json")} --min-level L2 --expect-agents data-analyst,platform-ops,content-live-growth,ad-profit-optimizer --output {q(run_dir / "depth-guard.json")} --pretty',
        f'python -B {q(scripts / "conflict_scan.py")} ' + " ".join(f'--handoff {role}={q(run_dir / "sealed" / (role + "-a1.json"))}' for role, _, _ in ROLE_CHAPTERS) + f' --baseline {q(run_dir / "baseline-pack.json")} --run-id {run_id} --output {q(run_dir / "conflict-scan.json")} --pretty',
        f'python -B {q(scripts / "coverage_guard.py")} --inventory {q(run_dir / "report-inventory.json")} --chapter-plan {q(run_dir / "chapter-plan.json")} --output {q(run_dir / "coverage-gate.json")}',
        f'python -B {q(scripts / "claim_guard.py")} validate --claims {q(run_dir / "claim-ledger.json")} --require-context --output {q(run_dir / "claim-receipt.json")}',
        f'python -B {q(scripts / "build_report_package.py")} --handoff {q(run_dir / "team-lead-handoff.json")} --client-scope {ACCEPTANCE_SCOPE} --collaboration-mode comprehensive --task-type single_topic {sealed_args} --report-revision R1 --report-inventory {q(run_dir / "report-inventory.json")} --report-clusters {q(run_dir / "report-clusters.json")} --chapter-plan {q(run_dir / "chapter-plan.json")} --coverage-gate {q(run_dir / "coverage-gate.json")} --claim-ledger {q(run_dir / "claim-ledger.json")} --metrics {q(run_dir / "acceptance-metrics.json")} --output-dir {q(run_dir)}',
    ]
    result = {
        "status": "acceptance_scaffold_ready", "run_id": run_id, "host": host, "team_name": team_name or None, "run_dir": str(run_dir),
        "launch_manifest": cards["manifest_path"], "claim_ledger": str(run_dir / "claim-ledger.json"),
        "lead_handoff": str(run_dir / "team-lead-handoff.json"), "launch_prompt_max_chars": cards["launch_prompt_max_chars"],
        "wait_command": wait_command,
        "analysis_binding_command_template": f'python -B {q(scripts / "bind_workbuddy_analysis_returns.py")} --run-dir {q(run_dir)} --host {host} --task data-analyst=<真实task_id> --task platform-ops=<真实task_id> --task content-live-growth=<真实task_id> --task ad-profit-optimizer=<真实task_id>',
        "after_binding_commands": after_binding_commands,
        "review_prepare_command": f'python -B {q(scripts / "prepare_workbuddy_acceptance_review.py")} --run-dir {q(run_dir)} --plugin-dir {q(plugin_dir)} --host {host}',
    }
    (run_dir / "acceptance-scaffold-receipt.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lead-card", required=True)
    parser.add_argument("--plugin-dir", required=True)
    args = parser.parse_args()
    result = prepare_scaffold(Path(args.lead_card), Path(args.plugin_dir))
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
