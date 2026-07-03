"""Cross-signal root cause synthesis for Huawei Cloud CCE incidents."""

from __future__ import annotations

import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

from . import aom, change_impact_analysis, dependency_impact_analysis, workload_rollout_diagnosis


def _to_bool(value: Any, default: bool = True) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() not in {"0", "false", "no", "off"}


def _to_int(value: Any, default: int) -> int:
    try:
        return int(value) if value not in (None, "") else default
    except (TypeError, ValueError):
        return default


def _confidence_value(value: Any, default: float = 0.5) -> float:
    if isinstance(value, (int, float)):
        return max(0.0, min(1.0, float(value)))
    text = str(value or "").lower()
    mapping = {"critical": 0.92, "high": 0.86, "medium": 0.62, "low": 0.35}
    return mapping.get(text, default)


def _md_cell(value: Any, max_len: int = 180) -> str:
    if value is None or value == "":
        return "-"
    text = str(value).replace("\n", " ").replace("|", "\\|").strip()
    if len(text) > max_len:
        return text[: max_len - 3] + "..."
    return text


def _safe_capture(label: str, collector: Callable[[], Dict[str, Any]]) -> Dict[str, Any]:
    try:
        result = collector()
        if isinstance(result, dict):
            return result
        return {"success": True, "result": result}
    except Exception as exc:  # pragma: no cover - defensive cloud/API boundary
        return {"success": False, "stage": label, "error": str(exc), "error_type": type(exc).__name__}


def _workload_name(params: Dict[str, str]) -> Optional[str]:
    return params.get("workload_name") or params.get("target_name") or params.get("app_name") or params.get("name")


def _cause_key(cause: Dict[str, Any]) -> str:
    return str(cause.get("type") or cause.get("title") or "Unknown")


def _add_or_merge(causes: List[Dict[str, Any]], new_cause: Dict[str, Any]) -> None:
    key = _cause_key(new_cause)
    for cause in causes:
        if _cause_key(cause) != key:
            continue
        cause["confidence"] = max(_confidence_value(cause.get("confidence")), _confidence_value(new_cause.get("confidence")))
        cause.setdefault("evidence", []).extend(new_cause.get("evidence") or [])
        cause["evidence"] = cause["evidence"][:12]
        for recommendation in new_cause.get("recommendation") or []:
            if recommendation not in cause.setdefault("recommendation", []):
                cause["recommendation"].append(recommendation)
        return
    causes.append(new_cause)


def _causes_from_rollout(rollout: Dict[str, Any]) -> List[Dict[str, Any]]:
    if not rollout.get("success"):
        return []
    result = []
    target = rollout.get("target") or {}
    target_key = f"{target.get('namespace')}/{target.get('name')}"
    for cause in rollout.get("top_causes") or []:
        cause_type = cause.get("type")
        evidence = list(cause.get("evidence") or [])
        evidence.append({"source": "workload_rollout", "summary": rollout.get("summary", {}).get("headline"), "target": target_key})
        confidence = _confidence_value(cause.get("confidence"), 0.72)
        if cause_type == "ContainerCommandNotFound":
            confidence = max(confidence, 0.94)
        result.append({
            "type": cause_type,
            "title": cause.get("title") or "工作负载发布异常",
            "domain": "workload",
            "confidence": confidence,
            "evidence": evidence[:10],
            "counter_evidence": [],
            "recommendation": cause.get("recommendation") or [],
            "remediation_hint": _remediation_hint_for_rollout(cause_type),
        })
    return result


def _remediation_hint_for_rollout(cause_type: Optional[str]) -> Dict[str, Any]:
    if cause_type in {"ContainerCommandNotFound", "CrashLoopOrAppExit", "ProbeFailure", "ImagePullBlocked"}:
        return {
            "skill": "auto-remediation-runner",
            "action": "huawei_auto_remediation_run",
            "strategy": "rollback_previous_revision",
            "requires_confirmation": True,
        }
    return {"skill": "auto-remediation-runner", "requires_confirmation": True}


def _causes_from_change_impact(change_impact: Dict[str, Any]) -> List[Dict[str, Any]]:
    if not change_impact.get("success"):
        return []
    result = []
    for change in change_impact.get("top_changes") or []:
        confidence = _confidence_value(change.get("confidence"), 0.55)
        score = _to_int(change.get("risk_score"), 0)
        if score >= 85:
            confidence = max(confidence, 0.82)
        result.append({
            "type": f"Change:{change.get('category')}",
            "title": change.get("title") or "近期变更可能触发故障",
            "domain": "change",
            "confidence": confidence,
            "evidence": change.get("evidence") or [],
            "counter_evidence": [],
            "recommendation": ["复核该变更的 before/after 差异；如需回滚，先由 auto-remediation-runner 生成预览。"],
            "remediation_hint": {"skill": "auto-remediation-runner", "requires_confirmation": True},
        })
    return result


