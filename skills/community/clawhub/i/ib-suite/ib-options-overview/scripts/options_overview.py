"""Read-only IB option acquisition and deterministic risk overview mapping."""
from __future__ import annotations

import argparse
from collections import defaultdict
from collections.abc import Callable
from datetime import date, datetime, timezone
import json
import math

from ib_common.config import load_config, resolve_base_currency

from ib_common.schema import (
    OptionExpirationBucket,
    OptionGreekCoverage,
    OptionPositionView,
    OptionUnderlyingConcentration,
    OptionsOverview,
    OptionsOverviewSummary,
)


_GREEKS = ("delta", "gamma", "theta", "vega")

_MARKET_DATA_DISABLED_LIMITATION = (
    "market data disabled (options.fetch_market_data=false) to avoid IBKR "
    "snapshot fees; Greeks, IV, underlying price and moneyness are unavailable"
)


def classify_moneyness(
    right: str, strike: float, underlying_price: float | None
) -> str | None:
    """Classify an option using the observed underlying price."""
    if right not in {"CALL", "PUT"}:
        raise ValueError(f"unsupported option right: {right!r}")
    if underlying_price is None:
        return None
    if underlying_price == strike:
        return "ATM"
    if right == "CALL":
        return "ITM" if underlying_price > strike else "OTM"
    return "ITM" if underlying_price < strike else "OTM"


def _scaled_greek(position: OptionPositionView, name: str) -> float | None:
    """Return the signed, contract-multiplier-adjusted Greek when available."""
    value = getattr(position, name)
    if value is None or position.fx_rate is None:
        return None
    return value * position.quantity * position.multiplier * position.fx_rate


def _contract_identifier(position: OptionPositionView) -> str:
    """Build the stable underlying, expiry, and strike identifier for coverage."""
    return (
        f"{position.underlying_symbol} {position.expiry_date.isoformat()} "
        f"{position.strike:g}"
    )


def _finite_float(value: object) -> float | None:
    """Return a finite numeric value or null for IB's unavailable sentinels."""
    if value is None:
        return None
    number = float(value)
    return number if math.isfinite(number) else None


def _parse_multiplier(raw_multiplier: object, contract_id: str) -> int:
    """Parse a positive whole-number contract multiplier."""
    try:
        numeric = float(raw_multiplier)
    except (TypeError, ValueError) as error:
        raise ValueError(
            f"{contract_id}: invalid multiplier {raw_multiplier!r}"
        ) from error
    if not numeric.is_integer() or numeric <= 0:
        raise ValueError(f"{contract_id}: invalid multiplier {raw_multiplier!r}")
    return int(numeric)


def _parse_expiry(raw_expiry: object, contract_id: str) -> date:
    """Parse an ISO option expiry date with contract-specific diagnostics."""
    try:
        return date.fromisoformat(str(raw_expiry))
    except (TypeError, ValueError) as error:
        raise ValueError(f"{contract_id}: invalid expiry_date {raw_expiry!r}") from error


def _limitations_for(position: OptionPositionView) -> list[str]:
    """Describe every unavailable data field needed for risk interpretation."""
    identifier = _contract_identifier(position)
    limitations: list[str] = []
    missing_greeks = [name for name in _GREEKS if getattr(position, name) is None]
    if missing_greeks:
        limitations.append(
            f"{identifier}: missing Greeks: {', '.join(missing_greeks)}"
        )
    if position.underlying_price is None:
        limitations.append(f"{identifier}: missing underlying price")
    if position.market_price is None:
        limitations.append(f"{identifier}: missing market price")
    if position.fx_rate is None:
        limitations.append(f"{identifier}: missing FX rate")
    return limitations


def _group_base_market_value(
    rows: list[OptionPositionView],
    group_name: str,
) -> tuple[float | None, float, str | None]:
    """Sum convertible exposure and disclose rows excluded for missing FX."""
    convertible = [
        abs(position.base_market_value)
        for position in rows
        if position.base_market_value is not None
    ]
    excluded = [
        _contract_identifier(position)
        for position in rows
        if position.base_market_value is None
    ]
    if not excluded:
        return sum(convertible), 1.0, None
    coverage_ratio = len(convertible) / len(rows)
    coverage = "partial" if convertible else "no"
    return (
        sum(convertible) if convertible else None,
        coverage_ratio,
        (
            f"{group_name}: {coverage} base market value coverage; "
            f"excluded {', '.join(excluded)}"
        ),
    )


