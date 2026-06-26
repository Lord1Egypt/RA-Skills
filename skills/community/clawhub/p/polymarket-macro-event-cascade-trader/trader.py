"""
polymarket-macro-event-cascade-trader
When a major event resolves on Polymarket, it creates second and third-order
effects that take hours to price in.  Example: Iran ceasefire resolves YES ->
(1st order) geopolitics markets reprice immediately -> (2nd order) oil drops,
BTC rises -> (3rd order) equity markets rise.  This skill trades the 2nd and
3rd order effects BEFORE they are fully priced.

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

TRADE_SOURCE = "sdk:polymarket-macro-event-cascade-trader"
SKILL_SLUG   = "polymarket-macro-event-cascade-trader"

# --------------- risk / signal tunables ---------------
MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  "40"))
MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    "10000"))
MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.07"))
MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      "3"))
MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "6"))
YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.38"))
NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",  "0.62"))
MIN_TRADE      = float(os.environ.get("SIMMER_MIN_TRADE",     "5"))
CASCADE_LAG    = float(os.environ.get("SIMMER_CASCADE_LAG",   "0.08"))

_client: SimmerClient | None = None


# --------------- helpers ---------------

def safe_print(*args, **kwargs):
    """Windows-safe print that replaces unencodable chars."""
    try:
        print(*args, **kwargs)
    except UnicodeEncodeError:
        text = " ".join(str(a) for a in args)
        print(text.encode(sys.stdout.encoding or "utf-8", errors="replace").decode(), **kwargs)


def get_client(live: bool = False) -> SimmerClient:
    global _client, MAX_POSITION, MIN_VOLUME, MAX_SPREAD, MIN_DAYS, MAX_POSITIONS
    global YES_THRESHOLD, NO_THRESHOLD, MIN_TRADE, CASCADE_LAG
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
        CASCADE_LAG    = float(os.environ.get("SIMMER_CASCADE_LAG",   str(CASCADE_LAG)))
    return _client


# --------------- event classification ---------------

EVENT_CATEGORIES = {
    "geopolitics": re.compile(
        r"(iran|israel|gaza|lebanon|ceasefire|war\b|military|strike|troops|invasion"
        r"|ukraine|russia|nato|china|taiwan|sanctions|tariff|peace\s+deal|summit"
        r"|diplomacy|nuclear|missile|bomb)", re.I
    ),
    "crypto": re.compile(
        r"(bitcoin|btc|ethereum|eth|crypto|solana|sol|altcoin|defi|nft"
        r"|binance|coinbase|stablecoin|usdt|usdc)", re.I
    ),
    "commodity": re.compile(
        r"(oil|wti|crude|brent|natural\s+gas|gold|silver|copper|wheat"
        r"|corn|soybean|commodity|opec|barrel)", re.I
    ),
    "health": re.compile(
        r"(pandemic|covid|vaccine|who\b|outbreak|virus|flu|epidemic"
        r"|fda|drug\s+approval|clinical\s+trial)", re.I
    ),
    "weather": re.compile(
        r"(hurricane|tornado|flood|drought|wildfire|temperature|heat\s+wave"
        r"|cold\s+snap|storm|cyclone|typhoon|el\s+nino|la\s+nina)", re.I
    ),
    "equity": re.compile(
        r"(s&p|nasdaq|dow|stock|equity|market\s+crash|recession|fed\s+rate"
        r"|interest\s+rate|gdp|inflation|unemployment|earnings)", re.I
    ),
}

# Cascade chains: when a trigger_category event resolves in a direction,
# these target categories move accordingly.
# Format: (trigger_category, trigger_direction) -> [(target_category, target_direction)]
CASCADE_CHAINS = {
    ("geopolitics", "escalation"):   [("commodity", "up"), ("crypto", "down"), ("equity", "down")],
    ("geopolitics", "deescalation"): [("commodity", "down"), ("crypto", "up"), ("equity", "up")],
    ("crypto", "up"):                [("equity", "up")],
    ("crypto", "down"):              [("equity", "down")],
    ("weather", "extreme"):          [("commodity", "up")],
    ("health", "outbreak"):          [("equity", "down"), ("commodity", "up")],
}

ESCALATION_WORDS = re.compile(
    r"(war|strike|attack|bomb|invasion|troops|military\s+action|escalat|missile|offensive)", re.I
)
DEESCALATION_WORDS = re.compile(
    r"(ceasefire|peace|truce|withdrawal|de-escalat|surrender|armistice|deal|agreement)", re.I
)


def classify_market(question: str) -> str | None:
    """Return the primary category for a market question."""
    for cat, pat in EVENT_CATEGORIES.items():
        if pat.search(question):
            return cat
    return None


def is_nearly_resolved(market) -> tuple[bool, str]:
    """Check if a market is nearly resolved (p > 0.90, p < 0.10, or resolves within 24h)."""
    p = getattr(market, "current_probability", None)
    if not isinstance(p, (int, float)):
        return False, "no probability"

    if p > 0.90:
        return True, "near_yes"
    if p < 0.10:
        return True, "near_no"

    resolves_at = getattr(market, "resolves_at", None)
    if resolves_at:
        try:
            resolves = datetime.fromisoformat(resolves_at.replace("Z", "+00:00"))
            hours = (resolves - datetime.now(timezone.utc)).total_seconds() / 3600
            if 0 < hours < 24:
                if p > 0.50:
                    return True, "near_yes"
                else:
                    return True, "near_no"
        except Exception:
            pass

    return False, "not near resolution"


def detect_geo_direction(question: str) -> str | None:
    """For geopolitics markets, detect escalation vs deescalation."""
    if DEESCALATION_WORDS.search(question):
        return "deescalation"
    if ESCALATION_WORDS.search(question):
        return "escalation"
    return None


def determine_trigger_signal(market) -> tuple[str, str] | None:
    """
    Determine what cascade signal a nearly-resolved market emits.
    Returns (trigger_key_category, trigger_key_direction) or None.
    """
    q = getattr(market, "question", "")
    p = getattr(market, "current_probability", 0.5)
    cat = classify_market(q)
    if not cat:
        return None

    resolving_yes = p > 0.50

    if cat == "geopolitics":
        geo_dir = detect_geo_direction(q)
        if geo_dir == "escalation":
            return ("geopolitics", "escalation") if resolving_yes else ("geopolitics", "deescalation")
        if geo_dir == "deescalation":
            return ("geopolitics", "deescalation") if resolving_yes else ("geopolitics", "escalation")
        # Ambiguous geo — skip
        return None
    elif cat == "crypto":
        return ("crypto", "up") if resolving_yes else ("crypto", "down")
    elif cat == "weather":
        return ("weather", "extreme") if resolving_yes else None
    elif cat == "health":
        return ("health", "outbreak") if resolving_yes else None

    return None


# --------------- market validation ---------------

def valid_market(market) -> tuple[bool, str]:
    """Standard market quality gates."""
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


def should_move_direction(target_direction: str) -> str:
    """Map cascade direction to trade side.
    'up' means we expect the market probability to rise -> buy YES when it's low.
    'down' means we expect probability to drop -> buy NO when it's high.
    """
    if target_direction == "up":
        return "yes"
    return "no"


# --------------- compute signal ---------------

def compute_signal(market, cascade_side: str, lag: float) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) using conviction-based sizing.
    cascade_side: 'yes' or 'no' — the direction the cascade implies.
    lag: how much the market lags behind expected repricing.
    """
    p = getattr(market, "current_probability", None)
    q = getattr(market, "question", "")

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

    if cascade_side == "yes" and p <= YES_THRESHOLD:
        conviction = (YES_THRESHOLD - p) / YES_THRESHOLD
        # Boost conviction by cascade lag magnitude
        conviction = min(1.0, conviction + lag)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = YES_THRESHOLD - p
        return "yes", size, f"YES {p:.0%} edge={edge:.0%} lag={lag:.0%} size=${size} -- {q[:70]}"

    if cascade_side == "no" and p >= NO_THRESHOLD:
        conviction = (p - NO_THRESHOLD) / (1 - NO_THRESHOLD)
        conviction = min(1.0, conviction + lag)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = p - NO_THRESHOLD
        return "no", size, f"NO YES={p:.0%} edge={edge:.0%} lag={lag:.0%} size=${size} -- {q[:70]}"

    return None, 0, f"Neutral at {p:.1%} for cascade_side={cascade_side} (outside bands)"


