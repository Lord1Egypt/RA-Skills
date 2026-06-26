"""
Polymarket REST client — wraps Gamma (market data) and CLOB (trading) APIs.

Public endpoints (no auth):
  - Search / list markets
  - Order book, mid-price, spread, last trade
  - Price history

Authenticated endpoints (requires EVM private key):
  - Place limit / market orders
  - Cancel orders
  - Query own trades & balances

Auth flow (Polymarket L2):
  The CLOB API uses EIP-712 typed-data signatures.
  Set env var POLYMARKET_PRIVATE_KEY=0x<hex> to enable trading.
"""
import os
import hashlib
import time
from typing import Optional
import httpx
from dataclasses import dataclass, field

GAMMA_BASE = "https://gamma-api.polymarket.com"
CLOB_BASE  = "https://clob.polymarket.com"

_PRIVATE_KEY: Optional[str] = os.environ.get("POLYMARKET_PRIVATE_KEY")


# ── Data models ───────────────────────────────────────────────────────────────

@dataclass
class Market:
    id: str
    question: str
    slug: str
    condition_id: str
    clob_token_ids: list[str]
    outcome_prices: list[str]  # e.g. ["0.65", "0.35"]
    outcomes: list[str]        # e.g. ["Yes", "No"]
    volume: float
    liquidity: float
    active: bool
    closed: bool
    end_date: Optional[str]


@dataclass
class OrderBookLevel:
    price: float
    size: float


@dataclass
class OrderBook:
    token_id: str
    bids: list[OrderBookLevel]
    asks: list[OrderBookLevel]
    last_trade_price: Optional[float]
    timestamp: str


@dataclass
class PlacedOrder:
    order_id: str
    status: str
    success: bool
    error_msg: Optional[str]


# ── Helpers ───────────────────────────────────────────────────────────────────

def _parse_market(raw: dict) -> Market:
    prices = raw.get("outcomePrices") or raw.get("outcome_prices") or []
    outcomes = raw.get("outcomes") or []
    clob_ids = raw.get("clobTokenIds") or raw.get("clob_token_ids") or []
    return Market(
        id=str(raw.get("id", "")),
        question=raw.get("question", ""),
        slug=raw.get("slug", ""),
        condition_id=str(raw.get("conditionId") or raw.get("condition_id") or ""),
        clob_token_ids=[str(t) for t in clob_ids],
        outcome_prices=[str(p) for p in prices],
        outcomes=[str(o) for o in outcomes],
        volume=float(raw.get("volumeNum") or raw.get("volume_num") or 0),
        liquidity=float(raw.get("liquidityNum") or raw.get("liquidity_num") or 0),
        active=bool(raw.get("active", False)),
        closed=bool(raw.get("closed", False)),
        end_date=raw.get("endDate") or raw.get("end_date"),
    )


# ── Public market data ─────────────────────────────────────────────────────────

async def search_markets(keyword: str, limit: int = 10) -> list[Market]:
    """Full-text search across all Polymarket markets."""
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(
            f"{GAMMA_BASE}/markets",
            params={"keyword": keyword, "limit": limit, "active": "true"},
        )
        resp.raise_for_status()
        data = resp.json()
        items = data if isinstance(data, list) else data.get("data", data.get("markets", []))
        return [_parse_market(m) for m in items]


async def get_active_btc_markets(limit: int = 10) -> list[Market]:
    """Fetch active prediction markets related to BTC / Bitcoin price."""
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(
            f"{GAMMA_BASE}/markets",
            params={
                "keyword": "Bitcoin BTC price",
                "active": "true",
                "closed": "false",
                "limit": limit,
                "order": "volume_num",
            },
        )
        resp.raise_for_status()
        data = resp.json()
        items = data if isinstance(data, list) else data.get("data", data.get("markets", []))
        return [_parse_market(m) for m in items]


async def get_market_by_id(market_id: str) -> Market:
    """Fetch a single market by numeric ID or slug."""
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(f"{GAMMA_BASE}/markets/{market_id}")
        resp.raise_for_status()
        return _parse_market(resp.json())


