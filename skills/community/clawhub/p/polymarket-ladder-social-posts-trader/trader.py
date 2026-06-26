"""
polymarket-ladder-social-posts-trader
Trades distribution-sum violations in social media post-count range markets
on Polymarket by reconstructing the implied probability distribution across
range bins for the same person and date range, then identifying sum violations
and individual bin anomalies.

Core edge: Polymarket lists multiple post-count range bins for the same person
and date range:
    "Will CZ post 140-159 posts from March 1 to April 1?" = 25%
    "Will CZ post 160-179 posts from March 1 to April 1?" = 30%
    "Will CZ post 180-199 posts from March 1 to April 1?" = 20%

These bins form a PROBABILITY DISTRIBUTION that must sum to ~100%.
When they don't, individual bins are mispriced. Additionally, individual bins
that are much higher or lower than their neighbors indicate local anomalies.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- live=True -> venue="polymarket" (real trades, only with --live flag).
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag.
"""
import os
import re
import sys
import argparse
from datetime import datetime, timezone
from collections import defaultdict
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-ladder-social-posts-trader"
SKILL_SLUG   = "polymarket-ladder-social-posts-trader"

KEYWORDS = [
    "posts", "CZ", "Khamenei", "tweets",
    "Truth Social", "social media", "X posts",
]

PERSONS = [
    "cz", "changpeng zhao", "binance cz",
    "khamenei", "ali khamenei", "ayatollah khamenei",
    "trump", "donald trump",
    "elon", "elon musk", "musk",
    "vitalik", "vitalik buterin",
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
MIN_VIOLATION  = float(os.environ.get("SIMMER_MIN_VIOLATION", "0.05"))

_client: SimmerClient | None = None


def safe_print(text):
    """Print with fallback for non-ASCII characters (Windows cp1252 terminals)."""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('ascii', 'replace').decode())


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
        MIN_VIOLATION  = float(os.environ.get("SIMMER_MIN_VIOLATION", str(MIN_VIOLATION)))
    return _client


# ---------------------------------------------------------------------------
# Market parsing -- extract person, range bounds, and date range
# ---------------------------------------------------------------------------

_PERSON_PATTERNS = {p: re.compile(re.escape(p), re.I) for p in PERSONS}

# Canonical name mapping
_PERSON_CANONICAL = {
    "cz": "cz", "changpeng zhao": "cz", "binance cz": "cz",
    "khamenei": "khamenei", "ali khamenei": "khamenei",
    "ayatollah khamenei": "khamenei",
    "trump": "trump", "donald trump": "trump",
    "elon": "musk", "elon musk": "musk", "musk": "musk",
    "vitalik": "vitalik", "vitalik buterin": "vitalik",
}

# Range pattern: "140-159 posts", "45-49 posts", "N-M posts/tweets"
_RANGE_PAT = re.compile(
    r"(\d+)\s*[-–]\s*(\d+)\s*(?:posts?|tweets?)", re.I
)

# Also match "fewer than N", "more than N", "N or more", "N or fewer"
_FEWER_THAN = re.compile(r"(?:fewer|less)\s+than\s+(\d+)\s*(?:posts?|tweets?)", re.I)
_MORE_THAN  = re.compile(r"(?:more|greater)\s+than\s+(\d+)\s*(?:posts?|tweets?)", re.I)
_N_OR_MORE  = re.compile(r"(\d+)\s+or\s+more\s*(?:posts?|tweets?)", re.I)
_N_OR_FEWER = re.compile(r"(\d+)\s+or\s+fewer\s*(?:posts?|tweets?)", re.I)

# Date range: "from March 1 to April 1" or "March 1 - April 1, 2026"
_DATE_RANGE_PAT = re.compile(
    r"(?:from\s+)?((?:January|February|March|April|May|June|July|August|"
    r"September|October|November|December)\s+\d{1,2}(?:,?\s*\d{4})?)"
    r"\s+(?:to|through|[-–])\s+"
    r"((?:January|February|March|April|May|June|July|August|"
    r"September|October|November|December)\s+\d{1,2}(?:,?\s*\d{4})?)",
    re.I,
)

# Single month pattern: "in March 2026"
_MONTH_PAT = re.compile(
    r"in\s+((?:January|February|March|April|May|June|July|August|"
    r"September|October|November|December)(?:\s+\d{4})?)", re.I,
)


def parse_person(question: str) -> str | None:
    q = question.lower()
    for person, pat in _PERSON_PATTERNS.items():
        if pat.search(q):
            return _PERSON_CANONICAL.get(person, person)
    return None


