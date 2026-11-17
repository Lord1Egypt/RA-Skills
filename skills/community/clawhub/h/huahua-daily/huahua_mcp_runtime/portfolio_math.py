"""Pure portfolio calculations shared by MCP portfolio tools."""

import math
import re
from datetime import date, datetime
from decimal import Decimal, ROUND_HALF_UP
from typing import Optional
from zoneinfo import ZoneInfo

from .estimate_frame_contract import estimate_frame_available


def beijing_date_string() -> str:
    return datetime.now(ZoneInfo("Asia/Shanghai")).strftime("%Y-%m-%d")


def normalize_observed_day(value, *, today: str | None = None) -> str:
    candidate = str(value or "")[:10]
    try:
        parsed = date.fromisoformat(candidate)
    except ValueError:
        return ""
    normalized = parsed.isoformat()
    return normalized if normalized <= (today or beijing_date_string()) else ""


_MISSING = object()
EFFECTIVE_ZERO_SHARES = 0.001
NAV_CHANGE_MISMATCH_TOLERANCE_PERCENT = 0.05
_PERCENT_VALUE_PATTERN = re.compile(r"^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:e[+-]?\d+)?$", re.IGNORECASE)


def parse_percent(value) -> float | None:
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, (int, float, Decimal)):
        parsed = float(value)
        return parsed if math.isfinite(parsed) else None
    if not isinstance(value, str):
        return None
    normalized = value.strip()
    if normalized.endswith("%"):
        normalized = normalized[:-1].strip()
    if not normalized or not _PERCENT_VALUE_PATTERN.fullmatch(normalized):
        return None
    parsed = float(normalized)
    return parsed if math.isfinite(parsed) else None


def parse_confirm_days(value) -> int | None:
    """Parse the same integer 1..30 settlement contract used by the App."""
    if isinstance(value, bool) or value is None:
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number) or not number.is_integer():
        return None
    parsed = int(number)
    return parsed if 1 <= parsed <= 30 else None


def _estimate_confirm_days(fund: dict, estimate: dict) -> int | None:
    candidate = _MISSING
    for source, keys in (
        (estimate, ("confirm_days", "confirmDays")),
        (fund, ("confirmDays", "confirm_days")),
    ):
        for key in keys:
            if key in source and source[key] is not None:
                candidate = source[key]
                break
        if candidate is not _MISSING:
            break
    return None if candidate is _MISSING else parse_confirm_days(candidate)


def resolve_official_attribution_date(fund: dict, estimate: dict) -> str:
    """Return a reliable G day paired with the latest official D day."""
    today = beijing_date_string()
    nav_date = normalize_observed_day(
        estimate.get("last_nav_date")
        or estimate.get("lastNavDate")
        or fund.get("lastNavDate"),
        today=today,
    )
    if not nav_date:
        return ""

    publish_date = normalize_observed_day(
        estimate.get("last_nav_publish_date")
        or estimate.get("lastNavPublishDate")
        or fund.get("lastNavPublishDate")
        or fund.get("last_nav_publish_date"),
        today=today,
    )
    if publish_date >= nav_date:
        return publish_date

    display_date = normalize_observed_day(
        estimate.get("display_date") or estimate.get("displayDate") or fund.get("displayDate"),
        today=today,
    )
    if display_date >= nav_date:
        return display_date

    confirm_days = _estimate_confirm_days(fund, estimate)
    if confirm_days == 1:
        return nav_date

    pair = estimate.get("estimate_vs_actual") or estimate.get("estimateVsActual")
    if not isinstance(pair, dict):
        pair = fund.get("estimateVsActual") or fund.get("estimate_vs_actual")
    if isinstance(pair, dict):
        paired_nav_date = normalize_observed_day(pair.get("nav_date"), today=today)
        paired_publish_date = normalize_observed_day(pair.get("publish_date"), today=today)
        if paired_nav_date == nav_date and paired_publish_date >= nav_date:
            return paired_publish_date
    return ""


