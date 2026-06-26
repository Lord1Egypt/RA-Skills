"""
kalshi_client.py — Authenticated Kalshi API client
Handles RSA-PSS request signing per Kalshi docs.
"""

import base64
import datetime
import os
import requests
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

BASE_URL = "https://api.elections.kalshi.com"
DEMO_URL = "https://demo-api.kalshi.co"


class KalshiClient:
    def __init__(self, key_id: str, private_key_path: str, demo: bool = False):
        self.key_id = key_id
        self.base_url = DEMO_URL if demo else BASE_URL
        self.demo = demo
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

        with open(private_key_path, "rb") as f:
            self.private_key = serialization.load_pem_private_key(
                f.read(), password=None, backend=default_backend()
            )

    def _sign(self, timestamp_ms: str, method: str, path: str) -> str:
        """Sign timestamp+method+path (no query params) with RSA-PSS."""
        path_no_query = path.split("?")[0]
        msg = (timestamp_ms + method.upper() + path_no_query).encode("utf-8")
        signature = self.private_key.sign(
            msg,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.DIGEST_LENGTH,
            ),
            hashes.SHA256(),
        )
        return base64.b64encode(signature).decode("utf-8")

    def _headers(self, method: str, path: str) -> dict:
        ts = str(int(datetime.datetime.now().timestamp() * 1000))
        return {
            "KALSHI-ACCESS-KEY": self.key_id,
            "KALSHI-ACCESS-TIMESTAMP": ts,
            "KALSHI-ACCESS-SIGNATURE": self._sign(ts, method, path),
            "Content-Type": "application/json",
        }

    def get(self, path: str, params: dict = None):
        full_path = path if "?" not in path else path
        if params:
            from urllib.parse import urlencode
            full_path = path + "?" + urlencode(params)
        r = self.session.get(
            self.base_url + full_path,
            headers=self._headers("GET", path),
        )
        r.raise_for_status()
        return r.json()

    def post(self, path: str, body: dict = None):
        import json
        r = self.session.post(
            self.base_url + path,
            headers=self._headers("POST", path),
            data=json.dumps(body or {}),
        )
        r.raise_for_status()
        return r.json()

    def delete(self, path: str):
        r = self.session.delete(
            self.base_url + path,
            headers=self._headers("DELETE", path),
        )
        r.raise_for_status()
        return r.json() if r.content else {}

    # ── Portfolio ──────────────────────────────────────────────────────────

    def get_balance(self) -> dict:
        """Returns balance in cents."""
        return self.get("/trade-api/v2/portfolio/balance")

    def get_positions(self) -> dict:
        return self.get("/trade-api/v2/portfolio/positions")

    def get_fills(self, limit: int = 25) -> dict:
        return self.get("/trade-api/v2/portfolio/fills", {"limit": limit})

    def get_orders(self, status: str = None) -> dict:
        params = {}
        if status:
            params["status"] = status
        return self.get("/trade-api/v2/portfolio/orders", params)

    # ── Markets ────────────────────────────────────────────────────────────

    def get_markets(self, status: str = "open", limit: int = 100, cursor: str = None) -> dict:
        params = {"status": status, "limit": limit}
        if cursor:
            params["cursor"] = cursor
        return self.get("/trade-api/v2/markets", params)

    def get_market(self, ticker: str) -> dict:
        return self.get(f"/trade-api/v2/markets/{ticker}")

    def get_orderbook(self, ticker: str, depth: int = 10) -> dict:
        return self.get(f"/trade-api/v2/markets/{ticker}/orderbook", {"depth": depth})

    def get_market_candlesticks(self, ticker: str, period_minutes: int = 60) -> dict:
        return self.get(
            f"/trade-api/v2/markets/{ticker}/candlesticks",
            {"period_seconds": period_minutes * 60},
        )

    def get_events(self, status: str = "open", limit: int = 50) -> dict:
        return self.get("/trade-api/v2/events", {"status": status, "limit": limit})

    # ── Orders ─────────────────────────────────────────────────────────────

    def create_order(
        self,
        ticker: str,
        side: str,           # "yes" or "no"
        action: str,         # "buy" or "sell"
        count: int,          # number of contracts
        limit_price: int,    # cents (1-99) — converted to dollars internally
        order_type: str = "limit",
        expiration_ts: int = None,
    ) -> dict:
        price_dollars = str(round(limit_price / 100, 4))
        body = {
            "ticker": ticker,
            "side": side,
            "action": action,
            "count": count,
            "type": order_type,
            "yes_price" if side == "yes" else "no_price": limit_price,
        }
        if expiration_ts:
            body["expiration_ts"] = expiration_ts
        return self.post("/trade-api/v2/portfolio/orders", body)

    def cancel_order(self, order_id: str) -> dict:
        return self.delete(f"/trade-api/v2/portfolio/orders/{order_id}")

    def get_order(self, order_id: str) -> dict:
        return self.get(f"/trade-api/v2/portfolio/orders/{order_id}")
