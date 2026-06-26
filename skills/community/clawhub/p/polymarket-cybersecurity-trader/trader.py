"""
polymarket-cybersecurity-trader
Trades Polymarket prediction markets on major cyberattacks, ransomware incidents, data breaches, zero-day exploits, and national cybersecurity legislation.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag.
"""
import os
import argparse
from datetime import datetime, timezone, timedelta
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-cybersecurity-trader"
SKILL_SLUG   = "polymarket-cybersecurity-trader"

KEYWORDS = [
    'cyberattack', 'ransomware', 'data breach', 'hack', 'zero-day', 'malware',
    'cyber espionage', 'infrastructure attack', 'power grid', 'CISA', 'CISA KEV',
    'cybersecurity legislation', 'data protection', 'phishing', 'DDoS',
    'supply chain hack', 'critical infrastructure', 'cyber warfare', 'CVE',
    'LockBit', 'ransomhub', 'BlackCat', 'ALPHV', 'Cl0p', 'Sandworm',
    'Volt Typhoon', 'Salt Typhoon', 'attribution', 'nation-state attack',
    'largest data breach', 'billion records', 'actively exploited',
]

# Risk parameters — declared as tunables in clawhub.json, adjustable from Simmer UI.
# Named SIMMER_* so apply_skill_config() can load automaton-managed overrides.
MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  "30"))
MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    "8000"))
MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.10"))
MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      "5"))
MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "6"))
# Signal thresholds — buy YES below YES_THRESHOLD, sell NO above NO_THRESHOLD.
# Position size scales with conviction, adjusted by question tractability,
# CISA KEV timing, and threat actor calendar signals.
YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.38"))
NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",  "0.62"))
MIN_TRADE      = float(os.environ.get("SIMMER_MIN_TRADE",     "5"))

# Q1 (Jan–Mar) and Q4 (Oct–Dec): Verizon DBIR documents peak ransomware frequency.
# End-of-year deadline pressure, budget cycles, holiday staffing gaps all spike
# ransomware activity in these months.
_RANSOMWARE_PEAK_MONTHS = {1, 2, 3, 10, 11, 12}

# Pre/post-US-election window: documented spike in state-sponsored targeting of
# government and election infrastructure (CISA, FBI annual threat reports).
_ELECTION_THREAT_MONTHS = {9, 10, 11}

_client: SimmerClient | None = None


def _is_patch_tuesday_window() -> bool:
    """
    Return True if within 72 hours after Patch Tuesday (2nd Tuesday of the month).

    Microsoft's Patch Tuesday (~17:00 UTC 2nd Tuesday of each month) is when
    CISA adds the most KEV entries — the 72-hour window immediately following
    is when CVE markets are most actionable. CISA typically adds 5–15 KEV
    entries per Patch Tuesday cycle, and Polymarket markets for 'will X
    vulnerability be exploited?' or 'will CISA issue emergency directive?'
    reprice with a 6–12h lag. This is the sharpest timing signal in the
    entire cybersecurity domain — computable from the date alone, no API.
    """
    now = datetime.now(timezone.utc)
    first_day = now.replace(day=1)
    # Tuesday = weekday 1. Find first Tuesday then add 7 days for second.
    days_to_first_tuesday = (1 - first_day.weekday()) % 7
    second_tuesday = first_day + timedelta(days=days_to_first_tuesday + 7)
    window_start = second_tuesday.replace(hour=17, minute=0, second=0, microsecond=0)
    window_end   = window_start + timedelta(hours=72)
    return window_start <= now <= window_end


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


