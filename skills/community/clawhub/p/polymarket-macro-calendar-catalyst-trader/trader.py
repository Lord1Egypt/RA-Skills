"""
polymarket-macro-calendar-catalyst-trader
Trades Polymarket prediction markets that resolve near known calendar catalyst
events (FOMC meetings, major tournament finals, geopolitical summits, crypto
halvings/upgrades, space launches). Markets near 50% that resolve during a
catalyst window are underpriced for movement -- they will move sharply one way
or another, but Polymarket prices direction, not volatility.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag (venue="polymarket").
"""
import os
import re
import argparse
from datetime import datetime, timezone, timedelta
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-macro-calendar-catalyst-trader"
SKILL_SLUG   = "polymarket-macro-calendar-catalyst-trader"

# ---------------------------------------------------------------------------
# Known catalyst calendar (updated periodically)
# Each entry: (date, category, description)
# FOMC meetings follow a predictable ~6-week cycle.
# Other catalysts are major known events with predictable dates.
# ---------------------------------------------------------------------------
CATALYST_CALENDAR = [
    # FOMC 2026 meetings (predictable 6-week cycle)
    ("2026-01-28", "fomc", "FOMC January meeting"),
    ("2026-01-29", "fomc", "FOMC January meeting day 2"),
    ("2026-03-18", "fomc", "FOMC March meeting"),
    ("2026-03-19", "fomc", "FOMC March meeting day 2"),
    ("2026-05-06", "fomc", "FOMC May meeting"),
    ("2026-05-07", "fomc", "FOMC May meeting day 2"),
    ("2026-06-17", "fomc", "FOMC June meeting"),
    ("2026-06-18", "fomc", "FOMC June meeting day 2"),
    ("2026-07-29", "fomc", "FOMC July meeting"),
    ("2026-07-30", "fomc", "FOMC July meeting day 2"),
    ("2026-09-16", "fomc", "FOMC September meeting"),
    ("2026-09-17", "fomc", "FOMC September meeting day 2"),
    ("2026-11-04", "fomc", "FOMC November meeting"),
    ("2026-11-05", "fomc", "FOMC November meeting day 2"),
    ("2026-12-16", "fomc", "FOMC December meeting"),
    ("2026-12-17", "fomc", "FOMC December meeting day 2"),

    # Major sports finals (approximate windows -- updated as brackets resolve)
    ("2026-02-08", "sports", "Super Bowl LX"),
    ("2026-06-15", "sports", "NBA Finals window"),
    ("2026-06-20", "sports", "NHL Stanley Cup Finals window"),
    ("2026-06-14", "sports", "FIFA World Cup 2026 opening"),
    ("2026-07-19", "sports", "FIFA World Cup 2026 final"),
    ("2026-10-20", "sports", "MLB World Series window"),
    ("2026-07-06", "sports", "Wimbledon finals window"),
    ("2026-06-07", "sports", "French Open finals window"),
    ("2026-09-13", "sports", "US Open tennis finals window"),

    # Geopolitical summits / deadlines
    ("2026-06-01", "geopolitical", "G7 Summit window"),
    ("2026-09-15", "geopolitical", "UN General Assembly opening"),
    ("2026-11-01", "geopolitical", "COP climate summit window"),
    ("2026-11-03", "geopolitical", "US midterm elections"),

    # Crypto events
    ("2026-04-15", "crypto", "Bitcoin halving anniversary / cycle milestone"),
    ("2026-03-15", "crypto", "Ethereum Pectra upgrade window"),

    # Space launches
    ("2026-06-01", "space", "SpaceX Starship orbital window"),
    ("2026-09-01", "space", "Artemis III launch window"),
]

# Macro directional signals by catalyst category
# When a catalyst is near, which direction do related markets tend to move?
_CATEGORY_DIRECTION_HINTS = {
    "fomc":        None,       # FOMC is genuinely uncertain -- use market-level analysis
    "sports":      "yes",      # Finals tend to resolve (someone wins) -- favorites get confirmed
    "geopolitical": "no",      # Summits often disappoint -- geopolitical markets overprice resolution
    "crypto":      "yes",      # Crypto events historically bullish (halving cycle, upgrades)
    "space":       "yes",      # Space launches have high success rates (SpaceX >95%)
}

