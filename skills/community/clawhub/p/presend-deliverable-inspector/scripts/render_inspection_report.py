#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


VERDICT_LABELS = {
    "can_send": "可以发送",
    "send_after_quick_fixes": "快改后发送",
    "hold_before_send": "暂缓发送",
    "rework_before_send": "重做后再发",
}

TIMEBOX_LABELS = ["0-10 分钟", "10-20 分钟", "20-30 分钟", "30-60 分钟"]
MISSING_CONTEXT_LABELS = {
    "recipient": "收件人",
    "target_action": "目标动作",
    "deadline": "截止时间",
    "material_stage": "材料阶段",
}


def missing_context_text(fields: list[str]) -> str:
    return "、".join(MISSING_CONTEXT_LABELS.get(field, field) for field in fields)


def context_line(data: dict) -> str:
    context = data["context_basis"]
    recipient = context.get("recipient") or data.get("audience") or "未确认"
    target = context.get("target_action") or "未确认"
    deadline = context.get("deadline") or data.get("deadline") or "未确认"
    missing = context.get("missing_context") or []
    if missing:
        return f"我先按保守场景判：缺 {missing_context_text(missing)}；当前按发给 {recipient}、目标 {target}、时间 {deadline} 处理。"
    return f"我按这个上下文判：发给 {recipient}，目标 {target}，时间 {deadline}。"


def weighting_line(data: dict) -> str | None:
    weights = data["context_basis"].get("risk_weighting") or []
    if not weights:
        return None
    labels = {
        "decision_gap": "下一步",
        "claim_evidence_gap": "证据强度",
        "privacy_or_commitment_risk": "承诺/隐私",
        "version_residue": "版本残留",
        "number_conflict": "数字一致",
        "formula_or_summary_mismatch": "汇总公式",
        "repair_priority": "修复优先级",
        "general_presend_risk": "通用出街风险",
    }
    parts = [labels.get(item["risk_area"], item["risk_area"]) for item in weights[:3]]
    return f"权重依据：优先看 {'、'.join(parts)}。"


def render_must_fix(items: list[dict]) -> list[str]:
    if not items:
        return ["- 暂未发现阻断发送的硬错误；仍需人工复查未核验项。"]
    lines = []
    for idx, item in enumerate(items, start=1):
        severity = item.get("severity", "must_fix")
        prefix = "阻断" if severity == "blocker" else "必改"
        error_label = item["error_type"]
        if item.get("error_family"):
            error_label = f"{item['error_family']}/{error_label}"
        context_reason = item.get("context_reason")
        reason_part = f"；上下文理由：{context_reason}" if context_reason else ""
        lines.append(
            f"{idx}. [{prefix}] {item['location']} {error_label}：{item['risk']}{reason_part}；发现依据：{item['evidence']} -> {item['fix']}"
        )
    return lines


def overflow_line(data: dict) -> str | None:
    overflow = data.get("finding_overflow") or {}
    omitted = overflow.get("omitted_total", 0)
    if not omitted:
        return None
    additional = data.get("additional_findings") or []
    details = []
    for item in additional:
        error_label = item.get("error_type", "unknown")
        if item.get("error_family"):
            error_label = f"{item['error_family']}/{error_label}"
        details.append(f"{item.get('location', '位置未标注')} [{error_label}; {item.get('severity', 'must_fix')}]")
    locations = "、".join(details or overflow.get("omitted_locations") or [])
    return (
        f"- 共发现 {overflow.get('detected_total', omitted)} 条，本屏展示 "
        f"{overflow.get('displayed_total', len(data.get('must_fix', [])))} 条；另有 {omitted} 条，"
        f"其中阻断 {overflow.get('omitted_blocker_count', 0)} 条。位置：{locations}。"
        "完整明细见 additional_findings。"
    )


def render_list(items: list[str], fallback: str) -> list[str]:
    if not items:
        return [f"- {fallback}"]
    return [f"- {item}" for item in items]


def render_route(items: list[dict]) -> list[str]:
    if not items:
        return ["1. [0-10 分钟] 做最终导出和发送前复查。"]
    lines = []
    for idx, item in enumerate(items, start=1):
        label = item.get("timebox") or TIMEBOX_LABELS[min(idx - 1, len(TIMEBOX_LABELS) - 1)]
        lines.append(f"{idx}. [{label}] {item['action']}")
    return lines


def render(data: dict) -> str:
    verdict = VERDICT_LABELS.get(data["verdict"], data["verdict"])
    weight = weighting_line(data)
    parts = [
        f"出街判定：{verdict}",
        context_line(data),
    ]
    if weight:
        parts.append(weight)
    overflow = overflow_line(data)
    parts.extend([
        "",
        "必须改：",
        *render_must_fix(data.get("must_fix", [])),
    ])
    if overflow:
        parts.append(overflow)
    parts.extend([
        "",
        "可以保留：",
        *render_list(data.get("can_keep", []), "结构可保留，先集中修硬风险。"),
        "",
        "30 分钟修复路线：",
        *render_route(data.get("repair_route", [])),
        "",
        "未核验项：",
        *render_list(data.get("unverified_items", []), "没有额外未核验项。"),
        "",
        "继续：按30分钟路线改 / 只看必须改 / 生成发送话术",
    ])
    return "\n".join(parts).rstrip() + "\n"


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: render_inspection_report.py <inspection.json>")
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print(render(data), end="")


if __name__ == "__main__":
    main()
