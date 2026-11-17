#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from extract_deliverable_text import extract  # noqa: E402


VERDICT_ORDER = {
    "can_send": 0,
    "send_after_quick_fixes": 1,
    "hold_before_send": 2,
    "rework_before_send": 3,
}

ERROR_FAMILIES = {
    "source_missing": "data_evidence",
    "source_stale_or_misaligned": "data_evidence",
    "number_conflict": "data_consistency",
    "formula_or_summary_mismatch": "data_consistency",
    "claim_evidence_gap": "reasoning_gap",
    "decision_gap": "audience_action",
    "format_rendering_error": "format_rendering",
    "privacy_or_commitment_risk": "privacy_commitment",
    "version_residue": "format_rendering",
    "audience_mismatch": "audience_action",
}

MISSING_CONTEXT_LABELS = {
    "recipient": "收件人",
    "target_action": "目标动作",
    "deadline": "截止时间",
    "material_stage": "材料阶段",
}

DEFAULT_CONTEXT_REASONS = {
    "source_missing": "关键数据进入出街材料时，缺来源、周期或口径会削弱可追问性。",
    "source_stale_or_misaligned": "来源范围、时间或样本和当前主张不匹配，会让结论失去托底。",
    "number_conflict": "同一指标多版本会直接影响收件人对口径和可信度的判断。",
    "formula_or_summary_mismatch": "汇总、公式或透视表异常会让上层结论失去数据基础。",
    "claim_evidence_gap": "标题或结论强于证据时，收件人会追问样本、因果链和边界。",
    "decision_gap": "材料没有把目标动作讲清，收件人看完也难以批准、确认或执行。",
    "format_rendering_error": "导出或呈现问题会阻断收件人理解正文、图表或来源。",
    "privacy_or_commitment_risk": "隐私、授权或承诺措辞会带来外发、法务和履约风险。",
    "version_residue": "旧版痕迹、隐藏内容或内部话术会暴露材料未清理干净。",
    "audience_mismatch": "语气、首页或结尾动作和收件人不匹配，会让材料目标跑偏。",
}

AUDIENCE_CONTEXT_REASONS = {
    "boss": {
        "decision_gap": "老板场景优先看能否推动批示、选方案或定下一步。",
        "claim_evidence_gap": "老板会直接追问结论凭什么成立，证据强度优先级上调。",
        "source_missing": "老板汇报里的关键数字要能被追溯，否则会卡住决策。",
        "number_conflict": "老板材料里同一数字多版本会破坏汇报可信度。",
    },
    "manager": {
        "decision_gap": "管理者场景优先看能否推动批示、选方案或定下一步。",
        "claim_evidence_gap": "管理者会追问结论凭什么成立，证据强度优先级上调。",
        "source_missing": "管理层材料里的关键数字要能被追溯，否则会卡住决策。",
        "number_conflict": "管理层材料里同一数字多版本会破坏汇报可信度。",
    },
    "leadership": {
        "decision_gap": "高层场景优先看能否推动批示、选方案或定下一步。",
        "claim_evidence_gap": "高层会追问结论凭什么成立，证据强度优先级上调。",
        "source_missing": "高层材料里的关键数字要能被追溯，否则会卡住决策。",
        "number_conflict": "高层材料里同一数字多版本会破坏汇报可信度。",
    },
    "executive": {
        "decision_gap": "高层场景优先看能否推动批示、选方案或定下一步。",
        "claim_evidence_gap": "高层会追问结论凭什么成立，证据强度优先级上调。",
        "source_missing": "高层材料里的关键数字要能被追溯，否则会卡住决策。",
        "number_conflict": "高层材料里同一数字多版本会破坏汇报可信度。",
    },
    "client": {
        "privacy_or_commitment_risk": "客户外发场景优先看授权、保密、价格和交付承诺。",
        "version_residue": "客户外发场景下，隐藏内容、批注和旧版话术会直接变成外泄风险。",
        "audience_mismatch": "客户版需要客户可见目标和下一步，内部讨论语气优先修。",
        "number_conflict": "客户材料里数字冲突会引发报价、范围或交付理解偏差。",
    },
    "customer": {
        "privacy_or_commitment_risk": "客户外发场景优先看授权、保密、价格和交付承诺。",
        "version_residue": "客户外发场景下，隐藏内容、批注和旧版话术会直接变成外泄风险。",
        "audience_mismatch": "客户版需要客户可见目标和下一步，内部讨论语气优先修。",
        "number_conflict": "客户材料里数字冲突会引发报价、范围或交付理解偏差。",
    },
    "external": {
        "privacy_or_commitment_risk": "对外场景优先看授权、保密、价格和交付承诺。",
        "version_residue": "对外场景下，隐藏内容、批注和旧版话术会直接变成外泄风险。",
        "audience_mismatch": "对外材料需要公开可见目标和下一步，内部讨论语气优先修。",
        "source_missing": "公开材料里的事实和数字需要可追溯来源。",
    },
    "board": {
        "formula_or_summary_mismatch": "董事会包优先看汇总、公式、透视表和明细能否对账。",
        "number_conflict": "董事会包里数字口径冲突会破坏审议基础。",
        "source_missing": "董事会包关键判断需要来源、周期和口径留痕。",
        "claim_evidence_gap": "董事会包结论不能越过已核验数据和审计线索。",
    },
    "directors": {
        "formula_or_summary_mismatch": "董事会包优先看汇总、公式、透视表和明细能否对账。",
        "number_conflict": "董事会包里数字口径冲突会破坏审议基础。",
        "source_missing": "董事会包关键判断需要来源、周期和口径留痕。",
        "claim_evidence_gap": "董事会包结论不能越过已核验数据和审计线索。",
    },
}


def missing_context_text(fields: list[str]) -> str:
    return "、".join(MISSING_CONTEXT_LABELS.get(field, field) for field in fields)


def is_known(value: str) -> bool:
    return bool(value and value != "unknown")


def has_issue(issues: list[dict], location: str, error_type: str) -> bool:
    return any(item["location"] == location and item["error_type"] == error_type for item in issues)


SOURCE_MARKERS = (
    "source:",
    "source：",
    "来源",
    "according to",
    "data from",
    "finance model",
    "research report",
    "survey",
    "财报",
    "年报",
)
NEGATIVE_SOURCE_MARKERS = (
    "no source",
    "source needed",
    "without source",
    "missing source",
    "缺来源",
    "待补来源",
)
DATA_BEARING_TERMS = (
    "market size",
    "addressable market",
    "market share",
    "revenue forecast",
    "sales forecast",
    "budget forecast",
    "市场规模",
    "可服务市场",
    "市场份额",
    "收入预测",
    "销售预测",
    "预算预测",
)
STRONG_CLAIM_MARKERS = (
    "proves",
    "fully proven",
    "guarantees",
    "will lead",
    "inevitable",
    "definitive",
    "fully validated",
    "verified scalable growth",
    "证明",
    "必然",
    "全面领先",
    "确定会",
    "已验证",
)
CLAIM_SUPPORT_MARKERS = (
    *SOURCE_MARKERS,
    "sample size",
    "confidence interval",
    "benchmark",
    "control group",
    "p-value",
    "样本量",
    "置信区间",
    "对照组",
    "基准",
)
DECISION_ACTION_MARKERS = (
    "please approve",
    "decision needed",
    "choose option",
    "please confirm",
    "next step",
    "owner:",
    "deadline:",
    "请批准",
    "需要决策",
    "请选择",
    "请确认",
    "下一步",
    "负责人",
    "截止时间",
)
NEGATIVE_DECISION_MARKERS = ("no decision request", "decision not requested", "缺少决策", "没有下一步")


