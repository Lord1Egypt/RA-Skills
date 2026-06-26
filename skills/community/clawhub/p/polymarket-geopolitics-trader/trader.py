"""
polymarket-geopolitics-trader
Trades geopolitical prediction markets: wars, ceasefires, sanctions, UN votes, and diplomatic events.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag.
"""
import os
import argparse
from datetime import datetime, timezone
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-geopolitics-trader"
SKILL_SLUG   = "polymarket-geopolitics-trader"

KEYWORDS = [
    'war', 'ceasefire', 'sanctions', 'NATO', 'Ukraine', 'Russia',
    'China', 'Taiwan', 'Iran', 'nuclear', 'UN', 'diplomacy',
    'invasion', 'treaty', 'military', 'missile', 'coup',
    'election interference', 'espionage', 'regime change',
    'Security Council', 'veto', 'peace deal', 'summit',
    'Gaza', 'Israel', 'North Korea', 'DPRK', 'South China Sea',
]

# Risk parameters — declared as tunables in clawhub.json, adjustable from Simmer UI.
# Named SIMMER_* so apply_skill_config() can load automaton-managed overrides.
MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  "30"))
MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    "1000"))
MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.12"))
MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      "0"))
MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "8"))
# Signal thresholds — buy YES below YES_THRESHOLD, sell NO above NO_THRESHOLD.
# Position size scales with conviction, corrected for fear premiums and
# regional news timezone repricing windows.
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
            if m.id not in seen and any(w in q for w in ("war", "ceasefire", "nato", "ukraine",
                    "russia", "china", "taiwan", "iran", "nuclear", "military", "gaza", "israel")):
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
            if m.id not in seen and any(w in q for w in ("war", "ceasefire", "nato", "ukraine",
                    "russia", "china", "taiwan", "iran", "nuclear", "military", "sanction")):
                seen.add(m.id)
                unique.append(m)
    except Exception:
        pass

    return unique