# Risk parameters -- declared as tunables in clawhub.json, adjustable from Simmer UI.
MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  "40"))
MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    "5000"))
MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.10"))
MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      "1"))
MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "10"))
YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.38"))
NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",  "0.62"))
MIN_TRADE      = float(os.environ.get("SIMMER_MIN_TRADE",     "5"))

# Catalyst-specific tunables
CATALYST_WINDOW = int(os.environ.get("SIMMER_CATALYST_WINDOW", "3"))
CATALYST_BOOST  = float(os.environ.get("SIMMER_CATALYST_BOOST", "1.25"))
COIL_LOW        = float(os.environ.get("SIMMER_COIL_LOW", "0.40"))
COIL_HIGH       = float(os.environ.get("SIMMER_COIL_HIGH", "0.60"))

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
    global YES_THRESHOLD, NO_THRESHOLD, MIN_TRADE
    global CATALYST_WINDOW, CATALYST_BOOST, COIL_LOW, COIL_HIGH
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
        # Re-read params in case apply_skill_config updated os.environ.
        MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  str(MAX_POSITION)))
        MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    str(MIN_VOLUME)))
        MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    str(MAX_SPREAD)))
        MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      str(MIN_DAYS)))
        MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", str(MAX_POSITIONS)))
        YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD", str(YES_THRESHOLD)))
        NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",  str(NO_THRESHOLD)))
        MIN_TRADE      = float(os.environ.get("SIMMER_MIN_TRADE",     str(MIN_TRADE)))
        CATALYST_WINDOW = int(os.environ.get("SIMMER_CATALYST_WINDOW", str(CATALYST_WINDOW)))
        CATALYST_BOOST  = float(os.environ.get("SIMMER_CATALYST_BOOST", str(CATALYST_BOOST)))
        COIL_LOW        = float(os.environ.get("SIMMER_COIL_LOW", str(COIL_LOW)))
        COIL_HIGH       = float(os.environ.get("SIMMER_COIL_HIGH", str(COIL_HIGH)))
    return _client


# ---------------------------------------------------------------------------
# Catalyst matching
# ---------------------------------------------------------------------------

def _parse_catalyst_dates() -> list[tuple[datetime, str, str]]:
    """Parse the catalyst calendar into (datetime, category, description) tuples."""
    results = []
    for date_str, category, desc in CATALYST_CALENDAR:
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            results.append((dt, category, desc))
        except ValueError:
            continue
    return results


def find_nearby_catalyst(resolves_at: str) -> tuple[str, str, int] | None:
    """
    Check if a market's resolution date falls within CATALYST_WINDOW days
    of any known catalyst event.
    Returns (category, description, days_delta) or None.
    """
    if not resolves_at:
        return None
    try:
        resolve_dt = datetime.fromisoformat(resolves_at.replace("Z", "+00:00"))
    except Exception:
        return None

    catalysts = _parse_catalyst_dates()
    best = None
    best_delta = float("inf")

    for cat_dt, category, desc in catalysts:
        delta = abs((resolve_dt - cat_dt).days)
        if delta <= CATALYST_WINDOW and delta < best_delta:
            best = (category, desc, delta)
            best_delta = delta

    return best


def _keyword_catalyst_match(question: str) -> str | None:
    """
    Fallback: match market question text to catalyst categories even if
    resolution date doesn't align perfectly. Returns category or None.
    """
    q = question.lower()

    if any(w in q for w in ("fomc", "fed rate", "interest rate", "federal reserve",
                             "rate cut", "rate hike", "monetary policy", "powell")):
        return "fomc"
    if any(w in q for w in ("super bowl", "world series", "nba finals", "stanley cup",
                             "world cup", "wimbledon", "us open", "french open",
                             "champions league", "grand slam")):
        return "sports"
    if any(w in q for w in ("g7", "g20", "un general assembly", "cop2", "climate summit",
                             "nato summit", "peace summit", "ceasefire deadline",
                             "election", "midterm", "vote")):
        return "geopolitical"
    if any(w in q for w in ("bitcoin halving", "btc halving", "ethereum upgrade",
                             "eth upgrade", "pectra", "dencun", "crypto upgrade")):
        return "crypto"
    if any(w in q for w in ("spacex", "starship", "artemis", "moon landing",
                             "orbital launch", "rocket launch", "nasa")):
        return "space"

    return None