def has_usable_source(text: str) -> bool:
    for line in text.lower().splitlines():
        if any(marker in line for marker in SOURCE_MARKERS) and not any(
            marker in line for marker in NEGATIVE_SOURCE_MARKERS
        ):
            return True
    return False


def contains_data_bearing_claim(text: str) -> bool:
    lower = text.lower()
    has_term = any(term in lower for term in DATA_BEARING_TERMS)
    has_number = bool(
        re.search(r"(?:[$¥￥]\s*)?\d+(?:\.\d+)?\s*(?:%|b|bn|billion|m|mn|million|k|亿|万)\b", lower)
    )
    return has_term and has_number


def strong_claim_without_support(text: str) -> bool:
    lower = text.lower()
    return any(marker in lower for marker in STRONG_CLAIM_MARKERS) and not any(
        marker in lower for marker in CLAIM_SUPPORT_MARKERS
    )


def has_decision_action(text: str) -> bool:
    lower = text.lower()
    if any(marker in lower for marker in NEGATIVE_DECISION_MARKERS):
        return False
    return any(marker in lower for marker in DECISION_ACTION_MARKERS)


def normalize_metric_value(value: str, unit: str) -> int:
    multiplier = {
        "b": 1_000_000_000,
        "bn": 1_000_000_000,
        "billion": 1_000_000_000,
        "m": 1_000_000,
        "mn": 1_000_000,
        "million": 1_000_000,
        "k": 1_000,
        "亿": 100_000_000,
        "万": 10_000,
    }[unit.lower()]
    return int(float(value.replace(",", "")) * multiplier)


def first_unique_match(text: str, patterns: list[tuple[str, str]]) -> str:
    matches = {value for pattern, value in patterns if re.search(pattern, text, re.IGNORECASE)}
    return next(iter(matches)) if len(matches) == 1 else ""


def metric_identity(text: str, full_text: str) -> dict[str, str]:
    region_patterns = [
        (r"\bglobal\b|\bworldwide\b|全球", "global"),
        (r"\bnorth america\b|北美", "north_america"),
        (r"\beast china\b|华东", "east_china"),
        (r"\bgreater china\b|大中华", "greater_china"),
        (r"\bchina\b|中国", "china"),
        (r"\bapac\b|亚太", "apac"),
        (r"\bemea\b", "emea"),
    ]
    currency_patterns = [
        (r"\busd\b|\$", "USD"),
        (r"\brmb\b|\bcny\b|[¥￥]", "CNY"),
        (r"\beur\b|€", "EUR"),
    ]
    scope_patterns = [
        (r"\bnet revenue\b|\bnet sales\b|净收入|净销售额|未税|不含税", "net"),
        (r"\bgross revenue\b|\bgross sales\b|总收入|含税", "gross"),
        (r"\bforecast\b|预测", "forecast"),
        (r"\bactual\b|实际", "actual"),
        (r"\baddressable market\b|\btam\b|可服务市场", "addressable_market"),
        (r"\bmarket size\b|市场规模", "market_size"),
        (r"累计", "cumulative"),
        (r"单月|当月", "monthly"),
    ]

    def value(patterns: list[tuple[str, str]]) -> str:
        local = first_unique_match(text, patterns)
        return local or first_unique_match(full_text, patterns)

    period_pattern = re.compile(
        r"\bfy\s*20\d{2}\b|\b20\d{2}\s*q[1-4]\b|\bq[1-4]\s*20\d{2}\b|20\d{2}年(?:q[1-4]|第?[一二三四1-4]季度|上半年|下半年|全年)?|\bq[1-4]\b",
        re.IGNORECASE,
    )

    def period_value(source: str) -> str:
        values = {match.group(0).lower().replace(" ", "") for match in period_pattern.finditer(source)}
        return next(iter(values)) if len(values) == 1 else ""

    period = period_value(text) or period_value(full_text)

    return {
        "period": period,
        "region": value(region_patterns),
        "currency": value(currency_patterns),
        "unit": "currency_amount",
        "scope": value(scope_patterns),
    }


def extract_metric_mentions(text: str) -> list[dict]:
    mentions: list[dict] = []
    pattern = re.compile(
        r"(?P<metric>market size|addressable market|revenue|sales|budget|市场规模|收入|销售额|预算)"
        r"[^\d\n]{0,40}(?:usd|rmb|cny|[$¥￥])?\s*"
        r"(?P<value>\d+(?:,\d{3})*(?:\.\d+)?)\s*"
        r"(?P<unit>bn|billion|mn|million|b|m|k|亿|万)\b",
        re.IGNORECASE,
    )
    metric_aliases = {
        "addressable market": "market size",
        "市场规模": "market size",
        "收入": "revenue",
        "销售额": "sales",
        "预算": "budget",
    }
    for match in pattern.finditer(text):
        raw_metric = match.group("metric").lower()
        metric = metric_aliases.get(raw_metric, raw_metric)
        value = normalize_metric_value(match.group("value"), match.group("unit"))
        line_start = text.rfind("\n", 0, match.start()) + 1
        line_end = text.find("\n", match.end())
        line_end = len(text) if line_end < 0 else line_end
        identity = {"metric": metric, **metric_identity(text[line_start:line_end], text)}
        missing = [field for field, field_value in identity.items() if not field_value]
        mentions.append(
            {
                "metric": metric,
                "value": value,
                "raw": match.group(0).strip(),
                "identity": identity,
                "missing_dimensions": missing,
                "identity_complete": not missing,
            }
        )
    return mentions


def analyze_metric_mentions(mentions: list[dict]) -> tuple[list[list[dict]], list[dict]]:
    conflicts: list[list[dict]] = []
    ambiguous: list[dict] = []
    by_metric: dict[str, list[dict]] = {}
    for mention in mentions:
        by_metric.setdefault(mention["metric"], []).append(mention)

    identity_fields = ("metric", "period", "region", "currency", "unit", "scope")
    for metric, metric_mentions in by_metric.items():
        if len({item["value"] for item in metric_mentions}) <= 1:
            continue
        complete_groups: dict[tuple[str, ...], list[dict]] = {}
        incomplete: list[dict] = []
        for mention in metric_mentions:
            if not mention["identity_complete"]:
                incomplete.append(mention)
                continue
            identity = mention["identity"]
            key = tuple(identity[field] for field in identity_fields)
            complete_groups.setdefault(key, []).append(mention)
        for group in complete_groups.values():
            if len({item["value"] for item in group}) > 1:
                conflicts.append(group)
        if incomplete:
            ambiguous.append(
                {
                    "metric": metric,
                    "mentions": incomplete,
                    "missing_dimensions": sorted(
                        {dimension for item in incomplete for dimension in item["missing_dimensions"]}
                    ),
                }
            )
    return conflicts, ambiguous


def metric_identity_label(identity: dict[str, str]) -> str:
    return ", ".join(
        f"{field}={identity[field]}"
        for field in ("period", "region", "currency", "unit", "scope")
    )


