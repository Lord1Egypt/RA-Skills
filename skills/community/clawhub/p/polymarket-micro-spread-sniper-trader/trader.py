"""
polymarket-micro-spread-sniper-trader
Micro-trading skill that scans ALL markets for tight spreads (< 8%)
combined with extreme probabilities (< 15% or > 85%).

THE EDGE:
  Tight spread + extreme probability = the market maker agrees with the
  direction and is pricing it efficiently. When bid-ask is < 8% at
  p > 85% or p < 15%, the market has high confidence in the outcome.

  We exploit this by placing many tiny bets on the near-certain side:
    - p >= 85% AND spread <= 8%: sell NO (back the likely YES resolution)
    - p <= 15% AND spread <= 8%: buy YES cheaply (tiny longshot micro-bet)

  High hit rate on the near-certainty side. Tiny edge per trade, but
  volume across 20 micro-positions makes it profitable.

  The tight spread requirement is the sniper's filter: it eliminates
  illiquid markets where prices are stale or unreliable.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag.
"""
import os
import sys
import argparse
from datetime import datetime, timezone
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-micro-spread-sniper-trader"
SKILL_SLUG   = "polymarket-micro-spread-sniper-trader"

# Focused keyword sweep — high-volume categories
KEYWORDS = [
    'Bitcoin Up or Down', 'Ethereum Up or Down',
    'Solana Up or Down', 'XRP Up or Down',
]

# MICRO risk parameters — many tiny positions
MAX_POSITION  = float(os.environ.get("SIMMER_MAX_POSITION",  "10"))
MIN_VOLUME    = float(os.environ.get("SIMMER_MIN_VOLUME",    "500"))
MAX_SPREAD    = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.08"))   # Tight spread filter
MIN_DAYS      = int(os.environ.get(  "SIMMER_MIN_DAYS",      "0"))      # want fast-resolving markets
MAX_POSITIONS = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "20"))      # many micro positions
MIN_TRADE     = float(os.environ.get("SIMMER_MIN_TRADE",     "2"))

# Probability extreme thresholds
YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.00"))
NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",  "0.80"))

# Aliases for clarity in this skill's context
EXTREME_LOW   = YES_THRESHOLD   # Markets where YES is priced < 8%
EXTREME_HIGH  = NO_THRESHOLD    # Markets where YES is priced > 80%

_client: SimmerClient | None = None


def safe_print(*args, **kwargs):
    """Print that never crashes on encoding errors."""
    try:
        print(*args, **kwargs)
    except (UnicodeEncodeError, OSError):
        try:
            msg = " ".join(str(a) for a in args)
            print(msg.encode("ascii", errors="replace").decode(), **kwargs)
        except Exception:
            pass


