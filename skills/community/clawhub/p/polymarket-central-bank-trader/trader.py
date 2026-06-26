"""
polymarket-central-bank-trader
Trades Polymarket prediction markets on central bank decisions, interest rates, inflation prints, and Fed/ECB/Riksbank policy moves.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag.
"""
import os
import argparse
from datetime import datetime, timezone, date
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-central-bank-trader"
SKILL_SLUG   = "polymarket-central-bank-trader"

KEYWORDS = [
    'Federal Reserve', 'Fed rate', 'FOMC', 'interest rate', 'rate cut', 'rate hike',
    'basis points', 'Fed funds rate', 'ECB', 'Bank of England', 'Riksbank', 'BOJ',
    'Bank of Japan', 'RBA', 'Norges Bank', 'inflation', 'CPI', 'PCE', 'core CPI',
    'Jerome Powell', 'Christine Lagarde', 'dot plot', 'forward guidance',
    'quantitative easing', 'QE', 'quantitative tightening', 'QT', 'yield curve',
    'inverted yield curve', 'recession', 'soft landing', 'stagflation',
    'non-farm payroll', 'NFP', 'unemployment rate', 'Sahm Rule', 'pivot',
    'emergency rate cut', 'inter-meeting', 'Jackson Hole',
]

# Risk parameters — declared as tunables in clawhub.json, adjustable from Simmer UI.
# Named SIMMER_* so apply_skill_config() can load automaton-managed overrides.
MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  "35"))
MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    "15000"))
MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.07"))
MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      "5"))
MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "6"))
# Signal thresholds — buy YES below YES_THRESHOLD, sell NO above NO_THRESHOLD.
# Position size scales with conviction, adjusted by question tractability and
# position in the FOMC communication cycle (blackout vs. Fedspeak vs. post-meeting).
YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.38"))
NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",  "0.62"))
MIN_TRADE      = float(os.environ.get("SIMMER_MIN_TRADE",     "5"))

# FOMC decision dates (day the statement drops — second day of two-day meetings).
# Blackout starts 10 calendar days before each date.
# Published by the Federal Reserve Board at least one year in advance.
_FOMC_DECISION_DATES = [
    date(2026, 1, 29),
    date(2026, 3, 19),
    date(2026, 4, 30),
    date(2026, 6, 18),
    date(2026, 7, 30),
    date(2026, 9, 17),
    date(2026, 10, 29),
    date(2026, 12, 10),
    date(2027, 1, 29),
    date(2027, 3, 18),
    date(2027, 4, 29),
    date(2027, 6, 17),
    date(2027, 7, 29),
    date(2027, 9, 16),
    date(2027, 10, 28),
    date(2027, 12, 9),
]

# Quarterly SEP (dot plot) meetings: March, June, September, December.
# Fresh median dot = the Fed's own official rate path for the year.
_SEP_MONTHS = {3, 6, 9, 12}

_client: SimmerClient | None = None


