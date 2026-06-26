"""
行情数据获取 — CoinGecko + Binance + Alternative.me
每次调用实时获取，不需要数据库
"""

from __future__ import annotations

import time
from datetime import datetime, timezone, timedelta
from typing import Optional

import requests

from config.settings import settings

BJT = timezone(timedelta(hours=8))

COINGECKO_IDS: dict[str, str] = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "SOL": "solana",
    "BNB": "binancecoin",
    "XRP": "ripple",
    "ADA": "cardano",
    "DOGE": "dogecoin",
    "AVAX": "avalanche-2",
    "DOT": "polkadot",
    "LINK": "chainlink",
    "UNI": "uniswap",
    "AAVE": "aave",
    "ARB": "arbitrum",
    "OP": "optimism",
    "APT": "aptos",
    "SUI": "sui",
    "NEAR": "near",
    "TON": "the-open-network",
    "PEPE": "pepe",
    "WIF": "dogwifcoin",
    "MATIC": "matic-network",
    "ATOM": "cosmos",
}


class MarketData:

    def __init__(self):
        self.s = requests.Session()
        self.s.headers.update({"User-Agent": settings.USER_AGENT})
        if settings.COINGECKO_API_KEY:
            self.s.headers["x-cg-demo-api-key"] = settings.COINGECKO_API_KEY

    def _cg_get(self, path: str, params: dict | None = None):
        """CoinGecko GET，自动重试 429 / ProxyError / ConnectionError（最多3次）"""
        url = f"{settings.COINGECKO_API_URL}{path}"
        last_exc: Exception | None = None
        for attempt in range(3):
            try:
                resp = self.s.get(url, params=params, timeout=settings.REQUEST_TIMEOUT)
                if resp.status_code == 429:
                    time.sleep(12 * (attempt + 1))
                    continue
                resp.raise_for_status()
                return resp
            except (requests.exceptions.ProxyError,
                    requests.exceptions.ConnectionError) as e:
                last_exc = e
                time.sleep(8 * (attempt + 1))
        raise last_exc or RuntimeError(f"CoinGecko request failed: {path}")

    # ── 实时价格 ──────────────────────────────────────────

    def get_prices(self, symbols: list[str] | None = None) -> list[dict]:
        symbols = symbols or settings.TRACKED_TOKENS[:10]
        ids: list[str] = []
        sym_map: dict[str, str] = {}
        for sym in symbols:
            cg = COINGECKO_IDS.get(sym.upper())
            if cg:
                ids.append(cg)
                sym_map[cg] = sym.upper()
        if not ids:
            return []

        resp = self._cg_get("/simple/price", {
            "ids": ",".join(ids),
            "vs_currencies": "usd",
            "include_24hr_change": "true",
            "include_24hr_vol": "true",
            "include_market_cap": "true",
        })
        data = resp.json()

        out: list[dict] = []
        for cg_id, info in data.items():
            out.append({
                "symbol": sym_map.get(cg_id, cg_id.upper()),
                "price_usd": info.get("usd", 0),
                "change_24h_pct": round(info.get("usd_24h_change", 0) or 0, 2),
                "volume_24h": info.get("usd_24h_vol", 0),
                "market_cap": info.get("usd_market_cap", 0),
            })
        out.sort(key=lambda x: x.get("market_cap", 0), reverse=True)
        return out

    # ── K线 (Binance) ────────────────────────────────────

    def get_klines(
        self, symbol: str, interval: str = "4h", limit: int = 200
    ) -> list[dict]:
        pair = f"{symbol.upper()}USDT"
        resp = self.s.get(
            f"{settings.BINANCE_API_URL}/klines",
            params={"symbol": pair, "interval": interval, "limit": limit},
            timeout=settings.REQUEST_TIMEOUT,
        )
        resp.raise_for_status()
        return [
            {
                "time": datetime.fromtimestamp(k[0] / 1000, tz=BJT),
                "open": float(k[1]),
                "high": float(k[2]),
                "low": float(k[3]),
                "close": float(k[4]),
                "volume": float(k[5]),
            }
            for k in resp.json()
        ]

    # ── 恐惧贪婪 ─────────────────────────────────────────

    def get_fear_greed_index(self) -> dict:
        resp = self.s.get(
            settings.FEAR_GREED_API,
            params={"limit": 1},
            timeout=settings.REQUEST_TIMEOUT,
        )
        resp.raise_for_status()
        item = resp.json().get("data", [{}])[0]
        val = int(item.get("value", 50))
        if val <= 25:
            label, emoji = "极度恐惧", "😱"
        elif val <= 45:
            label, emoji = "恐惧", "😰"
        elif val <= 55:
            label, emoji = "中性", "😐"
        elif val <= 75:
            label, emoji = "贪婪", "😏"
        else:
            label, emoji = "极度贪婪", "🤑"
        return {
            "value": val,
            "label": label,
            "emoji": emoji,
            "timestamp": item.get("timestamp", ""),
        }

    # ── 资金费率 ──────────────────────────────────────────

    def get_funding_rates(self) -> dict:
        out: dict = {}
        for pair in ["BTCUSDT", "ETHUSDT"]:
            try:
                resp = self.s.get(
                    f"{settings.BINANCE_FUTURES_URL}/premiumIndex",
                    params={"symbol": pair},
                    timeout=settings.REQUEST_TIMEOUT,
                )
                resp.raise_for_status()
                d = resp.json()
                sym = pair.replace("USDT", "")
                out[sym] = {
                    "funding_rate": round(
                        float(d.get("lastFundingRate", 0)) * 100, 4
                    ),
                    "mark_price": round(float(d.get("markPrice", 0)), 2),
                    "index_price": round(float(d.get("indexPrice", 0)), 2),
                }
            except Exception:
                pass
        return out

    # ── 多空比 ────────────────────────────────────────────

    def get_long_short_ratio(self) -> dict:
        out: dict = {}
        for pair in ["BTCUSDT", "ETHUSDT"]:
            try:
                resp = self.s.get(
                    f"{settings.BINANCE_FUTURES_URL}/globalLongShortAccountRatio",
                    params={"symbol": pair, "period": "5m", "limit": 1},
                    timeout=settings.REQUEST_TIMEOUT,
                )
                resp.raise_for_status()
                d = resp.json()
                if d:
                    sym = pair.replace("USDT", "")
                    out[sym] = {
                        "long_short_ratio": round(
                            float(d[0].get("longShortRatio", 1)), 4
                        ),
                        "long_account_pct": round(
                            float(d[0].get("longAccount", 0.5)) * 100, 2
                        ),
                        "short_account_pct": round(
                            float(d[0].get("shortAccount", 0.5)) * 100, 2
                        ),
                    }
            except Exception:
                pass
        return out

    # ── 全局数据 ──────────────────────────────────────────

    def get_global_data(self) -> dict:
        resp = self._cg_get("/global")
        d = resp.json().get("data", {})
        return {
            "total_market_cap_usd": d.get("total_market_cap", {}).get("usd", 0),
            "total_volume_24h_usd": d.get("total_volume", {}).get("usd", 0),
            "btc_dominance": round(
                d.get("market_cap_percentage", {}).get("btc", 0), 2
            ),
            "eth_dominance": round(
                d.get("market_cap_percentage", {}).get("eth", 0), 2
            ),
            "active_cryptocurrencies": d.get("active_cryptocurrencies", 0),
            "market_cap_change_24h_pct": round(
                d.get("market_cap_change_percentage_24h_usd", 0), 2
            ),
        }

    # ── 涨跌排行 ──────────────────────────────────────────

    def get_top_movers(self, limit: int = 5) -> dict:
        resp = self._cg_get("/coins/markets", {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 100,
            "page": 1,
            "sparkline": "false",
            "price_change_percentage": "24h,7d",
        })
        coins = [
            {
                "symbol": c.get("symbol", "").upper(),
                "name": c.get("name", ""),
                "price": c.get("current_price", 0),
                "change_24h_pct": round(
                    c.get("price_change_percentage_24h", 0) or 0, 2
                ),
                "change_7d_pct": round(
                    c.get("price_change_percentage_7d_in_currency", 0) or 0, 2
                ),
                "market_cap": c.get("market_cap", 0),
            }
            for c in resp.json()
        ]
        s = sorted(coins, key=lambda x: x["change_24h_pct"])
        return {"top_gainers": s[-limit:][::-1], "top_losers": s[:limit]}
