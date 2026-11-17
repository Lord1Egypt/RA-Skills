#!/usr/bin/env python3
"""Render an auditable, self-contained HTML report from deterministic strategy artifacts."""

from __future__ import annotations

import argparse
import html
import json
import math
import os
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import quote


SKILL_VERSION = "4.3.3"
TRADE_ACTIONS = {
    "CONTRIBUTION_REBALANCE",
    "STRATEGIC_REBALANCE",
    "RISK_REDUCE",
    "TACTICAL_ROTATE",
    "REENTRY_AFTER_RISK_OFF",
    "FUND_REPLACE",
}
BUY_ACTIONS = {"CONTRIBUTION_REBALANCE", "REENTRY_AFTER_RISK_OFF"}
NO_TRADE_ACTIONS = {
    "HOLD",
    "BLOCKED",
    "DATA_BLOCKED",
    "NEEDS_PROFILE",
    "AI_MODEL_BLOCKED",
    "ENGINE_BLOCKED",
    "INVALID_DECISION",
}
BLOCKER_COPY = {
    "DUPLICATE_PENDING_DIRECTION": ("存在同向在途交易", "同一基金已有同向交易等待确认，系统拒绝重复建议。"),
    "EXECUTION_WINDOW_CLOSED": ("交易窗口已关闭", "已超过场外基金当日交易截止时间，下一交易时点必须重新取数。"),
    "INVESTOR_POLICY_NOT_ACTIVE": ("政策尚未生效", "当前政策尚未正式启用，不展示可执行金额。"),
    "POLICY_REVIEW_DUE": ("政策等待复核", "投资政策已到复核时间，新的风险交易暂时停止。"),
    "FREE_CASH_NOT_CONFIRMED": ("自由现金未确认", "需要用户确认同日可用现金后才能计算金额。"),
    "FREE_CASH_SOURCE_NOT_USER_CONFIRMED": ("自由现金未确认", "本轮现金不是用户确认口径，不能生成买入金额。"),
    "MONTHLY_TURNOVER_NOT_PROVIDED": ("换手账本缺失", "无法验证当月交易活动，资金内核已失败关闭。"),
    "PURCHASE_NOT_AVAILABLE": ("基金暂不可申购", "基金侧申购门禁未通过，本轮不生成买入金额。"),
    "REDEMPTION_NOT_AVAILABLE": ("基金暂不可赎回", "基金侧赎回门禁未通过，本轮不生成卖出金额。"),
    "past_cutoff": ("交易窗口已关闭", "已超过场外基金当日交易截止时间，下一交易时点必须重新取数。"),
    "policy_not_active": ("政策尚未生效", "当前政策不是 ACTIVE，不展示可执行金额。"),
    "monthly_turnover_exhausted": ("普通换手额度不足", "普通交易桶已没有足够额度，保护性卖出仍单独审计。"),
    "pending_same_direction": ("存在同向在途交易", "同一基金已有同向交易等待确认，系统拒绝重复建议。"),
    "insufficient_cash": ("自由现金不足", "本轮用户确认的可用现金不足以形成最小有效交易。"),
    "fund_not_buyable": ("基金暂不可申购", "基金侧申购门禁未通过，本轮不生成买入金额。"),
    "fund_not_sellable": ("基金暂不可赎回", "基金侧赎回门禁未通过，本轮不生成卖出金额。"),
    "missing_activity": ("换手账本缺失", "无法验证当月交易活动，资金内核已失败关闭。"),
    "missing_cash": ("自由现金未确认", "需要用户确认同日可用现金后才能计算金额。"),
}
DRIVER_COPY = {
    "SLEEVE_UNDERWEIGHT": "当前袖套低于本轮目标",
    "SLEEVE_OVERWEIGHT": "当前袖套高于本轮目标",
    "FREE_CASH_ABOVE_TARGET": "现金高于战术目标",
    "FREE_CASH_AVAILABLE": "存在本轮已确认自由现金",
    "HARD_DRAWDOWN_LIMIT": "有效回撤越过硬限制",
    "SOFT_DRAWDOWN_FACTORS": "软回撤与不利因子同时确认",
    "RISK_OFF_REENTRY": "保护性降仓后的右侧再入场条件成立",
}
SLEEVE_DIRECTION_COPY = {
    "OVERWEIGHT": ("提高权重候选", "state-strong"),
    "NEUTRAL": ("保持目标", "state-hold"),
    "UNDERWEIGHT": ("降低目标", "state-weak"),
    "EXIT_REVIEW": ("退出复核", "state-weak"),
}
AI_DIRECTION_COPY = {
    "OVERWEIGHT": "建议提高权重",
    "NEUTRAL": "建议维持当前权重",
    "UNDERWEIGHT": "建议降低权重",
    "EXIT_REVIEW": "建议评估退出",
    "UNKNOWN": "尚未形成明确方向",
}
CRITIC_VERDICT_COPY = {
    "PASS": "通过",
    "PASS_WITH_LIMITS": "通过，但仍有约束",
    "FAIL": "未通过",
    "REJECT": "未通过",
}
CONFIDENCE_COPY = {
    "HIGH": "高",
    "MEDIUM": "中",
    "LOW": "低",
    "NONE": "不适用",
}
POLICY_STATUS_COPY = {
    "ACTIVE": "正式启用",
    "SHADOW": "影子观察",
    "CONFIRMED": "已确认，尚未启用",
    "DRAFT": "资料尚未确认",
    "REVIEW_DUE": "等待复核",
    "SUSPENDED": "已暂停",
}
ACTION_COPY = {
    "HOLD": "保持不动",
    "BLOCKED": "暂不执行",
    "DATA_BLOCKED": "数据不足，暂不交易",
    "NEEDS_PROFILE": "投资政策未完成",
    "AI_MODEL_BLOCKED": "研究结论未通过检查",
    "ENGINE_BLOCKED": "金额计算暂不可用",
    "INVALID_DECISION": "结果校验未通过",
    "CONTRIBUTION_REBALANCE": "用新增资金再平衡",
    "STRATEGIC_REBALANCE": "战略再平衡",
    "RISK_REDUCE": "降低风险仓位",
    "TACTICAL_ROTATE": "有限调整方向",
    "REENTRY_AFTER_RISK_OFF": "保护性减仓后分批恢复",
    "FUND_REPLACE": "同类基金替换",
}
HUMAN_TEXT_REPLACEMENTS = (
    (
        "HuahuaDaily|get_batch_fund_profiles|get_quant_strategy_context",
        "花花日记基金资料与量化快照",
    ),
    (
        "HuahuaDaily|get_batch_fund_profiles|official-fund-report",
        "花花日记基金资料与基金定期报告",
    ),
    (
        "HuahuaDaily|get_transaction_ledger|classified-activity",
        "花花日记交易账本与活动分类",
    ),
    (
        "HuahuaDaily|get_quant_strategy_context|investor_policy.v1",
        "花花日记量化快照与个人投资政策",
    ),
    ("HuahuaDaily|get_quant_strategy_context", "花花日记量化快照"),
    ("HuahuaDaily|Eastmoney-search|market", "花花日记与东方财富市场资讯"),
    ("official-company-earnings|Alphabet", "Alphabet 公司财报"),
    ("SEC|Applied-Materials", "美国证监会备案与应用材料公司财报"),
    ("market-report|Alphabet", "Alphabet 市场报道"),
    ("A股指数为broad_downtrend", "A股宽基指数整体处于下行趋势"),
    ("A股指数为broad_uptrend", "A股宽基指数整体处于上行趋势"),
    ("海外指数转为broad_uptrend", "海外宽基指数整体转为上行趋势"),
    ("海外指数转为broad_downtrend", "海外宽基指数整体转为下行趋势"),
    ("quant_strategy_context.v2", "花花日记量化数据"),
    ("STATIC_CASH_PROXY_V1", "静态现金代理法"),
    ("MCP_REPORTED", "基金组合原始回撤口径"),
    ("PASS_WITH_LIMITS", "通过，但仍有约束"),
    ("OVERWEIGHT", "建议提高权重"),
    ("UNDERWEIGHT", "建议降低权重"),
    ("EXIT_REVIEW", "建议评估退出"),
    ("NEUTRAL", "建议维持当前权重"),
    ("BLOCKED", "暂不执行"),
    ("HOLD", "保持不动"),
    ("broad_downtrend", "宽基指数普遍下行"),
    ("broad_uptrend", "宽基指数普遍上行"),
    ("broad_mixed", "宽基指数涨跌分化"),
    ("strong_uptrend", "明显上行"),
    ("strong_downtrend", "明显下行"),
    ("uptrend", "上行趋势"),
    ("downtrend", "下行趋势"),
    ("sideways", "横盘震荡"),
    ("HuahuaDaily MCP", "花花日记数据"),
    ("MA20", "20日均线"),
    ("MA60", "60日均线"),
)
PALETTE = [
    "var(--primary)",
    "var(--info)",
    "var(--accent)",
    "var(--warning)",
    "oklch(0.59 0.12 300)",
    "oklch(0.58 0.11 205)",
    "oklch(0.57 0.12 95)",
]