def cyber_bias(question: str) -> float:
    """
    Returns a conviction multiplier (0.70–1.35) combining two structural edges
    unique to cybersecurity prediction markets:

    1. QUESTION TYPE TRACTABILITY
       Cybersecurity markets are the least efficiently priced category on
       Polymarket — most traders cannot read a CVE advisory, interpret a CVSS
       score, or identify which ransomware group is active in a given sector.
       The edge scales with how precisely the outcome can be assessed from
       public threat intelligence data that retail ignores:

       Ransomware attack on named group / sector milestone           → 1.25x
         Ransomware.live tracks all public ransomware victims in real time.
         Verizon DBIR documents sector-specific frequency annually.
         Healthcare is the #1 ransomware target (~35% of all incidents).
         These base rates are precise; Polymarket prices them as vibes.

       CVE / zero-day exploit in CISA KEV critical infrastructure    → 1.20x
         CISA's Known Exploited Vulnerabilities catalog is updated within
         hours of a confirmed in-the-wild exploit. The CVSS severity score
         is precise (0.0–10.0). Polymarket markets for 'will CISA issue an
         emergency directive?' or 'will X vulnerability be widely exploited?'
         reprice with a 6–12 hour lag after KEV catalog additions. Retail
         cannot read the catalog; the JSON feed is free and public.

       Annual breach volume / record breach milestone                → 1.20x
         IBM Cost of Data Breach Report and Verizon DBIR publish annual
         breach cost and count data with clear upward trend lines. Retail
         guesses based on headlines; the statistical trend is in the reports.

       DDoS record / milestone attack                                → 1.10x
         Cloudflare and Akamai publish quarterly DDoS attack size records.
         The trend is clearly upward. Retail doesn't read these reports.

       Cybersecurity legislation / regulation                        → 0.85x
         The technical signal (CISA KEV) is secondary to political and
         legislative dynamics. Cyber bills are still bills — subject to
         all the noise of the legislative process.

       Nation-state attribution                                      → 0.80x
         Cyber attribution routinely takes weeks to months; CISA/FBI
         attribution advisories are politically sensitive and often revised.
         The resolution criteria for "was this attributed to X country?"
         markets are frequently ambiguous. Technical certainty ≠ political
         attribution timing.

       Physical infrastructure damage / outage from cyberattack      → 0.70x
         The most reliably overpriced category in cybersecurity markets.
         Retail anchors to Stuxnet (2010) and the Ukraine power grid
         attacks (2015, 2016) — two of a handful of examples across 15+
         years. "Will a cyberattack cause a power outage in [country]?"
         markets consistently trade at 15–30% when the base rate for any
         specific calendar window is far lower. Dampen every physical-
         damage-from-cyber question aggressively.

    2. TIMING SIGNAL — PATCH TUESDAY WINDOW + THREAT CALENDAR
       The highest-precision timing signal in all of cybersecurity:
       Microsoft's Patch Tuesday (2nd Tuesday of each month, ~17:00 UTC)
       is when CISA adds the most KEV entries. The 72-hour window following
       is peak information density for CVE/vulnerability markets.

       CVE / KEV question + within 72h of Patch Tuesday               → 1.20x
         Peak CISA KEV addition rate; Polymarket has maximum repricing lag.
         This is computable from the date alone — no API required.

       Ransomware question + Q1 or Q4 (Jan–Mar / Oct–Dec)             → 1.15x
         Verizon DBIR consistently shows ransomware frequency peaks in Q1
         (post-holiday understaffing, January patching debt) and Q4
         (end-of-year budget pressure, holiday skeleton crews).

       State-sponsored question + pre-election window (Sep–Nov)        → 1.15x
         CISA and FBI annual threat reports document elevated state-
         sponsored targeting of government and election infrastructure in
         the months immediately before and after US federal elections.

       Any question + within 72h of Patch Tuesday                      → 1.10x
         Even non-CVE markets see elevated activity as breach disclosures
         and security advisories pile up in the Patch Tuesday window.

    Combined and capped at 1.35x.
    Ransomware question in Q1 + KEV-type: 1.25 × 1.15 = 1.35x cap.
    Physical damage question any time: 0.70x — near MIN_TRADE floor.
    Attribution question: 0.80x — political timing unpredictable.
    """
    month     = datetime.now(timezone.utc).month
    patch_win = _is_patch_tuesday_window()
    q         = question.lower()

    # Factor 1: question type tractability
    if any(w in q for w in ("ransomware attack", "ransomware hit", "ransomware incident",
                              "ransomware group", "lockbit", "cl0p", "blackcat", "alphv",
                              "ransomhub", "extortion attack", "double extortion",
                              "ransomware victim", "ransomware gang")):
        type_mult = 1.25  # Ransomware.live + Verizon DBIR: sector base rates precise and public

    elif any(w in q for w in ("cisa", "kev", "known exploited", "zero-day exploit",
                               "actively exploited", "cve-", "critical vulnerability",
                               "cvss 9", "cvss 10", "patch tuesday", "emergency directive",
                               "mandatory patch", "unpatched vulnerability")):
        type_mult = 1.20  # CISA KEV catalog precise + public; 6-12h Polymarket repricing lag

    elif any(w in q for w in ("data breach record", "billion records", "largest breach",
                               "most expensive breach", "breach cost", "annual breach",
                               "breach report", "records exposed", "records leaked")):
        type_mult = 1.20  # IBM DBIR + Verizon DBIR trend lines; retail prices on headlines

    elif any(w in q for w in ("ddos", "distributed denial", "largest ddos", "ddos record",
                               "ddos attack", "terabit", "tbps attack", "gbps record")):
        type_mult = 1.10  # Cloudflare/Akamai quarterly reports; clear upward trend retail ignores

    elif any(w in q for w in ("cybersecurity law", "cyber legislation", "cisa authority",
                               "data protection law", "privacy law", "cyber bill",
                               "cybersecurity act", "cyber regulation", "shield act")):
        type_mult = 0.85  # Technical signal secondary to legislative dynamics

    elif any(w in q for w in ("attributed to", "attribution", "responsible for the attack",
                               "state-sponsored", "gru ", "fsb ", "mss ", "lazarus group",
                               "apt28", "apt29", "apt41", "volt typhoon", "salt typhoon",
                               "sandworm", "fancy bear", "cozy bear")):
        type_mult = 0.80  # Attribution takes months; politically sensitive; often revised

    elif any(w in q for w in ("power grid attack", "grid blackout", "blackout caused by",
                               "infrastructure failure from cyber", "pipeline hack",
                               "physical damage", "physical outage", "stuxnet",
                               "ukraine power", "cyber-physical")):
        type_mult = 0.70  # Stuxnet anchoring; retail overprices; physically damaging cyber ops are once-per-decade

    else:
        type_mult = 1.0

    # Factor 2: timing signal — Patch Tuesday window + threat calendar
    is_cve       = any(w in q for w in ("cve", "cisa", "kev", "zero-day", "vulnerability",
                                          "patch", "exploit", "unpatched", "critical flaw"))
    is_ransomware= any(w in q for w in ("ransomware", "extortion", "lockbit", "cl0p",
                                          "blackcat", "alphv", "ransomhub"))
    is_state     = any(w in q for w in ("russia", "china", "iran", "north korea", "dprk",
                                          "apt", "state-sponsored", "election interference",
                                          "government hack", "espionage"))

    if is_cve and patch_win:
        timing_mult = 1.20  # 72h post-Patch-Tuesday: CISA KEV additions peak; max Polymarket lag
    elif is_ransomware and month in _RANSOMWARE_PEAK_MONTHS:
        timing_mult = 1.15  # Q1/Q4: Verizon DBIR peak ransomware frequency quarters
    elif is_state and month in _ELECTION_THREAT_MONTHS:
        timing_mult = 1.15  # Pre/post-election: CISA/FBI document elevated state-sponsored activity
    elif patch_win:
        timing_mult = 1.10  # Patch Tuesday window: high advisory density even for non-CVE markets
    else:
        timing_mult = 1.0

    return min(1.35, type_mult * timing_mult)


