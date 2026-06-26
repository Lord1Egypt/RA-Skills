"""
polymarket-geopolitics-deadline-cascade-trader
Trades temporal inconsistencies across geopolitical markets with different
deadlines for the same conflict.  When P(event by later date) < P(event by
earlier date), the later-deadline market is underpriced — a mathematical
tautology violation.  Also detects diplomacy-vs-escalation inversions within
the same conflict.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- live=True -> venue="polymarket" (real trades, only with --live flag).
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag.
"""
import os
import re
import sys
import math
import argparse
from datetime import datetime, timezone
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-geopolitics-deadline-cascade-trader"
SKILL_SLUG   = "polymarket-geopolitics-deadline-cascade-trader"

KEYWORDS = [
    "Iran", "Israel", "military", "war", "ceasefire",
    "strike", "Gaza", "Lebanon", "nuclear", "sanctions",
    "tariff", "diplomacy", "meeting", "surrender", "troops",
]

# --------------- risk / signal tunables ---------------
MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  "40"))
MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    "10000"))
MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.07"))
MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      "3"))
MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "6"))
YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.38"))
NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",  "0.62"))
MIN_TRADE      = float(os.environ.get("SIMMER_MIN_TRADE",     "5"))
MIN_VIOLATION  = float(os.environ.get("SIMMER_MIN_VIOLATION",  "0.04"))

_client: SimmerClient | None = None


# --------------- helpers ---------------

def safe_print(*args, **kwargs):
    """Windows-safe print that replaces unencodable chars."""
    try:
        print(*args, **kwargs)
    except UnicodeEncodeError:
        text = " ".join(str(a) for a in args)
        print(text.encode(sys.stdout.encoding or "utf-8", errors="replace").decode(), **kwargs)


def get_client(live: bool = False) -> SimmerClient:
    global _client, MAX_POSITION, MIN_VOLUME, MAX_SPREAD, MIN_DAYS, MAX_POSITIONS
    global YES_THRESHOLD, NO_THRESHOLD, MIN_TRADE, MIN_VIOLATION
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
        MIN_VIOLATION  = float(os.environ.get("SIMMER_MIN_VIOLATION",  str(MIN_VIOLATION)))
    return _client


# --------------- date / theme parsing ---------------

MONTH_MAP = {
    "january": 1, "february": 2, "march": 3, "april": 4,
    "may": 5, "june": 6, "july": 7, "august": 8,
    "september": 9, "october": 10, "november": 11, "december": 12,
    "jan": 1, "feb": 2, "mar": 3, "apr": 4,
    "jun": 6, "jul": 7, "aug": 8, "sep": 9, "sept": 9,
    "oct": 10, "nov": 11, "dec": 12,
}

ESCALATION_WORDS = [
    "war", "strike", "attack", "invasion", "bomb", "military action",
    "troops", "offensive", "nuclear", "escalation", "retaliation",
]
DEESCALATION_WORDS = [
    "ceasefire", "peace", "truce", "withdrawal", "de-escalation",
    "surrender", "armistice", "ends",
]
DIPLOMATIC_WORDS = [
    "diplomacy", "meeting", "summit", "talks", "negotiation",
    "agreement", "deal", "sanctions", "tariff",
]

