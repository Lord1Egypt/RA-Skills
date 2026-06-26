"""
polymarket-bundle-dota2-props-trader
Trades bundle inconsistencies across correlated Dota 2 match props (kills O/U,
roshan, barracks, rampage, first blood, ultra kill, daytime) on Polymarket.

Core edge: A single Dota 2 match spawns 28+ prop markets that are fundamentally
correlated. High-kill games have more roshan fights, more barracks destroyed,
more rampages. When the kills O/U market implies a high-action game (60% over
50.5 kills) but "Both Teams Beat Roshan?" sits at 30%, that is a bundle
inconsistency -- the props disagree on the game's action level. This skill
detects these inconsistencies and trades the outlier prop toward the consensus.

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

TRADE_SOURCE = "sdk:polymarket-bundle-dota2-props-trader"
SKILL_SLUG   = "polymarket-bundle-dota2-props-trader"

KEYWORDS = [
    'Dota', 'kills', 'roshan', 'barracks', 'rampage',
    'first blood', 'ultra kill', 'daytime', 'BO3', 'ESL',
]

# Risk parameters -- declared as tunables in clawhub.json, adjustable from Simmer UI.
MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  "40"))
MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    "3000"))
MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.10"))
MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      "0"))
MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "10"))
YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.38"))
NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",  "0.62"))
MIN_TRADE      = float(os.environ.get("SIMMER_MIN_TRADE",     "5"))
# Minimum inconsistency magnitude to trade (prevents noise trades)
MIN_INCONSISTENCY = float(os.environ.get("SIMMER_MIN_INCONSISTENCY", "0.10"))

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
# Market parsing -- extract match_key, game_number, prop_type, prop_value
# ---------------------------------------------------------------------------

# Dota 2 indicator -- must match to be considered
_DOTA_INDICATOR = re.compile(
    r"dota|dota\s*2|the\s+international|dreamleague|esl.*dota|dpc|"
    r"roshan|barracks|rampage|ultra\s*kill|first\s*blood|"
    r"aegis|ancient|tower|mega\s*creep",
    re.I,
)

# Non-Dota noise
_NON_DOTA = re.compile(
    r"bitcoin|ethereum|btc|eth|crypto|price|stock|token|coin|nft|"
    r"election|president|congress|senate|weather|temperature|"
    r"counter[\s-]?strike|cs2|csgo|valorant|league\s+of\s+legends|lol",
    re.I,
)

# Kill threshold: "Total Kills Over/Under 50.5", "Kills O/U 47.5"
_KILLS_RE = re.compile(
    r"(?:total\s+)?kills?\s+(?:O/U|over[/ ]?under)\s+([\d]+(?:\.[\d]+)?)",
    re.I,
)
_KILLS_RE_ALT = re.compile(
    r"(?:O/U|over[/ ]?under)\s+([\d]+(?:\.[\d]+)?)\s+(?:total\s+)?kills?",
    re.I,
)

# Boolean props
_ROSHAN_RE = re.compile(r"roshan|aegis", re.I)
_BARRACKS_RE = re.compile(r"barracks|rax", re.I)
_RAMPAGE_RE = re.compile(r"rampage", re.I)
_FIRST_BLOOD_RE = re.compile(r"first\s*blood", re.I)
_ULTRA_KILL_RE = re.compile(r"ultra\s*kill", re.I)
_DAYTIME_RE = re.compile(r"daytime|day\s*time|night\s*time|day[\s/]night", re.I)

# Game number: "Game 1", "Game 2", "Map 1"
_GAME_NUM_RE = re.compile(r"(?:game|map)\s+(\d+)", re.I)

# Match key: team names / event prefix
_MATCH_PREFIX_RE = re.compile(
    r"^(.*?)(?:\s*[-|:]\s*)?(?:total\s+kills|kills?\s+(?:O/U|over)|"
    r"O/U\s+[\d.]+|roshan|barracks|rampage|first\s*blood|ultra\s*kill|daytime|day[\s/]night)",
    re.I,
)


def is_dota_prop_market(question: str) -> bool:
    """Return True if the question looks like a Dota 2 prop market."""
    if _NON_DOTA.search(question):
        return False
    if not _DOTA_INDICATOR.search(question):
        return False
    # Must be a recognizable prop type
    q = question.lower()
    return any([
        _KILLS_RE.search(question) or _KILLS_RE_ALT.search(question),
        _ROSHAN_RE.search(question),
        _BARRACKS_RE.search(question),
        _RAMPAGE_RE.search(question),
        _FIRST_BLOOD_RE.search(question),
        _ULTRA_KILL_RE.search(question),
        _DAYTIME_RE.search(question),
    ])


def parse_prop(question: str) -> tuple[str, float | None]:
    """
    Return (prop_type, prop_value) from a Dota 2 market question.
    prop_type: "kills_ou", "roshan", "barracks", "rampage", "first_blood",
               "ultra_kill", "daytime"
    prop_value: the O/U threshold for kills_ou, None for boolean props.
    """
    m = _KILLS_RE.search(question)
    if m:
        return "kills_ou", float(m.group(1))
    m = _KILLS_RE_ALT.search(question)
    if m:
        return "kills_ou", float(m.group(1))
    if _ROSHAN_RE.search(question):
        return "roshan", None
    if _BARRACKS_RE.search(question):
        return "barracks", None
    if _RAMPAGE_RE.search(question):
        return "rampage", None
    if _FIRST_BLOOD_RE.search(question):
        return "first_blood", None
    if _ULTRA_KILL_RE.search(question):
        return "ultra_kill", None
    if _DAYTIME_RE.search(question):
        return "daytime", None
    return "unknown", None


def parse_game_number(question: str) -> int:
    """Extract game/map number, default 0 for match-level markets."""
    m = _GAME_NUM_RE.search(question)
    return int(m.group(1)) if m else 0


def parse_match_key(question: str, market=None) -> str:
    """Extract a normalized match identifier from the question."""
    m = _MATCH_PREFIX_RE.search(question)
    if m:
        raw = m.group(1).strip()
        raw = _GAME_NUM_RE.sub("", raw)
        key = re.sub(r"\s+", " ", raw.lower()).strip(" -|:,")
        if len(key) >= 3:
            return key

    if market is not None:
        for attr in ("event_slug", "group_slug", "import_source", "event_id"):
            val = getattr(market, attr, None)
            if val and isinstance(val, str) and len(val) >= 3:
                return val.lower().strip()

    return "unknown_match"


# ---------------------------------------------------------------------------
# Bundle grouping and action-score inconsistency detection
# ---------------------------------------------------------------------------

class PropMarket:
    """One parsed Dota 2 prop market."""
    __slots__ = ("market", "match_key", "game_number", "prop_type",
                 "prop_value", "p", "question")

    def __init__(self, market, match_key, game_number, prop_type, prop_value):
        self.market = market
        self.match_key = match_key
        self.game_number = game_number
        self.prop_type = prop_type
        self.prop_value = prop_value
        self.p = float(market.current_probability)
        self.question = getattr(market, "question", "")


# Expected action-score direction for each boolean prop.
# "high_action" means: if game is high-action, this prop's YES probability should be HIGH.
# "low_action" means: if game is high-action, this prop's YES probability should be LOW.
PROP_ACTION_DIRECTION = {
    "roshan":     "high_action",   # More kills = more teamfights = more roshan contests
    "barracks":   "high_action",   # More kills = more pushing power = more barracks destroyed
    "rampage":    "high_action",   # More kills = more chances for a 5-kill spree
    "ultra_kill": "high_action",   # More kills = more chances for 4-kill spree
    "first_blood": "high_action",  # High-action games have early aggression
    "daytime":    "low_action",    # High-action games tend to extend into nighttime phases
}


def compute_action_score(props: list[PropMarket]) -> float | None:
    """
    Compute an action score (0.0 = low action, 1.0 = high action) from the
    kills O/U markets in the bundle. If no kills O/U market exists, return None.

    Logic: Higher kills O/U probability = higher expected kill total = high action.
    We use the highest-threshold kills market that has p > 0.40 as the anchor.
    """
    kills_markets = [pm for pm in props if pm.prop_type == "kills_ou"]
    if not kills_markets:
        return None

    # Use the highest-threshold kills market as the action signal
    kills_markets.sort(key=lambda pm: pm.prop_value or 0, reverse=True)

    # Weighted average of kills probabilities, higher thresholds weighted more
    total_weight = 0.0
    weighted_p = 0.0
    for km in kills_markets:
        # Weight by threshold level (higher threshold = more informative about action)
        w = (km.prop_value or 50) / 50.0
        weighted_p += km.p * w
        total_weight += w

    if total_weight == 0:
        return None

    return weighted_p / total_weight


def find_inconsistencies(props: list[PropMarket],
                         action_score: float) -> list[tuple]:
    """
    Compare each boolean prop's probability against the action score.
    If the action score says "high action" but a high_action prop is priced low
    (or vice versa), that's an inconsistency.

    Returns list of (PropMarket, expected_direction, inconsistency_magnitude, reasoning).
    expected_direction: "higher" or "lower" -- which way the prop should move.
    """
    results = []

    for pm in props:
        if pm.prop_type == "kills_ou":
            continue  # kills markets define the action score, not traded here
        if pm.prop_type not in PROP_ACTION_DIRECTION:
            continue

        direction = PROP_ACTION_DIRECTION[pm.prop_type]

        if direction == "high_action":
            # High-action game -> this prop should be HIGH
            # Action score 0.6 means 60% action -> expected prop ~0.55-0.65
            expected_p = 0.30 + action_score * 0.40  # range 0.30 to 0.70
            gap = expected_p - pm.p

            if gap > MIN_INCONSISTENCY:
                # Prop is too LOW for the action level -> buy YES
                results.append((
                    pm, "higher", gap,
                    f"INCONSISTENT: {pm.prop_type} at {pm.p:.0%} but action={action_score:.0%} "
                    f"expects ~{expected_p:.0%} (gap={gap:.0%}) -- {pm.question[:55]}"
                ))
            elif gap < -MIN_INCONSISTENCY:
                # Prop is too HIGH for the action level -> sell NO
                results.append((
                    pm, "lower", abs(gap),
                    f"INCONSISTENT: {pm.prop_type} at {pm.p:.0%} but action={action_score:.0%} "
                    f"expects ~{expected_p:.0%} (gap={gap:.0%}) -- {pm.question[:55]}"
                ))

        elif direction == "low_action":
            # High-action game -> this prop should be LOW (inverted)
            expected_p = 0.70 - action_score * 0.40  # range 0.70 to 0.30
            gap = expected_p - pm.p

            if gap > MIN_INCONSISTENCY:
                results.append((
                    pm, "higher", gap,
                    f"INCONSISTENT: {pm.prop_type} at {pm.p:.0%} but action={action_score:.0%} "
                    f"expects ~{expected_p:.0%} (gap={gap:.0%}) -- {pm.question[:55]}"
                ))
            elif gap < -MIN_INCONSISTENCY:
                results.append((
                    pm, "lower", abs(gap),
                    f"INCONSISTENT: {pm.prop_type} at {pm.p:.0%} but action={action_score:.0%} "
                    f"expects ~{expected_p:.0%} (gap={gap:.0%}) -- {pm.question[:55]}"
                ))

    return results


def compute_signal(market, inconsistency: tuple | None = None) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    When called with an inconsistency tuple, uses the inconsistency magnitude
    for conviction scaling. When called standalone, uses standard threshold logic.
    """
    p = market.current_probability
    q = market.question

    # Spread gate
    if market.spread_cents is not None and market.spread_cents / 100 > MAX_SPREAD:
        return None, 0, f"Spread {market.spread_cents/100:.1%} > {MAX_SPREAD:.1%}"

    # Days-to-resolution gate
    if market.resolves_at:
        try:
            resolves = datetime.fromisoformat(market.resolves_at.replace("Z", "+00:00"))
            days = (resolves - datetime.now(timezone.utc)).days
            if days < MIN_DAYS:
                return None, 0, f"Only {days}d to resolve"
        except Exception:
            pass

    # If we have an inconsistency signal, use it
    if inconsistency:
        pm, expected_dir, magnitude, reason = inconsistency

        if expected_dir == "higher":
            # Prop should be higher -> buy YES
            if p > YES_THRESHOLD:
                # Still trade if inconsistency is large enough
                if magnitude < MIN_INCONSISTENCY * 2:
                    return None, 0, f"YES blocked at {p:.1%}; threshold is {YES_THRESHOLD:.0%}"
            conviction = min(1.0, magnitude / 0.30)  # 30% gap = full conviction
            size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
            return "yes", size, reason

        elif expected_dir == "lower":
            # Prop should be lower -> sell NO
            if p < NO_THRESHOLD:
                if magnitude < MIN_INCONSISTENCY * 2:
                    return None, 0, f"NO blocked at {p:.1%}; threshold is {NO_THRESHOLD:.0%}"
            conviction = min(1.0, magnitude / 0.30)
            size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
            return "no", size, reason

    # Standard threshold logic (fallback)
    if p <= YES_THRESHOLD:
        conviction = (YES_THRESHOLD - p) / YES_THRESHOLD
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = YES_THRESHOLD - p
        return "yes", size, f"YES {p:.0%} edge={edge:.0%} size=${size} -- {q[:70]}"

    if p >= NO_THRESHOLD:
        conviction = (p - NO_THRESHOLD) / (1 - NO_THRESHOLD)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = p - NO_THRESHOLD
        return "no", size, f"NO YES={p:.0%} edge={edge:.0%} size=${size} -- {q[:70]}"

    return None, 0, f"Neutral at {p:.1%} (outside {YES_THRESHOLD:.0%}/{NO_THRESHOLD:.0%} bands)"


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
    Find active Dota 2 prop markets via keyword search + bulk fetch fallback,
    deduplicated. Uses get_markets(limit=200) as primary discovery since Dota
    markets are often missed by find_markets keyword search.
    """
    seen: set[str] = set()
    unique: list = []

    # Bulk fetch FIRST -- Dota markets often missed by keyword search
    try:
        for m in client.get_markets(limit=200):
            market_id = getattr(m, "id", None)
            if market_id and market_id not in seen:
                q = getattr(m, "question", "")
                if is_dota_prop_market(q):
                    seen.add(market_id)
                    unique.append(m)
    except Exception as e:
        safe_print(f"[bulk-fetch] {e}")

    # Keyword search as supplement
    for kw in KEYWORDS:
        try:
            for m in client.find_markets(query=kw):
                market_id = getattr(m, "id", None)
                if market_id and market_id not in seen:
                    q = getattr(m, "question", "")
                    if is_dota_prop_market(q):
                        seen.add(market_id)
                        unique.append(m)
        except Exception as e:
            safe_print(f"[search] {kw!r}: {e}")

    return unique


def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    safe_print(
        f"[bundle-dota2-props] mode={mode} max_pos=${MAX_POSITION} "
        f"min_inconsistency={MIN_INCONSISTENCY:.0%}"
    )

    client = get_client(live=live)
    markets = find_markets(client)
    safe_print(f"[bundle-dota2-props] {len(markets)} candidate Dota 2 prop markets")

    # Parse and group by (match_key, game_number)
    bundles: dict[str, list[PropMarket]] = {}
    for m in markets:
        q = getattr(m, "question", "")
        p = getattr(m, "current_probability", None)
        if not isinstance(p, (int, float)):
            continue

        prop_type, prop_value = parse_prop(q)
        if prop_type == "unknown":
            continue

        match_key = parse_match_key(q, market=m)
        game_number = parse_game_number(q)
        bundle_key = f"{match_key}|game{game_number}"

        pm = PropMarket(m, match_key, game_number, prop_type, prop_value)
        bundles.setdefault(bundle_key, []).append(pm)

    safe_print(f"[bundle-dota2-props] {len(bundles)} match bundles")

    # Log each bundle's structure
    for bundle_key, props in bundles.items():
        prop_summary = ", ".join(
            f"{pm.prop_type}{'=' + str(pm.prop_value) if pm.prop_value else ''}={pm.p:.0%}"
            for pm in props
        )
        safe_print(f"  [{bundle_key}] {len(props)} props: {prop_summary}")

    # Find inconsistencies across all bundles
    all_opps: list[tuple] = []
    for bundle_key, props in bundles.items():
        if len(props) < 2:
            continue

        action_score = compute_action_score(props)
        if action_score is None:
            safe_print(f"  [{bundle_key}] no kills O/U anchor -- skip")
            continue

        safe_print(f"  [{bundle_key}] action_score={action_score:.0%}")

        inconsistencies = find_inconsistencies(props, action_score)
        for inc in inconsistencies:
            all_opps.append(inc)

    safe_print(f"[bundle-dota2-props] {len(all_opps)} inconsistency opportunities")

    # Sort by magnitude descending and trade
    all_opps.sort(key=lambda x: -x[2])

    placed = 0
    for opp in all_opps:
        if placed >= MAX_POSITIONS:
            break

        pm = opp[0]
        side, size, reasoning = compute_signal(pm.market, opp)
        if not side:
            safe_print(f"  [skip] {reasoning}")
            continue

        ok, why = context_ok(client, pm.market.id)
        if not ok:
            safe_print(f"  [skip] {why}")
            continue

        try:
            r = client.trade(
                market_id=pm.market.id,
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
            safe_print(f"  [error] {pm.market.id}: {e}")

    safe_print(f"[bundle-dota2-props] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Trades bundle inconsistencies across correlated Dota 2 match props on Polymarket."
    )
    ap.add_argument(
        "--live",
        action="store_true",
        help="Real trades on Polymarket. Default is paper (sim) mode.",
    )
    run(live=ap.parse_args().live)
