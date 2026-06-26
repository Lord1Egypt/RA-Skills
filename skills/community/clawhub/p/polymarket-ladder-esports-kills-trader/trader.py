"""
polymarket-ladder-esports-kills-trader
Trades monotonicity violations in esports "Total Kills O/U" market ladders
on Polymarket.

Core edge: Dota 2, CS2, and other esports list multiple kill total thresholds
for the same match/game:
    O/U 47.5 = 58%, O/U 48.5 = 55%, O/U 49.5 = 52%, O/U 50.5 = 54%
These MUST be monotonically decreasing — P(Over 47.5) >= P(Over 48.5) >= ...
When they are not, it is structural arbitrage.

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

TRADE_SOURCE = "sdk:polymarket-ladder-esports-kills-trader"
SKILL_SLUG   = "polymarket-ladder-esports-kills-trader"

KEYWORDS = [
    'total kills', 'kills over', 'kills under',
    'Dota', 'Counter-Strike', 'Overwatch',
    'esports', 'BO3', 'game 1', 'game 2', 'game 3',
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
# Market parsing — extract match_key, game_number, kill_threshold
# ---------------------------------------------------------------------------

# Matches "Total Kills Over/Under 47.5", "Kills O/U 50.5", "total kills over under 49.5"
_KILLS_LINE = re.compile(
    r"(?:total\s+kills|kills)\s+(?:O/U|over[/ ]?under)\s+([\d]+(?:\.[\d]+)?)",
    re.I,
)

# Fallback: "Over/Under 47.5 Total Kills", "O/U 50.5 Kills"
_KILLS_LINE_ALT = re.compile(
    r"(?:O/U|over[/ ]?under)\s+([\d]+(?:\.[\d]+)?)\s+(?:total\s+)?kills",
    re.I,
)

# Game number: "Game 1", "Game 2", "Map 1", "Map 2"
_GAME_NUM = re.compile(
    r"(?:game|map)\s+(\d+)",
    re.I,
)

# Match identifier: team names / event before the kills part
_MATCH_PREFIX = re.compile(
    r"^(.*?)(?:\s*[-|:]\s*)?(?:total\s+kills|kills\s+(?:O/U|over)|O/U\s+[\d.]+\s+(?:total\s+)?kills)",
    re.I,
)

# Esports filter — must match at least one esports indicator
_ESPORTS_INDICATOR = re.compile(
    r"dota|counter[\s-]?strike|cs2|csgo|overwatch|valorant|league\s+of\s+legends|"
    r"lol|esport|kills?\s+(?:over|under|O/U)|total\s+kills|"
    r"bo[135]|best\s+of\s+[135]|game\s+[123]|map\s+[123]|"
    r"blast|esl|dreamleague|the\s+international|dpc|hltv|"
    r"vct|masters|owl|cdl|call\s+of\s+duty",
    re.I,
)

# Non-esports noise
_NON_ESPORTS = re.compile(
    r"bitcoin|ethereum|btc|eth|crypto|price|stock|token|coin|nft|"
    r"election|president|congress|senate|weather|temperature",
    re.I,
)


def parse_kill_threshold(question: str) -> float | None:
    """Extract the kill threshold (e.g. 47.5) from a market question."""
    m = _KILLS_LINE.search(question)
    if m:
        return float(m.group(1))
    m = _KILLS_LINE_ALT.search(question)
    if m:
        return float(m.group(1))
    return None


def parse_game_number(question: str) -> int:
    """Extract game/map number, default 0 for match-level markets."""
    m = _GAME_NUM.search(question)
    if m:
        return int(m.group(1))
    return 0


def parse_match_key(question: str, market=None) -> str:
    """Extract a normalized match identifier from the question.

    Falls back to a generic key when the question contains no team/event
    prefix (e.g. "Total Kills Over/Under 52.5 in Game 1?" has no teams).
    In that case we try the market's import_source or id to distinguish
    different matches, or default to 'unknown_match'.
    """
    m = _MATCH_PREFIX.search(question)
    if m:
        raw = m.group(1).strip()
        raw = _GAME_NUM.sub("", raw)
        key = re.sub(r"\s+", " ", raw.lower()).strip(" -|:,")
        if len(key) >= 3:
            return key

    # Fallback: use market metadata to group by parent event
    if market is not None:
        for attr in ("event_slug", "group_slug", "import_source", "event_id"):
            val = getattr(market, attr, None)
            if val and isinstance(val, str) and len(val) >= 3:
                return val.lower().strip()

    # Last resort: group all kills markets without prefix together
    return "unknown_match"


def is_esports_kills_market(question: str) -> bool:
    """Return True if the question looks like an esports kills O/U market."""
    if _NON_ESPORTS.search(question):
        return False
    if not _ESPORTS_INDICATOR.search(question):
        return False
    if parse_kill_threshold(question) is not None:
        return True
    return False


# ---------------------------------------------------------------------------
# Ladder construction and violation detection
# ---------------------------------------------------------------------------

class LadderPoint:
    """One market mapped to a point on the kill total O/U ladder."""
    __slots__ = ("market", "match_key", "game_number", "threshold", "price")

    def __init__(self, market, match_key: str, game_number: int, threshold: float, price: float):
        self.market = market
        self.match_key = match_key
        self.game_number = game_number
        self.threshold = threshold
        self.price = price


def build_ladders(markets: list) -> dict[str, list[LadderPoint]]:
    """
    Group markets into ladders keyed by (match_key, game_number).
    Each ladder contains LadderPoints sorted by kill threshold.
    """
    ladders: dict[str, list[LadderPoint]] = {}
    for m in markets:
        q = getattr(m, "question", "")
        p = getattr(m, "current_probability", None)
        if not isinstance(p, (int, float)):
            continue

        if not is_esports_kills_market(q):
            continue

        threshold = parse_kill_threshold(q)
        match_key = parse_match_key(q, market=m)
        if threshold is None:
            continue

        game_number = parse_game_number(q)
        key = f"{match_key}|game{game_number}"
        point = LadderPoint(m, match_key, game_number, threshold, float(p))
        ladders.setdefault(key, []).append(point)

    return ladders


def find_violations(ladders: dict[str, list[LadderPoint]]) -> list[tuple]:
    """
    Check each ladder for monotonicity violations.
    P(Over X) must decrease as X increases. When a higher threshold has a
    higher OVER probability than a lower threshold, the ladder is broken.

    Returns list of (market, side, violation_magnitude, reasoning).
    """
    opportunities: list[tuple] = []

    for ladder_key, points in ladders.items():
        if len(points) < 2:
            continue

        # Sort by kill threshold ascending
        sorted_pts = sorted(points, key=lambda pt: pt.threshold)

        for i in range(len(sorted_pts) - 1):
            lo_pt = sorted_pts[i]      # lower threshold (e.g. O/U 47.5)
            hi_pt = sorted_pts[i + 1]  # higher threshold (e.g. O/U 48.5)

            # OVER probability should be: lo_pt.price >= hi_pt.price
            # If hi_pt is priced HIGHER than lo_pt, monotonicity is broken
            violation = hi_pt.price - lo_pt.price
            if violation > MIN_VIOLATION:
                # Higher threshold is overpriced (sell NO = bet it won't go over)
                opportunities.append((
                    hi_pt.market, "no", violation,
                    f"Monotonicity break: P(O/U {hi_pt.threshold} OVER)={hi_pt.price:.1%} > "
                    f"P(O/U {lo_pt.threshold} OVER)={lo_pt.price:.1%} | "
                    f"violation={violation:.1%} -- {hi_pt.market.question[:55]}"
                ))
                # Lower threshold is underpriced (buy YES = bet it will go over)
                opportunities.append((
                    lo_pt.market, "yes", violation,
                    f"Monotonicity break: P(O/U {lo_pt.threshold} OVER)={lo_pt.price:.1%} < "
                    f"P(O/U {hi_pt.threshold} OVER)={hi_pt.price:.1%} | "
                    f"violation={violation:.1%} -- {lo_pt.market.question[:55]}"
                ))

    return opportunities


# ---------------------------------------------------------------------------
# Signal, safeguards, execution
# ---------------------------------------------------------------------------

def valid_market(market) -> tuple[bool, str]:
    """Standard spread and time-to-resolution checks."""
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


def discover_markets(client: SimmerClient) -> list:
    """
    Find active esports kills O/U markets via keyword search and bulk fetch,
    deduplicated. Uses both find_markets(query=...) and get_markets(limit=200)
    as fallback since find_markets may miss some.
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
                    if is_esports_kills_market(q):
                        seen.add(market_id)
                        unique.append(m)
        except Exception as e:
            safe_print(f"[search] {kw!r}: {e}")

    # Bulk fallback — scan recent/popular markets for kills O/U we may have missed
    try:
        for m in client.get_markets(limit=200):
            market_id = getattr(m, "id", None)
            if market_id and market_id not in seen:
                q = getattr(m, "question", "")
                if is_esports_kills_market(q):
                    seen.add(market_id)
                    unique.append(m)
    except Exception as e:
        safe_print(f"[bulk-fetch] {e}")

    return unique


