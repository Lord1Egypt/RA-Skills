from __future__ import annotations

from collections import Counter, defaultdict

from .models import FinancialFact, Issue

AMOUNT_UNIT_RANK = {"元": 1, "千元": 2, "万元": 3, "亿元": 4}
AMOUNT_UNIT_FACTOR = {"元": 1.0, "千元": 1_000.0, "万元": 10_000.0, "亿元": 100_000_000.0}
ROUNDING_STATUSES = {"CONFIRMED_CONSISTENT", "NORMAL_ROUNDING"}
MERGED_SCOPES = {"发行人合并", "合并"}
LAST_COMPARE_STATS: Counter[str] = Counter()

# 同一精确指标、同一期间、同一口径的两个正规披露，其差异比率不可能过大；
# 超过该阈值的“差异”几乎都是明细行对合计行、单一产品/客户对总体、
# 或单位/口径不一致造成的伪冲突，应降级为候选而非高置信冲突。
MAX_STRICT_DIFF_RATIO = 0.30

# 命中以下语义的上下文，说明数值来自敏感性分析、模拟测算、每股/市盈率等衍生口径，
# 不能与原始指标金额直接比较。
SENSITIVITY_KEYWORDS = (
    "敏感性", "假设", "假定", "情景", "模拟测算", "测算", "压力测试", "弹性",
    "每股", "市盈率", "市净率", "倍数", "摊薄", "备考", "基于", "计算依据",
    "融资规模", "募集资金", "销售额", "采购额", "对毛利率的影响", "累计对毛利率的影响", "毛利率差异率",
)
# 合计/汇总行标记，用于识别聚合层级，禁止合计行与明细行直接比较。
TOTAL_MARKERS = ("合计", "总计", "总额", "汇总", "总收入", "总成本")


def _aggregation_level(fact: FinancialFact) -> str:
    """返回 'total'（合计/整体披露）/ 'detail'（明细）/ 'unknown'。"""
    blob = f"{fact.category or ''} {fact.raw_metric or ''}"
    if any(m in blob for m in TOTAL_MARKERS):
        return "total"
    # 正文叙述型整体披露（如“2023-2025年营业收入分别为…”）通常是全年合计口径。
    if fact.position.startswith("PARA") and any(
        k in (fact.context or "") for k in ("分别为", "实现营业收入", "实现的营业收入", "营业收入为", "净利润为", "全年")
    ):
        return "total"
    return "unknown"


def _suspect_caliber(left: FinancialFact, right: FinancialFact, ratio: float | None) -> str:
    """判断一对差异是否疑似口径/层级/量级问题；返回原因字符串，无问题返回空串。"""
    if ratio is not None and ratio > MAX_STRICT_DIFF_RATIO:
        return f"差异比率{ratio:.0%}过大，疑似明细对合计或单位/口径不一致，不作高置信冲突"
    blob = f"{left.context or ''} {right.context or ''} {left.category or ''} {right.category or ''}"
    for kw in SENSITIVITY_KEYWORDS:
        if kw in blob:
            return f"上下文含敏感性/测算语义（命中“{kw}”），数值非原始指标口径"
    la, ra = _aggregation_level(left), _aggregation_level(right)
    if {la, ra} == {"total", "detail"}:
        return "比较双方分别为合计行与明细行，聚合层级不一致，不可直接比较"
    return ""


def compare_financial_facts(facts: list[FinancialFact], tolerance: dict) -> tuple[list[Issue], list[dict]]:
    LAST_COMPARE_STATS.clear()
    issues: list[Issue] = []
    exclusions: list[dict] = []
    comparable = []
    for fact in facts:
        reason = _exclusion_reason(fact)
        if reason:
            exclusions.append(_exclusion(fact, *reason))
        else:
            comparable.append(fact)

    groups: dict[tuple[str, str, str, str, str], list[FinancialFact]] = defaultdict(list)
    for fact in comparable:
        groups[_base_key(fact)].append(fact)

    for key, rows in groups.items():
        if len({r.source_doc_id for r in rows}) < 2:
            continue
        strict_rows, candidate_rows = _split_by_scope(rows)
        for sub_rows, candidate in [(strict_rows, False), (candidate_rows, True)]:
            if len({r.source_doc_id for r in sub_rows}) < 2:
                continue
            issue = _compare_group("|".join(key), sub_rows, tolerance, len(issues) + 1, candidate=candidate)
            if issue:
                issues.append(issue)
    return issues, exclusions


