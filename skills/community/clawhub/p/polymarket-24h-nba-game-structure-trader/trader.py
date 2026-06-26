"""
polymarket-24h-nba-game-structure-trader
Trades structural inconsistencies across correlated NBA game markets on Polymarket
by grouping moneyline, spread, O/U (full-game & 1H), and 1H moneyline markets
for the same game and detecting cross-market mispricings.

Core edge: Each NBA game spawns MULTIPLE correlated markets:
    Moneyline:    "Clippers vs. Pacers" = 79.7%
    1H Moneyline: "Clippers vs. Pacers: 1H Moneyline" = 50.5%
    Full O/U:     "Clippers vs. Pacers: O/U 235.5" = 56.7%
    1H O/U:       "Clippers vs. Pacers: 1H O/U 114.5" = 50.5%
    Spread:       "Spread: Clippers (-8.5)" = 41%

These MUST be internally consistent:
    - If Moneyline = 80% favorite, 1H Moneyline cannot be a coin-flip
    - Full-game O/U lines must be monotonically decreasing
    - 1H O/U < Full-game O/U always
    - Spread favorite must align with Moneyline favorite

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

TRADE_SOURCE = "sdk:polymarket-24h-nba-game-structure-trader"
SKILL_SLUG   = "polymarket-24h-nba-game-structure-trader"

# NBA team names for discovery
NBA_TEAMS = [
    "76ers", "Bucks", "Bulls", "Cavaliers", "Celtics", "Clippers",
    "Grizzlies", "Hawks", "Heat", "Hornets", "Jazz", "Kings",
    "Knicks", "Lakers", "Magic", "Mavericks", "Nets", "Nuggets",
    "Pacers", "Pelicans", "Pistons", "Raptors", "Rockets", "Spurs",
    "Suns", "Thunder", "Timberwolves", "Trail Blazers", "Warriors", "Wizards",
]

KEYWORDS = [
    "Clippers", "Celtics", "Hawks", "Cavaliers", "Heat",
    "Pelicans", "Raptors", "Lakers", "Warriors", "Pacers",
    "Spread", "Moneyline",
]

# Risk parameters -- declared as tunables in clawhub.json
MAX_POSITION       = float(os.environ.get("SIMMER_MAX_POSITION",      "40"))
MIN_VOLUME         = float(os.environ.get("SIMMER_MIN_VOLUME",        "5000"))
MAX_SPREAD         = float(os.environ.get("SIMMER_MAX_SPREAD",        "0.08"))
MIN_DAYS           = int(os.environ.get(  "SIMMER_MIN_DAYS",          "0"))
MAX_POSITIONS      = int(os.environ.get(  "SIMMER_MAX_POSITIONS",     "8"))
YES_THRESHOLD      = float(os.environ.get("SIMMER_YES_THRESHOLD",     "0.38"))
NO_THRESHOLD       = float(os.environ.get("SIMMER_NO_THRESHOLD",      "0.62"))
MIN_TRADE          = float(os.environ.get("SIMMER_MIN_TRADE",         "5"))
MIN_INCONSISTENCY  = float(os.environ.get("SIMMER_MIN_INCONSISTENCY", "0.05"))

_client: SimmerClient | None = None


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
        MAX_POSITION       = float(os.environ.get("SIMMER_MAX_POSITION",      str(MAX_POSITION)))
        MIN_VOLUME         = float(os.environ.get("SIMMER_MIN_VOLUME",        str(MIN_VOLUME)))
        MAX_SPREAD         = float(os.environ.get("SIMMER_MAX_SPREAD",        str(MAX_SPREAD)))
        MIN_DAYS           = int(os.environ.get(  "SIMMER_MIN_DAYS",          str(MIN_DAYS)))
        MAX_POSITIONS      = int(os.environ.get(  "SIMMER_MAX_POSITIONS",     str(MAX_POSITIONS)))
        YES_THRESHOLD      = float(os.environ.get("SIMMER_YES_THRESHOLD",     str(YES_THRESHOLD)))
        NO_THRESHOLD       = float(os.environ.get("SIMMER_NO_THRESHOLD",      str(NO_THRESHOLD)))
        MIN_TRADE          = float(os.environ.get("SIMMER_MIN_TRADE",         str(MIN_TRADE)))
        MIN_INCONSISTENCY  = float(os.environ.get("SIMMER_MIN_INCONSISTENCY", str(MIN_INCONSISTENCY)))
    return _client


# ---------------------------------------------------------------------------
# Market parsing -- extract teams, market type, scope, line value
# ---------------------------------------------------------------------------

# Match "vs." or "vs" between two team/city names
_VS_PATTERN = re.compile(r"(.+?)\s+vs\.?\s+(.+?)(?:\s*[:\-|]|$)", re.I)

# Market type detection
_MONEYLINE_1H = re.compile(r"1H\s+Moneyline", re.I)
_MONEYLINE    = re.compile(r"Moneyline", re.I)
_SPREAD_1H    = re.compile(r"1H\s+Spread", re.I)
_SPREAD       = re.compile(r"Spread", re.I)
_OU_1H        = re.compile(r"1H\s+O/U\s+([\d]+(?:\.[\d]+)?)", re.I)
_OU_FULL      = re.compile(r"O/U\s+([\d]+(?:\.[\d]+)?)", re.I)
_SPREAD_LINE  = re.compile(r"\(([+-]?[\d]+(?:\.[\d]+)?)\)", re.I)

# Filter: must be NBA-related
_NBA_INDICATOR = re.compile(
    r"NBA|" + "|".join(re.escape(t) for t in NBA_TEAMS),
    re.I,
)

# Non-NBA noise
_NON_NBA = re.compile(
    r"bitcoin|ethereum|btc|eth|crypto|price|stock|token|coin|nft|soccer|football|tennis|MLB|NHL|UFC|MMA",
    re.I,
)


class MarketInfo:
    """Parsed information about a single NBA market."""
    __slots__ = ("market", "game_key", "market_type", "scope", "line", "price",
                 "team1", "team2", "spread_team")

    def __init__(self, market, game_key: str, market_type: str, scope: str,
                 line: float | None, price: float, team1: str, team2: str,
                 spread_team: str | None = None):
        self.market = market
        self.game_key = game_key
        self.market_type = market_type  # "moneyline", "spread", "ou"
        self.scope = scope              # "full", "1h"
        self.line = line                # O/U line or spread line
        self.price = price
        self.team1 = team1
        self.team2 = team2
        self.spread_team = spread_team  # team name for spread markets


def normalize_team(name: str) -> str:
    """Normalize a team name for matching."""
    return re.sub(r"\s+", " ", name.lower()).strip(" -|:.")


def extract_game_key(team1: str, team2: str) -> str:
    """Create a canonical game key from two team names, sorted for consistency."""
    t1, t2 = normalize_team(team1), normalize_team(team2)
    return "|".join(sorted([t1, t2]))


def parse_market(market) -> MarketInfo | None:
    """Parse a market into a structured MarketInfo, or None if not an NBA market."""
    q = getattr(market, "question", "")
    p = getattr(market, "current_probability", None)
    if not isinstance(p, (int, float)):
        return None

    # Must be NBA-related
    if _NON_NBA.search(q):
        return None

    price = float(p)

    # Try to extract teams from "X vs. Y" pattern
    vs_match = _VS_PATTERN.search(q)
    if not vs_match:
        # Try spread format: "Spread: Team (-5.5)"
        spread_match = re.match(r"(?:1H\s+)?Spread:\s*(.+?)\s*\(", q, re.I)
        if not spread_match:
            return None
        # For standalone spread markets, we need the team name from context
        spread_team_raw = spread_match.group(1).strip()
        # We cannot determine both teams from this format alone;
        # these will be matched to game groups later via team name overlap
        team1 = spread_team_raw
        team2 = ""
    else:
        team1 = vs_match.group(1).strip()
        team2 = vs_match.group(2).strip()

    # Must have at least one NBA team indicator
    if not _NBA_INDICATOR.search(q):
        return None

    # Determine market type and scope
    spread_team = None

    if _OU_1H.search(q):
        market_type = "ou"
        scope = "1h"
        line = float(_OU_1H.search(q).group(1))
    elif _OU_FULL.search(q):
        market_type = "ou"
        scope = "full"
        line = float(_OU_FULL.search(q).group(1))
    elif _SPREAD_1H.search(q):
        market_type = "spread"
        scope = "1h"
        line_m = _SPREAD_LINE.search(q)
        line = float(line_m.group(1)) if line_m else None
        spread_m = re.search(r"(?:1H\s+)?Spread:\s*(.+?)\s*\(", q, re.I)
        if spread_m:
            spread_team = normalize_team(spread_m.group(1))
    elif _SPREAD.search(q):
        market_type = "spread"
        scope = "full"
        line_m = _SPREAD_LINE.search(q)
        line = float(line_m.group(1)) if line_m else None
        spread_m = re.search(r"Spread:\s*(.+?)\s*\(", q, re.I)
        if spread_m:
            spread_team = normalize_team(spread_m.group(1))
    elif _MONEYLINE_1H.search(q):
        market_type = "moneyline"
        scope = "1h"
        line = None
    elif _MONEYLINE.search(q):
        market_type = "moneyline"
        scope = "full"
        line = None
    else:
        # Plain "X vs. Y" with no qualifier -- treat as moneyline
        market_type = "moneyline"
        scope = "full"
        line = None

    if team2:
        game_key = extract_game_key(team1, team2)
    else:
        game_key = normalize_team(team1)

    return MarketInfo(
        market=market,
        game_key=game_key,
        market_type=market_type,
        scope=scope,
        line=line,
        price=price,
        team1=normalize_team(team1),
        team2=normalize_team(team2),
        spread_team=spread_team,
    )


# ---------------------------------------------------------------------------
# Game grouping and cross-market consistency checks
# ---------------------------------------------------------------------------

class GameGroup:
    """All markets for a single NBA game."""
    def __init__(self, game_key: str):
        self.game_key = game_key
        self.moneyline_full: MarketInfo | None = None
        self.moneyline_1h: MarketInfo | None = None
        self.spreads_full: list[MarketInfo] = []
        self.spreads_1h: list[MarketInfo] = []
        self.ou_full: list[MarketInfo] = []
        self.ou_1h: list[MarketInfo] = []

    def add(self, info: MarketInfo) -> None:
        if info.market_type == "moneyline":
            if info.scope == "1h":
                self.moneyline_1h = info
            else:
                self.moneyline_full = info
        elif info.market_type == "spread":
            if info.scope == "1h":
                self.spreads_1h.append(info)
            else:
                self.spreads_full.append(info)
        elif info.market_type == "ou":
            if info.scope == "1h":
                self.ou_1h.append(info)
            else:
                self.ou_full.append(info)

    @property
    def market_count(self) -> int:
        count = 0
        if self.moneyline_full:
            count += 1
        if self.moneyline_1h:
            count += 1
        count += len(self.spreads_full) + len(self.spreads_1h)
        count += len(self.ou_full) + len(self.ou_1h)
        return count


def build_game_groups(markets: list) -> dict[str, GameGroup]:
    """Parse all markets and group by game."""
    groups: dict[str, GameGroup] = {}

    for m in markets:
        info = parse_market(m)
        if info is None:
            continue
        if info.game_key not in groups:
            groups[info.game_key] = GameGroup(info.game_key)
        groups[info.game_key].add(info)

    return groups


def find_inconsistencies(groups: dict[str, GameGroup]) -> list[tuple]:
    """
    Cross-check consistency within each game group.
    Returns list of (market, side, inconsistency_magnitude, reasoning).

    Checks:
    1. Moneyline vs 1H Moneyline: heavy favorite (>70%) with coin-flip 1H
    2. O/U monotonicity: full-game O/U lines must decrease with higher totals
    3. 1H O/U vs Full O/U: at same line value, 1H must be <= full-game
    4. Spread direction vs Moneyline: favorite must align
    """
    opportunities: list[tuple] = []

    for game_key, group in groups.items():
        if group.market_count < 2:
            continue

        # --- Check 1: Moneyline vs 1H Moneyline consistency ---
        if group.moneyline_full and group.moneyline_1h:
            ml_full = group.moneyline_full.price
            ml_1h = group.moneyline_1h.price

            # A heavy full-game favorite should also lead 1H.
            # Expected: 1H ML >= 0.5 + (full ML - 0.5) * dampening
            # Simple heuristic: if full ML > 0.70, 1H ML should be > 0.55
            # The inconsistency grows with the gap
            if ml_full > 0.70:
                expected_1h_floor = 0.50 + (ml_full - 0.50) * 0.40
                if ml_1h < expected_1h_floor:
                    violation = expected_1h_floor - ml_1h
                    if violation >= MIN_INCONSISTENCY:
                        # 1H moneyline is too low -- buy YES on 1H
                        opportunities.append((
                            group.moneyline_1h.market, "yes", violation,
                            f"1H ML too low: full ML={ml_full:.1%} implies 1H>={expected_1h_floor:.1%} "
                            f"but 1H={ml_1h:.1%} | gap={violation:.1%} -- "
                            f"{group.moneyline_1h.market.question[:55]}"
                        ))
            elif ml_full < 0.30:
                expected_1h_ceil = 0.50 - (0.50 - ml_full) * 0.40
                if ml_1h > expected_1h_ceil:
                    violation = ml_1h - expected_1h_ceil
                    if violation >= MIN_INCONSISTENCY:
                        # 1H moneyline is too high -- sell NO on 1H
                        opportunities.append((
                            group.moneyline_1h.market, "no", violation,
                            f"1H ML too high: full ML={ml_full:.1%} implies 1H<={expected_1h_ceil:.1%} "
                            f"but 1H={ml_1h:.1%} | gap={violation:.1%} -- "
                            f"{group.moneyline_1h.market.question[:55]}"
                        ))

        # --- Check 2: Full-game O/U monotonicity ---
        if len(group.ou_full) >= 2:
            sorted_ou = sorted(group.ou_full, key=lambda x: x.line)
            for i in range(len(sorted_ou) - 1):
                lo = sorted_ou[i]
                hi = sorted_ou[i + 1]
                # P(OVER lower line) >= P(OVER higher line) always
                violation = hi.price - lo.price
                if violation > MIN_INCONSISTENCY:
                    opportunities.append((
                        hi.market, "no", violation,
                        f"O/U monotonicity: P(O/U {hi.line} OVER)={hi.price:.1%} > "
                        f"P(O/U {lo.line} OVER)={lo.price:.1%} | "
                        f"violation={violation:.1%} -- {hi.market.question[:55]}"
                    ))
                    opportunities.append((
                        lo.market, "yes", violation,
                        f"O/U monotonicity: P(O/U {lo.line} OVER)={lo.price:.1%} < "
                        f"P(O/U {hi.line} OVER)={hi.price:.1%} | "
                        f"violation={violation:.1%} -- {lo.market.question[:55]}"
                    ))

        # --- Check 3: 1H O/U vs Full-game O/U ---
        # At the same or similar line, P(1H OVER X) should generally be higher
        # than P(Full OVER X) because 1H lines are much lower.
        # But if we find 1H and full at SAME line value: P(Full OVER) >= P(1H OVER).
        if group.ou_1h and group.ou_full:
            full_map: dict[float, MarketInfo] = {m.line: m for m in group.ou_full}
            for h in group.ou_1h:
                full_match = full_map.get(h.line)
                if full_match is None:
                    continue
                # At same line: Full game total >= 1H total, so
                # P(Full OVER X) >= P(1H OVER X)
                violation = h.price - full_match.price
                if violation > MIN_INCONSISTENCY:
                    opportunities.append((
                        h.market, "no", violation,
                        f"1H O/U > Full O/U at line {h.line}: "
                        f"1H={h.price:.1%} > Full={full_match.price:.1%} | "
                        f"violation={violation:.1%} -- {h.market.question[:55]}"
                    ))
                    opportunities.append((
                        full_match.market, "yes", violation,
                        f"Full O/U < 1H O/U at line {h.line}: "
                        f"Full={full_match.price:.1%} < 1H={h.price:.1%} | "
                        f"violation={violation:.1%} -- {full_match.market.question[:55]}"
                    ))

        # --- Check 4: Spread direction vs Moneyline ---
        if group.moneyline_full and group.spreads_full:
            ml = group.moneyline_full
            ml_favorite = ml.team1 if ml.price > 0.50 else ml.team2

            for sp in group.spreads_full:
                if sp.spread_team is None or sp.line is None:
                    continue
                # Negative spread = favorite. If spread says team is favorite
                # (negative line) but moneyline says they are the underdog, inconsistency.
                spread_says_favorite = sp.line < 0
                spread_team_is_ml_favorite = any(
                    t in ml_favorite for t in sp.spread_team.split()
                ) or any(
                    t in sp.spread_team for t in ml_favorite.split()
                )

                if spread_says_favorite and not spread_team_is_ml_favorite:
                    # Spread market implies wrong favorite
                    violation = abs(ml.price - 0.50) * 0.5
                    if violation >= MIN_INCONSISTENCY:
                        opportunities.append((
                            sp.market, "no", violation,
                            f"Spread/ML mismatch: Spread favors {sp.spread_team} ({sp.line}) "
                            f"but ML favors {ml_favorite} ({ml.price:.1%}) | "
                            f"gap={violation:.1%} -- {sp.market.question[:55]}"
                        ))
                elif not spread_says_favorite and spread_team_is_ml_favorite:
                    violation = abs(ml.price - 0.50) * 0.5
                    if violation >= MIN_INCONSISTENCY:
                        opportunities.append((
                            sp.market, "yes", violation,
                            f"Spread/ML mismatch: Spread has {sp.spread_team} as dog ({sp.line}) "
                            f"but ML favors them ({ml.price:.1%}) | "
                            f"gap={violation:.1%} -- {sp.market.question[:55]}"
                        ))

    return opportunities


# ---------------------------------------------------------------------------
# Signal, safeguards, execution
# ---------------------------------------------------------------------------

def valid_market(market) -> tuple[bool, str]:
    """Check basic market quality gates."""
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

    Conviction scales with the magnitude of the structural inconsistency.
    Threshold gates (YES_THRESHOLD / NO_THRESHOLD) still apply as hard limits.
    """
    ok, why = valid_market(market)
    if not ok:
        return None, 0, why

    if not opportunity:
        return None, 0, "No structural inconsistency found"

    _, side, violation_mag, reason = opportunity
    p = float(getattr(market, "current_probability", 0))

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
            print(f"  [warn] {w}")
    except Exception as e:
        print(f"  [ctx] {market_id}: {e}")
    return True, "ok"


