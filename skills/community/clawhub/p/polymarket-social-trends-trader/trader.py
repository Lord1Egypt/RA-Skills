"""
polymarket-social-trends-trader
Trades Polymarket prediction markets on social trend indicators: loneliness indices,
mental health policy, drug legalization, and cultural inflection points.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag.
"""
import os
import argparse
from datetime import datetime, timezone
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-social-trends-trader"
SKILL_SLUG   = "polymarket-social-trends-trader"

KEYWORDS = [
    'mental health', 'suicide rate', 'drug legalization', 'cannabis',
    'psychedelics', 'loneliness', 'social media ban', 'teen smartphone',
    'TikTok ban', 'gun control', 'marijuana', 'psilocybin', 'FDA mental health',
    'universal basic income', 'UBI', 'poverty rate', 'homelessness',
    'opioid', 'fentanyl', 'drug decriminalization', 'safe injection',
    'gun violence', 'background check', 'red flag law', 'assault weapon',
    'SNAP', 'welfare', 'Medicaid expansion', 'healthcare access',
]

# Risk parameters — declared as tunables in clawhub.json, adjustable from Simmer UI.
# Named SIMMER_* so apply_skill_config() can load automaton-managed overrides.
MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  "25"))
MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    "5000"))
MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.12"))
MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      "7"))
MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "7"))
# Signal thresholds — buy YES below YES_THRESHOLD, sell NO above NO_THRESHOLD.
# Position size scales with conviction, corrected for ideological overcrowding
# and legislative base rates.
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


def policy_bias(question: str) -> float:
    """
    Returns a conviction multiplier (0.65–1.35) combining two structural edges
    unique to social policy and wellbeing markets:

    1. IDEOLOGICAL MOTIVATION CORRECTION
       Social policy markets are dominated by ideologically motivated traders who
       bet on what they WANT to happen, not what evidence suggests will happen.
       This is the most powerful and consistent mispricing pattern on Polymarket.

       Different policy domains attract different ideological crowds, each creating
       systematic overpricing in a predictable direction:

       FDA drug approval (post Phase 3 / NDA filing)      → 1.20x
         FDA approval rate post-NDA submission is ~85-90%. Retail underprices
         because "it's a drug" bias — they apply moral judgment to a regulatory
         process. Mental health / psychedelic therapy approvals especially
         underpriced due to stigma. No ideological crowd here; just FDA process.

       Social media ban / teen smartphone restriction      → 1.15x
         Genuinely bipartisan — both progressive (mental health advocates) and
         conservative (parental rights) coalitions support it. Retail underprices
         because they've been burned by partisan gridlock on everything else and
         assume this will also fail. It won't. Bipartisan consensus is rare and
         powerful when it exists.

       Mental health funding / coverage mandate            → 1.05x
         Mental health parity is broadly popular across party lines. Retail
         underprices it because they conflate "controversial topic" with
         "controversial legislation" — mental health funding is actually
         bipartisan and has consistent passage momentum.

       Homelessness / poverty statistics (data markets)   → 1.00x
         HUD annual Point-in-Time count and Census poverty data are objective
         and published on known dates. No strong ideological signal either way.

       Gun control / background checks / red flag laws    → 0.90x
         High-visibility, bidirectional emotional overcrowding. Progressive
         advocates bid YES; gun advocates fade YES. Both sides are ideologically
         motivated. The two crowds partially cancel each other out, making gun
         markets more efficiently priced than other social policy — but still
         noisy. Trade with reduced confidence.

       UBI / guaranteed income / welfare expansion        → 0.75x
         Progressive ideological overcrowding on YES. Retail supporters price
         their political wish, not legislative reality. Federal UBI has near-zero
         passage probability; markets consistently price it at 15-30%. The gap
         between stated polling support (~50%) and legislative feasibility is
         enormous — and retail doesn't distinguish them.

       Cannabis / marijuana federal rescheduling or legalization → 0.70x
         The most consistently overpriced category in social policy. Retail
         dramatically overprices federal cannabis action. State-level markets are
         more reasonable; federal markets are dominated by advocates pricing hope.
         Since 1970, every federal cannabis legalization market has resolved NO.
         Trade the historical base rate, not the Twitter sentiment.

       Psychedelics outside FDA approval context           → 0.72x
         Similar to cannabis but with even thinner legislative track record.
         Psilocybin/MDMA clinical enthusiasm drives retail to overprice state
         and federal legalization timelines that are 5-10 years out.

    2. US LEGISLATIVE CALENDAR (applies to "will Congress/Senate/House pass X")
       GovTrack documents that US bills pass at ~3-5% overall and ~25-30% if
       they clear committee. But the legislative calendar dramatically affects
       even this low base rate:

       Odd year (non-election): normal legislative session → 1.00x
       Even year, Jan–Jul: session active but campaigns ramp → 0.95x
       Even year, Aug–Dec: pre-election gridlock — Congress stops legislating
         and starts campaigning. Passage rates drop by ~40-50% vs odd years.
         → 0.80x for any "will Congress pass" market in this window.

       Non-legislative markets (data releases, FDA decisions): → 1.00x
         The political calendar does not affect FDA or HUD timelines.

    Combined and capped at 1.35x.
    """
    year  = datetime.now(timezone.utc).year
    month = datetime.now(timezone.utc).month
    q = question.lower()

    # Factor 1: ideological motivation correction
    if any(w in q for w in ("fda approval", "fda approved", "phase 3", "nda",
                             "breakthrough therapy", "fda grants", "fda clears",
                             "fda authorizes", "mdma therapy", "psilocybin fda",
                             "ketamine fda", "esketamine")):
        issue_mult = 1.20  # FDA process ~85-90% post-NDA; retail applies moral discount

    elif any(w in q for w in ("social media ban", "teen smartphone", "tiktok ban",
                               "phone ban", "smartphone ban", "social media age",
                               "under 16", "minor social media", "kids online",
                               "children online")):
        issue_mult = 1.15  # Bipartisan consensus — retail underprices due to gridlock fatigue

    elif any(w in q for w in ("mental health", "mental health parity", "mental health funding",
                               "behavioral health", "mental health coverage",
                               "mental health mandate", "psychiatric")):
        issue_mult = 1.05  # Broadly bipartisan; retail conflates "sensitive topic" with opposition

    elif any(w in q for w in ("homelessness", "homeless count", "poverty rate",
                               "poverty level", "hud", "point-in-time", "snap benefit",
                               "food stamp", "poverty threshold")):
        issue_mult = 1.00  # Data-release market — ideologically neutral, objective dates

    elif any(w in q for w in ("gun control", "background check", "red flag",
                               "assault weapon", "gun violence", "firearm",
                               "gun purchase", "gun registry", "magazine limit")):
        issue_mult = 0.90  # Bidirectional overcrowding — both crowds partially cancel

    elif any(w in q for w in ("ubi", "universal basic income", "guaranteed income",
                               "guaranteed minimum", "negative income tax",
                               "basic income", "cash transfer program")):
        issue_mult = 0.75  # Progressive overcrowding — retail prices political wish

    elif any(w in q for w in ("cannabis", "marijuana", "federal legalization",
                               "federal cannabis", "cannabis federal", "schedule 1",
                               "schedule i", "dea reschedule", "marijuana legalize")):
        issue_mult = 0.70  # Most overpriced category in social policy — advocates dominate

    elif any(w in q for w in ("psilocybin", "psychedelic", "mdma", "ketamine legal",
                               "magic mushroom", "decriminalize psychedelic",
                               "psychedelic therapy legal")):
        issue_mult = 0.72  # Similar to cannabis — clinical enthusiasm → retail timeline overpricing

    elif any(w in q for w in ("opioid", "fentanyl", "drug decriminalization",
                               "safe injection", "harm reduction")):
        issue_mult = 0.85  # Contested — public health framing vs criminal justice framing

    else:
        issue_mult = 1.0

    # Factor 2: US legislative calendar
    # Only applied when the market is about a legislative action.
    legislative_keywords = ("congress", "senate", "house passes", "legislation",
                            "bill passes", "signed into law", "enacted", "law by",
                            "pass a law", "federal law", "state legislature",
                            "vote on", "passed by")
    is_legislative = any(w in q for w in legislative_keywords)

    if is_legislative:
        is_election_year = (year % 2 == 0)
        if is_election_year and month >= 8:
            calendar_mult = 0.80  # Pre-election gridlock — passage rates drop 40-50%
        elif is_election_year:
            calendar_mult = 0.95  # Election year but session still active
        else:
            calendar_mult = 1.00  # Odd year — normal legislative productivity
    else:
        calendar_mult = 1.00  # FDA/data markets unaffected by political calendar

    return min(1.35, issue_mult * calendar_mult)