def _base_key(fact: FinancialFact) -> tuple[str, str, str, str, str]:
    return (
        fact.subject or "发行人",
        fact.metric_canonical_exact,
        fact.period,
        fact.period_type,
        fact.value_type,
    )


def _split_by_scope(rows: list[FinancialFact]) -> tuple[list[FinancialFact], list[FinancialFact]]:
    scope_counts = defaultdict(list)
    for row in rows:
        normalized = "发行人合并" if row.scope in MERGED_SCOPES else row.scope
        category = row.category if row.category and row.category != "未分类" else "UNRELIABLE_CATEGORY"
        scope_counts[(normalized, category)].append(row)
    strict = []
    for (scope, category), scoped in scope_counts.items():
        if scope in {"发行人合并", "母公司"} and category != "UNRELIABLE_CATEGORY" and len({r.source_doc_id for r in scoped}) >= 2:
            strict.extend(scoped)
    candidate = [r for r in rows if r not in strict]
    if not candidate and len({r.category for r in rows}) > 1:
        candidate = rows
    return strict, candidate


def _compare_group(key: str, rows: list[FinancialFact], tolerance: dict, seq: int, candidate: bool) -> Issue | None:
    best_issue = None
    best_diff = 0.0
    for i, left in enumerate(rows):
        for right in rows[i + 1:]:
            if left.source_doc_id == right.source_doc_id or left.evidence_id == right.evidence_id:
                continue
            if left.currency != right.currency:
                continue
            result = compare_pair(left, right)
            LAST_COMPARE_STATS[result["status"]] += 1
            if result["status"] in ROUNDING_STATUSES:
                continue
            diff = abs(result["diff"] or 0.0)
            if diff > best_diff:
                best_diff = diff
                best_issue = _issue_from_pair(seq, key, left, right, result, tolerance, candidate)
    return best_issue


def _norm_scope(scope: str) -> str:
    return "发行人合并" if scope in MERGED_SCOPES else scope


def _scope_conflict(left_scope: str, right_scope: str) -> bool:
    """母公司与合并是明确不同的报表口径，禁止直接比较；其余不确定口径仍可作候选。"""
    a, b = _norm_scope(left_scope), _norm_scope(right_scope)
    return {"母公司"} & {a, b} != set() and {"发行人合并"} & {a, b} != set()


def compare_pair(left: FinancialFact, right: FinancialFact) -> dict:
    if left.value_type != right.value_type:
        return {"status": "CALIBER_DIFFERENCE", "reason": "金额、比例、百分点或倍数类型不同", "diff": None}
    if left.currency != right.currency:
        return {"status": "CALIBER_DIFFERENCE", "reason": "币种不同且无汇率依据", "diff": None}
    if _scope_conflict(left.scope, right.scope):
        return {"status": "CALIBER_DIFFERENCE", "reason": f"合并与母公司口径不同（{left.scope} vs {right.scope}）", "diff": None}
    if left.value_type == "amount":
        unit = larger_amount_unit(left.raw_unit, right.raw_unit)
        if unit is None:
            return {"status": "UNIT_UNKNOWN", "reason": "单位未知或不可换算", "diff": None}
        lv = convert_amount(left.value or 0.0, left.raw_unit, unit)
        rv = convert_amount(right.value or 0.0, right.raw_unit, unit)
    else:
        unit = left.raw_unit
        lv = left.value or 0.0
        rv = right.value or 0.0
    places = min(left.raw_decimal_places, right.raw_decimal_places)
    lround = round(lv, places)
    rround = round(rv, places)
    interval = 0.5 * (10 ** (-places)) if places >= 0 else 0.5
    status = "CONFIRMED_CONSISTENT" if lround == rround else "HIGH_CONFIDENCE_CONFLICT"
    if status != "CONFIRMED_CONSISTENT" and abs(lv - rv) <= interval * 2:
        status = "NORMAL_ROUNDING"
    return {
        "status": status,
        "comparison_unit": unit,
        "left_unrounded": lv,
        "right_unrounded": rv,
        "left_rounded": lround,
        "right_rounded": rround,
        "decimal_places": places,
        "rounding_interval": interval,
        "diff": rround - lround,
        "reason": "按较大披露单位和较低披露精度比较。",
    }


