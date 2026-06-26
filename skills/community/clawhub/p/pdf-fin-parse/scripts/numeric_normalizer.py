"""数值规整：千分位、负数（括号/减号）、单位（万元/亿元/USD/百分比）、横线。

约束：不做"创意修正"。无法解析的原文返回 NumericValue(parse_ok=False, value=None)。
方向词正负（"下降 3%" → -3）放在 finance_terms_aligner 层处理（需要上下文）。

借鉴 `_legacy/numeric_normalizer.py` 并扩展：
  - "-"/"—"/"——"/"--"/"不适用"等空 placeholder → value=None
  - "12.5%" / "12.5％" → value=12.5, unit="percent"
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional


# 单位 → 倍率（标准化目标：元）；按字符串长度倒序匹配以避免 "万" 抢先匹配 "万元"
UNIT_FACTOR: dict[str, int] = {
    "亿元": 100_000_000,
    "百万元": 1_000_000,
    "万元": 10_000,
    "千元": 1_000,
    "亿": 100_000_000,
    "万": 10_000,
    "元": 1,
    "yuan": 1,
    "RMB": 1,
    "'000": 1_000,
    "HK$'000": 1_000,
}

_UNIT_KEYS_SORTED = sorted(UNIT_FACTOR.keys(), key=len, reverse=True)

# 货币符号 / 全角等价
_CURRENCY_RE = re.compile(r"[¥￥$＄€£HK]")

# 空白 / 不适用 / 横线占位符
_EMPTY_PLACEHOLDERS = {
    "", "-", "—", "——", "--", "－", "ー", "/",
    "n/a", "N/A", "N.A.", "n.a.", "NA",
    "不适用", "无", "空白", "—-",
}

# 单位声明（表格上方"以人民币百万元列示"、"单位：万元"等）
_UNIT_DECLARE_PATTERNS = [
    re.compile(r"单位\s*[:：]\s*([^\s,。币]+)"),
    re.compile(r"以人民币([^\s,。列]+?)(?:列示|单位|为单位|计)"),
    re.compile(r"以([^\s,。列]+?元)列示"),
]


@dataclass
class NumericValue:
    raw: str
    value: Optional[float]              # 已归一到元（含 percent 时按字面值，单位 percent）
    unit: Optional[str] = None          # 解析时实际使用的单位
    is_negative: bool = False
    parse_ok: bool = True
    reason: str = ""


def detect_unit_in_context(text: str) -> Optional[str]:
    """从一段文本（通常是表格上方）中识别单位声明。"""
    if not text:
        return None
    for pat in _UNIT_DECLARE_PATTERNS:
        m = pat.search(text)
        if m:
            candidate = m.group(1).strip()
            for key in _UNIT_KEYS_SORTED:
                if candidate.startswith(key) or candidate == key:
                    return key
    return None


def parse_number(raw: str, default_unit: Optional[str] = None) -> NumericValue:
    """解析单元格文本为标准化数值。

    输出 unit 含义：
      - "percent"        百分比，value 是字面数（12.5）
      - "yuan"/"万元"等   人民币单位，value 已归一化到 yuan
      - None             未识别单位（value 仍可能是数字，但单位缺失）
    """
    if raw is None:
        return NumericValue(raw="", value=None, parse_ok=False, reason="none")
    text_orig = str(raw).strip()
    if not text_orig or text_orig in _EMPTY_PLACEHOLDERS:
        return NumericValue(raw=raw, value=None, parse_ok=False, reason="empty")

    text = text_orig

    # 0) 百分比识别（在所有其他处理之前）
    is_percent = False
    if text.endswith("%") or text.endswith("％"):
        is_percent = True
        text = text[:-1].rstrip()

    # 1) 括号 → 负
    is_negative = False
    if ("(" in text and ")" in text) or ("（" in text and "）" in text):
        is_negative = True
        text = text.replace("(", "").replace(")", "")
        text = text.replace("（", "").replace("）", "")

    # 2) 内嵌单位后缀（先于符号清理，以免"万元"被破坏）
    detected_unit: Optional[str] = None
    text_stripped = text.strip()
    if not is_percent:
        for key in _UNIT_KEYS_SORTED:
            if text_stripped.endswith(key):
                detected_unit = key
                text = text_stripped[: -len(key)].rstrip()
                break

    # 3) 显式减号（半角/全角）
    text = text.strip()
    while text and text[0] in "-－":
        is_negative = True
        text = text[1:].lstrip()

    # 4) 千分位 + 货币符号 + 全角空白
    text = text.replace(",", "").replace("，", "")
    text = _CURRENCY_RE.sub("", text)
    text = text.replace("　", "").replace(" ", "").strip()

    if not text:
        return NumericValue(raw=raw, value=None, parse_ok=False, reason="no_digits")

    try:
        num = float(text)
    except ValueError:
        return NumericValue(raw=raw, value=None, parse_ok=False, reason="not_parseable")

    if is_negative:
        num = -abs(num)

    # 5) 百分比 → unit=percent，value 保持字面
    if is_percent:
        return NumericValue(
            raw=raw, value=num, unit="percent",
            is_negative=is_negative, parse_ok=True,
        )

    # 6) 单位归一化到元
    unit = detected_unit or default_unit
    if unit and unit in UNIT_FACTOR:
        num = num * UNIT_FACTOR[unit]
        canonical_unit = "yuan"
    else:
        canonical_unit = unit

    return NumericValue(
        raw=raw, value=num, unit=canonical_unit,
        is_negative=is_negative, parse_ok=True,
    )
