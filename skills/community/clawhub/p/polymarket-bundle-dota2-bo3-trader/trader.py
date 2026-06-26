"""
polymarket-bundle-dota2-bo3-trader
Trades structural inconsistencies between Dota 2 BO3 winner, individual game
winners, and game handicap markets on Polymarket.

Core edge: P(BO3 win) = f(P(Game1), P(Game2), P(Game3)). Game handicap (-1.5
means team must win 2-0) constrains the BO3 probability. When these are
inconsistent, it is structural arbitrage.

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

TRADE_SOURCE = "sdk:polymarket-bundle-dota2-bo3-trader"
SKILL_SLUG   = "polymarket-bundle-dota2-bo3-trader"

KEYWORDS = [
    'Dota 2',
    'Dota',
    'BO3',
    'Game 1 Winner',
    'Game 2 Winner',
    'Game Handicap',
    'ESL',
    'DreamLeague',
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
# Minimum inconsistency between implied and market BO3 probability to trade
MIN_INCONSISTENCY = float(os.environ.get("SIMMER_MIN_INCONSISTENCY", "0.08"))

_client: SimmerClient | None = None


def safe_print(text):
    """Print with fallback for non-ASCII characters (Windows cp1252 terminals)."""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('ascii', 'replace').decode())


def get_client(live: bool = False) -> SimmerClient:
    global _client, MAX_POSITION, MIN_VOLUME, MAX_SPREAD, MIN_DAYS, MAX_POSITIONS
    global YES_THRESHOLD, NO_THRESHOLD, MIN_TRADE, MIN_INCONSISTENCY
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
        MAX_POSITION      = float(os.environ.get("SIMMER_MAX_POSITION",      str(MAX_POSITION)))
        MIN_VOLUME        = float(os.environ.get("SIMMER_MIN_VOLUME",        str(MIN_VOLUME)))
        MAX_SPREAD        = float(os.environ.get("SIMMER_MAX_SPREAD",        str(MAX_SPREAD)))
        MIN_DAYS          = int(os.environ.get(  "SIMMER_MIN_DAYS",          str(MIN_DAYS)))
        MAX_POSITIONS     = int(os.environ.get(  "SIMMER_MAX_POSITIONS",     str(MAX_POSITIONS)))
        YES_THRESHOLD     = float(os.environ.get("SIMMER_YES_THRESHOLD",     str(YES_THRESHOLD)))
        NO_THRESHOLD      = float(os.environ.get("SIMMER_NO_THRESHOLD",      str(NO_THRESHOLD)))
        MIN_TRADE         = float(os.environ.get("SIMMER_MIN_TRADE",         str(MIN_TRADE)))
        MIN_INCONSISTENCY = float(os.environ.get("SIMMER_MIN_INCONSISTENCY", str(MIN_INCONSISTENCY)))
    return _client


# ---------------------------------------------------------------------------
# Market parsing -- extract match_key, market_type, team info
# ---------------------------------------------------------------------------

# "Dota 2: Team A vs Team B - Game N Winner"
_GAME_WINNER = re.compile(
    r"(?:dota\s*2?)\s*:\s*(.+?)\s+vs\.?\s+(.+?)\s*[-|]\s*game\s+(\d+)\s+winner",
    re.I,
)

# "Dota 2: Team A vs Team B (BO3) - Tournament" or "Dota 2: Team A vs Team B - BO3 Winner"
_BO3_WINNER = re.compile(
    r"(?:dota\s*2?)\s*:\s*(.+?)\s+vs\.?\s+(.+?)\s*(?:[-|]\s*)?(?:\(BO3\)|BO3|best\s+of\s+3|winner|match\s+winner)",
    re.I,
)

# "Game Handicap: Team A (-1.5) vs Team B (+1.5)" or "Dota 2: ... Game Handicap ... (-1.5)"
_HANDICAP = re.compile(
    r"(?:game\s+)?handicap.*?(\w[\w\s.]+?)\s*\(\s*([+-]?\d+\.?\d*)\s*\)\s*vs\.?\s*(\w[\w\s.]+?)\s*\(\s*([+-]?\d+\.?\d*)\s*\)",
    re.I,
)

# Broader Dota 2 filter
_DOTA_INDICATOR = re.compile(
    r"dota\s*2?|dreamleague|esl\s+one|the\s+international|dpc|bts\s+pro",
    re.I,
)


def normalize_team(name: str) -> str:
    """Normalize a team name for matching."""
    return re.sub(r"\s+", " ", name.lower().strip(" .-|:,"))


def make_match_key(team_a: str, team_b: str) -> str:
    """Create a canonical match key from two team names (sorted for consistency)."""
    a, b = normalize_team(team_a), normalize_team(team_b)
    return "|".join(sorted([a, b]))


def parse_market(question: str) -> dict | None:
    """
    Parse a Dota 2 market question into structured data.
    Returns dict with keys: match_key, type, team_a, team_b, and type-specific fields.
    Returns None if not a recognized Dota 2 market.
    """
    if not _DOTA_INDICATOR.search(question):
        return None

    # Try game winner first
    m = _GAME_WINNER.search(question)
    if m:
        team_a, team_b, game_num = m.group(1), m.group(2), int(m.group(3))
        return {
            "match_key": make_match_key(team_a, team_b),
            "type": "game_winner",
            "game_number": game_num,
            "team_a": normalize_team(team_a),
            "team_b": normalize_team(team_b),
        }

    # Try handicap
    m = _HANDICAP.search(question)
    if m:
        team_a, hcap_a, team_b, hcap_b = m.group(1), float(m.group(2)), m.group(3), float(m.group(4))
        return {
            "match_key": make_match_key(team_a, team_b),
            "type": "handicap",
            "team_a": normalize_team(team_a),
            "team_b": normalize_team(team_b),
            "handicap_team": normalize_team(team_a) if hcap_a < 0 else normalize_team(team_b),
            "handicap_value": min(hcap_a, hcap_b),  # e.g. -1.5
        }

    # Try BO3 winner (broader match -- check last to avoid false positives)
    m = _BO3_WINNER.search(question)
    if m:
        team_a, team_b = m.group(1), m.group(2)
        return {
            "match_key": make_match_key(team_a, team_b),
            "type": "bo3_winner",
            "team_a": normalize_team(team_a),
            "team_b": normalize_team(team_b),
        }

    return None


def is_dota_bo3_market(question: str) -> bool:
    """Return True if the question looks like a relevant Dota 2 BO3 market."""
    return parse_market(question) is not None


# ---------------------------------------------------------------------------
# Group markets by match and find inconsistencies
# ---------------------------------------------------------------------------

class MatchMarket:
    """One market mapped to a match with parsed metadata."""
    __slots__ = ("market", "parsed", "price")

    def __init__(self, market, parsed: dict, price: float):
        self.market = market
        self.parsed = parsed
        self.price = price


def group_by_match(markets: list) -> dict[str, list[MatchMarket]]:
    """Group markets by match_key."""
    matches: dict[str, list[MatchMarket]] = {}
    for m in markets:
        q = getattr(m, "question", "")
        p = getattr(m, "current_probability", None)
        if not isinstance(p, (int, float)):
            continue

        parsed = parse_market(q)
        if parsed is None:
            continue

        key = parsed["match_key"]
        mm = MatchMarket(m, parsed, float(p))
        matches.setdefault(key, []).append(mm)

    return matches


def compute_implied_bo3(game_probs: dict[int, float], team: str) -> float:
    """
    Compute implied BO3 win probability for a team from individual game probabilities.
    P(BO3 win) = P(G1)*P(G2) + P(G1)*(1-P(G2))*P(G3) + (1-P(G1))*P(G2)*P(G3)

    game_probs maps game_number -> P(team wins that game).
    If we only have G1 and G2, we estimate G3 as the average of G1 and G2.
    """
    g1 = game_probs.get(1)
    g2 = game_probs.get(2)
    g3 = game_probs.get(3)

    if g1 is None and g2 is None:
        return -1.0  # Not enough data

    # Fill missing games with available averages
    available = [v for v in [g1, g2, g3] if v is not None]
    avg = sum(available) / len(available) if available else 0.5

    if g1 is None:
        g1 = avg
    if g2 is None:
        g2 = avg
    if g3 is None:
        g3 = avg

    # P(win BO3) = P(win 2-0) + P(win 2-1 via lose G1) + P(win 2-1 via lose G2)
    p_2_0 = g1 * g2
    p_2_1_a = g1 * (1 - g2) * g3  # Win G1, lose G2, win G3
    p_2_1_b = (1 - g1) * g2 * g3  # Lose G1, win G2, win G3
    return p_2_0 + p_2_1_a + p_2_1_b


def find_inconsistencies(matches: dict[str, list[MatchMarket]]) -> list[tuple]:
    """
    For each match with BO3 winner + game winners:
    - Calculate implied BO3 from game probabilities
    - Check handicap consistency: P(handicap -1.5) should ~ P(win both games)
    - Trade inconsistencies

    Returns list of (market, side, inconsistency_magnitude, reasoning).
    """
    opportunities: list[tuple] = []

    for match_key, mms in matches.items():
        bo3_markets: list[MatchMarket] = []
        game_markets: dict[int, MatchMarket] = {}
        handicap_markets: list[MatchMarket] = []

        for mm in mms:
            t = mm.parsed["type"]
            if t == "bo3_winner":
                bo3_markets.append(mm)
            elif t == "game_winner":
                gn = mm.parsed["game_number"]
                if gn not in game_markets:
                    game_markets[gn] = mm
            elif t == "handicap":
                handicap_markets.append(mm)

        if not bo3_markets:
            continue

        # We need at least 1 game winner to compute implied BO3
        if len(game_markets) < 1:
            continue

        # Determine which team the BO3 market is pricing
        bo3_mm = bo3_markets[0]
        team_a = bo3_mm.parsed["team_a"]
        bo3_price = bo3_mm.price  # P(team_a wins BO3) as priced by market

        # Build game probabilities for team_a
        game_probs: dict[int, float] = {}
        for gn, gmm in game_markets.items():
            # The game winner market prices P(team_a wins game N)
            # If question lists team_a first, probability is for team_a
            if gmm.parsed["team_a"] == team_a:
                game_probs[gn] = gmm.price
            else:
                game_probs[gn] = 1.0 - gmm.price

        implied_bo3 = compute_implied_bo3(game_probs, team_a)
        if implied_bo3 < 0:
            continue

        inconsistency = implied_bo3 - bo3_price

        if abs(inconsistency) >= MIN_INCONSISTENCY:
            if inconsistency > 0:
                # Implied BO3 > market BO3 -> BO3 market is underpriced -> buy YES
                side = "yes"
                reason = (
                    f"YES BO3 implied={implied_bo3:.0%} vs market={bo3_price:.0%} "
                    f"gap={inconsistency:+.0%} games={len(game_probs)} "
                    f"-- {bo3_mm.market.question[:55]}"
                )
            else:
                # Implied BO3 < market BO3 -> BO3 market is overpriced -> sell NO
                side = "no"
                reason = (
                    f"NO BO3 implied={implied_bo3:.0%} vs market={bo3_price:.0%} "
                    f"gap={inconsistency:+.0%} games={len(game_probs)} "
                    f"-- {bo3_mm.market.question[:55]}"
                )
            opportunities.append((bo3_mm.market, side, abs(inconsistency), reason))

        # Check handicap consistency: P(handicap -1.5) ~ P(win G1) * P(win G2)
        for hmm in handicap_markets:
            hteam = hmm.parsed["handicap_team"]
            hval = hmm.parsed["handicap_value"]

            if abs(hval) != 1.5:
                continue  # Only handle -1.5 handicap for now

            # P(handicap -1.5 covers) = P(team wins 2-0) = P(G1) * P(G2)
            g1_p = game_probs.get(1)
            g2_p = game_probs.get(2)
            if g1_p is None or g2_p is None:
                continue

            # Adjust for which team the handicap is for
            if hteam == team_a:
                implied_hcap = g1_p * g2_p
            else:
                implied_hcap = (1 - g1_p) * (1 - g2_p)

            hcap_gap = implied_hcap - hmm.price

            if abs(hcap_gap) >= MIN_INCONSISTENCY:
                if hcap_gap > 0:
                    side = "yes"
                    reason = (
                        f"YES Handicap implied={implied_hcap:.0%} vs market={hmm.price:.0%} "
                        f"gap={hcap_gap:+.0%} -- {hmm.market.question[:55]}"
                    )
                else:
                    side = "no"
                    reason = (
                        f"NO Handicap implied={implied_hcap:.0%} vs market={hmm.price:.0%} "
                        f"gap={hcap_gap:+.0%} -- {hmm.market.question[:55]}"
                    )
                opportunities.append((hmm.market, side, abs(hcap_gap), reason))

    return opportunities


# ---------------------------------------------------------------------------
# Signal, safeguards, execution
# ---------------------------------------------------------------------------

def compute_signal(market, opportunity: tuple | None) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    Conviction scales with the magnitude of the structural inconsistency.
    Threshold gates (YES_THRESHOLD / NO_THRESHOLD) still apply as hard limits.
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
        return None, 0, "No inconsistency found"

    _, side, gap, reason = opportunity
    p = float(p)

    if side == "yes":
        if p > YES_THRESHOLD:
            return None, 0, f"YES blocked at {p:.1%}; threshold is {YES_THRESHOLD:.0%}"
        conviction = min(1.0, max(0.0, (gap - MIN_INCONSISTENCY) / max(0.01, YES_THRESHOLD)))
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        return "yes", size, reason

    if side == "no":
        if p < NO_THRESHOLD:
            return None, 0, f"NO blocked at {p:.1%}; threshold is {NO_THRESHOLD:.0%}"
        conviction = min(1.0, max(0.0, (gap - MIN_INCONSISTENCY) / max(0.01, 1 - NO_THRESHOLD)))
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
    Find active Dota 2 BO3-related markets via keyword search and bulk fetch,
    deduplicated. Uses both find_markets(query=...) and get_markets(limit=200)
    as primary fallback.
    """
    seen: set[str] = set()
    unique: list = []

    # Keyword search
    for kw in KEYWORDS:
        try:
            for m in client.find_markets(query=kw):
                market_id = getattr(m, "id", None)
                if market_id and market_id not in seen:
                    q = getattr(m, "question", "")
                    if is_dota_bo3_market(q):
                        seen.add(market_id)
                        unique.append(m)
        except Exception as e:
            safe_print(f"[search] {kw!r}: {e}")

    # Bulk fallback -- scan recent/popular markets for Dota 2 we may have missed
    try:
        for m in client.get_markets(limit=200):
            market_id = getattr(m, "id", None)
            if market_id and market_id not in seen:
                q = getattr(m, "question", "")
                if is_dota_bo3_market(q):
                    seen.add(market_id)
                    unique.append(m)
    except Exception as e:
        safe_print(f"[bulk-fetch] {e}")

    return unique