THEME_PATTERNS = [
    # "action ends" / "war ends" patterns BEFORE regular military — order matters
    (r"\b(?:military|action|war)\b.*\biran\b.*\b(?:ends|end)\b", "iran_military_timeline"),
    (r"\biran\b.*\b(?:military|action|war)\b.*\b(?:ends|end)\b", "iran_military_timeline"),
    # "declare war" against Iran — escalation with deadline
    (r"\b(?:declare\s+war|war)\b.*\biran\b.*\b(?:by|before)\b", "iran_military_timeline"),
    (r"\biran\b.*\b(?:declare\s+war|war)\b.*\b(?:by|before)\b", "iran_military_timeline"),
    # Daily military action on specific date — NOT a timeline market
    (r"\biran\b.*\b(?:military|strike|attack|bomb|action)\b.*\bon\s+\w+\s+\d", "iran_military_daily"),
    (r"\b(?:military|strike|attack|bomb|action)\b.*\biran\b.*\bon\s+\w+\s+\d", "iran_military_daily"),
    # Generic iran military (no date qualifier — catch-all)
    (r"\biran\b.*\b(?:military|strike|attack|bomb|war|action)\b", "iran_military"),
    (r"\b(?:military|strike|attack|bomb|war|action)\b.*\biran\b", "iran_military"),
    # Iran nuclear / uranium
    (r"\biran\b.*\b(?:uranium|enrichment|surrender|nuclear|stockpile)\b", "iran_nuclear"),
    (r"\b(?:uranium|enrichment|surrender|nuclear|stockpile)\b.*\biran\b", "iran_nuclear"),
    # Israel strike / military action
    (r"\bisrael\b.*\b(?:strike|attack|bomb|military|action|countr)\b", "israel_military"),
    (r"\b(?:strike|attack|bomb|military|action|countr)\b.*\bisrael\b", "israel_military"),
    # Iran diplomacy
    (r"\biran\b.*\b(?:diplomacy|meeting|summit|talks|deal|sanctions)\b", "iran_diplomacy"),
    (r"\b(?:diplomacy|meeting|summit|talks|deal|sanctions)\b.*\biran\b", "iran_diplomacy"),
    # Gaza
    (r"\bgaza\b.*\b(?:ceasefire|peace|truce|war|conflict|military|action)\b", "gaza_conflict"),
    (r"\b(?:ceasefire|peace|truce|war|conflict|military|action)\b.*\bgaza\b", "gaza_conflict"),
    # Lebanon
    (r"\blebanon\b.*\b(?:ceasefire|war|conflict|strike|military|action)\b", "lebanon_conflict"),
    (r"\b(?:ceasefire|war|conflict|strike|military|action)\b.*\blebanon\b", "lebanon_conflict"),
    # General
    (r"\btariff\b", "tariff_trade"),
    (r"\bsanctions\b", "sanctions_general"),
    (r"\bwar\b", "war_general"),
    (r"\bceasefire\b", "ceasefire_general"),
    (r"\bnuclear\b", "nuclear_general"),
    (r"\btroops\b", "troops_general"),
]


def extract_deadline(question: str) -> datetime | None:
    """Extract a deadline date from a market question."""
    q = question.lower()

    # "by March 31, 2026" / "by March 31 2026" / "on March 27, 2026"
    m = re.search(
        r"\b(?:by|before|on|not later than)\s+([a-z]+)\s+(\d{1,2}),?\s+(\d{4})\b", q
    )
    if m:
        month_str, day_str, year_str = m.group(1), m.group(2), m.group(3)
        month = MONTH_MAP.get(month_str)
        if month:
            try:
                return datetime(int(year_str), month, int(day_str), tzinfo=timezone.utc)
            except ValueError:
                pass

    # "by March 31" (assume current year or next year)
    m = re.search(r"\b(?:by|before|on|not later than)\s+([a-z]+)\s+(\d{1,2})\b", q)
    if m:
        month_str, day_str = m.group(1), m.group(2)
        month = MONTH_MAP.get(month_str)
        if month:
            now = datetime.now(timezone.utc)
            try:
                candidate = datetime(now.year, month, int(day_str), tzinfo=timezone.utc)
                if candidate < now:
                    candidate = datetime(now.year + 1, month, int(day_str), tzinfo=timezone.utc)
                return candidate
            except ValueError:
                pass

    # "by May 31" style already handled above; "by May 2026"
    m = re.search(r"\b(?:by|before|on|not later than)\s+([a-z]+)\s+(\d{4})\b", q)
    if m:
        month_str, year_str = m.group(1), m.group(2)
        month = MONTH_MAP.get(month_str)
        if month:
            try:
                import calendar
                last_day = calendar.monthrange(int(year_str), month)[1]
                return datetime(int(year_str), month, last_day, tzinfo=timezone.utc)
            except ValueError:
                pass

    # "by December 31, 2026" already caught; "in 2026" / "by end of 2026"
    m = re.search(r"\b(?:in|by end of|before end of|by)\s+(\d{4})\b", q)
    if m:
        year = int(m.group(1))
        return datetime(year, 12, 31, tzinfo=timezone.utc)

    return None