def larger_amount_unit(left: str, right: str) -> str | None:
    if left not in AMOUNT_UNIT_RANK or right not in AMOUNT_UNIT_RANK:
        return None
    return left if AMOUNT_UNIT_RANK[left] >= AMOUNT_UNIT_RANK[right] else right


def convert_amount(value: float, from_unit: str, to_unit: str) -> float:
    return value * AMOUNT_UNIT_FACTOR[from_unit] / AMOUNT_UNIT_FACTOR[to_unit]


def _issue_from_pair(seq: int, key: str, left: FinancialFact, right: FinancialFact, result: dict, tolerance: dict, candidate: bool) -> Issue:
    diff = result["diff"]
    base = max(abs(result["left_rounded"] or 0), abs(result["right_rounded"] or 0))
    ratio = abs(diff) / base if base else None
    suspect = _suspect_caliber(left, right, ratio)
    if candidate or suspect:
        # 候选组，或严格组中疑似口径/层级/量级问题的对，统一作为候选项，不升A/B。
        level = "C"
        status = "MANUAL_REVIEW_CANDIDATE"
        category = "候选跨文件差异"
        secondary_verified = False
    else:
        level = _level(abs(diff), ratio)
        secondary_verified = level in {"A", "B"} and _secondary_verify(left, right, result, ratio)
        status = result["status"]
        category = "跨文件财务数据差异"
        if level in {"A", "B"} and not secondary_verified:
            level = "C"
            status = "LOW_CONFIDENCE_CONFLICT"
    return Issue(
        issue_id=f"ISS{seq:05d}",
        level=level,
        category=category,
        round="",
        files=sorted({left.filename, right.filename}),
        item=key,
        conclusion=f"换算至{result['comparison_unit']}后存在差异，舍入后差异为 {diff:.6g}{result['comparison_unit']}。",
        source_1=f"{left.filename} {left.position}: {left.raw_metric}={left.raw_value_text}{left.raw_unit}",
        source_2=f"{right.filename} {right.position}: {right.raw_metric}={right.raw_value_text}{right.raw_unit}",
        diff_amount=diff,
        diff_ratio=ratio,
        caliber_analysis=(
            f"可比键：{key}；scope：{left.scope} vs {right.scope}；分类：{left.category} vs {right.category}；"
            f"共同比较单位：{result['comparison_unit']}；未舍入值：{result['left_unrounded']:.10g} vs {result['right_unrounded']:.10g}；"
            f"比较精度：{result['decimal_places']}位小数；舍入后：{result['left_rounded']} vs {result['right_rounded']}。"
        ),
        evidence_pages=[f"{left.filename} {left.position}", f"{right.filename} {right.position}"],
        evidence_ids=[left.evidence_id, right.evidence_id],
        comparison_unit=result["comparison_unit"],
        source_1_converted_unrounded=result["left_unrounded"],
        source_2_converted_unrounded=result["right_unrounded"],
        source_1_converted_rounded=result["left_rounded"],
        source_2_converted_rounded=result["right_rounded"],
        comparison_decimal_places=result["decimal_places"],
        rounding_interval=result["rounding_interval"],
        secondary_verified=secondary_verified,
        source_1_text=f"{left.filename} {left.position}｜{(left.context or '').strip()[:160]}",
        source_2_text=f"{right.filename} {right.position}｜{(right.context or '').strip()[:160]}",
        basis="单位可靠、期间明确、精确指标一致、类型一致后执行比较；候选项不升级A/B。",
        suggestion=(f"降级原因：{suspect}。请人工确认两处数值是否同一聚合层级与口径。" if suspect
                    else "核对披露口径、版本变化、分类维度和原始数据来源。"),
        extraction_confidence=min(left.confidence, right.confidence),
        judgement_confidence=0.86 if secondary_verified else (0.68 if candidate else 0.72),
        need_manual_review=True,
        status=status,
    )


def _level(diff: float, ratio: float | None) -> str:
    if ratio is not None and ratio > 0.05:
        return "A"
    if (ratio is not None and ratio > 0.01) or diff > 1:
        return "B"
    return "C"


