"""Customer-facing answer guardrails for the OEF skill."""

from __future__ import annotations

import re

DISCLAIMER = "数据查询由易方达指数直通车提供，以上内容由 AI 总结生成，仅供参考，不构成投资建议、收益预测或任何交易决策依据。更多信息请在微信搜索“指数直通车”小程序，或访问易方达指数直通车网页版：www.etf.com.cn"

# 禁止在回答中出现类似词汇
FORBIDDEN_PHRASES = (
    "推荐买入",
    "建议买入",
    "建议买这只",
    "现在适合买",
    "适合买入",
    "应该买",
    "应该卖",
    "应该加仓",
    "应该减仓",
    "可以无脑买",
    "稳赚",
    "保本",
)

FORBIDDEN_INTERNAL_PATTERNS = (
    r"Authorization",
    r"Bearer\s+[A-Za-z0-9._\-]+",
    r"config\.py",
    r"SKILL\.md",
    r"catalog-(?:etf|oef)\.md",
    r"BASE_URL",
    r"/skill/v1/",
    r"https?://[^\s]*etf-api-service[^\s]*",
    r"raw JSON",
    r"原始JSON",
)

INVALID_VALUE_PATTERNS = (
    r"\bNone\b",
    r"\bnull\b",
    r"-888\.89",
)

AUTO_REPLACEMENTS = (
    ("%%", "%"),
    ("元元/份", "元/份"),
    ("万元万元", "万元"),
    ("亿元亿元", "亿元"),
    ("\r\n", "\n"),
)


def _normalize_text(text: str) -> str:
    for old, new in AUTO_REPLACEMENTS:
        text = text.replace(old, new)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    text = re.sub(
        rf"(?:\n+)?{re.escape(DISCLAIMER)}(?:\s*{re.escape(DISCLAIMER)})*$",
        "",
        text,
    ).strip()
    return text


def _find_pattern(patterns: tuple[str, ...], text: str) -> str | None:
    for pattern in patterns:
        if re.search(pattern, text, flags=re.IGNORECASE):
            return pattern
    return None


def finalize_answer(answer: str) -> str:
    """Normalize and validate a final customer-facing answer.

    The caller should only print the returned string. If validation fails,
    rewrite the answer before showing it to the user.
    """

    if not isinstance(answer, str):
        raise TypeError("answer must be a string")

    body = _normalize_text(answer)
    if not body:
        raise ValueError("final answer is empty")

    forbidden_phrase = _find_pattern(FORBIDDEN_PHRASES, body)
    if forbidden_phrase:
        raise ValueError(f"final answer contains forbidden advice phrase: {forbidden_phrase}")

    forbidden_internal = _find_pattern(FORBIDDEN_INTERNAL_PATTERNS, body)
    if forbidden_internal:
        raise ValueError(
            f"final answer leaks internal implementation detail: {forbidden_internal}"
        )

    invalid_value = _find_pattern(INVALID_VALUE_PATTERNS, body)
    if invalid_value:
        raise ValueError(f"final answer exposes invalid internal value: {invalid_value}")

    return f"{body}\n\n{DISCLAIMER}"


def validate_answer(answer: str) -> None:
    """Validation-only wrapper used by tests or evals."""

    finalize_answer(answer)
