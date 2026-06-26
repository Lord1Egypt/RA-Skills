"""
polymarket-coffee-trader
Trades Polymarket markets on coffee prices, production, and weather events
by exploiting seasonal mispricings unique to the global coffee market.

THE EDGE — THREE STRUCTURAL LAYERS:

1. BRAZIL FROST WINDOW MISPRICING (strongest edge)
   Commercially damaging frost in Brazil's coffee belt (Cerrado Mineiro,
   Sul de Minas, Mogiana) is ONLY physically possible during June–August.
   Retail treats frost risk as a year-round threat. Markets asking "will
   coffee prices spike?" in October or February embed a frost premium that
   is meteorologically impossible to realize — we fade those markets.
   Conversely, during the frost window (especially July, the coldest month
   in Brazil's southern highlands), YES-side markets on price spikes are
   systematically underpriced.

2. BRAZIL HARVEST CYCLE
   Brazil's main arabica harvest runs April–September (on-year) or
   May–August (off-year in the biennial cycle). Post-harvest (Oct–Jan),
   supply is highest and carry-forward stock is well-understood —
   price-spike markets are overpriced. Pre-harvest (Feb–Mar), inventory
   anxiety is real but frost is still months away.

3. LA NIÑA / EL NIÑO REGIME
   La Niña → drought in Brazil's coffee belt → crop stress → higher prices.
   El Niño → excess rainfall → lower quality, logistic disruption in
   Vietnam → Robusta supply squeeze. ENSO-neutral years: standard seasonal
   model. Current ENSO phase is hardcoded but overridable via env var.

Combined, these layers create a conviction multiplier that is applied on
top of the standard threshold-based conviction sizing.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag.
"""
import os
import argparse
from datetime import datetime, timezone
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-coffee-trader"
SKILL_SLUG   = "polymarket-coffee-trader"

KEYWORDS = [
    # Price markets
    "coffee price", "arabica price", "robusta price", "coffee futures",
    "arabica futures", "KC futures", "coffee above", "coffee below",
    "coffee reaches", "coffee exceed",
    # Production / crop
    "coffee production", "coffee crop", "coffee harvest", "coffee yield",
    "brazil coffee", "vietnam coffee", "colombia coffee", "ethiopia coffee",
    "arabica production", "robusta production", "coffee bags", "million bags",
    "coffee output",
    # Weather / events
    "coffee frost", "frost event", "frost damage", "brazil frost",
    "coffee drought", "coffee rainfall", "cerrado", "sul de minas",
    "coffee belt", "coffee freeze",
    # Broader
    "coffee", "arabica", "robusta", "coffee market",
]

# Risk parameters
MAX_POSITION  = float(os.environ.get("SIMMER_MAX_POSITION",  "30"))
MIN_VOLUME    = float(os.environ.get("SIMMER_MIN_VOLUME",    "5000"))
MAX_SPREAD    = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.08"))
MIN_DAYS      = int(os.environ.get(  "SIMMER_MIN_DAYS",      "3"))
MAX_POSITIONS = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "8"))
YES_THRESHOLD = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.38"))
NO_THRESHOLD  = float(os.environ.get("SIMMER_NO_THRESHOLD",  "0.62"))
MIN_TRADE     = float(os.environ.get("SIMMER_MIN_TRADE",     "5"))

# ENSO phase: "la_nina", "el_nino", "neutral"
# La Niña → drought stress in Brazil → bullish coffee.
# El Niño → Vietnam disruption → Robusta squeeze.
# Override via env var when ENSO phase changes (NOAA updates quarterly).
ENSO_PHASE = os.environ.get("SIMMER_ENSO_PHASE", "neutral").lower()

_client: SimmerClient | None = None


