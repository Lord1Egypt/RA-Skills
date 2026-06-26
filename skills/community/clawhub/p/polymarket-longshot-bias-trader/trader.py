"""
polymarket-longshot-bias-trader
Systematically exploits longshot bias — the single most robust anomaly in
betting and prediction market research.

THE EDGE:
  Low-probability outcomes are consistently OVERpriced in prediction markets.
  High-probability outcomes are consistently UNDERpriced.

  Documented across horse racing (Griffith 1949), sports betting, financial
  options (volatility smile), and prediction markets. The mechanism is
  behavioral: retail traders overweight the excitement of longshots and
  underweight the boring near-certainty. We go the opposite direction.

  Fade the longshot (buy NO when p is very low):
    Market says 6% chance → true probability is closer to 2–3% → NO is cheap.

  Back the near-certainty (buy YES when p is very high):
    Market says 91% chance → true probability is closer to 95–97% → YES is cheap.

This is domain-agnostic — the bias exists in ALL categories of prediction
markets. We run broad keyword sweeps rather than targeting a single topic.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag.
"""
import os
import argparse
from datetime import datetime, timezone
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-longshot-bias-trader"
SKILL_SLUG   = "polymarket-longshot-bias-trader"

# Broad keyword sweep — longshot bias is category-agnostic.
# We want high volume, liquid markets where the bias is most exploitable.
KEYWORDS = [
    # High-volume political / macro
    "president", "election", "congress", "senate", "federal reserve", "rate cut",
    "rate hike", "inflation", "recession", "gdp", "unemployment",
    # High-volume crypto
    "bitcoin", "ethereum", "crypto", "btc", "eth",
    # High-volume sports
    "championship", "world cup", "super bowl", "nba finals", "world series",
    "premier league", "champions league",
    # High-volume tech / business
    "ipo", "acquisition", "merger", "bankruptcy", "earnings",
    # AI / science (very active on Polymarket)
    "agi", "artificial intelligence", "gpt", "clinical trial", "fda",
    # Geopolitical
    "ceasefire", "sanctions", "invasion", "treaty", "nato",
]

# Risk parameters
MAX_POSITION  = float(os.environ.get("SIMMER_MAX_POSITION",  "30"))
MIN_VOLUME    = float(os.environ.get("SIMMER_MIN_VOLUME",    "10000"))  # higher bar — we want liquid markets
MAX_SPREAD    = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.06"))
MIN_DAYS      = int(os.environ.get(  "SIMMER_MIN_DAYS",      "3"))      # avoid near-resolution noise
MAX_POSITIONS = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "10"))
MIN_TRADE     = float(os.environ.get("SIMMER_MIN_TRADE",     "5"))

# Longshot bias thresholds — INVERTED from the standard framework.
#
# LONGSHOT_THRESHOLD: buy NO when p <= this value.
#   A market at 7% is a screaming longshot — retail prices the excitement,
#   not the probability. We sell the dream.
#   Literature suggests the bias is strongest below 10%.
#
# CERTAINTY_THRESHOLD: buy YES when p >= this value.
#   A market at 91% is boring to retail but still offers edge.
#   The underpricing of near-certainties is the mirror image of longshot
#   overpricing — the same behavioral mechanism, opposite direction.
#   Literature suggests the bias is strongest above 88%.
LONGSHOT_THRESHOLD  = float(os.environ.get("SIMMER_LONGSHOT_THRESHOLD",  "0.10"))
CERTAINTY_THRESHOLD = float(os.environ.get("SIMMER_CERTAINTY_THRESHOLD", "0.88"))

_client: SimmerClient | None = None


