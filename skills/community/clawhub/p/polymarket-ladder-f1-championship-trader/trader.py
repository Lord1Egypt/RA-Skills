"""
polymarket-ladder-f1-championship-trader
Trades distribution-sum violations in F1 championship winner markets.

THE EDGE:
  In a winner-takes-all market ("Who will be 2026 F1 Drivers' Champion?"),
  the probabilities of all contestants MUST sum to ~100%.  In practice,
  Polymarket lists each driver as a separate binary market.  Because each
  market has its own bid-ask spread, retail activity, and narrative hype,
  the implied probabilities frequently drift apart:

    sum > 105% → the field is collectively OVERPRICED
                  (each driver's YES price is too high relative to fair value)
                  → sell overpriced drivers (buy NO on the highest-priced ones)

    sum < 95%  → the field is collectively UNDERPRICED
                  (each driver's YES price is too low relative to fair value)
                  → buy underpriced drivers (buy YES on the lowest-priced ones)

  This is a structural arbitrage on probability distributions, not a
  directional bet on any single driver.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag.
"""
import os
import re
import sys
import argparse
from collections import defaultdict
from datetime import datetime, timezone
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-ladder-f1-championship-trader"
SKILL_SLUG   = "polymarket-ladder-f1-championship-trader"

KEYWORDS = [
    "F1", "Formula 1", "champion", "Drivers Champion", "Grand Prix",
    "Verstappen", "Hamilton", "Norris", "Leclerc", "Piastri",
    "Russell", "Gasly", "Albon", "Bottas",
]

# Regex to match F1 / motorsport championship markets
F1_PATTERN = re.compile(
    r"(F1|Formula\s*1|Formula\s*One|Drivers.?\s*Champion|Grand\s*Prix|"
    r"Verstappen|Hamilton|Norris|Leclerc|Piastri|Russell|Gasly|Albon|Bottas|"
    r"Sainz|Perez|Ocon|Tsunoda|Stroll|Hulkenberg|Ricciardo|Lawson|Bearman|"
    r"Colapinto|Antonelli|Doohan|Hadjar|Bortoleto)",
    re.IGNORECASE,
)

# Pattern to extract (championship, driver) from market question
CHAMP_PATTERN = re.compile(
    r"Will\s+(.+?)\s+(?:be|win)\s+(?:the\s+)?(.+?(?:champion(?:ship)?|F1.+?champion))",
    re.IGNORECASE,
)

# Fallback: "Will X be the YYYY F1 Drivers' Champion?"
CHAMP_PATTERN_ALT = re.compile(
    r"Will\s+(.+?)\s+be\s+(?:the\s+)?(\d{4})\s+F1\s+Drivers.?\s*Champion",
    re.IGNORECASE,
)

# Risk parameters
MAX_POSITION  = float(os.environ.get("SIMMER_MAX_POSITION",  "40"))
MIN_VOLUME    = float(os.environ.get("SIMMER_MIN_VOLUME",    "5000"))
MAX_SPREAD    = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.06"))
MIN_DAYS      = int(os.environ.get(  "SIMMER_MIN_DAYS",      "7"))
MAX_POSITIONS = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "8"))
YES_THRESHOLD = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.38"))
NO_THRESHOLD  = float(os.environ.get("SIMMER_NO_THRESHOLD",  "0.62"))
MIN_TRADE     = float(os.environ.get("SIMMER_MIN_TRADE",     "5"))
MIN_VIOLATION = float(os.environ.get("SIMMER_MIN_VIOLATION", "0.05"))

_client: SimmerClient | None = None


def safe_print(msg: str) -> None:
    """Print that never crashes on encoding issues."""
    try:
        print(msg)
    except (UnicodeEncodeError, OSError):
        print(msg.encode("ascii", errors="replace").decode())


