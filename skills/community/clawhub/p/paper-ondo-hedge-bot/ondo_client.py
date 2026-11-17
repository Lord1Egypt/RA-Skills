"""
ONDO Perps 客户端
- HMAC-SHA256 签名交易请求
- 市价开/平仓
- 持仓与余额查询

注意：如果你已有可用的 ONDO 交易程序，可以直接复用其中的签名逻辑。
此处的签名实现基于 ONDO Perps 标准 API 模式，如遇签名错误请根据实际 API 调整 _sign 方法。
"""
from __future__ import annotations

import hashlib
import hmac
import json
import time
from dataclasses import dataclass
from typing import Any, Optional

import requests


ONDO_BASE_URL = "https://api.ondoperps.xyz"


@dataclass
class OndoConfig:
    key_id: str        # ondoKeyId_xxx
    api_secret: str    # ondoApiSecret_xxx
    base_url: str = ONDO_BASE_URL


class OndoClient:
    def __init__(self, config: OndoConfig):
        self.config = config
        self._http = requests.Session()
        self._http.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "paper-hedge-bot",
        })

    # ── 签名 ────────────────────────────────────────────────
    def _sign(self, method: str, path: str, body: Optional[dict] = None, params: Optional[dict] = None) -> dict:
        """
        生成 ONDO API 签名头。
        标准模式：HMAC-SHA256(secret, timestamp + method + path + body)
        如实际 API 签名格式不同，请修改此方法。
        """
        ts = str(int(time.time() * 1000))
        body_str = json.dumps(body, separators=(",", ":")) if body else ""
        # 签名串：timestamp + method + path + body
        sign_str = f"{ts}{method.upper()}{path}{body_str}"
        signature = hmac.new(
            self.config.api_secret.encode(),
            sign_str.encode(),
            hashlib.sha256,
        ).hexdigest()
        return {
            "X-API-Key": self.config.key_id,
            "X-API-Timestamp": ts,
            "X-API-Signature": signature,
        }

    def _request(self, method: str, path: str, body: Optional[dict] = None, params: Optional[dict] = None) -> Any:
        url = self.config.base_url + path
        headers = self._sign(method, path, body, params)
        resp = self._http.request(
            method, url, json=body, params=params, headers=headers, timeout=30,
        )
        data = resp.json() if resp.text else {}
        if not resp.ok or not data.get("success", False):
            err = data.get("error", data.get("message", resp.text))
            raise RuntimeError(f"ONDO API 错误 [{resp.status_code}]: {err}")
        result = data.get("result", data)
        return result

    def _unwrap_list(self, result: Any) -> list:
        """ONDO 有些接口返回 list，有些返回 {"list": [...]} 或 {"positions": [...]}"""
        if isinstance(result, list):
            return result
        if isinstance(result, dict):
            for key in ("positions", "list", "items", "data"):
                if key in result and isinstance(result[key], list):
                    return result[key]
        return []

    # ── 行情（公开） ────────────────────────────────────────
    def get_mark_prices(self) -> dict:
        """获取所有交易对标记价格"""
        resp = self._http.get(f"{self.config.base_url}/v1/perps/mark_prices", timeout=15)
        return resp.json().get("result", {})

    def get_mark_price(self, market: str) -> float:
        prices = self.get_mark_prices()
        return float(prices[market]["markPrice"])

    # ── 交易 ────────────────────────────────────────────────
    def place_market_order(
        self,
        market: str,
        side: str,            # "buy" or "sell"
        size_usd: float,      # 名义仓位价值 (USD)
        leverage: int = 10,
        reduce_only: bool = False,
    ) -> dict:
        """
        市价单开仓。
        market: 如 "BTC-USD.P"
        side: "buy"=做多, "sell"=做空
        size_usd: 名义仓位价值（margin * leverage）
        """
        # ONDO 下单需要 base 数量，根据 mark price 换算
        mark_price = self.get_mark_price(market)
        base_size = size_usd / mark_price
        # 根据交易对精度取整
        body = {
            "market": market,
            "side": side,
            "type": "market",
            "size": str(base_size),
            "leverage": leverage,
            "reduceOnly": reduce_only,
        }
        result = self._request("POST", "/v1/perps/orders", body=body)
        direction = "做多" if side == "buy" else "做空"
        print(f"[ONDO] 市价单已提交: {market} {direction} ${size_usd} x{leverage}")
        return result

    def close_position(self, market: str) -> dict:
        """平掉指定交易对的全部持仓"""
        positions = self.get_positions()
        pos = next((p for p in positions if p.get("market") == market), None)
        if not pos:
            print(f"[ONDO] {market} 无持仓")
            return {}
        size = abs(float(pos.get("size", 0)))
        if size <= 0:
            print(f"[ONDO] {market} 持仓为 0，跳过")
            return {}
        side = "sell" if float(pos.get("size", 0)) > 0 else "buy"
        return self.place_market_order(market, side, size * self.get_mark_price(market), reduce_only=True)

    def close_all(self) -> list[dict]:
        """平掉所有持仓（按市场去重，避免重复平仓）"""
        positions = self.get_positions()
        markets = list({p.get("market") for p in positions if p.get("market")})
        results = []
        for market in markets:
            results.append(self.close_position(market))
        return results

    # ── 查询 ────────────────────────────────────────────────
    def get_positions(self) -> list[dict]:
        """获取当前持仓"""
        result = self._request("GET", "/v1/perps/positions")
        return self._unwrap_list(result)

    def get_balance(self) -> dict:
        """获取账户余额"""
        return self._request("GET", "/v1/perps/balance")

    def get_account(self) -> dict:
        """获取账户概览"""
        return self._request("GET", "/v1/account")

    def get_leverage(self, market: str) -> dict:
        """获取指定交易对的杠杆设置"""
        return self._request("GET", f"/v1/perps/leverage", params={"market": market})

    def set_leverage(self, market: str, leverage: int) -> dict:
        """设置杠杆"""
        return self._request("POST", "/v1/perps/leverage", body={"market": market, "leverage": leverage})
