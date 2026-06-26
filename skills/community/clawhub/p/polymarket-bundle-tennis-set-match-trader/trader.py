"""
polymarket-bundle-tennis-set-match-trader
Trades cross-market constraint violations in tennis Set 1 O/U, Match O/U,
Total Sets O/U, Set Handicap, and Set/Match Winner bundles on Polymarket.

Core edge: Tennis matches have structural constraints across prop markets.
Match total >= Set 1 total always, so P(Match O/U X OVER) >= P(Set 1 O/U X
OVER). Total Sets O/U 2.5 constrains set handicap pricing. When these
constraints are violated, it is structural arbitrage.

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

TRADE_SOURCE = "sdk:polymarket-bundle-tennis-set-match-trader"
SKILL_SLUG   = "polymarket-bundle-tennis-set-match-trader"

KEYWORDS = [
    'tennis', 'Set 1', 'Match O/U', 'Total Sets', 'Set Handicap',
    'Sabalenka', 'Gauff', 'Garcia', 'Sherif', 'Djokovic', 'Alcaraz',
    'WTA', 'ATP', 'Miami Open',
]

# Risk parameters -- declared as tunables in clawhub.json, adjustable from Simmer UI.
MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  "40"))
MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    "3000"))
MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.08"))
MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      "1"))
MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "8"))
YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.38"))
NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",  "0.62"))
MIN_TRADE      = float(os.environ.get("SIMMER_MIN_TRADE",     "5"))
# Minimum constraint violation magnitude to trade
MIN_VIOLATION  = float(os.environ.get("SIMMER_MIN_VIOLATION",  "0.03"))

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
# Market parsing -- extract match_key, prop_type, line_value
# ---------------------------------------------------------------------------

# "Player A vs Player B: Set 1 Games O/U 9.5"
_SET1_OU = re.compile(
    r"(.+?)\s*[:|-]\s*Set\s*1\s+Games?\s+(?:O/U|Over[/ ]?Under)\s+([\d]+(?:\.[\d]+)?)",
    re.I,
)

# "Player A vs Player B: Match O/U 21.5" or "Match Games O/U 21.5"
_MATCH_OU = re.compile(
    r"(.+?)\s*[:|-]\s*Match\s+(?:Games?\s+)?(?:O/U|Over[/ ]?Under)\s+([\d]+(?:\.[\d]+)?)",
    re.I,
)

# "Player A vs Player B: Total Sets O/U 2.5"
_TOTAL_SETS = re.compile(
    r"(.+?)\s*[:|-]\s*Total\s+Sets?\s+(?:O/U|Over[/ ]?Under)\s+([\d]+(?:\.[\d]+)?)",
    re.I,
)

# "Set Handicap: Player A (-1.5) vs Player B (+1.5)"
_SET_HANDICAP = re.compile(
    r"(?:Set\s+Handicap\s*[:|-])?\s*(.+?)\s*\(\s*(-?\d+(?:\.\d+)?)\s*\)\s*vs\.?\s*(.+?)\s*\(\s*([+-]?\d+(?:\.\d+)?)\s*\)",
    re.I,
)

# "Player A vs Player B: Set Winner" or "Set 1 Winner"
_SET_WINNER = re.compile(
    r"(.+?)\s*[:|-]\s*Set\s*\d*\s*Winner",
    re.I,
)

# "Player A vs Player B" or "Player A vs. Player B"
_MATCH_KEY = re.compile(
    r"(.+?)\s+vs\.?\s+(.+?)(?:\s*[:|-]|\s*$)",
    re.I,
)

# Tennis indicators
_TENNIS_INDICATOR = re.compile(
    r"tennis|set\s*1|match\s+(?:games?\s+)?o/u|total\s+sets|set\s+handicap|"
    r"sabalenka|gauff|garcia|sherif|djokovic|alcaraz|sinner|medvedev|"
    r"swiatek|rybakina|pegula|zheng|wta|atp|miami\s+open|"
    r"roland\s+garros|wimbledon|us\s+open|australian\s+open|"
    r"grand\s+slam|games\s+o/u|set\s+winner",
    re.I,
)

_NON_TENNIS = re.compile(
    r"bitcoin|ethereum|btc|eth|crypto|price|stock|token|coin|nft|"
    r"election|president|congress|senate|weather|temperature|"
    r"dota|counter-strike|cs2|overwatch|valorant|league\s+of\s+legends",
    re.I,
)


def normalize_match_key(text: str) -> str:
    """Normalize a match key from player names."""
    text = text.strip().lower()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[:\-|,]+$", "", text).strip()
    # Sort player names for consistent keying regardless of order
    m = re.match(r"(.+?)\s+vs\.?\s+(.+)", text)
    if m:
        players = sorted([m.group(1).strip(), m.group(2).strip()])
        return f"{players[0]} vs {players[1]}"
    return text


def parse_market(question: str, market=None):
    """
    Parse a tennis market question and return (match_key, prop_type, line_value)
    or None if not a tennis bundle market.

    prop_type: 'set1_ou', 'match_ou', 'total_sets', 'set_handicap', 'set_winner'
    """
    if _NON_TENNIS.search(question):
        return None
    if not _TENNIS_INDICATOR.search(question):
        return None

    # Try Set 1 Games O/U
    m = _SET1_OU.search(question)
    if m:
        key = normalize_match_key(m.group(1))
        return (key, "set1_ou", float(m.group(2)))

    # Try Match O/U
    m = _MATCH_OU.search(question)
    if m:
        key = normalize_match_key(m.group(1))
        return (key, "match_ou", float(m.group(2)))

    # Try Total Sets O/U
    m = _TOTAL_SETS.search(question)
    if m:
        key = normalize_match_key(m.group(1))
        return (key, "total_sets", float(m.group(2)))

    # Try Set Handicap
    m = _SET_HANDICAP.search(question)
    if m:
        p1 = m.group(1).strip()
        p2 = m.group(3).strip()
        key = normalize_match_key(f"{p1} vs {p2}")
        handicap = float(m.group(2))
        return (key, "set_handicap", handicap)

    # Try Set Winner
    m = _SET_WINNER.search(question)
    if m:
        key = normalize_match_key(m.group(1))
        return (key, "set_winner", 0)

    return None


# ---------------------------------------------------------------------------
# Bundle construction and constraint checking
# ---------------------------------------------------------------------------

class BundleMarket:
    """One market mapped to a tennis prop bundle."""
    __slots__ = ("market", "match_key", "prop_type", "line_value", "price")

    def __init__(self, market, match_key: str, prop_type: str, line_value: float, price: float):
        self.market = market
        self.match_key = match_key
        self.prop_type = prop_type
        self.line_value = line_value
        self.price = price


def build_bundles(markets: list) -> dict[str, list[BundleMarket]]:
    """Group markets into bundles keyed by match_key."""
    bundles: dict[str, list[BundleMarket]] = {}
    for m in markets:
        q = getattr(m, "question", "")
        p = getattr(m, "current_probability", None)
        if not isinstance(p, (int, float)):
            continue

        parsed = parse_market(q, market=m)
        if parsed is None:
            continue

        match_key, prop_type, line_value = parsed
        bm = BundleMarket(m, match_key, prop_type, line_value, float(p))
        bundles.setdefault(match_key, []).append(bm)

    return bundles


def find_violations(bundles: dict[str, list[BundleMarket]]) -> list[tuple]:
    """
    Check each bundle for constraint violations:

    1. Match O/U X OVER >= Set 1 O/U X OVER (for same line X)
       Match total always >= Set 1 total, so this must hold.

    2. If Total Sets O/U 2.5 > 50% (likely 3 sets), Set Handicap -1.5
       should price lower (underdog more likely to win a set).

    Returns list of (market, side, violation_magnitude, reasoning).
    """
    opportunities: list[tuple] = []

    for match_key, props in bundles.items():
        if len(props) < 2:
            continue

        # Index by prop type and line
        set1_ou: dict[float, BundleMarket] = {}
        match_ou: dict[float, BundleMarket] = {}
        total_sets: BundleMarket | None = None
        set_handicap: BundleMarket | None = None

        for bm in props:
            if bm.prop_type == "set1_ou":
                set1_ou[bm.line_value] = bm
            elif bm.prop_type == "match_ou":
                match_ou[bm.line_value] = bm
            elif bm.prop_type == "total_sets":
                total_sets = bm
            elif bm.prop_type == "set_handicap":
                set_handicap = bm

        # Constraint 1: P(Match O/U X OVER) >= P(Set 1 O/U X OVER) for same X
        for line, set1_bm in set1_ou.items():
            if line in match_ou:
                match_bm = match_ou[line]
                # Match OVER should be >= Set 1 OVER
                violation = set1_bm.price - match_bm.price
                if violation > MIN_VIOLATION:
                    # Set 1 O/U is overpriced relative to Match O/U
                    opportunities.append((
                        set1_bm.market, "no", violation,
                        f"\U0001F3BE\U0001F517 Set1 O/U {line} OVER={set1_bm.price:.1%} > "
                        f"Match O/U {line} OVER={match_bm.price:.1%} | "
                        f"violation={violation:.1%} -- {set1_bm.market.question[:55]}"
                    ))
                    # Match O/U is underpriced
                    opportunities.append((
                        match_bm.market, "yes", violation,
                        f"\U0001F3BE\U0001F517 Match O/U {line} OVER={match_bm.price:.1%} < "
                        f"Set1 O/U {line} OVER={set1_bm.price:.1%} | "
                        f"violation={violation:.1%} -- {match_bm.market.question[:55]}"
                    ))

        # Constraint 2: Total Sets O/U 2.5 vs Set Handicap consistency
        if total_sets is not None and set_handicap is not None:
            ts_price = total_sets.price
            sh_price = set_handicap.price

            # If Total Sets O/U 2.5 OVER > 50% => likely 3 sets => underdog
            # wins at least one set => set handicap -1.5 favourite should be
            # lower (harder to cover -1.5 when match likely goes 3 sets)
            if ts_price > 0.50:
                # 3-set match likely: handicap -1.5 should be < (1 - ts_price)
                # because covering -1.5 means winning 2-0 in sets
                expected_straight_sets = 1.0 - ts_price  # P(2-0 finish)
                if sh_price > expected_straight_sets + MIN_VIOLATION:
                    violation = sh_price - expected_straight_sets
                    opportunities.append((
                        set_handicap.market, "no", violation,
                        f"\U0001F3BE\U0001F517 Set Hcap -1.5={sh_price:.1%} but "
                        f"P(straight sets)={expected_straight_sets:.1%} from "
                        f"Total Sets O/U 2.5={ts_price:.1%} | "
                        f"violation={violation:.1%} -- {set_handicap.market.question[:55]}"
                    ))
            elif ts_price < 0.50:
                # 2-set match likely: handicap -1.5 should be high
                expected_straight_sets = 1.0 - ts_price
                if sh_price < expected_straight_sets - MIN_VIOLATION:
                    violation = expected_straight_sets - sh_price
                    opportunities.append((
                        set_handicap.market, "yes", violation,
                        f"\U0001F3BE\U0001F517 Set Hcap -1.5={sh_price:.1%} but "
                        f"P(straight sets)={expected_straight_sets:.1%} from "
                        f"Total Sets O/U 2.5={ts_price:.1%} | "
                        f"violation={violation:.1%} -- {set_handicap.market.question[:55]}"
                    ))

    return opportunities


# ---------------------------------------------------------------------------
# Signal, safeguards, execution
# ---------------------------------------------------------------------------

def compute_signal(market, opportunity: tuple | None) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    Conviction scales with the magnitude of the bundle constraint violation.
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
        return None, 0, "No bundle violation found"

    _, side, violation_mag, reason = opportunity

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
    """
    Find active tennis bundle markets via keyword search + bulk fetch fallback,
    deduplicated.
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
                    if parse_market(q, market=m) is not None:
                        seen.add(market_id)
                        unique.append(m)
        except Exception as e:
            safe_print(f"[search] {kw!r}: {e}")

    # Bulk fallback
    try:
        for m in client.get_markets(limit=200):
            market_id = getattr(m, "id", None)
            if market_id and market_id not in seen:
                q = getattr(m, "question", "")
                if parse_market(q, market=m) is not None:
                    seen.add(market_id)
                    unique.append(m)
    except Exception as e:
        safe_print(f"[bulk-fetch] {e}")

    return unique


