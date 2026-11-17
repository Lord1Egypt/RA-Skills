"""Typed data models for the IB analyst pipeline.

These are the single source of truth for the shape of account, position,
execution, bar and dividend records. Storage and analysis layers depend
only on these types, never on raw ib_async objects.
"""
from __future__ import annotations
from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field, PrivateAttr, computed_field


class Account(BaseModel):
    """Account-level summary snapshot at a point in time."""

    account_id: str
    base_currency: str
    net_liquidation: float
    total_cash: float
    buying_power: float
    ts: datetime


class Position(BaseModel):
    """A single held position with cost basis and mark-to-market values.

    `market_value`/`unrealized_pnl` are in the position's own `currency`.
    `fx_rate` converts that currency into the account base currency (1.0 when
    the position is already in base). Use `base_value`/`base_unrealized_pnl`
    whenever aggregating across positions — summing raw `market_value` mixes
    currencies and understates or overstates the book.
    """

    account_id: str
    symbol: str
    sec_type: str
    currency: str
    quantity: float
    avg_cost: float
    market_price: float
    market_value: float
    unrealized_pnl: float
    fx_rate: float = 1.0   # local currency -> account base; 1.0 when already base

    @computed_field  # type: ignore[prop-decorator]
    @property
    def base_value(self) -> float:
        """Market value converted into the account base currency."""
        return self.market_value * self.fx_rate

    @computed_field  # type: ignore[prop-decorator]
    @property
    def base_unrealized_pnl(self) -> float:
        """Unrealized P&L converted into the account base currency."""
        return self.unrealized_pnl * self.fx_rate


class Execution(BaseModel):
    """A single trade execution (fill) record."""

    exec_id: str
    symbol: str
    side: str
    quantity: float
    price: float
    commission: float
    ts: datetime


class FlexTrade(BaseModel):
    """One IBKR Flex Trade execution with local and optional base FX amounts."""

    exec_id: str
    ts: datetime
    symbol: str
    side: str
    quantity: float
    price: float
    commission: float
    currency: str
    commission_currency: str
    multiplier: float = Field(default=1.0, gt=0)
    order_type: str
    exchange: str
    open_close: str = ""
    realized_pnl: float
    fx_rate_to_base: float | None = None
    _commission_fx_rate_to_base: float | None = PrivateAttr(default=None)

    @computed_field  # type: ignore[prop-decorator]
    @property
    def notional(self) -> float:
        """Absolute local-currency execution notional."""
        return abs(self.quantity * self.price * self.multiplier)

    @computed_field  # type: ignore[prop-decorator]
    @property
    def base_notional(self) -> float | None:
        """Execution notional converted by Flex's local-to-base FX rate."""
        return None if self.fx_rate_to_base is None else self.notional * self.fx_rate_to_base

    @computed_field  # type: ignore[prop-decorator]
    @property
    def base_commission(self) -> float | None:
        """Absolute commission converted by its own local-to-base FX rate."""
        rate = (
            self.fx_rate_to_base
            if self.commission_currency == self.currency
            else self._commission_fx_rate_to_base
        )
        return None if rate is None else abs(self.commission) * rate

    @computed_field  # type: ignore[prop-decorator]
    @property
    def base_realized_pnl(self) -> float | None:
        """IBKR FIFO realized P&L converted by Flex's local-to-base FX rate."""
        return None if self.fx_rate_to_base is None else self.realized_pnl * self.fx_rate_to_base


class FlexCashTransaction(BaseModel):
    """One normalized Flex cash movement used for dividend reconciliation."""

    account_id: str
    currency: str
    asset_class: str
    fx_rate_to_base: float | None
    symbol: str
    description: str | None
    conid: str | None
    underlying_conid: str | None
    underlying_symbol: str | None
    ts: datetime
    amount: float | None
    transaction_type: str
    trade_id: str | None
    code: str


class FlexDividendAccrual(BaseModel):
    """One raw changed or open Flex dividend-accrual record."""

    account_id: str
    currency: str
    asset_class: str
    fx_rate_to_base: float | None
    symbol: str
    description: str | None
    conid: str | None
    accrual_date: date | None
    ex_date: date
    pay_date: date
    quantity: float | None
    tax: float | None
    fee: float | None
    gross_rate: float | None
    gross_amount: float | None
    net_amount: float | None
    code: str
    report_date: date | None


class FlexOpenPosition(BaseModel):
    """One raw Flex open position used by annual dividend estimates."""

    account_id: str
    currency: str
    asset_class: str
    fx_rate_to_base: float | None
    symbol: str
    conid: str | None
    report_date: date
    quantity: float | None
    multiplier: float | None
    mark_price: float | None
    position_value: float | None
    side: str
    level_of_detail: str


