"""
polymarket-48h-sports-line-curve-trader
Trades structural mispricings in sports O/U (over/under) markets on Polymarket
by reconstructing the implied probability curve across multiple line values
for the same game/match, then identifying monotonicity violations.

Core edge: Polymarket lists multiple O/U lines for a single game:
    O/U 5.5 = 50%, O/U 6.5 = 46%, O/U 7.5 = 29%
These MUST be monotonically decreasing (higher total = less likely for OVER).
When they are not, it is structural arbitrage.

Also detects tennis Set 1 O/U vs Match O/U inconsistencies:
    Match total >= Set 1 total always, so P(Match O/U X) >= P(Set 1 O/U X).

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

TRADE_SOURCE = "sdk:polymarket-48h-sports-line-curve-trader"
SKILL_SLUG   = "polymarket-48h-sports-line-curve-trader"

KEYWORDS = [
    "O/U", "over under", "total kills", "total goals",
    "games O/U", "total points", "total runs", "total sets",
    "over/under", "total rounds", "total maps",
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
        MIN_VIOLATION  = float(os.environ.get("SIMMER_MIN_VIOLATION",  str(MIN_VIOLATION)))
    return _client


# ---------------------------------------------------------------------------
# Market parsing -- extract game/match name, O/U line value, scope (set/match)
# ---------------------------------------------------------------------------

# Matches patterns like "O/U 5.5", "Over/Under 7.5", "over under 6.5",
# "total goals 3.5", "total kills 22.5", "games O/U 9.5"
_OU_LINE = re.compile(
    r"(?:O/U|over[/ ]under|total\s+(?:goals|kills|points|runs|rounds|maps|sets|games))"
    r"\s+([\d]+(?:\.[\d]+)?)",
    re.I,
)

# Detect tennis set-level markets: "Set 1 O/U 9.5", "1st set over under 8.5"
_SET_SCOPE = re.compile(
    r"(?:set\s*(\d)|(\d)(?:st|nd|rd|th)\s+set)",
    re.I,
)

# Extract the game/match identifier: teams or player names before the O/U part.
# We take everything before "O/U" / "over" / "total" as the game key.
_GAME_PREFIX = re.compile(
    r"^(.*?)(?:\s*[-|:]\s*)?(?:O/U|over[/ ]under|total\s+(?:goals|kills|points|runs|rounds|maps|sets|games))",
    re.I,
)

# Non-sport noise filters
_NON_SPORT = re.compile(
    r"bitcoin|ethereum|btc|eth|crypto|price|stock|token|coin|nft",
    re.I,
)


def parse_ou_line(question: str) -> float | None:
    """Extract the O/U line value from a market question."""
    m = _OU_LINE.search(question)
    if m:
        return float(m.group(1))
    return None


def parse_set_scope(question: str) -> str:
    """Return 'set1', 'set2', etc. or 'match' for match-level markets."""
    m = _SET_SCOPE.search(question)
    if m:
        set_num = m.group(1) or m.group(2)
        return f"set{set_num}"
    return "match"


def parse_game_key(question: str) -> str | None:
    """Extract a normalized game/match identifier from the question."""
    m = _GAME_PREFIX.search(question)
    if m:
        raw = m.group(1).strip()
        # Normalize: lowercase, collapse whitespace
        key = re.sub(r"\s+", " ", raw.lower()).strip(" -|:")
        if len(key) >= 3:
            return key
    return None


def is_sport_market(question: str) -> bool:
    """Return True if the question looks like a sports O/U market, not crypto/finance."""
    if _NON_SPORT.search(question):
        return False
    if _OU_LINE.search(question):
        return True
    return False


# ---------------------------------------------------------------------------
# Curve construction and violation detection
# ---------------------------------------------------------------------------

class CurvePoint:
    """One market mapped to a point on the implied O/U probability curve."""
    __slots__ = ("market", "game_key", "line", "scope", "price")

    def __init__(self, market, game_key: str, line: float, scope: str, price: float):
        self.market = market
        self.game_key = game_key
        self.line = line
        self.scope = scope
        self.price = price


def build_curves(markets: list) -> dict[str, list[CurvePoint]]:
    """
    Group markets into curves keyed by (game_key, scope).
    Each curve contains CurvePoints sorted by line value.
    """
    curves: dict[str, list[CurvePoint]] = {}
    for m in markets:
        q = getattr(m, "question", "")
        p = getattr(m, "current_probability", None)
        if not isinstance(p, (int, float)):
            continue

        if not is_sport_market(q):
            continue

        line = parse_ou_line(q)
        game_key = parse_game_key(q)
        if line is None or game_key is None:
            continue

        scope = parse_set_scope(q)
        key = f"{game_key}|{scope}"
        point = CurvePoint(m, game_key, line, scope, float(p))
        curves.setdefault(key, []).append(point)

    return curves


def find_violations(curves: dict[str, list[CurvePoint]]) -> list[tuple]:
    """
    Analyze curves for mathematical violations.
    Returns list of (market, side, violation_magnitude, reasoning).

    Checks:
    1. Monotonicity: within the same game+scope, P(O/U X OVER) must decrease
       as X increases (higher line = less likely to go over).
    2. Tennis consistency: for the same game, P(Match O/U X OVER) >= P(Set 1 O/U X OVER)
       because match total always >= set 1 total.
    """
    opportunities: list[tuple] = []

    # --- Check 1: Monotonicity within each curve ---
    for curve_key, points in curves.items():
        if len(points) < 2:
            continue

        # Sort by line value ascending
        sorted_pts = sorted(points, key=lambda pt: pt.line)

        for i in range(len(sorted_pts) - 1):
            lo_pt = sorted_pts[i]      # lower line (e.g. O/U 5.5)
            hi_pt = sorted_pts[i + 1]  # higher line (e.g. O/U 6.5)

            # OVER probability should be: lo_pt.price >= hi_pt.price
            # (easier to go over a lower total)
            # If hi_pt is priced HIGHER than lo_pt, monotonicity is broken
            violation = hi_pt.price - lo_pt.price
            if violation > MIN_VIOLATION:
                # Higher line is overpriced (sell NO = bet it won't go over)
                opportunities.append((
                    hi_pt.market, "no", violation,
                    f"Monotonicity break: P(O/U {hi_pt.line} OVER)={hi_pt.price:.1%} > "
                    f"P(O/U {lo_pt.line} OVER)={lo_pt.price:.1%} | "
                    f"violation={violation:.1%} -- {hi_pt.market.question[:55]}"
                ))
                # Lower line is underpriced (buy YES = bet it will go over)
                opportunities.append((
                    lo_pt.market, "yes", violation,
                    f"Monotonicity break: P(O/U {lo_pt.line} OVER)={lo_pt.price:.1%} < "
                    f"P(O/U {hi_pt.line} OVER)={hi_pt.price:.1%} | "
                    f"violation={violation:.1%} -- {lo_pt.market.question[:55]}"
                ))

    # --- Check 2: Tennis set vs match consistency ---
    # Group curves by game_key to find set-level vs match-level pairs
    game_groups: dict[str, dict[str, list[CurvePoint]]] = {}
    for curve_key, points in curves.items():
        if not points:
            continue
        game_key = points[0].game_key
        scope = points[0].scope
        game_groups.setdefault(game_key, {})[scope] = points

    for game_key, scopes in game_groups.items():
        match_pts = scopes.get("match")
        if not match_pts:
            continue

        # Build line->price lookup for match-level
        match_map: dict[float, CurvePoint] = {}
        for pt in match_pts:
            match_map[pt.line] = pt

        # Check each set-level curve
        for scope_name, set_pts in scopes.items():
            if not scope_name.startswith("set"):
                continue

            for set_pt in set_pts:
                match_pt = match_map.get(set_pt.line)
                if match_pt is None:
                    continue

                # Match total always >= set total, so P(Match O/U X OVER) >= P(Set O/U X OVER)
                # If set probability exceeds match probability, that is a violation
                violation = set_pt.price - match_pt.price
                if violation > MIN_VIOLATION:
                    # Set market is overpriced
                    opportunities.append((
                        set_pt.market, "no", violation,
                        f"Set>Match break: P({scope_name} O/U {set_pt.line})={set_pt.price:.1%} > "
                        f"P(Match O/U {match_pt.line})={match_pt.price:.1%} | "
                        f"violation={violation:.1%} -- {set_pt.market.question[:55]}"
                    ))
                    # Match market is underpriced
                    opportunities.append((
                        match_pt.market, "yes", violation,
                        f"Set>Match break: P(Match O/U {match_pt.line})={match_pt.price:.1%} < "
                        f"P({scope_name} O/U {set_pt.line})={set_pt.price:.1%} | "
                        f"violation={violation:.1%} -- {match_pt.market.question[:55]}"
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
            safe_print(f"  [warn] {w}")
    except Exception as e:
        safe_print(f"  [ctx] {market_id}: {e}")
    return True, "ok"


def find_markets(client: SimmerClient) -> list:
    """Find active sports O/U markets, deduplicated.
    Filters out non-sport markets (crypto, finance, etc.)."""
    seen: set[str] = set()
    unique: list = []
    for kw in KEYWORDS:
        try:
            for m in client.find_markets(query=kw):
                market_id = getattr(m, "id", None)
                if market_id and market_id not in seen:
                    q = getattr(m, "question", "")
                    if is_sport_market(q):
                        seen.add(market_id)
                        unique.append(m)
        except Exception as e:
            safe_print(f"[search] {kw!r}: {e}")
    return unique


def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    print(f"[48h-sports-line-curve] mode={mode} max_pos=${MAX_POSITION} min_violation={MIN_VIOLATION:.0%}")

    client = get_client(live=live)
    markets = find_markets(client)
    print(f"[48h-sports-line-curve] {len(markets)} candidate markets")

    # Build implied O/U probability curves
    curves = build_curves(markets)
    safe_print(f"[48h-sports-line-curve] {len(curves)} curves: "
               + ", ".join(f"{k}({len(v)} pts)" for k, v in curves.items()))

    # Log each curve's structure
    for curve_key, points in curves.items():
        sorted_pts = sorted(points, key=lambda pt: pt.line)
        safe_print(f"  [{curve_key}] lines: " + ", ".join(
            f"O/U {pt.line}={pt.price:.1%}" for pt in sorted_pts
        ))

    # Find violations across all curves
    all_opps: dict[str, tuple] = {}
    violations = find_violations(curves)
    for market, side, mag, reason in violations:
        mid = getattr(market, "id", None)
        if not mid:
            continue
        existing = all_opps.get(mid)
        if existing is None or mag > existing[2]:
            all_opps[mid] = (market, side, mag, reason)

    print(f"[48h-sports-line-curve] {len(all_opps)} violation opportunities")

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
            safe_print(f"  [trade] {side.upper()} ${size} {tag} {status} -- {reasoning[:110]}")
            if r.success:
                placed += 1
        except Exception as e:
            safe_print(f"  [error] {market_id}: {e}")

    print(f"[48h-sports-line-curve] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Trades structural mispricings in sports O/U line curves on Polymarket."
    )
    ap.add_argument(
        "--live",
        action="store_true",
        help="Real trades on Polymarket. Default is paper (sim) mode.",
    )
    run(live=ap.parse_args().live)