def _fomc_cycle() -> tuple[str, float]:
    """
    Return (label, cycle_mult) based on position in the FOMC communication cycle.

    The Fed's communication cycle has three structurally distinct phases:

    POST-MEETING (0–5 days after decision):
      Maximum information density. The statement is public, the press conference
      transcript is indexed, and — in SEP months (Mar/Jun/Sep/Dec) — the dot plot
      gives the Fed's own median rate projection for the next 3 years. This is the
      window where CME FedWatch futures and Polymarket converge fastest. Trade with
      maximum conviction → 1.20x.

    FEDSPEAK WINDOW (11–20 days before next meeting):
      Fed officials speak freely and deliberately telegraph the upcoming decision.
      The Fed's 'no surprise' doctrine means this window is when forward guidance
      is sharpest — officials explicitly say 'the bar for a cut is high' or
      'conditions support further adjustment.' Retail hears the same speech but
      cannot translate Fedspeak into probability shifts → 1.15x.

    BLACKOUT (1–10 days before decision):
      The Fed imposes a strict communication blackout ~10 days before each meeting.
      No official can comment on monetary policy. The last forward guidance is
      already priced; no new signal can arrive. Rate decision markets under blackout
      are at maximum staleness — the signal quality drops sharply → 0.85x.

    MID-CYCLE (everything else):
      Normal inter-meeting period. Occasional Fedspeak but no concentrated signal
      density. Trade at base conviction → 1.00x.
    """
    today = datetime.now(timezone.utc).date()
    for fomc_date in sorted(_FOMC_DECISION_DATES):
        days_to = (fomc_date - today).days
        if days_to < -5:
            continue  # past meeting; skip to next
        if days_to <= 0:
            # 0-5 days after meeting (days_to is 0 or -1 to -5)
            label = f"post-FOMC({fomc_date.strftime('%b %d')})"
            # Extra boost if this is a SEP (dot plot) meeting
            dot_boost = 0.05 if fomc_date.month in _SEP_MONTHS else 0.0
            return label, 1.20 + dot_boost
        if days_to <= 10:
            return f"blackout({fomc_date.strftime('%b %d')})", 0.85
        if days_to <= 20:
            return f"fedspeak({fomc_date.strftime('%b %d')})", 1.15
        return f"mid-cycle({fomc_date.strftime('%b %d')})", 1.00
    return "mid-cycle", 1.00


def _data_calendar_overlay(question: str) -> float:
    """
    Secondary timing boost based on proximity to scheduled macro data releases.
    Compounds with FOMC cycle mult by returning an additional overlay multiplier.

    BLS CPI: released ~12th–15th of each month at 8:30 AM ET
    BEA PCE: released last week of month (25th+) at 8:30 AM ET
    BLS NFP: released first Friday (~1st–7th) at 8:30 AM ET
    """
    day = datetime.now(timezone.utc).day
    q = question.lower()

    is_inflation = any(w in q for w in ("cpi", "pce", "inflation", "core inflation",
                                          "price level", "consumer price", "deflation"))
    is_labor = any(w in q for w in ("unemployment", "nfp", "payroll", "jobs report",
                                      "labor market", "job gains", "sahm"))
    is_rate = any(w in q for w in ("rate cut", "rate hike", "rate hold", "basis points",
                                     "fed funds", "fomc", "rate decision"))

    in_cpi_window = 10 <= day <= 17   # BLS CPI release window
    in_pce_window = day >= 25          # BEA PCE release window
    in_nfp_window = 1 <= day <= 7     # BLS NFP release window

    if is_inflation and in_cpi_window:
        return 1.20  # CPI week: most market-moving data print; retail anchors to prior reading
    if is_inflation and in_pce_window:
        return 1.15  # PCE week: Fed's preferred measure; forward guidance recalibrates
    if is_labor and in_nfp_window:
        return 1.15  # NFP week: labor market signal shapes rate path for multiple meetings
    if is_rate and (in_cpi_window or in_pce_window or in_nfp_window):
        return 1.10  # Rate decision market during any major data week: signal freshest
    return 1.0


