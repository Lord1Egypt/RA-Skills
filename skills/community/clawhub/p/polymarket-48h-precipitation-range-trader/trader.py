"""
polymarket-48h-precipitation-range-trader
Trades mispricings in precipitation-range markets on Polymarket
by reconstructing the implied probability distribution across bins
for the same city and period, then identifying sum violations and
monotonicity breaks on cumulative ("more than X inches") markets.

Core edge: Polymarket lists multiple precipitation range bins for the
same city and period:
    "Will Seattle have more than 5 inches of precipitation in April?" = 18.8%
    "Will Seattle have between 4.5 and 5 inches in April?" = 17.5%
    "Will Seattle have between 4 and 4.5 inches in April?" = 29%

These range bins form a PROBABILITY DISTRIBUTION that must sum to ~100%.
When they don't, individual bins are mispriced. Additionally, cumulative
markets ("more than X inches") must be monotonically decreasing as X
increases.

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

TRADE_SOURCE = "sdk:polymarket-48h-precipitation-range-trader"
SKILL_SLUG   = "polymarket-48h-precipitation-range-trader"

KEYWORDS = [
    "precipitation", "Seattle", "inches",
    "rainfall", "rain", "snow",
]

CITIES = [
    "seattle", "portland", "san francisco", "los angeles", "la",
    "denver", "chicago", "nyc", "new york", "miami", "dallas",
    "austin", "houston", "boston", "atlanta", "munich", "london",
    "tokyo", "seoul",
]

PERIODS = [
    "january", "february", "march", "april", "may", "june",
    "july", "august", "september", "october", "november", "december",
]

# Risk parameters — declared as tunables in clawhub.json, adjustable from Simmer UI.
MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  "35"))
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
# Market parsing — extract city, metric, range, and period
# ---------------------------------------------------------------------------

_CITY_PATTERNS = {c: re.compile(re.escape(c), re.I) for c in CITIES}

# "between X and Y inches"
_BETWEEN_RANGE = re.compile(
    r"between\s+([\d.]+)\s+and\s+([\d.]+)\s+inch", re.I
)

# "more than X inches" / "over X inches" / "above X inches"
_MORE_THAN = re.compile(
    r"(?:more\s+than|over|above|greater\s+than)\s+([\d.]+)\s+inch", re.I
)

# "less than X inches" / "under X inches" / "below X inches"
_LESS_THAN = re.compile(
    r"(?:less\s+than|under|below|fewer\s+than)\s+([\d.]+)\s+inch", re.I
)

# Period patterns: month names
_PERIOD_PATTERN = re.compile(
    r"(January|February|March|April|May|June|July|August|"
    r"September|October|November|December)(?:\s+\d{4})?",
    re.I,
)


def parse_city(question: str) -> str | None:
    q = question.lower()
    for city, pat in _CITY_PATTERNS.items():
        if pat.search(q):
            if city in ("la", "los angeles"):
                return "los angeles"
            if city in ("nyc", "new york"):
                return "new york"
            return city
    return None


def parse_period(question: str) -> str | None:
    m = _PERIOD_PATTERN.search(question)
    if m:
        return m.group(1).strip().lower()
    return None


def parse_precip_bin(question: str) -> dict | None:
    """
    Parse a precipitation range market question.
    Returns dict with keys:
        type: "between" | "more_than" | "less_than"
        lo: float (lower bound, for between)
        hi: float (upper bound, for between)
        threshold: float (for more_than / less_than)
    """
    m = _BETWEEN_RANGE.search(question)
    if m:
        lo, hi = float(m.group(1)), float(m.group(2))
        return {"type": "between", "lo": lo, "hi": hi}

    m = _MORE_THAN.search(question)
    if m:
        return {"type": "more_than", "threshold": float(m.group(1))}

    m = _LESS_THAN.search(question)
    if m:
        return {"type": "less_than", "threshold": float(m.group(1))}

    return None


# ---------------------------------------------------------------------------
# Distribution construction and violation detection
# ---------------------------------------------------------------------------

class PrecipBin:
    """One market mapped to a point in the precipitation distribution."""
    __slots__ = ("market", "city", "period", "bin_info", "price")

    def __init__(self, market, city, period, bin_info, price):
        self.market = market
        self.city = city
        self.period = period
        self.bin_info = bin_info
        self.price = price


def build_distributions(markets: list) -> dict[str, list[PrecipBin]]:
    """
    Group markets into distributions keyed by (city, period).
    Each distribution contains PrecipBin entries.
    """
    distributions: dict[str, list[PrecipBin]] = {}
    for m in markets:
        q = getattr(m, "question", "")
        p = getattr(m, "current_probability", None)
        if not isinstance(p, (int, float)):
            continue

        city = parse_city(q)
        period = parse_period(q)
        bin_info = parse_precip_bin(q)
        if not city or not period or not bin_info:
            continue

        key = f"{city}|{period}"
        pb = PrecipBin(m, city, period, bin_info, float(p))
        distributions.setdefault(key, []).append(pb)

    return distributions


def find_violations(dist: list[PrecipBin]) -> list[tuple]:
    """
    Analyze a single (city, period) distribution for violations.
    Returns list of (market, side, violation_magnitude, reasoning).

    Checks:
    1. Sum check: all bins (between + more_than covering the top) must sum to ~100%
    2. Monotonicity: "more than X" must decrease as X increases
    3. Most mispriced bin identification when sum deviates
    """
    opportunities = []

    between_bins = [pb for pb in dist if pb.bin_info["type"] == "between"]
    more_than_bins = [pb for pb in dist if pb.bin_info["type"] == "more_than"]
    less_than_bins = [pb for pb in dist if pb.bin_info["type"] == "less_than"]

    # --- Check 1: Bin sum (between bins + the single top cumulative) ---
    # All between-range bins plus the "more than" top bin should sum to ~100%
    # because they partition the outcome space.
    all_range_bins = between_bins[:]
    # If there's a "more than" that covers the top of the range, include it
    if more_than_bins and between_bins:
        between_sorted = sorted(between_bins, key=lambda pb: pb.bin_info["hi"])
        more_sorted = sorted(more_than_bins, key=lambda pb: pb.bin_info["threshold"])
        # The highest "more than" threshold that matches the top "between" hi
        top_more = more_sorted[-1]  # highest threshold
        all_range_bins.append(top_more)

    if len(all_range_bins) >= 2:
        total = sum(pb.price for pb in all_range_bins)
        deviation = total - 1.0

        if abs(deviation) > SUM_TOLERANCE:
            if deviation > 0:
                # Sum too high -- sell the most overpriced bin
                target = _find_outlier_bin(all_range_bins, direction="high")
                if target:
                    opportunities.append((
                        target.market, "no", abs(deviation),
                        f"Sum={total:.1%} (>{1+SUM_TOLERANCE:.0%}): "
                        f"overpriced bin {_bin_label(target)}={target.price:.1%} "
                        f"deviation={deviation:+.1%} — {target.market.question[:55]}"
                    ))
            else:
                # Sum too low -- buy the most underpriced bin
                target = _find_outlier_bin(all_range_bins, direction="low")
                if target:
                    opportunities.append((
                        target.market, "yes", abs(deviation),
                        f"Sum={total:.1%} (<{1-SUM_TOLERANCE:.0%}): "
                        f"underpriced bin {_bin_label(target)}={target.price:.1%} "
                        f"deviation={deviation:+.1%} — {target.market.question[:55]}"
                    ))

    # --- Check 2: Monotonicity on "more than X" cumulative bins ---
    # P(more than X) must decrease as X increases
    if len(more_than_bins) >= 2:
        more_sorted = sorted(more_than_bins, key=lambda pb: pb.bin_info["threshold"])
        for i in range(len(more_sorted) - 1):
            lo_pb = more_sorted[i]      # lower threshold
            hi_pb = more_sorted[i + 1]  # higher threshold
            # P(more than lo) >= P(more than hi) must hold
            violation = hi_pb.price - lo_pb.price  # positive = monotonicity break
            if violation > SUM_TOLERANCE:
                opportunities.append((
                    hi_pb.market, "no", violation,
                    f"Cumulative break: P(>{hi_pb.bin_info['threshold']}in)="
                    f"{hi_pb.price:.1%} > P(>{lo_pb.bin_info['threshold']}in)="
                    f"{lo_pb.price:.1%} violation={violation:.1%} "
                    f"— {hi_pb.market.question[:55]}"
                ))
                opportunities.append((
                    lo_pb.market, "yes", violation,
                    f"Cumulative break: P(>{lo_pb.bin_info['threshold']}in)="
                    f"{lo_pb.price:.1%} < P(>{hi_pb.bin_info['threshold']}in)="
                    f"{hi_pb.price:.1%} violation={violation:.1%} "
                    f"— {lo_pb.market.question[:55]}"
                ))

    # --- Check 3: Monotonicity on "less than X" cumulative bins ---
    # P(less than X) must increase as X increases
    if len(less_than_bins) >= 2:
        less_sorted = sorted(less_than_bins, key=lambda pb: pb.bin_info["threshold"])
        for i in range(len(less_sorted) - 1):
            lo_pb = less_sorted[i]
            hi_pb = less_sorted[i + 1]
            # P(less than lo) <= P(less than hi) must hold
            violation = lo_pb.price - hi_pb.price  # positive = monotonicity break
            if violation > SUM_TOLERANCE:
                opportunities.append((
                    lo_pb.market, "no", violation,
                    f"Cumulative break: P(<{lo_pb.bin_info['threshold']}in)="
                    f"{lo_pb.price:.1%} > P(<{hi_pb.bin_info['threshold']}in)="
                    f"{hi_pb.price:.1%} violation={violation:.1%} "
                    f"— {lo_pb.market.question[:55]}"
                ))
                opportunities.append((
                    hi_pb.market, "yes", violation,
                    f"Cumulative break: P(<{hi_pb.bin_info['threshold']}in)="
                    f"{hi_pb.price:.1%} < P(<{lo_pb.bin_info['threshold']}in)="
                    f"{lo_pb.price:.1%} violation={violation:.1%} "
                    f"— {hi_pb.market.question[:55]}"
                ))

    return opportunities


def _bin_label(pb: PrecipBin) -> str:
    """Human-readable label for a precipitation bin."""
    info = pb.bin_info
    if info["type"] == "between":
        return f"{info['lo']}-{info['hi']}in"
    if info["type"] == "more_than":
        return f">{info['threshold']}in"
    if info["type"] == "less_than":
        return f"<{info['threshold']}in"
    return "unknown"


def _find_outlier_bin(bins: list[PrecipBin], direction: str) -> PrecipBin | None:
    """
    Find the bin that deviates most from its neighbors.
    direction="high" -> find highest outlier; direction="low" -> find lowest outlier.
    """
    if not bins:
        return None
    if len(bins) == 1:
        return bins[0]

    # Sort by a comparable key for neighbor analysis
    def sort_key(pb):
        info = pb.bin_info
        if info["type"] == "between":
            return info["lo"]
        if info["type"] == "more_than":
            return info["threshold"] + 1000  # sort after between bins
        if info["type"] == "less_than":
            return info["threshold"] - 1000  # sort before between bins
        return 0

    sorted_bins = sorted(bins, key=sort_key)

    best_score = -1.0
    best_bin = None

    for i, pb in enumerate(sorted_bins):
        neighbors = []
        if i > 0:
            neighbors.append(sorted_bins[i - 1].price)
        if i < len(sorted_bins) - 1:
            neighbors.append(sorted_bins[i + 1].price)
        avg_neighbor = sum(neighbors) / len(neighbors) if neighbors else pb.price

        if direction == "high":
            score = pb.price - avg_neighbor
        else:
            score = avg_neighbor - pb.price

        if score > best_score:
            best_score = score
            best_bin = pb

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
    """Find active precipitation range markets, deduplicated."""
    seen, unique = set(), []
    for kw in KEYWORDS:
        try:
            for m in client.find_markets(query=kw):
                market_id = getattr(m, "id", None)
                if market_id and market_id not in seen:
                    q = getattr(m, "question", "").lower()
                    # Only keep precipitation / rainfall / inches markets
                    if any(w in q for w in ("precipitation", "rainfall", "inches", "inch")):
                        seen.add(market_id)
                        unique.append(m)
        except Exception as e:
            print(f"[search] {kw!r}: {e}")
    return unique


def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    print(f"[48h-precip-range] mode={mode} max_pos=${MAX_POSITION} sum_tol={SUM_TOLERANCE:.0%}")

    client = get_client(live=live)
    markets = find_markets(client)
    print(f"[48h-precip-range] {len(markets)} candidate markets")

    # Build precipitation distributions
    distributions = build_distributions(markets)
    print(f"[48h-precip-range] {len(distributions)} distributions: "
          + ", ".join(f"{k}({len(v)} bins)" for k, v in distributions.items()))

    # Log each distribution
    for dist_key, bins in distributions.items():
        between = sorted(
            [pb for pb in bins if pb.bin_info["type"] == "between"],
            key=lambda pb: pb.bin_info["lo"],
        )
        cumul = [pb for pb in bins if pb.bin_info["type"] in ("more_than", "less_than")]
        if between:
            total = sum(pb.price for pb in between)
            print(f"  [{dist_key}] range bins (sum={total:.1%}): " + ", ".join(
                f"{pb.bin_info['lo']}-{pb.bin_info['hi']}in={pb.price:.1%}"
                for pb in between
            ))
        for pb in sorted(cumul, key=lambda p: p.bin_info.get("threshold", 0)):
            print(f"  [{dist_key}] {pb.bin_info['type']}: "
                  f"{pb.bin_info['threshold']}in={pb.price:.1%}")

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

    print(f"[48h-precip-range] {len(all_opps)} violation opportunities")

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

    print(f"[48h-precip-range] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Trades mispricings in precipitation-range distributions on Polymarket."
    )
    ap.add_argument(
        "--live",
        action="store_true",
        help="Real trades on Polymarket. Default is paper (sim) mode.",
    )
    run(live=ap.parse_args().live)