def _causes_from_dependency(dependency: Dict[str, Any]) -> List[Dict[str, Any]]:
    if not dependency.get("success"):
        return []
    summary = dependency.get("summary") or {}
    health = summary.get("pod_health") or {}
    if summary.get("risk_level") not in {"High", "Medium"}:
        return []
    return [{
        "type": "DependencyBlastRadius",
        "title": "目标服务不可用会沿 Service/Ingress 传播",
        "domain": "dependency",
        "confidence": 0.72 if summary.get("risk_level") == "High" else 0.55,
        "evidence": [
            {
                "source": "dependency_topology",
                "summary": summary.get("risk_reason"),
                "pod_health": health,
                "paths": dependency.get("propagation_paths", [])[:3],
            }
        ],
        "counter_evidence": ["静态 Kubernetes 拓扑不能证明真实调用链，需要 APM/访问日志补强下游消费者证据。"],
        "recommendation": ["先恢复目标工作负载，再复查入口、Service endpoint 和上游访问错误率。"],
        "remediation_hint": {"skill": "auto-remediation-runner", "requires_confirmation": True},
    }]


def _causes_from_alarms(alarms: Dict[str, Any]) -> List[Dict[str, Any]]:
    if not alarms.get("success"):
        return []
    alarm_items = []
    for key in ("sudden_alarms", "focus_alarms", "alarms", "items"):
        value = alarms.get(key)
        if isinstance(value, list):
            alarm_items.extend(value)
    if not alarm_items:
        return []
    return [{
        "type": "AlarmCorrelation",
        "title": "AOM 告警与故障窗口存在关联信号",
        "domain": "alarm",
        "confidence": 0.5,
        "evidence": [{"source": "aom", "summary": f"关联告警 {len(alarm_items)} 条", "sample": alarm_items[:5]}],
        "counter_evidence": ["告警本身通常是症状，需要与工作负载、事件和变更证据交叉验证。"],
        "recommendation": ["按突发告警时间回看对应 Pod/Node/Service 指标。"],
        "remediation_hint": {"skill": "root-cause-analyzer"},
    }]