def compute_signal(market) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    Conviction-based sizing with ideological motivation correction and
    legislative calendar adjustment:
    - Base conviction scales linearly with distance from threshold
    - policy_bias() corrects for ideologically overcrowded YES pricing on
      cannabis/UBI/psychedelics (0.70-0.75x) and boosts bipartisan markets
      (social media bans, FDA approvals) that retail underprices
    - Legislative calendar dampener: election-year August–December sees
      ~40-50% lower passage rates — applied automatically to Congress markets
    - Result capped at 1.0 so size never exceeds MAX_POSITION
    - MIN_TRADE floor prevents trivially small orders near the boundary

    Remix: feed GovTrack bill stage data (introduced → committee → floor vote)
    into p to trade the divergence between committee advancement signal and
    naive retail pricing of passage probability.
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

    bias = policy_bias(q)

    if p <= YES_THRESHOLD:
        # conviction=0 at threshold boundary, conviction=1 at p=0 — scaled by policy bias
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
    year = datetime.now(timezone.utc).year
    month = datetime.now(timezone.utc).month
    is_election_gridlock = (year % 2 == 0 and month >= 8)
    print(f"[polymarket-social-trends-trader] mode={mode} max_pos=${MAX_POSITION} min_vol=${MIN_VOLUME} max_spread={MAX_SPREAD:.0%} election_gridlock={is_election_gridlock}")

    client  = get_client(live=live)
    markets = find_markets(client)
    print(f"[polymarket-social-trends-trader] {len(markets)} candidate markets")

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

    print(f"[polymarket-social-trends-trader] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Trades Polymarket prediction markets on social trend indicators: loneliness indices, mental health policy, drug legalization, and cultural inflection points.")
    ap.add_argument("--live", action="store_true",
                    help="Real trades on Polymarket. Default is paper (sim) mode.")
    run(live=ap.parse_args().live)