def build_summary(
    options: list[OptionPositionView],
) -> tuple[OptionsOverviewSummary, list[str]]:
    """Aggregate Greeks and risk distributions from normalized option positions."""
    limitations: list[str] = []
    greek_coverage: dict[str, OptionGreekCoverage] = {}
    totals: dict[str, float | None] = {}

    for greek in _GREEKS:
        scaled_values: list[float] = []
        excluded: list[str] = []
        for position in options:
            scaled = _scaled_greek(position, greek)
            if scaled is None:
                excluded.append(_contract_identifier(position))
            else:
                scaled_values.append(scaled)
        greek_coverage[greek] = OptionGreekCoverage(
            contributing_contracts=len(scaled_values),
            excluded_contracts=excluded,
        )
        totals[greek] = round(sum(scaled_values), 12) if scaled_values else None

    expiry_rows: dict[date, list[OptionPositionView]] = defaultdict(list)
    underlying_rows: dict[str, list[OptionPositionView]] = defaultdict(list)
    for position in options:
        expiry_rows[position.expiry_date].append(position)
        underlying_rows[position.underlying_symbol].append(position)

    expiration_distribution: list[OptionExpirationBucket] = []
    for expiry, rows in sorted(expiry_rows.items()):
        absolute_value, coverage, limitation = _group_base_market_value(
            rows, f"expiration {expiry.isoformat()}"
        )
        expiration_distribution.append(
            OptionExpirationBucket(
                expiry_date=expiry,
                contract_count=len(rows),
                quantity=sum(position.quantity for position in rows),
                absolute_base_market_value=absolute_value,
                base_market_value_coverage=coverage,
            )
        )
        if limitation:
            limitations.append(limitation)

    absolute_values: dict[str, tuple[float | None, float]] = {}
    for symbol, rows in underlying_rows.items():
        absolute_value, coverage, limitation = _group_base_market_value(
            rows, f"underlying {symbol}"
        )
        absolute_values[symbol] = (absolute_value, coverage)
        if limitation:
            limitations.append(limitation)

    concentration_denom = sum(
        value
        for value, _ in absolute_values.values()
        if value is not None
    )
    underlying_concentration = sorted(
        [
            OptionUnderlyingConcentration(
                underlying_symbol=symbol,
                absolute_base_market_value=value,
                base_market_value_coverage=coverage,
                weight=(
                    value / concentration_denom
                    if value is not None and concentration_denom
                    else None
                ),
            )
            for symbol, (value, coverage) in absolute_values.items()
        ],
        key=lambda row: (
            row.absolute_base_market_value is None,
            -(row.absolute_base_market_value or 0.0),
            row.underlying_symbol,
        ),
    )

    return (
        OptionsOverviewSummary(
            total_delta=totals["delta"],
            total_gamma=totals["gamma"],
            total_theta=totals["theta"],
            total_vega=totals["vega"],
            daily_time_value_decay=(
                -totals["theta"] if totals["theta"] is not None else None
            ),
            greek_coverage=greek_coverage,
            expiration_distribution=expiration_distribution,
            underlying_concentration=underlying_concentration,
        ),
        limitations,
    )