def central_bank_bias(question: str) -> float:
    """
    Returns a conviction multiplier (0.70–1.40) combining three structural edges
    unique to central bank and monetary policy prediction markets:

    1. QUESTION TYPE TRACTABILITY
       Monetary policy is the most heavily telegraphed policy in modern finance.
       The Fed's 'no surprise' doctrine — communicating intent weeks in advance
       to avoid market disruption — means near-term decisions are, by design,
       nearly pre-determined from public data. The tractability scale:

       Next-meeting rate decision (1–2 meetings out)              → 1.25x
         CME FedWatch federal funds futures have ~95% accuracy for
         decisions where futures price ≥85% probability. The Fed holds
         this track record deliberately — surprising markets destroys the
         credibility of forward guidance. Retail prices Polymarket at 75%
         when futures say 92%; that 17-point gap is structural edge.

       CPI / PCE inflation print hitting specific level            → 1.20x
         BLS CPI and BEA PCE are measured to two decimal places.
         Cleveland Fed CPI Nowcast gives a real-time estimate updated
         daily using bond market inflation expectations and commodity
         prices — consistently within 0.1pp of the final print. Retail
         anchors to the prior month's number and doesn't check nowcasts.

       Year-end Fed funds rate target / annual cut count           → 1.15x
         The dot plot (median projection) gives the Fed's own central
         tendency. The CME FedWatch futures curve gives market-implied
         path through every remaining meeting of the year. Both are
         public, precise, and almost never read by Polymarket traders.

       Yield curve inversion / un-inversion by date               → 1.10x
         FRED publishes 10Y-2Y and 10Y-3M spreads daily. Duration and
         direction predictable from Fed path; retail treats yield curve
         questions as abstract rather than trackable.

       Recession declaration / GDP contraction by date             → 0.80x
         NBER's official recession declaration takes 6–18 months after
         the actual peak — it is backward-looking by definition. The
         Sahm Rule (real-time recession indicator, triggers when 3-month
         unemployment average rises 0.5pp above prior 12-month low) is
         a far better predictor, but virtually unknown to retail.
         Markets for 'recession by X' are chronically mis-sized because
         the resolution criteria (NBER) lags the signal (Sahm) by a year.

       Chair fired / resign / succession                           → 0.75x
         Technically a political question once it reaches Polymarket.
         Fed independence norms are strong (only one removal in modern
         history — forced or otherwise) but political risk is real.
         Resolution timing is entirely in executive/legislative hands.

       Emergency / inter-meeting rate action                       → 0.70x
         The most reliably overpriced category in monetary policy markets.
         Emergency inter-meeting cuts happened in 2001 (9/11), 2008
         (financial crisis), and 2020 (COVID) — three events in 25 years.
         Retail overprices in every crisis because those three moments
         are vivid and salient. In any given 3-month window the base
         rate for an emergency cut is near zero even in stressed markets.

    2. FOMC COMMUNICATION CYCLE (computed from official meeting calendar)
       The Fed's communication cycle creates predictable windows of high and
       low information quality:
       - Post-meeting (0–5 days): 1.20x (+0.05 in SEP/dot-plot months)
       - Fedspeak window (11–20 days before): 1.15x
       - Blackout (1–10 days before): 0.85x
       - Mid-cycle: 1.00x

    3. DATA CALENDAR OVERLAY
       Inflation and labor market questions get an additional boost during
       the release windows for CPI (10th–17th), PCE (25th+), and NFP (1st–7th).
       Peak: CPI release week for inflation questions → 1.20x overlay.

    All three factors compound; capped at 1.40x.
    Next-meeting cut + post-SEP-FOMC + CPI week: 1.25 × 1.25 × 1.20 → 1.40x cap.
    Emergency cut any time: 0.70x — near MIN_TRADE floor.
    Blackout + recession: 0.80 × 0.85 = 0.68 → near floor.
    """
    q = question.lower()

    # Factor 1: question type tractability
    if any(w in q for w in ("rate cut", "rate hike", "rate hold", "basis points",
                              "fed funds", "fomc decision", "rate decision",
                              "cut rates", "hike rates", "pause", "skip",
                              "25bp", "50bp", "75bp", "hold rates")):
        type_mult = 1.25  # No-surprise doctrine; futures track record ~95% near-term

    elif any(w in q for w in ("cpi", "pce", "inflation", "consumer price",
                               "core inflation", "deflation", "price level",
                               "above 3%", "below 2%", "2% target")):
        type_mult = 1.20  # Measured precisely; Cleveland Fed nowcast within 0.1pp

    elif any(w in q for w in ("year-end rate", "fed funds rate by", "rate by december",
                               "rate cuts this year", "rate hikes this year",
                               "how many cuts", "how many hikes", "dot plot",
                               "end of year rate", "rate target by")):
        type_mult = 1.15  # Dot plot + futures curve both public and precise

    elif any(w in q for w in ("yield curve", "inverted", "uninvert", "10-year",
                               "2-year spread", "10y-2y", "10y-3m", "term premium",
                               "treasury spread")):
        type_mult = 1.10  # FRED daily; duration predictable from rate path

    elif any(w in q for w in ("recession", "gdp contraction", "two quarters",
                               "negative growth", "nber", "sahm", "downturn")):
        type_mult = 0.80  # NBER lags 6-18 months; Sahm Rule unknown to retail

    elif any(w in q for w in ("powell", "lagarde", "chair", "governor", "fired",
                               "resign", "reappoint", "nomination", "succession",
                               "replace the fed", "fed chair")):
        type_mult = 0.75  # Political question; norm protection strong but not certain

    elif any(w in q for w in ("emergency cut", "emergency rate", "inter-meeting",
                               "unscheduled", "surprise cut", "surprise hike",
                               "emergency meeting")):
        type_mult = 0.70  # Three times in 25 years; retail overprices in every crisis

    else:
        type_mult = 1.0

    # Factor 2: FOMC communication cycle
    _, cycle_mult = _fomc_cycle()
    cycle_mult = min(1.25, cycle_mult)  # clamp individual factor

    # Blackout dampens rate-decision markets most; less impact on inflation/recession questions
    is_rate_question = any(w in q for w in ("rate cut", "rate hike", "fomc", "basis points",
                                              "fed funds", "rate decision", "cut rates",
                                              "hike rates", "year-end rate", "how many cuts"))
    if not is_rate_question:
        # For non-rate questions, blackout matters less; mid-cycle toward baseline
        cycle_mult = max(cycle_mult, 1.0) if cycle_mult < 1.0 else cycle_mult

    # Factor 3: Data calendar overlay — additional boost during release windows
    data_mult = _data_calendar_overlay(question)

    raw = type_mult * cycle_mult * data_mult
    return min(1.40, raw)