def audience_candidates(text: str, *, allow_label_fallback: bool) -> set[str]:
    lower = text.lower()
    candidates: set[str] = set()
    direct_patterns = {
        "board": r"send to (?:the )?board|submit to (?:the )?board|进董事会|提交董事会|董事会(?:审议|审批)",
        "boss": r"send to (?:my )?(?:boss|manager)|发(?:给)?[^。；\n]{0,12}(?:老板|领导|高层)|给(?:老板|领导|高层)|(?:老板|领导|高层)(?:审批|批准|批示|审阅)|向(?:老板|领导|高层)汇报",
        "client": r"send to (?:the )?(?:client|customer)|发(?:给)?[^。；\n]{0,12}客户|给客户|客户(?:确认|审阅|签字)|客户可见|对外发送|外发给",
    }
    for value, pattern in direct_patterns.items():
        if re.search(pattern, lower):
            candidates.add(value)
    if candidates or not allow_label_fallback:
        return candidates
    fallback_patterns = {
        "board": r"board pack|\bboard(?:[_ -](?:pack|deck|excel|memo))?\b|董事会",
        "boss": r"boss update|manager update|\bboss(?:[_ -](?:ppt|deck|email|memo|update))\b|老板汇报|领导汇报",
        "client": r"client-facing|customer-facing|\bclient(?:[_ -](?:word|ppt|pdf|excel|memo|deck|proposal))\b|客户版|客户提案|对外版|外发版",
    }
    for value, pattern in fallback_patterns.items():
        if re.search(pattern, lower):
            candidates.add(value)
    return candidates


def declared_audience_candidates(text: str) -> set[str]:
    lower = text.lower()
    patterns = {
        "board": r"board pack|board deck|board memo|board summary|for (?:the )?board|董事会(?:材料|包|汇报|摘要|审议|审批)",
        "boss": r"boss update|manager update|leadership update|executive update|for (?:the )?(?:boss|manager|leadership|executives)|(?:老板|领导|高层)(?:版|汇报|材料)",
        "client": r"client-facing|customer-facing|client memo|client proposal|client deck|client pack|customer proposal|客户版|客户提案|对外版|外发版",
    }
    return {audience for audience, pattern in patterns.items() if re.search(pattern, lower)}


def audience_family(audience: str) -> str:
    normalized = audience.lower()
    if normalized in {"client", "customer", "external"}:
        return "external"
    if normalized in {"boss", "manager", "leadership", "executive"}:
        return "leadership"
    if normalized in {"board", "directors"}:
        return "board"
    return normalized


def target_action_candidates(text: str) -> set[str]:
    lower = text.lower()
    if re.search(r"confirm scope|确认范围", lower):
        return {"confirm scope"}
    candidates: set[str] = set()
    patterns = {
        "approve decision": r"please approve|\bapprove\b|请批准|审批|批示",
        "choose option": r"choose option|选择方案|二选一",
        "confirm proposal": r"please confirm|\bconfirm\b|请确认",
        "provide feedback": r"feedback|反馈|意见",
    }
    for value, pattern in patterns.items():
        if re.search(pattern, lower):
            candidates.add(value)
    return candidates


def deadline_candidates(text: str) -> set[str]:
    return {
        match.group(0).lower()
        for match in re.finditer(
            r"tomorrow(?:\s+(?:morning|afternoon|evening))?|tonight|today|今晚|明晚|明天(?:上午|下午|晚上)?|周[一二三四五六日天]",
            text,
            re.IGNORECASE,
        )
    }


def material_stage_candidates(text: str) -> set[str]:
    lower = text.lower()
    if re.search(r"final send|final draft|终稿|定稿|客户版|外发版", lower):
        return {"final send draft"}
    if re.search(r"\bdraft\b|草稿|初稿", lower):
        return {"draft"}
    return set()


def infer_context(args: argparse.Namespace, extracted: list[dict]) -> argparse.Namespace:
    file_names = " ".join(Path(item["path"]).name for item in extracted)
    material_text = "\n".join(
        [
            *[entry["text"] for item in extracted for entry in item["entries"][:2]],
            *[entry["text"] for item in extracted for entry in item["entries"][-2:]],
        ]
    )
    sources = [
        ("current user instruction", args.context_text or "", True),
        ("conversation history", args.conversation_text or "", True),
        ("file name", file_names, True),
        ("file content", material_text, True),
    ]
    source_map: dict[str, str] = {}
    conflicts: list[dict] = []

    field_specs = [
        ("recipient", "audience", lambda text, fallback: audience_candidates(text, allow_label_fallback=fallback)),
        ("target_action", "target_action", lambda text, _fallback: target_action_candidates(text)),
        ("deadline", "deadline", lambda text, _fallback: deadline_candidates(text)),
        ("material_stage", "material_stage", lambda text, _fallback: material_stage_candidates(text)),
    ]
    for field, attr, extractor in field_specs:
        current = getattr(args, attr)
        selected = current if is_known(current) else ""
        selected_source = "explicit host argument" if selected else ""
        unresolved = False
        for source, text, allow_fallback in sources:
            if not text:
                continue
            candidates = extractor(text, allow_fallback)
            if not candidates:
                continue
            if not selected and not unresolved:
                if len(candidates) == 1:
                    selected = next(iter(candidates))
                    selected_source = source
                else:
                    unresolved = True
                    conflicts.append(
                        {
                            "field": field,
                            "selected": "unknown",
                            "source": source,
                            "candidates": sorted(candidates),
                        }
                    )
                continue
            conflicting = sorted(candidate for candidate in candidates if candidate != selected)
            if conflicting:
                conflicts.append(
                    {
                        "field": field,
                        "selected": selected or "unknown",
                        "source": source,
                        "candidates": conflicting,
                    }
                )
        if selected:
            setattr(args, attr, selected)
            source_map[field] = selected_source

    args._context_sources = source_map
    args._context_conflicts = conflicts
    return args


def add_issue(
    issues: list[dict],
    *,
    location: str,
    error_type: str,
    severity: str,
    risk: str,
    evidence: str,
    fix: str,
) -> None:
    key = (location, error_type, evidence)
    existing = {(item["location"], item["error_type"], item["evidence"]) for item in issues}
    if key in existing:
        return
    issues.append(
        {
            "location": location,
            "error_family": ERROR_FAMILIES.get(error_type, "other"),
            "error_type": error_type,
            "severity": severity,
            "risk": risk,
            "evidence": evidence,
            "fix": fix,
        }
    )


def add_context_signal(
    signals: list[dict],
    *,
    field: str,
    value: str,
    source: str,
    impact: str,
) -> None:
    if not value:
        return
    signals.append({"field": field, "value": value, "source": source, "impact": impact})


def add_unverified(items: list[str], text: str) -> None:
    if text not in items:
        items.append(text)