def find_markets(client: SimmerClient) -> list:
    """Find active NBA game markets, deduplicated."""
    seen: set[str] = set()
    unique: list = []

    # Search by keywords and team names
    search_terms = KEYWORDS + NBA_TEAMS[:10]  # Top teams for broader coverage
    _KEEP = re.compile(r"vs\.|Spread|Moneyline|O/U", re.I)
    for kw in search_terms:
        try:
            for m in client.find_markets(query=kw):
                market_id = getattr(m, "id", None)
                if market_id and market_id not in seen:
                    q = getattr(m, "question", "")
                    if _NBA_INDICATOR.search(q) and not _NON_NBA.search(q) and _KEEP.search(q):
                        seen.add(market_id)
                        unique.append(m)
        except Exception as e:
            print(f"[search] {kw!r}: {e}")
    return unique


def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    print(f"[24h-nba-game-structure] mode={mode} max_pos=${MAX_POSITION} "
          f"min_inconsistency={MIN_INCONSISTENCY:.0%}")

    client = get_client(live=live)
    markets = find_markets(client)
    print(f"[24h-nba-game-structure] {len(markets)} candidate markets")

    # Group markets by game
    groups = build_game_groups(markets)
    print(f"[24h-nba-game-structure] {len(groups)} games found: "
          + ", ".join(f"{k}({g.market_count} mkts)" for k, g in groups.items()))

    # Log each game's market structure
    for game_key, group in groups.items():
        parts = []
        if group.moneyline_full:
            parts.append(f"ML={group.moneyline_full.price:.1%}")
        if group.moneyline_1h:
            parts.append(f"1H-ML={group.moneyline_1h.price:.1%}")
        for ou in sorted(group.ou_full, key=lambda x: x.line):
            parts.append(f"O/U {ou.line}={ou.price:.1%}")
        for ou in sorted(group.ou_1h, key=lambda x: x.line):
            parts.append(f"1H O/U {ou.line}={ou.price:.1%}")
        for sp in group.spreads_full:
            parts.append(f"Spread({sp.spread_team} {sp.line})={sp.price:.1%}")
        for sp in group.spreads_1h:
            parts.append(f"1H-Spread({sp.spread_team} {sp.line})={sp.price:.1%}")
        print(f"  [{game_key}] {' | '.join(parts)}")

    # Find structural inconsistencies across all game groups
    all_opps: dict[str, tuple] = {}
    inconsistencies = find_inconsistencies(groups)
    for market, side, mag, reason in inconsistencies:
        mid = getattr(market, "id", None)
        if not mid:
            continue
        existing = all_opps.get(mid)
        if existing is None or mag > existing[2]:
            all_opps[mid] = (market, side, mag, reason)

    print(f"[24h-nba-game-structure] {len(all_opps)} inconsistency opportunities")

    # Execute trades on the most inconsistent legs
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

    print(f"[24h-nba-game-structure] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Trades structural inconsistencies across correlated NBA game markets on Polymarket."
    )
    ap.add_argument(
        "--live",
        action="store_true",
        help="Real trades on Polymarket. Default is paper (sim) mode.",
    )
    run(live=ap.parse_args().live)
