#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================
# ⚠️ 本文件是「京东黄金 (jdgold)」JoyCode Skill 的组成脚本。
# 执行任何脚本前，必须先阅读 Skill 根目录下的 SKILL.md，
# 严格遵循其中的执行契约、安全脱敏铁律与回复规范，
# 请勿脱离 SKILL.md 指引单独运行本脚本。
# ============================================================
"""黄金持仓与收益：渲染与意图解析（核心逻辑）。统一入口见 holdings_entry.py。"""
import argparse
import json
import re
import sys
import urllib.error
from typing import List, Optional

import jos
import bff_client

VIEW_MODE = "当前账号"  # Agent 内部标识，勿写入用户可见 stdout

HOLDINGS_PATTERNS = [
    r"查询持仓",
    r"持仓查询",
    r"我的(?:黄金)?持仓",
    r"黄金持仓",
    r"积存金持仓",
    r"查(?:一下|下)?持仓",
]
INCOME_PATTERNS = [
    r"查询收益",
    r"收益查询",
    r"我的(?:黄金)?收益",
    r"黄金收益",
    r"积存金收益",
    r"查(?:一下|下)?收益",
]
COMBINED_PATTERNS = [
    r"持仓和收益",
    r"持仓与收益",
    r"持仓.*收益",
    r"收益.*持仓",
    r"分析.*持仓",
    r"持仓.*分析",
    r"诊断.*持仓",
    r"持仓.*诊断",
]
CURRENT_ACCOUNT_PATTERNS = [
    r"我(?:的)?",
    r"当前账号",
    r"当前账户",
    r"本账号",
    r"登录账号",
    r"登录账户",
]
PIN_PATTERN = re.compile(r"\bjd_[0-9a-f]{8,}\b", re.I)
JRID_PATTERN = re.compile(r"\bjrid[\s=:：]*([A-Za-z0-9_\-]+)", re.I)
PIN_LABEL_PATTERN = re.compile(r"(?:pin|PIN)[\s=:：]*([A-Za-z0-9_\-]+)", re.I)


def parse_intent(text: str) -> Optional[str]:
    text = (text or "").strip()
    if not text:
        return None
    for pat in COMBINED_PATTERNS:
        if re.search(pat, text):
            return "both"
    has_holdings = any(re.search(p, text) for p in HOLDINGS_PATTERNS) or bool(re.search(r"持仓", text))
    has_income = any(re.search(p, text) for p in INCOME_PATTERNS) or bool(re.search(r"收益", text))
    if has_holdings and has_income:
        return "both"
    if has_holdings:
        return "holdings"
    if has_income:
        return "income"
    return None


def is_current_account_query(text: str) -> bool:
    return any(re.search(p, text or "") for p in CURRENT_ACCOUNT_PATTERNS)


def extract_specified_accounts(text: str) -> List[str]:
    text = text or ""
    found = list(PIN_PATTERN.findall(text))
    found.extend(JRID_PATTERN.findall(text))
    found.extend(PIN_LABEL_PATTERN.findall(text))
    seen, out = set(), []
    for item in found:
        key = item.lower()
        if key not in seen:
            seen.add(key)
            out.append(item)
    return out


def _fmt_num(v, digits=2):
    if v is None:
        return "—"
    try:
        n = float(v)
        if n == int(n) and abs(n) >= 1:
            return f"{n:,.2f}"
        return f"{n:,.{digits}f}".rstrip("0").rstrip(".")
    except (TypeError, ValueError):
        return str(v)


def _fmt_income(v, emoji=False):
    """收益格式化：正负仅用数值前的 +/- 号表达，不加 🔺🔻➖ 等方向符号。

    emoji 参数保留仅为兼容旧调用，始终不输出方向符号。
    """
    if v is None:
        return "—"
    n = float(v)
    sign = "+" if n > 0 else ""
    return f"{sign}{n:,.2f}"




def _active_items(holding_list):
    """有实际持仓的银行（totalGram > 0）。用于持仓维度。"""
    return [h for h in (holding_list or []) if float(h.get("totalGram") or 0) > 0]


def _has_income(item) -> bool:
    try:
        return abs(float(item.get("totalIncome") or 0)) > 0
    except (TypeError, ValueError):
        return False


def _display_items(holding_list, intent: str):
    """按意图筛选要展示的银行。

    holdings / income / both 统一口径：有持仓（totalGram > 0）或有累计卖出收益
    （totalIncome ≠ 0）的银行都要展示——不得因无持仓而遗漏已清仓但仍有累计
    收益的银行（如工商银行持仓 0 但收益 +77.63）。
    """
    items = holding_list or []
    return [
        h
        for h in items
        if float(h.get("totalGram") or 0) > 0 or _has_income(h)
    ]


