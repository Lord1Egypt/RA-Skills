# skills/ib-suite/ib-daily-pnl/scripts/daily_pnl.py
"""/ib-daily-pnl entrypoint: read-only daily (today's) P&L breakdown.

Answers "how did my account do today, and who moved it?" in one call: the
account's total daily P&L split into realized and unrealized, then every
position's contribution ranked into winners and losers, aggregated by asset
class (stock / option / ETF / forex / …) and by trading currency, with the
single position that moved today's number the most flagged.

Daily P&L is an IB *session* concept (it resets every trading day) that lives
only on a live connection — it is NOT in the data-lake snapshot. So this skill
connects directly, `readonly=True`, reads IB's `pnl` subscription
(`reqPnL` for account totals, `reqPnLSingle` per position), and persists
nothing. IB reports every P&L figure already in the account base currency, so
contributions sum directly with no FX step here.

The live connection is isolated behind `client_factory` so build_daily_pnl()
and the ranking helpers are fully testable against fixtures. This module NEVER
imports order-placing APIs — read-only by construction.
"""
from __future__ import annotations
import argparse
import math
from datetime import datetime, timezone

from ib_common.config import load_config, resolve_base_currency
from ib_common.schema import DailyPnLPosition, DailyPnLOverview


# IB's `pnl`/`pnlSingle` subscriptions report an *unset* figure as Double.MAX_VALUE
# (~1.7977e308), not None or NaN — e.g. realizedPnL for a name with no closing
# trade today. Passing that sentinel through would fabricate a nonsense number,
# so we map "unavailable" to 0.0 (no realized P&L today == 0).
def _clean_pnl(x) -> float:
    """Return a usable float, mapping IB's Double.MAX_VALUE / None / NaN to 0.0."""
    if x is None:
        return 0.0
    try:
        v = float(x)
    except (TypeError, ValueError):
        return 0.0
    if not math.isfinite(v) or abs(v) >= 1e300:   # NaN/inf or the DBL_MAX sentinel
        return 0.0
    return v


# The honest boundary for the "price vs vol vs theta vs FX" question. A single
# read-only pull gives each name's *net* daily P&L, not its Greek/FX decomposition
# — that needs day-over-day Greeks and FX history this snapshot does not carry.
# Shipped as a structural field of the output, never as a fabricated split.
_ATTRIBUTION_NOTE = (
    "Daily P&L is reported per position and per asset class as a net figure. "
    "Decomposing each name into price change vs. implied-volatility change vs. "
    "time-value decay (theta) vs. FX change requires day-over-day Greeks and "
    "exchange-rate history, which a single read-only pull does not contain. "
    "Asset-class buckets are a proxy: option P&L blends price/vol/theta, forex "
    "P&L is FX, stock/ETF P&L is price. No split is fabricated beyond that."
)


def build_daily_pnl(raw: dict, ts: datetime) -> DailyPnLOverview:
    """Convert a raw account+per-position daily-P&L dict into a typed overview.

    `raw["account"]` holds the base-currency daily/realized/unrealized totals
    from IB's account `pnl` subscription; `raw["positions"]` rows carry each
    name's own daily/realized/unrealized P&L (also base currency). Values are
    taken from IB and only sanitized via `_clean_pnl` (IB's unset sentinel /
    NaN -> 0.0); no P&L is otherwise fabricated or re-derived here.
    """
    a = raw["account"]
    positions = [
        DailyPnLPosition(
            account_id=a["account_id"],
            symbol=p["symbol"],
            name=p.get("name", ""),
            sec_type=p["sec_type"],
            stock_type=p.get("stock_type", ""),
            currency=p["currency"],
            daily_pnl=_clean_pnl(p["daily_pnl"]),
            unrealized_pnl=_clean_pnl(p["unrealized_pnl"]),
            realized_pnl=_clean_pnl(p["realized_pnl"]),
        )
        for p in raw["positions"]
    ]
    return DailyPnLOverview(
        account_id=a["account_id"],
        base_currency=a["base_currency"],
        daily_pnl=_clean_pnl(a["daily_pnl"]),
        unrealized_pnl=_clean_pnl(a["unrealized_pnl"]),
        realized_pnl=_clean_pnl(a["realized_pnl"]),
        positions=positions,
        ts=ts,
    )


# --- deterministic ranking / attribution views (all base-currency) -----------

def by_profit_contrib(positions: list[DailyPnLPosition]) -> list[DailyPnLPosition]:
    """Winners first: today's P&L high to low."""
    return sorted(positions, key=lambda p: p.daily_pnl, reverse=True)


def by_loss_contrib(positions: list[DailyPnLPosition]) -> list[DailyPnLPosition]:
    """Losers first: today's P&L most negative first."""
    return sorted(positions, key=lambda p: p.daily_pnl)


def by_asset_class(positions: list[DailyPnLPosition]) -> dict[str, float]:
    """Sum today's P&L per asset class (Stock/ETF/Option/Forex/…)."""
    out: dict[str, float] = {}
    for p in positions:
        out[p.asset_class] = out.get(p.asset_class, 0.0) + p.daily_pnl
    return out


def by_currency(positions: list[DailyPnLPosition]) -> dict[str, float]:
    """Sum today's P&L per trading currency."""
    out: dict[str, float] = {}
    for p in positions:
        out[p.currency] = out.get(p.currency, 0.0) + p.daily_pnl
    return out


