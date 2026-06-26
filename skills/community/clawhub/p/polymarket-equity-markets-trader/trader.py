"""
polymarket-equity-markets-trader
Trades Polymarket prediction markets on stock index milestones, major IPOs,
earnings surprises, analyst upgrades, and company-specific financial events.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag.
"""
import os
import argparse
from datetime import datetime, timezone
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-equity-markets-trader"
SKILL_SLUG   = "polymarket-equity-markets-trader"

KEYWORDS = [
    'S&P 500', 'Dow Jones', 'Nasdaq', 'stock market', 'bull market', 'bear market',
    'market crash', 'correction', 'IPO', 'earnings', 'revenue miss', 'beat',
    'Berkshire', 'Warren Buffett', 'Apple earnings', 'Tesla earnings',
    'Nvidia earnings', 'stock split', 'buyback', 'dividend', 'short squeeze',
    'all-time high', 'market cap trillion', 'index rebalance', 'EPS beat',
    'earnings surprise', 'guidance raised', 'revenue beat', 'beat estimates',
    'CPI', 'inflation', 'non-farm payroll', 'NFP', 'Fed rate', 'FOMC',
    'recession', 'bear market', 'VIX', 'volatility', 'circuit breaker',
]

# Risk parameters — declared as tunables in clawhub.json, adjustable from Simmer UI.
# Named SIMMER_* so apply_skill_config() can load automaton-managed overrides.
MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  "35"))
MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    "15000"))
MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.07"))
MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      "3"))
MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "8"))
# Signal thresholds — buy YES below YES_THRESHOLD, sell NO above NO_THRESHOLD.
# Position size scales with conviction, adjusted by event type, earnings base
# rates, and macro calendar timing.
YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.38"))
NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",  "0.62"))
MIN_TRADE      = float(os.environ.get("SIMMER_MIN_TRADE",     "5"))

# Earnings season: companies report Q1 (Apr–May), Q2 (Jul–Aug),
# Q3 (Oct–Nov), Q4 (Jan–Feb). Signal density peaks in these months.
_EARNINGS_SEASON_MONTHS = {1, 2, 4, 5, 7, 8, 10, 11}

# Quarter-start months (Jan, Apr, Jul, Oct) have maximum macro data density:
# GDP advance estimate, earnings flood, FOMC meetings, and NFP all land.
_HIGH_MACRO_MONTHS = {1, 4, 7, 10}

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