def js_round(value: float, digits: int) -> float:
    """Match the frontend decimal half-up metric rounding."""
    if not math.isfinite(value):
        return 0.0
    try:
        sign = -1 if value < 0 else 1
        shifted = float(abs(Decimal(repr(value))) * Decimal(10**digits))
        return sign * (math.floor(shifted + 0.5) / (10**digits))
    except Exception:
        return round(value, digits)


def r2(value: float) -> float:
    return js_round(value, 2)


def r4(value: float) -> float:
    return js_round(value, 4)


def r6(value: float) -> float:
    return js_round(value, 6)


def ratio_pct(numerator: float, denominator: float) -> Optional[float]:
    if not math.isfinite(numerator) or not math.isfinite(denominator) or denominator <= 0:
        return None
    try:
        value = (Decimal(repr(numerator)) * Decimal("100") / Decimal(repr(denominator))).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        return float(value)
    except Exception:
        return None


def to_float(value, default: float = 0.0) -> float:
    try:
        candidate = float(value)
        return candidate if math.isfinite(candidate) else default
    except (TypeError, ValueError):
        return default


TYPE_ORDER = {"CORRECTION": 0, "SELL": 1, "BUY": 2, "DIVIDEND_CASH": 3, "DIVIDEND_REINVEST": 3}


def tx_effective_date(transaction: dict) -> str:
    return transaction.get("confirmDate") or transaction.get("date") or ""


def sort_transactions(transactions: list[dict]) -> list[dict]:
    indexed = list(enumerate(transactions))
    indexed.sort(
        key=lambda pair: (
            tx_effective_date(pair[1]),
            1 if pair[1].get("type") == "DIVIDEND_CASH" else 0,
            pair[1].get("dayOrder") if pair[1].get("dayOrder") is not None else float("inf"),
            TYPE_ORDER.get(pair[1].get("type", ""), 9),
            pair[0],
        )
    )
    return [item for _, item in indexed]


def resolve_amount(transaction: dict) -> float:
    amount = to_float(transaction.get("amount"))
    if amount > 0:
        return amount
    shares = to_float(transaction.get("shares"))
    nav = to_float(transaction.get("nav"))
    return r2(shares * nav) if shares > 0 and nav > 0 else 0.0


def resolve_buy_shares(transaction: dict) -> float:
    shares = to_float(transaction.get("shares"))
    if shares > 0:
        return r6(shares)
    amount = to_float(transaction.get("amount"))
    fee = to_float(transaction.get("fee"))
    net_amount = r2(max(0.0, amount - fee))
    nav = to_float(transaction.get("nav"))
    return r6(net_amount / nav) if nav > 0 and net_amount > 0 else 0.0


def resolve_sell_shares(transaction: dict) -> float:
    shares = to_float(transaction.get("shares"))
    if shares > 0:
        return r6(shares)
    amount = to_float(transaction.get("amount"))
    nav = to_float(transaction.get("nav"))
    return r6(amount / nav) if nav > 0 and amount > 0 else 0.0


def is_valid_correction(transaction: dict) -> bool:
    shares = to_float(transaction.get("shares"), float("nan"))
    nav = to_float(transaction.get("nav"), float("nan"))
    return math.isfinite(shares) and math.isfinite(nav) and shares >= 0 and nav > 0


def calc_correction_delta_total(transactions: list[dict]) -> float:
    current_shares = 0.0
    current_cost_total = 0.0
    delta_total = 0.0
    for transaction in sort_transactions(
        [item for item in transactions if item.get("status") == "CONFIRMED"]
    ):
        transaction_type = transaction.get("type", "")
        if transaction_type == "BUY":
            current_shares = r6(current_shares + resolve_buy_shares(transaction))
            current_cost_total = r2(current_cost_total + resolve_amount(transaction))
        elif transaction_type == "SELL":
            sell_shares = resolve_sell_shares(transaction)
            sold_cost = (
                r2(current_cost_total * min(sell_shares, current_shares) / current_shares)
                if current_shares > 0
                else 0
            )
            current_shares = r6(current_shares - sell_shares)
            current_cost_total = r2(current_cost_total - sold_cost)
            if current_shares <= EFFECTIVE_ZERO_SHARES:
                current_shares = 0.0
                current_cost_total = 0.0
        elif transaction_type == "DIVIDEND_REINVEST":
            reinvest_shares = to_float(transaction.get("shares"))
            if (
                reinvest_shares <= 0
                and to_float(transaction.get("nav")) > 0
                and to_float(transaction.get("amount")) > 0
            ):
                reinvest_shares = to_float(transaction.get("amount")) / to_float(transaction.get("nav"))
            current_shares = r6(current_shares + reinvest_shares)
        elif transaction_type == "CORRECTION":
            if not is_valid_correction(transaction):
                continue
            new_cost_total = r2(to_float(transaction.get("shares")) * to_float(transaction.get("nav")))
            delta_total = r2(delta_total + r2(new_cost_total - current_cost_total))
            current_shares = r6(to_float(transaction.get("shares")))
            current_cost_total = new_cost_total
    return delta_total