def build_context_basis(extracted: list[dict], args: argparse.Namespace) -> dict:
    missing_context = []
    signals: list[dict] = []
    weights: list[dict] = []

    if is_known(args.audience):
        add_context_signal(
            signals,
            field="recipient",
            value=args.audience,
            source=getattr(args, "_context_sources", {}).get("recipient", "user request or host argument"),
            impact="sets audience-specific risk weighting",
        )
    else:
        missing_context.append("recipient")

    if is_known(args.target_action):
        add_context_signal(
            signals,
            field="target_action",
            value=args.target_action,
            source=getattr(args, "_context_sources", {}).get("target_action", "user request or host argument"),
            impact="tests whether the ending gives a clear next step",
        )
    else:
        missing_context.append("target_action")

    if is_known(args.deadline):
        add_context_signal(
            signals,
            field="deadline",
            value=args.deadline,
            source=getattr(args, "_context_sources", {}).get("deadline", "user request or host argument"),
            impact="sets repair-route time pressure",
        )
    else:
        missing_context.append("deadline")

    if is_known(args.material_stage):
        add_context_signal(
            signals,
            field="material_stage",
            value=args.material_stage,
            source=getattr(args, "_context_sources", {}).get("material_stage", "user request or host argument"),
            impact="sets tolerance for draft residue and unresolved caveats",
        )
    else:
        missing_context.append("material_stage")

    for conflict in getattr(args, "_context_conflicts", []):
        candidates = ", ".join(conflict["candidates"])
        add_context_signal(
            signals,
            field=f"{conflict['field']}_conflict",
            value=f"selected={conflict['selected']}; conflicting={candidates}",
            source=conflict["source"],
            impact="keeps lower-priority or unresolved context evidence visible for review",
        )

    file_summary = ", ".join(f"{Path(item['path']).name} ({item['artifact_type']})" for item in extracted)
    add_context_signal(
        signals,
        field="file_package",
        value=file_summary,
        source="input files",
        impact="sets file-type checks and cross-file package awareness",
    )

    audience = args.audience.lower()
    if audience in {"boss", "manager", "leadership", "executive"}:
        weights.extend(
            [
                {
                    "risk_area": "decision_gap",
                    "direction": "up",
                    "reason": "boss or leadership materials need a clear requested decision",
                },
                {
                    "risk_area": "claim_evidence_gap",
                    "direction": "up",
                    "reason": "senior-reader materials get challenged on evidence strength",
                },
            ]
        )
    elif audience in {"client", "customer", "external"}:
        weights.extend(
            [
                {
                    "risk_area": "privacy_or_commitment_risk",
                    "direction": "up",
                    "reason": "client-facing materials have commitment and authorization exposure",
                },
                {
                    "risk_area": "version_residue",
                    "direction": "up",
                    "reason": "external exports cannot retain internal wording or old-version traces",
                },
                {
                    "risk_area": "audience_mismatch",
                    "direction": "up",
                    "reason": "every external attachment must declare the same client-facing audience",
                },
            ]
        )
    elif audience in {"board", "directors"}:
        weights.extend(
            [
                {
                    "risk_area": "number_conflict",
                    "direction": "up",
                    "reason": "board packs require consistent metrics and audit trail",
                },
                {
                    "risk_area": "formula_or_summary_mismatch",
                    "direction": "up",
                    "reason": "board packs often rely on summaries, pivots, and hidden detail",
                },
            ]
        )

    deadline = args.deadline.lower()
    if any(token in deadline for token in ("tonight", "tomorrow", "30 min", "30-minute", "今晚", "明天")):
        weights.append(
            {
                "risk_area": "repair_priority",
                "direction": "up",
                "reason": "near-deadline review should focus on blocking factual, numeric, and commitment risks",
            }
        )

    if not weights:
        weights.append(
            {
                "risk_area": "general_presend_risk",
                "direction": "neutral",
                "reason": "recipient-specific weighting could not be fully inferred",
            }
        )

    return {
        "recipient": args.audience,
        "target_action": args.target_action,
        "deadline": args.deadline,
        "material_stage": args.material_stage,
        "known_limits": ["deterministic heuristic inspection"],
        "missing_context": missing_context,
        "context_signals": signals,
        "risk_weighting": weights[:6],
    }


def inspect_ppt(file_data: dict, issues: list[dict], unverified_items: list[str]) -> None:
    entries = file_data["entries"]
    metric_mentions: list[dict] = []
    for entry in entries:
        location = entry["location"]
        text = entry["text"]
        lower = text.lower()

        if (
            "no source" in lower
            or "no revenue source" in lower
            or "no conversion evidence" in lower
        ):
            add_issue(
                issues,
                location=location,
                error_type="source_missing",
                severity="blocker",
                risk="关键数据缺来源、周期或口径",
                evidence=f"{location} contains market or key data text without a usable source note.",
                fix="补来源、周期和口径；无法补时降级成内部估算。",
            )

        if (
            re.fullmatch(r"slide \d+", location)
            and contains_data_bearing_claim(text)
            and not has_usable_source(text)
            and not has_issue(issues, location, "source_missing")
        ):
            add_issue(
                issues,
                location=location,
                error_type="source_missing",
                severity="blocker",
                risk="数据型页面缺可追溯来源、周期或口径",
                evidence=f"{location} contains a market, revenue, sales, or budget figure without a usable source line.",
                fix="在同页补来源、统计周期和口径；无法补齐时降级结论。",
            )

        if "verified scalable growth" in lower or ("1.2%" in lower and "verified" in lower):
            add_issue(
                issues,
                location=location,
                error_type="claim_evidence_gap",
                severity="blocker",
                risk="结论强度高于证据",
                evidence=f"{location} claims verified scalable growth while evidence only shows 1.2% movement.",
                fix="把结论降为初步正向信号，并补样本量或置信说明。",
            )

        if (
            re.fullmatch(r"slide \d+", location)
            and strong_claim_without_support(text)
            and not has_issue(issues, location, "claim_evidence_gap")
        ):
            add_issue(
                issues,
                location=location,
                error_type="claim_evidence_gap",
                severity="blocker",
                risk="强结论缺同强度证据",
                evidence=f"{location} uses proof, certainty, or leadership wording without source, sample, benchmark, or confidence support.",
                fix="补充样本、基准和统计边界，或将标题降级为初步信号。",
            )

        if "conversion uplift" in lower and ("12.0% -> 12.0%" in text or "conversion 12.0%" in lower):
            add_issue(
                issues,
                location=location,
                error_type="claim_evidence_gap",
                severity="must_fix",
                risk="标题和图表方向冲突",
                evidence=f"{location} says conversion uplift while the chart note shows conversion unchanged.",
                fix="改标题为转化持平、客单价拉动收入。",
            )

        if re.fullmatch(r"slide \d+", location):
            for mention in extract_metric_mentions(text):
                mention["location"] = location
                metric_mentions.append(mention)

        if "notes" in location.lower() and any(
            token in lower
            for token in ("internal note", "do not show", "do not share", "old pricing", "client should not see", "draft only")
        ):
            add_issue(
                issues,
                location=location,
                error_type="version_residue",
                severity="must_fix",
                risk="PPT 备注区残留内部话术或旧版发送线索",
                evidence=f"{location} contains internal speaker-note wording.",
                fix="删除备注区内部话术，或导出不含备注的发送副本。",
            )

        if "hidden" in location.lower() and any(
            token in lower
            for token in ("internal draft", "internal note", "do not show", "do not share", "old pricing", "client should not see", "draft only")
        ):
            add_issue(
                issues,
                location=location,
                error_type="version_residue",
                severity="must_fix",
                risk="PPT 隐藏页残留内部话术或旧版发送线索",
                evidence=f"{location} contains internal hidden-slide wording.",
                fix="删除隐藏页或重建客户可见副本，确认导出和发送附件不含隐藏页。",
            )

        if re.search(r"2023.+2026|2026.+2023", lower):
            add_issue(
                issues,
                location=location,
                error_type="source_stale_or_misaligned",
                severity="blocker",
                risk="来源时间和当前判断周期错位",
                evidence=f"{location} mixes 2023 source context with 2026 decision language.",
                fix="换成当前周期来源，或把结论改为历史参考。",
            )

        if "national sample" in lower and "east china" in lower:
            add_issue(
                issues,
                location=location,
                error_type="source_stale_or_misaligned",
                severity="blocker",
                risk="全国样本支撑区域结论，来源范围错位",
                evidence=f"{location} uses a national sample to support an East China conclusion.",
                fix="补华东区域样本，或把结论改成全国层面参考。",
            )

        if "user growth" in lower and "revenue growth" in lower:
            add_issue(
                issues,
                location=location,
                error_type="claim_evidence_gap",
                severity="must_fix",
                risk="用用户增长直接证明收入增长，证据链断裂",
                evidence=f"{location} says revenue growth is proven by user growth without revenue or conversion evidence.",
                fix="补收入、转化或客单价证据；否则降级为用户增长信号。",
            )

    metric_conflicts, ambiguous_metrics = analyze_metric_mentions(metric_mentions)
    for mentions in metric_conflicts:
        metric = mentions[0]["metric"]
        identity = mentions[0]["identity"]
        locations = ", ".join(f"{item['location']}: {item['raw']}" for item in mentions[:6])
        add_issue(
            issues,
            location=f"{metric} metric across deck [{metric_identity_label(identity)}]",
            error_type="number_conflict",
            severity="blocker",
            risk="同一指标、周期、区域、币种、单位和范围下出现多个数值",
            evidence=f"Conflicting {metric} values with the same metric identity found: {locations}.",
            fix="统一主数字、周期、单位和口径，需保留差异时写入脚注。",
        )

    for item in ambiguous_metrics:
        sample = ", ".join(
            f"{mention['location']}: {mention['raw']}" for mention in item["mentions"][:6]
        )
        add_unverified(
            unverified_items,
            f"{item['metric']} 出现多个数值但指标身份不完整，暂不判为冲突；缺少 "
            f"{', '.join(item['missing_dimensions'])}。位置：{sample}。",
        )

    visible_slides = [entry for entry in entries if re.fullmatch(r"slide \d+", entry["location"])]
    if visible_slides:
        last_slide = max(visible_slides, key=lambda item: int(item["location"].split()[-1]))
        if not has_decision_action(last_slide["text"]):
            add_issue(
                issues,
                location=last_slide["location"],
                error_type="decision_gap",
                severity="blocker",
                risk="最后一页缺决策动作",
                evidence=f"{last_slide['location']} has no approval ask, option, owner, confirmation request, or deadline.",
                fix="补一页需要确认的决定、责任人和时间点。",
            )


