"""数值规整：千分位、负数（括号 / 减号）、单位（万元/亿元/USD）。

约束（SKILL.md "重要约束 §3"）：不做"创意修正"，无法解析的原文返回 parse_ok=False。

借鉴：PDF_Financial_Report_Analysis/base_extractor.py 的单位检测表与括号→负处理。
"""
from __future__ import annotations

import re
from dataclasses import dataclass

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


@dataclass
class NumericValue:
    raw: str
    value: float | None                # 始终已归一到元
    unit: str | None = None            # 解析时实际使用的单位（来自文本后缀或 default_unit）
    is_negative: bool = False
    parse_ok: bool = True
    reason: str = ""


def detect_unit_in_context(text: str) -> str | None:
    """从一段文本（通常是表格上方的"单位：万元 币种：人民币"）中识别单位声明。"""
    m = re.search(r"单位\s*[:：]\s*([^\s币]+)", text)
    if m:
        candidate = m.group(1).strip()
        for key in _UNIT_KEYS_SORTED:
            if candidate.startswith(key):
                return key
    return None


def parse_number(raw: str, default_unit: str | None = None) -> NumericValue:
    """解析单元格文本为标准化数值（元）。

    支持：
      - 千分位（半角/全角）："1,234,567.89" / "1，234"
      - 括号负数（半角/全角）："(1,234)" / "（1,234）"
      - 显式减号（半角/全角）："-1234" / "－1234"
      - 内嵌单位后缀："1234 万元" / "12亿"
      - 货币符号清理：¥ $ HK$ 等
      - default_unit 来自上下文（如表头上方"单位：万元"）
    """
    if raw is None:
        return NumericValue(raw="", value=None, parse_ok=False, reason="none")
    text = raw.strip()
    if not text:
        return NumericValue(raw=raw, value=None, parse_ok=False, reason="empty")

    # 1) 括号 → 负
    is_negative = False
    if ("(" in text and ")" in text) or ("（" in text and "）" in text):
        is_negative = True
        text = text.replace("(", "").replace(")", "")
        text = text.replace("（", "").replace("）", "")

    # 2) 内嵌单位后缀（先于符号清理，以免"万元"被破坏）
    detected_unit: str | None = None
    text_stripped = text.strip()
    for key in _UNIT_KEYS_SORTED:
        if text_stripped.endswith(key):
            detected_unit = key
            text = text_stripped[: -len(key)].rstrip()
            break

    # 3) 显式减号
    text = text.strip()
    while text and text[0] in "-－":
        is_negative = True
        text = text[1:].lstrip()

    # 4) 千分位 + 货币符号 + 全角空白
    text = text.replace(",", "").replace("，", "")
    text = _CURRENCY_RE.sub("", text)
    text = text.replace("　", "").strip()

    if not text:
        return NumericValue(raw=raw, value=None, parse_ok=False, reason="no_digits")

    try:
        num = float(text)
    except ValueError:
        return NumericValue(raw=raw, value=None, parse_ok=False, reason="not_parseable")

    if is_negative:
        num = -abs(num)

    # 5) 单位归一化到元
    unit = detected_unit or default_unit
    if unit and unit in UNIT_FACTOR:
        num = num * UNIT_FACTOR[unit]

    return NumericValue(
        raw=raw,
        value=num,
        unit=unit,
        is_negative=is_negative,
        parse_ok=True,
    )