def _frost_window_mult() -> tuple[str, float]:
    """
    Return (label, multiplier) based on the Brazil frost calendar.

    Commercially damaging frost in Brazil's coffee belt is ONLY possible
    when polar air masses (friagens) push north from Patagonia into the
    highlands of Minas Gerais, São Paulo, and Paraná. This happens
    exclusively between mid-June and end of August, with peak risk in July.

    Month mapping (UTC, month 1=Jan):
      July (7):              peak frost risk → 1.30x (most YES misprice)
      June (6) / Aug (8):    shoulder frost risk → 1.15x
      May (5) / Sep (9):     marginal — frost impossible but market starts
                             pricing/de-pricing → 1.05x
      Oct (10) – Apr (4):    frost meteorologically impossible → 0.80x
                             (retail still prices residual frost fear)

    Why this creates edge:
    A market priced at 25% asking "will arabica hit $4.50 before Oct?" in
    February embeds frost optionality that cannot physically materialize
    for 4 more months. We fade the YES side. The same market in July,
    after two weeks of polar air mass forecasts for Minas Gerais, should
    be at 40%+. We back YES aggressively.
    """
    month = datetime.now(timezone.utc).month
    if month == 7:
        return "JULY(peak-frost)", 1.30
    if month in (6, 8):
        return "FROST-SHOULDER(Jun/Aug)", 1.15
    if month in (5, 9):
        return "FROST-MARGINAL(May/Sep)", 1.05
    # Oct–Apr: frost impossible
    return f"NO-FROST(month={month})", 0.80


def _harvest_cycle_mult() -> tuple[str, float]:
    """
    Return (label, multiplier) based on Brazil's arabica harvest calendar.

    Brazil harvests on a biennial cycle (on-year = large crop, off-year =
    smaller). Main harvest: April–September. Post-harvest (Oct–Jan) supply
    is plentiful and well-understood — price spikes are less likely.
    Pre-harvest (Feb–Mar): inventory draws down, supply anxiety builds.

    Month mapping:
      Feb–Mar (2–3):  pre-harvest anxiety → 1.10x (supply tightness real)
      Apr–Jun (4–6):  harvest starts, uncertainty about size → 1.05x
      Jul–Sep (7–9):  harvest peak / mid-harvest → 1.00x (combines with frost)
      Oct–Jan (10–1): post-harvest, supply ample → 0.90x
    """
    month = datetime.now(timezone.utc).month
    if month in (2, 3):
        return "PRE-HARVEST(Feb/Mar)", 1.10
    if month in (4, 5, 6):
        return "HARVEST-START(Apr-Jun)", 1.05
    if month in (7, 8, 9):
        return "HARVEST-PEAK(Jul-Sep)", 1.00
    return f"POST-HARVEST(month={month})", 0.90


def _enso_mult(question: str) -> tuple[str, float]:
    """
    Return (label, multiplier) based on ENSO phase and market type.

    La Niña → drought in Brazil's coffee belt → arabica supply stress → bullish.
    El Niño → excessive rain in Vietnam → Robusta logistics disruption → bullish
              for Robusta; also weakens arabica demand from blenders.
    Neutral → standard seasonal model, no ENSO premium.

    Reads ENSO_PHASE global (overridable via SIMMER_ENSO_PHASE env var).
    """
    q = question.lower()
    is_robusta = any(w in q for w in ("robusta", "vietnam", "viet nam"))
    is_arabica = any(w in q for w in ("arabica", "brazil", "colombia", "ethiopia"))

    if ENSO_PHASE == "la_nina":
        if is_robusta:
            return "LA_NINA(robusta-neutral)", 1.00
        return "LA_NINA(arabica-bullish)", 1.15   # drought stress in Brazil
    if ENSO_PHASE == "el_nino":
        if is_robusta:
            return "EL_NINO(robusta-bullish)", 1.15  # Vietnam disruption
        return "EL_NINO(arabica-mixed)", 1.00
    return "ENSO-NEUTRAL", 1.00


