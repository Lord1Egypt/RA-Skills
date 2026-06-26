"""
polymarket-24h-equity-strike-trader
Trades structural mispricings in equity/stock price-threshold markets on
Polymarket by reconstructing the implied probability curve across strike
levels for the same company and period, then identifying violations.

Core edge: Polymarket lists equity strike-ladder markets analogous to
options chains:

    "Will PLTR finish week above $152?" = 7%
    "Will PLTR finish week above $153?" = 23.5%   <- VIOLATION (higher than $152!)
    "Will PLTR finish week above $154?" = 18.5%

Monotonicity must hold:
    P(above $152) >= P(above $153) >= P(above $154)

Range/bin consistency must hold:
    P(350-375k deliveries) + P(375-400k) + P(<350k) + P(>400k) ~= 100%

When these relationships break, the curve is internally inconsistent --
pure mathematical arbitrage, not opinion.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag.
"""
import os
import re
import argparse
from datetime import datetime, timezone
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-24h-equity-strike-trader"
SKILL_SLUG   = "polymarket-24h-equity-strike-trader"

KEYWORDS = [
    "Microsoft", "Palantir", "NVIDIA", "Tesla",
    "SpaceX", "Nasdaq", "Apple", "Amazon", "Meta",
    "finish week", "market cap", "deliver",
]

# Risk parameters -- declared as tunables in clawhub.json, adjustable from Simmer UI.
MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  "40"))
MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    "5000"))
MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.08"))
MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      "0"))
MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "8"))
YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.38"))
NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",  "0.62"))
MIN_TRADE      = float(os.environ.get("SIMMER_MIN_TRADE",     "5"))
# Minimum curve violation magnitude to trade (prevents noise trades)
MIN_VIOLATION  = float(os.environ.get("SIMMER_MIN_VIOLATION",  "0.03"))

_client: SimmerClient | None = None


def get_client(live: bool = False) -> SimmerClient:
    global _client, MAX_POSITION, MIN_VOLUME, MAX_SPREAD, MIN_DAYS, MAX_POSITIONS
    global YES_THRESHOLD, NO_THRESHOLD, MIN_TRADE, MIN_VIOLATION
    if _client is None:
        venue = "polymarket" if live else "sim"
        _client = SimmerClient(
            api_key=os.environ["SIMMER_API_KEY"],
            venue=venue,
        )
        if live:
            _client.live = True
        try:
            _client.apply_skill_config(SKILL_SLUG)
        except AttributeError:
            pass  # apply_skill_config only available in Simmer runtime
        MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  str(MAX_POSITION)))
        MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    str(MIN_VOLUME)))
        MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    str(MAX_SPREAD)))
        MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      str(MIN_DAYS)))
        MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", str(MAX_POSITIONS)))
        YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD", str(YES_THRESHOLD)))
        NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",  str(NO_THRESHOLD)))
        MIN_TRADE      = float(os.environ.get("SIMMER_MIN_TRADE",     str(MIN_TRADE)))
        MIN_VIOLATION  = float(os.environ.get("SIMMER_MIN_VIOLATION",  str(MIN_VIOLATION)))
    return _client


# ---------------------------------------------------------------------------
# Market parsing -- extract company/ticker, strike, date/period, and type
# ---------------------------------------------------------------------------

_TICKERS = {
    "microsoft": "MSFT", "msft": "MSFT",
    "palantir": "PLTR", "pltr": "PLTR",
    "nvidia": "NVDA", "nvda": "NVDA",
    "tesla": "TSLA", "tsla": "TSLA",
    "spacex": "SPACEX",
    "apple": "AAPL", "aapl": "AAPL",
    "amazon": "AMZN", "amzn": "AMZN",
    "google": "GOOG", "goog": "GOOG", "alphabet": "GOOG",
    "meta": "META",
    "nasdaq": "NDX", "nasdaq-100": "NDX", "nasdaq 100": "NDX",
}

