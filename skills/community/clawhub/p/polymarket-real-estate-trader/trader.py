"""
polymarket-real-estate-trader
Trades real estate and housing prediction markets: home prices, Fed rates, mortgage rates, crash scenarios, and regional markets.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag.
"""
import os
import argparse
from datetime import datetime, timezone
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-real-estate-trader"
SKILL_SLUG   = "polymarket-real-estate-trader"

KEYWORDS = [
    'housing', 'home price', 'real estate', 'mortgage', 'mortgage rate',
    'Fed rate', 'FOMC', 'rate cut', 'rate hike', 'Federal Reserve',
    'interest rate', 'basis point', 'Case-Shiller', 'home price index',
    'housing crash', 'bubble', 'correction', 'rent', 'apartment',
    'commercial real estate', 'office vacancy', 'Zillow', 'Redfin',
    '30-year mortgage', 'CRE', 'housing market',
]

# Risk parameters — declared as tunables in clawhub.json, adjustable from Simmer UI.
# Named SIMMER_* so apply_skill_config() can load automaton-managed overrides.
MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  "30"))
MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    "8000"))
MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.08"))
MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      "7"))
MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "6"))
# Signal thresholds — buy YES below YES_THRESHOLD, sell NO above NO_THRESHOLD.
# Position size scales with conviction, adjusted by FOMC calendar and market type.
YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.38"))
NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",  "0.62"))
MIN_TRADE      = float(os.environ.get("SIMMER_MIN_TRADE",     "5"))

# FOMC meets approximately 8x per year in these months.
# Rate-related markets have highest edge in the pre-meeting window.
_FOMC_MONTHS = {1, 3, 5, 6, 7, 9, 11, 12}

_client: SimmerClient | None = None


def get_client(live: bool = False) -> SimmerClient:
    """
    live=False → venue="sim"  (paper trades — safe default).
    live=True  → venue="polymarket" (real trades, only with --live flag).
    """
    global _client, MAX_POSITION, MIN_VOLUME, MAX_SPREAD, MIN_DAYS, MAX_POSITIONS, YES_THRESHOLD, NO_THRESHOLD, MIN_TRADE
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
            print(f"[search] {kw!r}: {e}")
    return unique


def macro_cycle_bias(question: str) -> float:
    """
    Returns a conviction multiplier (0.75–1.40) combining two real estate
    and macro-specific structural edges:

    1. FOMC CALENDAR TIMING
       Fed rate decision markets have their highest edge in the 2–4 weeks
       BEFORE an FOMC meeting — this is when CME FedWatch (professional
       market) and Polymarket (retail) diverge most. After the decision,
       markets reprice within hours and the window closes.

       FOMC meets ~8x/year: Jan, Mar, May, Jun, Jul, Sep, Nov, Dec.

       Rate question + FOMC active month  → timing_mult = 1.2
       Rate question + gap month          → timing_mult = 0.9
       Non-rate question                  → timing_mult = 1.0

    2. MARKET TYPE CONFIDENCE
       Different real estate sub-categories have vastly different signal quality.

       Fed/FOMC rate decisions   → 1.25x  (CME FedWatch = professional calibration)
       Mortgage rate markets     → 1.15x  (mechanically tied to Fed — predictable)
       Case-Shiller / price data → 1.10x  (index releases are trackable)
       Housing crash / bubble    → 0.75x  (narrative/fear-driven, high variance)
       Commercial RE / office    → 0.80x  (WFH narrative distorts pricing)

    Combined and capped at 1.40x.
    """
    month = datetime.now(timezone.utc).month
    q = question.lower()

    # Factor 1: FOMC calendar timing (only applied to rate-related questions)
    rate_keywords = ("fomc", "fed funds", "rate cut", "rate hike", "federal reserve",
                     "interest rate", "rate decision", "basis point", "rate pause")
    if any(w in q for w in rate_keywords):
        timing_mult = 1.2 if month in _FOMC_MONTHS else 0.9
    else:
        timing_mult = 1.0

    # Factor 2: market type confidence
    if any(w in q for w in ("fomc", "fed funds", "rate cut", "rate hike", "rate decision",
                             "federal reserve", "basis point", "rate pause")):
        type_mult = 1.25  # CME FedWatch provides professional-grade calibration
    elif any(w in q for w in ("mortgage rate", "30-year", "15-year", "mortgage")):
        type_mult = 1.15  # Mechanically tied to Fed funds — highly predictable direction
    elif any(w in q for w in ("case-shiller", "home price index", "zillow", "median home price", "redfin")):
        type_mult = 1.10  # Data-driven index releases — trackable trajectory
    elif any(w in q for w in ("crash", "bubble", "collapse", "correction", "crisis")):
        type_mult = 0.75  # Fear/narrative-driven — hard to time, high variance
    elif any(w in q for w in ("office vacancy", "commercial real estate", "wfh",
                               "work from home", "cre", "remote work")):
        type_mult = 0.80  # WFH narrative distorts rational pricing
    else:
        type_mult = 1.0

    return min(1.40, timing_mult * type_mult)


