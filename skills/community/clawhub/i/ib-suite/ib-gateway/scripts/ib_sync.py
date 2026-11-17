# skills/ib-gateway/scripts/ib_sync.py
"""/ib-sync entrypoint: pull read-only account + positions and land to the lake.

The live connection is isolated behind `client_factory` so business logic
(build_snapshot, storage) is fully testable against fixtures. This module
NEVER imports order-placing APIs — read-only by construction.
"""
from __future__ import annotations
import argparse
import math
from datetime import datetime, timezone
from pathlib import Path

from ib_common.config import load_config, resolve_base_currency
from ib_common.schema import Account, Position, Snapshot
from ib_common.storage import write_snapshot, append_timeseries


def _resolve_market_price(live_price: float | None, avg_cost: float,
                          close_price: float | None = None) -> float:
    """Pick a usable mark: live trade, else prior close, else cost basis.

    IB returns NaN (or nothing) for a side with no data. Off-hours or on a
    delayed feed there is often no last/bid/ask but a valid prior `close`; that
    close is a far better mark than the cost basis. Only when neither a live
    price nor a close is usable do we fall back to avg_cost — which makes that
    name's unrealized P&L 0 rather than fabricating a number.
    """
    def _ok(x: float | None) -> bool:
        return x is not None and math.isfinite(x) and x > 0.0

    if _ok(live_price):
        return float(live_price)
    if _ok(close_price):
        return float(close_price)
    return avg_cost


# config string -> IB reqMarketDataType code (see IB API tick_types docs)
_MARKET_DATA_TYPES = {"realtime": 1, "frozen": 2, "delayed": 3, "delayed_frozen": 4}


def _market_data_type_code(mode: str) -> int:
    """Map a config market_data_type string to its IB numeric code.

    Unknown modes raise rather than silently defaulting — a typo in config
    should surface, not quietly change which prices you get.
    """
    try:
        return _MARKET_DATA_TYPES[mode]
    except KeyError:
        raise ValueError(
            f"unknown market_data_type {mode!r}; "
            f"expected one of {sorted(_MARKET_DATA_TYPES)}")


def _exchange_rates(account_values) -> dict[str, float]:
    """Map each currency to its local->base exchange rate from IB's ledger.

    IB publishes a per-currency `$LEDGER-ExchangeRate` row (e.g. SGD -> 0.775,
    USD -> 1.0). We take it verbatim — it is the same rate IB uses internally
    to report NetLiquidation, so downstream base-currency sums reconcile with
    the account. The synthetic `BASE` summary currency is skipped; a position's
    own currency (USD/SGD/...) is what we look up later.
    """
    rates: dict[str, float] = {}
    for v in account_values:
        if v.tag == "$LEDGER-ExchangeRate" and v.currency and v.currency != "BASE":
            try:
                rates[v.currency] = float(v.value)
            except (TypeError, ValueError):
                continue
    return rates


def build_snapshot(raw: dict, ts: datetime) -> Snapshot:
    """Convert a raw account+positions dict into a typed, base-currency-checked Snapshot."""
    acct_raw = raw["account"]
    base = acct_raw.get("base_currency")
    account = Account(
        account_id=acct_raw["account_id"],
        base_currency=base,
        net_liquidation=float(acct_raw["net_liquidation"]),
        total_cash=float(acct_raw["total_cash"]),
        buying_power=float(acct_raw["buying_power"]),
        ts=ts,
    )
    positions: list[Position] = []
    for p in raw["positions"]:
        mkt_val = float(p["quantity"]) * float(p["market_price"])
        cost_val = float(p["quantity"]) * float(p["avg_cost"])
        positions.append(Position(
            account_id=account.account_id,
            symbol=p["symbol"],
            sec_type=p["sec_type"],
            currency=p["currency"],
            quantity=float(p["quantity"]),
            avg_cost=float(p["avg_cost"]),
            market_price=float(p["market_price"]),
            market_value=mkt_val,
            unrealized_pnl=mkt_val - cost_val,
            fx_rate=float(p.get("fx_rate", 1.0)),   # local -> base; 1.0 if absent
        ))
    return Snapshot(account=account, positions=positions, ts=ts)


