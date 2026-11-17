"""
Mock 客户端 - 用于演示和测试，不进行真实交易

模拟 PaperTrade 和 ONDO 的行为，输出真实的日志格式，
但不会提交任何交易意图到链上。
"""
from __future__ import annotations

import random
import time
from dataclasses import dataclass
from typing import Any, Optional

from paper_client import INSTRUMENTS


# ── 模拟 PaperTrade 客户端 ──────────────────────────────────
class MockPaperTradeClient:
    def __init__(self, wallet_private_key: str, session_key: Optional[str] = None):
        from eth_account import Account
        self.wallet = Account.from_key(wallet_private_key)
        self.wallet_address = self.wallet.address
        self.session = type("S", (), {
            "session_key": session_key or "0x" + "00" * 32,
            "session_address": "0x" + "11" * 20,
            "expiry": int(time.time()) + 30 * 24 * 3600,
        })()
        self._balance = 500.0  # 模拟余额 $500
        self._paper = 0.0       # 模拟 PAPER 数量
        self._positions = []    # 模拟持仓
        self._next_pos_id = 1

    def register_session_key(self):
        print(f"[PaperTrade][模拟] Session Key 注册成功: {self.session.session_address}")
        return self.session

    def _require_session(self):
        pass

    def open_position(self, symbol, is_long, margin_usd, leverage, use_debt=False):
        intent_id = f"mock-intent-{self._next_pos_id}"
        print(f"[PaperTrade][模拟] 开仓意图已提交: {symbol} {'多' if is_long else '空'} "
              f"${margin_usd} x{leverage} → intentId={intent_id}")
        self._positions.append({
            "positionId": str(self._next_pos_id),
            "instrumentId": INSTRUMENTS[symbol]["id"],
            "isLong": is_long,
            "entryPrice": 80000.0 if symbol == "BTC" else 2500.0,
            "marginUsd": margin_usd,
            "leverage": leverage,
        })
        self._balance -= margin_usd
        self._next_pos_id += 1
        return {"intentId": intent_id, "status": "submitted"}

    def close_positions(self, position_ids):
        ids = [str(pid) for pid in position_ids]
        closed = [p for p in self._positions if p["positionId"] in ids]
        for p in closed:
            self._balance += p["marginUsd"] * 0.99  # 扣 1% 模拟手续费
        self._positions = [p for p in self._positions if p["positionId"] not in ids]
        print(f"[PaperTrade][模拟] 平仓意图已提交: {len(ids)} 个仓位")
        return [{"intentId": f"mock-close-{i}"} for i in ids]

    def close_all(self, symbol=None):
        positions = self.get_positions()
        if symbol:
            target_id = INSTRUMENTS[symbol.upper()]["id"]
            positions = [p for p in positions if p["instrumentId"] == target_id]
        if not positions:
            print("[PaperTrade][模拟] 没有需要平仓的持仓")
            return []
        ids = [p["positionId"] for p in positions]
        return self.close_positions(ids)

    def get_account(self):
        return {
            "balance": int(self._balance * 10**18),
            "openPositions": [
                [p["positionId"], p["instrumentId"], p["isLong"], 0,
                 int(p["entryPrice"] * 10**10), int(p["marginUsd"] * 10**18),
                 p["leverage"], 0, int(time.time()), "mock-intent"]
                for p in self._positions
            ],
            "paper": {"balance": str(int(self._paper * 10**18)), "staked": "0"},
        }

    def get_positions(self):
        return list(self._positions)

    def get_paper_minted(self):
        return self._paper

    def get_balance_usd(self):
        return self._balance

    def get_protocol_summary(self):
        return {"totalLpUsd": str(int(4_760_000 * 10**18))}


# ── 模拟 ONDO 客户端 ────────────────────────────────────────
@dataclass
class MockOndoConfig:
    key_id: str = "mock_key_id"
    api_secret: str = "mock_secret"
    base_url: str = "https://api.ondoperps.xyz"


class MockOndoClient:
    def __init__(self, config=None):
        self.config = config or MockOndoConfig()
        self._positions = []
        self._balance = 1000.0
        self._base_price = {"BTC-USD.P": 80000.0, "ETH-USD.P": 2500.0}

    def get_mark_prices(self):
        # 模拟价格小幅波动
        for k in self._base_price:
            self._base_price[k] *= (1 + random.uniform(-0.001, 0.001))
        return {k: {"markPrice": str(v)} for k, v in self._base_price.items()}

    def get_mark_price(self, market):
        return self._base_price[market]

    def place_market_order(self, market, side, size_usd, leverage=10, reduce_only=False):
        base_size = size_usd / self.get_mark_price(market)
        direction = "做多" if side == "buy" else "做空"
        print(f"[ONDO][模拟] 市价单已提交: {market} {direction} ${size_usd} x{leverage}")
        if not reduce_only:
            existing = next((p for p in self._positions if p["market"] == market), None)
            if existing:
                existing["size"] += base_size if side == "buy" else -base_size
            else:
                self._positions.append({
                    "market": market,
                    "size": base_size if side == "buy" else -base_size,
                    "entryPrice": self.get_mark_price(market),
                })
        return {"orderId": f"mock-ondo-{int(time.time())}", "status": "filled"}

    def close_position(self, market):
        pos = next((p for p in self._positions if p["market"] == market), None)
        if not pos:
            print(f"[ONDO][模拟] {market} 无持仓")
            return {}
        size = abs(pos["size"])
        side = "sell" if pos["size"] > 0 else "buy"
        self._positions = [p for p in self._positions if p["market"] != market]
        return self.place_market_order(market, side, size * self.get_mark_price(market), reduce_only=True)

    def close_all(self):
        markets = list({p["market"] for p in self._positions})
        return [self.close_position(m) for m in markets]

    def get_positions(self):
        return list(self._positions)

    def get_balance(self):
        return {"freeCollateral": str(self._balance), "availableBalance": str(self._balance)}

    def get_account(self):
        return {"balance": self._balance}

    def get_leverage(self, market):
        return {"market": market, "leverage": 10}

    def set_leverage(self, market, leverage):
        return {"market": market, "leverage": leverage, "status": "ok"}
