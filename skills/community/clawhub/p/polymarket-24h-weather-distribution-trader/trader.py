"""
polymarket-24h-weather-distribution-trader
Trades mispricings in weather temperature-bin markets on Polymarket
by reconstructing the implied probability distribution across bins
for the same city and date, then identifying sum violations and
monotonicity breaks on cumulative markets.

Core edge: Polymarket lists multiple temperature bins for the same city
and date:
    "Will the highest temperature in Munich be 8C on March 28?" = 40%
    "Will the highest temperature in Munich be 9C on March 28?" = 45%
    "Will the highest temperature in Munich be 10C on March 28?" = 16%

These bins form a PROBABILITY DISTRIBUTION that must sum to ~100%.
When they don't, individual bins are mispriced. Additionally, cumulative
markets ("X C or below", "X C or higher") must be monotonic.

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

TRADE_SOURCE = "sdk:polymarket-24h-weather-distribution-trader"
SKILL_SLUG   = "polymarket-24h-weather-distribution-trader"

KEYWORDS = [
    "temperature", "highest temperature", "high temp",
    "temp in", "degrees",
]

CITIES = [
    "chengdu", "shenzhen", "munich", "dallas", "austin",
    "san francisco", "seoul", "chicago", "wuhan", "miami",
    "seattle", "los angeles", "la", "denver", "nyc", "new york",
]

# Risk parameters — declared as tunables in clawhub.json, adjustable from Simmer UI.
MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  "40"))
MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    "5000"))
MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.08"))
MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      "0"))
MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "8"))
YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.38"))
NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",  "0.62"))
MIN_TRADE      = float(os.environ.get("SIMMER_MIN_TRADE",     "5"))
SUM_TOLERANCE  = float(os.environ.get("SIMMER_SUM_TOLERANCE", "0.05"))

_client: SimmerClient | None = None


def get_client(live: bool = False) -> SimmerClient:
    global _client, MAX_POSITION, MIN_VOLUME, MAX_SPREAD, MIN_DAYS, MAX_POSITIONS
    global YES_THRESHOLD, NO_THRESHOLD, MIN_TRADE, SUM_TOLERANCE
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
        SUM_TOLERANCE  = float(os.environ.get("SIMMER_SUM_TOLERANCE", str(SUM_TOLERANCE)))
    return _client


# ---------------------------------------------------------------------------
# Market parsing — extract city, temperature, date, and bin type
# ---------------------------------------------------------------------------

_CITY_PATTERNS = {c: re.compile(re.escape(c), re.I) for c in CITIES}

_DATE_PATTERNS = [
    re.compile(
        r"on\s+((?:January|February|March|April|May|June|July|August|"
        r"September|October|November|December)\s+\d{1,2})", re.I
    ),
    re.compile(
        r"((?:January|February|March|April|May|June|July|August|"
        r"September|October|November|December)\s+\d{1,2},?\s*\d{4})", re.I
    ),
]

# Exact bin: "be 8C", "be 8 C", "be 8 degrees"
_EXACT_TEMP = re.compile(
    r"(?:be|is)\s+(-?\d+)\s*(?:°|degrees?\s*)?C\b", re.I
)
# Cumulative lower: "8C or below", "8 C or lower", "8 degrees or less"
_OR_BELOW = re.compile(
    r"(-?\d+)\s*(?:°|degrees?\s*)?C\s+or\s+(?:below|lower|less)", re.I
)
# Cumulative upper: "8C or above", "8 C or higher", "8 degrees or more"
_OR_HIGHER = re.compile(
    r"(-?\d+)\s*(?:°|degrees?\s*)?C\s+or\s+(?:above|higher|more)", re.I
)


def parse_city(question: str) -> str | None:
    q = question.lower()
    for city, pat in _CITY_PATTERNS.items():
        if pat.search(q):
            # Normalize LA / NYC
            if city in ("la", "los angeles"):
                return "los angeles"
            if city in ("nyc", "new york"):
                return "new york"
            return city
    return None


def parse_date_key(question: str) -> str | None:
    for pat in _DATE_PATTERNS:
        m = pat.search(question)
        if m:
            return m.group(1).strip().lower()
    return None


def parse_temp_bin(question: str) -> dict | None:
    """
    Parse a temperature market question.
    Returns dict with keys: type ("exact"|"or_below"|"or_higher"), temp (int).
    """
    m = _OR_BELOW.search(question)
    if m:
        return {"type": "or_below", "temp": int(m.group(1))}

    m = _OR_HIGHER.search(question)
    if m:
        return {"type": "or_higher", "temp": int(m.group(1))}

    m = _EXACT_TEMP.search(question)
    if m:
        return {"type": "exact", "temp": int(m.group(1))}

    return None


# ---------------------------------------------------------------------------
# Distribution construction and violation detection
# ---------------------------------------------------------------------------

class TempBin:
    """One market mapped to a point in the temperature distribution."""
    __slots__ = ("market", "city", "date_key", "bin_info", "price")

    def __init__(self, market, city, date_key, bin_info, price):
        self.market = market
        self.city = city
        self.date_key = date_key
        self.bin_info = bin_info
        self.price = price


def build_distributions(markets: list) -> dict[str, list[TempBin]]:
    """
    Group markets into distributions keyed by (city, date).
    Each distribution contains TempBin entries.
    """
    distributions: dict[str, list[TempBin]] = {}
    for m in markets:
        q = getattr(m, "question", "")
        p = getattr(m, "current_probability", None)
        if not isinstance(p, (int, float)):
            continue

        city = parse_city(q)
        date_key = parse_date_key(q)
        bin_info = parse_temp_bin(q)
        if not city or not date_key or not bin_info:
            continue

        key = f"{city}|{date_key}"
        tb = TempBin(m, city, date_key, bin_info, float(p))
        distributions.setdefault(key, []).append(tb)

    return distributions


def find_violations(dist: list[TempBin]) -> list[tuple]:
    """
    Analyze a single (city, date) distribution for violations.
    Returns list of (market, side, violation_magnitude, reasoning).

    Checks:
    1. Sum check: exact bins must sum to ~100% (+/- SUM_TOLERANCE)
    2. Monotonicity: "X C or below" must increase with X;
       "X C or higher" must decrease with X
    3. Most mispriced bin identification when sum deviates
    """
    opportunities = []

    exact_bins = [tb for tb in dist if tb.bin_info["type"] == "exact"]
    or_below_bins = [tb for tb in dist if tb.bin_info["type"] == "or_below"]
    or_higher_bins = [tb for tb in dist if tb.bin_info["type"] == "or_higher"]

    # --- Check 1: Exact bin sum ---
    if len(exact_bins) >= 2:
        exact_bins_sorted = sorted(exact_bins, key=lambda tb: tb.bin_info["temp"])
        total = sum(tb.price for tb in exact_bins_sorted)
        deviation = total - 1.0  # positive = overpriced, negative = underpriced

        if abs(deviation) > SUM_TOLERANCE:
            # Find the most mispriced bin:
            # For overpriced distributions (sum > 1): the bin with highest price
            # relative to its neighbors is likely the most overpriced
            # For underpriced distributions (sum < 1): the bin with lowest price
            # relative to its neighbors is the most underpriced
            if deviation > 0:
                # Sum too high — sell the most overpriced bin
                # Score each bin by how much it exceeds neighbors
                target = _find_outlier_bin(exact_bins_sorted, direction="high")
                if target:
                    mag = abs(deviation) / len(exact_bins_sorted)
                    opportunities.append((
                        target.market, "no", abs(deviation),
                        f"Sum={total:.1%} (>{1+SUM_TOLERANCE:.0%}): "
                        f"overpriced bin {target.bin_info['temp']}C={target.price:.1%} "
                        f"deviation={deviation:+.1%} — {target.market.question[:55]}"
                    ))
            else:
                # Sum too low — buy the most underpriced bin
                target = _find_outlier_bin(exact_bins_sorted, direction="low")
                if target:
                    mag = abs(deviation) / len(exact_bins_sorted)
                    opportunities.append((
                        target.market, "yes", abs(deviation),
                        f"Sum={total:.1%} (<{1-SUM_TOLERANCE:.0%}): "
                        f"underpriced bin {target.bin_info['temp']}C={target.price:.1%} "
                        f"deviation={deviation:+.1%} — {target.market.question[:55]}"
                    ))

    # --- Check 2: Monotonicity on "or below" cumulative bins ---
    if len(or_below_bins) >= 2:
        or_below_sorted = sorted(or_below_bins, key=lambda tb: tb.bin_info["temp"])
        for i in range(len(or_below_sorted) - 1):
            lo_tb = or_below_sorted[i]
            hi_tb = or_below_sorted[i + 1]
            # P(X C or below) must increase with X
            violation = lo_tb.price - hi_tb.price  # positive = monotonicity break
            if violation > SUM_TOLERANCE:
                opportunities.append((
                    lo_tb.market, "no", violation,
                    f"Cumulative break: P(<={lo_tb.bin_info['temp']}C)={lo_tb.price:.1%} > "
                    f"P(<={hi_tb.bin_info['temp']}C)={hi_tb.price:.1%} "
                    f"violation={violation:.1%} — {lo_tb.market.question[:55]}"
                ))
                opportunities.append((
                    hi_tb.market, "yes", violation,
                    f"Cumulative break: P(<={hi_tb.bin_info['temp']}C)={hi_tb.price:.1%} < "
                    f"P(<={lo_tb.bin_info['temp']}C)={lo_tb.price:.1%} "
                    f"violation={violation:.1%} — {hi_tb.market.question[:55]}"
                ))

    # --- Check 3: Monotonicity on "or higher" cumulative bins ---
    if len(or_higher_bins) >= 2:
        or_higher_sorted = sorted(or_higher_bins, key=lambda tb: tb.bin_info["temp"])
        for i in range(len(or_higher_sorted) - 1):
            lo_tb = or_higher_sorted[i]
            hi_tb = or_higher_sorted[i + 1]
            # P(X C or higher) must decrease with X
            violation = hi_tb.price - lo_tb.price  # positive = monotonicity break
            if violation > SUM_TOLERANCE:
                opportunities.append((
                    hi_tb.market, "no", violation,
                    f"Cumulative break: P(>={hi_tb.bin_info['temp']}C)={hi_tb.price:.1%} > "
                    f"P(>={lo_tb.bin_info['temp']}C)={lo_tb.price:.1%} "
                    f"violation={violation:.1%} — {hi_tb.market.question[:55]}"
                ))
                opportunities.append((
                    lo_tb.market, "yes", violation,
                    f"Cumulative break: P(>={lo_tb.bin_info['temp']}C)={lo_tb.price:.1%} < "
                    f"P(>={hi_tb.bin_info['temp']}C)={hi_tb.price:.1%} "
                    f"violation={violation:.1%} — {lo_tb.market.question[:55]}"
                ))

    return opportunities


def _find_outlier_bin(bins_sorted: list[TempBin], direction: str) -> TempBin | None:
    """
    Find the bin that deviates most from its neighbors.
    direction="high" → find highest outlier; direction="low" → find lowest outlier.
    """
    if not bins_sorted:
        return None
    if len(bins_sorted) == 1:
        return bins_sorted[0]

    best_score = -1.0
    best_bin = None

    for i, tb in enumerate(bins_sorted):
        # Calculate expected value from neighbors
        neighbors = []
        if i > 0:
            neighbors.append(bins_sorted[i - 1].price)
        if i < len(bins_sorted) - 1:
            neighbors.append(bins_sorted[i + 1].price)
        avg_neighbor = sum(neighbors) / len(neighbors) if neighbors else tb.price

        if direction == "high":
            score = tb.price - avg_neighbor
        else:
            score = avg_neighbor - tb.price

        if score > best_score:
            best_score = score
            best_bin = tb

    return best_bin


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

    Conviction scales with the magnitude of the distribution violation.
    Threshold gates (YES_THRESHOLD / NO_THRESHOLD) still apply as hard limits.
    """
    ok, why = valid_market(market)
    if not ok:
        return None, 0, why

    if not opportunity:
        return None, 0, "No distribution violation found"

    _, side, violation_mag, reason = opportunity
    p = float(getattr(market, "current_probability", 0))

    if side == "yes":
        if p > YES_THRESHOLD:
            return None, 0, f"YES blocked at {p:.1%}; threshold is {YES_THRESHOLD:.0%}"
        conviction = (YES_THRESHOLD - p) / YES_THRESHOLD
        # Boost conviction by violation magnitude
        conviction = min(1.0, conviction + violation_mag)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        return "yes", size, reason

    if side == "no":
        if p < NO_THRESHOLD:
            return None, 0, f"NO blocked at {p:.1%}; threshold is {NO_THRESHOLD:.0%}"
        conviction = (p - NO_THRESHOLD) / (1 - NO_THRESHOLD)
        # Boost conviction by violation magnitude
        conviction = min(1.0, conviction + violation_mag)
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
    """Find active weather temperature markets, deduplicated."""
    seen, unique = set(), []
    for kw in KEYWORDS:
        try:
            for m in client.find_markets(query=kw):
                market_id = getattr(m, "id", None)
                if market_id and market_id not in seen:
                    q = getattr(m, "question", "").lower()
                    # Only keep temperature markets
                    if any(w in q for w in ("temperature", "temp", "°c", "degrees")):
                        if any(c in q for c in CITIES):
                            seen.add(market_id)
                            unique.append(m)
        except Exception as e:
            print(f"[search] {kw!r}: {e}")
    return unique