class FlexInstrument(BaseModel):
    """One raw Flex financial-instrument identity and listing record."""

    asset_class: str
    symbol: str
    currency: str
    listing_exchange: str | None
    description: str | None
    conid: str | None
    isin: str | None
    multiplier: float | None
    security_subtype: str | None


class FlexDividendDataset(BaseModel):
    """Strictly parsed raw records from the six dividend Flex sections."""

    base_currency: str
    statement_from_date: date | None = None
    statement_to_date: date | None = None
    cash_transactions: list[FlexCashTransaction]
    dividend_accruals: list[FlexDividendAccrual]
    open_dividend_accruals: list[FlexDividendAccrual]
    open_positions: list[FlexOpenPosition]
    instruments: list[FlexInstrument]


class DividendIncomeLine(BaseModel):
    """One realized or expected dividend with native and base-currency facts."""

    symbol: str
    payment_date: date
    status: Literal["REALIZED", "EXPECTED"]
    gross: float | None
    withholding_tax: float | None
    fee: float | None
    net: float | None
    currency: str
    fx_rate_to_base: float | None
    base_gross: float | None
    base_withholding_tax: float | None
    base_fee: float | None
    base_net: float | None
    quantity: float | None
    country: str


class DividendTotals(BaseModel):
    """Four dividend amount components aggregated in one stated currency basis."""

    gross: float | None = 0.0
    withholding_tax: float | None = 0.0
    fee: float | None = 0.0
    net: float | None = 0.0


class DividendContribution(BaseModel):
    """One symbol's realized base-currency net contribution."""

    symbol: str
    base_net: float


class DividendAttribution(BaseModel):
    """Status-separated attribution buckets in one stated currency basis."""

    realized: dict[str, DividendTotals]
    expected: dict[str, DividendTotals]


class DividendIncomeSummary(BaseModel):
    """Separate base totals plus native-currency and listing-country attribution."""

    realized: DividendTotals
    expected: DividendTotals
    by_currency: DividendAttribution
    by_country: DividendAttribution
    top_contributors: list[DividendContribution]


class AnnualDividendHolding(BaseModel):
    """History-based annual dividend run rate for one current eligible holding."""

    symbol: str
    quantity: float
    currency: str
    fx_rate_to_base: float | None
    trailing_gross_rate: float
    effective_tax_rate: float | None
    estimated_gross: float
    estimated_net: float | None
    base_estimated_gross: float | None
    base_estimated_net: float | None


class AnnualDividendEstimate(BaseModel):
    """Portfolio annual dividend lower bound and gross-yield calculation."""

    holdings: list[AnnualDividendHolding]
    estimated_base_gross: float | None
    estimated_base_net: float | None
    eligible_base_market_value: float | None
    portfolio_estimated_gross_yield: float | None
    history_days_covered: int
    complete_history: bool


class DividendIncomeReport(BaseModel):
    """Pure calculated dividend report for an inclusive requested payment period."""

    start_date: date
    end_date: date
    base_currency: str
    realized_dividends: list[DividendIncomeLine]
    expected_dividends: list[DividendIncomeLine]
    summary: DividendIncomeSummary
    annual_estimate: AnnualDividendEstimate
    coverage_note: str | None = None
    data_limitations: list[str]


class TradeHistorySummary(BaseModel):
    """Base-currency aggregate statistics for an inclusive trade period."""

    total_trades: int
    buy_count: int
    sell_count: int
    total_notional: float
    total_commission: float
    profitable_trades: int
    losing_trades: int
    win_rate: float | None
    average_profit: float | None
    average_loss: float | None
    profit_loss_ratio: float | None


class TradeHistoryReport(BaseModel):
    """Read-only Flex trade records and their base-currency summary."""

    start_date: date
    end_date: date
    base_currency: str
    trades: list[FlexTrade]
    summary: TradeHistorySummary
    coverage_note: str | None = None


class DailyBar(BaseModel):
    """Daily OHLCV price bar for a symbol."""

    symbol: str
    date: date
    open: float
    high: float
    low: float
    close: float
    volume: float


class Dividend(BaseModel):
    """A dividend event with ex/pay dates and gross/tax amounts."""

    symbol: str
    ex_date: date
    pay_date: date | None
    gross: float
    tax: float
    currency: str