def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    safe_print(f"[ladder-esports-kills] mode={mode} max_pos=${MAX_POSITION} min_violation={MIN_VIOLATION:.0%}")

    client = get_client(live=live)
    markets = discover_markets(client)
    safe_print(f"[ladder-esports-kills] {len(markets)} candidate markets")

    # Build kill total O/U ladders
    ladders = build_ladders(markets)
    safe_print(f"[ladder-esports-kills] {len(ladders)} ladders: "
               + ", ".join(f"{k}({len(v)} pts)" for k, v in ladders.items()))

    # Log each ladder's structure
    for ladder_key, points in ladders.items():
        sorted_pts = sorted(points, key=lambda pt: pt.threshold)
        safe_print(f"  [{ladder_key}] thresholds: " + ", ".join(
            f"O/U {pt.threshold}={pt.price:.1%}" for pt in sorted_pts
        ))

    # Find violations across all ladders
    all_opps: dict[str, tuple] = {}
    violations = find_violations(ladders)
    for market, side, mag, reason in violations:
        mid = getattr(market, "id", None)
        if not mid:
            continue
        existing = all_opps.get(mid)
        if existing is None or mag > existing[2]:
            all_opps[mid] = (market, side, mag, reason)

    safe_print(f"[ladder-esports-kills] {len(all_opps)} violation opportunities")

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

    safe_print(f"[ladder-esports-kills] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Trades monotonicity violations in esports Total Kills O/U ladders on Polymarket."
    )
    ap.add_argument(
        "--live",
        action="store_true",
        help="Real trades on Polymarket. Default is paper (sim) mode.",
    )
    run(live=ap.parse_args().live)