def _rank_causes(causes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    def score(cause: Dict[str, Any]) -> float:
        confidence = _confidence_value(cause.get("confidence"))
        evidence_bonus = min(len(cause.get("evidence") or []) * 0.025, 0.08)
        domain_bonus = 0.05 if cause.get("domain") == "workload" else 0
        return confidence + evidence_bonus + domain_bonus

    ranked = sorted(causes, key=score, reverse=True)
    for index, cause in enumerate(ranked, start=1):
        cause["rank"] = index
        cause["confidence"] = round(_confidence_value(cause.get("confidence")), 2)
    return ranked


def _capture_status_rows(captures: Dict[str, Dict[str, Any]]) -> List[Tuple[str, str, str]]:
    labels = {
        "rollout": "Workload 发布诊断",
        "dependency": "依赖影响面分析",
        "change": "变更影响分析",
        "alarms": "AOM 告警关联",
    }
    rows = []
    for key, label in labels.items():
        item = captures.get(key)
        if not item:
            rows.append((label, "跳过", "未启用或缺少必要范围"))
            continue
        rows.append((label, "成功" if item.get("success") else "失败", item.get("error") or item.get("summary", {}).get("headline") or "已采集"))
    return rows


def _timeline_rows(captures: Dict[str, Dict[str, Any]]) -> str:
    rows = ["| 来源 | 时间/阶段 | 事件 |", "| --- | --- | --- |"]
    rollout = captures.get("rollout") or {}
    if rollout.get("success"):
        for event in (rollout.get("events") or {}).get("timeline") or []:
            rows.append(f"| K8s Event | {_md_cell(event.get('event_time') or event.get('last_timestamp'))} | {_md_cell(event.get('reason'))}: {_md_cell(event.get('message'), 260)} |")
    change = captures.get("change") or {}
    if change.get("success"):
        for item in change.get("top_changes") or []:
            rows.append(f"| Audit Change | {_md_cell(item.get('time'))} | {_md_cell(item.get('verb'))} {_md_cell(item.get('object_key'))}: {_md_cell(item.get('title'))} |")
    if len(rows) == 2:
        rows.append("| - | - | 未收集到可展示时间线 |")
    return "\n".join(rows)


def build_markdown_report(
    trace_id: str,
    params: Dict[str, str],
    captures: Dict[str, Dict[str, Any]],
    causes: List[Dict[str, Any]],
) -> str:
    target = _workload_name(params) or "未指定"
    top = causes[0] if causes else None
    conclusion = (
        f"最高置信根因是 `{top.get('title')}`，类型 `{top.get('type')}`，置信度 `{top.get('confidence')}`。"
        if top
        else "当前证据不足以给出明确根因，需要补齐事件、日志、审计或指标数据。"
    )
    status_rows = [
        "| 数据源 | 状态 | 说明 |",
        "| --- | --- | --- |",
        *[f"| {_md_cell(source)} | {_md_cell(status)} | {_md_cell(note, 260)} |" for source, status, note in _capture_status_rows(captures)],
    ]
    cause_rows = ["| 排名 | 根因候选 | 域 | 置信度 | 关键证据 |", "| --- | --- | --- | --- | --- |"]
    for cause in causes[:3]:
        evidence = cause.get("evidence") or []
        cause_rows.append(
            f"| {cause.get('rank')} | {_md_cell(cause.get('title'))} | {_md_cell(cause.get('domain'))} | "
            f"{_md_cell(cause.get('confidence'))} | {_md_cell(evidence[0] if evidence else '-', 300)} |"
        )
    if len(cause_rows) == 2:
        cause_rows.append("| - | - | - | - | - |")

    evidence_lines = []
    for cause in causes[:3]:
        evidence_lines.append(f"### Top {cause.get('rank')}: {cause.get('title')}")
        for item in cause.get("evidence") or []:
            evidence_lines.append(f"- `{item.get('source', cause.get('domain')) if isinstance(item, dict) else cause.get('domain')}`: {_md_cell(item, 360)}")
        for item in cause.get("counter_evidence") or []:
            evidence_lines.append(f"- 反证/限制: {_md_cell(item, 260)}")
    if not evidence_lines:
        evidence_lines.append("证据不足：没有形成可排序根因候选。")

    remediation_lines = []
    for cause in causes[:3]:
        hint = cause.get("remediation_hint") or {}
        recommendation = "；".join(cause.get("recommendation") or [])
        remediation_lines.append(
            f"- **{cause.get('title')}**: {recommendation or '先补充验证。'} "
            f"恢复交接: `{hint.get('skill', 'auto-remediation-runner')}`"
            + (f" / `{hint.get('action')}`" if hint.get("action") else "")
        )
    if not remediation_lines:
        remediation_lines.append("- 暂不建议执行恢复动作；先补齐缺失证据。")

    return "\n".join(
        [
            "# CCE 综合根因分析报告",
            "",
            "## 1. 分析摘要",
            "",
            f"- Analysis-Trace-ID: `{trace_id}`",
            f"- 集群: `{params.get('cluster_id')}`",
            f"- 区域: `{params.get('region')}`",
            f"- 命名空间: `{params.get('namespace') or '全集群'}`",
            f"- 目标对象: `{target}`",
            f"- 初步结论: {conclusion}",
            "",
            "## 2. 排查过程",
            "",
            "1. 明确故障对象和时间窗口，建立跨信号 Trace ID。",
            "2. 汇聚工作负载发布状态、Pod/事件/日志、依赖拓扑、近期变更和 AOM 告警。",
            "3. 将每类信号转换为根因候选，记录支持证据、反证和证据限制。",
            "4. 按证据强度、时间吻合度、影响面和可恢复性排序，输出 Top3 根因。",
            "5. 恢复动作只给交接建议，实际执行由 auto-remediation-runner 预览并确认。",
            "",
            "## 3. 数据源与采集状态",
            "",
            "\n".join(status_rows),
            "",
            "## 4. 时间线",
            "",
            _timeline_rows(captures),
            "",
            "## 5. Top3 根因结论",
            "",
            "\n".join(cause_rows),
            "",
            "## 6. 证据链与反证",
            "",
            "\n".join(evidence_lines),
            "",
            "## 7. 影响面",
            "",
            (captures.get("dependency") or {}).get("summary", {}).get("risk_reason", "影响面需要结合 dependency-impact-analyzer 输出继续确认。"),
            "",
            "## 8. 恢复建议与交接",
            "",
            "\n".join(remediation_lines),
            "",
            "## 9. 能力复用与缺口",
            "",
            "- 已复用 workload rollout、dependency impact、change impact、AOM alarm 等组合能力。",
            "- 对本次启动命令类故障，工作负载发布诊断可直接识别 command/args 与容器入口异常。",
            "- 建议继续补充 EndpointSlice、APM 调用边、CTS 云审计和 before/after YAML diff，提升影响面和变更归因置信度。",
            "",
        ]
    )


def analyze_root_cause(params: Dict[str, str]) -> Dict[str, Any]:
    missing = [key for key in ("region", "cluster_id") if not params.get(key)]
    if missing:
        return {"success": False, "error": f"{', '.join(missing)} is required"}

    trace_id = params.get("analysis_trace_id") or f"RCA-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:8]}"
    target = _workload_name(params)
    namespace = params.get("namespace")
    captures: Dict[str, Dict[str, Any]] = {}

    if target and namespace and _to_bool(params.get("include_rollout"), True):
        kind = params.get("kind") or params.get("workload_type") or "deployment"
        captures["rollout"] = _safe_capture(
            "rollout",
            lambda: workload_rollout_diagnosis.workload_rollout_diagnose(
                region=params["region"],
                cluster_id=params["cluster_id"],
                namespace=namespace,
                kind=kind,
                name=target,
                include_pod_diagnosis=True,
                include_logs=_to_bool(params.get("include_logs"), True),
                include_metrics=_to_bool(params.get("include_metrics"), False),
                tail_lines=_to_int(params.get("tail_lines"), 80),
                hours=_to_int(params.get("hours"), 1),
                max_pods=_to_int(params.get("max_pods"), 20),
                event_limit=_to_int(params.get("event_limit"), 500),
                label_selector=params.get("label_selector"),
                ak=params.get("ak"),
                sk=params.get("sk"),
                project_id=params.get("project_id"),
            ),
        )

    if _to_bool(params.get("include_dependency"), True):
        dep_params = dict(params)
        dep_params["analysis_trace_id"] = trace_id
        captures["dependency"] = _safe_capture("dependency", lambda: dependency_impact_analysis.analyze_dependency_impact(dep_params))

    if _to_bool(params.get("include_change"), True):
        change_params = dict(params)
        change_params["analysis_trace_id"] = trace_id
        if target and not change_params.get("target_name"):
            change_params["target_name"] = target
        captures["change"] = _safe_capture("change", lambda: change_impact_analysis.analyze_change_impact(change_params))

    if _to_bool(params.get("include_alarms"), True):
        captures["alarms"] = _safe_capture(
            "alarms",
            lambda: aom.analyze_aom_alarms(
                region=params["region"],
                ak=params.get("ak"),
                sk=params.get("sk"),
                project_id=params.get("project_id"),
                cluster_id=params.get("cluster_id"),
                cluster_name=params.get("cluster_name"),
                hours=_to_int(params.get("hours"), 1),
            ),
        )

    causes: List[Dict[str, Any]] = []
    for cause in _causes_from_rollout(captures.get("rollout") or {}):
        _add_or_merge(causes, cause)
    for cause in _causes_from_dependency(captures.get("dependency") or {}):
        _add_or_merge(causes, cause)
    for cause in _causes_from_change_impact(captures.get("change") or {}):
        _add_or_merge(causes, cause)
    for cause in _causes_from_alarms(captures.get("alarms") or {}):
        _add_or_merge(causes, cause)

    ranked = _rank_causes(causes)
    report_markdown = build_markdown_report(trace_id, params, captures, ranked)
    output_file = params.get("output_file")
    if output_file:
        Path(output_file).write_text(report_markdown, encoding="utf-8")

    return {
        "success": True,
        "analysis_trace_id": trace_id,
        "scope": {
            "region": params.get("region"),
            "cluster_id": params.get("cluster_id"),
            "namespace": namespace,
            "target_name": target,
        },
        "summary": {
            "top_cause": ranked[0] if ranked else None,
            "cause_count": len(ranked),
            "data_sources": {source: bool(result.get("success")) for source, result in captures.items()},
        },
        "top_causes": ranked[:3],
        "causes": ranked,
        "report_markdown": report_markdown,
        "report_file": output_file,
        "capture_metadata": {
            source: {
                "success": result.get("success"),
                "error": result.get("error"),
                "summary": result.get("summary"),
            }
            for source, result in captures.items()
        },
    }


def analyze_root_cause_action(params: Dict[str, str]) -> Dict[str, Any]:
    return analyze_root_cause(params)