def build_options_overview(
    raw: dict, report_date: date, ts: datetime
) -> OptionsOverview:
    """Map raw account option data into typed positions and aggregate risk."""
    account = raw["account"]
    account_id = account["account_id"]
    # Default True keeps injected-mock raw payloads (which omit the flag) on the
    # existing per-contract limitation path.
    market_data_enabled = raw.get("market_data_enabled", True)
    views: list[OptionPositionView] = []
    limitations: list[str] = []

    for option in raw["options"]:
        contract_id = str(option.get("contract_id", "<unknown contract>"))
        expiry_date = _parse_expiry(option.get("expiry_date"), contract_id)
        multiplier = _parse_multiplier(option.get("multiplier"), contract_id)
        right = option["right"]
        try:
            moneyness = classify_moneyness(
                right, float(option["strike"]), option.get("underlying_price")
            )
        except ValueError as error:
            raise ValueError(f"{contract_id}: right: {error}") from error

        fx_rate = option.get("fx_rate")
        view = OptionPositionView(
            account_id=account_id,
            underlying_symbol=option["underlying_symbol"],
            right=right,
            quantity=float(option["quantity"]),
            strike=float(option["strike"]),
            expiry_date=expiry_date,
            days_to_expiry=(expiry_date - report_date).days + 1,
            avg_cost=float(option["avg_cost"]),
            market_price=_finite_float(option.get("market_price")),
            market_value=float(option["market_value"]),
            unrealized_pnl=float(option["unrealized_pnl"]),
            currency=option["currency"],
            multiplier=multiplier,
            implied_volatility=option.get("implied_volatility"),
            delta=option.get("delta"),
            gamma=option.get("gamma"),
            theta=option.get("theta"),
            vega=option.get("vega"),
            underlying_price=option.get("underlying_price"),
            moneyness=moneyness,
            greeks_status=(
                "COMPLETE"
                if all(option.get(greek) is not None for greek in _GREEKS)
                else "INCOMPLETE"
            ),
            fx_rate=fx_rate,
            base_market_value=(
                float(option["market_value"]) * fx_rate
                if fx_rate is not None
                else None
            ),
            base_unrealized_pnl=(
                float(option["unrealized_pnl"]) * fx_rate
                if fx_rate is not None
                else None
            ),
        )
        views.append(view)
        if market_data_enabled:
            limitations.extend(_limitations_for(view))

    if not market_data_enabled:
        # One clear note instead of per-contract "missing Greeks" noise.
        limitations.append(_MARKET_DATA_DISABLED_LIMITATION)

    summary, summary_limitations = build_summary(views)
    return OptionsOverview(
        account_id=account_id,
        base_currency=account["base_currency"],
        options=views,
        summary=summary,
        data_limitations=limitations + summary_limitations,
        ts=ts,
    )


def _market_data_type_code(mode: str) -> int:
    """Return IB's configured market-data type code."""
    codes = {
        "realtime": 1,
        "frozen": 2,
        "delayed": 3,
        "delayed_frozen": 4,
    }
    try:
        return codes[mode]
    except KeyError as error:
        raise ValueError(
            f"unknown market_data_type {mode!r}; expected one of {sorted(codes)}"
        ) from error


def _usable_underlying_price(value: object) -> float | None:
    """Return a positive finite underlying price or null for IB sentinels."""
    try:
        price = float(value)
    except (TypeError, ValueError):
        return None
    return price if math.isfinite(price) and price > 0 else None


def _model_underlying_price(ticker: object) -> float | None:
    """Read the preferred underlying price from an option model payload."""
    greeks = getattr(ticker, "modelGreeks", None)
    return _usable_underlying_price(
        getattr(greeks, "undPrice", None) if greeks is not None else None
    )


def _shared_model_underlying_price(
    subscriptions: list[tuple[object, object]], key: tuple[str, str]
) -> float | None:
    """Resolve one model underlying price shared by matching option rows."""
    for item, ticker in subscriptions:
        contract = item.contract
        if (contract.symbol, contract.currency) == key:
            price = _model_underlying_price(ticker)
            if price is not None:
                return price
    return None


def _quoted_underlying_price(ticker: object) -> float | None:
    """Resolve an underlying quote from market price and then prior close."""
    market_price = _usable_underlying_price(ticker.marketPrice())
    return market_price or _usable_underlying_price(getattr(ticker, "close", None))


def _wait_until(
    ib: object,
    predicate: Callable[[], bool],
    timeout_s: float,
    poll_s: float = 0.25,
) -> None:
    """Let IB process events until data is ready or the bounded wait expires."""
    elapsed = 0.0
    while not predicate() and elapsed < timeout_s:
        interval = min(poll_s, timeout_s - elapsed)
        ib.sleep(interval)
        elapsed += interval


