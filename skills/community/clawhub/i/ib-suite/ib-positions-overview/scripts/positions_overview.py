# skills/ib-suite/ib-positions-overview/scripts/positions_overview.py
"""/ib-positions-overview entrypoint: read-only, enriched positions overview.

Reads every open position and turns it into the line a holder actually wants:
symbol, instrument name, asset type, quantity, long/short, average cost,
current price, market value, unrealized P&L, unrealized return, account weight,
industry, market/country, and pricing currency. It then ranks positions four
ways (market value, profit, loss, weight) and flags the single most
concentrated name — all computed deterministically here so the result is
testable and reproducible, not re-derived by a caller.

The live IB connection is isolated behind `client_factory` so build_positions()
and the ranking helpers are fully testable against fixtures. This module NEVER
imports order-placing APIs — read-only by construction.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone

from ib_common.config import load_config, resolve_base_currency
from ib_common.schema import PositionView, PositionsOverview


# IB listing exchange (primaryExchange) -> human country/market label. Covers the
# venues this toolchain sees; unknown exchanges leave country "" rather than guess.
_MARKET_COUNTRY = {
    "NASDAQ": "United States", "NYSE": "United States", "ARCA": "United States",
    "AMEX": "United States", "BATS": "United States", "PINK": "United States",
    "ISLAND": "United States",
    "SGX": "Singapore",
    "SEHK": "Hong Kong", "HKFE": "Hong Kong",
    "TSE": "Japan",
    "LSE": "United Kingdom",
    "SMART": "",   # SMART is a router, not a country; leave unmapped
}


def _country_for(market: str) -> str:
    """Map an IB listing exchange to a country label; "" when unknown."""
    return _MARKET_COUNTRY.get(market.upper(), "") if market else ""


def build_positions(raw: dict, ts: datetime) -> PositionsOverview:
    """Convert a raw account+positions dict into a typed PositionsOverview.

    `raw["positions"]` rows carry IB-computed `market_value`/`unrealized_pnl`
    (already multiplier-correct for options) plus descriptive fields. All values
    are taken verbatim from IB — no price or P&L is fabricated here. The account
    `weight` is filled in against net liquidation so ranking never re-derives it.
    """
    a = raw["account"]
    net_liq = float(a["net_liquidation"])
    denom = net_liq or 1.0   # avoid divide-by-zero on an empty/paper account

    views: list[PositionView] = []
    for p in raw["positions"]:
        fx = float(p.get("fx_rate", 1.0))
        market_value = float(p["market_value"])
        market = p.get("market", "")
        views.append(PositionView(
            account_id=a["account_id"],
            symbol=p["symbol"],
            name=p.get("name", ""),
            sec_type=p["sec_type"],
            quantity=float(p["quantity"]),
            avg_cost=float(p["avg_cost"]),
            market_price=float(p["market_price"]),
            market_value=market_value,
            unrealized_pnl=float(p["unrealized_pnl"]),
            currency=p["currency"],
            industry=p.get("industry", ""),
            market=market,
            country=p.get("country") or _country_for(market),
            fx_rate=fx,
            weight=(market_value * fx) / denom,
        ))

    return PositionsOverview(
        account_id=a["account_id"],
        base_currency=a["base_currency"],
        net_liquidation=net_liq,
        positions=views,
        ts=ts,
    )


# --- deterministic ranking views (all use base-currency values) --------------

def by_market_value(positions: list[PositionView]) -> list[PositionView]:
    """Positions by base-currency market value, high to low."""
    return sorted(positions, key=lambda p: p.base_value, reverse=True)


def by_profit(positions: list[PositionView]) -> list[PositionView]:
    """Positions by base-currency unrealized P&L, profit high to low."""
    return sorted(positions, key=lambda p: p.base_unrealized_pnl, reverse=True)


def by_loss(positions: list[PositionView]) -> list[PositionView]:
    """Positions by loss amount, biggest loss first (most negative P&L)."""
    return sorted(positions, key=lambda p: p.base_unrealized_pnl)


def by_weight(positions: list[PositionView]) -> list[PositionView]:
    """Positions by account weight, high to low (signed: shorts sort last)."""
    return sorted(positions, key=lambda p: p.weight, reverse=True)


def top_concentration(positions: list[PositionView]) -> PositionView | None:
    """The single most concentrated position by absolute account weight."""
    if not positions:
        return None
    return max(positions, key=lambda p: abs(p.weight))


def _default_client_factory(cfg):
    """Build a read-only IB Gateway client. Imported lazily to keep tests offline."""
    from ib_async import IB  # local import: no network dependency at import time

    class _LiveClient:
        def __init__(self, cfg):
            self.cfg = cfg
            self.ib = IB()
            self.ib.connect(cfg.connection.host, cfg.connection.port,
                            clientId=cfg.connection.client_id,
                            readonly=True)   # hard read-only

        def _exchange_rates(self) -> dict[str, float]:
            """currency -> local->base rate from IB's `$LEDGER-ExchangeRate` rows."""
            rates: dict[str, float] = {}
            for v in self.ib.accountValues():
                if (v.tag == "$LEDGER-ExchangeRate" and v.currency
                        and v.currency != "BASE"):
                    try:
                        rates[v.currency] = float(v.value)
                    except (TypeError, ValueError):
                        continue
            return rates

        def _describe(self, contract) -> dict:
            """Best-effort name/industry/market via read-only reqContractDetails.

            Never raises: a name IB cannot describe simply keeps blank
            descriptive fields rather than failing the whole overview.
            """
            try:
                details = self.ib.reqContractDetails(contract)
            except Exception:
                details = None
            if not details:
                return {"name": "", "industry": ""}
            d = details[0]
            return {"name": d.longName or "", "industry": d.industry or ""}

        def fetch_raw(self) -> dict:
            acct_id = self.ib.managedAccounts()[0]
            summary = {v.tag: v.value for v in self.ib.accountValues(acct_id)}
            fx = self._exchange_rates()

            positions = []
            # portfolio() carries IB-computed marketPrice/marketValue/unrealizedPNL
            # (multiplier-correct for options) — we never recompute those here.
            for item in self.ib.portfolio(acct_id):
                c = item.contract
                desc = self._describe(c)
                positions.append({
                    "symbol": c.symbol,
                    "name": desc["name"],
                    "sec_type": c.secType,
                    "currency": c.currency,
                    "quantity": item.position,
                    "avg_cost": item.averageCost,
                    "market_price": item.marketPrice,
                    "market_value": item.marketValue,
                    "unrealized_pnl": item.unrealizedPNL,
                    "industry": desc["industry"],
                    "market": c.primaryExchange or c.exchange or "",
                    "fx_rate": fx.get(c.currency, 1.0),   # base currency -> 1.0
                })

            return {
                "account": {
                    "account_id": acct_id,
                    "base_currency": summary.get("Currency", "USD"),
                    "net_liquidation": float(summary.get("NetLiquidation", 0) or 0),
                },
                "positions": positions,
            }

        def disconnect(self):
            self.ib.disconnect()

    return _LiveClient(cfg)


