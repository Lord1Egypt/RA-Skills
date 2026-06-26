"""
polymarket-ladder-chess-tournament-trader
Trades distribution-sum violations in chess tournament winner markets.

THE EDGE:
  In a winner-takes-all tournament (e.g. FIDE Candidates), the probabilities
  of all "Will X win?" markets MUST sum to ~100%. When they don't, the field
  is mispriced:

  - Sum > 105%: players are collectively overpriced. Sell NO on the most
    overpriced (highest-probability) players to capture the reversion.
  - Sum < 95%: players are collectively underpriced. Buy YES on the most
    underpriced (lowest-probability) players to capture the reversion.

  This is a pure structural arbitrage — no opinion on who wins required.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag.
"""
import os
import re
import argparse
from collections import defaultdict
from datetime import datetime, timezone
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-ladder-chess-tournament-trader"
SKILL_SLUG   = "polymarket-ladder-chess-tournament-trader"

# Keywords for finding chess tournament winner markets
KEYWORDS = [
    "FIDE", "chess", "Candidates", "Praggnanandhaa", "Sindarov",
    "Carlsen", "Ding", "Nepomniachtchi", "Firouzja", "Gukesh",
    "Caruana", "chess championship", "chess tournament", "grandmaster",
]

# Regex to extract (player, tournament) from "Will X win the Y?"
_WIN_RE = re.compile(
    r"^Will\s+(.+?)\s+win\s+(?:the\s+)?(.+?)\??$",
    re.IGNORECASE,
)

# Chess / FIDE filter — market question must match at least one
_CHESS_RE = re.compile(
    r"(?:FIDE|chess|Candidates|grandmaster|Carlsen|Ding|Nepomniachtchi|"
    r"Firouzja|Gukesh|Caruana|Praggnanandhaa|Sindarov|championship\s+tournament)",
    re.IGNORECASE,
)

# Risk parameters
MAX_POSITION  = float(os.environ.get("SIMMER_MAX_POSITION",  "40"))
MIN_VOLUME    = float(os.environ.get("SIMMER_MIN_VOLUME",    "5000"))
MAX_SPREAD    = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.06"))
MIN_DAYS      = int(os.environ.get(  "SIMMER_MIN_DAYS",      "3"))
MAX_POSITIONS = int(os.environ.get(  "SIMMER_MAX_POSITIONS",  "10"))
YES_THRESHOLD = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.38"))
NO_THRESHOLD  = float(os.environ.get("SIMMER_NO_THRESHOLD",  "0.62"))
MIN_TRADE     = float(os.environ.get("SIMMER_MIN_TRADE",     "5"))
MIN_VIOLATION = float(os.environ.get("SIMMER_MIN_VIOLATION",  "0.05"))  # 5% sum deviation

_client: SimmerClient | None = None


def safe_print(msg: str) -> None:
    try:
        print(msg)
    except (UnicodeEncodeError, OSError):
        print(msg.encode("ascii", errors="replace").decode())


def parse_tournament_market(question: str) -> tuple[str, str] | None:
    """
    Extract (tournament_name, player_name) from questions like:
      "Will Praggnanandhaa win the 2026 FIDE Candidates Tournament?"
      "Will Carlsen win the 2026 Chess Championship?"
    Returns None if the question doesn't match the pattern or chess filter.
    """
    m = _WIN_RE.match(question.strip())
    if not m:
        return None
    player = m.group(1).strip()
    tournament = m.group(2).strip()
    # Must be chess-related
    if not _CHESS_RE.search(question):
        return None
    return (tournament, player)