def coffee_seasonal_bias(question: str) -> float:
    """
    Returns a conviction multiplier (0.65–1.40) combining the three
    structural seasonal edges unique to coffee prediction markets.

    See individual helper functions for detailed reasoning.
    Combined and capped at 1.40x to prevent runaway sizing.

    Example combinations:
      July + pre-harvest + La Niña + arabica price spike market:
        1.30 × 1.00 × 1.15 = 1.495 → capped at 1.40x

      February + post-harvest + ENSO-neutral + frost market:
        0.80 × 1.10 × 1.00 = 0.88x (frost market in Feb is overpriced)

      October + post-harvest + El Niño + robusta:
        0.80 × 0.90 × 1.15 = 0.828x
    """
    frost_label,    frost_mult    = _frost_window_mult()
    harvest_label,  harvest_mult  = _harvest_cycle_mult()
    enso_label,     enso_mult     = _enso_mult(question)

    combined = frost_mult * harvest_mult * enso_mult
    capped   = min(1.40, max(0.65, combined))

    # Store labels for reasoning string (accessed via module-level last call)
    coffee_seasonal_bias._last_labels = f"{frost_label} × {harvest_label} × {enso_label}"
    return capped


coffee_seasonal_bias._last_labels = ""


def _is_coffee_market(question: str) -> bool:
    """Return True if the question is about coffee prices, production, or events."""
    q = question.lower()
    coffee_terms = ("coffee", "arabica", "robusta", "kc futures", "caffeine")
    return any(t in q for t in coffee_terms)


def compute_signal(market) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    Standard conviction-based sizing with coffee seasonal bias multiplier:
      size = max(MIN_TRADE, conviction × bias × MAX_POSITION)

    The bias can reduce conviction below threshold sizing (0.65x in
    off-season) or amplify it during peak frost window + La Niña (1.40x).
    Result is capped at MAX_POSITION.
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

    # Coffee market gate
    if not _is_coffee_market(q):
        return None, 0, "Not a coffee market"

    bias   = coffee_seasonal_bias(q)
    labels = coffee_seasonal_bias._last_labels

    if p <= YES_THRESHOLD:
        conviction = min(1.0, (YES_THRESHOLD - p) / YES_THRESHOLD * bias)
        size       = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge       = YES_THRESHOLD - p
        return (
            "yes", size,
            f"YES {p:.0%} edge={edge:.0%} bias={bias:.2f}x [{labels}] "
            f"size=${size} — {q[:60]}"
        )

    if p >= NO_THRESHOLD:
        conviction = min(1.0, (p - NO_THRESHOLD) / (1 - NO_THRESHOLD) * bias)
        size       = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge       = p - NO_THRESHOLD
        return (
            "no", size,
            f"NO YES={p:.0%} edge={edge:.0%} bias={bias:.2f}x [{labels}] "
            f"size=${size} — {q[:60]}"
        )

    return None, 0, (
        f"Neutral {p:.1%} — outside {YES_THRESHOLD:.0%}/{NO_THRESHOLD:.0%} bands"
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
    global YES_THRESHOLD, NO_THRESHOLD, MIN_TRADE, ENSO_PHASE
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
        YES_THRESHOLD = float(os.environ.get("SIMMER_YES_THRESHOLD", str(YES_THRESHOLD)))
        NO_THRESHOLD  = float(os.environ.get("SIMMER_NO_THRESHOLD",  str(NO_THRESHOLD)))
        MIN_TRADE     = float(os.environ.get("SIMMER_MIN_TRADE",     str(MIN_TRADE)))
        ENSO_PHASE    = os.environ.get("SIMMER_ENSO_PHASE",          ENSO_PHASE).lower()
    return _client


def find_markets(client: SimmerClient) -> list:
    """Find active coffee markets, deduplicated."""
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
    frost_label,   _ = _frost_window_mult()
    harvest_label, _ = _harvest_cycle_mult()
    mode = "LIVE" if live else "PAPER (sim)"
    print(
        f"[polymarket-coffee-trader] mode={mode} "
        f"frost={frost_label} harvest={harvest_label} enso={ENSO_PHASE} "
        f"max_pos=${MAX_POSITION}"
    )

    client  = get_client(live=live)
    markets = find_markets(client)
    print(f"[polymarket-coffee-trader] {len(markets)} candidate markets")

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

    print(f"[polymarket-coffee-trader] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description=(
            "Trades coffee prediction markets using seasonal frost window, "
            "harvest cycle, and ENSO phase as structural conviction multipliers."
        )
    )
    ap.add_argument("--live", action="store_true",
                    help="Real trades on Polymarket. Default is paper (sim) mode.")
    run(live=ap.parse_args().live)
