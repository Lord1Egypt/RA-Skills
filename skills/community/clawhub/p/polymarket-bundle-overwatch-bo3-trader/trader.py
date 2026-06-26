"""
polymarket-bundle-overwatch-bo3-trader
Trades structural arbitrage between Overwatch BO3 series winner markets and
individual game winner markets on Polymarket. P(BO3 winner) must be consistent
with P(Game 1 winner) and P(Game 2 winner) probabilities -- when it is not,
the inconsistency is a free edge.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag (venue="polymarket").
"""
import os
import re
import argparse
from datetime import datetime, timezone
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-bundle-overwatch-bo3-trader"
SKILL_SLUG   = "polymarket-bundle-overwatch-bo3-trader"

KEYWORDS = [
    'Overwatch', 'OCS', 'OWL', 'Game 1 Winner',
    'Game 2 Winner', 'BO3', 'Virtus.pro', 'Team Peps',
]

# Risk parameters -- declared as tunables in clawhub.json, adjustable from Simmer UI.
MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  "40"))
MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    "3000"))
MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.08"))
MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      "1"))
MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "10"))
YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.38"))
NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",  "0.62"))
MIN_TRADE      = float(os.environ.get("SIMMER_MIN_TRADE",     "5"))
MIN_VIOLATION  = float(os.environ.get("SIMMER_MIN_VIOLATION",  "0.05"))

_client: SimmerClient | None = None


def safe_print(text):
    """Print with fallback for non-ASCII characters (Windows cp1252 terminals)."""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('ascii', 'replace').decode())


def get_client(live: bool = False) -> SimmerClient:
    """
    live=False -> venue="sim"  (paper trades -- safe default).
    live=True  -> venue="polymarket" (real trades, only with --live flag).
    """
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
        # Re-read params in case apply_skill_config updated os.environ.
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
# Parsing Overwatch market questions
# ---------------------------------------------------------------------------

# "Overwatch: Team A vs Team B - Game N Winner"
_GAME_RE = re.compile(
    r"Overwatch[:\s]+(.+?)\s+vs\.?\s+(.+?)\s*[-\u2013]\s*Game\s+(\d+)\s+Winner",
    re.IGNORECASE,
)

# "Overwatch: Team A vs Team B (BO3) - Tournament"
_BO3_RE = re.compile(
    r"Overwatch[:\s]+(.+?)\s+vs\.?\s+(.+?)\s*\(BO3\)",
    re.IGNORECASE,
)


def _norm_team(name: str) -> str:
    """Normalise team name for grouping."""
    return name.strip().lower()


def _match_key(team_a: str, team_b: str) -> str:
    """Canonical match key: sorted team pair."""
    a, b = _norm_team(team_a), _norm_team(team_b)
    return "|".join(sorted([a, b]))


def parse_market(question: str):
    """
    Returns one of:
      ("game", match_key, game_number, team_a_norm, team_b_norm)
      ("bo3",  match_key, None,        team_a_norm, team_b_norm)
      None
    """
    gm = _GAME_RE.search(question)
    if gm:
        ta, tb, gnum = gm.groups()
        return "game", _match_key(ta, tb), int(gnum), _norm_team(ta), _norm_team(tb)

    bm = _BO3_RE.search(question)
    if bm:
        ta, tb = bm.groups()
        return "bo3", _match_key(ta, tb), None, _norm_team(ta), _norm_team(tb)

    return None


# ---------------------------------------------------------------------------
# Implied BO3 calculation
# ---------------------------------------------------------------------------

def implied_bo3(p1: float, p2: float, p3: float | None = None) -> float:
    """
    Compute implied P(Team wins BO3) from individual game win probabilities.

    Team wins BO3 if they win 2 of 3 games:
    - Win G1 AND Win G2 (series over in 2)
    - Win G1, Lose G2, Win G3
    - Lose G1, Win G2, Win G3

    If p3 (Game 3 winner probability) is not available, assume 0.5 (coin flip).
    """
    if p3 is None:
        p3 = 0.5

    # P(win BO3) = p1*p2 + p1*(1-p2)*p3 + (1-p1)*p2*p3
    return p1 * p2 + p1 * (1 - p2) * p3 + (1 - p1) * p2 * p3


# ---------------------------------------------------------------------------
# Signal
# ---------------------------------------------------------------------------