def _bank_realtime_price(bank_code):
    """取该银行积存金实时金价（元/克）与交易时间。失败返回 (None, None)。

    注意：持仓价值必须按各家积存金银行自己的实时金价计算，不能用京东24h金价。
    """
    try:
        import query_price_jhub
        quote = query_price_jhub.fetch_price_by_bank((bank_code or "").upper())
        if not quote or not isinstance(quote, dict):
            return None, None
        last = quote.get("lastPrice")
        price = float(last) if last is not None else None
        ts = quote.get("tradeDateTime")
        # 后端偶尔返回无效占位值（如 "{}"、"null"、空串），需过滤，避免展示成
        # "数据更新时间：{}" 这类脏数据。
        if not isinstance(ts, str) or ts.strip() in ("", "{}", "[]", "null", "None"):
            ts = None
        return price, ts
    except Exception:
        return None, None


def render_holdings(data: dict, intent: str = "both", session_pin: Optional[str] = None) -> str:
    holding_list = data.get("holdingList") or []
    active = _active_items(holding_list)              # 有持仓（持仓价值/实时金价用）
    display = _display_items(holding_list, intent)    # 按意图展示的银行集合
    total_gram = float(data.get("totalGramAll") or 0)
    # 收益汇总须包含所有有收益的银行（含已清仓的），不能只按有持仓的银行求和
    income_items = display
    total_income = sum(float(h.get("totalIncome") or 0) for h in income_items)
    avg_cost = data.get("avgCostPrice")

    # 预取各银行实时金价，用于计算持仓价值（按各行积存金金价，非京东24h金价）
    # 纯收益视角不涉及持仓价值，跳过实时价预取以省开销并避免无关时间戳。
    bank_price = {}          # 各行真实取到的实时价（None 表示取不到）
    latest_time = None
    fallback_price = None     # 兜底价：用某一家已取到的实时价估算取不到价的银行
    fallback_bank = None      # 兜底价来源银行名（用于提示）
    used_fallback = False     # 是否有银行用了兜底价
    total_value = 0.0
    has_value = False
    total_cost = 0.0          # 持仓成本合计（各行 克重 × 成本均价），用于浮盈浮亏
    has_cost = False
    if intent in ("holdings", "both"):
        for item in active:
            bc = item.get("bankCode")
            if bc and bc not in bank_price:
                price, ts = _bank_realtime_price(bc)
                bank_price[bc] = price
                if isinstance(ts, str) and ts and (latest_time is None or ts > latest_time):
                    latest_time = ts
                # 记录第一个成功取到的实时价作为兜底价
                if price is not None and fallback_price is None:
                    fallback_price = price
                    fallback_bank = item.get("bankName") or bc
        for item in active:
            p = bank_price.get(item.get("bankCode"))
            eff = p if p is not None else fallback_price
            if eff is not None:
                gram = float(item.get("totalGram") or 0)
                total_value += gram * eff
                has_value = True
                if p is None:
                    used_fallback = True
                # 同口径累加持仓成本：仅统计已计入市值的行，保证浮盈浮亏可比
                cost = item.get("avgCostPrice")
                if cost is not None:
                    total_cost += gram * float(cost)
                    has_cost = True

    # ============ 标题 ============
    if intent == "income":
        title = "## 📈 我的黄金收益"
    elif intent == "holdings":
        title = "## 💰 我的黄金持仓"
    else:
        title = "## 💰 我的黄金持仓与收益"
    lines = [title, ""]

    # ============ 汇总表格 ============
    lines.append("### 📊 汇总")
    lines.append("")
    sum_cols = []
    sum_vals = []
    if intent in ("holdings", "both"):
        sum_cols.append("⚖️ 总持仓(克)")
        sum_vals.append(_fmt_num(total_gram, 4))
        if avg_cost is not None:
            sum_cols.append("💵 平均成本价(元/克)")
            sum_vals.append(_fmt_num(avg_cost))
        if has_value:
            val_label = _fmt_num(total_value)
            if used_fallback:
                val_label += "*"
            sum_cols.append("💎 当前持仓价值(元)")
            sum_vals.append(val_label)
            # 当前持仓收益 = 持仓市值 − 持仓成本（同口径，未实现盈亏）
            if has_cost:
                pnl = total_value - total_cost
                pnl_label = _fmt_income(pnl, emoji=True)
                if total_cost > 0:
                    pnl_label += f"（{_fmt_income(pnl / total_cost * 100)}%）"
                if used_fallback:
                    pnl_label += "*"
                sum_cols.append("📈 当前持仓收益(元)")
                sum_vals.append(pnl_label)
    # 累计卖出收益列：holdings/both/income 均展示（总持仓也需含累计卖出收益）
    sum_cols.append("💰 累计卖出收益(元)")
    sum_vals.append(_fmt_income(total_income))
    lines.append("| " + " | ".join(sum_cols) + " |")
    lines.append("| " + " | ".join(["---:"] * len(sum_cols)) + " |")
    lines.append("| " + " | ".join(sum_vals) + " |")

    if not display:
        lines.append("")
        lines.append("> ℹ️ 您当前暂无积存金持仓。")
        return "\n".join(lines)

    # ============ 各银行明细表格 ============
    lines.append("")
    lines.append("### 🏦 各银行明细")
    lines.append("")
    if intent == "income":
        header = "| 🏦 银行 | 💰 累计卖出收益(元) |"
        divider = "| --- | ---: |"
        lines.append(header)
        lines.append(divider)
        for item in display:
            name = item.get("bankName") or item.get("bankCode") or "未知银行"
            inc = item.get("totalIncome")
            lines.append(f"| {name} | {_fmt_income(inc)} |")
    else:
        # holdings / both：持仓维度多列，两者均含「当前持仓收益」与「累计卖出收益」
        cols = ["🏦 银行", "⚖️ 持仓(克)", "💵 成本均价(元/克)", "📈 实时金价(元/克)", "💎 持仓价值(元)", "📊 当前持仓收益(元)", "💰 累计卖出收益(元)"]
        lines.append("| " + " | ".join(cols) + " |")
        lines.append("| " + " | ".join(["---"] + ["---:"] * (len(cols) - 1)) + " |")
        for item in display:
            name = item.get("bankName") or item.get("bankCode") or "未知银行"
            gram = item.get("totalGram")
            cost = item.get("avgCostPrice")
            gram_val = float(gram or 0)
            # 已清仓（持仓为 0）的银行：持仓相关列无意义，统一显示占位符 —，
            # 仅保留累计卖出收益列，避免展示 0*、-0.00* 这类无意义估算值。
            if gram_val <= 0:
                row = [name, _fmt_num(gram, 4), "—", "—", "—", "—"]
                inc = item.get("totalIncome")
                row.append(f"{_fmt_income(inc)}")
                lines.append("| " + " | ".join(row) + " |")
                continue
            p = bank_price.get(item.get("bankCode"))
            eff = p if p is not None else fallback_price
            # 取不到自家实时价时，用兜底价估算并以 * 标注
            if p is not None:
                price_cell = _fmt_num(p)
                val = _fmt_num(gram_val * p)
            elif eff is not None:
                price_cell = f"{_fmt_num(eff)}*"
                val = f"{_fmt_num(gram_val * eff)}*"
            else:
                price_cell = "—"
                val = "—"
            # 当前持仓收益 = 该行克重 ×（实时价 − 成本均价），同口径未实现盈亏；估算时标 *
            if eff is not None and cost is not None:
                pnl_cell = _fmt_income(gram_val * (eff - float(cost)))
                if p is None:
                    pnl_cell += "*"
            else:
                pnl_cell = "—"
            row = [
                name,
                _fmt_num(gram, 4),
                _fmt_num(cost) if cost is not None else "—",
                price_cell,
                val,
                pnl_cell,
            ]
            inc = item.get("totalIncome")
            row.append(f"{_fmt_income(inc)}")
            lines.append("| " + " | ".join(row) + " |")

    out = "\n".join(lines).rstrip()
    # 部分银行实时金价暂不可用时，用已取到的某家实时价（如中信）兜底估算其��仓价值，
    # 并以 * 标注、附注说明，避免用户误以为只统计了取到实时价的那家。
    if intent in ("holdings", "both") and used_fallback and fallback_bank:
        out += (
            f"\n\n> ⚠️ 部分银行实时金价暂不可用，标 * 的实时金价与持仓价值"
            f"均按「{fallback_bank}」的实时金价估算，仅供参考。"
        )
    # 仅在展示了持仓价值（holdings/both 且取到实时价）时附上数据更新时间；
    # 纯收益视角不涉及实时金价，不显示该行。latest_time 必须是有效字符串。
    if intent in ("holdings", "both") and has_value and isinstance(latest_time, str) and latest_time:
        out += f"\n\n> 🕒 数据更新时间：{latest_time}"
    return out


def main(argv=None):
    """兼容旧调用，转发至 holdings_entry.py。"""
    import holdings_entry
    p = argparse.ArgumentParser(description="查询黄金积存金持仓与收益（转发至 holdings_entry.py）")
    p.add_argument("--parse", "-p", metavar="TEXT")
    p.add_argument("--json", action="store_true")
    p.add_argument("--intent", choices=("holdings", "income", "both"), default="both")
    p.add_argument("--wait-login", action="store_true")
    p.add_argument("--claw", help="上报客户端 claw 类型（如 codex、openclaw）")
    args = p.parse_args(argv)
    bff_client.set_claw(args.claw)
    if not args.parse:
        p.print_help()
        return 1
    return holdings_entry.run(
        args.parse, args.intent, wait_login=args.wait_login, json_out=args.json, resume=False
    )


if __name__ == "__main__":
    sys.exit(main())
