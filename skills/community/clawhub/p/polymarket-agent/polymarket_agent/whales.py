"""Tracking large flow ("whales") and smart money.

Architecture decision, based on what the API actually offers: **there is no
public WebSocket channel for "every trade in the whole market"** — the
`/ws/market` channel requires an explicit list of `assets_ids`. To watch the
market as a whole, the path is *polling* `GET /trades`, which accepts a size
filter on the SERVER (`filterType=CASH&filterAmount=N`). This avoids paginating
thousands of small trades only to discard them on the client.

Important API trap: on `/trades`, `size` is the number of **shares**, not
dollars. The notional is `size × price`. A trade of 50,000 shares at $0.02 is
$1,000, not $50,000 — confusing the two would produce absurd alerts.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .config import DATA_API, GAMMA_API, LEADERBOARD_CATEGORIES, LEADERBOARD_PERIODS
from .http import ApiError, clean_slug, clean_text, get_json

#: The Data API caps `/holders` at 20 per token — asking for more returns 400.
MAX_HOLDERS = 20
#: `/v1/leaderboard` accepts at most 50 rows.
MAX_LEADERBOARD = 50
#: `/trades` accepts up to 10,000, but pulling all of that is wasteful and burns
#: rate limit (200 req/10s). 500 comfortably covers a window of alerts.
MAX_TRADES = 1000


@dataclass
class WhaleTrade:
    """A large trade, already carrying the computed notional."""

    tx_hash: str
    wallet: str
    trader: str
    side: str
    outcome: str
    size_shares: float
    price: float
    title: str
    slug: str = ""
    condition_id: str = ""
    asset_id: str = ""
    timestamp: int = 0
    event_slug: str = ""

    @property
    def notional_usd(self) -> float:
        """Value in USDC. The API's `size` is in SHARES — hence the multiply."""
        return self.size_shares * self.price

    @property
    def implied_pct(self) -> float:
        return self.price * 100

    @property
    def url(self) -> str:
        slug = self.event_slug or self.slug
        return f"https://polymarket.com/event/{slug}" if slug else ""

    @property
    def profile_url(self) -> str:
        return f"https://polymarket.com/profile/{self.wallet}" if self.wallet else ""

    def summary(self) -> str:
        return (
            f"${self.notional_usd:,.0f} {self.side} {self.outcome} "
            f"@ ${self.price:.3f} — {self.title}"
        )


def _as_float(raw: Any, default: float = 0.0) -> float:
    try:
        if raw is None or raw == "":
            return default
        return float(raw)
    except (TypeError, ValueError):
        return default


def parse_trade(raw: Dict[str, Any]) -> WhaleTrade:
    # Every free-text field is cleaned HERE, at the boundary where the API
    # payload becomes an object — so no consumer (terminal, cron alert, agent
    # context) has to remember to do it. See `http.clean_text`.
    trader = (
        clean_text(raw.get("name"), 48)
        or clean_text(raw.get("pseudonym"), 48)
        or clean_slug(raw.get("proxyWallet"))[:10]
    )
    return WhaleTrade(
        tx_hash=str(raw.get("transactionHash") or ""),
        wallet=str(raw.get("proxyWallet") or ""),
        trader=trader,
        side=str(raw.get("side") or "").upper(),
        outcome=clean_text(raw.get("outcome"), 40) or "?",
        size_shares=_as_float(raw.get("size")),
        price=_as_float(raw.get("price")),
        title=clean_text(raw.get("title")) or "?",
        slug=clean_slug(raw.get("slug")),
        condition_id=str(raw.get("conditionId") or ""),
        asset_id=str(raw.get("asset") or ""),
        timestamp=int(_as_float(raw.get("timestamp"))),
        event_slug=clean_slug(raw.get("eventSlug")),
    )


def recent_whales(
    min_notional: float = 25_000.0,
    window_seconds: int = 3600,
    limit: int = 50,
    market: Optional[str] = None,
    side: Optional[str] = None,
    taker_only: bool = False,
) -> List[WhaleTrade]:
    """Trades above `min_notional` USDC in the recent window.

    The size filter is applied by the SERVER (`filterType=CASH`), so we do not
    paginate junk. `taker_only=False` includes the maker side — a whale that
    *provides* liquidity is also a signal.
    """
    import time

    params: Dict[str, Any] = {
        "limit": max(1, min(int(limit), MAX_TRADES)),
        "filterType": "CASH",
        "filterAmount": max(0.0, float(min_notional)),
        "takerOnly": "true" if taker_only else "false",
    }
    if window_seconds > 0:
        params["start"] = int(time.time()) - int(window_seconds)
    if market:
        params["market"] = market
    if side and side.upper() in {"BUY", "SELL"}:
        params["side"] = side.upper()

    rows = get_json(DATA_API, "/trades", params, label="Data API /trades")
    if not isinstance(rows, list):
        return []

    trades = [parse_trade(r) for r in rows if isinstance(r, dict)]
    # The API filters by notional, but we revalidate: `size` comes in shares and
    # a degenerate price (0) would produce a notional of 0 passing the filter.
    trades = [t for t in trades if t.notional_usd >= min_notional]
    trades.sort(key=lambda t: t.notional_usd, reverse=True)
    return trades


