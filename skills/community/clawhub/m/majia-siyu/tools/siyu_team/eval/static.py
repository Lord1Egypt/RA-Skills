"""Mode-aware deterministic compliance and static anti-pattern scanning.

``scan`` keeps the v1 dictionary API.  New integrations can use
``scan_result`` for typed hits with offsets and context.  The same lexicon is
interpreted differently for customer copy, internal reports, knowledge atoms,
and quoted evidence; a word alone is no longer a hard-redline decision.
"""
from __future__ import annotations

import re
from typing import Any

from ..errors import ComplianceBlockedError
from .compliance_lexicon import (
    ABSOLUTE_SUPERLATIVE_PATTERN,
    GUARANTEE_PATTERN,
    RESTRICTED_TOOL_PATTERN,
    RISK_TERM_PATTERN,
    LexiconRule,
    RULES,
)
from .models import ScanHit, ScanMode, ScanResult


_ATTRIBUTION = re.compile(
    r"(自称|声称|宣称|号称|对外称|对方称|厂商称|品牌方称|报道称|"
    r"据悉|据称|据介绍|报道中称|原文称|引用称)"
)
_NEGATION_BEFORE = re.compile(
    r"(不是|并非|不要|不得|不应|不该|不能|不会|未曾|未经|所谓|"
    r"避免|禁止|严禁|切勿|拒绝|杜绝|规避|防止|反对|警惕)"
    r"(?:再|去|做|采用|使用|设置|进行|靠|通过|让用户)?"
    r"[\s，、：:]{0,3}.{0,10}$"
)
_NEGATION_AFTER = re.compile(
    r"^.{0,12}(不成立|并不成立|不代表|不等于|未必|不可取|不可信|"
    r"有风险|系违规|涉嫌违法|待核验|尚未核验|未经核验|需核验|"
    r"仍需验证|需要验证|尚待验证|未验证|是红线|为反例|是误导)"
)
_RISK_EXPLANATION = re.compile(
    r"(红线|封号风险|合规风险|涉嫌违规|涉嫌违法|违规机制|违法机制|"
    r"风险提示|待核验|尚未核验|未经核验|未核实|不可取|不可信|"
    r"失败模式|反例|误区|会直接炸|炸掉账号|会导致封号)"
)
_DELIVERABLE_MARKER = re.compile(
    r"(建议|要求|应当|必须|执行|采用|上线|设置|活动机制|营销机制|"
    r"对外文案|发布文案|客户文案|海报|话术|宣传语|口号|让用户|"
    r"让顾客|让会员)"
)
_CLEAR_AD_CONTEXT = re.compile(
    r"(本品牌|本店|本产品|本服务|本方案|我们(?:是|的)|我司|"
    r"全国|全网|全行业|全市|销量|排名|成绩|测试结果|市场占有率|"
    r"第一名|品牌|产品|服务|"
    r"效果|首选|选择|价格|品质|广告|宣传|海报|口号|文案)"
)
_RANKING_CONTEXT = re.compile(
    r"(本品牌|本店|本产品|本服务|我司|全国|全网|全行业|全市|"
    r"销量|排名|成绩|测试结果|市场占有率)"
)
_CHINESE_QUOTE_PAIRS = (("「", "」"), ("『", "』"), ("“", "”"))
_CONTEXT_BOUNDARIES = "。！？!?；;\n"


def _coerce_mode(mode: ScanMode | str) -> ScanMode:
    if isinstance(mode, ScanMode):
        return mode
    try:
        return ScanMode(mode)
    except ValueError as exc:
        allowed = ", ".join(item.value for item in ScanMode)
        raise ValueError(f"未知 ScanMode {mode!r}；可选：{allowed}") from exc


def _snippet(text: str, start: int, end: int, radius: int = 28) -> str:
    if start < 0:
        return text[: radius * 2].strip()
    return text[max(0, start - radius) : min(len(text), end + radius)].strip()


def _local_parts(
    text: str, start: int, end: int, radius: int = 36
) -> tuple[str, str, str]:
    left = text[max(0, start - radius) : start]
    right = text[end : min(len(text), end + radius)]
    left_boundary = max(left.rfind(char) for char in _CONTEXT_BOUNDARIES)
    if left_boundary >= 0:
        left = left[left_boundary + 1 :]
    right_boundaries = [
        index
        for char in _CONTEXT_BOUNDARIES
        if (index := right.find(char)) >= 0
    ]
    if right_boundaries:
        right = right[: min(right_boundaries)]
    return left, right, left + text[start:end] + right


