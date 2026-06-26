"""财务术语对齐：标题 → statement_type；row label → 科目（基础版）.

P2 最小可用：靠关键词识别"三大主表"和常见科目类别。完整词表/科目编码留 P2.5。
"""
from __future__ import annotations

from typing import Optional


# 表类型关键词（含中英；优先级按出现顺序）
_STATEMENT_KEYWORDS = [
    ("balance_sheet",     ["资产负债表", "财务状况表", "balance sheet",
                            "statement of financial position"]),
    ("income_statement",  ["利润表", "综合收益", "income statement",
                            "profit or loss", "operations"]),
    ("cash_flow",         ["现金流量表", "cash flow"]),
    ("equity_change",     ["权益变动", "股东权益变动",
                            "changes in equity", "changes in shareholders"]),
]

# 资产负债表常见类目标签（用于分组行）
_BALANCE_GROUP_LABELS = {
    "资产：":          "asset",
    "资产":            "asset",
    "Assets":          "asset",
    "负债：":          "liability",
    "负债":            "liability",
    "Liabilities":     "liability",
    "股东权益：":      "equity",
    "股东权益":        "equity",
    "所有者权益：":    "equity",
    "所有者权益":      "equity",
    "权益":            "equity",
    "Equity":          "equity",
    "Shareholders' Equity": "equity",
}

# 常见合计行（用于 finance_validator 校验）
_SUBTOTAL_KEYWORDS = {
    "asset":     ["资产总计", "资产合计", "Total assets"],
    "liability": ["负债总计", "负债合计", "Total liabilities"],
    "equity":    ["股东权益合计", "所有者权益合计", "权益合计",
                   "Total equity", "Total shareholders' equity"],
}

# 表格末尾的"全表总计"行（资产 = 负债 + 权益 的恒等总计），既非任一 group 的 subtotal
# 也不应被累加进任一 group 的明细。validator 看到这些 label 时直接 skip。
_GRAND_TOTAL_KEYWORDS = [
    "负债和股东权益总计", "负债和所有者权益总计",
    "负债及股东权益总计", "负债及所有者权益总计",
    "负债和股东权益合计", "负债和所有者权益合计",
    "Total liabilities and equity",
    "Total liabilities and shareholders' equity",
]


def detect_statement_type(caption: Optional[str], context_text: str = "") -> Optional[str]:
    """从表标题/上下文识别报表类型。返回 statement_type 或 None。"""
    text = ((caption or "") + "\n" + (context_text or "")).lower()
    if not text.strip():
        return None
    for stype, kws in _STATEMENT_KEYWORDS:
        for kw in kws:
            if kw.lower() in text:
                return stype
    return None


def classify_row_label(label: str) -> Optional[str]:
    """识别行标签是否为类目分组标签（"资产：" 等）。返回类目 key 或 None。"""
    if not label:
        return None
    s = label.strip()
    return _BALANCE_GROUP_LABELS.get(s) or _BALANCE_GROUP_LABELS.get(s.rstrip("：:"))


def is_subtotal_row(label: str, group: Optional[str] = None) -> Optional[str]:
    """判断行标签是否是已知小计/合计行；命中返回所属 group，否则 None。

    Args:
        label:   行标签文本（如 "资产总计"）
        group:   可选限定（如 "asset"），不指定则跨 group 查
    """
    if not label:
        return None
    s = label.strip()
    # 优先排除"全表总计"（"负债和股东权益总计"），它不属于任一 subgroup
    if is_grand_total_row(s):
        return None
    groups = [group] if group else list(_SUBTOTAL_KEYWORDS.keys())
    for g in groups:
        for kw in _SUBTOTAL_KEYWORDS.get(g, []):
            if kw in s:
                return g
    return None


def is_grand_total_row(label: str) -> bool:
    """是否是"资产 = 负债 + 权益"恒等式的全表总计行（应从 group 累加中排除）。"""
    if not label:
        return False
    s = label.strip()
    return any(kw in s for kw in _GRAND_TOTAL_KEYWORDS)