def geopolitics_bias(question: str) -> float:
    """
    Returns a conviction multiplier (0.65–1.35) combining two geopolitical
    structural edges:

    1. FEAR/NARRATIVE PREMIUM CORRECTION
       Retail systematically overprices dramatic, scary outcomes and
       underprices boring but likely ones. Conflict research databases
       (ACLED, ICG) document actual base rates that deviate sharply from
       media-driven market pricing.

       Nuclear / WMD use           → 0.65x  (near-zero modern base rate; media panic inflates)
       Coup / regime change        → 0.75x  (retail overprices drama; ~50% actual success)
       Full invasion / occupation  → 0.80x  (retail overprices escalation to worst case)
       Ceasefire / truce           → 0.80x  (~40% of ceasefires hold within 6 months)
       Sanctions / embargo         → 0.85x  (~30-40% achieve objectives; overestimated)
       Diplomatic breakthrough     → 1.15x  (underpriced — boring, retail ignores)
       UN vote / Security Council  → 1.10x  (procedural; P5 veto patterns predictable)

    2. REGIONAL NEWS TIMING
       Geopolitical news breaks in local time. Polymarket is US-dominated —
       markets take 15–45 min to reprice events that break during Asian or
       European business hours when US retail is asleep or just waking.

       Asia/Pacific events (China, Taiwan, NK, Japan):
         Active 00:00–08:00 UTC → 1.20x  (US asleep, repricing window open)
         US hours 13:00–22:00 UTC → 0.95x  (priced in quickly)

       Europe/Middle East (Ukraine, Russia, Iran, Israel, Gaza, NATO):
         Active 06:00–14:00 UTC → 1.15x  (US just waking, lag window)
         Off-hours 18:00–04:00 UTC → 0.95x  (smaller edge)

    Combined and capped at 1.35x.
    """
    hour_utc = datetime.now(timezone.utc).hour
    q = question.lower()

    # Factor 1: event type fear/base rate correction
    if any(w in q for w in ("nuclear", "nuke", "wmd", "atomic", "radiological",
                             "dirty bomb", "nuclear weapon", "nuclear strike")):
        event_mult = 0.65  # Post-WWII nuclear use base rate is zero — retail panics irrationally

    elif any(w in q for w in ("coup", "regime change", "overthrow", "depose", "topple")):
        event_mult = 0.75  # Dramatic outcome retail overprices; ~50% actual success rate

    elif any(w in q for w in ("full invasion", "full-scale", "ground invasion",
                               "occupy", "annexe", "annex")):
        event_mult = 0.80  # Retail anchors to worst-case escalation; base rates lower

    elif any(w in q for w in ("ceasefire", "peace deal", "truce", "armistice", "peace agreement")):
        event_mult = 0.80  # Only ~40% of ceasefires hold within 6 months; market overprices

    elif any(w in q for w in ("sanction", "embargo", "trade ban")):
        event_mult = 0.85  # ~30-40% achieve stated objectives — effectiveness overestimated

    elif any(w in q for w in ("diplomatic", "negotiation", "talks", "summit",
                               "agreement", "accord", "dialogue")):
        event_mult = 1.15  # Diplomatic progress is boring — retail underprices it

    elif any(w in q for w in ("un vote", "security council", "un resolution",
                               "veto", "general assembly")):
        event_mult = 1.10  # UN procedure is structured; P5 veto patterns well-documented

    else:
        event_mult = 1.0

    # Factor 2: regional news timing window
    # Asia/Pacific — local business hours roughly 00:00-08:00 UTC
    if any(w in q for w in ("china", "taiwan", "north korea", "dprk", "japan",
                             "south china sea", "pacific", "beijing", "seoul")):
        if 0 <= hour_utc <= 8:
            timing_mult = 1.20   # Asia active hours — US retail asleep, lag window open
        elif 13 <= hour_utc <= 22:
            timing_mult = 0.95   # US prime time — reprices quickly, edge gone
        else:
            timing_mult = 1.05   # Transition period

    # Europe / Middle East — local business hours roughly 06:00-16:00 UTC
    elif any(w in q for w in ("ukraine", "russia", "iran", "israel", "gaza",
                               "nato", "europe", "middle east", "syria", "turkey",
                               "moscow", "kyiv", "brussels")):
        if 6 <= hour_utc <= 14:
            timing_mult = 1.15   # Europe/ME active hours — US just waking, partial lag
        elif 18 <= hour_utc <= 4:
            timing_mult = 0.95   # Off-hours — less news flow
        else:
            timing_mult = 1.0

    else:
        timing_mult = 1.0  # General/Americas — no systematic timezone edge

    return min(1.35, event_mult * timing_mult)


def compute_signal(market) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    Conviction-based sizing with fear-premium correction and timezone adjustment:
    - Base conviction scales linearly with distance from threshold
    - geopolitics_bias() discounts fear-driven overpricing (nuclear, invasion)
      and boosts underpriced diplomatic/procedural markets
    - Regional timing layer adds boost when trading in the news lag window
      before US retail has repriced non-US breaking events
    - Result capped at 1.0 so size never exceeds MAX_POSITION
    - MIN_TRADE floor prevents trivially small orders near the boundary

    Remix: feed GDELT event velocity or ACLED conflict intensity scores
    into p to trade divergence between conflict data and market pricing.
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

    bias = geopolitics_bias(q)

    if p <= YES_THRESHOLD:
        # conviction=0 at threshold boundary, conviction=1 at p=0 — scaled by geopolitics bias
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
    print(f"[polymarket-geopolitics-trader] mode={mode} max_pos=${MAX_POSITION} min_vol=${MIN_VOLUME} max_spread={MAX_SPREAD:.0%} min_days={MIN_DAYS}")

    client  = get_client(live=live)
    markets = find_markets(client)
    print(f"[polymarket-geopolitics-trader] {len(markets)} candidate markets")

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

    print(f"[polymarket-geopolitics-trader] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Trades geopolitical prediction markets: wars, ceasefires, sanctions, UN votes, and diplomatic events.")
    ap.add_argument("--live", action="store_true",
                    help="Real trades on Polymarket. Default is paper (sim) mode.")
    run(live=ap.parse_args().live)