def _secondary_verify(left: FinancialFact, right: FinancialFact, result: dict, ratio: float | None) -> bool:
    """二次验证：内容级核对，而非字段赋值。任一不满足即不确认为高置信冲突。"""
    if result["status"] != "HIGH_CONFIDENCE_CONFLICT":
        return False
    if left.evidence_id == right.evidence_id:
        return False
    # 精确指标、期间必须一致。
    if left.metric_canonical_exact != right.metric_canonical_exact:
        return False
    if left.period != right.period:
        return False
    # 单位必须可靠。
    if left.raw_unit == "unknown" or right.raw_unit == "unknown":
        return False
    if left.unit_confidence < 0.6 or right.unit_confidence < 0.6:
        return False
    # 量级护栏：差异比率过大者疑似明细/合计或口径问题，不确认。
    if ratio is None or ratio > MAX_STRICT_DIFF_RATIO:
        return False
    # 语义/层级护栏。
    if _suspect_caliber(left, right, ratio):
        return False
    # 原文回溯：两个数值都应真实出现在各自上下文中。
    if left.raw_value_text not in left.context or right.raw_value_text not in right.context:
        return False
    return True


def _exclusion_reason(fact: FinancialFact) -> tuple[str, str] | None:
    if fact.value is None:
        return "value_missing", "value is None"
    if getattr(fact, "semantic_role", "") == "forecast_or_assumption" or getattr(fact, "is_calculated", False):
        return "forecast_or_assumption_metric", "假定增长、预测、测算或敏感性口径，不能与实际历史财务指标比较"
    if getattr(fact, "semantic_role", "primary_metric_value") != "primary_metric_value":
        return "semantic_role_not_primary", f"semantic_role={fact.semantic_role}"
    if getattr(fact, "value_binding_reason", "primary_metric_value") not in {"", "primary_metric_value"}:
        return "value_binding_not_primary", f"value_binding_reason={fact.value_binding_reason}"
    if getattr(fact, "is_adjusted_metric", False):
        return "metric_caliber_modifier_mismatch", f"adjustment_type={fact.adjustment_type}; base_metric={fact.base_metric}"
    # “孰低/孰高”是按扣非前后取低（高）值的特殊口径，既非归母净利润也非扣非归母净利润，
    # 不能与任一原始指标直接比较。
    if any(k in (fact.context or "") for k in ("孰低", "孰高")):
        return "special_caliber_lower_higher", "上下文含‘孰低/孰高’，为扣非前后取值的特殊口径"
    if any(k in (fact.context or "") for k in ("基于", "为计算依据", "假设", "预计", "不低于", "敏感性测算")) and any(
        k in (fact.context or "") for k in ("市盈率", "融资规模", "募集资金", "每股", "估值")
    ):
        return "derived_metric_context", "上下文为衍生指标或测算口径"
    if any(k in (fact.context or "") for k in ("对毛利率的影响", "累计对毛利率的影响", "毛利率差异率")):
        return "gross_margin_impact", "毛利率影响/差异率不是正常毛利率"
    if fact.raw_unit == "unknown" or fact.unit_confidence < 0.5:
        return "unit_unknown", "raw_unit unknown or unit_confidence < 0.5"
    if not fact.period_exact:
        return "period_vague", "period_exact is False"
    if not fact.metric_canonical_exact:
        return "metric_not_exact", "metric_canonical_exact empty"
    if fact.value_type not in {"amount", "percent"}:
        return "value_type_mismatch", f"value_type={fact.value_type}"
    if fact.currency != "人民币":
        return "currency_not_comparable", f"currency={fact.currency}"
    return None


def _exclusion(fact: FinancialFact, reason: str, condition: str) -> dict:
    return {
        "fact_id": fact.fact_id,
        "file": fact.filename,
        "position": fact.position,
        "metric": fact.raw_metric,
        "period": fact.period,
        "unit": fact.raw_unit,
        "value": fact.raw_value_text,
        "scope": fact.scope,
        "value_type": fact.value_type,
        "semantic_role": getattr(fact, "semantic_role", ""),
        "value_binding_reason": getattr(fact, "value_binding_reason", ""),
        "caliber_modifier": getattr(fact, "caliber_modifier", ""),
        "adjustment_type": getattr(fact, "adjustment_type", ""),
        "base_metric": getattr(fact, "base_metric", ""),
        "cutoff_date": getattr(fact, "cutoff_date", ""),
        "data_nature": getattr(fact, "data_nature", ""),
        "exclusion_reason": reason,
        "triggered_condition": condition,
    }