def compute_signal(market) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    Conviction-based sizing with Fed communication cycle awareness:
    - Base conviction scales linearly with distance from threshold
    - central_bank_bias() applies three compounding structural edges:
      (1) question tractability — near-term rate decisions are near-certain from
          CME FedWatch futures; retail still prices them as uncertain
      (2) FOMC cycle position — maximum conviction post-meeting (fresh guidance,
          dot plot); minimum conviction during blackout (no new signal possible)
      (3) data calendar overlay — CPI/PCE/NFP release weeks boost inflation and
          rate-decision markets when data is freshest
    - Emergency cut / recession / chair questions dampened — rare events and
      backward-looking definitions structurally inflate retail pricing
    - Result capped at 1.0 so size never exceeds MAX_POSITION
    - MIN_TRADE floor prevents trivially small orders near the boundary

    Remix: wire CME FedWatch probability directly into p — when FedWatch says 92%
    and Polymarket says 75%, the 17-point arbitrage is structural, not random.
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

    bias = central_bank_bias(q)

    if p <= YES_THRESHOLD:
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
    fomc_label, _ = _fomc_cycle()
    sep_tag = " +dot-plot" if datetime.now(timezone.utc).month in _SEP_MONTHS else ""
    print(f"[polymarket-central-bank-trader] mode={mode} max_pos=${MAX_POSITION} min_vol=${MIN_VOLUME} fomc={fomc_label}{sep_tag}")

    client  = get_client(live=live)
    markets = find_markets(client)
    print(f"[polymarket-central-bank-trader] {len(markets)} candidate markets")

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

    print(f"[polymarket-central-bank-trader] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Trades Polymarket prediction markets on central bank decisions, interest rates, inflation prints, and Fed/ECB/Riksbank policy moves.")
    ap.add_argument("--live", action="store_true",
                    help="Real trades on Polymarket. Default is paper (sim) mode.")
    run(live=ap.parse_args().live)