def extract_conflict_theme(question: str) -> str | None:
    """Classify a market question into a conflict theme."""
    q = question.lower()
    for pattern, theme in THEME_PATTERNS:
        if re.search(pattern, q):
            return theme
    return None


def extract_event_type(question: str) -> str:
    """Classify event as escalation / de-escalation / diplomatic."""
    q = question.lower()
    if any(w in q for w in ESCALATION_WORDS):
        return "escalation"
    if any(w in q for w in DEESCALATION_WORDS):
        return "de-escalation"
    if any(w in q for w in DIPLOMATIC_WORDS):
        return "diplomatic"
    return "unknown"


def parse_market(question: str) -> tuple[str | None, datetime | None, str]:
    """Return (conflict_theme, deadline_date, event_type)."""
    theme = extract_conflict_theme(question)
    deadline = extract_deadline(question)
    event_type = extract_event_type(question)
    return theme, deadline, event_type


# --------------- market helpers ---------------

def market_volume(market) -> float:
    for attr in ("volume", "volume_usd", "liquidity", "total_volume"):
        value = getattr(market, attr, None)
        if isinstance(value, (int, float)):
            return float(value)
    return math.inf


def valid_market(market) -> tuple[bool, str]:
    p = getattr(market, "current_probability", None)
    if not isinstance(p, (int, float)):
        return False, "missing probability"

    if market_volume(market) < MIN_VOLUME:
        return False, f"Volume ${market_volume(market):.0f} < ${MIN_VOLUME:.0f}"

    spread_cents = getattr(market, "spread_cents", None)
    if isinstance(spread_cents, (int, float)) and spread_cents / 100 > MAX_SPREAD:
        return False, f"Spread {spread_cents/100:.1%} > {MAX_SPREAD:.1%}"

    resolves_at = getattr(market, "resolves_at", None)
    if resolves_at:
        try:
            resolves = datetime.fromisoformat(resolves_at.replace("Z", "+00:00"))
            days = (resolves - datetime.now(timezone.utc)).days
            if days < MIN_DAYS:
                return False, f"Only {days} days to resolve"
        except Exception:
            pass

    return True, "ok"


_GEO_FILTER = re.compile(
    r"(iran|israel|gaza|lebanon|military|ceasefire|war\b|invasion|nuclear"
    r"|strike.*countr|sanction|tariff|troops|uranium|surrender|diplomac"
    r"|nato|ukraine|russia|china|taiwan|peace\s+deal|summit)",
    re.I,
)


def find_markets(client: SimmerClient) -> list:
    """Find active geopolitical markets, deduplicated.

    Uses both keyword search AND get_markets() fallback because
    find_markets() doesn't always return all imported markets.
    Filters non-geopolitical false positives via _GEO_FILTER.
    """
    seen, unique = set(), []

    # 1. Keyword search
    for kw in KEYWORDS:
        try:
            for m in client.find_markets(query=kw):
                market_id = getattr(m, "id", None)
                q = getattr(m, "question", "")
                if market_id and market_id not in seen and _GEO_FILTER.search(q):
                    seen.add(market_id)
                    unique.append(m)
        except Exception as e:
            safe_print(f"[search] {kw!r}: {e}")

    # 2. Fallback: scan all account markets for geo matches
    try:
        for m in client.get_markets(limit=200):
            market_id = getattr(m, "id", None)
            q = getattr(m, "question", "")
            if market_id and market_id not in seen and _GEO_FILTER.search(q):
                seen.add(market_id)
                unique.append(m)
    except Exception as e:
        safe_print(f"[get_markets fallback] {e}")

    return unique