class CurrencyBalance(BaseModel):
    """Per-currency cash/net-liq balance with its local->base exchange rate.

    `cash_balance`/`net_liquidation` are in the row's own `currency`. Use the
    `base_*` computed fields whenever presenting a single-currency total — the
    raw amounts mix currencies and must not be summed directly.
    """

    currency: str
    cash_balance: float
    net_liquidation: float
    exchange_rate: float = 1.0   # local currency -> account base; 1.0 when already base

    @computed_field  # type: ignore[prop-decorator]
    @property
    def base_cash_balance(self) -> float:
        """Cash balance converted into the account base currency."""
        return self.cash_balance * self.exchange_rate

    @computed_field  # type: ignore[prop-decorator]
    @property
    def base_net_liquidation(self) -> float:
        """Net liquidation converted into the account base currency."""
        return self.net_liquidation * self.exchange_rate


class AccountOverview(BaseModel):
    """Account-level financial overview: equity, margin, liquidity and P&L.

    A richer companion to `Account` for the /ib-account-overview command. All monetary
    figures are in `base_currency`; per-currency detail lives in
    `currency_balances`. This model reads account state only — it never carries
    positions, orders, or any write path to IB.
    """

    account_id: str
    base_currency: str
    net_liquidation: float
    total_cash: float
    buying_power: float
    margin_used: float          # current margin requirement in use
    init_margin_req: float      # initial margin requirement
    maint_margin_req: float     # maintenance margin requirement
    available_funds: float
    excess_liquidity: float
    gross_position_value: float
    daily_pnl: float            # today's P&L (mark-to-market)
    unrealized_pnl: float
    realized_pnl: float
    currency_balances: list[CurrencyBalance]
    ts: datetime


class PositionView(BaseModel):
    """A single position enriched for a human-readable positions overview.

    Extends the raw `Position` shape with the descriptive attributes a holder
    checks first — instrument `name`, `industry`, listing `market`/`country` —
    plus derived read-outs (`side`, `unrealized_return`) and the portfolio
    `weight`. `market_value`/`unrealized_pnl` are in the position's own
    `currency`; `fx_rate` converts them into the account base currency. Use the
    `base_*` computed fields whenever ranking across positions — summing raw
    `market_value` mixes currencies. This model reads position state only; it
    carries no order path to IB.
    """

    account_id: str
    symbol: str
    name: str = ""              # instrument long name; "" when IB has none
    sec_type: str
    quantity: float
    avg_cost: float
    market_price: float
    market_value: float         # in the position's own currency
    unrealized_pnl: float       # in the position's own currency
    currency: str               # pricing/quote currency
    industry: str = ""          # IB contract-detail industry; "" when unknown
    market: str = ""            # listing exchange (IB primaryExchange); "" when unknown
    country: str = ""           # market -> country label; "" when not mapped
    fx_rate: float = 1.0        # local currency -> account base; 1.0 when already base
    weight: float = 0.0         # base_value / account net liquidation; set at build time

    @computed_field  # type: ignore[prop-decorator]
    @property
    def side(self) -> str:
        """LONG for a positive quantity, SHORT for negative, FLAT for zero."""
        if self.quantity > 0:
            return "LONG"
        if self.quantity < 0:
            return "SHORT"
        return "FLAT"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def base_value(self) -> float:
        """Market value converted into the account base currency."""
        return self.market_value * self.fx_rate

    @computed_field  # type: ignore[prop-decorator]
    @property
    def base_unrealized_pnl(self) -> float:
        """Unrealized P&L converted into the account base currency."""
        return self.unrealized_pnl * self.fx_rate

    @computed_field  # type: ignore[prop-decorator]
    @property
    def unrealized_return(self) -> float:
        """Unrealized P&L as a fraction of cost basis (0.0 when cost is zero).

        Cost basis is recovered as `market_value - unrealized_pnl`, so this
        stays correct for shorts (negative basis) without re-deriving it from
        quantity/avg_cost. Returns 0.0 rather than dividing by zero.
        """
        cost_basis = self.market_value - self.unrealized_pnl
        if cost_basis == 0:
            return 0.0
        return self.unrealized_pnl / abs(cost_basis)


class PositionsOverview(BaseModel):
    """Account-level positions overview: every position, enriched and rankable.

    Companion to `AccountOverview` for the /ib-positions-overview command. All
    ranking must use each position's `base_value` (base currency); `weight` is
    already normalized against `net_liquidation`. Reads position state only —
    no orders, no write path to IB.
    """

    account_id: str
    base_currency: str
    net_liquidation: float
    positions: list[PositionView]
    ts: datetime


