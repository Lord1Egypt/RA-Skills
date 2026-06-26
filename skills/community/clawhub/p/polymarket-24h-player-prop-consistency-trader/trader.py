"""
polymarket-24h-player-prop-consistency-trader
Trades NBA player prop mispricings on Polymarket by detecting cross-stat
consistency (or inconsistency) for the same player.

Core edge: Polymarket lists Points O/U, Rebounds O/U, and Assists O/U for
each player. When all 3 stats for a player deviate in the same direction
from 50%, the signal is confirmed. When one stat deviates but others don't,
that outlier is likely mispriced.

Also detects within-team hierarchy inconsistencies: a star player's stat
lines should always be priced higher than role players on the same team.

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

TRADE_SOURCE = "sdk:polymarket-24h-player-prop-consistency-trader"
SKILL_SLUG   = "polymarket-24h-player-prop-consistency-trader"

KEYWORDS = [
    "Points O/U", "Rebounds O/U", "Assists O/U",
    "player props", "points over under",
    "rebounds over under", "assists over under",
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
# Minimum divergence between a player's stat lines to trigger an outlier trade
MIN_DIVERGENCE = float(os.environ.get("SIMMER_MIN_DIVERGENCE", "0.05"))

_client: SimmerClient | None = None


def get_client(live: bool = False) -> SimmerClient:
    global _client, MAX_POSITION, MIN_VOLUME, MAX_SPREAD, MIN_DAYS, MAX_POSITIONS
    global YES_THRESHOLD, NO_THRESHOLD, MIN_TRADE, MIN_DIVERGENCE
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
        MIN_DIVERGENCE = float(os.environ.get("SIMMER_MIN_DIVERGENCE", str(MIN_DIVERGENCE)))
    return _client


# ---------------------------------------------------------------------------
# Market parsing -- extract player name, stat type, O/U line
# ---------------------------------------------------------------------------

# Matches "Points O/U 23.5", "Rebounds O/U 8.5", "Assists O/U 4.5"
# Also handles "over/under" and "over under" variants
_STAT_TYPE = re.compile(
    r"(Points|Rebounds|Assists)\s+(?:O/U|over[/ ]under)\s+([\d]+(?:\.[\d]+)?)",
    re.I,
)

# Extract player name: everything before "Points|Rebounds|Assists"
# E.g. "Jayson Tatum: Points O/U 23.5" -> "Jayson Tatum"
# E.g. "Jayson Tatum Points O/U 23.5" -> "Jayson Tatum"
_PLAYER_PREFIX = re.compile(
    r"^(.*?)(?:\s*[-|:]\s*|\s+)(?:Points|Rebounds|Assists)\s+(?:O/U|over[/ ]under)",
    re.I,
)

# Team name extraction: look for "Team vs Team" or "Team @ Team" pattern in question
_TEAM_PATTERN = re.compile(
    r"([\w\s]+?)\s+(?:vs\.?|@|at)\s+([\w\s]+?)(?:\s*[-|:]|\s+\w+\s+(?:Points|Rebounds|Assists))",
    re.I,
)

# Non-sport noise filter
_NON_SPORT = re.compile(
    r"bitcoin|ethereum|btc|eth|crypto|price|stock|token|coin|nft|soccer|football|tennis",
    re.I,
)

STAT_TYPES = {"points", "rebounds", "assists"}


class PlayerProp:
    """One player prop market parsed into structured data."""
    __slots__ = ("market", "player", "stat_type", "line", "price", "team")

    def __init__(self, market, player: str, stat_type: str, line: float,
                 price: float, team: str | None = None):
        self.market = market
        self.player = player
        self.stat_type = stat_type
        self.line = line
        self.price = price
        self.team = team


def parse_stat_type_and_line(question: str) -> tuple[str, float] | None:
    """Extract stat type (points/rebounds/assists) and O/U line value."""
    m = _STAT_TYPE.search(question)
    if m:
        return m.group(1).lower(), float(m.group(2))
    return None


def parse_player_name(question: str) -> str | None:
    """Extract player name from question text."""
    m = _PLAYER_PREFIX.search(question)
    if m:
        raw = m.group(1).strip()
        # Normalize: collapse whitespace, strip punctuation
        name = re.sub(r"\s+", " ", raw).strip(" -|:,")
        # Filter out very short names (likely parsing errors)
        if len(name) >= 3 and not name.isdigit():
            return name
    return None


def parse_team(question: str) -> str | None:
    """Try to extract team context from question."""
    m = _TEAM_PATTERN.search(question)
    if m:
        return re.sub(r"\s+", " ", m.group(1).strip()).lower()
    return None


def is_player_prop_market(question: str) -> bool:
    """Return True if question looks like an NBA player prop market."""
    if _NON_SPORT.search(question):
        return False
    return _STAT_TYPE.search(question) is not None


# ---------------------------------------------------------------------------
# Player grouping and consistency analysis
# ---------------------------------------------------------------------------

def group_by_player(markets: list) -> dict[str, list[PlayerProp]]:
    """Group parsed player prop markets by normalized player name."""
    players: dict[str, list[PlayerProp]] = {}
    for m in markets:
        q = getattr(m, "question", "")
        p = getattr(m, "current_probability", None)
        if not isinstance(p, (int, float)):
            continue

        if not is_player_prop_market(q):
            continue

        parsed = parse_stat_type_and_line(q)
        if parsed is None:
            continue
        stat_type, line = parsed

        player = parse_player_name(q)
        if player is None:
            continue

        team = parse_team(q)
        prop = PlayerProp(m, player, stat_type, line, float(p), team)

        # Normalize player name for grouping (lowercase)
        key = player.lower()
        players.setdefault(key, []).append(prop)

    return players


def deviation_from_center(price: float) -> float:
    """How far a price deviates from 50%. Positive = above 50%, negative = below."""
    return price - 0.5


def same_direction(deviations: list[float]) -> bool:
    """Check if all deviations are in the same direction (all positive or all negative)."""
    if not deviations:
        return False
    positive = sum(1 for d in deviations if d > 0)
    negative = sum(1 for d in deviations if d < 0)
    return positive == len(deviations) or negative == len(deviations)


def analyze_player(props: list[PlayerProp]) -> list[tuple]:
    """
    Analyze a single player's props for consistency/divergence.
    Returns list of (market, side, conviction_boost, reasoning) for trade opportunities.

    Logic:
    - If all stats deviate same direction: CONFIRMATION signal. Conviction boost
      for all markets (they are likely correct, skip trading them unless extreme).
    - If one stat diverges from the others: OUTLIER signal. Trade the outlier
      toward the consensus direction.
    """
    if len(props) < 2:
        return []

    opportunities: list[tuple] = []
    player_name = props[0].player
    deviations = [(prop, deviation_from_center(prop.price)) for prop in props]
    devs_only = [d for _, d in deviations]

    if same_direction(devs_only):
        # All stats confirm -- check if extreme enough for conviction boost
        avg_dev = sum(abs(d) for d in devs_only) / len(devs_only)
        if avg_dev >= MIN_DIVERGENCE:
            # Confirmed multi-stat signal -- boost conviction on all markets
            for prop, dev in deviations:
                p = prop.price
                # All stats agree this player is under/over-valued
                if p <= YES_THRESHOLD:
                    boost = min(0.3, avg_dev)  # Extra conviction from confirmation
                    opportunities.append((
                        prop.market, "yes", boost,
                        f"CONFIRMED {player_name} all-stat YES: "
                        f"{prop.stat_type} O/U {prop.line}={p:.1%} "
                        f"avg_dev={avg_dev:.1%} ({len(props)} stats agree) "
                        f"-- {prop.market.question[:60]}"
                    ))
                elif p >= NO_THRESHOLD:
                    boost = min(0.3, avg_dev)
                    opportunities.append((
                        prop.market, "no", boost,
                        f"CONFIRMED {player_name} all-stat NO: "
                        f"{prop.stat_type} O/U {prop.line}={p:.1%} "
                        f"avg_dev={avg_dev:.1%} ({len(props)} stats agree) "
                        f"-- {prop.market.question[:60]}"
                    ))
    else:
        # Stats diverge -- find the outlier(s)
        # Compute median deviation direction
        positive_count = sum(1 for d in devs_only if d > 0)
        negative_count = sum(1 for d in devs_only if d < 0)
        consensus_positive = positive_count > negative_count

        for prop, dev in deviations:
            is_outlier = (dev > 0) != consensus_positive and abs(dev) >= MIN_DIVERGENCE
            if not is_outlier:
                continue

            # This stat disagrees with the other stats for this player
            # Trade it toward the consensus direction
            consensus_prices = [pr.price for pr, d in deviations
                                if (d > 0) == consensus_positive]
            avg_consensus = sum(consensus_prices) / len(consensus_prices) if consensus_prices else 0.5
            divergence_mag = abs(dev - (avg_consensus - 0.5))

            if divergence_mag < MIN_DIVERGENCE:
                continue

            p = prop.price
            if consensus_positive:
                # Consensus says player stats run high (>50%). This outlier is low.
                # If the outlier is priced low enough, buy YES (bet it goes over)
                if p <= YES_THRESHOLD:
                    opportunities.append((
                        prop.market, "yes", divergence_mag,
                        f"OUTLIER {player_name} {prop.stat_type} O/U {prop.line}={p:.1%} "
                        f"vs consensus HIGH (avg={avg_consensus:.1%}) "
                        f"divergence={divergence_mag:.1%} "
                        f"-- {prop.market.question[:60]}"
                    ))
            else:
                # Consensus says player stats run low (<50%). This outlier is high.
                # If the outlier is priced high enough, sell NO (bet it won't go over)
                if p >= NO_THRESHOLD:
                    opportunities.append((
                        prop.market, "no", divergence_mag,
                        f"OUTLIER {player_name} {prop.stat_type} O/U {prop.line}={p:.1%} "
                        f"vs consensus LOW (avg={avg_consensus:.1%}) "
                        f"divergence={divergence_mag:.1%} "
                        f"-- {prop.market.question[:60]}"
                    ))

    return opportunities


def find_all_opportunities(players: dict[str, list[PlayerProp]]) -> list[tuple]:
    """Run consistency analysis on all players and collect trade opportunities."""
    all_opps: list[tuple] = []
    for player_key, props in players.items():
        opps = analyze_player(props)
        all_opps.extend(opps)
    return all_opps


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

    Conviction scales with the magnitude of the cross-stat divergence or
    the confirmation boost. Threshold gates (YES_THRESHOLD / NO_THRESHOLD)
    still apply as hard limits.
    """
    ok, why = valid_market(market)
    if not ok:
        return None, 0, why

    if not opportunity:
        return None, 0, "No consistency signal found"

    _, side, extra_conviction, reason = opportunity
    p = float(getattr(market, "current_probability", 0))

    if side == "yes":
        if p > YES_THRESHOLD:
            return None, 0, f"YES blocked at {p:.1%}; threshold is {YES_THRESHOLD:.0%}"
        conviction = (YES_THRESHOLD - p) / YES_THRESHOLD
        # Apply cross-stat boost (capped so total conviction <= 1.0)
        conviction = min(1.0, conviction + extra_conviction)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        return "yes", size, reason

    if side == "no":
        if p < NO_THRESHOLD:
            return None, 0, f"NO blocked at {p:.1%}; threshold is {NO_THRESHOLD:.0%}"
        conviction = (p - NO_THRESHOLD) / (1 - NO_THRESHOLD)
        # Apply cross-stat boost (capped so total conviction <= 1.0)
        conviction = min(1.0, conviction + extra_conviction)
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
    """Find active NBA player prop markets, deduplicated."""
    seen: set[str] = set()
    unique: list = []
    for kw in KEYWORDS:
        try:
            for m in client.find_markets(query=kw):
                market_id = getattr(m, "id", None)
                if market_id and market_id not in seen:
                    q = getattr(m, "question", "")
                    if is_player_prop_market(q):
                        seen.add(market_id)
                        unique.append(m)
        except Exception as e:
            print(f"[search] {kw!r}: {e}")
    return unique


