# skills/ib-suite/ib-account-overview/scripts/account_overview.py
"""/ib-account-overview entrypoint: read-only account financial overview.

Pulls the account-level figures a trader checks first — net liquidation, cash,
buying power, margin, excess liquidity, and daily/unrealized/realized P&L —
plus a per-currency balance breakdown converted into the account base currency.

The live IB connection is isolated behind `client_factory` so build_overview()
and the orchestration are fully testable against fixtures. This module NEVER
imports order-placing APIs — read-only by construction.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone

from ib_common.config import load_config, resolve_base_currency
from ib_common.schema import AccountOverview, CurrencyBalance


def build_overview(raw: dict, ts: datetime) -> AccountOverview:
    """Convert a raw account-overview dict into a typed AccountOverview.

    `raw["account"]` holds base-currency scalars; `raw["currency_balances"]`
    is a list of per-currency rows carrying their own local->base rate. All
    values are taken verbatim from IB — no figure is fabricated here.
    """
    a = raw["account"]
    balances = [
        CurrencyBalance(
            currency=b["currency"],
            cash_balance=float(b["cash_balance"]),
            net_liquidation=float(b["net_liquidation"]),
            exchange_rate=float(b.get("exchange_rate", 1.0)),
        )
        for b in raw.get("currency_balances", [])
    ]
    return AccountOverview(
        account_id=a["account_id"],
        base_currency=a["base_currency"],
        net_liquidation=float(a["net_liquidation"]),
        total_cash=float(a["total_cash"]),
        buying_power=float(a["buying_power"]),
        margin_used=float(a["margin_used"]),
        init_margin_req=float(a["init_margin_req"]),
        maint_margin_req=float(a["maint_margin_req"]),
        available_funds=float(a["available_funds"]),
        excess_liquidity=float(a["excess_liquidity"]),
        gross_position_value=float(a["gross_position_value"]),
        daily_pnl=float(a["daily_pnl"]),
        unrealized_pnl=float(a["unrealized_pnl"]),
        realized_pnl=float(a["realized_pnl"]),
        currency_balances=balances,
        ts=ts,
    )


def _currency_balances(account_values) -> dict[str, dict]:
    """Group IB's per-currency ledger rows into {currency: {tag: value}}.

    IB publishes cash/net-liq/exchange-rate per currency under `$LEDGER-*`
    tags (e.g. SGD -> ExchangeRate 0.7747). The synthetic `BASE` summary row is
    skipped; a real currency (USD/SGD/...) is what we report.
    """
    rows: dict[str, dict] = {}
    wanted = {
        "$LEDGER-CashBalance": "cash_balance",
        "$LEDGER-NetLiquidationByCurrency": "net_liquidation",
        "$LEDGER-ExchangeRate": "exchange_rate",
    }
    for v in account_values:
        key = wanted.get(v.tag)
        if key and v.currency and v.currency != "BASE":
            try:
                rows.setdefault(v.currency, {})[key] = float(v.value)
            except (TypeError, ValueError):
                continue
    return rows


def _default_client_factory(cfg):
    """Build a read-only IB Gateway client. Imported lazily to keep tests offline."""
    from ib_async import IB  # local import: no network dependency at import time

    class _LiveClient:
        def __init__(self, cfg):
            self.cfg = cfg
            self._pnl_wait_s = 3.0   # window for the pnl subscription to populate
            self.ib = IB()
            self.ib.connect(cfg.connection.host, cfg.connection.port,
                            clientId=cfg.connection.client_id,
                            readonly=True)   # hard read-only

        def fetch_raw(self) -> dict:
            acct_id = self.ib.managedAccounts()[0]
            # Account-level scalars: last value per tag (base currency).
            summary = {v.tag: v.value for v in self.ib.accountValues(acct_id)}

            def _f(tag: str) -> float:
                try:
                    return float(summary.get(tag, 0) or 0)
                except (TypeError, ValueError):
                    return 0.0

            # Daily/unrealized/realized P&L come from the pnl subscription, not
            # accountValues. Always cancel it (read-only pull).
            pnl = self.ib.reqPnL(acct_id)
            try:
                self.ib.sleep(self._pnl_wait_s)
                daily = float(pnl.dailyPnL) if pnl.dailyPnL is not None else 0.0
                unreal = float(pnl.unrealizedPnL) if pnl.unrealizedPnL is not None else 0.0
                real = float(pnl.realizedPnL) if pnl.realizedPnL is not None else 0.0
            finally:
                try:
                    self.ib.cancelPnL(acct_id)
                except Exception:
                    pass

            ledger = _currency_balances(self.ib.accountValues(acct_id))
            balances = [
                {"currency": ccy,
                 "cash_balance": d.get("cash_balance", 0.0),
                 "net_liquidation": d.get("net_liquidation", 0.0),
                 "exchange_rate": d.get("exchange_rate", 1.0)}
                for ccy, d in sorted(ledger.items())
            ]

            return {
                "account": {
                    "account_id": acct_id,
                    "base_currency": summary.get("Currency", "USD"),
                    "net_liquidation": _f("NetLiquidation"),
                    "total_cash": _f("TotalCashValue"),
                    "buying_power": _f("BuyingPower"),
                    "margin_used": _f("MaintMarginReq"),
                    "init_margin_req": _f("FullInitMarginReq"),
                    "maint_margin_req": _f("FullMaintMarginReq"),
                    "available_funds": _f("AvailableFunds"),
                    "excess_liquidity": _f("ExcessLiquidity"),
                    "gross_position_value": _f("GrossPositionValue"),
                    "daily_pnl": daily,
                    "unrealized_pnl": unreal,
                    "realized_pnl": real,
                },
                "currency_balances": balances,
            }

        def disconnect(self):
            self.ib.disconnect()

    return _LiveClient(cfg)


def overview(cfg_path: str, client_factory=None, now=None) -> dict:
    """Load config, pull a read-only account overview, return a plain dict."""
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

    ov = build_overview(raw, now())
    return ov.model_dump(mode="json")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Read-only account financial overview from IB Gateway.")
    parser.add_argument("--config", required=True, help="path to config.yaml")
    args = parser.parse_args()
    import json
    print(json.dumps(overview(args.config), indent=2, ensure_ascii=False))