def equity_bias(question: str) -> float:
    """
    Returns a conviction multiplier (0.65–1.40) combining two structural edges
    unique to equity prediction markets:

    1. MARKET TYPE / EARNINGS BASE RATE CORRECTION
       Equity markets run in parallel with the deepest, most quantified financial
       markets in the world. The edge on Polymarket is the LAG: retail prices
       equity outcomes using headlines and gut feeling while professional data
       (options implied volatility, earnings base rates, futures term structure)
       is sitting in public databases they never check.

       Large-cap tech earnings beat (NVDA, AAPL, MSFT, META, GOOG, AMZN) → 1.25x
         These companies beat Wall Street consensus EPS estimates ~80–85% of the
         time, sustained across multiple years. Nvidia beat consensus 7 consecutive
         quarters 2022–2024. Apple beats ~80%. Meta beats ~85%. Retail prices
         these as ~50–60% likely to beat — a 20–30 percentage point gap that
         is pure edge. Options implied volatility (available free from Yahoo
         Finance) gives a precise probability band for the earnings move; Polymarket
         consistently misprices vs the options-implied range.

       General S&P 500 earnings beat (any large company)           → 1.15x
         The most underknown stat in all of equity markets: S&P 500 companies
         beat analyst consensus EPS estimates approximately 73–75% of the time
         historically. This rate has been consistent across multiple cycles.
         Retail has no idea. They price earnings beats as coin flips. Every
         "will X beat earnings?" market is a structural YES lean unless the
         company has a specific documented miss history.

       Index level milestone (S&P 500, Nasdaq, Dow reaching X)    → 1.15x
         S&P 500 futures market is a 24-hour reference. Polymarket markets on
         index thresholds take 20–60 minutes to reprice after major macro
         catalysts (CPI prints, payrolls, FOMC decisions). This is especially
         large during pre-market hours when futures have already moved but
         Polymarket participants haven't absorbed the move yet.

       Dividend / buyback / stock split announcement               → 0.90x
         Corporate decisions with some information leakage (insider buying
         patterns, SEC pre-disclosure windows) but timing is genuinely
         uncertain. Trade with moderate caution.

       IPO by date / IPO valuation milestone                       → 0.85x
         Banker and market-condition driven. IPO windows are real but timing
         within a window is hard to predict. S-1 filing dates are public but
         the gap from filing to pricing is highly variable.

       Market crash / correction / bear market by date             → 0.75x
         The single most reliably overpriced category in equity prediction
         markets. "Will the S&P fall 20% by X?" Retail dramatically overprices
         crash scenarios for any specific calendar window because crashes are
         vivid and memorable but statistically rare in any given period.
         VIX-spike periods create especially overcrowded crash markets — retail
         fears anchor to the worst case when mean reversion is the more likely
         outcome.

       Short squeeze / meme stock milestone                        → 0.65x
         Pure retail sentiment and social media coordination. GME/AMC-style
         squeezes require specific short float data, borrow rate spikes, and
         coordinated retail buying — all of which are impossible to predict
         from the question text alone. Lowest edge category in equity markets.

    2. EARNINGS CALENDAR TIMING
       Earnings beat/miss markets have dramatically stronger signal during
       earnings season. Outside earnings season, only pre-announcements and
       guidance updates trickle in — the market lacks the data density to
       price these questions accurately, which means the base rate edge
       (73–75% beat rate) is noisier and less actionable.

       Earnings-type question + peak season (Jan, Feb, Apr, May, Jul, Aug, Oct, Nov)
         → 1.20x: Maximum signal density; options implied vol is fresh; analyst
         estimates are current; company guidance is recent.

       Earnings-type question + off-season (Mar, Jun, Sep, Dec)
         → 0.85x: Sparse data; retail prices on stale information from
         last quarter; estimates drift.

       Index/macro question + quarter-start month (Jan, Apr, Jul, Oct)
         → 1.10x: GDP advance estimate + earnings flood + FOMC + NFP all land
         in quarter-start months. Maximum macro catalyst density.

    Combined and capped at 1.40x.
    Large-cap tech earnings in peak season: 1.25 × 1.20 = 1.40x cap — maximum edge.
    Market crash question any time: 0.75x — always trade defensively.
    Short squeeze: 0.65x — near MIN_TRADE floor regardless of probability.
    """
    month = datetime.now(timezone.utc).month
    q = question.lower()

    # Factor 1: market type / earnings base rate
    if any(w in q for w in ("nvidia", "nvda earnings", "nvda beat", "apple earnings",
                             "aapl earnings", "microsoft earnings", "msft earnings",
                             "meta earnings", "google earnings", "alphabet earnings",
                             "amazon earnings", "amzn earnings", "tesla earnings",
                             "tsla earnings")):
        type_mult = 1.25  # ~80-85% beat rate; options market precise; retail prices 50-60%

    elif any(w in q for w in ("earnings beat", "beat estimates", "beat expectations",
                               "eps beat", "revenue beat", "earnings surprise",
                               "beat consensus", "guidance raised", "guidance above",
                               "earnings miss", "miss estimates")):
        type_mult = 1.15  # S&P 500 ~73-75% beat rate — retail has no idea

    elif any(w in q for w in ("s&p 500", "s&p500", "spx ", "nasdaq", "dow jones",
                               "dow ", "nikkei", "ftse", "dax ", "all-time high",
                               "market cap trillion", "index level", "index milestone",
                               "reach 5000", "reach 6000", "reach 7000", "reach 8000",
                               "reach 20000", "reach 30000")):
        type_mult = 1.15  # Futures market reference; Polymarket lags macro catalysts 20-60 min

    elif any(w in q for w in ("dividend", "buyback", "stock split", "share repurchase",
                               "special dividend", "capital return")):
        type_mult = 0.90  # Some leakage signal but timing uncertain

    elif any(w in q for w in ("ipo", "initial public offering", "go public",
                               "direct listing", "spac ", "s-1 filing",
                               "ipo by", "ipo this year")):
        type_mult = 0.85  # Window-driven but precise timing hard

    elif any(w in q for w in ("market crash", "crash by", "stock market crash",
                               "bear market", "recession by", "market collapse",
                               "circuit breaker", "trading halt", "black swan",
                               "20% drop", "30% drop", "market bottom")):
        type_mult = 0.75  # Retail systematically overprices crash for any specific period

    elif any(w in q for w in ("short squeeze", "meme stock", "gamestop", "gme ",
                               "amc ", "wallstreetbets", "wsb ", "roaring kitty",
                               "most shorted", "short interest")):
        type_mult = 0.65  # Social coordination unpredictable; lowest edge category

    else:
        type_mult = 1.0

    # Factor 2: earnings calendar timing
    earnings_keywords = ("earnings", "eps", "revenue beat", "guidance", "quarterly results",
                         "beat estimates", "beat expectations", "earnings surprise",
                         "q1 results", "q2 results", "q3 results", "q4 results")
    is_earnings_type = any(w in q for w in earnings_keywords)

    index_keywords = ("s&p", "nasdaq", "dow", "nikkei", "ftse", "dax", "index",
                      "market cap", "all-time high")
    is_index_type = any(w in q for w in index_keywords)

    if is_earnings_type:
        if month in _EARNINGS_SEASON_MONTHS:
            calendar_mult = 1.20  # Peak season: fresh estimates, current guidance, live options vol
        else:
            calendar_mult = 0.85  # Off-season: stale data, sparse pre-announcements
    elif is_index_type and month in _HIGH_MACRO_MONTHS:
        calendar_mult = 1.10  # Quarter-start: GDP + earnings flood + FOMC maximum density
    else:
        calendar_mult = 1.0

    return min(1.40, type_mult * calendar_mult)