# --------------- context guard ---------------

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


# --------------- market discovery ---------------

TRIGGER_KEYWORDS = [
    "Iran", "Israel", "ceasefire", "war", "military",
    "Bitcoin", "BTC", "Ethereum", "crypto",
    "oil", "crude", "hurricane", "pandemic",
]


def discover_markets(client: SimmerClient) -> list:
    """Discover markets via get_markets (primary) and keyword search (secondary)."""
    seen, all_markets = set(), []

    # Primary: get_markets
    try:
        for m in client.get_markets(limit=200):
            mid = getattr(m, "id", None)
            if mid and mid not in seen:
                seen.add(mid)
                all_markets.append(m)
    except Exception as e:
        safe_print(f"[get_markets] {e}")

    # Secondary: keyword search for trigger markets
    for kw in TRIGGER_KEYWORDS:
        try:
            for m in client.find_markets(query=kw):
                mid = getattr(m, "id", None)
                if mid and mid not in seen:
                    seen.add(mid)
                    all_markets.append(m)
        except Exception as e:
            safe_print(f"[search] {kw!r}: {e}")

    return all_markets


# --------------- cascade engine ---------------

def find_cascade_opportunities(markets: list) -> list[tuple]:
    """
    1. Identify trigger markets (nearly resolved).
    2. For each trigger, determine cascade chain.
    3. For each cascade target category, find markets in that category.
    4. Check if target has already repriced or is still lagging.
    5. Return list of (target_market, trade_side, lag, reasoning).
    """
    # Classify all markets
    categorized: dict[str, list] = {}
    for m in markets:
        q = getattr(m, "question", "")
        cat = classify_market(q)
        if cat:
            categorized.setdefault(cat, []).append(m)

    # Find trigger events
    triggers = []
    for m in markets:
        near, direction = is_nearly_resolved(m)
        if not near:
            continue
        signal = determine_trigger_signal(m)
        if signal:
            triggers.append((m, signal))

    if not triggers:
        safe_print("[cascade] No nearly-resolved trigger events found")
        return []

    safe_print(f"[cascade] {len(triggers)} trigger events detected")

    opportunities = []
    seen_targets = set()

    for trigger_market, (trig_cat, trig_dir) in triggers:
        chain = CASCADE_CHAINS.get((trig_cat, trig_dir), [])
        if not chain:
            continue

        trig_q = getattr(trigger_market, "question", "")[:60]
        safe_print(f"  [trigger] {trig_cat}/{trig_dir}: {trig_q}")

        for target_cat, target_dir in chain:
            target_markets = categorized.get(target_cat, [])
            trade_side = should_move_direction(target_dir)

            for tm in target_markets:
                tm_id = getattr(tm, "id", None)
                if not tm_id or tm_id == getattr(trigger_market, "id", None):
                    continue
                if tm_id in seen_targets:
                    continue

                ok, why = valid_market(tm)
                if not ok:
                    continue

                p = float(getattr(tm, "current_probability", 0.5))

                # Compute lag: how much the target HASN'T moved yet
                # For 'yes' cascade: target should be moving UP, lag = how far below midpoint
                # For 'no' cascade: target should be moving DOWN, lag = how far above midpoint
                if trade_side == "yes":
                    lag = max(0, 0.50 - p)  # Further below 50% = more lag
                else:
                    lag = max(0, p - 0.50)  # Further above 50% = more lag

                if lag < CASCADE_LAG:
                    continue

                seen_targets.add(tm_id)
                tm_q = getattr(tm, "question", "")[:70]
                reason = (
                    f"Cascade {trig_cat}/{trig_dir} -> {target_cat}/{target_dir} "
                    f"lag={lag:.0%} | trigger: {trig_q} | target: {tm_q}"
                )
                opportunities.append((tm, trade_side, lag, reason))

    return opportunities