# --------------- temporal monotonicity detection ---------------

def detect_temporal_violations(markets: list) -> list[tuple]:
    """
    Group markets by conflict_theme, sort by deadline, and find pairs where
    P(event by earlier date) > P(event by later date) — a tautology violation.
    """
    groups: dict[str, list[tuple[datetime, object]]] = {}

    for m in markets:
        ok, _ = valid_market(m)
        if not ok:
            continue
        q = getattr(m, "question", "")
        theme, deadline, _ = parse_market(q)
        if not theme or not deadline:
            continue
        groups.setdefault(theme, []).append((deadline, m))

    violations = []
    for theme, items in groups.items():
        if len(items) < 2:
            continue
        items.sort(key=lambda x: x[0])

        for i in range(len(items) - 1):
            dt_early, early = items[i]
            for dt_late, late in items[i + 1:]:
                if dt_early >= dt_late:
                    continue
                p_early = float(getattr(early, "current_probability", 0))
                p_late = float(getattr(late, "current_probability", 0))
                violation = p_early - p_late
                if violation < MIN_VIOLATION:
                    continue

                q_early = getattr(early, "question", "")[:70]
                q_late = getattr(late, "question", "")[:70]

                # Earlier deadline is overpriced -> sell NO on it
                violations.append((
                    early,
                    "no",
                    violation,
                    f"Temporal violation [{theme}]: early {p_early:.0%} > late {p_late:.0%} | {q_early}",
                ))
                # Later deadline is underpriced -> buy YES on it
                violations.append((
                    late,
                    "yes",
                    violation,
                    f"Temporal violation [{theme}]: late {p_late:.0%} < early {p_early:.0%} | {q_late}",
                ))

    return violations


# --------------- diplomacy-escalation inversion ---------------

def detect_diplomacy_escalation_inversions(markets: list) -> list[tuple]:
    """
    Within the same conflict theme, if both a diplomatic event and an
    escalation event are priced above 50%, that is logically questionable --
    diplomacy should constrain escalation and vice-versa.
    """
    groups: dict[str, dict[str, list]] = {}

    for m in markets:
        ok, _ = valid_market(m)
        if not ok:
            continue
        q = getattr(m, "question", "")
        theme, _, event_type = parse_market(q)
        if not theme or event_type == "unknown":
            continue
        groups.setdefault(theme, {}).setdefault(event_type, []).append(m)

    inversions = []
    for theme, type_map in groups.items():
        esc_markets = type_map.get("escalation", [])
        dip_markets = type_map.get("diplomatic", [])
        if not esc_markets or not dip_markets:
            continue

        for esc in esc_markets:
            for dip in dip_markets:
                p_esc = float(getattr(esc, "current_probability", 0))
                p_dip = float(getattr(dip, "current_probability", 0))
                if p_esc > 0.50 and p_dip > 0.50:
                    tension = min(p_esc, p_dip) - 0.50
                    if tension < MIN_VIOLATION:
                        continue
                    q_esc = getattr(esc, "question", "")[:70]
                    q_dip = getattr(dip, "question", "")[:70]

                    # Escalation overpriced relative to diplomacy
                    inversions.append((
                        esc,
                        "no",
                        tension,
                        f"Diplo-esc inversion [{theme}]: esc={p_esc:.0%} + diplo={p_dip:.0%} both >50% | {q_esc}",
                    ))
                    # Diplomacy overpriced relative to escalation
                    inversions.append((
                        dip,
                        "no",
                        tension,
                        f"Diplo-esc inversion [{theme}]: diplo={p_dip:.0%} + esc={p_esc:.0%} both >50% | {q_dip}",
                    ))

    return inversions


# --------------- best opportunities ---------------