# ---------------------------------------------------------------------------
# Market discovery
# ---------------------------------------------------------------------------

def find_markets(client: SimmerClient) -> list:
    """
    Discover markets using get_markets(limit=200) as PRIMARY discovery,
    with keyword search as secondary fallback.
    """
    seen, unique = set(), []

    # 1. Primary: broad scan
    try:
        for m in client.get_markets(limit=200):
            mid = getattr(m, "id", None)
            if mid and mid not in seen:
                seen.add(mid)
                unique.append(m)
    except Exception as e:
        safe_print(f"[primary] get_markets: {e}")

    # 2. Secondary: targeted keyword search
    search_terms = [
        'FOMC', 'fed rate', 'Super Bowl', 'World Cup', 'NBA Finals',
        'bitcoin halving', 'SpaceX', 'election', 'G7 summit',
        'rate cut', 'Artemis', 'World Series',
    ]
    for kw in search_terms:
        try:
            for m in client.find_markets(query=kw):
                if m.id not in seen:
                    seen.add(m.id)
                    unique.append(m)
        except Exception as e:
            safe_print(f"[search] {kw!r}: {e}")

    return unique


# ---------------------------------------------------------------------------
# Signal
# ---------------------------------------------------------------------------

def compute_signal(market, catalyst_category: str, catalyst_desc: str,
                   days_to_catalyst: int) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    Conviction-based sizing per CLAUDE.md.
    Markets near 50% (coiled springs) resolving during a catalyst window get
    boosted conviction. The direction hint comes from macro analysis of the
    catalyst category. Markets outside the 50% zone use standard threshold logic.
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
                return None, 0, f"Only {days} days to resolve"
        except Exception:
            pass

    # Get directional hint from catalyst category
    direction_hint = _CATEGORY_DIRECTION_HINTS.get(catalyst_category)

    # --- COILED SPRING: market near 50% resolving during catalyst ---
    is_coiled = COIL_LOW <= p <= COIL_HIGH
    if is_coiled and direction_hint:
        # This market WILL move sharply -- we have a directional signal
        # Distance from 50% gives base conviction, boosted by catalyst proximity
        base_conviction = abs(p - 0.5) / 0.5  # small when near 50%
        # Catalyst boost: closer catalyst = stronger boost
        proximity_factor = 1.0 + (CATALYST_WINDOW - days_to_catalyst) / max(1, CATALYST_WINDOW) * 0.5
        boosted_conviction = min(1.0, max(0.15, base_conviction * CATALYST_BOOST * proximity_factor))
        size = max(MIN_TRADE, round(boosted_conviction * MAX_POSITION, 2))

        if direction_hint == "yes":
            return "yes", size, (
                f"COILED catalyst={catalyst_category} {days_to_catalyst}d "
                f"YES {p:.0%} boost={CATALYST_BOOST}x size=${size} -- {q[:50]}"
            )
        else:
            return "no", size, (
                f"COILED catalyst={catalyst_category} {days_to_catalyst}d "
                f"NO YES={p:.0%} boost={CATALYST_BOOST}x size=${size} -- {q[:50]}"
            )

    # --- STANDARD THRESHOLD: catalyst-adjacent markets outside 50% zone ---
    # Catalyst proximity boosts standard conviction
    if p <= YES_THRESHOLD:
        conviction = (YES_THRESHOLD - p) / YES_THRESHOLD
        conviction = min(1.0, conviction * CATALYST_BOOST)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = YES_THRESHOLD - p
        return "yes", size, (
            f"CATALYST {catalyst_category} {days_to_catalyst}d "
            f"YES {p:.0%} edge={edge:.0%} boost={CATALYST_BOOST}x size=${size} -- {q[:45]}"
        )

    if p >= NO_THRESHOLD:
        conviction = (p - NO_THRESHOLD) / (1 - NO_THRESHOLD)
        conviction = min(1.0, conviction * CATALYST_BOOST)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = p - NO_THRESHOLD
        return "no", size, (
            f"CATALYST {catalyst_category} {days_to_catalyst}d "
            f"NO YES={p:.0%} edge={edge:.0%} boost={CATALYST_BOOST}x size=${size} -- {q[:45]}"
        )

    # Near 50% but no directional hint (e.g., FOMC) -- skip
    if is_coiled and not direction_hint:
        return None, 0, (
            f"Coiled spring near catalyst={catalyst_category} but no directional hint "
            f"at {p:.1%} -- {q[:60]}"
        )

    return None, 0, f"Neutral at {p:.1%} (outside bands, no coil) -- {q[:60]}"


