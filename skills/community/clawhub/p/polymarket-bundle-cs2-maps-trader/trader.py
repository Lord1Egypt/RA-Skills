"""
polymarket-bundle-cs2-maps-trader
Trades CS2 BO3 Winner markets when individual map probabilities imply a
different BO3 outcome on Polymarket.

Core edge: CS2 Map 1 Winner + Map 2 Winner constrain BO3 Winner. P(BO3 win)
should approximately equal P(win Map1)*P(win Map2) + P(win Map1)*P(lose Map2)
*P(win Map3) + P(lose Map1)*P(win Map2)*P(win Map3). When P(BO3 winner) is
inconsistent with individual map probabilities, the BO3 market is mispriced.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- live=True -> venue="polymarket" (real trades, only with --live flag).
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag.
"""
import os
import re
import argparse
from datetime import datetime, timezone
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-bundle-cs2-maps-trader"
SKILL_SLUG   = "polymarket-bundle-cs2-maps-trader"

KEYWORDS = [
    'Counter-Strike', 'CS2', 'Map 1', 'Map 2', 'Map 3', 'BO3', 'BO1',
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
# Minimum difference between implied and actual BO3 probability to trade
MIN_VIOLATION  = float(os.environ.get("SIMMER_MIN_VIOLATION",  "0.05"))

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
# Market parsing — extract match_key, map_number, team
# ---------------------------------------------------------------------------

# Matches "Counter-Strike: Team A vs Team B - Map 1 Winner"
_MAP_WINNER = re.compile(
    r"counter[\s-]?strike[^:]*:\s*(.+?)\s+vs\.?\s+(.+?)\s*[-\u2013]\s*map\s+(\d+)\s+winner",
    re.I,
)

# Matches "Counter-Strike: Team A vs Team B (BO3) - Tournament"
# or "CS2: Team A vs Team B - BO3 Winner"
_BO3_WINNER = re.compile(
    r"(?:counter[\s-]?strike|cs2)[^:]*:\s*(.+?)\s+vs\.?\s+(.+?)\s*"
    r"(?:[-\u2013]\s*(?:BO3|best\s+of\s+3)\s*(?:winner|match\s+winner)?|"
    r"\(BO3\)\s*[-\u2013])",
    re.I,
)

# Broader BO3 match: captures "Team A vs Team B" with BO3 in question
_BO3_BROAD = re.compile(
    r"(?:counter[\s-]?strike|cs2).*?([\w\s.']+?)\s+vs\.?\s+([\w\s.']+?).*?(?:BO3|best\s+of\s+3)",
    re.I,
)

# CS2 indicator
_CS2_INDICATOR = re.compile(
    r"counter[\s-]?strike|cs2|csgo|hltv|blast|esl|iem|major|challengers|legends",
    re.I,
)

# Non-CS2 noise
_NON_CS2 = re.compile(
    r"bitcoin|ethereum|btc|eth|crypto|price|stock|token|coin|nft|"
    r"election|president|congress|senate|weather|temperature|"
    r"dota|overwatch|valorant|league\s+of\s+legends",
    re.I,
)


def normalize_team(raw: str) -> str:
    """Normalize team name for matching."""
    return re.sub(r"\s+", " ", raw.lower().strip(" -|:,.'"))


def normalize_match_key(team_a: str, team_b: str) -> str:
    """Create a canonical match key from two team names (sorted)."""
    a = normalize_team(team_a)
    b = normalize_team(team_b)
    return "|".join(sorted([a, b]))


def parse_map_market(question: str):
    """
    Parse a CS2 map winner market.
    Returns (match_key, map_number, team_a, team_b) or None.
    """
    if _NON_CS2.search(question):
        return None
    m = _MAP_WINNER.search(question)
    if m:
        team_a = m.group(1).strip()
        team_b = m.group(2).strip()
        map_num = int(m.group(3))
        match_key = normalize_match_key(team_a, team_b)
        return (match_key, map_num, team_a, team_b)
    return None


def parse_bo3_market(question: str):
    """
    Parse a CS2 BO3 winner market.
    Returns (match_key, team_a, team_b) or None.
    """
    if _NON_CS2.search(question):
        return None

    m = _BO3_WINNER.search(question)
    if m:
        team_a = m.group(1).strip()
        team_b = m.group(2).strip()
        match_key = normalize_match_key(team_a, team_b)
        return (match_key, team_a, team_b)

    m = _BO3_BROAD.search(question)
    if m:
        team_a = m.group(1).strip()
        team_b = m.group(2).strip()
        match_key = normalize_match_key(team_a, team_b)
        return (match_key, team_a, team_b)

    return None


def is_cs2_market(question: str) -> bool:
    """Return True if the question looks like a CS2 match market."""
    if _NON_CS2.search(question):
        return False
    return bool(_CS2_INDICATOR.search(question))


# ---------------------------------------------------------------------------
# Bundle construction and BO3 probability model
# ---------------------------------------------------------------------------

class MatchBundle:
    """Groups a BO3 winner market with its individual map winner markets."""
    __slots__ = ("match_key", "team_a", "team_b", "bo3_market", "map_markets")

    def __init__(self, match_key: str, team_a: str, team_b: str):
        self.match_key = match_key
        self.team_a = team_a
        self.team_b = team_b
        self.bo3_market = None          # The BO3 winner market
        self.map_markets: dict = {}     # map_number -> market


def implied_bo3_probability(p1: float, p2: float, p3: float = 0.5) -> float:
    """
    Calculate implied BO3 win probability for team A from individual map
    win probabilities.

    P(BO3 win) = P(win M1)*P(win M2)
               + P(win M1)*P(lose M2)*P(win M3)
               + P(lose M1)*P(win M2)*P(win M3)

    p1, p2, p3 are P(team A wins Map 1/2/3).
    If Map 3 market doesn't exist, use 0.5 (no information).
    """
    win_2_0 = p1 * p2
    win_2_1_a = p1 * (1 - p2) * p3
    win_2_1_b = (1 - p1) * p2 * p3
    return win_2_0 + win_2_1_a + win_2_1_b


def build_bundles(markets: list) -> dict[str, MatchBundle]:
    """Group CS2 markets into match bundles with BO3 + map winners."""
    bundles: dict[str, MatchBundle] = {}

    for m in markets:
        q = getattr(m, "question", "")
        p = getattr(m, "current_probability", None)
        if not isinstance(p, (int, float)):
            continue

        if not is_cs2_market(q):
            continue

        # Try map winner first
        map_parsed = parse_map_market(q)
        if map_parsed:
            match_key, map_num, team_a, team_b = map_parsed
            if match_key not in bundles:
                bundles[match_key] = MatchBundle(match_key, team_a, team_b)
            bundles[match_key].map_markets[map_num] = m
            continue

        # Try BO3 winner
        bo3_parsed = parse_bo3_market(q)
        if bo3_parsed:
            match_key, team_a, team_b = bo3_parsed
            if match_key not in bundles:
                bundles[match_key] = MatchBundle(match_key, team_a, team_b)
            bundles[match_key].bo3_market = m
            continue

    return bundles


def find_opportunities(bundles: dict[str, MatchBundle]) -> list[tuple]:
    """
    For each BO3 match with at least Map 1 + Map 2 + BO3 winner, calculate
    implied BO3 probability from map probabilities and compare with actual.

    Returns list of (bo3_market, side, violation_mag, reasoning).
    """
    opportunities: list[tuple] = []

    for key, bundle in bundles.items():
        if bundle.bo3_market is None:
            continue
        if 1 not in bundle.map_markets or 2 not in bundle.map_markets:
            continue

        bo3_p = float(getattr(bundle.bo3_market, "current_probability", 0))
        p1 = float(getattr(bundle.map_markets[1], "current_probability", 0))
        p2 = float(getattr(bundle.map_markets[2], "current_probability", 0))

        # Use Map 3 probability if available, else 0.5
        p3 = 0.5
        if 3 in bundle.map_markets:
            p3 = float(getattr(bundle.map_markets[3], "current_probability", 0))

        implied = implied_bo3_probability(p1, p2, p3)
        diff = implied - bo3_p

        if abs(diff) < MIN_VIOLATION:
            continue

        maps_str = f"M1={p1:.1%} M2={p2:.1%}"
        if 3 in bundle.map_markets:
            maps_str += f" M3={p3:.1%}"

        if diff > 0:
            # Implied is higher than actual -> BO3 is underpriced -> buy YES
            reason = (
                f"BO3 underpriced: implied={implied:.1%} vs actual={bo3_p:.1%} "
                f"(diff={diff:+.1%}) [{maps_str}] -- "
                f"{bundle.team_a} vs {bundle.team_b}"
            )
            opportunities.append((bundle.bo3_market, "yes", abs(diff), reason))
        else:
            # Implied is lower than actual -> BO3 is overpriced -> buy NO
            reason = (
                f"BO3 overpriced: implied={implied:.1%} vs actual={bo3_p:.1%} "
                f"(diff={diff:+.1%}) [{maps_str}] -- "
                f"{bundle.team_a} vs {bundle.team_b}"
            )
            opportunities.append((bundle.bo3_market, "no", abs(diff), reason))

    return opportunities


# ---------------------------------------------------------------------------
# Signal, safeguards, execution
# ---------------------------------------------------------------------------

def compute_signal(market, opportunity: tuple | None) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    Conviction-based sizing per CLAUDE.md.
    """
    p = getattr(market, "current_probability", None)
    if not isinstance(p, (int, float)):
        return None, 0, "missing probability"

    # Spread gate
    spread_cents = getattr(market, "spread_cents", None)
    if isinstance(spread_cents, (int, float)) and spread_cents / 100 > MAX_SPREAD:
        return None, 0, f"Spread {spread_cents/100:.1%} > {MAX_SPREAD:.1%}"

    # Days-to-resolution gate
    resolves_at = getattr(market, "resolves_at", None)
    if resolves_at:
        try:
            resolves = datetime.fromisoformat(resolves_at.replace("Z", "+00:00"))
            days = (resolves - datetime.now(timezone.utc)).days
            if days < MIN_DAYS:
                return None, 0, f"Only {days} days to resolve"
        except Exception:
            pass

    if not opportunity:
        return None, 0, "No BO3 vs map disagreement found"

    _, side, violation_mag, reason = opportunity
    p = float(p)

    if side == "yes":
        if p > YES_THRESHOLD:
            return None, 0, f"YES blocked at {p:.1%}; threshold is {YES_THRESHOLD:.0%}"
        conviction = (YES_THRESHOLD - p) / YES_THRESHOLD
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        return "yes", size, reason

    if side == "no":
        if p < NO_THRESHOLD:
            return None, 0, f"NO blocked at {p:.1%}; threshold is {NO_THRESHOLD:.0%}"
        conviction = (p - NO_THRESHOLD) / (1 - NO_THRESHOLD)
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
    """
    Find active CS2 markets via keyword search and bulk fetch, deduplicated.
    Uses get_markets(limit=200) as primary since CS2 markets often appear in bulk.
    """
    seen: set[str] = set()
    unique: list = []

    # Bulk fetch first -- CS2 markets often in bulk
    try:
        for m in client.get_markets(limit=200):
            market_id = getattr(m, "id", None)
            if market_id and market_id not in seen:
                q = getattr(m, "question", "")
                if is_cs2_market(q):
                    seen.add(market_id)
                    unique.append(m)
    except Exception as e:
        safe_print(f"[bulk-fetch] {e}")

    # Keyword search for additional coverage
    for kw in KEYWORDS:
        try:
            for m in client.find_markets(query=kw):
                market_id = getattr(m, "id", None)
                if market_id and market_id not in seen:
                    q = getattr(m, "question", "")
                    if is_cs2_market(q):
                        seen.add(market_id)
                        unique.append(m)
        except Exception as e:
            safe_print(f"[search] {kw!r}: {e}")

    return unique


def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    safe_print(f"[bundle-cs2-maps] mode={mode} max_pos=${MAX_POSITION} min_violation={MIN_VIOLATION:.0%}")

    client = get_client(live=live)
    markets = find_markets(client)
    safe_print(f"[bundle-cs2-maps] {len(markets)} candidate markets")

    # Build match bundles
    bundles = build_bundles(markets)
    safe_print(f"[bundle-cs2-maps] {len(bundles)} match bundles: "
               + ", ".join(
                   f"{b.team_a} vs {b.team_b} "
                   f"(BO3={'Y' if b.bo3_market else 'N'}, maps={list(b.map_markets.keys())})"
                   for b in bundles.values()
               ))

    # Log each bundle
    for key, bundle in bundles.items():
        bo3_p = "N/A"
        if bundle.bo3_market:
            bo3_p = f"{float(getattr(bundle.bo3_market, 'current_probability', 0)):.1%}"
        map_prices = ", ".join(
            f"M{n}={float(getattr(m, 'current_probability', 0)):.1%}"
            for n, m in sorted(bundle.map_markets.items())
        )
        safe_print(f"  [{key}] BO3={bo3_p} {map_prices}")

    # Find opportunities
    opps = find_opportunities(bundles)
    safe_print(f"[bundle-cs2-maps] {len(opps)} opportunities found")

    # Execute trades on best violations
    placed = 0
    for opp in sorted(opps, key=lambda x: -x[2]):
        if placed >= MAX_POSITIONS:
            break

        market = opp[0]
        market_id = getattr(market, "id", None)
        if not market_id:
            continue

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

    safe_print(f"[bundle-cs2-maps] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Trades CS2 BO3 Winner markets when map probabilities imply a different outcome on Polymarket."
    )
    ap.add_argument(
        "--live",
        action="store_true",
        help="Real trades on Polymarket. Default is paper (sim) mode.",
    )
    run(live=ap.parse_args().live)