def compute_signal(market, violation_pct: float, sum_total: float, direction: str) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) using conviction-based sizing.

    direction is "overpriced" (sum>105%, sell NO on highest) or
    "underpriced" (sum<95%, buy YES on lowest).

    Conviction is proportional to the magnitude of the distribution violation.
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

    if direction == "overpriced":
        # Sum > 105%: field overpriced, sell NO on highest-priced players
        # Higher p = more overpriced = more conviction
        if p >= NO_THRESHOLD:
            conviction = (p - NO_THRESHOLD) / (1 - NO_THRESHOLD)
            # Scale conviction by violation magnitude
            violation_mult = min(2.0, violation_pct / MIN_VIOLATION)
            conviction = min(1.0, conviction * violation_mult)
            size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
            edge = p - NO_THRESHOLD
            return "no", size, (
                f"NO p={p:.0%} edge={edge:.0%} sum={sum_total:.0%} "
                f"violation={violation_pct:.0%} size=${size} -- {q[:60]}"
            )
        return None, 0, f"Overpriced field but p={p:.0%} < NO_THRESHOLD={NO_THRESHOLD:.0%}"

    elif direction == "underpriced":
        # Sum < 95%: field underpriced, buy YES on lowest-priced players
        # Lower p = more underpriced = more conviction
        if p <= YES_THRESHOLD:
            conviction = (YES_THRESHOLD - p) / YES_THRESHOLD
            # Scale conviction by violation magnitude
            violation_mult = min(2.0, violation_pct / MIN_VIOLATION)
            conviction = min(1.0, conviction * violation_mult)
            size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
            edge = YES_THRESHOLD - p
            return "yes", size, (
                f"YES p={p:.0%} edge={edge:.0%} sum={sum_total:.0%} "
                f"violation={violation_pct:.0%} size=${size} -- {q[:60]}"
            )
        return None, 0, f"Underpriced field but p={p:.0%} > YES_THRESHOLD={YES_THRESHOLD:.0%}"

    return None, 0, f"Unknown direction: {direction}"


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
    """Find chess tournament winner markets via keyword sweep + fallback, deduplicated."""
    seen, unique = set(), []
    # Primary: keyword-targeted search
    for kw in KEYWORDS:
        try:
            for m in client.find_markets(query=kw):
                if m.id not in seen:
                    seen.add(m.id)
                    unique.append(m)
        except Exception as e:
            safe_print(f"[search] {kw!r}: {e}")
    # Fallback: broad market scan filtered by chess regex
    try:
        for m in client.get_markets(limit=200):
            if m.id not in seen and _CHESS_RE.search(m.question):
                seen.add(m.id)
                unique.append(m)
    except Exception as e:
        safe_print(f"[fallback] get_markets: {e}")
    return unique


def group_tournaments(markets: list) -> dict[str, list]:
    """
    Group markets by tournament name. Only includes markets whose question
    matches the "Will X win the Y?" pattern with chess keywords.
    """
    groups: dict[str, list] = defaultdict(list)
    for m in markets:
        parsed = parse_tournament_market(m.question)
        if parsed:
            tournament, _player = parsed
            groups[tournament].append(m)
    return dict(groups)


def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    safe_print(
        f"[chess-tournament-trader] mode={mode} "
        f"yes<={YES_THRESHOLD:.0%} no>={NO_THRESHOLD:.0%} "
        f"min_violation={MIN_VIOLATION:.0%} max_pos=${MAX_POSITION}"
    )

    client  = get_client(live=live)
    markets = find_markets(client)
    safe_print(f"[chess-tournament-trader] {len(markets)} candidate markets found")

    # Group by tournament and analyze distribution sums
    tournaments = group_tournaments(markets)
    safe_print(f"[chess-tournament-trader] {len(tournaments)} tournament(s) detected")

    placed = 0
    for tournament, tmkts in tournaments.items():
        if placed >= MAX_POSITIONS:
            break

        sum_total = sum(m.current_probability for m in tmkts)
        safe_print(
            f"\n[tournament] {tournament} — {len(tmkts)} players, "
            f"sum={sum_total:.1%}"
        )

        # Check for distribution violation
        if 0.95 <= sum_total <= 1.05:
            safe_print(f"  [ok] Sum {sum_total:.1%} within 95%-105% — no violation")
            continue

        violation_pct = abs(sum_total - 1.0)
        if violation_pct < MIN_VIOLATION:
            safe_print(f"  [skip] Violation {violation_pct:.1%} < MIN_VIOLATION {MIN_VIOLATION:.0%}")
            continue

        if sum_total > 1.05:
            # Overpriced: sell NO on highest-priced players
            direction = "overpriced"
            # Sort descending by probability — trade the most overpriced first
            targets = sorted(tmkts, key=lambda m: m.current_probability, reverse=True)
            safe_print(f"  [signal] OVERPRICED by {violation_pct:.1%} — selling NO on top players")
        else:
            # Underpriced: buy YES on lowest-priced players
            direction = "underpriced"
            # Sort ascending by probability — trade the most underpriced first
            targets = sorted(tmkts, key=lambda m: m.current_probability)
            safe_print(f"  [signal] UNDERPRICED by {violation_pct:.1%} — buying YES on bottom players")

        for m in targets:
            if placed >= MAX_POSITIONS:
                break

            side, size, reasoning = compute_signal(m, violation_pct, sum_total, direction)
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
                safe_print(f"  [trade] {side.upper()} ${size} {tag} {status} -- {reasoning[:75]}")
                if r.success:
                    placed += 1
            except Exception as e:
                safe_print(f"  [error] {m.id}: {e}")

    safe_print(f"\n[chess-tournament-trader] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description=(
            "Trades distribution-sum violations in chess tournament winner markets. "
            "Player probabilities must sum to ~100%. When they don't, the field is "
            "mispriced. Paper trading by default, --live for real trades."
        )
    )
    ap.add_argument("--live", action="store_true",
                    help="Real trades on Polymarket. Default is paper (sim) mode.")
    run(live=ap.parse_args().live)