class DailyPnLPosition(BaseModel):
    """A single position's contribution to today's P&L.

    All three P&L figures come from IB's `pnl` subscription (`reqPnLSingle`) and
    are already in the account base currency — IB converts foreign positions
    before it publishes them, so these are summed directly (no `fx_rate` here,
    unlike `Position`/`PositionView`). `currency` is the position's trading
    currency, kept only for the per-currency breakdown, not for conversion.
    """

    account_id: str
    symbol: str
    name: str = ""              # instrument long name; "" when IB has none
    sec_type: str              # STK / OPT / FUT / CASH ...
    stock_type: str = ""       # IB contract-detail stockType (COMMON/ETF/...) for STK
    currency: str              # trading currency (for the per-currency breakdown)
    daily_pnl: float           # today's P&L (base currency)
    unrealized_pnl: float      # open-position P&L (base currency)
    realized_pnl: float        # P&L booked today from closes (base currency)

    @computed_field  # type: ignore[prop-decorator]
    @property
    def asset_class(self) -> str:
        """Human asset-class label derived from sec_type (+ stockType for STK).

        STK splits into ETF vs Stock via IB's stockType; OPT/FUT/CASH map to
        Option/Future/Forex. Anything unrecognized keeps its raw sec_type so an
        unmapped instrument is visible rather than silently bucketed wrong.
        """
        st = self.sec_type.upper()
        if st == "STK":
            return "ETF" if self.stock_type.upper() == "ETF" else "Stock"
        return {"OPT": "Option", "FOP": "Option", "FUT": "Future",
                "CASH": "Forex", "BOND": "Bond", "FUND": "Fund"}.get(st, self.sec_type)


class DailyPnLOverview(BaseModel):
    """Account-level daily P&L: today's total split into realized/unrealized,
    with every position's contribution.

    Companion to `AccountOverview`/`PositionsOverview` for the /ib-daily-pnl
    command. Every P&L figure is already base-currency (IB's pnl subscription
    converts before publishing), so contributions sum directly. Reads P&L state
    only — no orders, no write path to IB.
    """

    account_id: str
    base_currency: str
    daily_pnl: float           # today's total P&L (base currency)
    unrealized_pnl: float
    realized_pnl: float
    positions: list[DailyPnLPosition]
    ts: datetime


class OptionPositionView(BaseModel):
    """One live option holding with IB valuation and model-Greeks fields."""

    account_id: str
    underlying_symbol: str
    right: str
    quantity: float
    strike: float
    expiry_date: date
    days_to_expiry: int
    avg_cost: float
    market_price: float | None
    market_value: float
    unrealized_pnl: float
    currency: str
    multiplier: int
    implied_volatility: float | None = None
    delta: float | None = None
    gamma: float | None = None
    theta: float | None = None
    vega: float | None = None
    underlying_price: float | None = None
    moneyness: str | None = None
    greeks_status: str
    fx_rate: float | None = None
    base_market_value: float | None = None
    base_unrealized_pnl: float | None = None

    @computed_field  # type: ignore[prop-decorator]
    @property
    def position_side(self) -> str:
        """Return the direction represented by the signed holding quantity."""
        return "LONG" if self.quantity > 0 else "SHORT" if self.quantity < 0 else "FLAT"


class OptionGreekCoverage(BaseModel):
    """Coverage metadata for one account-level Greek."""

    contributing_contracts: int
    excluded_contracts: list[str] = Field(default_factory=list)


class OptionExpirationBucket(BaseModel):
    """Absolute option exposure and signed quantity for one expiry."""

    expiry_date: date
    contract_count: int
    quantity: float
    absolute_base_market_value: float | None = None
    base_market_value_coverage: float | None = None


class OptionUnderlyingConcentration(BaseModel):
    """Absolute option-market-value concentration for one underlying."""

    underlying_symbol: str
    absolute_base_market_value: float | None = None
    base_market_value_coverage: float | None = None
    weight: float | None = None


class OptionsOverviewSummary(BaseModel):
    """Aggregate option Greeks and deterministic risk distributions."""

    total_delta: float | None = None
    total_gamma: float | None = None
    total_theta: float | None = None
    total_vega: float | None = None
    daily_time_value_decay: float | None = None
    greek_coverage: dict[str, OptionGreekCoverage] = Field(default_factory=dict)
    expiration_distribution: list[OptionExpirationBucket] = Field(default_factory=list)
    underlying_concentration: list[OptionUnderlyingConcentration] = Field(default_factory=list)


class OptionsOverview(BaseModel):
    """Read-only option holdings and aggregate risk overview."""

    account_id: str
    base_currency: str
    options: list[OptionPositionView]
    summary: OptionsOverviewSummary
    data_limitations: list[str]
    ts: datetime


class Snapshot(BaseModel):
    """Point-in-time snapshot combining account summary and positions."""

    account: Account
    positions: list[Position]
    ts: datetime