def inspect_word(file_data: dict, issues: list[dict]) -> None:
    all_text = "\n".join(f"{entry['location']}\n{entry['text']}" for entry in file_data["entries"])
    lower_all = all_text.lower()

    for entry in file_data["entries"]:
        location = entry["location"]
        lower = entry["text"].lower()

        if "42.8b" in lower and ("no source" in lower or "no period" in lower or "no metric definition" in lower):
            add_issue(
                issues,
                location=location,
                error_type="source_missing",
                severity="blocker",
                risk="Word 备忘录关键市场数字缺来源、周期和口径",
                evidence=f"{location} states 42.8B and says source, period, or metric definition is missing.",
                fix="补完整来源、统计周期和口径；无法补时降级为内部估算。",
            )

        if "fully proven by user growth" in lower or ("revenue growth" in lower and "without revenue evidence" in lower):
            add_issue(
                issues,
                location=location,
                error_type="claim_evidence_gap",
                severity="must_fix",
                risk="摘要结论用用户增长证明收入增长，证据链断裂",
                evidence=f"{location} claims revenue growth is proven while revenue evidence is absent.",
                fix="补收入、转化或客单价证据；否则降级为用户增长信号。",
            )

        if not location.startswith("comment") and ("guarantee" in lower or "fixed pricing" in lower):
            add_issue(
                issues,
                location=location,
                error_type="privacy_or_commitment_risk",
                severity="blocker",
                risk="客户备忘录出现未经审批的上线或价格承诺",
                evidence=f"{location} contains guarantee or fixed pricing language.",
                fix="改成以合同、审批和排期确认为准。",
            )

        if location.startswith(("header ", "footer ", "footnote ", "endnote ")) and any(
            token in lower
            for token in (
                "internal draft",
                "do not share",
                "do not show",
                "old pricing",
                "client should not see",
                "draft only",
                "confidential internal",
            )
        ):
            add_issue(
                issues,
                location=location,
                error_type="version_residue",
                severity="must_fix",
                risk="Word 页眉页脚或脚注残留内部话术",
                evidence=f"{location} contains internal header/footer/footnote wording.",
                fix="清理页眉页脚、脚注和尾注，重新导出客户可见副本。",
            )

    if "legal has not approved" in lower_all and "guarantee" in lower_all:
        add_issue(
            issues,
            location="comments and executive summary",
            error_type="privacy_or_commitment_risk",
            severity="blocker",
            risk="正文承诺和内部法律批注冲突",
            evidence="The memo promises a guarantee while an internal comment says legal has not approved it.",
            fix="删除确定承诺，待法务确认后再写客户可见表述。",
        )

    if any(token in lower_all for token in ("[todo", "internal comment", "trackrevisions")):
        add_issue(
            issues,
            location="Word comments / revisions / placeholders",
            error_type="version_residue",
            severity="must_fix",
            risk="Word 文件残留 TODO、内部批注或修订状态",
            evidence="The document contains TODO text, internal comments, or tracked revision markers.",
            fix="清理批注、修订和 TODO，占位内容改成客户可见文本。",
        )


def inspect_pasted_text(file_data: dict, issues: list[dict]) -> None:
    all_text = "\n".join(f"{entry['location']}\n{entry['text']}" for entry in file_data["entries"])
    lower_all = all_text.lower()

    for entry in file_data["entries"]:
        location = entry["location"]
        lower = entry["text"].lower()

        if "42.8b" in lower and ("no source" in lower or "source needed" in lower or "no period" in lower):
            add_issue(
                issues,
                location=location,
                error_type="source_missing",
                severity="blocker",
                risk="邮件正文关键数字缺来源、周期和口径",
                evidence=f"{location} cites 42.8B while source, period, or metric definition is missing.",
                fix="补来源、周期和口径；无法补时改成内部估算或删除数字。",
            )

        if "definitely prove" in lower or ("revenue growth" in lower and "user growth" in lower and "no revenue" in lower):
            add_issue(
                issues,
                location=location,
                error_type="claim_evidence_gap",
                severity="blocker",
                risk="邮件结论强于正文证据",
                evidence=f"{location} uses user growth to prove revenue growth without revenue evidence.",
                fix="降级为用户增长信号，补收入、转化或客单价证据后再写收入结论。",
            )

        if "guarantee" in lower or "firm commitment" in lower:
            add_issue(
                issues,
                location=location,
                error_type="privacy_or_commitment_risk",
                severity="blocker",
                risk="邮件正文含未确认承诺",
                evidence=f"{location} contains guarantee or firm commitment language.",
                fix="改成待审批、待合同确认或待排期确认。",
            )

        if (
            any(
                marker in lower
                for marker in (
                    "fixed fee",
                    "price is locked",
                    "will deliver by",
                    "commit to deliver",
                    "we commit",
                    "价格锁定",
                    "固定报价",
                    "承诺于",
                    "必将交付",
                )
            )
            and not has_issue(issues, location, "privacy_or_commitment_risk")
        ):
            add_issue(
                issues,
                location=location,
                error_type="privacy_or_commitment_risk",
                severity="blocker",
                risk="邮件正文把价格或交付日写成已锁定承诺",
                evidence=f"{location} contains fixed-fee, locked-price, or unconditional delivery wording.",
                fix="改成以商务、法务、合同和排期确认为准。",
            )

        if "[todo" in lower or "internal note" in lower:
            add_issue(
                issues,
                location=location,
                error_type="version_residue",
                severity="must_fix",
                risk="邮件正文残留内部占位或待办",
                evidence=f"{location} contains TODO or internal note text.",
                fix="删除内部占位，换成收件人可见内容。",
            )

    if not has_decision_action(all_text):
        add_issue(
            issues,
            location="ending",
            error_type="decision_gap",
            severity="blocker",
            risk="邮件结尾缺少明确下一步",
            evidence="The pasted text has no approval ask, owner, deadline, or next-step request.",
            fix="补一句需要对方确认的动作、责任人和时间点。",
        )