# ---------------------------------------------------------------------------
# Safeguards
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    safe_print(
        f"[calendar-catalyst] mode={mode} max_pos=${MAX_POSITION} "
        f"window={CATALYST_WINDOW}d boost={CATALYST_BOOST}x "
        f"coil=[{COIL_LOW:.0%}-{COIL_HIGH:.0%}]"
    )

    client  = get_client(live=live)
    markets = find_markets(client)
    safe_print(f"[calendar-catalyst] {len(markets)} total markets scanned")

    # Match markets to catalysts
    catalyst_matches = []
    for m in markets:
        q = getattr(m, "question", "")
        resolve_str = getattr(m, "resolves_at", None)

        # Try date-based catalyst match first
        match = find_nearby_catalyst(resolve_str) if resolve_str else None

        # Fallback: keyword-based category match (use resolution date proximity check)
        if not match:
            kw_cat = _keyword_catalyst_match(q)
            if kw_cat and resolve_str:
                # Check if resolution is within a broader window (7 days)
                try:
                    resolve_dt = datetime.fromisoformat(resolve_str.replace("Z", "+00:00"))
                    now = datetime.now(timezone.utc)
                    days_to_resolve = (resolve_dt - now).days
                    if 0 < days_to_resolve <= CATALYST_WINDOW * 3:
                        match = (kw_cat, f"keyword-match: {kw_cat}", min(CATALYST_WINDOW, days_to_resolve))
                except Exception:
                    pass

        if match:
            catalyst_matches.append((m, match[0], match[1], match[2]))

    safe_print(f"[calendar-catalyst] {len(catalyst_matches)} markets near catalyst events")

    if not catalyst_matches:
        safe_print("[calendar-catalyst] no catalyst-adjacent markets found. Done.")
        return

    placed = 0
    for m, cat_category, cat_desc, days_delta in catalyst_matches:
        if placed >= MAX_POSITIONS:
            break

        side, size, reasoning = compute_signal(m, cat_category, cat_desc, days_delta)
        if not side:
            safe_print(f"  [skip] {reasoning}")
            continue

        ok, why = context_ok(client, m.id)
        if not ok:
            safe_print(f"  [skip] {why}")
            continue

        try:
            r = client.trade(
                market_id=m.id,
                side=side,
                amount=size,
                source=TRADE_SOURCE,
                skill_slug=SKILL_SLUG,
                reasoning=reasoning,
            )
            tag    = "(sim)" if r.simulated else "(live)"
            status = "OK" if r.success else f"FAIL:{r.error}"
            safe_print(f"  [trade] {side.upper()} ${size} {tag} {status} -- {reasoning[:70]}")
            if r.success:
                placed += 1
        except Exception as e:
            safe_print(f"  [error] {m.id}: {e}")

    safe_print(f"[calendar-catalyst] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Trades Polymarket markets resolving near known calendar catalyst events."
    )
    ap.add_argument("--live", action="store_true",
                    help="Real trades on Polymarket. Default is paper (sim) mode.")
    run(live=ap.parse_args().live)