def parse_date_range_key(question: str) -> str | None:
    m = _DATE_RANGE_PAT.search(question)
    if m:
        return f"{m.group(1).strip().lower()} to {m.group(2).strip().lower()}"
    m = _MONTH_PAT.search(question)
    if m:
        return m.group(1).strip().lower()
    return None


def parse_post_range(question: str) -> dict | None:
    """
    Parse a post-count market question.
    Returns dict with keys: type ("range"|"fewer_than"|"more_than"), low (int), high (int|None).
    """
    m = _FEWER_THAN.search(question)
    if m:
        return {"type": "fewer_than", "low": 0, "high": int(m.group(1)) - 1}

    m = _N_OR_FEWER.search(question)
    if m:
        return {"type": "fewer_than", "low": 0, "high": int(m.group(1))}

    m = _MORE_THAN.search(question)
    if m:
        return {"type": "more_than", "low": int(m.group(1)) + 1, "high": None}

    m = _N_OR_MORE.search(question)
    if m:
        return {"type": "more_than", "low": int(m.group(1)), "high": None}

    m = _RANGE_PAT.search(question)
    if m:
        return {"type": "range", "low": int(m.group(1)), "high": int(m.group(2))}

    return None


# ---------------------------------------------------------------------------
# Distribution construction and violation detection
# ---------------------------------------------------------------------------

class PostBin:
    """One market mapped to a point in the post-count distribution."""
    __slots__ = ("market", "person", "date_key", "bin_info", "price")

    def __init__(self, market, person, date_key, bin_info, price):
        self.market = market
        self.person = person
        self.date_key = date_key
        self.bin_info = bin_info
        self.price = price


def build_distributions(markets: list) -> dict[str, list[PostBin]]:
    """
    Group markets into distributions keyed by (person, date_range).
    Each distribution contains PostBin entries.
    """
    distributions: dict[str, list[PostBin]] = {}
    for m in markets:
        q = getattr(m, "question", "")
        p = getattr(m, "current_probability", None)
        if not isinstance(p, (int, float)):
            continue

        person = parse_person(q)
        date_key = parse_date_range_key(q)
        bin_info = parse_post_range(q)
        if not person or not date_key or not bin_info:
            continue

        key = f"{person}|{date_key}"
        pb = PostBin(m, person, date_key, bin_info, float(p))
        distributions.setdefault(key, []).append(pb)

    return distributions


