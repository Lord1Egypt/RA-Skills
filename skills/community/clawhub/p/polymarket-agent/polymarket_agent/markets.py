"""Reading markets from the Gamma API (read-only, no credentials).

BUG FIX (functional, critical): v1.0.2 fetched the `limit` most liquid markets
and ONLY THEN filtered by text on the client. With `limit=10`, searching for
"bitcoin" only hit if a bitcoin market happened to be in the top-10 by volume
at that instant — in practice it returned empty almost always. The search now
uses the server's search endpoint and, on the fallback, paginates for real.

BUG FIX (functional, critical): `clobTokenIds` arrived from the API as a JSON
STRING and was passed through raw. Since trading requires the outcome's
`token_id`, the "find market → buy" flow was impossible to complete. Now each
outcome comes paired with its token_id.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .config import GAMMA_API, HTTP_TIMEOUT
from .http import ApiError, clean_slug, clean_text, get_json

PAGE_SIZE = 100
MAX_PAGES = 10  # cap of 1000 markets scanned in the fallback


#: Kept as an alias for compatibility: the shared HTTP layer already raises
#: ApiError with retry/backoff, which MarketError now extends.
class MarketError(ApiError):
    """Failure querying the Gamma API."""


@dataclass
class Outcome:
    """A tradable outcome, already carrying the token_id needed to trade."""

    name: str
    price: Optional[float]
    token_id: str = ""

    @property
    def implied_pct(self) -> Optional[float]:
        return None if self.price is None else self.price * 100


@dataclass
class Market:
    id: str
    question: str
    slug: str = ""
    volume_24h: float = 0.0
    liquidity: float = 0.0
    end_date: str = ""
    closed: bool = False
    outcomes: List[Outcome] = field(default_factory=list)

    @property
    def url(self) -> str:
        return f"https://polymarket.com/market/{self.slug}" if self.slug else ""

    def token_for(self, outcome_name: str) -> Optional[str]:
        target = outcome_name.strip().lower()
        for out in self.outcomes:
            if out.name.strip().lower() == target:
                return out.token_id or None
        return None

    def prices_label(self) -> str:
        if not self.outcomes:
            return "N/A"
        parts = []
        for out in self.outcomes:
            parts.append(f"{out.name}: ${out.price:.2f}" if out.price is not None
                         else f"{out.name}: ?")
        return ", ".join(parts)


def _as_list(raw: Any) -> List[Any]:
    """Gamma returns some fields as a JSON string ('["Yes","No"]')."""
    if isinstance(raw, list):
        return raw
    if isinstance(raw, str) and raw.strip():
        try:
            parsed = json.loads(raw)
            return parsed if isinstance(parsed, list) else []
        except json.JSONDecodeError:
            return []
    return []


def _as_float(raw: Any, default: float = 0.0) -> float:
    try:
        if raw is None or raw == "":
            return default
        return float(raw)
    except (TypeError, ValueError):
        return default


def parse_market(raw: Dict[str, Any]) -> Market:
    """Normalize a Gamma market, pairing outcome ↔ price ↔ token_id."""
    names = [clean_text(n, 60) for n in _as_list(raw.get("outcomes"))]
    prices = _as_list(raw.get("outcomePrices"))
    tokens = [str(t) for t in _as_list(raw.get("clobTokenIds"))]

    outcomes: List[Outcome] = []
    for idx, name in enumerate(names):
        price = _as_float(prices[idx], -1.0) if idx < len(prices) else -1.0
        outcomes.append(
            Outcome(
                name=name,
                price=None if price < 0 else price,
                token_id=tokens[idx] if idx < len(tokens) else "",
            )
        )

    return Market(
        id=str(raw.get("id") or ""),
        question=clean_text(raw.get("question") or raw.get("title")) or "Unknown",
        slug=clean_slug(raw.get("slug")),
        volume_24h=_as_float(raw.get("volume24hr")),
        liquidity=_as_float(raw.get("liquidityNum") or raw.get("liquidity")),
        end_date=str(raw.get("endDate") or ""),
        closed=bool(raw.get("closed")),
        outcomes=outcomes,
    )


def _get(path: str, params: Dict[str, Any]) -> Any:
    """GET on Gamma with the shared layer's retry/backoff."""
    try:
        return get_json(GAMMA_API, path, params, timeout=HTTP_TIMEOUT,
                        label="Gamma API")
    except ApiError as exc:
        raise MarketError(str(exc), exc.status) from exc