def compute_signal(market) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    Conviction-based sizing with FOMC calendar and market type adjustment:
    - Base conviction scales linearly with distance from threshold
    - macro_cycle_bias() boosts Fed/rate markets in FOMC-active months,
      dampens emotional crash/WFH narrative markets year-round
    - Result capped at 1.0 so size never exceeds MAX_POSITION
    - MIN_TRADE floor prevents trivially small orders near the boundary

    Remix: feed CME FedWatch implied probability directly into p to trade
    the divergence between professional futures market and Polymarket retail.
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

    bias = macro_cycle_bias(q)

    if p <= YES_THRESHOLD:
        # conviction=0 at threshold boundary, conviction=1 at p=0 — scaled by macro bias
        conviction = min(1.0, (YES_THRESHOLD - p) / YES_THRESHOLD * bias)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = YES_THRESHOLD - p
        return "yes", size, f"YES {p:.0%} edge={edge:.0%} bias={bias:.2f}x size=${size} — {q[:65]}"

    if p >= NO_THRESHOLD:
        conviction = min(1.0, (p - NO_THRESHOLD) / (1 - NO_THRESHOLD) * bias)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = p - NO_THRESHOLD
        return "no", size, f"NO YES={p:.0%} edge={edge:.0%} bias={bias:.2f}x size=${size} — {q[:65]}"

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
            print(f"  [warn] {w}")
    except Exception as e:
        print(f"  [ctx] {market_id}: {e}")
    return True, "ok"


def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    print(f"[polymarket-real-estate-trader] mode={mode} max_pos=${MAX_POSITION} min_vol=${MIN_VOLUME} max_spread={MAX_SPREAD:.0%} min_days={MIN_DAYS}")

    client  = get_client(live=live)
    markets = find_markets(client)
    print(f"[polymarket-real-estate-trader] {len(markets)} candidate markets")

    placed = 0
    for m in markets:
        if placed >= MAX_POSITIONS:
            break

        side, size, reasoning = compute_signal(m)
        if not side:
            print(f"  [skip] {reasoning}")
            continue

        ok, why = context_ok(client, m.id)
        if not ok:
            print(f"  [skip] {why}")
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
            print(f"  [trade] {side.upper()} ${size} {tag} {status} — {reasoning[:70]}")
            if r.success:
                placed += 1
        except Exception as e:
            print(f"  [error] {m.id}: {e}")

    print(f"[polymarket-real-estate-trader] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Trades real estate and housing prediction markets: home prices, Fed rates, mortgage rates, crash scenarios, and regional markets.")
    ap.add_argument("--live", action="store_true",
                    help="Real trades on Polymarket. Default is paper (sim) mode.")
    run(live=ap.parse_args().live)