def calc_change_profit(shares: float, base_nav: float, change_percent, current_nav) -> float:
    if not math.isfinite(shares) or shares <= 0 or not math.isfinite(base_nav) or base_nav <= 0:
        return 0.0
    percent = parse_percent(change_percent)
    percent = percent if percent is not None else float("nan")
    nav = to_float(current_nav, float("nan"))
    if math.isfinite(nav) and nav > 0:
        difference = nav - base_nav
        difference_growth_rate = difference * 100 / base_nav
        if not math.isfinite(percent) or abs(difference_growth_rate - percent) <= NAV_CHANGE_MISMATCH_TOLERANCE_PERCENT:
            return r2(shares * difference)
    if not math.isfinite(percent):
        return 0.0
    return r2(shares * base_nav * percent / 100)


def uses_official_change_fallback(base_nav: float, change_percent, current_nav) -> bool:
    """Whether the official percentage is a total-return adjustment, not raw NAV movement."""
    if not math.isfinite(base_nav) or base_nav <= 0:
        return False
    parsed_percent = parse_percent(change_percent)
    percent = parsed_percent if parsed_percent is not None else float("nan")
    nav = to_float(current_nav, float("nan"))
    if not math.isfinite(percent) or not math.isfinite(nav) or nav <= 0:
        return False
    return abs((nav - base_nav) * 100 / base_nav - percent) > NAV_CHANGE_MISMATCH_TOLERANCE_PERCENT


def transaction_amount_on_date(transactions: list[dict], transaction_type: str, target_date: str) -> float:
    if not target_date:
        return 0.0
    total = 0.0
    for transaction in transactions:
        if (
            transaction.get("status") == "CONFIRMED"
            and transaction.get("type") == transaction_type
            and tx_effective_date(transaction) == target_date
        ):
            total = r2(total + to_float(transaction.get("amount")))
    return total


def reinvested_shares_on_date(transactions: list[dict], target_date: str) -> float:
    if not target_date:
        return 0.0
    total = 0.0
    for transaction in transactions:
        if (
            transaction.get("status") != "CONFIRMED"
            or transaction.get("type") != "DIVIDEND_REINVEST"
            or tx_effective_date(transaction) != target_date
        ):
            continue
        shares = to_float(transaction.get("shares"))
        if shares <= 0:
            amount = to_float(transaction.get("amount"))
            nav = to_float(transaction.get("nav"))
            shares = amount / nav if amount > 0 and nav > 0 else 0.0
        total = r6(total + shares)
    return total


def resolve_official_valuation_anchor(fund: dict, estimate: dict) -> dict:
    """Choose the newest observed official NAV without treating an estimate as official."""
    today = beijing_date_string()
    snapshot_nav = to_float(fund.get("lastNav"))
    snapshot_date = normalize_observed_day(fund.get("lastNavDate"), today=today)
    live_nav = to_float(estimate.get("dwjz"))
    live_date = normalize_observed_day(
        estimate.get("last_nav_date") or estimate.get("lastNavDate"),
        today=today,
    )

    use_live = live_nav > 0 and bool(live_date) and (
        not snapshot_date or live_date >= snapshot_date
    )
    if use_live:
        return {
            "nav": live_nav,
            "date": live_date,
            "source": "market_official_anchor",
            "freshened": not snapshot_date or live_date > snapshot_date or live_nav != snapshot_nav,
            "snapshot_date": snapshot_date,
        }
    return {
        "nav": snapshot_nav if snapshot_nav > 0 else 0.0,
        "date": snapshot_date,
        "source": "portfolio_snapshot" if snapshot_nav > 0 else "unavailable",
        "freshened": False,
        "snapshot_date": snapshot_date,
    }