def positions_overview(cfg_path: str, client_factory=None, now=None) -> dict:
    """Load config, pull read-only positions, return a plain dict.

    The dict carries the enriched positions plus all four rankings (as symbol
    lists) and the top-concentration call-out, so callers render directly
    without re-deriving any ordering.
    """
    cfg = load_config(cfg_path)
    now = now or (lambda: datetime.now(timezone.utc))
    client_factory = client_factory or _default_client_factory

    client = client_factory(cfg)
    try:
        raw = client.fetch_raw()
    finally:
        client.disconnect()

    # enforce base-currency policy (account wins over config)
    raw["account"]["base_currency"] = resolve_base_currency(
        cfg, raw["account"].get("base_currency"))

    ov = build_positions(raw, now())
    top = top_concentration(ov.positions)
    result = ov.model_dump(mode="json")
    result["rankings"] = {
        "by_market_value": [p.symbol for p in by_market_value(ov.positions)],
        "by_profit": [p.symbol for p in by_profit(ov.positions)],
        "by_loss": [p.symbol for p in by_loss(ov.positions)],
        "by_weight": [p.symbol for p in by_weight(ov.positions)],
    }
    result["top_concentration"] = top.model_dump(mode="json") if top else None
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Read-only enriched positions overview from IB Gateway.")
    parser.add_argument("--config", required=True, help="path to config.yaml")
    args = parser.parse_args()
    import json
    print(json.dumps(positions_overview(args.config), indent=2, ensure_ascii=False))