def top_pnl_driver(positions: list[DailyPnLPosition]) -> DailyPnLPosition | None:
    """The single position moving today's P&L the most (largest |daily_pnl|)."""
    if not positions:
        return None
    return max(positions, key=lambda p: abs(p.daily_pnl))


def _default_client_factory(cfg):
    """Build a read-only IB Gateway client. Imported lazily to keep tests offline."""
    from ib_async import IB  # local import: no network dependency at import time

    class _LiveClient:
        def __init__(self, cfg):
            self.cfg = cfg
            self._pnl_wait_s = 4.0   # window for the pnl subscriptions to populate
            self.ib = IB()
            self.ib.connect(cfg.connection.host, cfg.connection.port,
                            clientId=cfg.connection.client_id,
                            readonly=True)   # hard read-only

        def _describe(self, contract) -> dict:
            """Best-effort long name + stockType via read-only reqContractDetails.

            Never raises: a name IB cannot describe keeps blank descriptive
            fields (so its asset class falls back to raw sec_type) rather than
            failing the whole report.
            """
            try:
                details = self.ib.reqContractDetails(contract)
            except Exception:
                details = None
            if not details:
                return {"name": "", "stock_type": ""}
            d = details[0]
            return {"name": d.longName or "",
                    "stock_type": getattr(d, "stockType", "") or ""}

        def fetch_raw(self) -> dict:
            acct_id = self.ib.managedAccounts()[0]

            # Account-level daily/realized/unrealized totals from the pnl
            # subscription (base currency); always cancelled after reading.
            acct_pnl = self.ib.reqPnL(acct_id)
            positions = []
            singles: dict = {}   # conId -> (pnl_single, contract); cancelled in finally
            try:
                self.ib.sleep(self._pnl_wait_s)
                # Sanitizing (IB's unset sentinel -> 0) happens once in
                # build_daily_pnl; pass the raw subscription values through here.
                a_daily = acct_pnl.dailyPnL
                a_unreal = acct_pnl.unrealizedPnL
                a_real = acct_pnl.realizedPnL

                # Per-position daily P&L needs conId; reqPnLSingle publishes
                # dailyPnL/unrealizedPnL/realizedPnL already in base currency.
                for p in self.ib.positions(acct_id):
                    c = p.contract
                    single = self.ib.reqPnLSingle(acct_id, "", c.conId)
                    singles[c.conId] = (single, c)
                self.ib.sleep(self._pnl_wait_s)   # let the single-position pnl arrive

                for conid, (single, c) in singles.items():
                    desc = self._describe(c)
                    positions.append({
                        "symbol": c.symbol,
                        "name": desc["name"],
                        "sec_type": c.secType,
                        "stock_type": desc["stock_type"],
                        "currency": c.currency,
                        "daily_pnl": single.dailyPnL,
                        "unrealized_pnl": single.unrealizedPnL,
                        "realized_pnl": single.realizedPnL,
                    })
            finally:
                # Always cancel every pnl subscription we opened (read-only pull).
                try:
                    self.ib.cancelPnL(acct_id)
                except Exception:
                    pass
                for conid in singles:
                    try:
                        self.ib.cancelPnLSingle(acct_id, "", conid)
                    except Exception:
                        pass

            summary = {v.tag: v.value for v in self.ib.accountValues(acct_id)}
            return {
                "account": {
                    "account_id": acct_id,
                    "base_currency": summary.get("Currency", "USD"),
                    "daily_pnl": a_daily,
                    "unrealized_pnl": a_unreal,
                    "realized_pnl": a_real,
                },
                "positions": positions,
            }

        def disconnect(self):
            self.ib.disconnect()

    return _LiveClient(cfg)


def daily_pnl(cfg_path: str, client_factory=None, now=None) -> dict:
    """Load config, pull read-only daily P&L, return a plain dict.

    The dict carries the account totals plus both rankings (winners/losers as
    symbol lists), the asset-class and per-currency attribution (with the honest
    decomposition note), and the single top driver — so callers render directly
    without re-deriving any ordering or fabricating a Greek/FX split.
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

    ov = build_daily_pnl(raw, now())
    result = ov.model_dump(mode="json")
    result["rankings"] = {
        "by_profit_contrib": [p.symbol for p in by_profit_contrib(ov.positions)],
        "by_loss_contrib": [p.symbol for p in by_loss_contrib(ov.positions)],
    }
    result["attribution"] = {
        "by_asset_class": by_asset_class(ov.positions),
        "by_currency": by_currency(ov.positions),
        "note": _ATTRIBUTION_NOTE,
    }

    top = top_pnl_driver(ov.positions)
    if top is not None:
        gross = sum(abs(p.daily_pnl) for p in ov.positions) or 1.0
        td = top.model_dump(mode="json")
        td["share_of_gross"] = abs(top.daily_pnl) / gross
        result["top_driver"] = td
    else:
        result["top_driver"] = None
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Read-only daily (today's) P&L breakdown from IB Gateway.")
    parser.add_argument("--config", required=True, help="path to config.yaml")
    args = parser.parse_args()
    import json
    print(json.dumps(daily_pnl(args.config), indent=2, ensure_ascii=False))
