"""
Self-contained Polymarket client for pmbuysell.skills.
Copied from pmbuysell.polymarket_client, imports only from .local_config.
"""

from __future__ import annotations

import json
import hashlib
import time
from dataclasses import asdict
from decimal import Decimal, getcontext
from pathlib import Path
from typing import Optional, Dict, Any

import requests
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import (
    ApiCreds,
    MarketOrderArgs,
    OrderType,
    BalanceAllowanceParams,
    AssetType,
    OrderArgs,
)
from py_clob_client.exceptions import PolyApiException
from py_clob_client.order_builder.constants import BUY, SELL

from .local_config import CLOB_HOST, CHAIN_ID


getcontext().prec = 28

_SKILLS_DIR = Path(__file__).resolve().parent
_PMBUYSELL_DIR = _SKILLS_DIR.parent
_DATA_DIR = _PMBUYSELL_DIR / "data"


def _api_creds_cache_path(funder: str) -> Path:
    s = (funder or "").strip().lower()
    try:
        _DATA_DIR.mkdir(parents=True, exist_ok=True)
    except Exception:
        return _PMBUYSELL_DIR / "polymarket_api_creds_fallback.json"
    if not s:
        return _DATA_DIR / "polymarket_api_creds_unknown.json"
    tail = s[-8:].replace("0x", "")
    h = hashlib.sha1(s.encode("utf-8")).hexdigest()[:10]
    return _DATA_DIR / f"polymarket_api_creds_{tail}_{h}.json"


def _load_api_creds_cache(cache_path: Path) -> Optional[dict]:
    if not cache_path.exists():
        return None
    try:
        with cache_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def _save_api_creds_cache(cache_path: Path, api_creds: ApiCreds) -> None:
    try:
        with cache_path.open("w", encoding="utf-8") as f:
            json.dump(asdict(api_creds), f, indent=2)
    except Exception:
        pass


def _clear_api_creds_cache(cache_path: Path) -> None:
    try:
        if cache_path.exists():
            cache_path.unlink()
    except Exception:
        pass


def _is_invalid_api_key_error(e: Exception) -> bool:
    if getattr(e, "status_code", None) == 401:
        return True
    msg = str(e).lower()
    err_d = getattr(e, "error_msg", None) or getattr(e, "error_message", None)
    if isinstance(err_d, dict):
        api_err = str(err_d.get("error") or err_d.get("message") or "").lower()
        msg = f"{msg} {api_err}"
    return "unauthorized" in msg or "invalid api key" in msg


def _trade_error_message(e: Exception) -> str:
    msg = str(e).strip()
    msg_l = msg.lower()
    if hasattr(e, "error_msg") and isinstance(getattr(e, "error_msg"), dict):
        err_d = getattr(e, "error_msg")
        api_err = err_d.get("error") or err_d.get("message") or ""
        msg_l = f"{msg_l} {str(api_err).lower()}"
    if "not enough balance" in msg_l or "没有余额" in msg_l or "insufficient" in msg_l:
        return "没有余额了，请充值 USDC 后重试。"
    if "没有持有任何" in msg_l or ("持仓" in msg_l and "0" in msg):
        return "没有对应持仓，无法卖出。"
    if "no match" in msg_l or "无匹配" in msg_l or "no liquidity" in msg_l:
        return "没有对应的交易市场或当前无订单簿，可能市场已结束或暂无对手盘。"
    if "market" in msg_l and ("close" in msg_l or "end" in msg_l or "resolved" in msg_l):
        return "市场已关闭或已结算，无法交易。"
    if "slug" in msg_l and ("not found" in msg_l or "404" in msg_l or "不存在" in msg_l):
        return "没有对应的交易市场（该时段或 slug 不存在）。"
    if "request exception" in msg_l or "timeout" in msg_l or "connection" in msg_l or "network" in msg_l:
        return "网络请求失败，请稍后重试。"
    if "fok" in msg_l and ("fully" in msg_l or "killed" in msg_l or "fill" in msg_l):
        return "订单未完全成交（FOK 已撤销），可稍后重试。"
    if "amount 必须" in msg_l or "action must" in msg_l or "side must" in msg_l:
        return msg if msg else "请求参数错误。"
    return f"交易失败: {msg}" if msg else "交易未成功（重试耗尽）。"


