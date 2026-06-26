"""
polymarket-nordic-trader
Trades Nordic/Scandinavian prediction markets on Polymarket using local knowledge and CET timezone edge.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag.
"""
import os
import argparse
from datetime import datetime, timezone
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-nordic-trader"
SKILL_SLUG   = "polymarket-nordic-trader"

KEYWORDS = [
    'Sweden', 'Sverige', 'Stockholm', 'Malmö', 'Göteborg',
    'Norway', 'Norge', 'Oslo', 'Denmark', 'Danmark', 'Copenhagen',
    'Finland', 'Helsinki', 'Nordic', 'Scandinavian',
    'Spotify', 'Northvolt', 'Klarna', 'Ericsson', 'Volvo', 'IKEA',
    'Riksdag', 'Melodifestivalen', 'Zlatan', 'Allsvenskan',
    'SMHI', 'Öresund',
]

# Risk parameters — declared as tunables in clawhub.json, tunable from Simmer UI.
# Named SIMMER_* so apply_skill_config() can load automaton-managed overrides.
MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  "20"))
MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    "1000"))
MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.2"))
MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      "3"))
MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "8"))
# Signal thresholds — buy YES below YES_THRESHOLD, sell NO above NO_THRESHOLD.
# Position size scales with conviction, further boosted by timezone and domain edge.
YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.38"))
NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",  "0.62"))
MIN_TRADE      = float(os.environ.get("SIMMER_MIN_TRADE",     "5"))

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


def local_edge_bias(question: str) -> float:
    """
    Returns a conviction multiplier (0.75–1.40) combining two Nordic-specific
    structural edges:

    1. CET TIMEZONE ADVANTAGE
       Nordic news breaks during CET business hours (approx 06:00–18:00 UTC).
       Polymarket is US-dominated — repricing on Nordic news takes 2–6h.
       Trading during CET hours means local information is still fresh.
       Outside those hours the window is likely already priced in.

       In CET hours  → time_multiplier = 1.2
       Outside hours → time_multiplier = 0.9

    2. DOMAIN CONFIDENCE
       Some Nordic categories have highly verifiable, public, structured
       signals. Others (sports, culture) are more random.

       Riksdag / politics   → 1.20x  (public data, predictable process)
       Nordic tech / unicorns → 1.15x  (Swedish press is early and detailed)
       SMHI / local weather → 1.10x  (Swedish forecasts public before English)
       Sports / culture     → 0.85x  (high randomness, fan noise)

    Combined and capped at 1.40 to avoid over-sizing on illiquid markets.
    """
    hour_utc = datetime.now(timezone.utc).hour
    time_multiplier = 1.2 if 6 <= hour_utc <= 18 else 0.9

    q = question.lower()

    if any(w in q for w in ("riksdag", "election", "government", "budget", "legislation", "coalition", "prime minister", "statsminister")):
        domain_multiplier = 1.2
    elif any(w in q for w in ("spotify", "klarna", "northvolt", "ericsson", "volvo", "ikea", "h&m", "atlas copco")):
        domain_multiplier = 1.15
    elif any(w in q for w in ("smhi", "temperature", "snowfall", "weather", "heatwave", "öresund")):
        domain_multiplier = 1.1
    elif any(w in q for w in ("melodifestivalen", "eurovision", "zlatan", "football", "hockey", "allsvenskan")):
        domain_multiplier = 0.85
    else:
        domain_multiplier = 1.0

    return min(1.4, time_multiplier * domain_multiplier)


def compute_signal(market) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    Conviction-based sizing with local knowledge and timezone boost:
    - Base conviction scales linearly with distance from threshold
    - local_edge_bias() combines CET timing and domain confidence
    - Result capped at 1.0 so size never exceeds MAX_POSITION
    - MIN_TRADE floor prevents trivially small orders near the boundary

    Remix: feed Riksdagen API voting data or SMHI forecast probability
    directly into p to trade the divergence between local data and market.
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

    bias = local_edge_bias(q)

    if p <= YES_THRESHOLD:
        # conviction=0 at threshold boundary, conviction=1 at p=0 — scaled by local edge bias
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
    print(f"[polymarket-nordic-trader] mode={mode} max_pos=${MAX_POSITION} min_vol=${MIN_VOLUME} max_spread={MAX_SPREAD:.0%} min_days={MIN_DAYS}")

    client  = get_client(live=live)
    markets = find_markets(client)
    print(f"[polymarket-nordic-trader] {len(markets)} candidate markets")

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
            tag = "(sim)" if r.simulated else "(live)"
            status = "OK" if r.success else f"FAIL:{r.error}"
            print(f"  [trade] {side.upper()} ${size} {tag} {status} — {reasoning[:70]}")
            if r.success:
                placed += 1
        except Exception as e:
            print(f"  [error] {m.id}: {e}")

    print(f"[polymarket-nordic-trader] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Trades Nordic/Scandinavian prediction markets on Polymarket using local knowledge and CET timezone edge.")
    ap.add_argument("--live", action="store_true",
                    help="Real trades on Polymarket. Default is paper (sim) mode.")
    run(live=ap.parse_args().live)