def compute_signal(market, violation: float, implied: float, actual: float) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    Conviction-based sizing per CLAUDE.md.
    - If implied > actual + MIN_VIOLATION: BO3 market underprices team -> buy YES
    - If implied < actual - MIN_VIOLATION: BO3 market overprices team -> sell NO
    """
    p = market.current_probability
    q = getattr(market, "question", "")

    # Spread gate
    if market.spread_cents is not None and market.spread_cents / 100 > MAX_SPREAD:
        return None, 0, f"Spread {market.spread_cents/100:.1%} > {MAX_SPREAD:.1%}"

    # Days-to-resolution gate
    if market.resolves_at:
        try:
            resolves = datetime.fromisoformat(market.resolves_at.replace("Z", "+00:00"))
            days = (resolves - datetime.now(timezone.utc)).days
            if days < MIN_DAYS:
                return None, 0, f"Only {days} days to resolve"
        except Exception:
            pass

    # BO3 underpriced: implied > actual -> buy YES if p <= YES_THRESHOLD
    if violation > 0 and p <= YES_THRESHOLD:
        conviction = (YES_THRESHOLD - p) / YES_THRESHOLD
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = YES_THRESHOLD - p
        return "yes", size, (
            f"YES {p:.0%} edge={edge:.0%} implied={implied:.0%} actual={actual:.0%} "
            f"violation={violation:+.0%} size=${size} -- {q[:50]}"
        )

    # BO3 overpriced: implied < actual -> sell NO if p >= NO_THRESHOLD
    if violation < 0 and p >= NO_THRESHOLD:
        conviction = (p - NO_THRESHOLD) / (1 - NO_THRESHOLD)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = p - NO_THRESHOLD
        return "no", size, (
            f"NO YES={p:.0%} edge={edge:.0%} implied={implied:.0%} actual={actual:.0%} "
            f"violation={violation:+.0%} size=${size} -- {q[:50]}"
        )

    return None, 0, (
        f"Violation={violation:+.1%} but p={p:.0%} outside threshold bands -- {q[:60]}"
    )


# ---------------------------------------------------------------------------
# Market discovery
# ---------------------------------------------------------------------------

def find_markets(client: SimmerClient) -> list:
    """Find active Overwatch markets via keyword search + get_markets fallback."""
    seen, unique = set(), []

    # 1. Keyword search
    for kw in KEYWORDS:
        try:
            for m in client.find_markets(query=kw):
                if m.id not in seen:
                    seen.add(m.id)
                    unique.append(m)
        except Exception as e:
            safe_print(f"[search] {kw!r}: {e}")

    # 2. Fallback: scan broad market list for Overwatch matches
    try:
        for m in client.get_markets(limit=200):
            mid = getattr(m, "id", None)
            q = getattr(m, "question", "")
            if mid and mid not in seen and "overwatch" in q.lower():
                seen.add(mid)
                unique.append(m)
    except Exception as e:
        safe_print(f"[fallback] get_markets: {e}")

    return unique


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


# ---------------------------------------------------------------------------
# Grouping and arbitrage detection
# ---------------------------------------------------------------------------

def find_arbitrage_opportunities(markets: list) -> list:
    """
    Group Overwatch markets by match. For each match with a BO3 market and
    at least Game 1 + Game 2 winner markets, compute implied BO3 probability
    and compare to actual. Return tradeable opportunities.
    """
    # Group: match_key -> {"bo3": market, "games": {1: market, 2: market, 3: market}}
    matches: dict[str, dict] = {}

    for m in markets:
        q = getattr(m, "question", "")
        parsed = parse_market(q)
        if not parsed:
            continue

        mtype, mkey, gnum, ta, tb = parsed
        if mkey not in matches:
            matches[mkey] = {"bo3": None, "games": {}, "teams": (ta, tb)}

        if mtype == "bo3":
            matches[mkey]["bo3"] = m
        elif mtype == "game" and gnum is not None:
            matches[mkey]["games"][gnum] = m

    opportunities = []

    for mkey, data in matches.items():
        bo3_market = data["bo3"]
        games = data["games"]
        teams = data["teams"]

        if bo3_market is None:
            continue
        if 1 not in games or 2 not in games:
            continue

        # Get probabilities (probability is for first team listed in question)
        # We need to figure out which team the BO3 market references.
        # For simplicity, use the BO3 market probability as P(team_a wins BO3)
        # and game probabilities as P(team_a wins Game N).
        # The team ordering in parsed questions is normalised, so probabilities
        # should be consistently for the same team.
        bo3_q = getattr(bo3_market, "question", "").lower()
        bo3_parsed = parse_market(getattr(bo3_market, "question", ""))
        if not bo3_parsed:
            continue
        _, _, _, bo3_ta, bo3_tb = bo3_parsed

        # BO3 market probability = P(bo3_ta wins BO3)
        actual_bo3 = bo3_market.current_probability

        # Game probabilities -- we need to align team direction
        p1_market = games[1]
        p1_parsed = parse_market(getattr(p1_market, "question", ""))
        if not p1_parsed:
            continue
        _, _, _, g1_ta, g1_tb = p1_parsed

        p2_market = games[2]
        p2_parsed = parse_market(getattr(p2_market, "question", ""))
        if not p2_parsed:
            continue
        _, _, _, g2_ta, g2_tb = p2_parsed

        # Get raw probabilities
        p1 = p1_market.current_probability
        p2 = p2_market.current_probability

        # Align: if game market has teams in different order than BO3 market,
        # flip the probability. We compare the first team in each parsed result.
        if g1_ta != bo3_ta:
            p1 = 1 - p1
        if g2_ta != bo3_ta:
            p2 = 1 - p2

        # Game 3 if available
        p3 = None
        if 3 in games:
            p3_market = games[3]
            p3_parsed = parse_market(getattr(p3_market, "question", ""))
            if p3_parsed:
                _, _, _, g3_ta, g3_tb = p3_parsed
                p3 = p3_market.current_probability
                if g3_ta != bo3_ta:
                    p3 = 1 - p3

        implied = implied_bo3(p1, p2, p3)
        violation = implied - actual_bo3

        if abs(violation) >= MIN_VIOLATION:
            safe_print(
                f"[arb] {teams[0]} vs {teams[1]}: "
                f"p1={p1:.0%} p2={p2:.0%} p3={'N/A' if p3 is None else f'{p3:.0%}'} "
                f"implied={implied:.0%} actual={actual_bo3:.0%} "
                f"violation={violation:+.1%}"
            )
            opportunities.append((bo3_market, violation, implied, actual_bo3))

    return opportunities


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    safe_print(
        f"[overwatch-bo3] mode={mode} max_pos=${MAX_POSITION} "
        f"min_violation={MIN_VIOLATION:.0%} yes_thresh={YES_THRESHOLD} "
        f"no_thresh={NO_THRESHOLD}"
    )

    client  = get_client(live=live)
    markets = find_markets(client)
    safe_print(f"[overwatch-bo3] {len(markets)} candidate Overwatch markets")

    opportunities = find_arbitrage_opportunities(markets)
    safe_print(f"[overwatch-bo3] {len(opportunities)} arbitrage opportunities")

    placed = 0
    for bo3_market, violation, implied, actual in opportunities:
        if placed >= MAX_POSITIONS:
            break

        side, size, reasoning = compute_signal(bo3_market, violation, implied, actual)
        if not side:
            safe_print(f"  [skip] {reasoning}")
            continue

        ok, why = context_ok(client, bo3_market.id)
        if not ok:
            safe_print(f"  [skip] {why}")
            continue

        try:
            r = client.trade(
                market_id=bo3_market.id,
                side=side,
                amount=size,
                source=TRADE_SOURCE,
                skill_slug=SKILL_SLUG,
                reasoning=reasoning,
            )
            tag    = "(sim)" if r.simulated else "(live)"
            status = "OK" if r.success else f"FAIL:{r.error}"
            safe_print(f"  [trade] {side.upper()} ${size} {tag} {status} -- {reasoning[:70]}")
            if r.success:
                placed += 1
        except Exception as e:
            safe_print(f"  [error] {bo3_market.id}: {e}")

    safe_print(f"[overwatch-bo3] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Trades structural arbitrage between Overwatch BO3 and individual game winner markets."
    )
    ap.add_argument("--live", action="store_true",
                    help="Real trades on Polymarket. Default is paper (sim) mode.")
    run(live=ap.parse_args().live)
