"""
polymarket-ladder-nhl-hockey-trader
Trades monotonicity violations in NHL hockey O/U market ladders and
spread-vs-total consistency on Polymarket.

Core edge: Each NHL game spawns multiple O/U lines at different totals:
    Wild vs Bruins: O/U 4.5 = 62%,  O/U 5.5 = 45%,  O/U 7.5 = 12%
    Maple Leafs vs Blues: O/U 4.5, O/U 5.5, O/U 6.5, O/U 7.5

These MUST be monotonically decreasing:
    P(O/U 4.5 OVER) >= P(O/U 5.5 OVER) >= P(O/U 6.5 OVER) >= P(O/U 7.5 OVER)

Additionally, spread markets constrain the O/U curve:
    - A large spread (one team heavily favored) implies a scoring profile
      that must be consistent with the O/U distribution.

When the ladder is broken, we trade the repair.

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
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-ladder-nhl-hockey-trader"
SKILL_SLUG   = "polymarket-ladder-nhl-hockey-trader"

# NHL team names for discovery and filtering
NHL_TEAMS = [
    "Bruins", "Maple Leafs", "Rangers", "Penguins", "Wild", "Blues",
    "Oilers", "Avalanche", "Lightning", "Panthers", "Capitals",
    "Hurricanes", "Stars", "Canadiens", "Senators", "Flames",
    "Canucks", "Jets", "Predators", "Red Wings", "Blackhawks",
    "Sabres", "Islanders", "Devils", "Flyers", "Blue Jackets",
    "Sharks", "Ducks", "Coyotes", "Kraken", "Golden Knights",
]

KEYWORDS = [
    "NHL", "hockey", "O/U", "Bruins", "Maple Leafs", "Rangers",
    "Penguins", "Wild", "Blues", "Oilers", "Avalanche", "Lightning",
    "Panthers", "Capitals", "Hurricanes", "Stars",
]

# Risk parameters -- declared as tunables in clawhub.json
MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",   "40"))
MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",     "5000"))
MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",     "0.08"))
MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",       "0"))
MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS",  "8"))
YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD",  "0.38"))
NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",   "0.62"))
MIN_TRADE      = float(os.environ.get("SIMMER_MIN_TRADE",      "5"))
MIN_VIOLATION  = float(os.environ.get("SIMMER_MIN_VIOLATION",  "0.05"))

_client: SimmerClient | None = None


def safe_print(*args, **kwargs):
    """Print that never crashes on encoding errors."""
    try:
        print(*args, **kwargs)
    except (UnicodeEncodeError, OSError):
        text = " ".join(str(a) for a in args)
        print(text.encode("ascii", "replace").decode(), **kwargs)


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
        MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",   str(MAX_POSITION)))
        MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",     str(MIN_VOLUME)))
        MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",     str(MAX_SPREAD)))
        MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",       str(MIN_DAYS)))
        MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS",  str(MAX_POSITIONS)))
        YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD",  str(YES_THRESHOLD)))
        NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",   str(NO_THRESHOLD)))
        MIN_TRADE      = float(os.environ.get("SIMMER_MIN_TRADE",      str(MIN_TRADE)))
        MIN_VIOLATION  = float(os.environ.get("SIMMER_MIN_VIOLATION",  str(MIN_VIOLATION)))
    return _client


# ---------------------------------------------------------------------------
# Market parsing -- extract game key, O/U line, spread info
# ---------------------------------------------------------------------------

# "Team A vs Team B: O/U X" or "Team A vs. Team B: O/U X"
_OU_PATTERN = re.compile(
    r"(.+?)\s+vs\.?\s+(.+?):\s*O/U\s+([\d]+(?:\.[\d]+)?)",
    re.I,
)

# "Spread: Team (X)" or "Spread: Team (-X)"
_SPREAD_PATTERN = re.compile(
    r"Spread:\s*(.+?)\s*\(([+-]?[\d]+(?:\.[\d]+)?)\)",
    re.I,
)

# "Team A vs Team B" plain moneyline (for spread context matching)
_VS_PATTERN = re.compile(r"(.+?)\s+vs\.?\s+(.+?)(?:\s*[:\-|]|$)", re.I)

# NHL indicator -- must match at least one NHL team or "NHL"/"hockey"
_NHL_INDICATOR = re.compile(
    r"NHL|hockey|" + "|".join(re.escape(t) for t in NHL_TEAMS),
    re.I,
)

# Non-NHL noise filter
_NON_NHL = re.compile(
    r"bitcoin|ethereum|btc|eth|crypto|price|stock|token|coin|nft|"
    r"soccer|football|tennis|MLB|NBA|UFC|MMA|cricket|rugby|golf|"
    r"boxing|wrestling|volleyball|baseball",
    re.I,
)


def normalize_team(name: str) -> str:
    """Normalize a team name for matching."""
    return re.sub(r"\s+", " ", name.lower()).strip(" -|:.")


def extract_game_key(team1: str, team2: str) -> str:
    """Create a canonical game key from two team names, sorted for consistency."""
    t1, t2 = normalize_team(team1), normalize_team(team2)
    return "|".join(sorted([t1, t2]))


class OUMarket:
    """Parsed O/U market info."""
    __slots__ = ("market", "game_key", "ou_line", "price", "team1", "team2")

    def __init__(self, market, game_key: str, ou_line: float, price: float,
                 team1: str, team2: str):
        self.market = market
        self.game_key = game_key
        self.ou_line = ou_line
        self.price = price
        self.team1 = team1
        self.team2 = team2


class SpreadMarket:
    """Parsed spread market info."""
    __slots__ = ("market", "spread_team", "spread_value", "price", "game_key")

    def __init__(self, market, spread_team: str, spread_value: float,
                 price: float, game_key: str | None = None):
        self.market = market
        self.spread_team = spread_team
        self.spread_value = spread_value
        self.price = price
        self.game_key = game_key


def parse_ou_market(market) -> OUMarket | None:
    """Parse a market question into an OUMarket, or None if not an NHL O/U market."""
    q = getattr(market, "question", "")
    p = getattr(market, "current_probability", None)
    if not isinstance(p, (int, float)):
        return None
    if _NON_NHL.search(q):
        return None
    if not _NHL_INDICATOR.search(q):
        return None

    m = _OU_PATTERN.search(q)
    if not m:
        return None

    team1 = m.group(1).strip()
    team2 = m.group(2).strip()
    ou_line = float(m.group(3))
    game_key = extract_game_key(team1, team2)

    return OUMarket(
        market=market,
        game_key=game_key,
        ou_line=ou_line,
        price=float(p),
        team1=normalize_team(team1),
        team2=normalize_team(team2),
    )


def parse_spread_market(market) -> SpreadMarket | None:
    """Parse a market question into a SpreadMarket, or None if not an NHL spread."""
    q = getattr(market, "question", "")
    p = getattr(market, "current_probability", None)
    if not isinstance(p, (int, float)):
        return None
    if _NON_NHL.search(q):
        return None
    if not _NHL_INDICATOR.search(q):
        return None

    m = _SPREAD_PATTERN.search(q)
    if not m:
        return None

    spread_team = normalize_team(m.group(1))
    spread_value = float(m.group(2))

    # Try to extract game_key from a "vs" pattern in the full question
    game_key = None
    vs = _VS_PATTERN.search(q)
    if vs:
        game_key = extract_game_key(vs.group(1).strip(), vs.group(2).strip())

    return SpreadMarket(
        market=market,
        spread_team=spread_team,
        spread_value=spread_value,
        price=float(p),
        game_key=game_key,
    )


# ---------------------------------------------------------------------------
# Ladder grouping and consistency checks
# ---------------------------------------------------------------------------

class GameLadder:
    """All O/U markets and spread markets for a single NHL game."""
    def __init__(self, game_key: str):
        self.game_key = game_key
        self.ou_markets: list[OUMarket] = []
        self.spread_markets: list[SpreadMarket] = []

    def add_ou(self, ou: OUMarket) -> None:
        self.ou_markets.append(ou)

    def add_spread(self, sp: SpreadMarket) -> None:
        self.spread_markets.append(sp)

    @property
    def market_count(self) -> int:
        return len(self.ou_markets) + len(self.spread_markets)


def build_ladders(ou_markets: list[OUMarket], spread_markets: list[SpreadMarket]) -> dict[str, GameLadder]:
    """Group O/U and spread markets by game key into ladders."""
    ladders: dict[str, GameLadder] = {}

    for ou in ou_markets:
        if ou.game_key not in ladders:
            ladders[ou.game_key] = GameLadder(ou.game_key)
        ladders[ou.game_key].add_ou(ou)

    # Match spread markets to games by team name overlap
    for sp in spread_markets:
        matched = False
        if sp.game_key and sp.game_key in ladders:
            ladders[sp.game_key].add_spread(sp)
            matched = True
        else:
            # Try to match by team name overlap
            for gk, ladder in ladders.items():
                if sp.spread_team in gk or any(
                    t in sp.spread_team for t in gk.split("|")
                ):
                    ladder.add_spread(sp)
                    matched = True
                    break
        # If no match but we have a game_key, create a new ladder
        if not matched and sp.game_key:
            ladders[sp.game_key] = GameLadder(sp.game_key)
            ladders[sp.game_key].add_spread(sp)

    return ladders


def find_violations(ladders: dict[str, GameLadder]) -> list[tuple]:
    """
    Check each game ladder for:
    1. O/U monotonicity violations: P(OVER lower line) >= P(OVER higher line)
    2. Spread-vs-O/U consistency: large spread implies scoring profile

    Returns list of (market, side, violation_magnitude, reasoning).
    """
    opportunities: list[tuple] = []

    for game_key, ladder in ladders.items():
        # --- Check 1: O/U monotonicity ---
        if len(ladder.ou_markets) >= 2:
            sorted_ou = sorted(ladder.ou_markets, key=lambda x: x.ou_line)
            for i in range(len(sorted_ou) - 1):
                lo = sorted_ou[i]      # lower line (e.g., O/U 4.5)
                hi = sorted_ou[i + 1]  # higher line (e.g., O/U 5.5)

                # P(OVER lower line) must >= P(OVER higher line)
                # If hi.price > lo.price, the curve is broken
                violation = hi.price - lo.price
                if violation > MIN_VIOLATION:
                    # The higher-line OVER is overpriced -- sell NO on it
                    opportunities.append((
                        hi.market, "no", violation,
                        f"Monotonicity: P(O/U {hi.ou_line} OVER)={hi.price:.1%} > "
                        f"P(O/U {lo.ou_line} OVER)={lo.price:.1%} | "
                        f"violation={violation:.1%} -- {hi.market.question[:55]}"
                    ))
                    # The lower-line OVER is underpriced -- buy YES on it
                    opportunities.append((
                        lo.market, "yes", violation,
                        f"Monotonicity: P(O/U {lo.ou_line} OVER)={lo.price:.1%} < "
                        f"P(O/U {hi.ou_line} OVER)={hi.price:.1%} | "
                        f"violation={violation:.1%} -- {lo.market.question[:55]}"
                    ))

            # Check non-adjacent pairs for larger violations
            for i in range(len(sorted_ou)):
                for j in range(i + 2, len(sorted_ou)):
                    lo = sorted_ou[i]
                    hi = sorted_ou[j]
                    violation = hi.price - lo.price
                    if violation > MIN_VIOLATION:
                        # Only add if not already covered by adjacent pair
                        # with a larger violation
                        opportunities.append((
                            hi.market, "no", violation,
                            f"Ladder break: P(O/U {hi.ou_line} OVER)={hi.price:.1%} > "
                            f"P(O/U {lo.ou_line} OVER)={lo.price:.1%} | "
                            f"gap={violation:.1%} -- {hi.market.question[:55]}"
                        ))
                        opportunities.append((
                            lo.market, "yes", violation,
                            f"Ladder break: P(O/U {lo.ou_line} OVER)={lo.price:.1%} < "
                            f"P(O/U {hi.ou_line} OVER)={hi.price:.1%} | "
                            f"gap={violation:.1%} -- {lo.market.question[:55]}"
                        ))

        # --- Check 2: Spread-vs-O/U consistency ---
        # If spread is large (one team heavily favored), the expected total
        # score distribution shifts. A large negative spread (e.g., -2.5)
        # means one team is expected to score significantly more, which
        # typically pushes the total higher.
        #
        # Heuristic: if |spread| >= 2.5, the O/U midpoint should be at
        # least 5.5 (i.e., P(O/U 5.5 OVER) should be >= 0.40).
        # If |spread| >= 1.5, P(O/U 4.5 OVER) should be >= 0.50.
        if ladder.spread_markets and ladder.ou_markets:
            max_spread_abs = max(abs(sp.spread_value) for sp in ladder.spread_markets)
            ou_by_line = {ou.ou_line: ou for ou in ladder.ou_markets}

            if max_spread_abs >= 2.5:
                # Large spread -- expect higher total
                ou_55 = ou_by_line.get(5.5)
                if ou_55 and ou_55.price < 0.35:
                    violation = 0.40 - ou_55.price
                    if violation > MIN_VIOLATION:
                        opportunities.append((
                            ou_55.market, "yes", violation,
                            f"Spread/O/U: spread={max_spread_abs:.1f} implies higher total "
                            f"but O/U 5.5 OVER only {ou_55.price:.1%} | "
                            f"gap={violation:.1%} -- {ou_55.market.question[:55]}"
                        ))

            if max_spread_abs >= 1.5:
                ou_45 = ou_by_line.get(4.5)
                if ou_45 and ou_45.price < 0.40:
                    violation = 0.50 - ou_45.price
                    if violation > MIN_VIOLATION:
                        opportunities.append((
                            ou_45.market, "yes", violation,
                            f"Spread/O/U: spread={max_spread_abs:.1f} implies O/U 4.5 OVER "
                            f">= 50% but only {ou_45.price:.1%} | "
                            f"gap={violation:.1%} -- {ou_45.market.question[:55]}"
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

    Conviction scales with the magnitude of the ladder violation.
    Threshold gates (YES_THRESHOLD / NO_THRESHOLD) still apply as hard limits.
    """
    ok, why = valid_market(market)
    if not ok:
        return None, 0, why

    if not opportunity:
        return None, 0, "No ladder violation found"

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
            safe_print(f"  [warn] {w}")
    except Exception as e:
        safe_print(f"  [ctx] {market_id}: {e}")
    return True, "ok"


