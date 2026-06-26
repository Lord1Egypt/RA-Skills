"""
Self-contained multi-account trade/balance for pmbuysell.skills.
Imports only from .local_config and .polymarket_client.
"""

from __future__ import annotations

import time
from typing import Any, Dict

from .local_config import (
    get_account,
    get_auto_buy_max_amount,
    get_auto_buy_min_amount,
    get_balance_cache_ttl_sec,
)
from .polymarket_client import PolymarketBot


_USDC_BALANCE_CACHE: dict[str, tuple[float, float]] = {}


def _get_usdc_balance_cached(account_id: str, bot: PolymarketBot) -> float:
    ttl = get_balance_cache_ttl_sec(default=10)
    key = (account_id or "").strip().upper()
    now = time.time()
    if ttl > 0:
        cached = _USDC_BALANCE_CACHE.get(key)
        if cached:
            bal, ts = cached
            if now - ts <= ttl:
                return float(bal)
    bal = float(bot.get_balance().get("usdc") or 0.0)
    _USDC_BALANCE_CACHE[key] = (bal, now)
    return bal


def _auto_buy_amount_from_balance(usdc_balance: float) -> float:
    min_amt = float(get_auto_buy_min_amount(default=1.0))
    max_amt = float(get_auto_buy_max_amount(default=50.0))
    bal = float(usdc_balance)
    if bal < 3.0:
        base = 1.0
    else:
        stake = int(bal // 3)
        if stake <= 0:
            return 0.0
        base = float(stake)
    amt = max(min_amt, base)
    if max_amt > 0:
        amt = min(amt, max_amt)
    amt = min(amt, bal)
    return round(max(0.0, amt), 2)


def trade_for_account(
    account_id: str,
    action: str,
    side: str = "down",
    amount: float = 0.0,
    order_type: str | None = None,
    limit_price: float | None = None,
    slug: str | None = None,
) -> Dict[str, Any]:
    account = get_account(account_id)
    if not account:
        return {
            "ok": False,
            "usdc_balance": None,
            "message": f"未找到账号配置：{account_id}。请检查环境变量 PM_ACCOUNTS_JSON 或 PM_ACCOUNT_IDS。",
            "order_message": None,
        }

    bot = PolymarketBot(private_key=account["private_key"], funder=account["funder"])
    requested_amount = float(amount) if amount is not None else 0.0
    auto_amount: float | None = None
    if action == "buy" and float(amount) == 0.0:
        usdc_balance = _get_usdc_balance_cached(account_id=account_id, bot=bot)
        auto_amount = _auto_buy_amount_from_balance(usdc_balance)
        if auto_amount <= 0:
            return {
                "ok": False,
                "usdc_balance": usdc_balance,
                "message": "自动下注失败：余额不足（至少需要 1U）",
                "order_message": None,
                "requested_amount": requested_amount,
                "auto_amount": auto_amount,
            }
        amount = auto_amount

    result = bot.trade_with_retry(
        action=action,
        slug=slug if slug is not None else "",
        side=side,
        amount=amount,
        order_type=order_type,
        limit_price=limit_price,
    )
    # 交易成功则变更余额缓存
    if result.get("ok") and result.get("usdc_balance") is not None:
        key = (account_id or "").strip().upper()
        _USDC_BALANCE_CACHE[key] = (float(result["usdc_balance"]), time.time())
    if result.get("ok") and not result.get("message"):
        result["message"] = "交易请求已提交"
    if "order_message" not in result:
        result["order_message"] = None
    result["requested_amount"] = requested_amount
    if auto_amount is not None:
        result["auto_amount"] = auto_amount
    return result


def market_buy(account_id: str, slug: str, side: str, amount: float) -> Dict[str, Any]:
    return trade_for_account(account_id=account_id, action="buy", side=side, amount=amount, slug=slug)


def market_sell(account_id: str, slug: str, side: str, amount: float) -> Dict[str, Any]:
    return trade_for_account(account_id=account_id, action="sell", side=side, amount=amount, slug=slug)


def get_balance(account_id: str, slug: str | None = None) -> Dict[str, Any]:
    account = get_account(account_id)
    if not account:
        return {
            "ok": False,
            "usdc": None,
            "conditional": None,
            "message": f"未找到账号配置：{account_id}。请检查环境变量 PM_ACCOUNTS_JSON 或 PM_ACCOUNT_IDS。",
        }
    try:
        bot = PolymarketBot(private_key=account["private_key"], funder=account["funder"])
        result = bot.get_balance(slug=slug)
        return {"ok": True, "usdc": result["usdc"], "conditional": result.get("conditional"), "message": None}
    except Exception as e:
        return {"ok": False, "usdc": None, "conditional": None, "message": str(e)}