def inspect_excel(file_data: dict, issues: list[dict]) -> None:
    all_text = "\n".join(f"{entry['location']}\n{entry['text']}" for entry in file_data["entries"])
    formula_error_pattern = re.compile(r"#(?:DIV/0!|REF!|VALUE!|N/A|NAME\?|NUM!|NULL!)")
    formula_error_hits = []
    for entry in file_data["entries"]:
        for line in entry["text"].splitlines():
            if formula_error_pattern.search(line):
                cell_ref = line.split(":", 1)[0]
                formula_error_hits.append(f"{entry['location']}!{cell_ref}")

    if formula_error_hits:
        sample = ", ".join(formula_error_hits[:4])
        add_issue(
            issues,
            location=sample,
            error_type="formula_or_summary_mismatch",
            severity="blocker",
            risk="Excel 公式返回错误值，汇总或图表可能已经失真",
            evidence=f"Workbook contains formula error values in {sample}.",
            fix="修复除数、引用区域或缺失输入，重新计算并复核相关汇总和图表。",
        )

    for entry in file_data["entries"]:
        lower = entry["text"].lower()
        if "sheet_state=hidden" in lower and any(
            token in lower
            for token in (
                "internal draft",
                "internal note",
                "do not show",
                "do not share",
                "old pricing",
                "client should not see",
                "draft only",
                "confidential internal",
            )
        ):
            add_issue(
                issues,
                location=entry["location"],
                error_type="version_residue",
                severity="must_fix",
                risk="Excel 隐藏工作表残留内部话术或旧版发送线索",
                evidence=f"{entry['location']} is hidden and contains internal workbook wording.",
                fix="删除隐藏工作表或重建发送副本，确认隐藏表、隐藏行列和外部可见附件均不含内部口径。",
            )

        if "comment" in entry["location"].lower() and any(
            token in lower
            for token in (
                "internal draft",
                "internal note",
                "do not show",
                "do not share",
                "old pricing",
                "client should not see",
                "draft only",
                "confidential internal",
                "internal approval",
            )
        ):
            add_issue(
                issues,
                location=entry["location"],
                error_type="version_residue",
                severity="must_fix",
                risk="Excel 批注或备注残留内部话术或旧版发送线索",
                evidence=f"{entry['location']} contains internal workbook comment wording.",
                fix="删除批注/备注或重建无批注发送副本，确认外发文件不含内部审批、旧价格或客户不可见说明。",
            )

    if "230000000" in all_text and "210000000" in all_text:
        add_issue(
            issues,
            location="Summary / Detail revenue",
            error_type="number_conflict",
            severity="blocker",
            risk="汇总收入和明细收入不一致",
            evidence="Summary contains 230000000 while Detail contains 210000000 for the revenue metric.",
            fix="统一汇总公式引用区域，保留差异口径说明。",
        )

    hidden_negative_adjustments = []
    for entry in file_data["entries"]:
        if "sheet_state=hidden" not in entry["text"]:
            continue
        for line in entry["text"].splitlines():
            if re.search(r"^[A-Z]+\d+:\s*-\d+(?:\.\d+)?(?:\s|$)", line):
                cell_ref = line.split(":", 1)[0]
                hidden_negative_adjustments.append(f"{entry['location']}!{cell_ref}")

    if hidden_negative_adjustments:
        sample = ", ".join(hidden_negative_adjustments[:4])
        add_issue(
            issues,
            location=sample,
            error_type="formula_or_summary_mismatch",
            severity="blocker",
            risk="隐藏工作表含负数调整，可能影响汇总",
            evidence=f"A hidden sheet contains a negative adjustment in {sample}.",
            fix="确认隐藏行列和隐藏表对汇总的影响，必要时移到公开假设区。",
        )

    if "last refresh" in all_text.lower() and "current detail updated" in all_text.lower():
        add_issue(
            issues,
            location="Pivot",
            error_type="formula_or_summary_mismatch",
            severity="blocker",
            risk="透视表刷新时间早于明细更新时间",
            evidence="Pivot says last refresh 2026-06-01 while detail was updated 2026-07-02.",
            fix="刷新透视表并锁定发送前筛选状态。",
        )

    if "unit and currency missing" in all_text.lower():
        add_issue(
            issues,
            location="Summary chart",
            error_type="source_missing",
            severity="must_fix",
            risk="图表缺单位或币种，容易误读规模",
            evidence="Summary note states unit and currency missing.",
            fix="补单位、币种、税前税后和周期。",
        )


def inspect_pdf(file_data: dict, issues: list[dict]) -> None:
    page_count = len(file_data["entries"])
    all_text = "\n".join(entry["text"] for entry in file_data["entries"])
    extractable_chars = len(re.sub(r"\s+", "", all_text))
    if page_count > 0 and extractable_chars < 20:
        add_issue(
            issues,
            location="PDF text layer",
            error_type="format_rendering_error",
            severity="blocker",
            risk="PDF 几乎没有可抽取文字，无法核验正文、来源、数字或承诺",
            evidence=f"Extracted only {extractable_chars} non-space characters across {page_count} PDF pages.",
            fix="改用源文件或重新导出带可选文字层的 PDF；至少渲染逐页复查后再判断能否发送。",
        )
    if re.search(r"12 pages|12 页|/12", all_text) and page_count != 12:
        add_issue(
            issues,
            location="table of contents / footer",
            error_type="version_residue",
            severity="must_fix",
            risk="目录或页脚页数和实际 PDF 页数不一致",
            evidence=f"Text references 12 pages while extracted page count is {page_count}.",
            fix="重新导出并复查目录、页脚和正文页数。",
        )

    for entry in file_data["entries"]:
        location = entry["location"]
        lower = entry["text"].lower()
        if "white box" in lower or "covered" in lower:
            add_issue(
                issues,
                location=location,
                error_type="format_rendering_error",
                severity="blocker",
                risk="导出后图表或图例被遮挡",
                evidence=f"{location} text indicates the legend is covered by a white box.",
                fix="重新导出，渲染检查该页图表图例。",
            )
        if "truncated" in lower or "source url is truncated" in lower:
            add_issue(
                issues,
                location=location,
                error_type="source_missing",
                severity="must_fix",
                risk="来源链接导出后断裂或不完整",
                evidence=f"{location} states source URL is truncated.",
                fix="补完整来源链接，导出后逐页复查脚注。",
            )
        if "internal project codename" in lower or "apollo-r9" in lower:
            add_issue(
                issues,
                location=location,
                error_type="version_residue",
                severity="must_fix",
                risk="客户版残留内部项目代号",
                evidence=f"{location} contains internal project codename text.",
                fix="删除内部代号，改成客户可见项目名。",
            )
        if "guarantee" in lower or "firm commitment" in lower:
            add_issue(
                issues,
                location=location,
                error_type="privacy_or_commitment_risk",
                severity="blocker",
                risk="客户版出现未经确认的确定承诺",
                evidence=f"{location} contains guarantee or firm commitment language.",
                fix="改成以合同、排期或审批确认为准。",
            )
        if "realclientco" in lower or "no authorization" in lower:
            add_issue(
                issues,
                location=location,
                error_type="privacy_or_commitment_risk",
                severity="blocker",
                risk="客户案例可能缺授权或未脱敏",
                evidence=f"{location} contains a named client case without authorization marker.",
                fix="删除真实客户名，保留行业、规模和已授权信息。",
            )
        if "internal discussion draft" in lower or "internal framing" in lower:
            add_issue(
                issues,
                location=location,
                error_type="audience_mismatch",
                severity="must_fix",
                risk="客户版开头仍像内部讨论稿",
                evidence=f"{location} uses internal discussion framing in a client-facing PDF.",
                fix="重写开头为客户可见目标、范围和下一步。",
            )