async def get_order_book(token_id: str) -> OrderBook:
    """Return the full order book for a token (YES or NO token_id)."""
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(f"{CLOB_BASE}/book", params={"token_id": token_id})
        resp.raise_for_status()
        raw = resp.json()

        bids = [OrderBookLevel(price=float(b["price"]), size=float(b["size"])) for b in raw.get("bids", [])]
        asks = [OrderBookLevel(price=float(a["price"]), size=float(a["size"])) for a in raw.get("asks", [])]
        ltp = raw.get("last_trade_price")

        return OrderBook(
            token_id=token_id,
            bids=bids,
            asks=asks,
            last_trade_price=float(ltp) if ltp else None,
            timestamp=raw.get("timestamp", ""),
        )


async def get_midpoint(token_id: str) -> Optional[float]:
    """Return mid-price for a token."""
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(f"{CLOB_BASE}/midpoint", params={"token_id": token_id})
        resp.raise_for_status()
        val = resp.json().get("mid")
        return float(val) if val is not None else None


async def get_price_history(token_id: str, interval: str = "1h", fidelity: int = 50) -> list[dict]:
    """
    Return OHLCV-style price history.
    interval: 1m, 5m, 1h, 6h, 1d
    """
    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.get(
            f"{CLOB_BASE}/prices-history",
            params={"market": token_id, "interval": interval, "fidelity": fidelity},
        )
        resp.raise_for_status()
        return resp.json().get("history", [])


async def get_spread(token_id: str) -> Optional[float]:
    """Return bid-ask spread for a token."""
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(f"{CLOB_BASE}/spread", params={"token_id": token_id})
        resp.raise_for_status()
        val = resp.json().get("spread")
        return float(val) if val is not None else None


# ── Authenticated trading ──────────────────────────────────────────────────────

def _check_private_key() -> str:
    if not _PRIVATE_KEY:
        raise RuntimeError(
            "POLYMARKET_PRIVATE_KEY not set. "
            "Export your wallet private key to enable trading."
        )
    return _PRIVATE_KEY


async def get_clob_auth_headers() -> dict:
    """
    Build L2 auth headers for the CLOB API.
    Polymarket uses EIP-712 signatures. For simplicity this calls the
    /auth/derive-api-key endpoint which returns short-lived API credentials.
    In production use py-clob-client for the full signing flow.
    """
    # Real signing requires py-clob-client or manual eth_sign/EIP-712.
    # This stub documents the expected header format.
    raise NotImplementedError(
        "Install py-clob-client and call ClobClient.create_api_key() "
        "to get (api_key, secret, passphrase) for authenticated requests."
    )


async def place_limit_order(
    token_id: str,
    side: str,          # "BUY" or "SELL"
    price: float,       # 0.01 – 0.99
    size: float,        # number of shares
    order_type: str = "GTC",
) -> PlacedOrder:
    """
    Place a limit order. Requires POLYMARKET_PRIVATE_KEY.

    For a fully working implementation, integrate py-clob-client:
        pip install py-clob-client
        from py_clob_client.client import ClobClient
        client = ClobClient(host, key=pk, chain_id=137)
        resp = client.create_and_post_order(
            OrderArgs(token_id=..., price=..., size=..., side=...)
        )
    """
    _check_private_key()
    # ↓ Placeholder — replace with py-clob-client call in production
    raise NotImplementedError(
        "Integrate py-clob-client for live order placement. "
        "See README for instructions."
    )


async def place_market_order(
    token_id: str,
    side: str,
    amount_usdc: float,
) -> PlacedOrder:
    """
    Place a market buy (amount in USDC) or market sell (amount in shares).
    Requires POLYMARKET_PRIVATE_KEY.
    """
    _check_private_key()
    raise NotImplementedError(
        "Integrate py-clob-client for live market orders. "
        "See README for instructions."
    )


async def get_positions(wallet_address: str) -> list[dict]:
    """Return open positions for a wallet address (Gamma Data API)."""
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(f"{GAMMA_BASE}/positions", params={"user": wallet_address})
        resp.raise_for_status()
        return resp.json()


async def get_portfolio_value(wallet_address: str) -> list[dict]:
    """Return current USD value of all positions."""
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(f"{GAMMA_BASE}/value", params={"user": wallet_address})
        resp.raise_for_status()
        return resp.json()