_DATE_PATTERNS = [
    # "finish week above" -- week-ending context
    re.compile(r"finish\s+week", re.I),
    # "on March 27" / "on March 28"
    re.compile(r"on\s+((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2})", re.I),
    # "March 23-29" / "March 23 - 29"
    re.compile(r"((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}\s*[-\u2013]\s*\d{1,2})", re.I),
    # "in Q1" / "in 2025"
    re.compile(r"in\s+(Q[1-4]\s*\d{4}|\d{4})", re.I),
    # "in March" / "in April"
    re.compile(r"in\s+((?:January|February|March|April|May|June|July|August|September|October|November|December)(?:\s+\d{4})?)", re.I),
    # "by end of March"
    re.compile(r"by\s+end\s+of\s+((?:January|February|March|April|May|June|July|August|September|October|November|December))", re.I),
]

# "above $152" / "reach $370" / "exceed $400"
_PRICE_ABOVE = re.compile(
    r"(?:above|reach|hit|exceed|surpass|break|over)\s+\$?([\d,.]+)", re.I
)
# "between $350k and $375k" or "between 350 and 375"
_PRICE_BETWEEN = re.compile(
    r"between\s+\$?([\d,.]+)\s*[k]?\s*(?:and|-)\s*\$?([\d,.]+)\s*[k]?", re.I
)
# "below $150" / "under $300k"
_PRICE_BELOW = re.compile(
    r"(?:below|under|less\s+than)\s+\$?([\d,.]+)", re.I
)
# Bin patterns like "<350k" or "350-375k" in delivery/unit markets
_BIN_RANGE = re.compile(
    r"([\d,.]+)\s*[k]?\s*[-\u2013]\s*([\d,.]+)\s*[k]?", re.I
)
_BIN_LESS = re.compile(r"<\s*([\d,.]+)\s*[k]?", re.I)
_BIN_MORE = re.compile(r">\s*([\d,.]+)\s*[k]?", re.I)


def _parse_num(s: str) -> float:
    """Parse a number string, handling commas and optional 'k' suffix."""
    s = s.replace(",", "").strip()
    return float(s)


def parse_ticker(question: str) -> str | None:
    q = question.lower()
    for keyword, ticker in _TICKERS.items():
        if keyword in q:
            return ticker
    return None


def parse_date_key(question: str) -> str | None:
    for pat in _DATE_PATTERNS:
        m = pat.search(question)
        if m:
            groups = m.groups()
            if groups:
                return groups[0].strip().lower()
            # "finish week" pattern has no capture group
            return "week"
    return None


def parse_threshold(question: str) -> dict | None:
    """
    Parse a market question into a structured threshold descriptor.
    Returns dict with keys: type ("above"|"between"|"below"), strike/lo/hi.
    """
    q = question

    # Check between first (more specific)
    m = _PRICE_BETWEEN.search(q)
    if m:
        lo, hi = _parse_num(m.group(1)), _parse_num(m.group(2))
        # Handle 'k' suffix in context (e.g., "350-375k deliveries")
        if "k" in q[m.start():m.end() + 5].lower():
            if lo < 1000:
                lo *= 1000
            if hi < 1000:
                hi *= 1000
        return {"type": "between", "lo": lo, "hi": hi}

    # Bin patterns for delivery/unit markets
    m = _BIN_LESS.search(q)
    if m:
        strike = _parse_num(m.group(1))
        if "k" in q[m.start():m.end() + 3].lower():
            if strike < 1000:
                strike *= 1000
        return {"type": "below", "strike": strike}

    m = _BIN_MORE.search(q)
    if m:
        strike = _parse_num(m.group(1))
        if "k" in q[m.start():m.end() + 3].lower():
            if strike < 1000:
                strike *= 1000
        return {"type": "above", "strike": strike}

    m = _PRICE_ABOVE.search(q)
    if m:
        strike = _parse_num(m.group(1))
        return {"type": "above", "strike": strike}

    m = _PRICE_BELOW.search(q)
    if m:
        strike = _parse_num(m.group(1))
        return {"type": "below", "strike": strike}

    return None


# ---------------------------------------------------------------------------
# Curve construction and violation detection
# ---------------------------------------------------------------------------

class CurvePoint:
    """One market mapped to a point on the implied strike curve."""
    __slots__ = ("market", "ticker", "date_key", "threshold", "price")

    def __init__(self, market, ticker, date_key, threshold, price):
        self.market = market
        self.ticker = ticker
        self.date_key = date_key
        self.threshold = threshold
        self.price = price


