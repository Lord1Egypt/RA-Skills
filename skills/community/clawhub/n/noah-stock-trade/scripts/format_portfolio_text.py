#!/usr/bin/env python3
from typing import Any, Dict, List


def _normalize_code(code):
    if code is None:
        return '-'
    s = str(code)
    if s.startswith('HK.HK-'):
        return 'HK.' + s.split('HK.HK-', 1)[1]
    if s.startswith('US.US-'):
        return 'US.' + s.split('US.US-', 1)[1]
    return s


def _safe(v):
    return '-' if v is None else v


def _num(v):
    if v is None:
        return '-'
    try:
        fv = float(v)
        if abs(fv) >= 1000:
            return f'{fv:,.2f}'.rstrip('0').rstrip('.')
        return f'{fv:.2f}'.rstrip('0').rstrip('.')
    except Exception:
        return v


def format_account_info(summary: Dict[str, Any]) -> str:
    return '\n'.join([
        '账户信息：',
        f'账户类型：{_safe(summary.get("account_type"))}',
        f'资金账户：{_safe(summary.get("fund_account"))}',
        f'分组号：{_safe(summary.get("group_no"))}',
        f'交易模式：{_safe(summary.get("trade_mode"))}',
        f'股票账户：{"已开通" if summary.get("stock_account_open") else "未开通"}',
        f'资金账户：{"已开通" if summary.get("fund_account_open") else "未开通"}',
    ])


def format_positions(summary: Dict[str, Any]) -> str:
    lines = [f'持仓概览：共 {summary.get("count", 0)} 条']
    for i, x in enumerate(summary.get('items', []), 1):
        lines.append(
            f'{i}. {x.get("name") or "-"}（{_normalize_code(x.get("code"))}）｜持仓{_num(x.get("quantity"))}｜可卖{_num(x.get("available_quantity"))}｜现价{_num(x.get("current_price"))}｜市值{_num(x.get("market_value"))}｜浮盈亏{_num(x.get("pnl"))}'
        )
    if summary.get('truncated'):
        lines.append('说明：仅展示前 10 条持仓记录。')
    return '\n'.join(lines)


def format_sec_asset(summary: Dict[str, Any]) -> str:
    lines = [f'证券资产：共 {summary.get("count", 0)} 条']
    for i, x in enumerate(summary.get('items', []), 1):
        lines.append(
            f'{i}. 币种{_safe(x.get("money_type_desc") or x.get("money_type"))}｜总资产{_num(x.get("asset_value"))}｜证券市值{_num(x.get("market_value"))}｜现金{_num(x.get("cash_value"))}｜冻结{_num(x.get("frozen_value"))}'
        )
    return '\n'.join(lines)


def format_capital_flow(summary: Dict[str, Any]) -> str:
    lines = [f'资金流水：最近 {summary.get("count", 0)} 条']
    for i, x in enumerate(summary.get('items', []), 1):
        lines.append(
            f'{i}. {x.get("curr_datetime") or "-"}｜{x.get("stock_name") or "-"}（{_normalize_code(x.get("stock_code"))}）｜{x.get("fund_direction_desc") or "-"}｜金额{_num(x.get("occur_balance"))}｜余额{_num(x.get("post_balance"))}｜{x.get("biz_type_desc") or "-"}｜{x.get("biz_flag_desc") or "-"}'
        )
    if summary.get('truncated'):
        lines.append('说明：仅展示前 10 条资金流水记录。')
    return '\n'.join(lines)
