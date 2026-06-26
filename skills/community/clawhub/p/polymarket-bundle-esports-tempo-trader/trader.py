"""
polymarket-bundle-esports-tempo-trader
Trades tempo inconsistencies across Dota2/esports game props -- first blood,
kills O/U, daytime ending, ultra kill, and rampage -- on Polymarket.

Core edge: Within the same Dota2/esports game, first blood timing correlates
with overall kill pace. If first blood is expected (high p), kills O/U should
also be high. If "Ends in Daytime" is high probability, that implies a fast
stompy game which correlates with lower total kills. Rampage/ultra kill should
correlate with high kills. Inconsistencies between tempo indicators are
structural mispricings.

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

TRADE_SOURCE = "sdk:polymarket-bundle-esports-tempo-trader"
SKILL_SLUG   = "polymarket-bundle-esports-tempo-trader"

KEYWORDS = [
    'first blood', 'daytime', 'kills', 'rampage', 'ultra kill',
    'Dota', 'Game 1', 'Game 2', 'Game 3',
]

# Risk parameters -- declared as tunables in clawhub.json, adjustable from Simmer UI.
MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  "40"))
MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    "3000"))
MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.08"))
MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      "0"))
MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "8"))
YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.38"))
NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",  "0.62"))
MIN_TRADE      = float(os.environ.get("SIMMER_MIN_TRADE",     "5"))
# Minimum tempo inconsistency magnitude to trade
MIN_VIOLATION  = float(os.environ.get("SIMMER_MIN_VIOLATION",  "0.04"))

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
# Market parsing -- extract (match_key, game_number, prop_type, line_value)
# ---------------------------------------------------------------------------

# "Team A vs Team B Game 1: First Blood" or "First Blood - Game 1"
_FIRST_BLOOD = re.compile(
    r"first\s+blood",
    re.I,
)

# "Ends in Daytime" / "Game Ends in Daytime" / "Daytime Ending"
_DAYTIME = re.compile(
    r"(?:ends?\s+in\s+)?daytime|daytime\s+ending",
    re.I,
)

# "Total Kills O/U 47.5" / "Kills Over/Under 50.5"
_KILLS_OU = re.compile(
    r"(?:total\s+)?kills?\s+(?:O/U|over[/ ]?under)\s+([\d]+(?:\.[\d]+)?)",
    re.I,
)
_KILLS_OU_ALT = re.compile(
    r"(?:O/U|over[/ ]?under)\s+([\d]+(?:\.[\d]+)?)\s+(?:total\s+)?kills?",
    re.I,
)

# "Rampage" (5-kill streak in Dota2)
_RAMPAGE = re.compile(
    r"\brampage\b",
    re.I,
)

# "Ultra Kill" (4-kill streak in Dota2)
_ULTRA_KILL = re.compile(
    r"ultra\s*kill",
    re.I,
)

# Game number: "Game 1", "Game 2", "Map 1"
_GAME_NUM = re.compile(
    r"(?:game|map)\s+(\d+)",
    re.I,
)

# Match prefix for key extraction
_MATCH_PREFIX = re.compile(
    r"^(.*?)(?:\s*[-|:]\s*)?(?:first\s+blood|daytime|kills?\s+(?:O/U|over)|"
    r"O/U\s+[\d.]+\s+(?:total\s+)?kills|rampage|ultra\s*kill|game\s+\d+)",
    re.I,
)

# Esports indicators
_ESPORTS_INDICATOR = re.compile(
    r"dota|dota\s*2|counter[\s-]?strike|cs2|overwatch|valorant|league\s+of\s+legends|"
    r"esport|first\s+blood|daytime|kills?\s+(?:over|under|O/U)|total\s+kills|"
    r"rampage|ultra\s*kill|"
    r"bo[135]|best\s+of\s+[135]|game\s+[123]|map\s+[123]|"
    r"blast|esl|dreamleague|the\s+international|dpc",
    re.I,
)

_NON_ESPORTS = re.compile(
    r"bitcoin|ethereum|btc|eth|crypto|price|stock|token|coin|nft|"
    r"election|president|congress|senate|weather|temperature|"
    r"tennis|nba|nfl|mlb|nhl|soccer|football",
    re.I,
)


def parse_game_number(question: str) -> int:
    """Extract game/map number, default 0 for match-level markets."""
    m = _GAME_NUM.search(question)
    return int(m.group(1)) if m else 0


def parse_match_key(question: str, market=None) -> str:
    """Extract a normalized match identifier."""
    m = _MATCH_PREFIX.search(question)
    if m:
        raw = m.group(1).strip()
        raw = _GAME_NUM.sub("", raw)
        key = re.sub(r"\s+", " ", raw.lower()).strip(" -|:,")
        if len(key) >= 3:
            return key

    if market is not None:
        for attr in ("event_slug", "group_slug", "import_source", "event_id"):
            val = getattr(market, attr, None)
            if val and isinstance(val, str) and len(val) >= 3:
                return val.lower().strip()

    return "unknown_match"


def parse_prop_type(question: str):
    """
    Determine the prop type from the question.
    Returns (prop_type, line_value) or None.
    prop_type: 'first_blood', 'daytime', 'kills_ou', 'rampage', 'ultra_kill'
    """
    q = question

    if _FIRST_BLOOD.search(q):
        return ("first_blood", 0)

    if _DAYTIME.search(q):
        return ("daytime", 0)

    m = _KILLS_OU.search(q)
    if m:
        return ("kills_ou", float(m.group(1)))
    m = _KILLS_OU_ALT.search(q)
    if m:
        return ("kills_ou", float(m.group(1)))

    if _RAMPAGE.search(q):
        return ("rampage", 0)

    if _ULTRA_KILL.search(q):
        return ("ultra_kill", 0)

    return None


def is_esports_tempo_market(question: str) -> bool:
    """Return True if the question looks like an esports tempo prop market."""
    if _NON_ESPORTS.search(question):
        return False
    if not _ESPORTS_INDICATOR.search(question):
        return False
    return parse_prop_type(question) is not None


# ---------------------------------------------------------------------------
# Bundle construction and tempo analysis
# ---------------------------------------------------------------------------

class TempoMarket:
    """One market mapped to a tempo prop bundle."""
    __slots__ = ("market", "match_key", "game_number", "prop_type", "line_value", "price")

    def __init__(self, market, match_key: str, game_number: int,
                 prop_type: str, line_value: float, price: float):
        self.market = market
        self.match_key = match_key
        self.game_number = game_number
        self.prop_type = prop_type
        self.line_value = line_value
        self.price = price


def build_bundles(markets: list) -> dict[str, list[TempoMarket]]:
    """Group markets into tempo bundles keyed by (match_key, game_number)."""
    bundles: dict[str, list[TempoMarket]] = {}
    for m in markets:
        q = getattr(m, "question", "")
        p = getattr(m, "current_probability", None)
        if not isinstance(p, (int, float)):
            continue

        if not is_esports_tempo_market(q):
            continue

        prop = parse_prop_type(q)
        if prop is None:
            continue

        prop_type, line_value = prop
        match_key = parse_match_key(q, market=m)
        game_number = parse_game_number(q)
        key = f"{match_key}|game{game_number}"
        tm = TempoMarket(m, match_key, game_number, prop_type, line_value, float(p))
        bundles.setdefault(key, []).append(tm)

    return bundles


def compute_tempo_score(props: list[TempoMarket]) -> dict:
    """
    Compute a tempo consensus from the available props.

    Returns a dict with:
      - 'aggressive_signals': count of props suggesting fast/aggressive game
      - 'passive_signals': count of props suggesting slow/passive game
      - 'tempo': float between 0 (passive) and 1 (aggressive)
      - props by type for detailed analysis
    """
    by_type: dict[str, list[TempoMarket]] = {}
    for tm in props:
        by_type.setdefault(tm.prop_type, []).append(tm)

    aggressive = 0.0
    passive = 0.0
    total_indicators = 0

    # First blood: high p => early aggression => aggressive tempo
    for fb in by_type.get("first_blood", []):
        total_indicators += 1
        if fb.price > 0.55:
            aggressive += fb.price
        else:
            passive += (1.0 - fb.price)

    # Kills O/U: higher line with high p => more kills => aggressive
    for ko in by_type.get("kills_ou", []):
        total_indicators += 1
        if ko.price > 0.50:
            aggressive += ko.price * 0.8  # weight slightly less
        else:
            passive += (1.0 - ko.price) * 0.8

    # Daytime ending: high p => fast/stompy game => aggressive tempo
    # BUT fast games = fewer total kills (game ends before late teamfights)
    for dt in by_type.get("daytime", []):
        total_indicators += 1
        if dt.price > 0.50:
            aggressive += dt.price * 0.6  # fast game signal
        else:
            passive += (1.0 - dt.price) * 0.6

    # Rampage: high p => one-sided game => aggressive tempo, high kills
    for rp in by_type.get("rampage", []):
        total_indicators += 1
        if rp.price > 0.40:
            aggressive += rp.price
        else:
            passive += (1.0 - rp.price)

    # Ultra kill: similar to rampage
    for uk in by_type.get("ultra_kill", []):
        total_indicators += 1
        if uk.price > 0.40:
            aggressive += uk.price
        else:
            passive += (1.0 - uk.price)

    total = aggressive + passive
    tempo = aggressive / total if total > 0 else 0.5

    return {
        "aggressive_signals": aggressive,
        "passive_signals": passive,
        "tempo": tempo,
        "total_indicators": total_indicators,
        "by_type": by_type,
    }


def find_violations(bundles: dict[str, list[TempoMarket]]) -> list[tuple]:
    """
    Find tempo inconsistencies within each bundle.

    Key checks:
    1. Daytime ending high + kills O/U high => inconsistent
       (fast game should have LOWER total kills)
    2. First blood high + kills O/U low => inconsistent
       (early aggression correlates with more kills)
    3. Rampage/ultra kill high + kills O/U low => inconsistent
       (multi-kills require high overall kill count)
    4. Trade the prop that deviates most from the tempo consensus.

    Returns list of (market, side, violation_magnitude, reasoning).
    """
    opportunities: list[tuple] = []

    for bundle_key, props in bundles.items():
        if len(props) < 2:
            continue

        tempo_data = compute_tempo_score(props)
        by_type = tempo_data["by_type"]
        if tempo_data["total_indicators"] < 2:
            continue

        # Check 1: Daytime high + Kills O/U high => inconsistency
        # Daytime = fast game => fewer total kills expected
        for dt in by_type.get("daytime", []):
            if dt.price > 0.55:
                # Fast game expected -- kills should be lower
                for ko in by_type.get("kills_ou", []):
                    if ko.price > 0.55:
                        # Both high -- inconsistent
                        violation = min(dt.price, ko.price) - 0.50
                        if violation > MIN_VIOLATION:
                            # Kills O/U OVER is the weaker signal -- sell it
                            opportunities.append((
                                ko.market, "no", violation,
                                f"\u26A1\U0001F3AE Kills O/U {ko.line_value} OVER={ko.price:.1%} "
                                f"but Daytime={dt.price:.1%} (fast game = fewer kills) | "
                                f"violation={violation:.1%} -- {ko.market.question[:55]}"
                            ))
            elif dt.price < 0.40:
                # Slow game expected -- kills should be higher
                for ko in by_type.get("kills_ou", []):
                    if ko.price < 0.40:
                        # Both low -- inconsistent (slow game still has kills)
                        violation = 0.50 - max(dt.price, ko.price)
                        if violation > MIN_VIOLATION:
                            opportunities.append((
                                ko.market, "yes", violation,
                                f"\u26A1\U0001F3AE Kills O/U {ko.line_value} OVER={ko.price:.1%} "
                                f"but Daytime={dt.price:.1%} (slow game = more teamfights) | "
                                f"violation={violation:.1%} -- {ko.market.question[:55]}"
                            ))

        # Check 2: First blood high + Kills O/U low => inconsistency
        for fb in by_type.get("first_blood", []):
            for ko in by_type.get("kills_ou", []):
                if fb.price > 0.60 and ko.price < 0.40:
                    # Early first blood but low kills expected -- contradictory
                    violation = (fb.price - 0.50) - (0.50 - ko.price)
                    violation = abs(fb.price - ko.price) - 0.15
                    if violation > MIN_VIOLATION:
                        opportunities.append((
                            ko.market, "yes", violation,
                            f"\u26A1\U0001F3AE Kills O/U {ko.line_value} OVER={ko.price:.1%} "
                            f"but FirstBlood={fb.price:.1%} (early aggro = more kills) | "
                            f"violation={violation:.1%} -- {ko.market.question[:55]}"
                        ))
                elif fb.price < 0.35 and ko.price > 0.65:
                    # No first blood expected but high kills -- contradictory
                    violation = abs(ko.price - fb.price) - 0.15
                    if violation > MIN_VIOLATION:
                        opportunities.append((
                            ko.market, "no", violation,
                            f"\u26A1\U0001F3AE Kills O/U {ko.line_value} OVER={ko.price:.1%} "
                            f"but FirstBlood={fb.price:.1%} (passive early = fewer kills) | "
                            f"violation={violation:.1%} -- {ko.market.question[:55]}"
                        ))

        # Check 3: Rampage/Ultra Kill high + Kills O/U low => inconsistency
        for multi_type in ("rampage", "ultra_kill"):
            label = "Rampage" if multi_type == "rampage" else "UltraKill"
            for mk in by_type.get(multi_type, []):
                for ko in by_type.get("kills_ou", []):
                    if mk.price > 0.50 and ko.price < 0.40:
                        # Multi-kill likely but low total kills -- contradictory
                        violation = mk.price - ko.price - 0.10
                        if violation > MIN_VIOLATION:
                            opportunities.append((
                                ko.market, "yes", violation,
                                f"\u26A1\U0001F3AE Kills O/U {ko.line_value} OVER={ko.price:.1%} "
                                f"but {label}={mk.price:.1%} (multi-kills need high kills) | "
                                f"violation={violation:.1%} -- {ko.market.question[:55]}"
                            ))
                    elif mk.price > 0.50 and ko.price > 0.70:
                        pass  # consistent -- high kills, high multi-kill chance
                    elif mk.price < 0.25 and ko.price > 0.65:
                        # No multi-kill but high total kills -- less contradictory
                        # but still tradeable if gap is large
                        violation = ko.price - mk.price - 0.30
                        if violation > MIN_VIOLATION:
                            opportunities.append((
                                mk.market, "yes", violation,
                                f"\u26A1\U0001F3AE {label}={mk.price:.1%} "
                                f"but Kills O/U {ko.line_value} OVER={ko.price:.1%} "
                                f"(high kills = more multi-kill chances) | "
                                f"violation={violation:.1%} -- {mk.market.question[:55]}"
                            ))

    return opportunities


# ---------------------------------------------------------------------------
# Signal, safeguards, execution
# ---------------------------------------------------------------------------

def compute_signal(market, opportunity: tuple | None) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    Conviction scales with the magnitude of the tempo inconsistency.
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
        return None, 0, "No tempo inconsistency found"

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
    Find active esports tempo markets via keyword search + bulk fetch fallback,
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
                    if is_esports_tempo_market(q):
                        seen.add(market_id)
                        unique.append(m)
        except Exception as e:
            safe_print(f"[search] {kw!r}: {e}")

    # Bulk fallback -- primary discovery since many tempo props are not easily keyword-matched
    try:
        for m in client.get_markets(limit=200):
            market_id = getattr(m, "id", None)
            if market_id and market_id not in seen:
                q = getattr(m, "question", "")
                if is_esports_tempo_market(q):
                    seen.add(market_id)
                    unique.append(m)
    except Exception as e:
        safe_print(f"[bulk-fetch] {e}")

    return unique


def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    safe_print(
        f"[bundle-esports-tempo] mode={mode} max_pos=${MAX_POSITION} "
        f"min_violation={MIN_VIOLATION:.0%}"
    )

    client = get_client(live=live)
    markets = find_markets(client)
    safe_print(f"[bundle-esports-tempo] {len(markets)} candidate markets")

    # Build tempo bundles by (match, game)
    bundles = build_bundles(markets)
    safe_print(
        f"[bundle-esports-tempo] {len(bundles)} bundles: "
        + ", ".join(f"{k}({len(v)} props)" for k, v in bundles.items())
    )

    # Log each bundle's structure
    for bundle_key, props in bundles.items():
        safe_print(f"  [{bundle_key}] props: " + ", ".join(
            f"{tm.prop_type}({tm.line_value})={tm.price:.1%}" for tm in props
        ))
        tempo = compute_tempo_score(props)
        safe_print(f"    tempo={tempo['tempo']:.2f} "
                   f"(aggressive={tempo['aggressive_signals']:.2f} "
                   f"passive={tempo['passive_signals']:.2f})")

    # Find tempo inconsistencies across all bundles
    all_opps: dict[str, tuple] = {}
    violations = find_violations(bundles)
    for market, side, mag, reason in violations:
        mid = getattr(market, "id", None)
        if not mid:
            continue
        existing = all_opps.get(mid)
        if existing is None or mag > existing[2]:
            all_opps[mid] = (market, side, mag, reason)

    safe_print(f"[bundle-esports-tempo] {len(all_opps)} tempo inconsistency opportunities")

    # Execute trades on largest inconsistencies
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

    safe_print(f"[bundle-esports-tempo] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Trades tempo inconsistencies across Dota2/esports game props on Polymarket."
    )
    ap.add_argument(
        "--live",
        action="store_true",
        help="Real trades on Polymarket. Default is paper (sim) mode.",
    )
    run(live=ap.parse_args().live)