def _default_client_factory(cfg):
    """Build a read-only IB Gateway client. Imported lazily to keep tests offline."""
    from ib_async import IB  # local import: no network dependency at import time

    class _LiveClient:
        def __init__(self, cfg):
            self.cfg = cfg
            self._mktdata_wait_s = 5.0   # window for (delayed) ticks to arrive
            self.ib = IB()
            self.ib.connect(cfg.connection.host, cfg.connection.port,
                            clientId=cfg.connection.client_id,
                            readonly=True)   # hard read-only
            # Ask for the configured tier (default: delayed) so accounts without
            # a live market-data subscription still get usable marks.
            self.ib.reqMarketDataType(
                _market_data_type_code(cfg.connection.market_data_type))

        def _live_prices(self, contracts) -> dict[int, tuple[float, float]]:
            """conId -> (market price, prior close), best-effort.

            Never blocks forever, never raises. We stream-subscribe every
            contract, wait a fixed window, then read whatever each ticker has
            received — we do NOT require every ticker to be "ready". That matters
            because names without a live subscription never report a trade price
            on a delayed feed, which would otherwise stall a batch reqTickers
            until timeout and yield nothing. Missing names fall back to close,
            then avg_cost. Subscriptions are always cancelled (read-only pull).
            """
            if not contracts:
                return {}
            tickers = []
            try:
                for c in contracts:
                    tickers.append(self.ib.reqMktData(c, "", False, False))
                self.ib.sleep(self._mktdata_wait_s)   # let delayed ticks arrive
                return {t.contract.conId: (t.marketPrice(), t.close)
                        for t in tickers}
            except Exception:
                return {}   # caller falls back to avg_cost for everything
            finally:
                for c in contracts:
                    try:
                        self.ib.cancelMktData(c)
                    except Exception:
                        pass

        def fetch_raw(self) -> dict:
            summary = {v.tag: v.value for v in self.ib.accountSummary()}
            acct_id = self.ib.managedAccounts()[0]
            ib_positions = list(self.ib.positions())

            # Per-currency local->base FX from IB's ledger (no market-data sub needed).
            fx = _exchange_rates(self.ib.accountValues())

            # Read-only market-data pull; still no order path is ever touched.
            live_by_conid = self._live_prices([p.contract for p in ib_positions])

            positions = []
            for p in ib_positions:
                c = p.contract
                live, close = live_by_conid.get(c.conId, (None, None))
                mkt_price = _resolve_market_price(live, p.avgCost, close)
                positions.append({
                    "symbol": c.symbol, "sec_type": c.secType,
                    "currency": c.currency, "quantity": p.position,
                    "avg_cost": p.avgCost,
                    "market_price": mkt_price,
                    "fx_rate": fx.get(c.currency, 1.0),   # base currency -> 1.0
                })
            return {
                "account": {
                    "account_id": acct_id,
                    "base_currency": summary.get("Currency", "USD"),
                    "net_liquidation": float(summary.get("NetLiquidation", 0)),
                    "total_cash": float(summary.get("TotalCashValue", 0)),
                    "buying_power": float(summary.get("BuyingPower", 0)),
                },
                "positions": positions,
            }

        def disconnect(self):
            self.ib.disconnect()

    return _LiveClient(cfg)


def sync(cfg_path: str, client_factory=None, now=None) -> dict:
    """Load config, pull data via a read-only client, land snapshot + time-series."""
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

    snap = build_snapshot(raw, now())
    snap_path = write_snapshot(snap, cfg.storage.root)
    ts_path = append_timeseries(snap.positions, cfg.storage.root, "positions_history")
    return {"snapshot": str(snap_path), "timeseries": str(ts_path)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync read-only IB data to the local lake.")
    parser.add_argument("--config", required=True, help="path to config.yaml")
    args = parser.parse_args()
    result = sync(args.config)
    print(result)