def _inside_chinese_quote(text: str, start: int, end: int) -> bool:
    for opening, closing in _CHINESE_QUOTE_PAIRS:
        last_open = text.rfind(opening, 0, start + 1)
        last_close = text.rfind(closing, 0, start + 1)
        next_close = text.find(closing, end)
        if last_open > last_close and next_close >= end:
            return True
    return False


def _context_reason(
    text: str, start: int, end: int, mode: ScanMode
) -> str | None:
    """Return why a risky token is a mention rather than an active claim."""

    if mode is ScanMode.QUOTED_EVIDENCE:
        return "quoted_evidence"
    left, right, local = _local_parts(text, start, end)
    if _NEGATION_BEFORE.search(left) or _NEGATION_AFTER.search(right):
        return "negated"
    if _ATTRIBUTION.search(left[-24:]):
        return "attributed"
    if mode is not ScanMode.CUSTOMER_COPY and _inside_chinese_quote(
        text, start, end
    ):
        return "quoted"
    # “无风险/零风险”是承诺本身，不得因包含“风险”二字而被降级。
    risk_local = local.replace("无风险", "").replace("零风险", "")
    if _RISK_EXPLANATION.search(risk_local):
        return "risk_explanation"
    return None


def _is_prescriptive(text: str, start: int, end: int) -> bool:
    left, right, local = _local_parts(text, start, end, radius=30)
    del left, right
    return bool(_DELIVERABLE_MARKER.search(local))


def _is_clear_ad_claim(text: str, start: int, end: int) -> bool:
    _left, _right, local = _local_parts(text, start, end, radius=24)
    return bool(_CLEAR_AD_CONTEXT.search(local))


def _red_match_kind(token: str) -> str:
    if GUARANTEE_PATTERN.fullmatch(token):
        return "guarantee"
    if RESTRICTED_TOOL_PATTERN.fullmatch(token):
        return "restricted_tool"
    if RISK_TERM_PATTERN.fullmatch(token):
        return "risk_term"
    if ABSOLUTE_SUPERLATIVE_PATTERN.fullmatch(token):
        return "superlative"
    return "redline_candidate"


def _effective_rule_id(rule: LexiconRule, token: str) -> str:
    if rule.flag != "COMPLIANCE_RED":
        return rule.rule
    return {
        "guarantee": "deceptive_guarantee",
        "restricted_tool": "restricted_tool",
        "risk_term": "induced_share_risk_term",
        "superlative": "absolute_superlative_claim",
        "redline_candidate": rule.rule,
    }[_red_match_kind(token)]


def _is_ordering_first(text: str, start: int, end: int, token: str) -> bool:
    """Recognise “第一，先……” as an ordinal rather than a ranking claim."""

    if token != "第一":
        return False
    suffix = text[end : end + 2]
    if not re.match(r"^[\s，、,:：]", suffix):
        return False
    _left, _right, local = _local_parts(text, start, end, radius=20)
    return not _RANKING_CONTEXT.search(local)


def _contextual_flag(reason: str) -> str:
    if reason == "attributed":
        return "ATTRIBUTED_CLAIM"
    if reason in {"quoted", "quoted_evidence"}:
        return "QUOTED_RISK_MENTION"
    return "RISK_TERM_MENTION"