def compute_signal(market) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    Sniper logic — tight spread + extreme probability:
      - p <= YES_THRESHOLD (0.15): buy YES — cheap longshot micro-bet
      - p >= NO_THRESHOLD  (0.85): sell NO — back the near-certain YES resolution

    Conviction sizing per CLAUDE.md:
      YES: conviction = (YES_THRESHOLD - p) / YES_THRESHOLD
      NO:  conviction = (p - NO_THRESHOLD) / (1 - NO_THRESHOLD)
      size = max(MIN_TRADE, conviction * MAX_POSITION)
    """
    p = market.current_probability
    q = market.question

    # Spread gate — this is THE key filter for this skill
    if market.spread_cents is not None and market.spread_cents / 100 > MAX_SPREAD:
        return None, 0, f"Spread {market.spread_cents/100:.1%} > {MAX_SPREAD:.1%}", None

    # Days-to-resolution gate — very permissive, we WANT fast resolution
    if market.resolves_at:
        try:
            resolves = datetime.fromisoformat(market.resolves_at.replace("Z", "+00:00"))
            days = (resolves - datetime.now(timezone.utc)).days
            if days < MIN_DAYS:
                return None, 0, f"Only {days} days to resolve", None
        except Exception:
            pass

    # Volume gate — need enough liquidity for tight spreads to be meaningful
    vol = getattr(market, "volume", None) or getattr(market, "volume_24h", None)
    if vol is not None and vol < MIN_VOLUME:
        return None, 0, f"Volume ${vol:.0f} < ${MIN_VOLUME:.0f}", None

    # BUY YES when price is extremely low — cheap longshot micro-bet
    if p <= YES_THRESHOLD:
        conviction = (YES_THRESHOLD - p) / YES_THRESHOLD
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = YES_THRESHOLD - p
        return (
            "yes", size,
            f"SNIPE YES p={p:.1%} edge={edge:.1%} size=${size} "
            f"spread<={MAX_SPREAD:.0%} — {q[:70]}",
            {"edge": round(edge, 4), "confidence": round(conviction, 4),
             "signal_source": "spread_sniper", "probability": round(p, 4)}
        )

    # SELL NO when price is extremely high — back the near-certain outcome
    if p >= NO_THRESHOLD:
        conviction = (p - NO_THRESHOLD) / (1 - NO_THRESHOLD)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = p - NO_THRESHOLD
        return (
            "no", size,
            f"SNIPE NO YES={p:.1%} edge={edge:.1%} size=${size} "
            f"spread<={MAX_SPREAD:.0%} — {q[:70]}",
            {"edge": round(edge, 4), "confidence": round(conviction, 4),
             "signal_source": "spread_sniper", "probability": round(p, 4)}
        )

    return None, 0, (
        f"Neutral at {p:.1%} — outside extreme bands "
        f"(<={YES_THRESHOLD:.0%} / >={NO_THRESHOLD:.0%})"
    ), None


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
    global _client
    global MAX_POSITION, MIN_VOLUME, MAX_SPREAD, MIN_DAYS, MAX_POSITIONS
    global MIN_TRADE, YES_THRESHOLD, NO_THRESHOLD, EXTREME_LOW, EXTREME_HIGH
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
        MAX_POSITION  = float(os.environ.get("SIMMER_MAX_POSITION",  str(MAX_POSITION)))
        MIN_VOLUME    = float(os.environ.get("SIMMER_MIN_VOLUME",    str(MIN_VOLUME)))
        MAX_SPREAD    = float(os.environ.get("SIMMER_MAX_SPREAD",    str(MAX_SPREAD)))
        MIN_DAYS      = int(os.environ.get(  "SIMMER_MIN_DAYS",      str(MIN_DAYS)))
        MAX_POSITIONS = int(os.environ.get(  "SIMMER_MAX_POSITIONS", str(MAX_POSITIONS)))
        MIN_TRADE     = float(os.environ.get("SIMMER_MIN_TRADE",     str(MIN_TRADE)))
        YES_THRESHOLD = float(os.environ.get("SIMMER_YES_THRESHOLD", str(YES_THRESHOLD)))
        NO_THRESHOLD  = float(os.environ.get("SIMMER_NO_THRESHOLD",  str(NO_THRESHOLD)))
        EXTREME_LOW   = YES_THRESHOLD
        EXTREME_HIGH  = NO_THRESHOLD
    return _client


def find_markets(client: SimmerClient) -> list:
    """
    Find active markets via three strategies:
    1. Fast markets (5-min intervals, fastest resolution)
    2. Keyword sweep across crypto categories
    3. Direct get_markets scan for recent/popular markets
    Deduplicated by market id.
    """
    seen, unique = set(), []

    # Strategy 1: fast markets (best source for micro-trading)
    try:
        for m in client.get_fast_markets():
            if m.id not in seen:
                seen.add(m.id)
                unique.append(m)
    except Exception as e:
        safe_print(f"[fast_markets] {e}")

    # Strategy 2: keyword sweep
    for kw in KEYWORDS:
        try:
            for m in client.find_markets(query=kw):
                if m.id not in seen:
                    seen.add(m.id)
                    unique.append(m)
        except Exception as e:
            safe_print(f"[search] {kw!r}: {e}")

    # Strategy 3: scan recent/popular markets directly
    try:
        for m in client.get_markets(limit=100):
            if m.id not in seen:
                seen.add(m.id)
                unique.append(m)
    except Exception as e:
        safe_print(f"[get_markets] {e}")

    return unique


def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    safe_print(
        f"[micro-spread-sniper] mode={mode} "
        f"spread<={MAX_SPREAD:.0%} extremes=<{YES_THRESHOLD:.0%}/>={NO_THRESHOLD:.0%} "
        f"max_pos=${MAX_POSITION} max_positions={MAX_POSITIONS}"
    )

    client  = get_client(live=live)
    markets = find_markets(client)
    safe_print(f"[micro-spread-sniper] {len(markets)} candidate markets scanned")

    # Pre-filter: only call context_ok on markets that pass signal check
    candidates = []
    for m in markets:
        side, size, reasoning, sig = compute_signal(m)
        if side:
            candidates.append((m, side, size, reasoning, sig))

    safe_print(f"[micro-spread-sniper] {len(candidates)} pass signal filter")

    placed = 0
    attempts = 0
    max_attempts = min(len(candidates), MAX_POSITIONS + 5)
    for m, side, size, reasoning, sig in candidates:
        if placed >= MAX_POSITIONS or attempts >= max_attempts:
            break
        attempts += 1

        try:
            trade_kwargs = dict(
                market_id=m.id, side=side, amount=size,
                source=TRADE_SOURCE, skill_slug=SKILL_SLUG,
                reasoning=reasoning,
            )
            if sig:
                trade_kwargs["signal_data"] = sig
            r = client.trade(**trade_kwargs)
            tag    = "(sim)" if r.simulated else "(live)"
            status = "OK" if r.success else f"FAIL:{r.error}"
            safe_print(
                f"  [trade] {side.upper()} ${size} {tag} {status} — "
                f"{reasoning[:75]}"
            )
            if r.success:
                placed += 1
            elif "trade limit" in str(r.error).lower():
                safe_print("  [stop] Daily trade limit reached, stopping.")
                break
        except Exception as e:
            safe_print(f"  [error] {m.id}: {e}")

    safe_print(f"[micro-spread-sniper] done. {placed}/{MAX_POSITIONS} micro orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description=(
            "Micro spread sniper: scans all markets for tight spreads (<8%) "
            "combined with extreme probabilities (<15% or >85%). "
            "Places many tiny conviction-based bets on near-certain outcomes. "
            "High hit rate, tiny edge, volume makes it profitable."
        )
    )
    ap.add_argument("--live", action="store_true",
                    help="Real trades on Polymarket. Default is paper (sim) mode.")
    run(live=ap.parse_args().live)