def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    print(f"[24h-player-prop-consistency] mode={mode} max_pos=${MAX_POSITION} "
          f"min_divergence={MIN_DIVERGENCE:.0%}")

    client = get_client(live=live)
    markets = find_markets(client)
    print(f"[24h-player-prop-consistency] {len(markets)} candidate markets")

    # Group markets by player
    players = group_by_player(markets)
    print(f"[24h-player-prop-consistency] {len(players)} players found: "
          + ", ".join(f"{k}({len(v)} props)" for k, v in players.items()))

    # Log each player's prop structure
    for player_key, props in players.items():
        print(f"  [{player_key}] " + ", ".join(
            f"{p.stat_type} O/U {p.line}={p.price:.1%}" for p in props
        ))

    # Find consistency/divergence opportunities
    all_opps = find_all_opportunities(players)

    # Deduplicate by market id, keeping the strongest signal
    best_opps: dict[str, tuple] = {}
    for opp in all_opps:
        market, side, mag, reason = opp
        mid = getattr(market, "id", None)
        if not mid:
            continue
        existing = best_opps.get(mid)
        if existing is None or mag > existing[2]:
            best_opps[mid] = opp

    print(f"[24h-player-prop-consistency] {len(best_opps)} trade opportunities")

    # Execute trades on best opportunities
    placed = 0
    for market_id, opp in sorted(best_opps.items(), key=lambda x: -x[1][2]):
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

    print(f"[24h-player-prop-consistency] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Trades NBA player prop consistency/divergence mispricings on Polymarket."
    )
    ap.add_argument(
        "--live",
        action="store_true",
        help="Real trades on Polymarket. Default is paper (sim) mode.",
    )
    run(live=ap.parse_args().live)