def compute_signal(market) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    Conviction-based sizing with earnings base rate correction and calendar timing:
    - Base conviction scales linearly with distance from threshold
    - equity_bias() corrects for the most important underknown stat in equity
      markets: S&P 500 companies beat consensus ~73-75% of the time; large-cap
      tech ~80-85%. Retail prices these as coin flips. Every earnings beat market
      is a structural YES lean during earnings season.
    - Calendar multiplier: peak earnings season (1.20x) vs off-season (0.85x)
    - Crash/meme markets dampened (0.65-0.75x) — narrative overpricing
    - Result capped at 1.0 so size never exceeds MAX_POSITION
    - MIN_TRADE floor prevents trivially small orders near the boundary

    Remix: feed options market implied earnings move (from Yahoo Finance options
    chain) into p — the options-implied probability is far more precise than
    Polymarket retail pricing for earnings beat/miss questions.
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

    bias = equity_bias(q)

    if p <= YES_THRESHOLD:
        # conviction=0 at threshold boundary, conviction=1 at p=0 — scaled by equity bias
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
    month = datetime.now(timezone.utc).month
    earnings_season = "PEAK" if month in _EARNINGS_SEASON_MONTHS else "off-season"
    print(f"[polymarket-equity-markets-trader] mode={mode} max_pos=${MAX_POSITION} min_vol=${MIN_VOLUME} max_spread={MAX_SPREAD:.0%} earnings={earnings_season}")

    client  = get_client(live=live)
    markets = find_markets(client)
    print(f"[polymarket-equity-markets-trader] {len(markets)} candidate markets")

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

    print(f"[polymarket-equity-markets-trader] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Trades Polymarket prediction markets on stock index milestones, major IPOs, earnings surprises, and company-specific financial events.")
    ap.add_argument("--live", action="store_true",
                    help="Real trades on Polymarket. Default is paper (sim) mode.")
    run(live=ap.parse_args().live)
