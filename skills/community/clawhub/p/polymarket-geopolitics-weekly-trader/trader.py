"""
polymarket-geopolitics-weekly-trader
Trades weekly cyclical patterns in geopolitical prediction markets.

The edge: Geopolitical news flow follows weekly cycles — military operations
spike Mon-Thu, diplomacy announcements cluster around working days, weekend =
reduced news flow = stale prices = Monday repricing opportunity. Polymarket's
US-dominated retail base creates predictable weekly patterns.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag.
"""
import os
import re
import sys
import argparse
from datetime import datetime, timezone
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-geopolitics-weekly-trader"
SKILL_SLUG   = "polymarket-geopolitics-weekly-trader"

KEYWORDS = [
    'war', 'ceasefire', 'military', 'strike', 'Iran', 'Israel',
    'Gaza', 'Lebanon', 'sanctions', 'nuclear', 'troops', 'conflict',
    'diplomacy', 'NATO', 'Ukraine', 'Russia', 'China', 'Taiwan',
    'meeting', 'summit', 'peace',
]

# Geopolitics filter — question must match at least one of these patterns
# to avoid non-geopolitical false positives (e.g. "labour strike", "lightning strike").
_GEOPOLITICS_RE = re.compile(
    r"(?i)\b("
    r"war|ceasefire|military|airstrike|missile|troops|invasion|conflict|"
    r"diplomacy|diplomat|NATO|sanctions?|nuclear|peace\s*deal|"
    r"Iran|Israel|Gaza|Lebanon|Hezbollah|Hamas|"
    r"Ukraine|Russia|Kremlin|Kyiv|Moscow|"
    r"China|Taiwan|Beijing|"
    r"summit|UN\b|Security\s*Council|G[27]0?|"
    r"regime\s*change|coup|treaty|armistice|ceasefire|embargo"
    r")\b"
)

# Diplomatic keywords — markets mentioning these get a midweek boost
_DIPLOMATIC_RE = re.compile(
    r"(?i)\b("
    r"diplomacy|diplomat|summit|talks|negotiation|peace\s*deal|"
    r"accord|agreement|treaty|UN\b|Security\s*Council|G[27]0?|"
    r"meeting|dialogue|envoy|ambassador"
    r")\b"
)

# Risk parameters — declared as tunables in clawhub.json, adjustable from Simmer UI.
MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  "40"))
MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    "15000"))
MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.08"))
MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      "3"))
MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "8"))
# Signal thresholds — buy YES below YES_THRESHOLD, sell NO above NO_THRESHOLD.
YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.38"))
NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",  "0.62"))
MIN_TRADE      = float(os.environ.get("SIMMER_MIN_TRADE",     "5"))

_client: SimmerClient | None = None


def safe_print(msg: str) -> None:
    """Print with Windows Unicode safety — replace unencodable chars."""
    try:
        print(msg)
    except UnicodeEncodeError:
        print(msg.encode(sys.stdout.encoding or "utf-8", errors="replace").decode())


def weekly_pattern_multiplier(question: str) -> tuple[str, float]:
    """
    Returns (label, multiplier) based on current day-of-week and hour (UTC),
    combining four weekly pattern factors unique to geopolitical markets.

    Factor 1: Weekend Staleness (Saturday/Sunday)
      On weekends, geopolitical markets get less attention from US retail.
      News that broke Friday evening or Saturday hasn't been fully priced in.
      Markets at moderate prices (20-40% or 60-80%) on weekends are more
      likely to move Monday. Weekend: 1.15x

    Factor 2: Monday Repricing Window (Monday 00:00-14:00 UTC)
      Monday mornings = repricing of weekend events. Asian/European news
      from weekend flows into US market opening. Early Monday: 1.25x

    Factor 3: Friday Afternoon Position Unwinding (Friday 18:00+ UTC)
      Traders reduce risk before weekend — creates temporary dislocations.
      Prices may drift from fair value as positions are closed.
      Friday evening: 1.10x

    Factor 4: Midweek Diplomatic Calendar (Tue-Thu)
      UN sessions, G7/G20 meetings, diplomatic summits cluster Tue-Thu.
      Diplomatic markets are more actionable midweek.
      For diplomatic-tagged markets on Tue-Thu: 1.10x

    weekday(): 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri, 5=Sat, 6=Sun
    """
    now     = datetime.now(timezone.utc)
    weekday = now.weekday()
    hour    = now.hour

    is_diplomatic = bool(_DIPLOMATIC_RE.search(question))

    # Factor 1: Weekend staleness
    if weekday in (5, 6):
        return "WEEKEND(stale-pricing)", 1.15

    # Factor 2: Monday repricing window
    if weekday == 0 and hour < 14:
        return "MONDAY-AM(repricing)", 1.25
    if weekday == 0:
        return "MONDAY-PM(fading)", 1.05

    # Factor 3: Friday afternoon unwinding
    if weekday == 4 and hour >= 18:
        return "FRIDAY-PM(unwinding)", 1.10
    if weekday == 4:
        return "FRIDAY-AM(normal)", 1.0

    # Factor 4: Midweek diplomatic calendar (Tue-Thu)
    if weekday in (1, 2, 3) and is_diplomatic:
        day_name = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][weekday]
        return f"{day_name}(diplomatic-calendar)", 1.10

    # Tue-Thu, non-diplomatic
    if weekday in (1, 2, 3):
        day_name = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][weekday]
        return f"{day_name}(midweek)", 1.0

    return "default", 1.0