def trending(limit: int = 10, min_volume: float = 0.0) -> List[Market]:
    """Active markets ordered by 24h volume."""
    limit = max(1, min(int(limit), PAGE_SIZE))
    raw = _get(
        "/markets",
        {
            "limit": limit,
            "active": "true",
            "closed": "false",
            "order": "volume24hr",
            "ascending": "false",
        },
    )
    rows = raw if isinstance(raw, list) else raw.get("data", [])
    markets = [parse_market(m) for m in rows if isinstance(m, dict)]
    if min_volume > 0:
        markets = [m for m in markets if m.volume_24h >= min_volume]
    return markets[:limit]


def _search_via_public_endpoint(query: str, limit: int) -> List[Market]:
    """Server-side text search (/public-search)."""
    payload = _get("/public-search", {"q": query, "limit_per_type": limit * 2})
    if not isinstance(payload, dict):
        return []

    found: List[Market] = []
    seen: set[str] = set()

    def absorb(raw: Dict[str, Any]) -> None:
        market = parse_market(raw)
        if market.closed or not market.id or market.id in seen:
            return
        seen.add(market.id)
        found.append(market)

    # The response groups by type; markets can arrive loose or inside events.
    for row in payload.get("markets") or []:
        if isinstance(row, dict):
            absorb(row)
    for event in payload.get("events") or []:
        if not isinstance(event, dict):
            continue
        for row in event.get("markets") or []:
            if isinstance(row, dict):
                absorb(row)

    return found[:limit]


def _search_via_pagination(query: str, limit: int) -> List[Market]:
    """Fallback: paginate the active markets and filter on the client.

    This is what fixes the v1.0.2 bug — before, only the first page (the size
    of `limit`!) was examined.
    """
    needle = query.lower()
    found: List[Market] = []
    for page in range(MAX_PAGES):
        raw = _get(
            "/markets",
            {
                "limit": PAGE_SIZE,
                "offset": page * PAGE_SIZE,
                "active": "true",
                "closed": "false",
                "order": "volume24hr",
                "ascending": "false",
            },
        )
        rows = raw if isinstance(raw, list) else raw.get("data", [])
        if not rows:
            break
        for row in rows:
            if not isinstance(row, dict):
                continue
            haystack = " ".join(
                str(row.get(k) or "") for k in ("question", "slug", "description")
            ).lower()
            if needle in haystack:
                found.append(parse_market(row))
                if len(found) >= limit:
                    return found
        if len(rows) < PAGE_SIZE:
            break
    return found


def search_markets(query: Optional[str] = None, limit: int = 10,
                   min_volume: float = 0.0) -> List[Market]:
    """Search markets. Without a `query`, returns the most-traded ones."""
    limit = max(1, min(int(limit), 100))
    if not query or not query.strip():
        return trending(limit, min_volume)

    query = query.strip()
    try:
        results = _search_via_public_endpoint(query, limit)
    except MarketError:
        results = []
    if not results:
        results = _search_via_pagination(query, limit)

    if min_volume > 0:
        results = [m for m in results if m.volume_24h >= min_volume]
    return results[:limit]


def get_market(market_id: str) -> Optional[Market]:
    """Fetch a specific market by numeric id or slug."""
    market_id = str(market_id).strip()
    if not market_id:
        return None
    params: Dict[str, Any] = (
        {"id": market_id} if market_id.isdigit() else {"slug": market_id}
    )
    params["limit"] = 1
    raw = _get("/markets", params)
    rows = raw if isinstance(raw, list) else raw.get("data", [])
    for row in rows:
        if isinstance(row, dict):
            return parse_market(row)
    return None