def _classify_hit(
    rule: LexiconRule,
    text: str,
    start: int,
    end: int,
    token: str,
    mode: ScanMode,
) -> tuple[str, str, float, bool]:
    """Return ``(flag, description, severity, hard)`` for one occurrence."""

    if rule.flag in {"NO_CALIBRATION", "NO_METRIC", "PRIVACY_COLLECT"}:
        return rule.flag, rule.description, rule.severity, False

    reason = _context_reason(text, start, end, mode)
    if reason is not None:
        reason_labels = {
            "negated": "否定语境中的风险词提及",
            "attributed": "归因转述中的未核验主张",
            "quoted": "内部引文中的风险词提及",
            "quoted_evidence": "引证模式中的风险词提及",
            "risk_explanation": "风险说明中的词语提及",
        }
        return (
            _contextual_flag(reason),
            f"{rule.description}；{reason_labels[reason]}，不阻断",
            min(rule.severity, 0.05),
            False,
        )

    if mode is ScanMode.QUOTED_EVIDENCE:
        # Kept as a defensive branch should context handling change later.
        return (
            "QUOTED_RISK_MENTION",
            f"{rule.description}；引证模式仅提示",
            min(rule.severity, 0.05),
            False,
        )

    if rule.flag == "ABSOLUTE_CLAIM":
        clear_ad_claim = _is_clear_ad_claim(text, start, end)
        hard = (
            mode is ScanMode.CUSTOMER_COPY and clear_ad_claim
        ) or (
            mode is ScanMode.KNOWLEDGE
            and clear_ad_claim
            and _is_prescriptive(text, start, end)
        )
        description = rule.description
        if not hard:
            description += f"；{mode.value} 语境仅提示或转人工复核"
        return rule.flag, description, rule.severity, hard

    if rule.flag == "INDUCE_SHARE":
        if mode is ScanMode.CUSTOMER_COPY:
            return rule.flag, rule.description, rule.severity, True
        hard = mode is ScanMode.KNOWLEDGE and _is_prescriptive(
            text, start, end
        )
        description = rule.description
        if not hard:
            description += f"；{mode.value} 语境保留风险提示，不阻断"
        return rule.flag, description, rule.severity, hard

    if rule.flag == "COMPLIANCE_RED":
        kind = _red_match_kind(token)
        if mode is ScanMode.CUSTOMER_COPY:
            return rule.flag, rule.description, rule.severity, True
        if kind == "superlative":
            hard = (
                mode is ScanMode.KNOWLEDGE
                and _is_clear_ad_claim(text, start, end)
                and _is_prescriptive(text, start, end)
            )
            description = rule.description
            if not hard:
                description += f"；{mode.value} 语境仅提示或转人工复核"
            return (
                rule.flag if hard else "ABSOLUTE_CLAIM",
                description,
                rule.severity,
                hard,
            )
        hard = mode is ScanMode.KNOWLEDGE and _is_prescriptive(
            text, start, end
        )
        description = rule.description
        if not hard:
            description += f"；{mode.value} 语境保留风险提示，不阻断"
        return rule.flag, description, rule.severity, hard

    return rule.flag, rule.description, rule.severity, rule.default_hard


def _match_hit(
    rule: LexiconRule,
    text: str,
    start: int,
    end: int,
    token: str,
    mode: ScanMode,
) -> ScanHit:
    flag, description, severity, hard = _classify_hit(
        rule, text, start, end, token, mode
    )
    return ScanHit(
        flag=flag,
        description=description,
        offset=start,
        end=end,
        snippet=_snippet(text, start, end),
        rule=_effective_rule_id(rule, token),
        mode=mode,
        severity=severity,
        hard=hard,
        soft=not hard,
    )


def scan_result(
    text: str, mode: ScanMode | str = ScanMode.CUSTOMER_COPY
) -> ScanResult:
    """Return a typed, mode-aware static scan result."""

    scan_mode = _coerce_mode(mode)
    hits: list[ScanHit] = []
    for rule in RULES:
        pattern = rule.pattern
        if pattern is None:
            continue
        if rule.absence_rule:
            if pattern.search(text):
                continue
            hits.append(
                _match_hit(rule, text, -1, -1, "", scan_mode)
            )
            continue
        for match in pattern.finditer(text):
            if rule.flag == "COMPLIANCE_RED" and _is_ordering_first(
                text,
                match.start(),
                match.end(),
                match.group(0),
            ):
                continue
            hits.append(
                _match_hit(
                    rule,
                    text,
                    match.start(),
                    match.end(),
                    match.group(0),
                    scan_mode,
                )
            )

    weighted_penalty_sum = sum(hit.severity for hit in hits)
    penalty = max(0.5, 1.0 - weighted_penalty_sum)
    return ScanResult(
        mode=scan_mode,
        text_length=len(text),
        hits=tuple(hits),
        penalty=penalty,
    )


def scan(
    text: str, mode: ScanMode | str = ScanMode.CUSTOMER_COPY
) -> dict[str, Any]:
    """Compatibility wrapper returning the historical dictionary shape."""

    return scan_result(text, mode=mode).to_dict()


def assert_compliant(
    text: str, mode: ScanMode | str = ScanMode.CUSTOMER_COPY
) -> dict[str, Any]:
    """Raise only for hard hits under the selected scanning context."""

    result = scan(text, mode=mode)
    if not result["hard_fail"]:
        return result
    raise ComplianceBlockedError(
        "命中合规红线，方案不得交付",
        flags=tuple(result["flags"]),
        details=tuple(dict(d) for d in result["details"]),
    )