def normalized_large_number(value: str, multiplier: int = 1) -> int | None:
    try:
        number = float(value.replace(",", ""))
    except ValueError:
        return None
    return int(number * multiplier)


def inspect_cross_file_package(extracted: list[dict], issues: list[dict]) -> None:
    if len(extracted) < 2:
        return

    metric_mentions: list[tuple[str, int]] = []
    for file_data in extracted:
        file_name = Path(file_data["path"]).name
        for entry in file_data["entries"]:
            location = f"{file_name} / {entry['location']}"
            text = entry["text"]
            lower = text.lower()
            if not any(token in lower for token in ("sales", "revenue", "销售额", "收入")):
                continue
            for match in re.finditer(r"(\d+(?:,\d{3})+|\d+(?:\.\d+)?)\s*m\b", lower):
                value = normalized_large_number(match.group(1), 1_000_000)
                if value is not None:
                    metric_mentions.append((location, value))
            for match in re.finditer(r"\b(2[01]0(?:,?000){2}|230(?:,?000){2})\b", lower):
                value = normalized_large_number(match.group(1))
                if value is not None:
                    metric_mentions.append((location, value))

    values = {value for _, value in metric_mentions}
    files = {location.split(" / ", 1)[0] for location, _ in metric_mentions}
    if len(values) > 1 and len(files) > 1:
        sample = ", ".join(f"{location}: {value}" for location, value in metric_mentions[:6])
        add_issue(
            issues,
            location="package revenue / sales metric across files",
            error_type="number_conflict",
            severity="blocker",
            risk="同一附件包里的收入或销售额口径冲突",
            evidence=f"Cross-file metric values disagree: {sample}.",
            fix="先锁一个主口径，再同步更新 PPT、Excel、Word/PDF 附件中的同名指标。",
        )


def inspect_audience_alignment(extracted: list[dict], issues: list[dict], args: argparse.Namespace) -> None:
    if not is_known(args.audience):
        return

    selected_family = audience_family(args.audience)
    mismatches: list[dict[str, str]] = []
    for file_data in extracted:
        file_name = Path(file_data["path"]).name
        file_candidates: set[str] = set()
        if file_data["artifact_type"] != "pasted_text":
            file_label_text = file_name.replace("_", " ").replace("-", " ")
            file_candidates = audience_candidates(file_label_text, allow_label_fallback=True)
        for candidate in sorted(file_candidates):
            if audience_family(candidate) != selected_family:
                mismatches.append(
                    {
                        "location": f"{file_name} / file name",
                        "audience": candidate,
                        "evidence": file_name,
                        "source": "file_name",
                    }
                )
        for entry in file_data["entries"]:
            candidates = declared_audience_candidates(entry["text"])
            for candidate in sorted(candidates):
                if audience_family(candidate) == selected_family:
                    continue
                evidence = " ".join(entry["text"].split())[:180]
                mismatches.append(
                    {
                        "location": f"{file_name} / {entry['location']}",
                        "audience": candidate,
                        "evidence": evidence,
                        "source": "content",
                    }
                )

    unique: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for item in mismatches:
        key = (item["location"], item["audience"])
        if key not in seen:
            seen.add(key)
            unique.append(item)
    if not unique:
        return

    locations = "; ".join(item["location"] for item in unique[:6])
    evidence = "; ".join(
        f"{item['location']} declares {item['audience']}: {item['evidence']}" for item in unique[:6]
    )
    severity = "blocker" if any(item["source"] == "content" for item in unique) else "must_fix"
    add_issue(
        issues,
        location=f"package audience labels: {locations}",
        error_type="audience_mismatch",
        severity=severity,
        risk=f"附件声明的受众与当前收件人 {args.audience} 冲突",
        evidence=f"Current recipient is {args.audience}; conflicting attachment labels found: {evidence}.",
        fix="逐个附件改成当前收件人版本，统一文件名、封面或首表标题、页眉页脚、审阅占位语和结尾动作后再导出。",
    )


def verdict_for(issues: list[dict]) -> str:
    if any(item["severity"] == "blocker" for item in issues):
        return "hold_before_send"
    if any(item["severity"] == "must_fix" for item in issues):
        return "send_after_quick_fixes"
    return "can_send"


def context_priority(error_type: str, args: argparse.Namespace) -> int:
    audience = args.audience.lower()
    priority_by_audience = {
        "boss": {
            "decision_gap": 0,
            "claim_evidence_gap": 1,
            "source_missing": 2,
            "number_conflict": 3,
            "privacy_or_commitment_risk": 4,
            "version_residue": 5,
        },
        "manager": {
            "decision_gap": 0,
            "claim_evidence_gap": 1,
            "source_missing": 2,
            "number_conflict": 3,
            "privacy_or_commitment_risk": 4,
            "version_residue": 5,
        },
        "leadership": {
            "decision_gap": 0,
            "claim_evidence_gap": 1,
            "source_missing": 2,
            "number_conflict": 3,
            "privacy_or_commitment_risk": 4,
            "version_residue": 5,
        },
        "executive": {
            "decision_gap": 0,
            "claim_evidence_gap": 1,
            "source_missing": 2,
            "number_conflict": 3,
            "privacy_or_commitment_risk": 4,
            "version_residue": 5,
        },
        "client": {
            "privacy_or_commitment_risk": 0,
            "version_residue": 1,
            "audience_mismatch": 2,
            "number_conflict": 3,
            "source_missing": 4,
            "claim_evidence_gap": 5,
            "decision_gap": 6,
        },
        "customer": {
            "privacy_or_commitment_risk": 0,
            "version_residue": 1,
            "audience_mismatch": 2,
            "number_conflict": 3,
            "source_missing": 4,
            "claim_evidence_gap": 5,
            "decision_gap": 6,
        },
        "external": {
            "privacy_or_commitment_risk": 0,
            "version_residue": 1,
            "audience_mismatch": 2,
            "number_conflict": 3,
            "source_missing": 4,
            "claim_evidence_gap": 5,
            "decision_gap": 6,
        },
        "board": {
            "formula_or_summary_mismatch": 0,
            "number_conflict": 1,
            "source_missing": 2,
            "claim_evidence_gap": 3,
            "decision_gap": 4,
            "version_residue": 5,
        },
        "directors": {
            "formula_or_summary_mismatch": 0,
            "number_conflict": 1,
            "source_missing": 2,
            "claim_evidence_gap": 3,
            "decision_gap": 4,
            "version_residue": 5,
        },
    }
    return priority_by_audience.get(audience, {}).get(error_type, 20)