def _longshot_quality_mult(question: str, p: float) -> float:
    """
    Returns a conviction multiplier (0.70–1.30) that adjusts for market
    characteristics known to amplify or dampen the longshot bias.

    1. DEPTH OF LONGSHOT / CERTAINTY (magnitude of mispricing)
       The further from 50%, the more extreme the behavioral distortion.
       p=2% is a more extreme longshot than p=9% — retail excitement peaks
       at tiny probabilities ('imagine if it happened!'). Similarly, p=98%
       is more underpriced than p=89%.

    2. NARRATIVE SALIENCE (does the event have a compelling story?)
       Markets with emotionally charged keywords attract retail dreamers who
       push longshot prices up further. A 'miracle comeback', 'dark horse',
       or 'against all odds' framing inflates longshot prices the most.
       We gain more edge fading narratively salient longshots.

    3. RESOLUTION CLARITY (is the outcome unambiguous?)
       Clear resolution criteria → less 'phantom upside' that retail
       embeds in prices. Vague criteria → wider noise band → edge less clean.
       We prefer markets with precise, objective resolution language.
    """
    q = question.lower()

    # Factor 1: depth of bias — deeper longshot / higher certainty = more edge
    if p <= LONGSHOT_THRESHOLD:
        # Deeper longshots: more overpriced, more edge fading them
        depth = (LONGSHOT_THRESHOLD - p) / LONGSHOT_THRESHOLD   # 0 at boundary, 1 at p=0
        depth_mult = 1.0 + 0.25 * depth                         # 1.00 → 1.25
    else:
        # Deeper certainties: more underpriced, more edge backing them
        depth = (p - CERTAINTY_THRESHOLD) / (1 - CERTAINTY_THRESHOLD)  # 0 at boundary, 1 at p=1
        depth_mult = 1.0 + 0.25 * depth                                 # 1.00 → 1.25

    # Factor 2: narrative salience — emotionally charged longshots are MORE overpriced
    # (retail dreams harder → price is more inflated → our NO is cheaper → more edge)
    narrative_keywords = (
        "miracle", "dark horse", "upset", "comeback", "surprise", "shock",
        "unexpected", "against all odds", "long shot", "longshot", "underdog",
        "wildcard", "wild card", "unlikely", "improbable", "remote chance",
        "outsider", "unprecedented",
    )
    if any(w in q for w in narrative_keywords):
        narrative_mult = 1.15   # narrative hype inflates price → more edge for us
    elif any(w in q for w in ("guarantee", "certain", "inevitable", "lock",
                               "foregone", "obvious", "clear", "definite")):
        narrative_mult = 1.10   # certainty framing but still not priced at 100%
    else:
        narrative_mult = 1.00

    # Factor 3: resolution clarity — objective criteria → cleaner edge
    clarity_good = ("official", "announced", "confirmed", "recorded", "reported",
                    "signed", "published", "voted", "declared", "certified")
    clarity_bad  = ("widely considered", "generally accepted", "consensus",
                    "deemed", "regarded as", "seen as")
    if any(w in q for w in clarity_good):
        clarity_mult = 1.05
    elif any(w in q for w in clarity_bad):
        clarity_mult = 0.90   # ambiguous resolution → noisy edge
    else:
        clarity_mult = 1.00

    return min(1.30, max(0.70, depth_mult * narrative_mult * clarity_mult))


