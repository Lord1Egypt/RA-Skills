"""
polymarket-music-entertainment-trader
Trades music streaming milestones, album charts, Grammy awards, and entertainment markets on Polymarket.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag.
"""
import os
import argparse
from datetime import datetime, timezone
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-music-entertainment-trader"
SKILL_SLUG   = "polymarket-music-entertainment-trader"

KEYWORDS = [
    'Taylor Swift', 'Bad Bunny', 'Beyoncé', 'Drake', 'Kendrick',
    'Spotify', 'Billboard', 'Grammy', 'streaming', 'album',
    'chart', 'tour', 'concert', 'certification', 'RIAA',
    'K-pop', 'Afrobeats', 'Latin music', 'country', 'TikTok music',
    'music catalog', 'record label', 'music deal',
]

# Risk parameters — declared as tunables in clawhub.json, tunable from Simmer UI.
# Named SIMMER_* so apply_skill_config() can load automaton-managed overrides.
MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  "15"))
MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    "1000"))
MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.15"))
MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      "0"))
MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "10"))
# Signal thresholds — buy YES below YES_THRESHOLD, sell NO above NO_THRESHOLD.
# Position size scales with conviction, further adjusted by market sentiment patterns.
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
            if m.id not in seen and any(w in q for w in ("taylor swift", "beyonc", "drake", "kendrick", "grammys", "concert", "album")):
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
            if m.id not in seen and any(w in q for w in ("taylor swift", "beyonc", "drake", "kendrick", "grammys", "concert", "album")):
                seen.add(m.id)
                unique.append(m)
    except Exception:
        pass

    return unique


def sentiment_bias(question: str) -> float:
    """
    Returns a conviction multiplier (0.75–1.20) based on known sentiment
    patterns in music and entertainment prediction markets.

    Megastar markets are emotionally driven — retail overbets on beloved
    artists, creating noisy and irrational pricing. Trade smaller.

    Streaming and chart milestone markets are data-driven and trackable
    in near real-time via Spotify/Billboard APIs — lean in when edge exists.

    Emerging global genres are consistently underweighted by US-centric
    retail traders — lean in on Afrobeats, K-pop, Latin milestones.

    Pattern                        Reason
    ─────────────────────────────  ──────────────────────────────────────────
    Megastar fan markets → 0.75x   Fan bias inflates YES; market is high noise
    Awards ceremonies → 0.85x      Fan voting + industry politics = hard to model
    Streaming / chart data → 1.15x Data available before market reprices
    Emerging global genres → 1.20x Underweighted by US-centric retail traders
    """
    q = question.lower()

    # Megastar fan-favorite markets — emotionally driven, high noise
    if any(w in q for w in ("taylor swift", "beyoncé", "beyonce", "bts", "blackpink", "ariana grande")):
        return 0.75

    # Awards markets — fan voting + label politics = hard to model
    if any(w in q for w in ("grammy", "oscar", "vma", "ama", "brit award", "billboard award")):
        return 0.85

    # Streaming and chart milestone markets — data-driven, trackable
    if any(w in q for w in ("spotify", "billboard", "streams", "chart", "certification", "riaa", "platinum")):
        return 1.15

    # Emerging global genres — underpriced by US-centric retail
    if any(w in q for w in ("afrobeats", "k-pop", "latin", "amapiano", "regional mexican", "afropop")):
        return 1.2

    return 1.0  # no sentiment pattern detected — neutral


def compute_signal(market) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    Conviction-based sizing with sentiment bias adjustment:
    - Base conviction scales linearly with distance from threshold
    - sentiment_bias() multiplies conviction up/down based on market type
    - Result capped at 1.0 so size never exceeds MAX_POSITION
    - MIN_TRADE floor prevents trivially small orders near the boundary

    Remix: feed Spotify Charts streaming velocity or Chartmetric scores
    into p to trade the divergence between real-time data and market price.
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

    bias = sentiment_bias(q)

    if p <= YES_THRESHOLD:
        # conviction=0 at threshold boundary, conviction=1 at p=0 — scaled by sentiment bias
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
    print(f"[polymarket-music-entertainment-trader] mode={mode} max_pos=${MAX_POSITION} min_vol=${MIN_VOLUME} max_spread={MAX_SPREAD:.0%} min_days={MIN_DAYS}")

    client  = get_client(live=live)
    markets = find_markets(client)
    print(f"[polymarket-music-entertainment-trader] {len(markets)} candidate markets")

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

    print(f"[polymarket-music-entertainment-trader] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Trades music streaming milestones, album charts, Grammy awards, and entertainment markets on Polymarket.")
    ap.add_argument("--live", action="store_true",
                    help="Real trades on Polymarket. Default is paper (sim) mode.")
    run(live=ap.parse_args().live)