def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    safe_print(
        f"[dota2-bo3] mode={mode} max_pos=${MAX_POSITION} "
        f"min_inconsistency={MIN_INCONSISTENCY:.0%}"
    )

    client = get_client(live=live)
    markets = find_markets(client)
    safe_print(f"[dota2-bo3] {len(markets)} candidate markets")

    # Group by match
    matches = group_by_match(markets)
    safe_print(f"[dota2-bo3] {len(matches)} matches found")

    # Log each match's structure
    for match_key, mms in matches.items():
        types = [mm.parsed["type"] for mm in mms]
        safe_print(f"  [{match_key}] {len(mms)} markets: {', '.join(types)}")

    # Find inconsistencies across all matches
    all_opps: dict[str, tuple] = {}
    inconsistencies = find_inconsistencies(matches)
    for market, side, gap, reason in inconsistencies:
        mid = getattr(market, "id", None)
        if not mid:
            continue
        existing = all_opps.get(mid)
        if existing is None or gap > existing[2]:
            all_opps[mid] = (market, side, gap, reason)

    safe_print(f"[dota2-bo3] {len(all_opps)} inconsistency opportunities")

    # Execute trades on best inconsistencies
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

    safe_print(f"[dota2-bo3] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Trades structural inconsistencies between Dota 2 BO3 winner, game winners, and handicap markets on Polymarket."
    )
    ap.add_argument(
        "--live",
        action="store_true",
        help="Real trades on Polymarket. Default is paper (sim) mode.",
    )
    run(live=ap.parse_args().live)