def parse_championship(question: str) -> tuple[str | None, str | None]:
    """
    Extract (championship_name, driver_name) from a market question.

    Examples:
      "Will Verstappen be the 2026 F1 Drivers' Champion?" -> ("2026 F1 Drivers Champion", "Verstappen")
      "Will Gasly win the 2026 Formula 1 championship?"   -> ("2026 Formula 1 championship", "Gasly")
    """
    m = CHAMP_PATTERN_ALT.search(question)
    if m:
        driver = m.group(1).strip()
        year = m.group(2)
        return (f"{year} F1 Drivers Champion", driver)

    m = CHAMP_PATTERN.search(question)
    if m:
        driver = m.group(1).strip()
        champ = m.group(2).strip()
        return (champ, driver)

    return (None, None)


def compute_signal(market, violation: float, total_sum: float, is_overpriced: bool) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) for a single driver market within a
    championship group that has a distribution-sum violation.

    - Overpriced field (sum > 105%): sell the overpriced driver -> buy NO
      Conviction scales with how far above 100% the total sum is.
    - Underpriced field (sum < 95%): buy the underpriced driver -> buy YES
      Conviction scales with how far below 100% the total sum is.
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

    if is_overpriced:
        # Field overpriced: buy NO on highest-probability drivers (most overpriced)
        # Only trade drivers above NO_THRESHOLD — the most overpriced ones
        if p < NO_THRESHOLD:
            return None, 0, f"Driver at {p:.1%} below NO band {NO_THRESHOLD:.0%} in overpriced field"

        # Conviction: how far the sum exceeds 100%, scaled by driver's own probability
        conviction = (p - NO_THRESHOLD) / (1 - NO_THRESHOLD)
        # Boost conviction by violation magnitude (larger violation = more edge)
        violation_boost = min(1.5, 1.0 + violation)
        conviction = min(1.0, conviction * violation_boost)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = p - NO_THRESHOLD
        return (
            "no", size,
            f"OVERPRICED-FIELD NO p={p:.0%} edge={edge:.0%} sum={total_sum:.1%} "
            f"size=${size} — {q[:60]}"
        )

    else:
        # Field underpriced: buy YES on lowest-probability drivers (most underpriced)
        # Only trade drivers below YES_THRESHOLD — the most underpriced ones
        if p > YES_THRESHOLD:
            return None, 0, f"Driver at {p:.1%} above YES band {YES_THRESHOLD:.0%} in underpriced field"

        # Conviction: how far below threshold the driver is
        conviction = (YES_THRESHOLD - p) / YES_THRESHOLD
        # Boost conviction by violation magnitude
        violation_boost = min(1.5, 1.0 + violation)
        conviction = min(1.0, conviction * violation_boost)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = YES_THRESHOLD - p
        return (
            "yes", size,
            f"UNDERPRICED-FIELD YES p={p:.0%} edge={edge:.0%} sum={total_sum:.1%} "
            f"size=${size} — {q[:60]}"
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
            safe_print(f"  [warn] {w}")
    except Exception as e:
        safe_print(f"  [ctx] {market_id}: {e}")
    return True, "ok"


def get_client(live: bool = False) -> SimmerClient:
    """
    live=False -> venue="sim"  (paper trades -- safe default).
    live=True  -> venue="polymarket" (real trades, only with --live flag).
    """
    global _client
    global MAX_POSITION, MIN_VOLUME, MAX_SPREAD, MIN_DAYS, MAX_POSITIONS
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
        MAX_POSITION  = float(os.environ.get("SIMMER_MAX_POSITION",  str(MAX_POSITION)))
        MIN_VOLUME    = float(os.environ.get("SIMMER_MIN_VOLUME",    str(MIN_VOLUME)))
        MAX_SPREAD    = float(os.environ.get("SIMMER_MAX_SPREAD",    str(MAX_SPREAD)))
        MIN_DAYS      = int(os.environ.get(  "SIMMER_MIN_DAYS",      str(MIN_DAYS)))
        MAX_POSITIONS = int(os.environ.get(  "SIMMER_MAX_POSITIONS", str(MAX_POSITIONS)))
        YES_THRESHOLD = float(os.environ.get("SIMMER_YES_THRESHOLD", str(YES_THRESHOLD)))
        NO_THRESHOLD  = float(os.environ.get("SIMMER_NO_THRESHOLD",  str(NO_THRESHOLD)))
        MIN_TRADE     = float(os.environ.get("SIMMER_MIN_TRADE",     str(MIN_TRADE)))
        MIN_VIOLATION = float(os.environ.get("SIMMER_MIN_VIOLATION", str(MIN_VIOLATION)))
    return _client


def find_markets(client: SimmerClient) -> list:
    """Find active F1 championship markets via keyword search + fallback, deduplicated."""
    seen, unique = set(), []

    # Primary: keyword-based search
    for kw in KEYWORDS:
        try:
            for m in client.find_markets(query=kw):
                if m.id not in seen and F1_PATTERN.search(m.question):
                    seen.add(m.id)
                    unique.append(m)
        except Exception as e:
            safe_print(f"[search] {kw!r}: {e}")

    # Fallback: broad market fetch, filtered by regex
    try:
        for m in client.get_markets(limit=200):
            if m.id not in seen and F1_PATTERN.search(m.question):
                seen.add(m.id)
                unique.append(m)
    except Exception as e:
        safe_print(f"[fallback] get_markets: {e}")

    return unique


def group_by_championship(markets: list) -> dict[str, list]:
    """Group markets by championship name. Only include parseable F1 markets."""
    groups: dict[str, list] = defaultdict(list)
    for m in markets:
        champ, driver = parse_championship(m.question)
        if champ and driver:
            groups[champ].append(m)
    return dict(groups)


def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    safe_print(
        f"[ladder-f1-championship] mode={mode} "
        f"YES<={YES_THRESHOLD:.0%} NO>={NO_THRESHOLD:.0%} "
        f"min_violation={MIN_VIOLATION:.0%} max_pos=${MAX_POSITION}"
    )

    client  = get_client(live=live)
    markets = find_markets(client)
    safe_print(f"[ladder-f1-championship] {len(markets)} F1 markets found")

    groups = group_by_championship(markets)
    safe_print(f"[ladder-f1-championship] {len(groups)} championship groups")

    placed = 0
    for champ_name, champ_markets in groups.items():
        if placed >= MAX_POSITIONS:
            break

        if len(champ_markets) < 2:
            safe_print(f"  [skip] {champ_name}: only {len(champ_markets)} driver(s), need >= 2")
            continue

        total_sum = sum(m.current_probability for m in champ_markets)
        violation = abs(total_sum - 1.0)
        safe_print(
            f"  [group] {champ_name}: {len(champ_markets)} drivers, "
            f"sum={total_sum:.1%}, violation={violation:.1%}"
        )

        if violation < MIN_VIOLATION:
            safe_print(f"  [skip] {champ_name}: violation {violation:.1%} < {MIN_VIOLATION:.0%} threshold")
            continue

        is_overpriced = total_sum > 1.0

        # Sort: overpriced -> highest p first; underpriced -> lowest p first
        if is_overpriced:
            champ_markets.sort(key=lambda m: m.current_probability, reverse=True)
        else:
            champ_markets.sort(key=lambda m: m.current_probability)

        for m in champ_markets:
            if placed >= MAX_POSITIONS:
                break

            side, size, reasoning = compute_signal(m, violation, total_sum, is_overpriced)
            if not side:
                safe_print(f"  [skip] {reasoning}")
                continue

            ok, why = context_ok(client, m.id)
            if not ok:
                safe_print(f"  [skip] {why}")
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
                safe_print(f"  [trade] {side.upper()} ${size} {tag} {status} — {reasoning[:75]}")
                if r.success:
                    placed += 1
            except Exception as e:
                safe_print(f"  [error] {m.id}: {e}")

    safe_print(f"[ladder-f1-championship] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description=(
            "Trades distribution-sum violations in F1 championship winner markets. "
            "Driver probabilities must sum to ~100%. When they drift beyond 95-105%, "
            "the field is mispriced and we trade the correction."
        )
    )
    ap.add_argument("--live", action="store_true",
                    help="Real trades on Polymarket. Default is paper (sim) mode.")
    run(live=ap.parse_args().live)
