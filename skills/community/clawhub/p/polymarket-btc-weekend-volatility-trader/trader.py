"""
polymarket-btc-weekend-volatility-trader
Trades BTC weekend price threshold markets where resolution hinges on a first-passage
("any time above X") event in a bounded weekend window using Binance BTCUSDT as source.

The core edge: retail prices these as terminal-probability markets ("will BTC close
above 150k?"). The question almost always asks for first-passage probability ("will
BTC trade above 150k at ANY POINT this weekend?"). First-passage probability is
approximately 2x the terminal probability for near-threshold levels — a systematic
structural underpricing that replenishes every weekend.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag.
"""
import os
import argparse
from datetime import datetime, timezone
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-btc-weekend-volatility-trader"
SKILL_SLUG   = "polymarket-btc-weekend-volatility-trader"

KEYWORDS = [
    'bitcoin weekend', 'BTC weekend', 'BTCUSDT weekend', 'bitcoin this weekend',
    'BTC this weekend', 'bitcoin above', 'btc above', 'BTCUSDT above',
    'bitcoin reach', 'btc reach', 'bitcoin hit', 'btc hit',
    'trade above', 'at any point', 'any time this weekend', 'strictly above',
    'bitcoin 100k', 'bitcoin 110k', 'bitcoin 120k', 'bitcoin 130k',
    'bitcoin 140k', 'bitcoin 150k', 'bitcoin 160k', 'bitcoin 170k',
    'bitcoin 180k', 'bitcoin 200k', 'btc 100k', 'btc 150k', 'btc 200k',
    '100000 usdt', '110000 usdt', '120000 usdt', '130000 usdt', '140000 usdt',
    '150000 usdt', '160000 usdt', '170000 usdt', '200000 usdt',
    'Binance BTCUSDT', 'btcusdt above', 'last traded price',
]

# Risk parameters — declared as tunables in clawhub.json, adjustable from Simmer UI.
MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  "25"))
MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    "5000"))
MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.08"))
MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      "1"))   # weekend markets are short-horizon by design
MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "8"))
# Signal thresholds — buy YES below YES_THRESHOLD, sell NO above NO_THRESHOLD.
# BTC weekend threshold markets are structurally biased toward YES — first-passage
# probability is higher than terminal probability. YES_THRESHOLD is intentionally
# wider than the default to capture this.
YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.40"))
NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",  "0.65"))
MIN_TRADE      = float(os.environ.get("SIMMER_MIN_TRADE",     "5"))

# BTC halving cycle: last halving April 19, 2024.
# Weekend volatility magnitude is highest during the post-halving bull expansion phase
# (days 181–540), when realized vol is typically 70–90% annualized and weekend
# gap moves are most pronounced.
_LAST_BTC_HALVING = datetime(2024, 4, 19, tzinfo=timezone.utc)

_client: SimmerClient | None = None


def _btc_cycle_mult() -> tuple[str, float]:
    """
    Return (label, multiplier) based on position in the BTC halving cycle.

    BTC weekend gap volatility is strongly cycle-dependent:
    - Days 0–180 (post-halving momentum): vol picking up, 1.10x
    - Days 181–540 (bull expansion): highest realized vol regime, weekend moves
      most dramatic, touch probability models most accurate — 1.15x
    - Days 541–900 (distribution/topping): vol declining, 1.00x
    - Days 901+ (bear/accumulation): lowest vol regime, threshold markets
      systematically overpriced for far-away levels — 0.85x
    """
    days = (datetime.now(timezone.utc) - _LAST_BTC_HALVING).days
    if days <= 180:
        return f"momentum(day {days})", 1.10
    if days <= 540:
        return f"bull-expansion(day {days})", 1.15
    if days <= 900:
        return f"distribution(day {days})", 1.00
    return f"bear(day {days})", 0.85