def compute_signal(market) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    INVERTED from the standard framework:
      - buy NO  when p <= LONGSHOT_THRESHOLD  (fade the overpriced longshot)
      - buy YES when p >= CERTAINTY_THRESHOLD (back the underpriced near-certainty)

    Conviction for NO (fading longshot):
      The deeper the longshot, the more overpriced it is, the more we bet.
      conviction = (LONGSHOT_THRESHOLD - p) / LONGSHOT_THRESHOLD
      At p=0%: conviction=1.0 → MAX_POSITION.
      At p=LONGSHOT_THRESHOLD: conviction=0.0 → MIN_TRADE floor.

    Conviction for YES (backing near-certainty):
      The higher the probability above CERTAINTY_THRESHOLD, the more underpriced.
      conviction = (p - CERTAINTY_THRESHOLD) / (1 - CERTAINTY_THRESHOLD)
      At p=100%: conviction=1.0 → MAX_POSITION.
      At p=CERTAINTY_THRESHOLD: conviction=0.0 → MIN_TRADE floor.
    """
    p = market.current_probability
    q = market.question

    # Spread gate — wide spreads eat into the statistical edge
    if market.spread_cents is not None and market.spread_cents / 100 > MAX_SPREAD:
        return None, 0, f"Spread {market.spread_cents/100:.1%} > {MAX_SPREAD:.1%}"

    # Days-to-resolution gate — avoid near-resolution noise where prices
    # may have already started converging (reducing the bias)
    if market.resolves_at:
        try:
            resolves = datetime.fromisoformat(market.resolves_at.replace("Z", "+00:00"))
            days = (resolves - datetime.now(timezone.utc)).days
            if days < MIN_DAYS:
                return None, 0, f"Only {days}d to resolve — bias may have converged"
        except Exception:
            pass

    mult = _longshot_quality_mult(q, p)

    # FADE THE LONGSHOT — buy NO when market overprices a rare event
    if p <= LONGSHOT_THRESHOLD:
        conviction = min(1.0, (LONGSHOT_THRESHOLD - p) / LONGSHOT_THRESHOLD * mult)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = LONGSHOT_THRESHOLD - p
        return (
            "no", size,
            f"LONGSHOT-FADE NO p={p:.1%} edge={edge:.1%} mult={mult:.2f}x "
            f"size=${size} — {q[:65]}"
        )

    # BACK THE NEAR-CERTAINTY — buy YES when market underprices a likely event
    if p >= CERTAINTY_THRESHOLD:
        conviction = min(1.0, (p - CERTAINTY_THRESHOLD) / (1 - CERTAINTY_THRESHOLD) * mult)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = p - CERTAINTY_THRESHOLD
        return (
            "yes", size,
            f"CERTAINTY-BACK YES p={p:.1%} edge={edge:.1%} mult={mult:.2f}x "
            f"size=${size} — {q[:65]}"
        )

    return None, 0, (
        f"Neutral {p:.1%} — outside longshot(<={LONGSHOT_THRESHOLD:.0%}) "
        f"and certainty(>={CERTAINTY_THRESHOLD:.0%}) bands"
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
            print(f"  [warn] {w}")
    except Exception as e:
        print(f"  [ctx] {market_id}: {e}")
    return True, "ok"


def get_client(live: bool = False) -> SimmerClient:
    """
    live=False → venue="sim"  (paper trades — safe default).
    live=True  → venue="polymarket" (real trades, only with --live flag).
    """
    global _client
    global MAX_POSITION, MIN_VOLUME, MAX_SPREAD, MIN_DAYS, MAX_POSITIONS
    global MIN_TRADE, LONGSHOT_THRESHOLD, CERTAINTY_THRESHOLD
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
        MAX_POSITION        = float(os.environ.get("SIMMER_MAX_POSITION",        str(MAX_POSITION)))
        MIN_VOLUME          = float(os.environ.get("SIMMER_MIN_VOLUME",          str(MIN_VOLUME)))
        MAX_SPREAD          = float(os.environ.get("SIMMER_MAX_SPREAD",          str(MAX_SPREAD)))
        MIN_DAYS            = int(os.environ.get(  "SIMMER_MIN_DAYS",            str(MIN_DAYS)))
        MAX_POSITIONS       = int(os.environ.get(  "SIMMER_MAX_POSITIONS",       str(MAX_POSITIONS)))
        MIN_TRADE           = float(os.environ.get("SIMMER_MIN_TRADE",           str(MIN_TRADE)))
        LONGSHOT_THRESHOLD  = float(os.environ.get("SIMMER_LONGSHOT_THRESHOLD",  str(LONGSHOT_THRESHOLD)))
        CERTAINTY_THRESHOLD = float(os.environ.get("SIMMER_CERTAINTY_THRESHOLD", str(CERTAINTY_THRESHOLD)))
    return _client


def find_markets(client: SimmerClient) -> list:
    """Find active markets via broad keyword sweep, deduplicated."""
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


def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    print(
        f"[polymarket-longshot-bias-trader] mode={mode} "
        f"longshot<={LONGSHOT_THRESHOLD:.0%} certainty>={CERTAINTY_THRESHOLD:.0%} "
        f"max_pos=${MAX_POSITION}"
    )

    client  = get_client(live=live)
    markets = find_markets(client)
    print(f"[polymarket-longshot-bias-trader] {len(markets)} candidate markets")

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
            print(f"  [trade] {side.upper()} ${size} {tag} {status} — {reasoning[:75]}")
            if r.success:
                placed += 1
        except Exception as e:
            print(f"  [error] {m.id}: {e}")

    print(f"[polymarket-longshot-bias-trader] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description=(
            "Exploits longshot bias: fades overpriced low-probability markets (buy NO), "
            "backs underpriced near-certainties (buy YES). "
            "The most documented anomaly in betting research, now systematized."
        )
    )
    ap.add_argument("--live", action="store_true",
                    help="Real trades on Polymarket. Default is paper (sim) mode.")
    run(live=ap.parse_args().live)