def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    safe_print(
        f"[bundle-tennis-set-match] mode={mode} max_pos=${MAX_POSITION} "
        f"min_violation={MIN_VIOLATION:.0%}"
    )

    client = get_client(live=live)
    markets = find_markets(client)
    safe_print(f"[bundle-tennis-set-match] {len(markets)} candidate markets")

    # Build bundles by match
    bundles = build_bundles(markets)
    safe_print(
        f"[bundle-tennis-set-match] {len(bundles)} bundles: "
        + ", ".join(f"{k}({len(v)} props)" for k, v in bundles.items())
    )

    # Log each bundle's structure
    for match_key, props in bundles.items():
        safe_print(f"  [{match_key}] props: " + ", ".join(
            f"{bm.prop_type}({bm.line_value})={bm.price:.1%}" for bm in props
        ))

    # Find violations across all bundles
    all_opps: dict[str, tuple] = {}
    violations = find_violations(bundles)
    for market, side, mag, reason in violations:
        mid = getattr(market, "id", None)
        if not mid:
            continue
        existing = all_opps.get(mid)
        if existing is None or mag > existing[2]:
            all_opps[mid] = (market, side, mag, reason)

    safe_print(f"[bundle-tennis-set-match] {len(all_opps)} violation opportunities")

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

    safe_print(f"[bundle-tennis-set-match] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Trades tennis Set 1 / Match O/U / Total Sets / Set Handicap constraint violations on Polymarket."
    )
    ap.add_argument(
        "--live",
        action="store_true",
        help="Real trades on Polymarket. Default is paper (sim) mode.",
    )
    run(live=ap.parse_args().live)