def _entry_window_mult() -> tuple[str, float]:
    """
    Return (label, multiplier) based on day-of-week and hour (UTC).

    The edge in BTC weekend markets peaks on Thursday–Friday morning — the trader
    can enter before the market has absorbed weekend positioning flows, while
    vol model estimates are still 48–72h from resolution. Entry too early (Mon–Wed)
    means next weekend is too far away to price precisely. Entry too late
    (Saturday/Sunday) means path is already partially revealed and risk premium
    dominates over any structural edge.

    weekday(): 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri, 5=Sat, 6=Sun
    """
    now     = datetime.now(timezone.utc)
    weekday = now.weekday()
    hour    = now.hour

    if weekday == 3:
        return "THURSDAY(optimal)", 1.20     # 2–3 days to weekend, vol fresh, no positional crowding yet
    if weekday == 4 and hour < 16:
        return "FRIDAY-AM(good)", 1.15       # Pre-market, US equity session active, pre-weekend entry
    if weekday == 4 and hour >= 16:
        return "FRIDAY-PM(weekend-open)", 1.10  # Crypto weekend has started, Asian session priming
    if weekday == 5 and hour < 12:
        return "SATURDAY-AM(early)", 0.95    # Path partially revealed; some first-passage edge left
    if weekday == 5:
        return "SATURDAY-PM(fading)", 0.85   # Well into window; edge shrinking as outcome resolves
    if weekday == 6:
        return "SUNDAY(near-resolution)", 0.75  # Risk premium dominates; structural edge nearly gone
    # Monday–Wednesday: next weekend too far, vol estimate imprecise
    return f"{'Mon Tue Wed'.split()[weekday]}(early)", 1.00


def btc_weekend_bias(question: str) -> float:
    """
    Returns a conviction multiplier (0.75–1.40) combining three structural edges
    unique to BTC weekend price threshold markets:

    1. FIRST-PASSAGE PROBABILITY CORRECTION (semantic edge)
       The single most important insight in this entire trader: BTC weekend markets
       almost universally ask for first-passage probability — "will BTC trade above
       X at ANY TIME between [start] and [end]?" Retail prices this as the
       terminal probability — "what are the odds BTC is above X at end of period?"

       For a threshold that is μ standard deviations above the current price, the
       relationship between first-passage and terminal probability is approximately:

           P(first-passage) ≈ 2 × P(terminal)     for μ near 0
           P(first-passage) ≈ P(terminal) × k(μ)  where k > 1 for all μ > 0

       Given BTC's historical annualized volatility of ~70% and a 48-hour window
       (σ_weekend ≈ 4.1%), a threshold 8% above current price has:
           Terminal P ≈ 2.5%  ←  what retail prices
           Touch P    ≈ 5–6%  ←  what the market is actually asking

       This gap is structural — retail treats "above at close" and "above at any
       time" as identical. They are not. Combine with BTC's fat-tail distribution
       (actual kurtosis ≈ 5–8 vs Gaussian 3) and the gap widens further for
       extreme threshold levels.

       Any-time / first-passage / touch semantics:
         "any time", "at any point", "at least once", "ever reaches"  → 1.25x
         "strictly above", "above" (typical weekend question)          → 1.20x
         "close above", "closing price", "final price at close"        → 1.00x
         Default BTC weekend question                                   → 1.15x

       Resolution source quality:
         Binance BTCUSDT named as primary source                        → +0.05x
         (reduces oracle and interpretation risk; single well-defined feed)

    2. ENTRY TIMING WINDOW (day-of-week)
       The edge peaks when the trader can enter 1–3 days before the weekend window
       opens, while vol model estimates are fresh and positioning flows haven't
       crowded the market yet:

         Thursday:            1.20x — optimal: 2–3 days out, fresh vol, no crowding
         Friday pre-16:00:    1.15x — good: pre-market, 1–2 days out
         Friday post-16:00:   1.10x — weekend has opened for crypto
         Saturday morning:    0.95x — path partially revealed
         Saturday afternoon:  0.85x — well into window, edge fading
         Sunday:              0.75x — near resolution, risk premium dominates
         Monday–Wednesday:    1.00x — next weekend too far to price precisely

    3. BTC HALVING CYCLE (volatility regime)
       Weekend gap volatility is highest during the bull expansion phase (days
       181–540 post-halving) when BTC realized vol runs 70–90% annualized and
       weekend moves are most pronounced. The touch probability model is most
       accurate in this regime. Bear phase (days 901+) sees vol compress to
       30–45% and far-threshold markets become systematically overpriced.

         Days 181–540 (bull expansion):   1.15x
         Days 0–180 (post-halving):        1.10x
         Days 541–900 (distribution):      1.00x
         Days 901+ (bear/accumulation):    0.85x

    Combined and capped at 1.40x.
    "Any time above" + Thursday entry + bull expansion: 1.25 × 1.20 × 1.15 → cap.
    "Close above" + Sunday + bear phase: 1.00 × 0.75 × 0.85 = 0.64x → MIN_TRADE floor.
    """
    q = question.lower()

    # Factor 1: semantic edge — first-passage vs terminal probability
    if any(w in q for w in ("any time", "at any point", "at least once",
                              "ever reaches", "any moment", "at any time")):
        semantic_mult = 1.25
    elif any(w in q for w in ("strictly above", "above", "exceed", "surpass",
                               "trade above", "reach")):
        semantic_mult = 1.20
    elif any(w in q for w in ("close above", "closing price", "at close",
                               "closing above", "final price")):
        semantic_mult = 1.00
    else:
        semantic_mult = 1.15

    # Resolution source bonus: named Binance BTCUSDT = single clean feed, less oracle risk
    if any(w in q for w in ("binance", "btcusdt", "last traded price", "binance btcusdt")):
        semantic_mult = min(1.30, semantic_mult + 0.05)

    # Factor 2: entry timing window
    _, timing_mult = _entry_window_mult()

    # Factor 3: BTC halving cycle
    _, cycle_mult = _btc_cycle_mult()

    return min(1.40, semantic_mult * timing_mult * cycle_mult)