def compute_signal(market) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    Conviction-based sizing with threat intelligence tractability correction
    and Patch Tuesday timing:
    - Base conviction scales linearly with distance from threshold
    - cyber_bias() corrects for the core information asymmetry in this domain:
      retail cannot read CVE advisories or CISA KEV entries; the edge is in
      knowing the base rates (73-75% S&P beat rate equivalent = Verizon DBIR
      sector ransomware frequencies) when retail is trading on headlines
    - Patch Tuesday window boosts CVE market edge (unique to this trader)
    - Physical damage / attribution markets dampened — resolution uncertainty
    - Result capped at 1.0 so size never exceeds MAX_POSITION
    - MIN_TRADE floor prevents trivially small orders near the boundary

    Remix: feed the CISA KEV JSON feed (free, public) into compute_signal —
    when a KEV entry is added for critical infrastructure, that is a direct
    signal for related Polymarket incident and legislation markets.
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

    bias = cyber_bias(q)

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


def _timing_tag() -> str:
    """Return a human-readable timing context tag for the startup log."""
    if _is_patch_tuesday_window():
        return "timing=PATCH-TUESDAY-WINDOW"
    month = datetime.now(timezone.utc).month
    if month in _RANSOMWARE_PEAK_MONTHS:
        return "timing=ransomware-peak(Q1/Q4)"
    if month in _ELECTION_THREAT_MONTHS:
        return "timing=election-threat-window"
    return "timing=normal"


def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    print(f"[polymarket-cybersecurity-trader] mode={mode} max_pos=${MAX_POSITION} min_vol=${MIN_VOLUME} max_spread={MAX_SPREAD:.0%} {_timing_tag()}")

    client  = get_client(live=live)
    markets = find_markets(client)
    print(f"[polymarket-cybersecurity-trader] {len(markets)} candidate markets")

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

    print(f"[polymarket-cybersecurity-trader] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Trades Polymarket prediction markets on major cyberattacks, ransomware incidents, data breaches, zero-day exploits, and national cybersecurity legislation.")
    ap.add_argument("--live", action="store_true",
                    help="Real trades on Polymarket. Default is paper (sim) mode.")
    run(live=ap.parse_args().live)