# --------------- main loop ---------------

def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    safe_print(
        f"[event-cascade] mode={mode} max_pos=${MAX_POSITION} "
        f"min_vol=${MIN_VOLUME} max_spread={MAX_SPREAD:.0%} min_days={MIN_DAYS} "
        f"cascade_lag={CASCADE_LAG:.0%}"
    )

    client = get_client(live=live)
    markets = discover_markets(client)
    safe_print(f"[event-cascade] {len(markets)} total markets discovered")

    opportunities = find_cascade_opportunities(markets)
    safe_print(f"[event-cascade] {len(opportunities)} cascade opportunities found")

    # Sort by lag descending (biggest lag = biggest opportunity)
    opportunities.sort(key=lambda x: x[2], reverse=True)

    placed = 0
    for target_market, trade_side, lag, reason in opportunities:
        if placed >= MAX_POSITIONS:
            break

        side, size, reasoning = compute_signal(target_market, trade_side, lag)
        if not side:
            safe_print(f"  [skip] {reasoning}")
            continue

        market_id = getattr(target_market, "id", None)
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
            safe_print(f"  [trade] {side.upper()} ${size} {tag} {status} - {reasoning[:110]}")
            if r.success:
                placed += 1
        except Exception as e:
            safe_print(f"  [error] {market_id}: {e}")

    safe_print(f"[event-cascade] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Trades 2nd/3rd order cascade effects from nearly-resolved Polymarket events."
    )
    ap.add_argument(
        "--live",
        action="store_true",
        help="Real trades on Polymarket. Default is paper (sim) mode.",
    )
    run(live=ap.parse_args().live)