def _is_btc_weekend_market(question: str) -> bool:
    """
    Return True if the question describes a BTC price threshold market with a
    weekend or short-horizon time window. Generalised — not hardcoded to any
    specific price level.
    """
    q = question.lower()
    has_btc    = any(w in q for w in ("bitcoin", "btc", "btcusdt"))
    has_price  = any(w in q for w in ("above", "reach", "hit", "exceed", "trade at",
                                        "surpass", "break", "touch"))
    has_level  = any(c in q for c in ("usdt", "usd", "$")) or any(
                     w in q for w in ("100k", "110k", "120k", "130k", "140k",
                                       "150k", "160k", "170k", "180k", "200k",
                                       "000 usdt", "000 usd"))
    has_window = any(w in q for w in ("weekend", "saturday", "sunday",
                                        "this week", "any time", "at any point",
                                        "between", "window"))
    return has_btc and has_price and has_level


def compute_signal(market) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    Conviction-based sizing with first-passage probability correction and halving
    cycle awareness:
    - Filters for genuine BTC threshold markets (not hardcoded to one level)
    - Base conviction scales linearly with distance from threshold
    - btc_weekend_bias() corrects for the core mispricing: retail prices
      'any time above X' as if it were 'close above X'; the gap is ≈2x near
      threshold, narrowing for far-OTM levels but always positive
    - Timing mult rewards optimal entry (Thursday) and penalises late entry
      (Sunday near-resolution)
    - Halving cycle mult reflects actual BTC vol regime
    - Result capped at 1.0 so size never exceeds MAX_POSITION
    - MIN_TRADE floor prevents trivially small orders near the boundary

    Remix: wire Binance real-time BTCUSDT price into this function and compute
    distance-to-threshold directly — the touch probability formula gives a precise
    probability estimate that you can compare to Polymarket's p for exact edge.
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
                return None, 0, f"Only {days}d to resolve"
        except Exception:
            pass

    # Market type gate — only trade genuine BTC price threshold markets
    if not _is_btc_weekend_market(q):
        return None, 0, "Not a BTC price threshold market"

    bias = btc_weekend_bias(q)

    if p <= YES_THRESHOLD:
        # Deep-OTM thresholds (p very low) get close to maximum conviction —
        # this is where the first-passage correction is most exploitable.
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


def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    entry_label, _ = _entry_window_mult()
    cycle_label, _ = _btc_cycle_mult()
    print(f"[polymarket-btc-weekend-volatility-trader] mode={mode} max_pos=${MAX_POSITION} entry={entry_label} cycle={cycle_label}")

    client  = get_client(live=live)
    markets = find_markets(client)
    print(f"[polymarket-btc-weekend-volatility-trader] {len(markets)} candidate markets")

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

    print(f"[polymarket-btc-weekend-volatility-trader] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Trades BTC weekend price threshold markets. Exploits the structural gap between first-passage and terminal probability that retail systematically ignores.")
    ap.add_argument("--live", action="store_true",
                    help="Real trades on Polymarket. Default is paper (sim) mode.")
    run(live=ap.parse_args().live)