def find_violations(dist: list[PostBin]) -> list[tuple]:
    """
    Analyze a single (person, date_range) distribution for violations.
    Returns list of (market, side, violation_magnitude, reasoning).

    Checks:
    1. Sum check: all bins must sum to ~100% (+/- MIN_VIOLATION)
    2. Neighbor anomaly: any bin much higher/lower than its neighbors
    """
    opportunities = []

    # Sort bins by lower bound for consistent ordering
    bins_sorted = sorted(dist, key=lambda pb: pb.bin_info["low"])

    if len(bins_sorted) < 2:
        return opportunities

    total = sum(pb.price for pb in bins_sorted)
    deviation = total - 1.0  # positive = overpriced, negative = underpriced

    # --- Check 1: Sum violation ---
    if abs(deviation) > MIN_VIOLATION:
        if deviation > 0:
            # Sum too high -- sell NO on the highest-priced bins
            target = max(bins_sorted, key=lambda pb: pb.price)
            lo = target.bin_info["low"]
            hi = target.bin_info.get("high", "?")
            opportunities.append((
                target.market, "no", abs(deviation),
                f"Sum={total:.1%} (>105%): overpriced bin {lo}-{hi}="
                f"{target.price:.1%} person={target.person} "
                f"deviation={deviation:+.1%} -- {target.market.question[:55]}"
            ))
        else:
            # Sum too low -- buy YES on the lowest-priced bins
            target = min(bins_sorted, key=lambda pb: pb.price)
            lo = target.bin_info["low"]
            hi = target.bin_info.get("high", "?")
            opportunities.append((
                target.market, "yes", abs(deviation),
                f"Sum={total:.1%} (<95%): underpriced bin {lo}-{hi}="
                f"{target.price:.1%} person={target.person} "
                f"deviation={deviation:+.1%} -- {target.market.question[:55]}"
            ))

    # --- Check 2: Individual bin anomalies (neighbor comparison) ---
    for i, pb in enumerate(bins_sorted):
        neighbors = []
        if i > 0:
            neighbors.append(bins_sorted[i - 1].price)
        if i < len(bins_sorted) - 1:
            neighbors.append(bins_sorted[i + 1].price)
        if not neighbors:
            continue
        avg_neighbor = sum(neighbors) / len(neighbors)
        anomaly = pb.price - avg_neighbor

        lo = pb.bin_info["low"]
        hi = pb.bin_info.get("high", "?")

        # Bin much higher than neighbors -- overpriced
        if anomaly > MIN_VIOLATION * 2:
            mid = getattr(pb.market, "id", "")
            # Avoid duplicating if already caught by sum check
            already = any(getattr(o[0], "id", "") == mid for o in opportunities)
            if not already:
                opportunities.append((
                    pb.market, "no", anomaly,
                    f"Anomaly: bin {lo}-{hi}={pb.price:.1%} vs neighbors avg "
                    f"{avg_neighbor:.1%} (+{anomaly:.1%}) person={pb.person} "
                    f"-- {pb.market.question[:55]}"
                ))

        # Bin much lower than neighbors -- underpriced
        if anomaly < -MIN_VIOLATION * 2:
            mid = getattr(pb.market, "id", "")
            already = any(getattr(o[0], "id", "") == mid for o in opportunities)
            if not already:
                opportunities.append((
                    pb.market, "yes", abs(anomaly),
                    f"Anomaly: bin {lo}-{hi}={pb.price:.1%} vs neighbors avg "
                    f"{avg_neighbor:.1%} ({anomaly:.1%}) person={pb.person} "
                    f"-- {pb.market.question[:55]}"
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
            safe_print(f"  [warn] {w}")
    except Exception as e:
        safe_print(f"  [ctx] {market_id}: {e}")
    return True, "ok"


def discover_markets(client: SimmerClient) -> list:
    """Find active social-media post-count range markets, deduplicated."""
    seen, unique = set(), []

    # Strategy 1: keyword search
    for kw in KEYWORDS:
        try:
            for m in client.find_markets(query=kw):
                market_id = getattr(m, "id", None)
                if market_id and market_id not in seen:
                    q = getattr(m, "question", "").lower()
                    if any(w in q for w in ("post", "tweet", "truth social")):
                        if parse_post_range(getattr(m, "question", "")) is not None:
                            seen.add(market_id)
                            unique.append(m)
        except Exception as e:
            safe_print(f"[search] {kw!r}: {e}")

    # Strategy 2: broad get_markets fallback to catch markets find_markets may miss
    try:
        for m in client.get_markets(limit=200):
            market_id = getattr(m, "id", None)
            if market_id and market_id not in seen:
                q = getattr(m, "question", "").lower()
                if any(w in q for w in ("post", "tweet", "truth social")):
                    if parse_post_range(getattr(m, "question", "")) is not None:
                        seen.add(market_id)
                        unique.append(m)
    except Exception as e:
        safe_print(f"[get_markets fallback] {e}")

    return unique


def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    safe_print(f"[social-posts] mode={mode} max_pos=${MAX_POSITION} "
               f"min_violation={MIN_VIOLATION:.0%}")

    client = get_client(live=live)
    markets = discover_markets(client)
    safe_print(f"[social-posts] {len(markets)} candidate markets")

    # Build post-count distributions
    distributions = build_distributions(markets)
    safe_print(f"[social-posts] {len(distributions)} distributions: "
               + ", ".join(f"{k}({len(v)} bins)" for k, v in distributions.items()))

    # Log each distribution
    for dist_key, bins in distributions.items():
        bins_sorted = sorted(bins, key=lambda pb: pb.bin_info["low"])
        total = sum(pb.price for pb in bins_sorted)
        safe_print(f"  [{dist_key}] {len(bins_sorted)} bins (sum={total:.1%}): "
                   + ", ".join(
                       f"{pb.bin_info['low']}-{pb.bin_info.get('high', '?')}="
                       f"{pb.price:.1%}"
                       for pb in bins_sorted
                   ))

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

    safe_print(f"[social-posts] {len(all_opps)} violation opportunities")

    # Execute trades on best violations
    placed = 0
    for market_id, opp in sorted(all_opps.items(), key=lambda x: -x[1][2]):
        if placed >= MAX_POSITIONS:
            break

        market = opp[0]
        side, size, reasoning = compute_signal(market, opp)
        if not side:
            safe_print(f"  [skip] {reasoning}")
            continue

        ok, why = context_ok(client, market_id)
        if not ok:
            safe_print(f"  [skip] {why}")
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
            safe_print(f"  [trade] {side.upper()} ${size} {tag} {status} "
                       f"-- {reasoning[:110]}")
            if r.success:
                placed += 1
        except Exception as e:
            safe_print(f"  [error] {market_id}: {e}")

    safe_print(f"[social-posts] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Trades distribution-sum violations in social media "
                    "post-count range markets on Polymarket."
    )
    ap.add_argument(
        "--live",
        action="store_true",
        help="Real trades on Polymarket. Default is paper (sim) mode.",
    )
    run(live=ap.parse_args().live)
