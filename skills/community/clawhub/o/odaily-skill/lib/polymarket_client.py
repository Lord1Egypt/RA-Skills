"""Polymarket 数据获取"""

from __future__ import annotations

import json
import time
from datetime import datetime, timezone, timedelta

import requests

from config.settings import settings

BJT = timezone(timedelta(hours=8))


GAMMA_API = "https://gamma-api.polymarket.com"


class PolymarketClient:

    def __init__(self):
        self.s = requests.Session()
        self.s.headers.update({"User-Agent": settings.USER_AGENT})
        self.base = settings.POLYMARKET_DATA_API

    def _get(self, path: str, params: dict | None = None, base: str | None = None):
        """带 ProxyError / ConnectionError 重试的 GET（最多3次）"""
        url = f"{base or self.base}{path}"
        last_exc: Exception | None = None
        for attempt in range(3):
            try:
                resp = self.s.get(url, params=params, timeout=settings.REQUEST_TIMEOUT)
                resp.raise_for_status()
                return resp
            except (requests.exceptions.ProxyError,
                    requests.exceptions.ConnectionError) as e:
                last_exc = e
                time.sleep(8 * (attempt + 1))
        raise last_exc or RuntimeError(f"Polymarket request failed: {path}")

    def get_whale_trades(self, min_size: float = 10000, limit: int = 50) -> list[dict]:
        resp = self._get("/trades", {
            "takerOnly": "true",
            "limit": limit,
            "offset": 0,
            "filterType": "CASH",
            "filterAmount": int(min_size),
        })
        out: list[dict] = []
        for t in resp.json():
            ts = int(t.get("timestamp", 0))
            out.append({
                "transaction_hash": t.get("transactionHash", ""),
                "proxy_wallet": t.get("proxyWallet", ""),
                "name": t.get("name") or t.get("pseudonym") or "匿名巨鲸",
                "side": t.get("side", ""),
                "size": float(t.get("size", 0)),
                "price": float(t.get("price", 0)),
                "outcome": t.get("outcome", ""),
                "title": t.get("title", ""),
                "slug": t.get("slug", ""),
                "event_slug": t.get("eventSlug", ""),
                "icon": t.get("icon", ""),
                "timestamp": ts,
                "timestamp_str": (
                    datetime.fromtimestamp(ts, tz=BJT).strftime("%m-%d %H:%M")
                    if ts else ""
                ),
            })
        return out

    def filter_tail_trades(self, trades: list[dict], min_price: float = 0.95) -> list[dict]:
        tail = [t for t in trades if t["price"] >= min_price]
        tail.sort(key=lambda x: x["size"], reverse=True)
        return tail

    def get_hot_events(self, limit: int = 20) -> list[dict]:
        try:
            resp = self._get(
                "/events",
                {
                    "limit": limit * 10,
                    "active": "true",
                    "closed": "false",
                    "_sort": "volume24hr",
                    "_order": "DESC",
                },
                base=GAMMA_API,
            )
            now_ts = time.time()
            from datetime import datetime as _dt, timezone as _tz
            out: list[dict] = []
            for e in resp.json():
                if e.get("closed") or e.get("archived"):
                    continue
                # 过滤已过截止日期的事件
                end_date = e.get("endDate") or ""
                if end_date:
                    try:
                        end_ts = _dt.fromisoformat(
                            end_date.replace("Z", "+00:00")
                        ).timestamp()
                        if end_ts < now_ts:
                            continue
                    except Exception:
                        pass
                markets = e.get("markets", [])
                if not markets:
                    continue
                m = markets[0]
                raw_prices = m.get("outcomePrices", [])
                if isinstance(raw_prices, str):
                    raw_prices = json.loads(raw_prices)
                yp = float(raw_prices[0]) if raw_prices else 0.5
                vol24 = float(e.get("volume24hr") or 0)
                vol = float(e.get("volume") or m.get("volume") or 0)
                out.append({
                    "title": e.get("title", ""),
                    "slug": e.get("slug", ""),
                    "yes_probability": round(yp * 100, 1),
                    "no_probability": round((1 - yp) * 100, 1),
                    "volume": vol,
                    "volume24hr": vol24,
                    "liquidity": float(e.get("liquidity") or m.get("liquidity") or 0),
                    "url": f"https://polymarket.com/event/{e.get('slug', '')}",
                    "end_date": e.get("endDate", ""),
                })
            # 按当日成交量降序，确保展示查询时刻最热事件
            out.sort(key=lambda x: x["volume24hr"], reverse=True)
            return out[:limit]
        except Exception:
            return []
