"""
polymarket-geopolitics-sentiment-reversal-trader
Trades mean reversion on geopolitical markets pushed to probability extremes
by breaking news overreaction.

THE EDGE:
  Daily geopolitical markets (military action, strikes, sanctions) at >92% or
  <8% systematically over-react to breaking news and revert 30-50% of the move
  within 24-48h. This is documented in behavioral finance as "overreaction bias"
  in politically charged markets.

  The key insight is STALENESS: a market at 92% with 180 days to resolve is
  far more likely to be an overreaction than the same market at 92% with 2 days
  left. Long time horizons amplify overreaction because there is more time for
  mean reversion to play out, and the extreme price is less likely to reflect
  genuine near-term resolution information.

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

TRADE_SOURCE = "sdk:polymarket-geopolitics-sentiment-reversal-trader"
SKILL_SLUG   = "polymarket-geopolitics-sentiment-reversal-trader"

KEYWORDS = [
    'war', 'ceasefire', 'military', 'strike', 'Iran', 'Israel',
    'Gaza', 'Lebanon', 'sanctions', 'nuclear', 'troops', 'conflict',
    'attack', 'bomb', 'invasion', 'Hezbollah', 'Hamas',
]

# Regex filter — only trade markets whose question matches geopolitical topics.
_GEO_RE = re.compile(
    r"(?i)\b("
    r"war|ceasefire|military|strike|iran|israel|gaza|lebanon|sanctions|nuclear|"
    r"troops|conflict|attack|bomb|invasion|hezbollah|hamas|nato|ukraine|russia|"
    r"china|taiwan|missile|drone|airstrike|artillery|occupation|regime|"
    r"escalat|retaliat|deploy|weapon|army|navy|insurgent|terror"
    r")\b"
)

# Risk parameters — declared as tunables in clawhub.json, adjustable from Simmer UI.
MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  "40"))
MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    "15000"))
MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.08"))
MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      "3"))
MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "6"))
MIN_TRADE      = float(os.environ.get("SIMMER_MIN_TRADE",     "5"))

# Standard signal thresholds (gates from CLAUDE.md).
YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.38"))
NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",  "0.62"))

# Reversal-specific parameters.
# REVERSAL_ZONE_HIGH: above this probability, market is in the "too certain" zone.
# REVERSAL_ZONE_LOW: below this probability, same thing on the downside.
# MIN_DAYS_FOR_REVERSAL: only trade reversal if market has enough runway to revert.
REVERSAL_ZONE_HIGH    = float(os.environ.get("SIMMER_REVERSAL_ZONE_HIGH",    "0.92"))
REVERSAL_ZONE_LOW     = float(os.environ.get("SIMMER_REVERSAL_ZONE_LOW",     "0.08"))
MIN_DAYS_FOR_REVERSAL = int(os.environ.get(  "SIMMER_MIN_DAYS_REVERSAL",     "7"))

_client: SimmerClient | None = None


def safe_print(msg: str) -> None:
    """Print with fallback for Windows Unicode errors."""
    try:
        print(msg)
    except UnicodeEncodeError:
        print(msg.encode("ascii", errors="replace").decode())


def get_client(live: bool = False) -> SimmerClient:
    """
    live=False -> venue="sim"  (paper trades -- safe default).
    live=True  -> venue="polymarket" (real trades, only with --live flag).
    """
    global _client
    global MAX_POSITION, MIN_VOLUME, MAX_SPREAD, MIN_DAYS, MAX_POSITIONS
    global MIN_TRADE, YES_THRESHOLD, NO_THRESHOLD
    global REVERSAL_ZONE_HIGH, REVERSAL_ZONE_LOW, MIN_DAYS_FOR_REVERSAL
    if _client is None:
        venue = "polymarket" if live else "sim"
        _client = SimmerClient(
            api_key=os.environ["SIMMER_API_KEY"],
            venue=venue,
        )
        # Load tunable overrides set via the Simmer UI (SIMMER_* vars only).
        if live:
            _client.live = True
        try:
            _client.apply_skill_config(SKILL_SLUG)
        except AttributeError:
            pass  # apply_skill_config only available in Simmer runtime
        # Re-read params in case apply_skill_config updated os.environ.
        MAX_POSITION          = float(os.environ.get("SIMMER_MAX_POSITION",       str(MAX_POSITION)))
        MIN_VOLUME            = float(os.environ.get("SIMMER_MIN_VOLUME",         str(MIN_VOLUME)))
        MAX_SPREAD            = float(os.environ.get("SIMMER_MAX_SPREAD",         str(MAX_SPREAD)))
        MIN_DAYS              = int(os.environ.get(  "SIMMER_MIN_DAYS",           str(MIN_DAYS)))
        MAX_POSITIONS         = int(os.environ.get(  "SIMMER_MAX_POSITIONS",      str(MAX_POSITIONS)))
        MIN_TRADE             = float(os.environ.get("SIMMER_MIN_TRADE",          str(MIN_TRADE)))
        YES_THRESHOLD         = float(os.environ.get("SIMMER_YES_THRESHOLD",      str(YES_THRESHOLD)))
        NO_THRESHOLD          = float(os.environ.get("SIMMER_NO_THRESHOLD",       str(NO_THRESHOLD)))
        REVERSAL_ZONE_HIGH    = float(os.environ.get("SIMMER_REVERSAL_ZONE_HIGH", str(REVERSAL_ZONE_HIGH)))
        REVERSAL_ZONE_LOW     = float(os.environ.get("SIMMER_REVERSAL_ZONE_LOW",  str(REVERSAL_ZONE_LOW)))
        MIN_DAYS_FOR_REVERSAL = int(os.environ.get(  "SIMMER_MIN_DAYS_REVERSAL",  str(MIN_DAYS_FOR_REVERSAL)))
    return _client


def find_markets(client: SimmerClient) -> list:
    """Find active geopolitical markets matching strategy keywords, deduplicated."""
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


def compute_signal(market) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    Mean-reversion signal for geopolitical markets at probability extremes.

    The staleness factor is the key innovation: a market at 92% with 180 days
    to resolve is far more overpriced than the same market with 3 days left.
    Staleness scales linearly from 0.0 (at MIN_DAYS_FOR_REVERSAL) to 1.0
    (at 90+ days), capping at 1.0.

    When p >= REVERSAL_ZONE_HIGH (default 0.92):
      - We think the market will revert DOWN from the extreme.
      - Trade "no" to profit from the expected decline.
      - conviction = staleness_factor * (p - REVERSAL_ZONE_HIGH) / (1 - REVERSAL_ZONE_HIGH)
      - Gate: must also pass p >= NO_THRESHOLD (standard framework gate).

    When p <= REVERSAL_ZONE_LOW (default 0.08):
      - We think the market will revert UP from the extreme.
      - Trade "yes" to profit from the expected rise.
      - conviction = staleness_factor * (REVERSAL_ZONE_LOW - p) / REVERSAL_ZONE_LOW
      - Gate: must also pass p <= YES_THRESHOLD (standard framework gate).

    Size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
    """
    p = market.current_probability
    q = market.question

    # Geopolitics filter — skip non-geopolitical markets that slipped through keywords.
    if not _GEO_RE.search(q):
        return None, 0, f"Not geopolitical: {q[:60]}"

    # Spread gate
    if market.spread_cents is not None and market.spread_cents / 100 > MAX_SPREAD:
        return None, 0, f"Spread {market.spread_cents/100:.1%} > {MAX_SPREAD:.1%}"

    # Days-to-resolution calculation (needed for both the gate and staleness).
    days = None
    if market.resolves_at:
        try:
            resolves = datetime.fromisoformat(market.resolves_at.replace("Z", "+00:00"))
            days = (resolves - datetime.now(timezone.utc)).days
        except Exception:
            pass

    # Standard min-days gate.
    if days is not None and days < MIN_DAYS:
        return None, 0, f"Only {days} days to resolve"

    # Reversal requires enough runway for mean reversion to play out.
    if days is not None and days < MIN_DAYS_FOR_REVERSAL:
        return None, 0, f"Only {days}d — need {MIN_DAYS_FOR_REVERSAL}d+ for reversal to play out"

    # Staleness factor: longer horizon = more likely the extreme is an overreaction.
    # 0.0 at MIN_DAYS_FOR_REVERSAL days, 1.0 at 90+ days.
    if days is not None:
        staleness = min(1.0, (days - MIN_DAYS_FOR_REVERSAL) / max(1, 90 - MIN_DAYS_FOR_REVERSAL))
    else:
        # No resolution date available — use moderate staleness assumption.
        staleness = 0.5

    # HIGH EXTREME — market is "too certain," expect reversion DOWN.
    # Gate: p must be in the reversal zone AND above the standard NO_THRESHOLD.
    if p >= REVERSAL_ZONE_HIGH and p >= NO_THRESHOLD:
        raw_conviction = (p - REVERSAL_ZONE_HIGH) / (1 - REVERSAL_ZONE_HIGH)
        conviction = min(1.0, staleness * raw_conviction)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = p - REVERSAL_ZONE_HIGH
        days_str = f"{days}d" if days is not None else "?d"
        return (
            "no", size,
            f"REVERSAL-DOWN NO p={p:.0%} edge={edge:.0%} stale={staleness:.2f} "
            f"days={days_str} size=${size} — {q[:60]}"
        )

    # LOW EXTREME — market is "too pessimistic," expect reversion UP.
    # Gate: p must be in the reversal zone AND below the standard YES_THRESHOLD.
    if p <= REVERSAL_ZONE_LOW and p <= YES_THRESHOLD:
        raw_conviction = (REVERSAL_ZONE_LOW - p) / REVERSAL_ZONE_LOW
        conviction = min(1.0, staleness * raw_conviction)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = REVERSAL_ZONE_LOW - p
        days_str = f"{days}d" if days is not None else "?d"
        return (
            "yes", size,
            f"REVERSAL-UP YES p={p:.0%} edge={edge:.0%} stale={staleness:.2f} "
            f"days={days_str} size=${size} — {q[:60]}"
        )

    return None, 0, (
        f"Neutral at {p:.1%} — not in reversal zones "
        f"(<={REVERSAL_ZONE_LOW:.0%} / >={REVERSAL_ZONE_HIGH:.0%})"
    )


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


def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    safe_print(
        f"[geopolitics-sentiment-reversal] mode={mode} "
        f"reversal_high={REVERSAL_ZONE_HIGH:.0%} reversal_low={REVERSAL_ZONE_LOW:.0%} "
        f"min_days_reversal={MIN_DAYS_FOR_REVERSAL} max_pos=${MAX_POSITION}"
    )

    client  = get_client(live=live)
    markets = find_markets(client)
    safe_print(f"[geopolitics-sentiment-reversal] {len(markets)} candidate markets")

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
            safe_print(f"  [trade] {side.upper()} ${size} {tag} {status} — {reasoning[:75]}")
            if r.success:
                placed += 1
        except Exception as e:
            safe_print(f"  [error] {m.id}: {e}")

    safe_print(f"[geopolitics-sentiment-reversal] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description=(
            "Trades mean reversion on geopolitical markets at probability extremes. "
            "Markets at >92% or <8% with long time horizons systematically over-react "
            "to breaking news. Staleness factor scales conviction with days-to-resolution."
        )
    )
    ap.add_argument("--live", action="store_true",
                    help="Real trades on Polymarket. Default is paper (sim) mode.")
    run(live=ap.parse_args().live)