def best_opportunities(markets: list) -> dict[str, tuple]:
    """Merge all violations and keep the strongest signal per market."""
    best: dict[str, tuple] = {}
    all_opps = detect_temporal_violations(markets) + detect_diplomacy_escalation_inversions(markets)
    for market, side, magnitude, reason in all_opps:
        market_id = getattr(market, "id", None)
        if not market_id:
            continue
        current = best.get(market_id)
        if current is None or magnitude > current[2]:
            best[market_id] = (market, side, magnitude, reason)
    return best


# --------------- signal & sizing ---------------

def compute_signal(market, opportunity: tuple | None) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    Conviction is derived from the violation magnitude, clamped into the
    CLAUDE.md conviction-based sizing framework.
    """
    ok, why = valid_market(market)
    if not ok:
        return None, 0, why

    if not opportunity:
        return None, 0, "No temporal or logical inconsistency found"

    _, side, magnitude, reason = opportunity
    p = float(getattr(market, "current_probability", 0))
    q = getattr(market, "question", "")

    if side == "yes":
        if p > YES_THRESHOLD:
            return None, 0, f"YES blocked at {p:.1%}; threshold is {YES_THRESHOLD:.0%}"
        conviction = (YES_THRESHOLD - p) / YES_THRESHOLD
        # Boost conviction by violation magnitude
        conviction = min(1.0, conviction + magnitude)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = YES_THRESHOLD - p
        return "yes", size, f"YES {p:.0%} edge={edge:.0%} size=${size} | {reason}"

    if side == "no":
        if p < NO_THRESHOLD:
            return None, 0, f"NO blocked at {p:.1%}; threshold is {NO_THRESHOLD:.0%}"
        conviction = (p - NO_THRESHOLD) / (1 - NO_THRESHOLD)
        conviction = min(1.0, conviction + magnitude)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = p - NO_THRESHOLD
        return "no", size, f"NO YES={p:.0%} edge={edge:.0%} size=${size} | {reason}"

    return None, 0, "Unknown side"


# --------------- context guard ---------------

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


# --------------- main loop ---------------

def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    safe_print(
        f"[geopolitics-deadline-cascade] mode={mode} max_pos=${MAX_POSITION} "
        f"min_vol=${MIN_VOLUME} max_spread={MAX_SPREAD:.0%} min_days={MIN_DAYS} "
        f"min_violation={MIN_VIOLATION:.0%}"
    )

    client = get_client(live=live)
    markets = find_markets(client)
    safe_print(f"[geopolitics-deadline-cascade] {len(markets)} candidate markets")

    opportunities = best_opportunities(markets)
    safe_print(f"[geopolitics-deadline-cascade] {len(opportunities)} inconsistency opportunities")

    placed = 0
    for market_id, opportunity in opportunities.items():
        if placed >= MAX_POSITIONS:
            break

        market = opportunity[0]
        side, size, reasoning = compute_signal(market, opportunity)
        if not side:
            safe_print(f"  [skip] {reasoning}")
            continue

        ok, why = context_ok(client, market_id)
        if not ok:
            safe_print(f"  [skip] {why}")
            continue

        try:
            r = client.trade(
                market_id=market_id,
                side=side,
                amount=size,
                source=TRADE_SOURCE,
                skill_slug=SKILL_SLUG,
                reasoning=reasoning,
            )
            tag = "(sim)" if r.simulated else "(live)"
            status = "OK" if r.success else f"FAIL:{r.error}"
            safe_print(f"  [trade] {side.upper()} ${size} {tag} {status} - {reasoning[:110]}")
            if r.success:
                placed += 1
        except Exception as e:
            safe_print(f"  [error] {market_id}: {e}")

    safe_print(f"[geopolitics-deadline-cascade] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Trades temporal inconsistencies across geopolitical deadline markets."
    )
    ap.add_argument(
        "--live",
        action="store_true",
        help="Real trades on Polymarket. Default is paper (sim) mode.",
    )
    run(live=ap.parse_args().live)
