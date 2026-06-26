"""
polymarket-resolution-lattice-trader
Trades cross-market inconsistencies on Polymarket by enforcing logical
relations between related markets rather than relying on a single-market bias.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag.
"""
import os
import re
import math
import argparse
from datetime import datetime, timezone
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-resolution-lattice-trader"
SKILL_SLUG   = "polymarket-resolution-lattice-trader"

KEYWORDS = [
    "before", "by ", "deadline", "nominee", "nomination",
    "president", "elected", "win the election", "will win",
    "ceasefire", "agreement", "deal", "approval", "launch",
    "ETF", "rate cut", "IPO", "release", "pass by", "before end of",
]

# Risk parameters — declared as tunables in clawhub.json, adjustable from Simmer UI.
# Named SIMMER_* so apply_skill_config() can load automaton-managed overrides.
MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  "35"))
MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    "10000"))
MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.07"))
MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      "3"))
MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "6"))
# Signal thresholds — buy YES below YES_THRESHOLD, sell NO above NO_THRESHOLD.
# Position size scales with conviction from graph inconsistency magnitude.
YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.38"))
NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",  "0.62"))
MIN_TRADE      = float(os.environ.get("SIMMER_MIN_TRADE",     "5"))

_client: SimmerClient | None = None


def get_client(live: bool = False) -> SimmerClient:
    """
    live=False -> venue="sim"  (paper trades — safe default).
    live=True  -> venue="polymarket" (real trades, only with --live flag).
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


def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def canonical_subject(question: str) -> str:
    q = normalize_text(question)
    q = re.sub(r"^will\s+", "", q)
    q = re.sub(r"\b(before|by|on or before|not later than)\b.*$", "", q).strip()
    q = re.sub(
        r"\b(win|be|become|get|receive|approve|approved|launch|release|cut|sign|pass)\b.*$",
        "",
        q,
    ).strip()
    return q[:120]


def parse_time_bucket(question: str) -> tuple[str, int] | None:
    q = normalize_text(question)

    m = re.search(r"\b(before|by|on or before|not later than)\s+([a-z]+\s+\d{1,2}\s+\d{4})\b", q)
    if m:
        raw = m.group(2)
        try:
            dt = datetime.strptime(raw, "%B %d %Y")
            return raw, int(dt.timestamp())
        except ValueError:
            pass

    m = re.search(r"\b(before|by|on or before|not later than)\s+([a-z]+\s+\d{4})\b", q)
    if m:
        raw = m.group(2)
        try:
            dt = datetime.strptime("1 " + raw, "%d %B %Y")
            return raw, int(dt.timestamp())
        except ValueError:
            pass

    m = re.search(r"\b(before|by|on or before|not later than)\s+(end of\s+\d{4})\b", q)
    if m:
        raw = m.group(2)
        year = int(re.search(r"\d{4}", raw).group(0))
        dt = datetime(year, 12, 31)
        return raw, int(dt.timestamp())

    m = re.search(r"\b(before|by|on or before|not later than)\s+(\d{4})\b", q)
    if m:
        raw = m.group(2)
        dt = datetime(int(raw), 12, 31)
        return raw, int(dt.timestamp())

    return None


def parse_nomination_chain(question: str) -> tuple[str, int] | None:
    q = normalize_text(question)
    subject = canonical_subject(question)
    if not subject:
        return None

    if any(w in q for w in ("democratic nominee", "republican nominee", "party nominee", "nomination")):
        return subject, 1

    if any(w in q for w in ("president", "win the election", "elected", "win presidency", "be president")):
        return subject, 2

    return None


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


def find_markets(client: SimmerClient) -> list:
    """Find active markets matching structural relation keywords, deduplicated."""
    seen, unique = set(), []
    for kw in KEYWORDS:
        try:
            for m in client.find_markets(query=kw):
                market_id = getattr(m, "id", None)
                if market_id and market_id not in seen:
                    seen.add(market_id)
                    unique.append(m)
        except Exception as e:
            print(f"[search] {kw!r}: {e}")
    return unique


def score_time_lattice(markets: list) -> list[tuple]:
    opportunities = []
    groups: dict[str, list[tuple]] = {}

    for m in markets:
        ok, _ = valid_market(m)
        if not ok:
            continue
        parsed = parse_time_bucket(getattr(m, "question", ""))
        subject = canonical_subject(getattr(m, "question", ""))
        if not parsed or not subject:
            continue
        _, ts = parsed
        groups.setdefault(subject, []).append((ts, m))

    for subject, items in groups.items():
        if len(items) < 2:
            continue
        items.sort(key=lambda x: x[0])
        for i in range(len(items) - 1):
            ts_early, early = items[i]
            for ts_late, late in items[i + 1:]:
                if ts_early >= ts_late:
                    continue
                p_early = float(getattr(early, "current_probability", 0))
                p_late = float(getattr(late, "current_probability", 0))
                violation = p_early - p_late
                if violation <= 0.03:
                    continue

                opportunities.append((
                    early,
                    "no",
                    violation,
                    f"Temporal lattice break: earlier deadline {p_early:.0%} > later deadline {p_late:.0%} for {subject[:55]}",
                ))
                opportunities.append((
                    late,
                    "yes",
                    violation,
                    f"Temporal lattice break: later deadline {p_late:.0%} < earlier deadline {p_early:.0%} for {subject[:55]}",
                ))
    return opportunities


def score_chain_lattice(markets: list) -> list[tuple]:
    opportunities = []
    groups: dict[str, dict[int, list]] = {}

    for m in markets:
        ok, _ = valid_market(m)
        if not ok:
            continue
        parsed = parse_nomination_chain(getattr(m, "question", ""))
        if not parsed:
            continue
        subject, stage = parsed
        groups.setdefault(subject, {}).setdefault(stage, []).append(m)

    for subject, stages in groups.items():
        if 1 not in stages or 2 not in stages:
            continue
        for nomination in stages[1]:
            for presidency in stages[2]:
                p_nom = float(getattr(nomination, "current_probability", 0))
                p_pres = float(getattr(presidency, "current_probability", 0))
                violation = p_pres - p_nom
                if violation <= 0.04:
                    continue

                opportunities.append((
                    nomination,
                    "yes",
                    violation,
                    f"Chain break: presidency {p_pres:.0%} > nomination {p_nom:.0%} for {subject[:55]}",
                ))
                opportunities.append((
                    presidency,
                    "no",
                    violation,
                    f"Chain break: presidency {p_pres:.0%} > nomination {p_nom:.0%} for {subject[:55]}",
                ))
    return opportunities


def best_opportunities(markets: list) -> dict[str, tuple]:
    best: dict[str, tuple] = {}
    for market, side, mispricing, reason in score_time_lattice(markets) + score_chain_lattice(markets):
        market_id = getattr(market, "id", None)
        if not market_id:
            continue
        current = best.get(market_id)
        if current is None or mispricing > current[2]:
            best[market_id] = (market, side, mispricing, reason)
    return best


def compute_signal(market, opportunity: tuple | None) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    This strategy trades only when a market violates a logical constraint
    implied by related markets:
    - Earlier deadlines cannot be more likely than later deadlines
    - Upstream prerequisite events cannot be less likely than downstream ones

    Thresholds remain as hard gates:
    - Buy YES only if p <= YES_THRESHOLD
    - Sell NO only if p >= NO_THRESHOLD

    Size scales with inconsistency magnitude, not with single-market narrative.
    """
    ok, why = valid_market(market)
    if not ok:
        return None, 0, why

    if not opportunity:
        return None, 0, "No lattice inconsistency found"

    _, side, mispricing, reason = opportunity
    p = float(getattr(market, "current_probability", 0))

    if side == "yes":
        if p > YES_THRESHOLD:
            return None, 0, f"YES blocked at {p:.1%}; threshold is {YES_THRESHOLD:.0%}"
        conviction = min(1.0, max(0.0, (mispricing - 0.03) / max(0.01, YES_THRESHOLD)))
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        return "yes", size, f"{reason} | YES {p:.0%} mispricing={mispricing:.1%} size=${size}"

    if side == "no":
        if p < NO_THRESHOLD:
            return None, 0, f"NO blocked at {p:.1%}; threshold is {NO_THRESHOLD:.0%}"
        conviction = min(1.0, max(0.0, (mispricing - 0.03) / max(0.01, 1 - NO_THRESHOLD)))
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        return "no", size, f"{reason} | NO YES={p:.0%} mispricing={mispricing:.1%} size=${size}"

    return None, 0, "Unknown side"


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
    print(f"[polymarket-resolution-lattice-trader] mode={mode} max_pos=${MAX_POSITION} min_vol=${MIN_VOLUME} max_spread={MAX_SPREAD:.0%} min_days={MIN_DAYS}")

    client = get_client(live=live)
    markets = find_markets(client)
    print(f"[polymarket-resolution-lattice-trader] {len(markets)} candidate markets")

    opportunities = best_opportunities(markets)
    print(f"[polymarket-resolution-lattice-trader] {len(opportunities)} graph opportunities")

    placed = 0
    for market_id, opportunity in opportunities.items():
        if placed >= MAX_POSITIONS:
            break

        market = opportunity[0]
        side, size, reasoning = compute_signal(market, opportunity)
        if not side:
            print(f"  [skip] {reasoning}")
            continue

        ok, why = context_ok(client, market_id)
        if not ok:
            print(f"  [skip] {why}")
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
            print(f"  [trade] {side.upper()} ${size} {tag} {status} - {reasoning[:110]}")
            if r.success:
                placed += 1
        except Exception as e:
            print(f"  [error] {market_id}: {e}")

    print(f"[polymarket-resolution-lattice-trader] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Trades logical inconsistencies between related Polymarket markets."
    )
    ap.add_argument(
        "--live",
        action="store_true",
        help="Real trades on Polymarket. Default is paper (sim) mode.",
    )
    run(live=ap.parse_args().live)
