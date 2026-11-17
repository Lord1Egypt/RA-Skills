"""Shared customer-facing answer guardrails for Index Hub V3 skills."""

from __future__ import annotations

import re

DISCLAIMER = "数据查询由易方达指数直通车提供，以上内容由 AI 总结生成，仅供参考，不构成投资建议、收益预测或任何交易决策依据。更多信息请在微信搜索“指数直通车”小程序，或访问易方达指数直通车网页版：www.etf.com.cn"

# 投资表达只做本地硬门禁：按分句组合三组词，不尝试解析完整中文语义。
ACTION_CUES = ("建议", "推荐", "应该", "应当", "可以", "可考虑", "可以考虑", "不妨", "最好", "优先", "首选", "倾向", "值得", "适合", "我会")
RECOMMENDATION_CUES = ("推荐", "优先", "首选", "倾向", "值得", "适合", "可考虑", "可以考虑", "我会")
TRADE_ACTIONS = ("买入", "卖出", "购买", "申购", "赎回", "持有", "加仓", "减仓", "定投", "配置", "建仓", "清仓", "调仓")
PRODUCT_TERMS = ("这只", "该基金", "这只基金", "该产品", "这只产品", "ETF", "场外基金", "A类", "C类")
DIRECT_ADVICE_TERMS = ("建议买", "建议卖", "推荐买", "推荐卖", "应该买", "应该卖", "值得买", "适合买", "适合卖", "该买", "可以买", "可以卖", "该卖", "买它", "选它", "无脑买", "满仓", "梭哈", "上车")
PROMISE_TERMS = ("稳赚", "保本", "保证收益", "保证盈利", "承诺收益", "承诺回报", "本金无忧", "本金不受损失", "收益有保障", "最低收益", "零风险", "无风险")
PREDICTION_CUES = ("预测", "预计", "预期", "必然", "肯定", "一定", "大概率", "确定会", "可达", "将达", "目标收益")
FUTURE_OUTCOMES = ("收益", "回报", "涨幅", "业绩", "上涨", "下跌", "盈利", "获利", "涨", "跌")
NEGATION_TERMS = ("不能", "无法", "不会", "不应", "不应该", "不可", "不宜", "不要", "不建议", "不推荐", "请勿", "避免", "禁止", "不得", "不代表", "不等于", "不意味着", "不足以", "不保证", "不保本")
EDUCATION_TERMS = ("不当", "误导", "违规", "宣传", "话术", "示例", "引用", "不可信", "不应相信")
PROCESS_TERMS = ("通过", "渠道", "平台", "账户", "流程", "方式", "规则")
CLAUSE_BOUNDARY = re.compile(r"[，,。！？!?；;\n]+|(?:但|不过|然而|可是|却)")
FUND_CODE = re.compile(r"(?<!\d)\d{6}(?!\d)")
PERCENTAGE = re.compile(r"\d+(?:\.\d+)?%")

FORBIDDEN_INTERNAL_PATTERNS = (
    r"Bearer\s+[A-Za-z0-9._\-]{8,}",
    r"\bSKA[A-Za-z0-9._\-]{16,}\b",
    r"\bsk-[A-Za-z0-9._\-]{16,}\b",
    r"(?:API[_ -]?KEY|密钥|秘钥)\s*[:=：]\s*[\"']?[A-Za-z0-9._\-]{12,}",
    r"https?://[^\s]*etf-api-service[^\s]*",
)

INVALID_VALUE_PATTERNS = (
    r"(?<!\d)-888\.89(?!\d)",
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


def _find_term(text: str, terms: tuple[str, ...]) -> str | None:
    return next((term for term in terms if term in text), None)


def _has_product(clause: str) -> bool:
    return bool(_find_term(clause, PRODUCT_TERMS) or FUND_CODE.search(clause))


def _is_safe_clause(clause: str) -> bool:
    if any(term in clause for term in ("不是说", "并不是说", "并非不", "不能不")):
        return False
    return bool(_find_term(clause, NEGATION_TERMS + EDUCATION_TERMS))


def _find_investment_violation(text: str) -> tuple[str, str] | None:
    for clause in filter(None, (part.strip() for part in CLAUSE_BOUNDARY.split(text))):
        promise = _find_term(clause, PROMISE_TERMS)
        prediction = _find_term(clause, PREDICTION_CUES)
        direct = _find_term(clause, DIRECT_ADVICE_TERMS)
        cue = _find_term(clause, ACTION_CUES)
        recommendation = _find_term(clause, RECOMMENDATION_CUES)
        action = _find_term(clause, TRADE_ACTIONS)
        product_choice = "选择" if "选择" in clause and _has_product(clause) else None
        preference = _find_term(clause, ("更好", "更优", "更合适", "更值得", "首选"))
        percentage = PERCENTAGE.search(clause)
        allocation = percentage.group(0) if percentage and _find_term(clause, ("仓位", "配置比例")) else None
        process = _find_term(clause, PROCESS_TERMS)
        factual_process = bool(
            process
            and (
                cue in ("可以", "适合")
                and action in ("购买", "申购", "赎回")
                or recommendation == "适合"
                and "交易" in clause
            )
        )
        checks = (
            ("收益承诺", promise),
            ("收益预测", prediction if prediction and _find_term(clause, FUTURE_OUTCOMES) else None),
            ("交易指令", direct),
            ("交易指令", cue if cue and action and not factual_process else None),
            ("产品推荐", cue if cue and product_choice else None),
            ("产品推荐", recommendation if recommendation and _has_product(clause) and not factual_process else None),
            ("产品推荐", preference if preference and _has_product(clause) else None),
            ("仓位建议", allocation),
        )
        for category, match in checks:
            if match and not _is_safe_clause(clause):
                return category, match
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

    investment_violation = _find_investment_violation(body)
    if investment_violation:
        category, excerpt = investment_violation
        raise ValueError(
            f"final answer contains prohibited investment expression ({category}): {excerpt}"
        )

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
