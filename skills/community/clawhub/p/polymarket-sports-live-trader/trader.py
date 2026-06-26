"""
polymarket-sports-live-trader
Trades sports prediction markets: championships, MVP races, tournament brackets, transfers, and season milestones.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag.
"""
import os
import argparse
from datetime import datetime, timezone
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-sports-live-trader"
SKILL_SLUG   = "polymarket-sports-live-trader"

KEYWORDS = [
    'Champions League', 'World Cup', 'Super Bowl', 'NBA Finals',
    'Premier League', 'La Liga', 'Bundesliga', 'Serie A',
    'NFL', 'NBA', 'MLB', 'NHL', 'UFC', 'tennis', 'Grand Slam',
    'transfer', 'signing', 'MVP', 'Ballon d\'Or', 'Golden Boot',
    'playoff', 'championship', 'title', 'Wimbledon',
    'Tour de France', 'Formula 1', 'F1', 'MotoGP',
]

# Risk parameters — declared as tunables in clawhub.json, adjustable from Simmer UI.
# Named SIMMER_* so apply_skill_config() can load automaton-managed overrides.
MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  "25"))
MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    "1000"))
MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.08"))
MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      "0"))
MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "8"))
# Signal thresholds — buy YES below YES_THRESHOLD, sell NO above NO_THRESHOLD.
# Position size scales with conviction, adjusted by fan bias and sports calendar.
YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.42"))
NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",  "0.58"))
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

    # Fast markets (may not exist in older SDK)
    try:
        for m in client.get_fast_markets():
            q = getattr(m, "question", "").lower()
            if m.id not in seen and any(w in q for w in ("champions league", "nba", "nfl", "premier league", "world cup", "tennis", "ufc")):
                seen.add(m.id)
                unique.append(m)
    except (AttributeError, Exception):
        pass

    # Keyword search
    for kw in KEYWORDS:
        try:
            for m in client.find_markets(query=kw):
                if m.id not in seen:
                    seen.add(m.id)
                    unique.append(m)
        except Exception as e:
            print(f"[search] {kw!r}: {e}")

    # Bulk scan fallback
    try:
        for m in client.get_markets(limit=200):
            q = getattr(m, "question", "").lower()
            if m.id not in seen and any(w in q for w in ("champions league", "nba", "nfl", "premier league", "world cup", "tennis", "ufc")):
                seen.add(m.id)
                unique.append(m)
    except Exception:
        pass

    return unique


def sport_bias(question: str) -> float:
    """
    Returns a conviction multiplier (0.70–1.35) combining two sports-specific
    structural edges:

    1. FAN LOYALTY BIAS
       Popular club markets attract the most emotional retail betting.
       Supporters of Real Madrid, Man City, Lakers consistently overprice
       YES — trade smaller to avoid being squeezed by fan irrationality.
       Transfer and award markets are more data-driven — lean in.

       Fan-favorite clubs (Real Madrid, Man City, Lakers) → 0.75x
       Peak fan events (Super Bowl, UCL final, World Cup final) → 0.80x
       Individual sports (tennis, F1, golf)                  → 1.15x
       Transfer / contract markets                           → 1.20x
       Award markets (MVP, Ballon d'Or, Golden Boot)         → 1.10x

    2. SPORTS CALENDAR TIMING
       Each sport has a defined season with periods of peak information
       density. Trading when a sport is in its active season means more
       signal, less noise, better edge.

       Football title run-in (Mar–May)   → 1.15x
       NFL season (Sep–Feb)              → 1.10x
       NBA playoffs (Apr–Jun)            → 1.15x
       Transfer windows (Jan, Jun–Sep)   → 1.20x
       Wimbledon / tennis slams (Jun–Sep)→ 1.15x

    Combined and capped at 1.35x.
    """
    month = datetime.now(timezone.utc).month
    q = question.lower()

    # Factor 1: fan loyalty / market type
    if any(w in q for w in ("real madrid", "manchester city", "man city", "liverpool",
                             "barcelona", "lakers", "golden state warriors", "new england patriots")):
        fan_mult = 0.75
    elif any(w in q for w in ("super bowl", "champions league final", "world cup final",
                               "nba finals", "el clásico", "el clasico", "nfl championship")):
        fan_mult = 0.80
    elif any(w in q for w in ("transfer", "signing", "contract extension", "fee", "move to")):
        fan_mult = 1.20  # Transfer leaks trackable through journalist sources
    elif any(w in q for w in ("mvp", "ballon d'or", "golden boot", "player of the year",
                               "top scorer", "best player")):
        fan_mult = 1.10  # Stats-driven — quantifiable edge
    elif any(w in q for w in ("wimbledon", "us open", "french open", "australian open",
                               "grand slam", "formula 1", "f1 ", "golf major", "masters golf")):
        fan_mult = 1.15  # Individual performance: more data-driven than team sports
    else:
        fan_mult = 1.0

    # Factor 2: sports calendar timing
    if any(w in q for w in ("transfer", "signing")):
        calendar_mult = 1.2 if month in (1, 6, 7, 8, 9) else 0.85
    elif any(w in q for w in ("champions league", "premier league", "la liga", "bundesliga", "serie a", "ligue 1")):
        calendar_mult = 1.15 if 3 <= month <= 5 else 1.0   # Title run-in
    elif any(w in q for w in ("nfl", "super bowl", "american football")):
        calendar_mult = 1.1 if month in (9, 10, 11, 12, 1, 2) else 0.85
    elif any(w in q for w in ("nba", "basketball playoffs")):
        calendar_mult = 1.15 if 4 <= month <= 6 else 1.0
    elif any(w in q for w in ("wimbledon", "tennis", "grand slam")):
        calendar_mult = 1.15 if 6 <= month <= 9 else 1.0
    else:
        calendar_mult = 1.0

    return min(1.35, fan_mult * calendar_mult)


def compute_signal(market) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    Conviction-based sizing with fan bias and calendar adjustment:
    - Base conviction scales linearly with distance from threshold
    - sport_bias() dampens fan-favorite markets, boosts data-driven ones,
      and adjusts for whether the sport is in its active season
    - Result capped at 1.0 so size never exceeds MAX_POSITION
    - MIN_TRADE floor prevents trivially small orders near the boundary

    Remix: feed Club Elo ratings or FiveThirtyEight model probabilities
    into p to trade the divergence between quantitative rankings and market.
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

    bias = sport_bias(q)

    if p <= YES_THRESHOLD:
        # conviction=0 at threshold boundary, conviction=1 at p=0 — scaled by sport bias
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
    print(f"[polymarket-sports-live-trader] mode={mode} max_pos=${MAX_POSITION} min_vol=${MIN_VOLUME} max_spread={MAX_SPREAD:.0%} min_days={MIN_DAYS}")

    client  = get_client(live=live)
    markets = find_markets(client)
    print(f"[polymarket-sports-live-trader] {len(markets)} candidate markets")

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

    print(f"[polymarket-sports-live-trader] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Trades sports prediction markets: championships, MVP races, tournament brackets, transfers, and season milestones.")
    ap.add_argument("--live", action="store_true",
                    help="Real trades on Polymarket. Default is paper (sim) mode.")
    run(live=ap.parse_args().live)