def market_holders(condition_id: str, limit: int = MAX_HOLDERS) -> List[Dict[str, Any]]:
    """Largest holders of each outcome in a market.

    The response is a list of `{token, holders[]}` — one object per outcome.
    """
    rows = get_json(
        DATA_API,
        "/holders",
        {"market": condition_id, "limit": max(1, min(int(limit), MAX_HOLDERS))},
        label="Data API /holders",
    )
    return [r for r in rows if isinstance(r, dict)] if isinstance(rows, list) else []


@dataclass
class Trader:
    rank: int
    wallet: str
    name: str
    pnl: float
    volume: float

    @property
    def profile_url(self) -> str:
        return f"https://polymarket.com/profile/{self.wallet}" if self.wallet else ""


def leaderboard(
    category: str = "OVERALL",
    period: str = "MONTH",
    order_by: str = "PNL",
    limit: int = 20,
) -> List[Trader]:
    """Ranking of traders by profit or volume — the "smart money" filter."""
    category = (category or "OVERALL").upper()
    period = (period or "MONTH").upper()
    order_by = (order_by or "PNL").upper()

    if category not in LEADERBOARD_CATEGORIES:
        raise ApiError(
            f"invalid category: {category}. Use one of {sorted(LEADERBOARD_CATEGORIES)}"
        )
    if period not in LEADERBOARD_PERIODS:
        raise ApiError(
            f"invalid period: {period}. Use one of {sorted(LEADERBOARD_PERIODS)}"
        )
    if order_by not in {"PNL", "VOL"}:
        raise ApiError("orderBy must be PNL or VOL")

    rows = get_json(
        DATA_API,
        "/v1/leaderboard",
        {
            "category": category,
            "timePeriod": period,
            "orderBy": order_by,
            "limit": max(1, min(int(limit), MAX_LEADERBOARD)),
        },
        label="Data API /v1/leaderboard",
    )
    if not isinstance(rows, list):
        return []

    traders: List[Trader] = []
    for idx, row in enumerate(rows, 1):
        if not isinstance(row, dict):
            continue
        traders.append(
            Trader(
                # `rank` arrives as a STRING in the real response; falls back
                # to the index.
                rank=int(_as_float(row.get("rank"), idx)),
                wallet=str(row.get("proxyWallet") or ""),
                name=str(row.get("userName") or "") or str(row.get("proxyWallet") or "")[:10],
                pnl=_as_float(row.get("pnl")),
                volume=_as_float(row.get("vol")),
            )
        )
    return traders


def trader_positions(wallet: str, limit: int = 20) -> List[Dict[str, Any]]:
    """Current positions of any wallet (public endpoint)."""
    rows = get_json(
        DATA_API,
        "/positions",
        {
            "user": wallet,
            "limit": max(1, min(int(limit), 500)),
            "sortBy": "CURRENT",
            "sortDirection": "DESC",
            "sizeThreshold": 1,
        },
        label="Data API /positions",
    )
    return [r for r in rows if isinstance(r, dict)] if isinstance(rows, list) else []


def trader_value(wallet: str) -> Optional[float]:
    """Total value of a wallet's positions (contextualizes conviction)."""
    rows = get_json(DATA_API, "/value", {"user": wallet}, label="Data API /value")
    if isinstance(rows, list) and rows and isinstance(rows[0], dict):
        return _as_float(rows[0].get("value"), 0.0)
    return None


def trader_trades(wallet: str, limit: int = 20) -> List[WhaleTrade]:
    """Recent trades of a specific wallet."""
    rows = get_json(
        DATA_API,
        "/trades",
        {"user": wallet, "limit": max(1, min(int(limit), MAX_TRADES)), "takerOnly": "false"},
        label="Data API /trades",
    )
    if not isinstance(rows, list):
        return []
    return [parse_trade(r) for r in rows if isinstance(r, dict)]


@dataclass
class Quote:
    """A market's quote — spread and top of book.

    Gamma already returns `spread`/`bestBid`/`bestAsk` on the market object
    itself, which avoids an extra call to the CLOB just to learn whether you
    can get in and out without bleeding on the spread.
    """

    question: str
    best_bid: float
    best_ask: float
    spread: float
    last_trade: float
    volume_24h: float
    liquidity: float

    @property
    def spread_pct(self) -> float:
        mid = (self.best_bid + self.best_ask) / 2
        return (self.spread / mid * 100) if mid > 0 else 0.0


def quote_for(market_id: str) -> Optional[Quote]:
    """Spread and top of book for a market, straight from Gamma."""
    market_id = str(market_id).strip()
    params: Dict[str, Any] = (
        {"id": market_id} if market_id.isdigit() else {"slug": market_id}
    )
    params["limit"] = 1
    raw = get_json(GAMMA_API, "/markets", params, label="Gamma API /markets")
    rows = raw if isinstance(raw, list) else (raw or {}).get("data", [])
    for row in rows:
        if not isinstance(row, dict):
            continue
        return Quote(
            question=str(row.get("question") or "?"),
            best_bid=_as_float(row.get("bestBid")),
            best_ask=_as_float(row.get("bestAsk")),
            spread=_as_float(row.get("spread")),
            last_trade=_as_float(row.get("lastTradePrice")),
            volume_24h=_as_float(row.get("volume24hr")),
            liquidity=_as_float(row.get("liquidityNum") or row.get("liquidity")),
        )
    return None