def calc_fund_stats(fund: dict, estimate: Optional[dict] = None) -> dict:
    has_current_estimate = isinstance(estimate, dict) and bool(estimate)
    estimate = estimate if isinstance(estimate, dict) else {}
    shares = to_float(fund.get("holdingShares"))
    safe_shares = shares if shares > 0 else 0.0
    cost_per_share = to_float(fund.get("holdingCost"))
    valuation_anchor = resolve_official_valuation_anchor(fund, estimate)
    official_nav = valuation_anchor["nav"]
    valuation_available = official_nav > 0

    fallback_cost_total = r2(safe_shares * cost_per_share) if safe_shares > 0 and cost_per_share > 0 else 0.0
    stored_cost_total = to_float(fund.get("holdingCostTotal"), float("nan"))
    cost_total = (
        stored_cost_total
        if safe_shares > 0 and math.isfinite(stored_cost_total) and stored_cost_total >= 0
        else fallback_cost_total
    )

    transactions = fund.get("transactions") or []
    buy_total = 0.0
    total_sold = 0.0
    for transaction in transactions:
        if transaction.get("status", "") != "CONFIRMED":
            continue
        if transaction.get("type", "") == "BUY":
            buy_total = r2(buy_total + resolve_amount(transaction))
        elif transaction.get("type", "") == "SELL":
            total_sold = r2(total_sold + resolve_amount(transaction))
    total_invested = r2(buy_total + calc_correction_delta_total(transactions))

    market_value = r2(safe_shares * official_nav) if valuation_available else 0.0
    holding_profit = r2(market_value - cost_total) if valuation_available else 0.0
    sold_cost = r2(max(0.0, total_invested - cost_total)) if total_invested > 0 else 0.0
    realized_fallback = r2(total_sold - sold_cost) if total_invested > 0 else 0.0
    raw_realized = to_float(fund.get("realizedProfit"), float("nan"))
    realized = raw_realized if math.isfinite(raw_realized) else realized_fallback
    total_profit = r2(holding_profit + realized)
    holding_return_rate = ratio_pct(holding_profit, cost_total) if valuation_available else None

    source = (
        str(estimate.get("source") or "")
        if has_current_estimate
        else "unavailable"
    )
    official_attribution_date = (
        resolve_official_attribution_date(fund, estimate)
        if source == "official_published"
        else ""
    )
    current_estimated_nav = to_float(estimate.get("estimatedNav") or estimate.get("nav"))
    current_previous_nav = to_float(estimate.get("prev_dwjz") or estimate.get("prevNav"))
    current_change_percent = estimate.get("estimatedChangePercent")
    if current_change_percent is None:
        current_change_percent = estimate.get("gszzl")
    estimate_freshness = str(
        estimate.get("freshness")
        or ("stale" if estimate.get("stale") is True else "")
        or ""
    ).strip().lower()
    stale_frame = source != "official_published" and (
        estimate.get("stale") is True
        or estimate.get("estimateStale") is True
        or estimate_freshness == "stale"
    )
    estimate_available = has_current_estimate and estimate_frame_available(estimate)
    displayed_day_attributable = estimate_available and (
        source != "official_published" or bool(official_attribution_date)
    )
    estimated_nav = current_estimated_nav
    if estimated_nav <= 0:
        estimated_nav = 0.0
    estimated_change_percent = (
        current_change_percent
        if current_change_percent is not None
        else None
    )
    estimate_stale = stale_frame
    estimate_display_date = normalize_observed_day(
        estimate.get("display_date") or estimate.get("displayDate")
    )
    target_nav_date = normalize_observed_day(
        estimate.get("target_nav_date") or estimate.get("targetNavDate")
    )
    latest_official_nav_date = normalize_observed_day(
        estimate.get("last_nav_date")
        or estimate.get("lastNavDate")
        or fund.get("lastNavDate")
    )
    last_nav_publish_date = normalize_observed_day(
        estimate.get("last_nav_publish_date")
        or estimate.get("lastNavPublishDate")
        or fund.get("lastNavPublishDate")
    )
    effective_date = (
        official_attribution_date
        if source == "official_published"
        else estimate_display_date
        or normalize_observed_day(fund.get("displayDate"))
        or beijing_date_string()
    )
    dividend_event_date = (
        normalize_observed_day(
            estimate.get("last_nav_date")
            or estimate.get("lastNavDate")
            or fund.get("lastNavDate")
        )
        if source == "official_published"
        else effective_date
    )
    cash_dividend_today = (
        transaction_amount_on_date(transactions, "DIVIDEND_CASH", dividend_event_date)
        if displayed_day_attributable
        else 0.0
    )
    reinvested_shares_today = (
        reinvested_shares_on_date(transactions, dividend_event_date)
        if displayed_day_attributable
        else 0.0
    )
    official_fallback = displayed_day_attributable and uses_official_change_fallback(
        current_previous_nav,
        current_change_percent,
        current_estimated_nav,
    )
    market_shares = (
        max(0.0, r6(safe_shares - reinvested_shares_today))
        if official_fallback
        else safe_shares
    )
    market_day_profit = (
        0.0
        if source == "reset" or not displayed_day_attributable
        else calc_change_profit(
            market_shares,
            current_previous_nav,
            current_change_percent,
            current_estimated_nav,
        )
    )
    today_profit = r2(market_day_profit + (0.0 if official_fallback else cash_dividend_today))
    day_base_market_value = (
        r2(market_shares * current_previous_nav)
        if displayed_day_attributable and market_shares > 0 and current_previous_nav > 0
        else 0.0
    )
    estimated_market_value = (
        r2(safe_shares * estimated_nav)
        if estimate_available and estimated_nav > 0
        else None
    )
    return {
        "marketValue": market_value,
        "currentMarketValue": market_value,
        "costPerShare": r4(cost_per_share),
        "costTotal": cost_total,
        "holdingShares": r6(safe_shares),
        "holdingProfit": holding_profit,
        "realizedProfit": r2(realized),
        "totalProfit": total_profit,
        "totalInvested": total_invested,
        "returnRate": holding_return_rate,
        "holdingReturnRate": holding_return_rate,
        "todayProfit": today_profit,
        "dayProfit": today_profit,
        "dayBaseMarketValue": day_base_market_value,
        "currentNav": official_nav,
        "lastNav": official_nav if official_nav > 0 else None,
        "valuationNavDate": valuation_anchor["date"] or None,
        "portfolioSnapshotNavDate": valuation_anchor["snapshot_date"] or None,
        "valuationSource": valuation_anchor["source"],
        "valuationFreshenedFromMarketData": valuation_anchor["freshened"],
        "valuationAvailable": valuation_available,
        "estimatedMarketValue": estimated_market_value,
        "estimatedNav": estimated_nav if estimate_available and estimated_nav > 0 else None,
        "estimatedChangePercent": estimated_change_percent if estimate_available else None,
        "displayedDayAttributable": displayed_day_attributable,
        "estimateSource": source,
        "estimateAvailable": estimate_available,
        "estimateFreshness": estimate_freshness or None,
        "estimateStale": estimate_stale,
        # Date roles are deliberately separate: target/latest NAV are D days;
        # returnAttributionDate is the reliable user-visible G day.
        "estimateDisplayDate": (
            effective_date
            if estimate_available and effective_date
            else None
        ),
        "targetNavDate": target_nav_date or None,
        "latestOfficialNavDate": latest_official_nav_date or None,
        "lastNavPublishDate": last_nav_publish_date or None,
        "returnAttributionDate": (
            effective_date if displayed_day_attributable else None
        ),
    }