def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    print(f"[24h-weather-dist] mode={mode} max_pos=${MAX_POSITION} sum_tol={SUM_TOLERANCE:.0%}")

    client = get_client(live=live)
    markets = find_markets(client)
    print(f"[24h-weather-dist] {len(markets)} candidate markets")

    # Build temperature distributions
    distributions = build_distributions(markets)
    print(f"[24h-weather-dist] {len(distributions)} distributions: "
          f"{', '.join(f'{k}({len(v)} bins)' for k, v in distributions.items())}")

    # Log each distribution
    for dist_key, bins in distributions.items():
        exact = sorted(
            [tb for tb in bins if tb.bin_info["type"] == "exact"],
            key=lambda tb: tb.bin_info["temp"],
        )
        cumul = [tb for tb in bins if tb.bin_info["type"] in ("or_below", "or_higher")]
        if exact:
            total = sum(tb.price for tb in exact)
            print(f"  [{dist_key}] exact bins (sum={total:.1%}): " + ", ".join(
                f"{tb.bin_info['temp']}C={tb.price:.1%}" for tb in exact
            ))
        for tb in sorted(cumul, key=lambda t: t.bin_info["temp"]):
            print(f"  [{dist_key}] {tb.bin_info['type']}: "
                  f"{tb.bin_info['temp']}C={tb.price:.1%}")

    # Find violations across all distributions
    all_opps: dict[str, tuple] = {}
    for dist_key, bins in distributions.items():
        if len(bins) < 2:
            continue
        violations = find_violations(bins)
        for market, side, mag, reason in violations:
            mid = getattr(market, "id", None)
            if not mid:
                continue
            existing = all_opps.get(mid)
            if existing is None or mag > existing[2]:
                all_opps[mid] = (market, side, mag, reason)

    print(f"[24h-weather-dist] {len(all_opps)} violation opportunities")

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
            print(f"  [trade] {side.upper()} ${size} {tag} {status} — {reasoning[:110]}")
            if r.success:
                placed += 1
        except Exception as e:
            print(f"  [error] {market_id}: {e}")

    print(f"[24h-weather-dist] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Trades mispricings in weather temperature-bin distributions on Polymarket."
    )
    ap.add_argument(
        "--live",
        action="store_true",
        help="Real trades on Polymarket. Default is paper (sim) mode.",
    )
    run(live=ap.parse_args().live)