def _exchange_rates(account_values) -> dict[str, float]:
    """Collect local-to-base exchange rates from IB ledger rows."""
    rates: dict[str, float] = {}
    for value in account_values:
        if (
            value.tag == "$LEDGER-ExchangeRate"
            and value.currency
            and value.currency != "BASE"
        ):
            try:
                rates[value.currency] = float(value.value)
            except (TypeError, ValueError):
                continue
    return rates


def _account_base_currency(account_values) -> str | None:
    """Resolve IB's account base currency from account-value metadata."""
    values = list(account_values)
    for value in values:
        if value.tag == "Currency" and value.value:
            return str(value.value)
    for value in values:
        if value.tag == "NetLiquidation" and value.currency:
            return str(value.currency)
    return None


def _option_right(right: str) -> str:
    """Normalize IB's compact option right value to the report vocabulary."""
    return {"C": "CALL", "P": "PUT"}.get(right, right)


def _contract_id(contract) -> str:
    """Build a stable readable identifier for an IB option contract."""
    return (
        f"{contract.symbol}-{contract.lastTradeDateOrContractMonth}-"
        f"{contract.right}-{contract.strike:g}"
    )


def _default_client_factory(cfg):
    """Build a read-only IB Gateway client, imported lazily for offline tests."""
    from ib_async import IB, Stock

    class _LiveClient:
        """Read the account option book and its model Greeks from IB Gateway."""

        def __init__(self, cfg):
            """Connect with IB's enforced read-only Gateway API mode."""
            self._market_data = cfg.options.fetch_market_data
            self.ib = IB()
            self.ib.connect(
                cfg.connection.host,
                cfg.connection.port,
                clientId=cfg.connection.client_id,
                readonly=True,
            )
            # Free mode never touches market data, so we do not even request a
            # data type — that keeps the run away from any snapshot billing.
            if self._market_data:
                self.ib.reqMarketDataType(
                    _market_data_type_code(cfg.connection.market_data_type)
                )

        def fetch_raw(self) -> dict:
            """Read IB-valued option positions and their bounded quote snapshot."""
            account_id = self.ib.managedAccounts()[0]
            account_values = self.ib.accountValues(account_id)
            summary = {value.tag: value.value for value in account_values}
            fx_rates = _exchange_rates(account_values)
            base_currency = _account_base_currency(account_values)
            if base_currency:
                fx_rates[base_currency] = 1.0
            positions = [
                item
                for item in self.ib.portfolio(account_id)
                if item.contract.secType == "OPT"
            ]
            if not self._market_data:
                # Free mode: no reqMktData at all. Position, price, market value
                # and P&L are IB-computed portfolio fields (no snapshot billing);
                # Greeks, IV and the underlying price are left unavailable.
                options = [
                    {
                        "contract_id": _contract_id(item.contract),
                        "underlying_symbol": item.contract.symbol,
                        "right": _option_right(item.contract.right),
                        "strike": item.contract.strike,
                        "expiry_date": str(
                            item.contract.lastTradeDateOrContractMonth
                        ),
                        "multiplier": str(item.contract.multiplier),
                        "quantity": item.position,
                        "avg_cost": item.averageCost,
                        "market_price": item.marketPrice,
                        "market_value": item.marketValue,
                        "unrealized_pnl": item.unrealizedPNL,
                        "currency": item.contract.currency,
                        "fx_rate": fx_rates.get(item.contract.currency),
                        "implied_volatility": None,
                        "delta": None,
                        "gamma": None,
                        "theta": None,
                        "vega": None,
                        "underlying_price": None,
                    }
                    for item in positions
                ]
                return {
                    "account": {
                        "account_id": account_id,
                        "base_currency": base_currency,
                    },
                    "options": options,
                    "market_data_enabled": False,
                }
            option_subscriptions: list[tuple[object, object]] = []
            underlying_subscriptions: dict[tuple[str, str], tuple[object, object]] = {}
            try:
                for item in positions:
                    contract = item.contract
                    ticker = self.ib.reqMktData(contract, "", False, False)
                    option_subscriptions.append((item, ticker))
                _wait_until(
                    self.ib,
                    lambda: all(
                        _model_underlying_price(ticker) is not None
                        for _, ticker in option_subscriptions
                    ),
                    timeout_s=4.0,
                )
                missing_keys = {
                    (item.contract.symbol, item.contract.currency)
                    for item, ticker in option_subscriptions
                    if _model_underlying_price(ticker) is None
                    and _shared_model_underlying_price(
                        option_subscriptions,
                        (item.contract.symbol, item.contract.currency),
                    )
                    is None
                }
                underlying_contracts = {
                    key: Stock(key[0], "SMART", key[1]) for key in missing_keys
                }
                if underlying_contracts:
                    qualified_contracts = self.ib.qualifyContracts(
                        *underlying_contracts.values()
                    )
                    for contract in qualified_contracts:
                        if contract is None:
                            continue
                        key = (contract.symbol, contract.currency)
                        if key not in missing_keys or key in underlying_subscriptions:
                            continue
                        ticker = self.ib.reqMktData(contract, "", False, False)
                        underlying_subscriptions[key] = (contract, ticker)
                _wait_until(
                    self.ib,
                    lambda: all(
                        _shared_model_underlying_price(option_subscriptions, key)
                        is not None
                        or _quoted_underlying_price(ticker) is not None
                        for key, (_, ticker) in underlying_subscriptions.items()
                    ),
                    timeout_s=20.0,
                )

                options: list[dict] = []
                for item, ticker in option_subscriptions:
                    contract = item.contract
                    greeks = ticker.modelGreeks
                    key = (contract.symbol, contract.currency)
                    underlying_price = _model_underlying_price(ticker)
                    if underlying_price is None:
                        underlying_price = _shared_model_underlying_price(
                            option_subscriptions, key
                        )
                    if underlying_price is None and key in underlying_subscriptions:
                        underlying_price = _quoted_underlying_price(
                            underlying_subscriptions[key][1]
                        )
                    options.append(
                        {
                            "contract_id": _contract_id(contract),
                            "underlying_symbol": contract.symbol,
                            "right": _option_right(contract.right),
                            "strike": contract.strike,
                            "expiry_date": str(
                                contract.lastTradeDateOrContractMonth
                            ),
                            "multiplier": str(contract.multiplier),
                            "quantity": item.position,
                            "avg_cost": item.averageCost,
                            "market_price": ticker.marketPrice(),
                            "market_value": item.marketValue,
                            "unrealized_pnl": item.unrealizedPNL,
                            "currency": contract.currency,
                            "fx_rate": fx_rates.get(contract.currency),
                            "implied_volatility": (
                                greeks.impliedVol if greeks is not None else None
                            ),
                            "delta": greeks.delta if greeks is not None else None,
                            "gamma": greeks.gamma if greeks is not None else None,
                            "theta": greeks.theta if greeks is not None else None,
                            "vega": greeks.vega if greeks is not None else None,
                            "underlying_price": underlying_price,
                        }
                    )
            finally:
                for item, _ in option_subscriptions:
                    self.ib.cancelMktData(item.contract)
                for contract, _ in underlying_subscriptions.values():
                    self.ib.cancelMktData(contract)

            return {
                "account": {
                    "account_id": account_id,
                    "base_currency": base_currency,
                },
                "options": options,
                "market_data_enabled": True,
            }

        def disconnect(self) -> None:
            """Close the read-only Gateway session."""
            self.ib.disconnect()

    return _LiveClient(cfg)


def options_overview(cfg_path: str, client_factory=None, now=None) -> dict:
    """Load config, pull a read-only option book, and return JSON-safe data."""
    cfg = load_config(cfg_path)
    client = (client_factory or _default_client_factory)(cfg)
    try:
        raw = client.fetch_raw()
    finally:
        client.disconnect()
    raw["account"]["base_currency"] = resolve_base_currency(
        cfg, raw["account"].get("base_currency")
    )
    stamp = (now or (lambda: datetime.now(timezone.utc)))()
    return build_options_overview(raw, stamp.date(), stamp).model_dump(mode="json")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Read-only option Greeks overview from IB Gateway."
    )
    parser.add_argument("--config", required=True, help="path to config.yaml")
    args = parser.parse_args()
    try:
        print(json.dumps(options_overview(args.config), ensure_ascii=False))
    except (FileNotFoundError, ValueError) as error:
        parser.error(str(error))