def context_reason(issue: dict, args: argparse.Namespace) -> str:
    audience = args.audience.lower()
    error_type = issue["error_type"]
    reason = AUDIENCE_CONTEXT_REASONS.get(audience, {}).get(error_type) or DEFAULT_CONTEXT_REASONS.get(
        error_type,
        "该问题会影响本次发送目标，需在出街前处理。",
    )
    context_parts = []
    if is_known(args.audience):
        context_parts.append(f"recipient={args.audience}")
    if is_known(args.target_action):
        context_parts.append(f"target_action={args.target_action}")
    if is_known(args.deadline):
        context_parts.append(f"deadline={args.deadline}")
    if context_parts:
        reason += " 本次上下文：" + "；".join(context_parts) + "。"
    deadline = args.deadline.lower()
    if issue.get("severity") == "blocker" and any(
        token in deadline for token in ("tonight", "tomorrow", "30 min", "30-minute", "今晚", "明天")
    ):
        reason += " 临近发送，先处理这类阻断风险，弱化低收益润色。"
    return reason


def attach_context_reasons(issues: list[dict], args: argparse.Namespace) -> list[dict]:
    for issue in issues:
        issue["context_reason"] = context_reason(issue, args)
    return issues


def build_repair_route(issues: list[dict]) -> list[dict]:
    if not issues:
        return [{"timebox": "0-10 min", "action": "做最终导出和发送前复查。"}]
    type_to_action = {
        "source_missing": "补来源、周期、口径和单位。",
        "source_stale_or_misaligned": "替换错位来源或降级结论。",
        "number_conflict": "统一主数字和口径。",
        "formula_or_summary_mismatch": "修公式、刷新透视表、核对隐藏行列。",
        "claim_evidence_gap": "降低标题和结论强度。",
        "decision_gap": "补决策请求、责任人和时间点。",
        "format_rendering_error": "重新导出并渲染复查问题页。",
        "privacy_or_commitment_risk": "脱敏并改承诺措辞。",
        "version_residue": "清理旧版本和页脚目录残留。",
        "audience_mismatch": "重写首页和结尾动作。",
    }
    ordered_types = []
    for issue in issues:
        if issue["error_type"] not in ordered_types:
            ordered_types.append(issue["error_type"])
    actions = [type_to_action.get(error_type, "处理剩余必须改项。") for error_type in ordered_types[:3]]
    labels = ["0-10 min", "10-20 min", "20-30 min"]
    return [{"timebox": labels[idx], "action": action} for idx, action in enumerate(actions)]


def build_can_keep(extracted: list[dict], issues: list[dict]) -> list[str]:
    issue_locations = [item["location"] for item in issues]
    artifact_types = {item["artifact_type"] for item in extracted}
    if len(extracted) > 1:
        names = "、".join(Path(item["path"]).name for item in extracted)
        if issue_locations:
            return [f"附件包 {names} 的文件分工可保留；集中修正已定位的跨文件口径和外发风险。"]
        return [f"附件包 {names} 的文件分工和现有组合可保留。"]

    file_data = extracted[0]
    artifact_type = file_data["artifact_type"]
    if artifact_type == "ppt":
        visible = [entry["location"] for entry in file_data["entries"] if re.fullmatch(r"slide \d+", entry["location"])]
        affected = {location for location in visible if location in issue_locations}
        clean_count = max(0, len(visible) - len(affected))
        if affected:
            locations = "、".join(sorted(affected, key=lambda item: int(item.split()[-1])))
            return [f"PPT 现有页序可保留；{clean_count} 个未命中硬错误的可见页不用大改，集中修正 {locations}。"]
        return [f"PPT 当前 {len(visible)} 页的页序、来源说明和末页决策动作可保留。"]
    if artifact_type == "word":
        body_count = sum(entry["location"].startswith("paragraph ") for entry in file_data["entries"])
        return [f"Word 当前 {body_count} 个正文段落的主体结构可保留；只处理已定位的正文、批注或页眉页脚问题。"]
    if artifact_type == "excel":
        sheets = [entry["location"] for entry in file_data["entries"] if " comment " not in entry["location"]]
        return [f"Excel 当前的 {'、'.join(sheets[:4])} 工作表分层可保留；集中修正已定位的公式、口径或隐藏内容。"]
    if artifact_type == "pdf":
        return [f"PDF 当前 {len(file_data['entries'])} 页的页序可保留；只重导并复查已定位的页码、来源或呈现问题。"]
    if artifact_type == "pasted_text":
        return [f"邮件当前 {len(file_data['entries'])} 个段落的主体顺序可保留；集中修改已定位的数据、承诺和结尾动作。"]
    return [f"{'、'.join(sorted(artifact_types))} 交付物的主体结构可保留，集中处理已定位的必改项。"]


def inspect_files(paths: list[Path], args: argparse.Namespace) -> dict:
    extracted = [extract(path) for path in paths]
    args = infer_context(args, extracted)
    issues: list[dict] = []
    unverified_items: list[str] = []
    artifact_type = extracted[0]["artifact_type"] if len(extracted) == 1 else "mixed_package"
    for file_data in extracted:
        if file_data["artifact_type"] == "ppt":
            inspect_ppt(file_data, issues, unverified_items)
        elif file_data["artifact_type"] == "word":
            inspect_word(file_data, issues)
        elif file_data["artifact_type"] == "pasted_text":
            inspect_pasted_text(file_data, issues)
        elif file_data["artifact_type"] == "excel":
            inspect_excel(file_data, issues)
        elif file_data["artifact_type"] == "pdf":
            inspect_pdf(file_data, issues)
    inspect_cross_file_package(extracted, issues)
    inspect_audience_alignment(extracted, issues, args)

    all_issues = sorted(
        issues,
        key=lambda item: (
            0 if item["severity"] == "blocker" else 1,
            context_priority(item["error_type"], args),
            item["location"],
            item["error_type"],
        ),
    )
    all_issues = attach_context_reasons(all_issues, args)
    must_fix = all_issues[:7]
    additional_findings = all_issues[7:]
    omitted_locations = [
        f"{item['location']} [{item['error_type']}; {item['severity']}]"
        for item in additional_findings
    ]
    finding_overflow = {
        "detected_total": len(all_issues),
        "displayed_total": len(must_fix),
        "omitted_total": len(additional_findings),
        "omitted_blocker_count": sum(item["severity"] == "blocker" for item in additional_findings),
        "omitted_locations": omitted_locations,
        "expand_instruction": "读取 additional_findings 展开首屏以外的完整发现。",
    }
    context_basis = build_context_basis(extracted, args)
    confidence = "medium"
    if context_basis["missing_context"]:
        confidence = "low"
    if context_basis["missing_context"]:
        add_unverified(
            unverified_items,
            "上下文缺口待确认："
            + missing_context_text(context_basis["missing_context"])
            + "；补齐后需复核风险排序和发送判定。"
        )
    add_unverified(
        unverified_items,
        "脚本只检查可抽取文本和基础元数据；视觉版式、图表底层数据、批注、外部来源仍需复查。"
    )

    return {
        "artifact_type": artifact_type,
        "audience": args.audience,
        "deadline": args.deadline,
        "context_basis": context_basis,
        "verdict": verdict_for(all_issues),
        "must_fix": must_fix,
        "additional_findings": additional_findings,
        "finding_overflow": finding_overflow,
        "can_keep": build_can_keep(extracted, all_issues),
        "repair_route": build_repair_route(all_issues),
        "unverified_items": unverified_items,
        "confidence": confidence,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run deterministic pre-send checks on deliverable files.")
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--audience", default="unknown")
    parser.add_argument("--target-action", default="unknown")
    parser.add_argument("--deadline", default="unknown")
    parser.add_argument("--material-stage", default="unknown")
    parser.add_argument("--context-text", default="")
    parser.add_argument("--conversation-text", default="")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = inspect_files(args.files, args)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