def build_curves(markets: list) -> dict[str, list[CurvePoint]]:
    """
    Group markets into curves keyed by (ticker, date/period).
    Each curve contains CurvePoints sorted by strike price.
    """
    curves: dict[str, list[CurvePoint]] = {}
    for m in markets:
        q = getattr(m, "question", "")
        p = getattr(m, "current_probability", None)
        if not isinstance(p, (int, float)):
            continue

        ticker = parse_ticker(q)
        date_key = parse_date_key(q)
        threshold = parse_threshold(q)
        if not ticker or not date_key or not threshold:
            continue

        key = f"{ticker}|{date_key}"
        point = CurvePoint(m, ticker, date_key, threshold, float(p))
        curves.setdefault(key, []).append(point)

    return curves


def find_violations(curve: list[CurvePoint]) -> list[tuple]:
    """
    Analyze a single curve for mathematical violations.
    Returns list of (market, side, violation_magnitude, reasoning).

    Checks:
    1. Monotonicity: P(above $X) must decrease as X increases
    2. Range-sum consistency: bin probabilities must be coherent with
       above/below thresholds
    """
    opportunities = []

    # Separate by type
    above_points = [pt for pt in curve if pt.threshold.get("type") == "above"]
    between_points = [pt for pt in curve if pt.threshold.get("type") == "between"]
    below_points = [pt for pt in curve if pt.threshold.get("type") == "below"]

    # Sort above points by strike (ascending)
    above_points.sort(key=lambda pt: pt.threshold["strike"])

    # Build strike->point lookup for above markets
    above_map: dict[float, CurvePoint] = {}
    for pt in above_points:
        strike = pt.threshold["strike"]
        if strike not in above_map:
            above_map[strike] = pt

    strikes_sorted = sorted(above_map.keys())

    # --- Check 1: Monotonicity ---
    # P(above lower_strike) >= P(above higher_strike)
    for i in range(len(strikes_sorted) - 1):
        lo_strike = strikes_sorted[i]
        hi_strike = strikes_sorted[i + 1]
        lo_pt = above_map[lo_strike]
        hi_pt = above_map[hi_strike]

        violation = hi_pt.price - lo_pt.price  # positive = broken monotonicity
        if violation > MIN_VIOLATION:
            # Higher strike overpriced: sell NO on it
            opportunities.append((
                hi_pt.market, "no", violation,
                f"Monotonicity break: P(>{hi_strike:,.0f})={hi_pt.price:.1%} > "
                f"P(>{lo_strike:,.0f})={lo_pt.price:.1%} | "
                f"violation={violation:.1%} -- {hi_pt.market.question[:55]}"
            ))
            # Lower strike underpriced: buy YES on it
            opportunities.append((
                lo_pt.market, "yes", violation,
                f"Monotonicity break: P(>{lo_strike:,.0f})={lo_pt.price:.1%} < "
                f"P(>{hi_strike:,.0f})={hi_pt.price:.1%} | "
                f"violation={violation:.1%} -- {lo_pt.market.question[:55]}"
            ))

    # --- Check 2: Range consistency ---
    # For "between $X and $Y": price should equal P(above $X) - P(above $Y)
    for pt in between_points:
        lo = pt.threshold["lo"]
        hi = pt.threshold["hi"]

        lo_pt = above_map.get(lo)
        hi_pt = above_map.get(hi)

        if lo_pt is None or hi_pt is None:
            continue

        implied_range = lo_pt.price - hi_pt.price
        actual_range = pt.price
        violation = actual_range - implied_range

        if abs(violation) > MIN_VIOLATION:
            if violation > 0:
                opportunities.append((
                    pt.market, "no", abs(violation),
                    f"Range overpriced: P({lo:,.0f}-{hi:,.0f})={actual_range:.1%} but "
                    f"implied={implied_range:.1%} | "
                    f"violation={violation:.1%} -- {pt.market.question[:50]}"
                ))
            else:
                opportunities.append((
                    pt.market, "yes", abs(violation),
                    f"Range underpriced: P({lo:,.0f}-{hi:,.0f})={actual_range:.1%} but "
                    f"implied={implied_range:.1%} | "
                    f"violation={abs(violation):.1%} -- {pt.market.question[:50]}"
                ))

    # --- Check 3: Bin-sum consistency ---
    # If we have a full set of bins (below, between-ranges, above) they must sum ~100%
    if between_points and (above_points or below_points):
        bin_sum = sum(pt.price for pt in between_points)
        for pt in below_points:
            bin_sum += pt.price
        # Add the highest "above" point if it exists (acts as the >max bin)
        if above_points:
            highest_above = max(above_points, key=lambda pt: pt.threshold["strike"])
            bin_sum += highest_above.price

        overshoot = bin_sum - 1.0
        if abs(overshoot) > MIN_VIOLATION and len(between_points) + len(below_points) >= 2:
            # Find the bin that is most likely mispriced (furthest from expected)
            all_bins = between_points + below_points
            if above_points:
                all_bins.append(highest_above)

            if overshoot > 0:
                # Total > 100%: some bin is overpriced
                most_overpriced = max(all_bins, key=lambda pt: pt.price)
                opportunities.append((
                    most_overpriced.market, "no", abs(overshoot),
                    f"Bin-sum={bin_sum:.1%} (>{1.0:.0%}): overpriced bin at "
                    f"{most_overpriced.price:.1%} | violation={overshoot:.1%} "
                    f"-- {most_overpriced.market.question[:50]}"
                ))
            else:
                # Total < 100%: some bin is underpriced
                most_underpriced = min(all_bins, key=lambda pt: pt.price)
                opportunities.append((
                    most_underpriced.market, "yes", abs(overshoot),
                    f"Bin-sum={bin_sum:.1%} (<{1.0:.0%}): underpriced bin at "
                    f"{most_underpriced.price:.1%} | violation={abs(overshoot):.1%} "
                    f"-- {most_underpriced.market.question[:50]}"
                ))

    return opportunities