def find_markets(client: SimmerClient) -> list:
    """Find active NHL hockey markets, deduplicated."""
    seen: set[str] = set()
    unique: list = []

    _KEEP = re.compile(r"vs\.|vs |Spread|O/U", re.I)

    for kw in KEYWORDS:
        try:
            for m in client.find_markets(query=kw):
                market_id = getattr(m, "id", None)
                if market_id and market_id not in seen:
                    q = getattr(m, "question", "")
                    if _NHL_INDICATOR.search(q) and not _NON_NHL.search(q) and _KEEP.search(q):
                        seen.add(market_id)
                        unique.append(m)
        except Exception as e:
            safe_print(f"[search] {kw!r}: {e}")

    # Fallback: broad sweep if keyword search yields few results
    if len(unique) < 5:
        try:
            for m in client.get_markets(limit=200):
                market_id = getattr(m, "id", None)
                if market_id and market_id not in seen:
                    q = getattr(m, "question", "")
                    if _NHL_INDICATOR.search(q) and not _NON_NHL.search(q) and _KEEP.search(q):
                        seen.add(market_id)
                        unique.append(m)
        except Exception as e:
            safe_print(f"[fallback] get_markets: {e}")

    return unique


def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    safe_print(f"[ladder-nhl-hockey] mode={mode} max_pos=${MAX_POSITION} "
               f"min_violation={MIN_VIOLATION:.0%}")

    client = get_client(live=live)
    markets = find_markets(client)
    safe_print(f"[ladder-nhl-hockey] {len(markets)} candidate markets")

    # Parse all markets into O/U and spread categories
    ou_markets: list[OUMarket] = []
    spread_markets: list[SpreadMarket] = []

    for m in markets:
        ou = parse_ou_market(m)
        if ou:
            ou_markets.append(ou)
            continue
        sp = parse_spread_market(m)
        if sp:
            spread_markets.append(sp)

    safe_print(f"[ladder-nhl-hockey] {len(ou_markets)} O/U markets, "
               f"{len(spread_markets)} spread markets")

    # Group into ladders by game
    ladders = build_ladders(ou_markets, spread_markets)
    safe_print(f"[ladder-nhl-hockey] {len(ladders)} game ladders found:")

    # Log each ladder structure
    for game_key, ladder in ladders.items():
        parts = []
        for ou in sorted(ladder.ou_markets, key=lambda x: x.ou_line):
            parts.append(f"O/U {ou.ou_line}={ou.price:.1%}")
        for sp in ladder.spread_markets:
            parts.append(f"Spread({sp.spread_team} {sp.spread_value})={sp.price:.1%}")
        safe_print(f"  [{game_key}] {' | '.join(parts)}")

    # Find ladder violations
    all_opps: dict[str, tuple] = {}
    violations = find_violations(ladders)
    for market, side, mag, reason in violations:
        mid = getattr(market, "id", None)
        if not mid:
            continue
        existing = all_opps.get(mid)
        if existing is None or mag > existing[2]:
            all_opps[mid] = (market, side, mag, reason)

    safe_print(f"[ladder-nhl-hockey] {len(all_opps)} violation opportunities")

    # Execute trades on the largest violations first
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

    safe_print(f"[ladder-nhl-hockey] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Trades monotonicity violations in NHL hockey O/U market ladders "
                    "and spread-vs-total consistency on Polymarket."
    )
    ap.add_argument(
        "--live",
        action="store_true",
        help="Real trades on Polymarket. Default is paper (sim) mode.",
    )
    run(live=ap.parse_args().live)