def compute_signal(market) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    Conviction-based sizing with weekly pattern correction:
    - Filters for genuine geopolitical markets via regex
    - Base conviction scales linearly with distance from threshold
    - weekly_pattern_multiplier() boosts conviction during exploitable
      weekly windows: weekend staleness, Monday repricing, Friday unwinding,
      and midweek diplomatic calendar alignment
    - Result capped at 1.0 so size never exceeds MAX_POSITION
    - MIN_TRADE floor prevents trivially small orders near the boundary

    Remix: wire a news API (GDELT, ACLED) velocity-by-day-of-week feed
    into this function to dynamically adjust the weekly multiplier based
    on actual news flow deviations from the historical weekly baseline.
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

    # Geopolitics filter — skip non-geopolitical markets
    if not _GEOPOLITICS_RE.search(q):
        return None, 0, "Not a geopolitical market"

    timing_label, weekly_mult = weekly_pattern_multiplier(q)

    if p <= YES_THRESHOLD:
        base_conviction = (YES_THRESHOLD - p) / YES_THRESHOLD
        conviction = min(1.0, base_conviction * weekly_mult)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = YES_THRESHOLD - p
        return "yes", size, f"YES {p:.0%} edge={edge:.0%} wk={weekly_mult:.2f}x({timing_label}) size=${size} — {q[:60]}"

    if p >= NO_THRESHOLD:
        base_conviction = (p - NO_THRESHOLD) / (1 - NO_THRESHOLD)
        conviction = min(1.0, base_conviction * weekly_mult)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = p - NO_THRESHOLD
        return "no", size, f"NO YES={p:.0%} edge={edge:.0%} wk={weekly_mult:.2f}x({timing_label}) size=${size} — {q[:60]}"

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


def get_client(live: bool = False) -> SimmerClient:
    """
    live=False -> venue="sim"  (paper trades -- safe default).
    live=True  -> venue="polymarket" (real trades, only with --live flag).
    """
    global _client, MAX_POSITION, MIN_VOLUME, MAX_SPREAD, MIN_DAYS, MAX_POSITIONS, YES_THRESHOLD, NO_THRESHOLD, MIN_TRADE
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
    return _client


def find_markets(client: SimmerClient) -> list:
    """Find active markets matching strategy keywords, deduplicated."""
    seen, unique = set(), []
    for kw in KEYWORDS:
        try:
            for m in client.find_markets(query=kw):
                if m.id not in seen:
                    seen.add(m.id)
                    unique.append(m)
        except Exception as e:
            safe_print(f"[search] {kw!r}: {e}")
    return unique


def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    timing_label, timing_mult = weekly_pattern_multiplier("")
    safe_print(f"[polymarket-geopolitics-weekly-trader] mode={mode} max_pos=${MAX_POSITION} timing={timing_label}({timing_mult:.2f}x)")

    client  = get_client(live=live)
    markets = find_markets(client)
    safe_print(f"[polymarket-geopolitics-weekly-trader] {len(markets)} candidate markets")

    placed = 0
    for m in markets:
        if placed >= MAX_POSITIONS:
            break

        side, size, reasoning = compute_signal(m)
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
            safe_print(f"  [trade] {side.upper()} ${size} {tag} {status} — {reasoning[:70]}")
            if r.success:
                placed += 1
        except Exception as e:
            safe_print(f"  [error] {m.id}: {e}")

    safe_print(f"[polymarket-geopolitics-weekly-trader] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Trades weekly cyclical patterns in geopolitical prediction markets. Weekend staleness, Monday repricing, Friday unwinding, and midweek diplomatic calendar alignment.")
    ap.add_argument("--live", action="store_true",
                    help="Real trades on Polymarket. Default is paper (sim) mode.")
    run(live=ap.parse_args().live)