class ReportValidationError(ValueError):
    """Raised when source artifacts cannot safely produce a report."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ReportValidationError(message)


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ReportValidationError(f"cannot read JSON {path}: {exc}") from exc
    _require(isinstance(value, dict), f"JSON root must be an object: {path}")
    return value


def _num(value: Any, default: float = 0.0) -> float:
    if isinstance(value, bool) or value is None:
        return default
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def _money(value: Any) -> str:
    number = _num(value)
    decimals = 0 if abs(number - round(number)) < 0.005 else 2
    return f"{number:,.{decimals}f}"


def _pct(value: Any, signed: bool = False) -> str:
    number = _num(value)
    prefix = "+" if signed and number > 0 else ""
    return f"{prefix}{number:.2f}%"


def _plain(value: Any) -> str:
    return "" if value is None else str(value).strip()


def _esc(value: Any) -> str:
    return html.escape(_plain(value), quote=True)


def _humanize(value: Any) -> str:
    text = _plain(value)
    for technical, readable in HUMAN_TEXT_REPLACEMENTS:
        text = text.replace(technical, readable)
    return text


def _catalog(decision: dict[str, Any], payload: dict[str, Any]) -> dict[str, str]:
    catalog: dict[str, str] = {}
    holdings = (((payload.get("context") or {}).get("portfolio") or {}).get("holdings") or [])
    for holding in holdings:
        code = _plain(holding.get("code"))
        name = _plain(holding.get("name"))
        if re.fullmatch(r"\d{6}", code) and name:
            catalog[code] = name
    pending = (((payload.get("context") or {}).get("pendingTransactions") or {}).get("items") or [])
    for item in pending:
        code = _plain(item.get("code"))
        name = _plain(item.get("name"))
        if re.fullmatch(r"\d{6}", code) and name and code not in catalog:
            catalog[code] = name
    code = _plain(decision.get("fundCode"))
    name = _plain(decision.get("fundName"))
    if code:
        _require(bool(re.fullmatch(r"\d{6}", code)), "decision fundCode must be six digits")
        _require(bool(name), "decision fundName is required when fundCode is present")
        if code in catalog:
            _require(catalog[code] == name, "decision fundName does not match the current holding catalog")
        else:
            catalog[code] = name
    return catalog


def _fund_label(code: str, catalog: dict[str, str]) -> str:
    _require(code in catalog, f"fund name missing for code {code}")
    return f"{catalog[code]}（{code}）"


def _fund_family_aliases(catalog: dict[str, str]) -> dict[str, list[str]]:
    aliases: dict[str, list[str]] = {}
    for code, name in catalog.items():
        base = re.sub(r"(?:人民币)?[A-Z]$", "", name).strip()
        shorter = re.sub(r"(?:混合|股票|指数|联接|发起式)$", "", base).strip()
        for alias in {base, shorter}:
            if len(alias) >= 5 and alias != name:
                aliases.setdefault(alias, []).append(code)
    return aliases


def _rich(value: Any, catalog: dict[str, str]) -> str:
    """Escape text and expand every known fund name/code into one complete label."""
    text = _humanize(value)
    if not text:
        return ""
    patterns: list[tuple[str, list[str]]] = []
    for code, name in sorted(catalog.items(), key=lambda item: len(item[1]), reverse=True):
        patterns.extend([
            (rf"{re.escape(name)}\s*[（(]\s*{re.escape(code)}\s*[)）]", [code]),
            (re.escape(name), [code]),
            (rf"(?<!\d){re.escape(code)}(?!\d)", [code]),
        ])
    for alias, codes in sorted(_fund_family_aliases(catalog).items(), key=lambda item: len(item[0]), reverse=True):
        patterns.append((re.escape(alias), list(dict.fromkeys(codes))))
    if not patterns:
        return html.escape(text).replace("\n", "<br>")
    combined = re.compile("|".join(f"(?P<p{i}>{pattern})" for i, (pattern, _) in enumerate(patterns)))
    output: list[str] = []
    cursor = 0
    for match in combined.finditer(text):
        output.append(html.escape(text[cursor:match.start()]).replace("\n", "<br>"))
        group = match.lastgroup or ""
        index = int(group[1:])
        codes = patterns[index][1]
        labels = "、".join(_fund_label(code, catalog) for code in codes)
        output.append(f'<span class="fund-ref">{_esc(labels)}</span>')
        cursor = match.end()
    output.append(html.escape(text[cursor:]).replace("\n", "<br>"))
    return "".join(output)


def _validate(decision: dict[str, Any], payload: dict[str, Any], diagnostic: dict[str, Any] | None) -> None:
    _require(decision.get("schemaVersion") == "decision_result.v1", "unsupported decision result schema")
    context = payload.get("context") or {}
    policy = payload.get("policy") or {}
    _require(context.get("schemaVersion") == "quant_strategy_context.v2", "unsupported strategy context schema")
    _require(policy.get("schemaVersion") == "investor_policy.v1", "unsupported policy schema")
    action = _plain(decision.get("action"))
    _require(action in TRADE_ACTIONS | NO_TRADE_ACTIONS, f"unsupported action: {action}")
    mode = _plain(decision.get("executionMode"))
    amount = decision.get("amountCny")
    if mode != "ACTIVE":
        _require(amount is None, "non-ACTIVE report must not expose an amount")
    if action in TRADE_ACTIONS and decision.get("status") == "VALID" and mode == "ACTIVE":
        _require(_num(amount) > 0, "valid ACTIVE trade must contain a positive engine amount")
    if action in NO_TRADE_ACTIONS:
        _require(amount is None, "no-trade action must not contain an amount")
    _require(decision.get("dataAsOf") == context.get("asOfDate"), "decision and context dates differ")
    audit = decision.get("audit") or {}
    _require(bool(audit.get("canonicalOutputHash")), "decision audit hash is required")
    if audit.get("contextHash") and context.get("contextHash"):
        _require(audit["contextHash"] == context["contextHash"], "decision and context hashes differ")
    if audit.get("policyVersion") is not None:
        _require(audit["policyVersion"] == policy.get("policyVersion"), "decision and policy versions differ")
    weights = ((decision.get("allocation") or {}).get("targetWeightsPct") or {})
    if weights:
        _require(abs(sum(_num(value) for value in weights.values()) - 100) <= 0.02, "target weights do not sum to 100")
    if diagnostic is not None:
        _require(diagnostic.get("schemaVersion") == "decision_result.v1", "unsupported diagnostic result schema")
        _require(diagnostic.get("dataAsOf") == decision.get("dataAsOf"), "diagnostic result date differs")


def _trade_verb(decision: dict[str, Any]) -> str:
    action = _plain(decision.get("action"))
    change = _num(decision.get("changeWeightPct"))
    if action in BUY_ACTIONS or change > 0:
        return "加仓"
    if action in {"RISK_REDUCE", "STRATEGIC_REBALANCE"} or change < 0:
        return "减仓"
    return "调整"


def _action_model(decision: dict[str, Any], catalog: dict[str, str]) -> dict[str, str]:
    action = _plain(decision.get("action"))
    mode = _plain(decision.get("executionMode"))
    status = _plain(decision.get("status"))
    code = _plain(decision.get("fundCode"))
    fund_html = _rich(code, catalog) if code else "当前组合"
    fund_plain = _fund_label(code, catalog) if code else "当前组合"
    blockers = decision.get("blockers") or []
    blocker_titles = [BLOCKER_COPY[item][0] for item in blockers if item in BLOCKER_COPY]
    if action in TRADE_ACTIONS and mode == "ACTIVE" and status == "VALID":
        verb = _trade_verb(decision)
        amount = _money(decision.get("amountCny"))
        headline_plain = f"今天{verb}{fund_plain} {amount}元"
        headline_html = f"今天{verb}{fund_html} {amount}元"
        copy = "；".join(DRIVER_COPY.get(item, "资金内核确认的组合约束") for item in (decision.get("drivers") or [])[:3])
        return {
            "headline_plain": headline_plain,
            "headline_html": headline_html,
            "note": f"这是本轮唯一可执行草案，有效期为{_plain(decision.get('validUntil')) or '本轮数据有效期'}，真实交易仍需用户确认。",
            "label": f"正式结论：{verb}",
            "title": f"{verb}{fund_html} {amount}元",
            "copy": _esc(copy or "动作与金额已经通过政策、现金、换手和基金侧门禁。"),
            "tone": "valid",
        }
    if mode != "ACTIVE" and action in TRADE_ACTIONS:
        verb = _trade_verb(decision)
        return {
            "headline_plain": f"影子候选：{verb}{fund_plain}",
            "headline_html": f"影子候选：{verb}{fund_html}",
            "note": "当前不是 ACTIVE，报告只记录方向，不展示或暗示真实交易金额。",
            "label": f"影子结论：仅记录{verb}方向",
            "title": "仅记录方向，不执行交易",
            "copy": "必须先由用户确认并启用政策，再以新鲜数据重新运行资金内核。",
            "tone": "",
        }
    if action == "HOLD":
        return {
            "headline_plain": "今天保持不动",
            "headline_html": "今天保持不动",
            "note": "HOLD 是本轮唯一决定，所有基金均不新增、不减仓。",
            "label": "正式结论：保持不动",
            "title": "所有基金不买、不卖",
            "copy": "组合仍在政策允许范围内，或当前交易不足以改善风险收益结构。",
            "tone": "valid",
        }
    if action == "BLOCKED":
        why = "、".join(blocker_titles) or "执行条件未满足"
        return {
            "headline_plain": "今天暂不执行",
            "headline_html": "今天暂不执行",
            "note": f"正式结果因{why}而阻断，报告不会把研究候选写成交易指令。",
            "label": "正式结论：暂不执行",
            "title": "不提交任何买卖",
            "copy": f"当前没有买卖金额。需要在下一可执行时点重新取数并通过全部门禁。",
            "tone": "",
        }
    labels = {
        "DATA_BLOCKED": "数据不足，今天不交易",
        "NEEDS_PROFILE": "政策未完成，今天不交易",
        "AI_MODEL_BLOCKED": "研究产物不合格，今天不交易",
        "ENGINE_BLOCKED": "资金内核不可用，今天不交易",
        "INVALID_DECISION": "校验失败，今天不交易",
    }
    title = labels.get(action, "今天不交易")
    return {
        "headline_plain": title,
        "headline_html": title,
        "note": "系统已失败关闭，不推测方向或金额。",
        "label": f"正式结论：{ACTION_COPY.get(action, '暂不交易')}",
        "title": "不提交任何买卖",
        "copy": "修复数据、政策、研究或内核问题后，必须重新完整运行。",
        "tone": "danger",
    }


def _header(decision: dict[str, Any], action: dict[str, str]) -> str:
    audit = decision.get("audit") or {}
    mode = _plain(decision.get("executionMode")) or "UNKNOWN"
    badge_class = "badge-active" if mode == "ACTIVE" else "badge-shadow" if mode == "SHADOW" else "badge-blocked"
    mode_label = "正式模式" if mode == "ACTIVE" else "影子模式" if mode == "SHADOW" else "受限模式"
    data_as_of = _plain(decision.get("dataAsOf"))
    return f'''<header class="report-heading">
      <div class="meta-row">
        <span class="badge {badge_class}">{_esc(mode_label)}</span>
        <span>报告模板 v{SKILL_VERSION}</span>
        <span>资金内核 v{_esc(audit.get("engineVersion") or "未知")}</span>
        <span>政策版本 {_esc(audit.get("policyVersion"))}</span>
        <time datetime="{_esc(data_as_of)}">数据截至 {_esc(data_as_of)}</time>
      </div>
      <h1>{action["headline_html"]}</h1>
      <p class="heading-note">{_rich(action["note"], {})}</p>
    </header>'''


def _candidate(decision: dict[str, Any], diagnostic: dict[str, Any] | None, catalog: dict[str, str]) -> str:
    value = diagnostic or decision
    action = _plain(value.get("action"))
    code = _plain(value.get("fundCode"))
    fund = _rich(code, catalog) if code else "当前组合"
    if action == "HOLD":
        title = f"保持{fund}现有仓位" if code else "保持现有仓位"
    elif action in TRADE_ACTIONS:
        title = f"{ACTION_COPY.get(action, '仓位调整')} · {fund}"
    elif action == "BLOCKED" and code:
        title = f"暂不执行 · {fund}"
    else:
        title = f"{ACTION_COPY.get(action, '暂不执行')} · 暂无可执行动作"
    raw_confidence = _plain(value.get("confidence"))
    confidence = CONFIDENCE_COPY.get(raw_confidence, raw_confidence or "未给出")
    return f'''<div class="candidate">
      <small>{"开放窗口诊断" if diagnostic else "本轮研究候选"}</small>
      <strong>{title}</strong>
      <span>置信等级：{_esc(confidence)}。研究候选不拥有金额权限。</span>
    </div>'''


def _action_panel(decision: dict[str, Any], diagnostic: dict[str, Any] | None, action: dict[str, str], catalog: dict[str, str]) -> str:
    return f'''<section class="action-panel" aria-labelledby="action-title">
      <div class="action-inner">
        <div>
          <div class="action-label"><span class="status-dot {action["tone"]}" aria-hidden="true"></span>{_esc(action["label"])}</div>
          <h2 class="action-title" id="action-title">{action["title"]}</h2>
          <p class="action-copy">{action["copy"]}</p>
        </div>
        {_candidate(decision, diagnostic, catalog)}
      </div>
    </section>'''


def _gates(decision: dict[str, Any], payload: dict[str, Any], catalog: dict[str, str]) -> str:
    context = payload.get("context") or {}
    policy = payload.get("policy") or {}
    ai_view = payload.get("aiView") or {}
    gates: list[tuple[str, str, bool]] = []
    for blocker in (decision.get("blockers") or [])[:3]:
        title, detail = BLOCKER_COPY.get(blocker, ("交易条件未满足", "引擎返回未识别门禁，请展开机器审计数据核对。"))
        gates.append((title, detail, False))
    checks = [
        (
            "数据门禁已通过" if context.get("readyForAnalysis") else "数据门禁未通过",
            f"花花日记量化数据已就绪，数据日期{_plain(context.get('asOfDate')) or '未知'}。",
            bool(context.get("readyForAnalysis")),
        ),
        (
            "政策已启用" if policy.get("status") == "ACTIVE" else "政策限制金额",
            f"当前政策状态：{POLICY_STATUS_COPY.get(policy.get('status'), '状态未知')}，版本{_plain(policy.get('policyVersion')) or '未知'}。",
            policy.get("status") == "ACTIVE",
        ),
        (
            "独立反方审查已完成" if ai_view.get("criticVerdict") else "反方审查缺失",
            f"反方审查结论：{CRITIC_VERDICT_COPY.get(ai_view.get('criticVerdict'), '未提供')}。",
            bool(ai_view.get("criticVerdict")),
        ),
    ]
    for check in checks:
        if len(gates) >= 3:
            break
        gates.append(check)
    articles = []
    for index, (title, detail, passed) in enumerate(gates[:3], 1):
        articles.append(f'''<article class="gate {"pass" if passed else ""}">
          <span class="gate-icon" aria-hidden="true">{"✓" if passed else index}</span>
          <strong>{_rich(title, catalog)}</strong>
          <p>{_rich(detail, catalog)}</p>
        </article>''')
    return f'<section class="gate-row" aria-label="决策门禁">{"".join(articles)}</section>'


def _account(decision: dict[str, Any], payload: dict[str, Any]) -> str:
    allocation = decision.get("allocation") or {}
    weights = allocation.get("currentWeightsPct") or {}
    if not weights:
        return ""
    context = payload.get("context") or {}
    portfolio = context.get("portfolio") or {}
    cash = payload.get("cash") or {}
    pending = context.get("pendingTransactions") or {}
    total = _num(allocation.get("totalInvestableAssetsCny"))
    fund_value = _num(portfolio.get("totalMarketValue"))
    cash_value = _num(cash.get("availableCny"))
    pending_buy = _num(pending.get("pendingBuyAmount"))
    positive = [(key, _num(value)) for key, value in weights.items() if _num(value) > 0]
    segments: list[str] = []
    legends: list[str] = []
    sleeve_labels = {item.get("id"): item.get("label") for item in ((payload.get("policy") or {}).get("assetSleeves") or [])}
    for index, (sleeve_id, weight) in enumerate(positive):
        color = PALETTE[index % len(PALETTE)]
        label = sleeve_labels.get(sleeve_id) or sleeve_id
        segments.append(f'<span class="segment" style="width:{max(weight, 0.05):.4f}%;background:{color}" title="{_esc(label)} {_pct(weight)}"></span>')
        legends.append(f'<span class="legend-item"><i class="legend-swatch" style="background:{color}"></i>{_esc(label)} {_pct(weight)}</span>')
    fund_weight = max(0.0, 100 - _num(weights.get("cash")))
    return f'''<section class="section" id="account">
      <div class="section-heading"><h2>账户结构</h2><p>总资产、基金市值、自由现金与在途买入来自同一轮输入；横条使用全账户权重。</p></div>
      <div class="account-summary">
        <article class="account-total">
          <span class="label">总可投资资产</span>
          <div class="value">{_money(total)}<small>元</small></div>
          <dl>
            <dt>已确认自由现金</dt><dd>{_money(cash_value)}元</dd>
            <dt>基金当前市值</dt><dd>{_money(fund_value)}元</dd>
            <dt>待确认买入</dt><dd>{_money(pending_buy)}元</dd>
          </dl>
        </article>
        <article class="allocation-panel">
          <h3>当前资产分布</h3>
          <p>现金占比{_pct(weights.get('cash'))}，基金风险敞口{_pct(fund_weight)}。</p>
          <div class="allocation-track" role="img" aria-label="当前资产分布">{"".join(segments)}</div>
          <div class="allocation-legend">{"".join(legends)}</div>
        </article>
      </div>
    </section>'''


def _allocation(decision: dict[str, Any], payload: dict[str, Any]) -> str:
    allocation = decision.get("allocation") or {}
    current = allocation.get("currentWeightsPct") or {}
    targets = allocation.get("targetWeightsPct") or {}
    sleeves = (payload.get("policy") or {}).get("assetSleeves") or []
    views = {item.get("sleeveId"): item for item in ((payload.get("aiView") or {}).get("sleeveViews") or [])}
    if not sleeves or not targets:
        return ""
    max_scale = max(30.0, max((_num(item.get("maxWeightPct")) for item in sleeves), default=30.0))
    rows: list[str] = []
    for sleeve in sleeves:
        sleeve_id = _plain(sleeve.get("id"))
        strategic = _num(sleeve.get("targetWeightPct"))
        tactical = _num(targets.get(sleeve_id, strategic))
        now = _num(current.get(sleeve_id))
        view = views.get(sleeve_id) or {}
        action_label, state_class = SLEEVE_DIRECTION_COPY.get(view.get("direction"), ("未形成观点", "state-mixed"))
        rows.append(f'''<tr>
          <td>{_esc(sleeve.get("label") or sleeve_id)}</td><td>{_pct(strategic)}</td><td>{_pct(tactical)}</td>
          <td class="weight-cell">
            <div class="weight-labels"><span>当前{_pct(now)}</span><span>目标{_pct(tactical)}</span></div>
            <div class="mini-track" style="--current-width:{min(100, now / max_scale * 100):.2f}%;--target-left:{min(99.5, tactical / max_scale * 100):.2f}%"><span class="mini-current"></span><span class="mini-target"></span></div>
          </td>
          <td><span class="state {state_class}">{_esc(action_label)}</span></td>
        </tr>''')
    return f'''<section class="section" id="allocation">
      <div class="section-heading"><h2>战略目标与战术目标</h2><p>目标权重来自政策与本轮 AI 对各类资产的判断；目标不是第二笔交易建议，最终金额只认资金内核。</p></div>
      <div class="table-wrap"><table>
        <caption>横条表示当前仓位，黑色标记表示本轮战术目标。</caption>
        <thead><tr><th scope="col">资产类别</th><th scope="col">战略目标</th><th scope="col">战术目标</th><th scope="col">当前仓位与目标</th><th scope="col">研究方向</th></tr></thead>
        <tbody>{"".join(rows)}</tbody>
      </table></div>
    </section>'''


def _metric(value: Any, *, signed: bool = False, suffix: str = "%") -> tuple[str, str]:
    if value is None:
        return "数据缺失", ""
    number = _num(value)
    tone = "trend-positive" if signed and number > 0 else "trend-negative" if signed and number < 0 else ""
    prefix = "+" if signed and number > 0 else ""
    return f"{prefix}{number:.2f}{suffix}", tone


def _fund_conclusion(
    holding: dict[str, Any],
    decision: dict[str, Any],
    view: dict[str, Any],
    positive: int,
    adverse: int,
) -> str:
    code = _plain(holding.get("code"))
    if code == _plain(decision.get("fundCode")) and decision.get("action") in TRADE_ACTIONS:
        if decision.get("executionMode") == "ACTIVE" and decision.get("status") == "VALID":
            return f"本轮唯一动作：{_trade_verb(decision)}，金额由资金内核给出"
        return "本轮研究候选，当前不得执行"
    if view.get("direction") == "OVERWEIGHT" and positive >= 3:
        return "保持为下一轮买入候选"
    if view.get("direction") in {"UNDERWEIGHT", "EXIT_REVIEW"} and adverse >= 2:
        return "保持观察，不做逆势加仓"
    return "维持当前仓位，等待下一次复核"


def _funds(decision: dict[str, Any], payload: dict[str, Any], catalog: dict[str, str]) -> str:
    context = payload.get("context") or {}
    holdings = list(((context.get("portfolio") or {}).get("holdings") or []))
    if not holdings:
        return ""
    holdings.sort(key=lambda item: _num(item.get("marketValue")), reverse=True)
    allocation = decision.get("allocation") or {}
    fund_weights = allocation.get("currentFundWeightsPct") or {}
    factor_states = allocation.get("factorStates") or {}
    policy = payload.get("policy") or {}
    sleeve_map = policy.get("fundSleeveMap") or {}
    sleeve_labels = {item.get("id"): item.get("label") for item in (policy.get("assetSleeves") or [])}
    views = {item.get("sleeveId"): item for item in ((payload.get("aiView") or {}).get("sleeveViews") or [])}
    cards: list[str] = []
    for index, holding in enumerate(holdings):
        code = _plain(holding.get("code"))
        _require(code in catalog, f"holding name missing for {code}")
        metrics = holding.get("metrics") or {}
        r20 = metrics.get("r20Pct")
        r60 = metrics.get("r60Pct")
        bias20 = metrics.get("bias20Pct")
        ma20 = metrics.get("ma20")
        ma60 = metrics.get("ma60")
        factors = [
            None if r20 is None else _num(r20) > 0,
            None if r60 is None else _num(r60) > 0,
            None if bias20 is None else _num(bias20) > 0,
            None if ma20 is None or ma60 is None else _num(ma20) > _num(ma60),
        ]
        positive = sum(value is True for value in factors)
        adverse = sum(value is False for value in factors)
        factor_label = f"{positive}项正向" if positive >= adverse else f"{adverse}项不利"
        factor_class = "state-strong" if positive >= 3 else "state-weak" if adverse >= 3 else "state-mixed"
        sleeve_id = sleeve_map.get(code)
        view = views.get(sleeve_id) or {}
        r20_text, r20_tone = _metric(r20, signed=True)
        r60_text, r60_tone = _metric(r60, signed=True)
        bias_text, bias_tone = _metric(bias20, signed=True)
        drawdown_text, _ = _metric(metrics.get("currentDrawdownPct"))
        volatility_text, _ = _metric(metrics.get("annualizedVolatilityPct"))
        ma_text = "数据缺失" if ma20 is None or ma60 is None else "高于" if _num(ma20) > _num(ma60) else "低于"
        ma_tone = "trend-positive" if ma_text == "高于" else "trend-negative" if ma_text == "低于" else ""
        conclusion = _fund_conclusion(holding, decision, view, positive, adverse)
        direction = AI_DIRECTION_COPY.get(_plain(view.get("direction")) or "UNKNOWN", "尚未形成明确方向")
        confidence = _num(view.get("confidence"))
        conditions = view.get("invalidationTriggers") or []
        condition_html = "" if not conditions else "<ul>" + "".join(f"<li>{_rich(item, catalog)}</li>" for item in conditions) + "</ul>"
        cards.append(f'''<details class="fund" {"open" if index == 0 or code == decision.get("fundCode") else ""}>
          <summary><div class="fund-summary">
            <div class="fund-name"><strong>{_esc(_fund_label(code, catalog))}</strong><span>{_esc(sleeve_labels.get(sleeve_id) or sleeve_id or '未映射袖套')}</span></div>
            <div class="fund-stat"><span>市值 / 总资产</span><strong>{_money(holding.get('marketValue'))} / {_pct(fund_weights.get(code))}</strong></div>
            <div class="fund-stat"><span>近20日</span><strong class="{r20_tone}">{r20_text}</strong></div>
            <div><span class="state {factor_class}">{factor_label}</span></div>
            <span class="chevron" aria-hidden="true">⌄</span>
          </div></summary>
          <div class="fund-body">
            <div class="factor-grid">
              <div class="factor"><span>近20日收益</span><b class="{r20_tone}">{r20_text}</b></div>
              <div class="factor"><span>近60日收益</span><b class="{r60_tone}">{r60_text}</b></div>
              <div class="factor"><span>价格相对20日均线</span><b class="{bias_tone}">{bias_text}</b></div>
              <div class="factor"><span>20日均线 / 60日均线</span><b class="{ma_tone}">{ma_text}</b></div>
              <div class="factor"><span>当前回撤</span><b>{drawdown_text}</b></div>
              <div class="factor"><span>年化波动</span><b>{volatility_text}</b></div>
            </div>
            <div class="fund-analysis">
              <strong>{_esc(conclusion)}</strong>
              <p>AI 对该类资产的判断是“{_esc(direction)}”，置信度{confidence:.2f}。这个判断只能缩小交易空间，不能覆盖资金内核金额。</p>
              {condition_html}
            </div>
          </div>
        </details>''')
    return f'''<section class="section detail-section" id="funds">
      <div class="section-heading"><h2>逐只基金诊断</h2><p>点击基金全名与代码展开趋势指标和失效条件；指标只使用同一轮花花日记数据。</p></div>
      <div class="fund-list">{"".join(cards)}</div>
    </section>'''


def _market(payload: dict[str, Any], catalog: dict[str, str]) -> str:
    ai_view = payload.get("aiView") or {}
    evidence = ai_view.get("evidence") or []
    report_date = _plain((payload.get("context") or {}).get("asOfDate"))
    scenarios = ai_view.get("scenarioProbabilities") or {}
    critic_notes = ai_view.get("criticNotes") or []
    unknowns = ai_view.get("unknowns") or []
    if not evidence and not scenarios:
        return ""
    def render_evidence(entry: dict[str, Any]) -> str:
        return f'''<article class="evidence-item">
          <div class="evidence-head"><h3>{_rich(entry.get('title'), catalog)}</h3><span class="evidence-source">{_rich(entry.get('source'), catalog)} · {_esc(entry.get('asOfDate'))}</span></div>
          <p><strong>事实：</strong>{_rich(entry.get('fact'), catalog)}</p>
          <p class="evidence-inference"><strong>AI 推断：</strong>{_rich(entry.get('inference'), catalog)}</p>
        </article>'''
    current_evidence = [item for item in evidence if _plain(item.get("asOfDate")) == report_date]
    background_evidence = [item for item in evidence if _plain(item.get("asOfDate")) != report_date]
    items: list[str] = []
    if current_evidence:
        items.append(f'<h3 class="evidence-group-title">{_esc(report_date)} 当日证据</h3>')
        items.extend(render_evidence(item) for item in current_evidence)
    else:
        items.append('<p class="evidence-empty">本轮没有取得同日可信资讯；以下材料只作为中期背景，不冒充今日新闻。</p>')
    if background_evidence:
        background_items = "".join(render_evidence(item) for item in background_evidence)
        items.append(f'''<details class="evidence-background">
          <summary>展开中期背景证据（{len(background_evidence)}条）</summary>
          <p>这些材料早于报告日期，只用于检验产业逻辑是否仍成立，不代表今日新增消息。</p>
          <div class="evidence-list">{background_items}</div>
        </details>''')
    scenario_labels = {"base": "基准", "bull": "转强", "bear": "走弱", "stress": "压力"}
    scenario_spans: list[str] = []
    scenario_legend: list[str] = []
    for key in ("base", "bull", "bear", "stress"):
        probability = _num(scenarios.get(key))
        if probability <= 0:
            continue
        percent = probability * 100 if probability <= 1 else probability
        scenario_spans.append(f'<span class="scenario-{key}" style="width:{percent:.2f}%">{scenario_labels[key]} {percent:.0f}%</span>')
        scenario_legend.append(f'<span>{scenario_labels[key]}情景 {percent:.0f}%</span>')
    critic_html = ""
    if critic_notes or unknowns:
        critic_html = f'''<article class="evidence-item">
          <div class="evidence-head"><h3>独立反方审查</h3><span class="evidence-source">{_esc(CRITIC_VERDICT_COPY.get(ai_view.get('criticVerdict'), '未给出'))}</span></div>
          <p><strong>不交易基准：</strong>{_rich(ai_view.get('noTradeCase'), catalog)}</p>
          <p><strong>限制：</strong>{"；".join(_rich(item, catalog) for item in critic_notes)}</p>
          <p><strong>未知项：</strong>{"；".join(_rich(item, catalog) for item in unknowns)}</p>
        </article>'''
    return f'''<section class="section detail-section" id="market">
      <div class="section-heading"><h2>市场证据与反证</h2><p>同日资讯与中期背景分层展示；每条记录区分来源事实与 AI 推断，新闻和研究不拥有交易金额权限。</p></div>
      <div class="evidence-list">{"".join(items)}{critic_html}</div>
      <div style="margin-top:26px"><h3 style="margin-bottom:14px">情景分布</h3>
        <div class="scenario-track" role="img" aria-label="本轮AI情景分布">{"".join(scenario_spans)}</div>
        <div class="scenario-legend">{"".join(scenario_legend)}</div>
      </div>
    </section>'''


def _risk(decision: dict[str, Any]) -> str:
    allocation = decision.get("allocation") or {}
    risk = allocation.get("riskControl") or {}
    basis = risk.get("drawdownBasis") or {}
    if not risk and allocation.get("currentDrawdownPct") is None:
        return ""
    fund_drawdown = _num(allocation.get("sourceMcpDrawdownPct", basis.get("sourceDrawdownPct")))
    effective = _num(allocation.get("currentDrawdownPct", basis.get("effectiveDrawdownPct")))
    hard = _num(allocation.get("effectiveMaxDrawdownPct"), 15)
    soft = _num(risk.get("softDrawdownTriggerPct"), min(10, hard))
    scale = max(20.0, fund_drawdown * 1.15, effective * 1.15, hard * 1.25)
    fund_width = min(100, fund_drawdown / scale * 100)
    effective_width = min(100, effective / scale * 100)
    soft_left = min(100, soft / scale * 100)
    hard_left = min(100, hard / scale * 100)
    method = _humanize(_plain(basis.get("method")) or "MCP_REPORTED")
    approximation = "代理估算" if basis.get("isApproximation") else "MCP原始口径"
    return f'''<section class="section detail-section" id="risk">
      <div class="section-heading"><h2>回撤与风险口径</h2><p>风控比较使用政策确认的有效回撤；基金子组合原始值单独保留，不能互相替代。</p></div>
      <div class="risk-comparison">
        <h3>同一账户的两种回撤口径</h3>
        <div class="risk-bars">
          <div class="risk-row"><label>基金子组合回撤</label><div class="risk-track"><span class="risk-fill" style="--risk-width:{fund_width:.2f}%;--risk-color:var(--danger)"></span><i class="risk-threshold" style="left:{soft_left:.2f}%" title="软触发线"></i><i class="risk-threshold" style="left:{hard_left:.2f}%" title="硬限制"></i></div><output>{_pct(fund_drawdown)}</output></div>
          <div class="risk-row"><label>全账户有效回撤</label><div class="risk-track"><span class="risk-fill" style="--risk-width:{effective_width:.2f}%;--risk-color:var(--primary)"></span><i class="risk-threshold" style="left:{soft_left:.2f}%" title="软触发线"></i><i class="risk-threshold" style="left:{hard_left:.2f}%" title="硬限制"></i></div><output>{_pct(effective)}</output></div>
        </div>
        <p class="risk-notes">显示刻度上限{_pct(scale)}；软触发线{_pct(soft)}，硬限制{_pct(hard)}。有效口径：{_esc(method)}（{approximation}）。</p>
      </div>
    </section>'''


def _turnover(payload: dict[str, Any]) -> str:
    activity = payload.get("activity") or {}
    if not activity:
        return ""
    gross = _num(activity.get("grossMonthlyTurnoverUsedPct", activity.get("monthlyTurnoverUsedPct")))
    ordinary = _num(activity.get("ordinaryMonthlyTurnoverUsedPct", activity.get("monthlyTurnoverUsedPct")))
    protective = _num(activity.get("protectiveSellTurnoverPct"))
    reentry = _num(activity.get("riskOffReentryUsedPct"))
    limit = _num(((payload.get("policy") or {}).get("portfolioLimits") or {}).get("maxMonthlyTurnoverPct"), 20)
    scale = max(20.0, math.ceil(max(gross, limit) / 20) * 20)
    gross_width = min(100, gross / scale * 100)
    cap_left = min(100, limit / scale * 100)
    denominator = gross if gross > 0 else 1
    ordinary_share = max(0, ordinary / denominator * 100)
    protective_share = max(0, protective / denominator * 100)
    return f'''<section class="section detail-section" id="turnover">
      <div class="section-heading"><h2>交易活动约束</h2><p>总换手完整审计，普通交易、保护性卖出和风险后再入场分桶展示。</p></div>
      <div class="turnover">
        <div class="turnover-head"><div><h3>本月已确认换手</h3><p style="margin:7px 0 0;color:var(--muted)">数据日期 {_esc(activity.get('asOfDate'))}</p></div><div class="turnover-value">{_pct(gross)}</div></div>
        <div class="turnover-track" role="img" aria-label="本月换手分桶" style="--turnover-width:{gross_width:.2f}%;--ordinary-share:{ordinary_share:.2f}%;--protective-share:{protective_share:.2f}%;--cap-left:{cap_left:.2f}%">
          <div class="turnover-fill"><span class="turnover-ordinary"></span><span class="turnover-protective"></span><span class="turnover-reentry"></span></div><i class="turnover-cap" title="普通换手政策上限"></i>
        </div>
        <div class="turnover-labels"><span>0%</span><span>普通上限 {_pct(limit)}</span><span>显示刻度 {_pct(scale)}</span></div>
        <div class="turnover-legend">
          <span><i style="background:var(--danger)"></i>普通换手 {_pct(ordinary)}</span>
          <span><i style="background:var(--info)"></i>保护性卖出 {_pct(protective)}</span>
          <span><i style="background:var(--primary)"></i>风险后再入场已用 {_pct(reentry)}</span>
        </div>
      </div>
    </section>'''


def _next_steps(decision: dict[str, Any], payload: dict[str, Any], catalog: dict[str, str], action: dict[str, str]) -> str:
    execution = (payload.get("context") or {}).get("execution") or {}
    next_review = _plain(decision.get("nextReviewAt")) or _plain(execution.get("nextTradingDay")) or "下一交易日"
    triggers = decision.get("invalidationTriggers") or []
    if not triggers:
        view = next((item for item in ((payload.get("aiView") or {}).get("sleeveViews") or []) if item.get("sleeveId") == decision.get("scope")), {})
        triggers = view.get("invalidationTriggers") or []
    trigger_text = "；".join(_rich(item, catalog) for item in triggers[:3]) or "市场、持仓、现金或在途状态发生变化。"
    today_body = "本轮不创建交易。" if decision.get("amountCny") is None else "仅在用户确认后，重新取数并复算仍有效时才能发送 App 待确认请求。"
    return f'''<section class="section" id="next">
      <div class="section-heading"><h2>下一步操作路径</h2><p>每一步都需要重新取数；HTML 报告本身不会下单或保存策略快照。</p></div>
      <div class="timeline">
        <article class="timeline-step"><span class="timeline-marker">今</span><h3>{action['headline_html']}</h3><p>{_esc(today_body)}</p></article>
        <article class="timeline-step"><span class="timeline-marker">复</span><h3>{_esc(next_review)}：重新运行完整流水线</h3><p>刷新持仓、在途、交易活动、市场证据和 AI 反方审查，金额不沿用本报告。</p></article>
        <article class="timeline-step"><span class="timeline-marker">失</span><h3>以下条件出现时结论失效</h3><p>{trigger_text}</p></article>
      </div>
    </section>'''


def _relative_href(source: Path, output: Path) -> str:
    relative = os.path.relpath(source.resolve(), output.parent.resolve())
    return quote(relative.replace(os.sep, "/"), safe="/-._")


def _audit(
    decision: dict[str, Any],
    payload: dict[str, Any],
    output: Path,
    result_path: Path,
    input_path: Path,
    diagnostic_path: Path | None,
) -> str:
    audit = decision.get("audit") or {}
    ai_view = payload.get("aiView") or {}
    files = [
        ("正式决策审计", "动作、金额、阻断原因与校验信息 · JSON", result_path),
        ("本次完整输入", "持仓、政策、现金、活动与AI观点 · JSON", input_path),
    ]
    if diagnostic_path is not None:
        files.insert(1, ("开放窗口诊断", "排除指定执行门禁后的诊断结果 · JSON", diagnostic_path))
    links = "".join(
        f'<a class="audit-file" href="{_relative_href(path, output)}"><strong>{_esc(label)}</strong><span>{_esc(description)}</span></a>'
        for label, description, path in files
    )
    return f'''<footer class="audit" id="audit">
      <h2>审计信息</h2>
      <p>报告模板 v{SKILL_VERSION} 只负责展示；动作与金额来自资金内核 v{_esc(audit.get('engineVersion') or '未知')}。AI 模型 {_esc(ai_view.get('modelVersion') or audit.get('aiModelVersion') or '未记录')} 只提供研究观点。</p>
      <details class="audit-details">
        <summary>展开机器审计数据（JSON）</summary>
        <p>这些文件是本次报告使用的结构化数据，不是程序源码。日常阅读无需打开；核对动作、约束或计算输入时再查看。</p>
        <nav class="audit-links" aria-label="机器审计数据文件">{links}</nav>
        <div class="hash">正式结果校验码（SHA-256）：{_esc(audit.get('canonicalOutputHash'))}</div>
      </details>
    </footer>'''


def render_report(
    decision: dict[str, Any],
    payload: dict[str, Any],
    *,
    template: str,
    output_path: Path,
    result_path: Path,
    input_path: Path,
    diagnostic: dict[str, Any] | None = None,
    diagnostic_path: Path | None = None,
) -> str:
    _validate(decision, payload, diagnostic)
    catalog = _catalog(decision, payload)
    action = _action_model(decision, catalog)
    replacements = {
        "@@PAGE_TITLE@@": _esc(f"花花基金仓位决策 · {decision.get('dataAsOf')}"),
        "@@META_DESCRIPTION@@": _esc(f"花花个人基金仓位决策引擎 {decision.get('dataAsOf')} 可审计报告"),
        "@@REPORT_HEADER@@": _header(decision, action),
        "@@ACTION_PANEL@@": _action_panel(decision, diagnostic, action, catalog),
        "@@GATES@@": _gates(decision, payload, catalog),
        "@@ACCOUNT@@": _account(decision, payload),
        "@@ALLOCATION@@": _allocation(decision, payload),
        "@@FUNDS@@": _funds(decision, payload, catalog),
        "@@MARKET@@": _market(payload, catalog),
        "@@RISK@@": _risk(decision),
        "@@TURNOVER@@": _turnover(payload),
        "@@NEXT_STEPS@@": _next_steps(decision, payload, catalog, action),
        "@@AUDIT@@": _audit(decision, payload, output_path, result_path, input_path, diagnostic_path),
    }
    rendered = template
    for token, value in replacements.items():
        _require(token in rendered, f"template token missing: {token}")
        rendered = rendered.replace(token, value)
    leftover = re.findall(r"@@[A-Z_]+@@", rendered)
    _require(not leftover, f"unresolved template tokens: {sorted(set(leftover))}")
    return rendered


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Render a deterministic Hua personal strategy HTML report")
    parser.add_argument("--decision-result", required=True, type=Path)
    parser.add_argument("--decision-input", required=True, type=Path)
    parser.add_argument("--diagnostic-result", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--template", type=Path)
    return parser


def main() -> int:
    args = _parser().parse_args()
    template_path = args.template or Path(__file__).resolve().parents[1] / "assets" / "report-template.html"
    try:
        decision = _load_json(args.decision_result)
        payload = _load_json(args.decision_input)
        diagnostic = _load_json(args.diagnostic_result) if args.diagnostic_result else None
        template = template_path.read_text(encoding="utf-8")
        rendered = render_report(
            decision,
            payload,
            template=template,
            output_path=args.output,
            result_path=args.decision_result,
            input_path=args.decision_input,
            diagnostic=diagnostic,
            diagnostic_path=args.diagnostic_result,
        )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    except (OSError, ReportValidationError) as exc:
        print(f"REPORT_BLOCKED: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({
        "schemaVersion": "fund_position_report_render.v1",
        "status": "OK",
        "output": str(args.output.resolve()),
        "decisionHash": decision.get("audit", {}).get("canonicalOutputHash"),
        "templateVersion": SKILL_VERSION,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