# ---------------------------------------------------------------------------
# Signal, safeguards, execution
# ---------------------------------------------------------------------------

def valid_market(market) -> tuple[bool, str]:
    p = getattr(market, "current_probability", None)
    if not isinstance(p, (int, float)):
        return False, "missing probability"

    spread_cents = getattr(market, "spread_cents", None)
    if isinstance(spread_cents, (int, float)) and spread_cents / 100 > MAX_SPREAD:
        return False, f"Spread {spread_cents/100:.1%} > {MAX_SPREAD:.1%}"

    resolves_at = getattr(market, "resolves_at", None)
    if resolves_at:
        try:
            resolves = datetime.fromisoformat(resolves_at.replace("Z", "+00:00"))
            days = (resolves - datetime.now(timezone.utc)).days
            if days < MIN_DAYS:
                return False, f"Only {days} days to resolve"
        except Exception:
            pass

    return True, "ok"


def compute_signal(market, opportunity: tuple | None) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    Conviction scales with the magnitude of the curve violation.
    Threshold gates (YES_THRESHOLD / NO_THRESHOLD) still apply as hard limits.
    """
    ok, why = valid_market(market)
    if not ok:
        return None, 0, why

    if not opportunity:
        return None, 0, "No curve violation found"

    _, side, violation_mag, reason = opportunity
    p = float(getattr(market, "current_probability", 0))

    if side == "yes":
        if p > YES_THRESHOLD:
            return None, 0, f"YES blocked at {p:.1%}; threshold is {YES_THRESHOLD:.0%}"
        conviction = min(1.0, max(0.0, (violation_mag - MIN_VIOLATION) / max(0.01, YES_THRESHOLD)))
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        return "yes", size, reason

    if side == "no":
        if p < NO_THRESHOLD:
            return None, 0, f"NO blocked at {p:.1%}; threshold is {NO_THRESHOLD:.0%}"
        conviction = min(1.0, max(0.0, (violation_mag - MIN_VIOLATION) / max(0.01, 1 - NO_THRESHOLD)))
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        return "no", size, reason

    return None, 0, "Unknown side"


def context_ok(client: SimmerClient, market_id: str) -> tuple[bool, str]:
    """Check flip-flop and slippage safeguards."""
    try:
        ctx = client.get_market_context(market_id)
        if not ctx:
            return True, "no context"
        if ctx.get("discipline", {}).get("is_flip_flop"):
            reason = ctx["discipline"].get("flip_flop_reason", "recent reversal")
            return False, f"Flip-flop: {reason}"
        slip = ctx.get("slippage", {})
        if isinstance(slip, dict) and slip.get("slippage_pct", 0) > 0.15:
            return False, f"Slippage {slip['slippage_pct']:.1%}"
        for w in ctx.get("warnings", []):
            print(f"  [warn] {w}")
    except Exception as e:
        print(f"  [ctx] {market_id}: {e}")
    return True, "ok"


def find_markets(client: SimmerClient) -> list:
    """Find active equity price-threshold markets, deduplicated.
    Filters out non-threshold markets."""
    seen, unique = set(), []
    for kw in KEYWORDS:
        try:
            for m in client.find_markets(query=kw):
                market_id = getattr(m, "id", None)
                if market_id and market_id not in seen:
                    q = getattr(m, "question", "").lower()
                    if any(w in q for w in (
                        "above", "between", "below",
                        "deliver", "finish", "market cap",
                    )):
                        seen.add(market_id)
                        unique.append(m)
        except Exception as e:
            print(f"[search] {kw!r}: {e}")
    return unique


def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    print(f"[24h-equity-strike] mode={mode} max_pos=${MAX_POSITION} min_violation={MIN_VIOLATION:.0%}")

    client = get_client(live=live)
    markets = find_markets(client)
    print(f"[24h-equity-strike] {len(markets)} candidate markets")

    # Build implied strike curves
    curves = build_curves(markets)
    print(f"[24h-equity-strike] {len(curves)} curves: {', '.join(f'{k}({len(v)} pts)' for k, v in curves.items())}")

    # Log each curve's structure
    for curve_key, points in curves.items():
        above_pts = sorted(
            [pt for pt in points if pt.threshold.get("type") == "above"],
            key=lambda pt: pt.threshold["strike"],
        )
        between_pts = [pt for pt in points if pt.threshold.get("type") == "between"]
        below_pts = [pt for pt in points if pt.threshold.get("type") == "below"]
        print(f"  [{curve_key}] above-strikes: " + ", ".join(
            f"${pt.threshold['strike']:,.0f}={pt.price:.1%}" for pt in above_pts
        ))
        for pt in between_pts:
            print(f"  [{curve_key}] range: ${pt.threshold['lo']:,.0f}-${pt.threshold['hi']:,.0f}={pt.price:.1%}")
        for pt in below_pts:
            print(f"  [{curve_key}] below: ${pt.threshold['strike']:,.0f}={pt.price:.1%}")

    # Find violations across all curves
    all_opps: dict[str, tuple] = {}
    for curve_key, points in curves.items():
        if len(points) < 2:
            continue
        violations = find_violations(points)
        for market, side, mag, reason in violations:
            mid = getattr(market, "id", None)
            if not mid:
                continue
            existing = all_opps.get(mid)
            if existing is None or mag > existing[2]:
                all_opps[mid] = (market, side, mag, reason)

    print(f"[24h-equity-strike] {len(all_opps)} violation opportunities")

    # Execute trades on best violations
    placed = 0
    for market_id, opp in sorted(all_opps.items(), key=lambda x: -x[1][2]):
        if placed >= MAX_POSITIONS:
            break

        market = opp[0]
        side, size, reasoning = compute_signal(market, opp)
        if not side:
            print(f"  [skip] {reasoning}")
            continue

        ok, why = context_ok(client, market_id)
        if not ok:
            print(f"  [skip] {why}")
            continue

        try:
            r = client.trade(
                market_id=market_id,
                side=side,
                amount=size,
                source=TRADE_SOURCE,
                skill_slug=SKILL_SLUG,
                reasoning=reasoning,
            )
            tag = "(sim)" if r.simulated else "(live)"
            status = "OK" if r.success else f"FAIL:{r.error}"
            print(f"  [trade] {side.upper()} ${size} {tag} {status} -- {reasoning[:110]}")
            if r.success:
                placed += 1
        except Exception as e:
            print(f"  [error] {market_id}: {e}")

    print(f"[24h-equity-strike] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Trades structural mispricings in equity strike-ladder markets on Polymarket."
    )
    ap.add_argument(
        "--live",
        action="store_true",
        help="Real trades on Polymarket. Default is paper (sim) mode.",
    )
    run(live=ap.parse_args().live)