class PolymarketBot:
    """Polymarket 交易客户端，支持 slug + side + amount 市价/限价买卖。"""

    def __init__(
        self,
        private_key: str,
        funder: str,
        host: str | None = None,
        chain_id: int | None = None,
    ):
        self.host = host or CLOB_HOST
        self.chain_id = chain_id or CHAIN_ID
        self.private_key = private_key
        self.funder = funder

    def _new_client(self) -> ClobClient:
        client = ClobClient(
            self.host,
            key=self.private_key,
            chain_id=self.chain_id,
            signature_type=2,
            funder=self.funder,
        )
        cache_path = _api_creds_cache_path(self.funder)
        cached = _load_api_creds_cache(cache_path)
        if cached:
            try:
                creds = ApiCreds(
                    api_key=cached["api_key"],
                    api_secret=cached["api_secret"],
                    api_passphrase=cached["api_passphrase"],
                )
                client.set_api_creds(creds)
            except (KeyError, TypeError):
                cached = None
        if not cached:
            api_creds = client.create_or_derive_api_creds()
            client.set_api_creds(api_creds)
            _save_api_creds_cache(cache_path, api_creds)
        return client

    def _get_usdc_balance(self, client: ClobClient) -> float:
        params = BalanceAllowanceParams(asset_type=AssetType.COLLATERAL)
        if hasattr(client, "get_balance_allowance"):
            bal = client.get_balance_allowance(params)["balance"]
        else:
            bal = client.getBalanceAllowance(params)["balance"]
        return float(Decimal(bal) / Decimal(1_000_000))

    def get_balance(self, slug: str | None = None) -> Dict[str, Any]:
        client = self._new_client()
        usdc = self._get_usdc_balance(client)
        result: Dict[str, Any] = {"usdc": usdc}
        if slug and slug.strip():
            try:
                data = self._get_market_data(slug)
                token_ids = data.get("clobTokenIds") or []
                if len(token_ids) >= 2:
                    up_bal = self._get_conditional_balance(client, token_ids[0])
                    down_bal = self._get_conditional_balance(client, token_ids[1])
                    result["conditional"] = {"up": up_bal, "down": down_bal, "slug": slug}
            except Exception:
                result["conditional"] = None
        return result

    @staticmethod
    def _get_market_data(slug: str) -> dict:
        url = f"https://gamma-api.polymarket.com/markets/slug/{slug}"
        headers = {"Accept": "application/json", "User-Agent": "Mozilla/5.0 (compatible; PmBuysell/1.0;)"}
        r = requests.get(url, headers=headers, timeout=5)
        r.raise_for_status()
        d = r.json()
        return {
            "outcomes": json.loads(d.get("outcomes", "[]")),
            "outcomePrices": json.loads(d.get("outcomePrices", "[]")),
            "clobTokenIds": json.loads(d.get("clobTokenIds", "[]")),
        }

    def _get_conditional_balance(self, client: ClobClient, token_id: str) -> float:
        params = BalanceAllowanceParams(asset_type=AssetType.CONDITIONAL, token_id=token_id)
        if hasattr(client, "get_balance_allowance"):
            balance_data = client.get_balance_allowance(params)
        else:
            balance_data = client.getBalanceAllowance(params)
        return float(Decimal(balance_data["balance"]) / Decimal(1_000_000))

    def trade_once(
        self,
        action: str,
        slug: str,
        side: str,
        amount: float,
        order_type: str | None = None,
        limit_price: float | None = None,
    ):
        if not slug:
            raise ValueError("slug 不能为空")
        if side not in ("up", "down"):
            raise ValueError("side must be 'up' or 'down'")

        data = self._get_market_data(slug)
        token_id = data["clobTokenIds"][0] if side == "up" else data["clobTokenIds"][1]
        client = self._new_client()
        balance = self._get_usdc_balance(client)

        if order_type == "limit" and limit_price is not None:
            price = float(limit_price)
            if price <= 0:
                raise ValueError("limit_price must be > 0 for limit order")
            if action == "buy":
                if amount <= 0:
                    amount = int(balance * 0.3)
                size = float(Decimal(str(amount)) / Decimal(str(price)))
                order_args = OrderArgs(token_id=token_id, price=price, size=size, side=BUY)
            elif action == "sell":
                balance_conditional = self._get_conditional_balance(client, token_id)
                if balance_conditional <= 0:
                    raise RuntimeError(f"没有持有任何 {token_id}，当前持仓为 {balance_conditional}")
                size = balance_conditional if (amount <= 0 or amount >= 1000) else min(float(amount), balance_conditional)
                order_args = OrderArgs(token_id=token_id, price=price, size=size, side=SELL)
            else:
                raise ValueError("action must be 'buy' or 'sell'")
            signed = client.create_order(order_args)
            resp = client.post_order(signed, OrderType.GTC)
        else:
            if action == "buy":
                if amount <= 0:
                    amount = int(balance * 0.3)
                order = MarketOrderArgs(token_id=token_id, amount=amount, side=BUY, order_type=OrderType.FOK)
                signed = client.create_market_order(order)
                resp = client.post_order(signed, OrderType.FOK)
            elif action == "sell":
                balance_conditional = self._get_conditional_balance(client, token_id)
                if balance_conditional <= 0:
                    raise RuntimeError(f"没有持有任何 {token_id}，当前持仓为 {balance_conditional}")
                if amount <= 0 or amount >= 1000:
                    amount = balance_conditional
                order = MarketOrderArgs(token_id=token_id, amount=amount, side=SELL, order_type=OrderType.FOK)
                signed = client.create_market_order(order)
                resp = client.post_order(signed, OrderType.FOK)
            else:
                raise ValueError("action must be 'buy' or 'sell'")

        try:
            usdc_balance = self._get_usdc_balance(client)
            if action == "buy" and order_type != "limit":
                usdc_balance = max(0.0, usdc_balance - amount)
        except Exception:
            usdc_balance = None
        return resp, usdc_balance

    def trade_with_retry(
        self,
        action: str,
        slug: str,
        side: str,
        amount: float,
        order_type: str | None = None,
        limit_price: float | None = None,
        max_retries: int = 5,
        retry_delay: float = 2.0,
    ) -> Dict[str, Any]:
        last_error_message = None
        for i in range(1, max_retries + 1):
            try:
                resp, usdc_balance = self.trade_once(
                    action=action, slug=slug, side=side, amount=amount,
                    order_type=order_type, limit_price=limit_price,
                )
                if order_type == "limit":
                    order_id = resp.get("orderID") or resp.get("orderId") or resp.get("id")
                    if not order_id or not str(order_id).strip():
                        return {"ok": False, "usdc_balance": usdc_balance, "message": "限价单未成功：Polymarket 未返回有效 orderID", "order_message": None}
                    order_message = {"action": action, "side": side, "amount": amount, "order_type": "limit", "limit_price": limit_price, "slug": slug, "order_id": order_id, "orderId": order_id}
                else:
                    usdc_amount = resp.get("makingAmount") if action == "buy" else resp.get("takingAmount")
                    token_amount = resp.get("takingAmount") if action == "buy" else resp.get("makingAmount")
                    trade_price = float(usdc_amount) / float(token_amount) if token_amount and float(token_amount) > 0 else None
                    order_message = {"action": action, "side": side, "amount": amount, "slug": slug, "usdc_amount": usdc_amount, "token_amount": token_amount, "trade_price": round(trade_price, 4) if trade_price is not None else None}
                return {"ok": True, "usdc_balance": usdc_balance, "message": None, "order_message": order_message}
            except Exception as e:
                last_error_message = _trade_error_message(e)
                if _is_invalid_api_key_error(e):
                    _clear_api_creds_cache(_api_creds_cache_path(self.funder))
                msg_l = str(e).lower()
                if isinstance(e, PolyApiException) and isinstance(getattr(e, "error_msg", None), dict):
                    msg_l = f"{msg_l} {str(e.error_msg.get('error') or e.error_msg.get('message') or '').lower()}"
                is_transient = "request exception" in msg_l or "timeout" in msg_l or "connection" in msg_l or "network" in msg_l
                is_transient = is_transient or ("fok" in msg_l and ("fully filled" in msg_l or "killed" in msg_l or "fully" in msg_l or "fill" in msg_l))
                is_transient = is_transient or _is_invalid_api_key_error(e)
                if not is_transient or i >= max_retries:
                    break
                time.sleep(retry_delay)
        return {"ok": False, "usdc_balance": None, "message": last_error_message}
