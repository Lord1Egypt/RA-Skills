"""
polymarket-copy-size-conviction-trader
Weights copytrading by portfolio concentration. A whale committing 30%
of their capital to a single market signals far more conviction than one
spreading 2% across 50 positions. The skill scans top leaderboard wallets,
reconstructs each wallet's portfolio from on-chain activity, identifies
positions where concentration exceeds a configurable threshold, and copies
those high-conviction plays with proportionally boosted sizing.

Core edge: Portfolio concentration is a direct, observable proxy for
conviction. A whale who concentrates 30% of capital in one market is
putting their money where their mouth is. This is stronger signal than
raw position size (which scales with wallet size) or trade count
(which favours churn).

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag.
"""
import os
import sys
import json
import argparse
from datetime import datetime, timezone
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-copy-size-conviction-trader"
SKILL_SLUG   = "polymarket-copy-size-conviction-trader"

# ---------------------------------------------------------------------------
# Public APIs
# ---------------------------------------------------------------------------
LEADERBOARD_URL = "https://predicting.top/api/leaderboard"
DATA_API        = "https://data-api.polymarket.com"

# ---------------------------------------------------------------------------
# Risk parameters — declared as tunables in clawhub.json
# ---------------------------------------------------------------------------
MAX_POSITION    = float(os.environ.get("SIMMER_MAX_POSITION",    "50"))
MIN_VOLUME      = float(os.environ.get("SIMMER_MIN_VOLUME",      "3000"))
MAX_SPREAD      = float(os.environ.get("SIMMER_MAX_SPREAD",      "0.10"))
MIN_DAYS        = int(os.environ.get(  "SIMMER_MIN_DAYS",        "5"))
MAX_POSITIONS   = int(os.environ.get(  "SIMMER_MAX_POSITIONS",   "8"))
YES_THRESHOLD   = float(os.environ.get("SIMMER_YES_THRESHOLD",   "0.38"))
NO_THRESHOLD    = float(os.environ.get("SIMMER_NO_THRESHOLD",    "0.62"))
MIN_TRADE       = float(os.environ.get("SIMMER_MIN_TRADE",       "5"))

# ---------------------------------------------------------------------------
# Skill-specific parameters
# ---------------------------------------------------------------------------
MIN_CONCENTRATION    = float(os.environ.get("SIMMER_MIN_CONCENTRATION",    "0.10"))
CONCENTRATION_MULT   = float(os.environ.get("SIMMER_CONCENTRATION_MULT",   "2.0"))
LEADERBOARD_LIMIT    = int(os.environ.get(  "SIMMER_LEADERBOARD_LIMIT",    "15"))

_client: SimmerClient | None = None


def safe_print(*args, **kwargs):
    """Flush-safe print for cron/daemon environments."""
    print(*args, **kwargs, flush=True)


def get_client(live: bool = False) -> SimmerClient:
    global _client, MAX_POSITION, MIN_VOLUME, MAX_SPREAD, MIN_DAYS, MAX_POSITIONS
    global YES_THRESHOLD, NO_THRESHOLD, MIN_TRADE
    global MIN_CONCENTRATION, CONCENTRATION_MULT, LEADERBOARD_LIMIT
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
        except (AttributeError, Exception):
            pass  # apply_skill_config only available in Simmer runtime
        MAX_POSITION       = float(os.environ.get("SIMMER_MAX_POSITION",       str(MAX_POSITION)))
        MIN_VOLUME         = float(os.environ.get("SIMMER_MIN_VOLUME",         str(MIN_VOLUME)))
        MAX_SPREAD         = float(os.environ.get("SIMMER_MAX_SPREAD",         str(MAX_SPREAD)))
        MIN_DAYS           = int(os.environ.get(  "SIMMER_MIN_DAYS",           str(MIN_DAYS)))
        MAX_POSITIONS      = int(os.environ.get(  "SIMMER_MAX_POSITIONS",      str(MAX_POSITIONS)))
        YES_THRESHOLD      = float(os.environ.get("SIMMER_YES_THRESHOLD",      str(YES_THRESHOLD)))
        NO_THRESHOLD       = float(os.environ.get("SIMMER_NO_THRESHOLD",       str(NO_THRESHOLD)))
        MIN_TRADE          = float(os.environ.get("SIMMER_MIN_TRADE",          str(MIN_TRADE)))
        MIN_CONCENTRATION  = float(os.environ.get("SIMMER_MIN_CONCENTRATION",  str(MIN_CONCENTRATION)))
        CONCENTRATION_MULT = float(os.environ.get("SIMMER_CONCENTRATION_MULT", str(CONCENTRATION_MULT)))
        LEADERBOARD_LIMIT  = int(os.environ.get(  "SIMMER_LEADERBOARD_LIMIT",  str(LEADERBOARD_LIMIT)))
    return _client


# ---------------------------------------------------------------------------
# HTTP helper
# ---------------------------------------------------------------------------

def _http_get_json(url: str, timeout: int = 15) -> dict | list | None:
    """Simple stdlib JSON GET request."""
    try:
        req = Request(url, headers={"User-Agent": "simmer-copy-size-conviction/1.0"})
        with urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except (URLError, HTTPError, json.JSONDecodeError, OSError) as exc:
        safe_print(f"  [WARN] HTTP GET failed: {url} -> {exc}")
        return None


# ---------------------------------------------------------------------------
# Leaderboard fetching
# ---------------------------------------------------------------------------

def fetch_leaderboard(limit: int = 15) -> list[dict]:
    """Fetch top traders from predicting.top leaderboard API."""
    url = f"{LEADERBOARD_URL}?limit={limit}"
    data = _http_get_json(url)
    if data is None:
        safe_print("  [WARN] Leaderboard fetch returned None, using empty list")
        return []
    if isinstance(data, dict):
        traders = data.get("traders", data.get("data", data.get("results", [])))
    elif isinstance(data, list):
        traders = data
    else:
        traders = []
    safe_print(f"  Fetched {len(traders)} traders from leaderboard")
    return traders[:limit]


# ---------------------------------------------------------------------------
# Wallet activity fetching
# ---------------------------------------------------------------------------

def fetch_wallet_activity(wallet: str, limit: int = 200) -> list[dict]:
    """Fetch full trade history for a wallet from the data API."""
    url = f"{DATA_API}/activity?user={wallet}&limit={limit}"
    data = _http_get_json(url, timeout=20)
    if not data:
        return []
    if isinstance(data, list):
        return data
    return data.get("history", data.get("data", data.get("activities", [])))


# ---------------------------------------------------------------------------
# Portfolio concentration analysis
# ---------------------------------------------------------------------------

def compute_portfolio_concentration(activities: list[dict]) -> list[tuple[str, str, float, float]]:
    """Track open positions per market and compute concentration.

    Returns list of (market_title, side, position_cost, concentration_pct)
    sorted by concentration descending.
    """
    if not activities:
        return []

    # Aggregate net position per market
    positions: dict[str, dict] = {}
    for act in activities:
        market_id = act.get("market", act.get("conditionId", act.get("id", "")))
        title = act.get("title", act.get("question", act.get("market_title", market_id[:20])))
        if not market_id:
            continue

        side_raw = act.get("side", act.get("type", "")).lower()
        price = float(act.get("price", 0))
        size = float(act.get("size", act.get("amount", 0)))
        cost = price * size

        if market_id not in positions:
            positions[market_id] = {
                "title": title,
                "buy_cost": 0.0,
                "sell_cost": 0.0,
                "buy_size": 0.0,
                "sell_size": 0.0,
                "side": "yes",
            }

        entry = positions[market_id]
        if title and len(title) > len(entry["title"]):
            entry["title"] = title

        if side_raw in ("buy", "long"):
            entry["buy_cost"] += cost
            entry["buy_size"] += size
        elif side_raw in ("sell", "short"):
            entry["sell_cost"] += cost
            entry["sell_size"] += size

        # Determine predominant side from outcome token
        outcome = act.get("outcome", act.get("token", "")).lower()
        if outcome in ("yes", "no"):
            entry["side"] = outcome

    # Calculate open position cost (buys minus sells, floored at 0)
    open_positions: list[tuple[str, str, float]] = []
    total_portfolio_cost = 0.0

    for market_id, entry in positions.items():
        net_cost = max(0.0, entry["buy_cost"] - entry["sell_cost"])
        if net_cost <= 0:
            continue
        open_positions.append((entry["title"], entry["side"], net_cost))
        total_portfolio_cost += net_cost

    if total_portfolio_cost <= 0:
        return []

    # Compute concentration percentage
    result: list[tuple[str, str, float, float]] = []
    for title, side, cost in open_positions:
        concentration = cost / total_portfolio_cost
        result.append((title, side, round(cost, 2), round(concentration, 4)))

    # Sort by concentration descending
    result.sort(key=lambda x: x[3], reverse=True)
    return result


# ---------------------------------------------------------------------------
# High-conviction position discovery
# ---------------------------------------------------------------------------

def find_high_conviction_positions(
    all_wallet_portfolios: dict[str, list[tuple[str, str, float, float]]],
    min_concentration: float,
) -> list[tuple[str, list[tuple[str, str, float, float]]]]:
    """Across all wallets, find markets where at least one whale has high concentration.

    Args:
        all_wallet_portfolios: wallet_address -> concentration list
        min_concentration: minimum concentration to qualify as high-conviction

    Returns:
        List of (market_title, [(wallet, side, concentration, position_cost), ...])
        sorted by max concentration descending.
    """
    # Aggregate by market title
    market_signals: dict[str, list[tuple[str, str, float, float]]] = {}

    for wallet, portfolio in all_wallet_portfolios.items():
        for title, side, cost, concentration in portfolio:
            if concentration < min_concentration:
                continue
            market_signals.setdefault(title, []).append(
                (wallet, side, concentration, cost)
            )

    if not market_signals:
        return []

    # Sort each market's signals by concentration desc
    for title in market_signals:
        market_signals[title].sort(key=lambda x: x[2], reverse=True)

    # Sort markets by max concentration across whales
    result = sorted(
        market_signals.items(),
        key=lambda x: x[1][0][2],  # max concentration (first entry after sort)
        reverse=True,
    )
    return result


# ---------------------------------------------------------------------------
# Signal computation (per CLAUDE.md conviction-based sizing)
# ---------------------------------------------------------------------------

def compute_signal(market) -> tuple[str | None, float, str]:
    """Standard conviction-based signal per CLAUDE.md."""
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

    if p <= YES_THRESHOLD:
        conviction = (YES_THRESHOLD - p) / YES_THRESHOLD
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = YES_THRESHOLD - p
        return "yes", size, f"YES {p:.0%} edge={edge:.0%} size=${size} -- {q[:70]}"

    if p >= NO_THRESHOLD:
        conviction = (p - NO_THRESHOLD) / (1 - NO_THRESHOLD)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = p - NO_THRESHOLD
        return "no", size, f"NO YES={p:.0%} edge={edge:.0%} size=${size} -- {q[:70]}"

    return None, 0, f"Neutral at {p:.1%} (outside {YES_THRESHOLD:.0%}/{NO_THRESHOLD:.0%} bands)"


# ---------------------------------------------------------------------------
# Concentration-boosted signal
# ---------------------------------------------------------------------------

def compute_concentration_signal(
    market,
    whale_side: str,
    concentration: float,
    num_whales: int,
) -> tuple[str | None, float, str]:
    """Compute signal boosted by whale portfolio concentration.

    Only trades if whale_side aligns with compute_signal direction.
    Concentration multiplier scales the base conviction up to CONCENTRATION_MULT.
    Multiple whales agreeing adds an additional boost.

    Returns (side, size, reasoning) or (None, 0, reasoning).
    """
    base_side, base_size, base_reasoning = compute_signal(market)

    # No base signal -> no trade regardless of whale conviction
    if base_side is None:
        return None, 0, base_reasoning

    # Whale must agree with signal direction
    if whale_side.lower() != base_side.lower():
        return None, 0, (
            f"Whale side ({whale_side}) != signal side ({base_side}) -- {market.question[:60]}"
        )

    p = market.current_probability

    # Recompute base conviction
    if base_side == "yes":
        base_conviction = (YES_THRESHOLD - p) / YES_THRESHOLD
    else:
        base_conviction = (p - NO_THRESHOLD) / (1 - NO_THRESHOLD)

    # Concentration multiplier: scales from 1.0 to CONCENTRATION_MULT
    # At concentration=0.5 (50% of portfolio), we hit max multiplier
    conc_mult = 1 + min(CONCENTRATION_MULT - 1, concentration / 0.5)

    # Multi-whale boost: +0.1 per additional whale, capped at +0.3
    whale_boost = min(0.3, (num_whales - 1) * 0.1) if num_whales > 1 else 0.0

    # Final conviction: base * concentration_mult + whale_boost, capped at 1.0
    boosted_conviction = min(1.0, base_conviction * conc_mult + whale_boost)

    size = max(MIN_TRADE, round(boosted_conviction * MAX_POSITION, 2))

    q = market.question[:60]
    return (
        base_side,
        size,
        f"{base_side.upper()} p={p:.0%} conc={concentration:.0%} whales={num_whales} "
        f"conv={base_conviction:.2f}->{boosted_conviction:.2f} size=${size} -- {q}",
    )


# ---------------------------------------------------------------------------
# Context check
# ---------------------------------------------------------------------------

def context_ok(client: SimmerClient) -> bool:
    """Check portfolio context to prevent excessive positions."""
    try:
        positions = client.get_positions()
        open_count = len([p for p in positions if float(getattr(p, "size", 0)) > 0])
        if open_count >= MAX_POSITIONS:
            safe_print(f"  [GATE] Already at {open_count}/{MAX_POSITIONS} positions, skipping")
            return False
    except Exception as exc:
        safe_print(f"  [WARN] Could not check positions: {exc}")
    return True


# ---------------------------------------------------------------------------
# Market matching
# ---------------------------------------------------------------------------

def find_matching_market(client: SimmerClient, title: str):
    """Find a Simmer market matching a leaderboard position title."""
    try:
        markets = client.find_markets(title[:80])
        if not markets:
            return None
        # Return best match by title similarity
        title_lower = title.lower()
        best = None
        best_score = 0
        for m in markets:
            q = getattr(m, "question", "").lower()
            # Simple word overlap score
            title_words = set(title_lower.split())
            q_words = set(q.split())
            overlap = len(title_words & q_words)
            if overlap > best_score:
                best_score = overlap
                best = m
        # Require at least 2 words overlap
        if best_score >= 2:
            return best
    except Exception as exc:
        safe_print(f"  [WARN] Market search failed for '{title[:40]}': {exc}")
    return None


# ---------------------------------------------------------------------------
# Main run loop
# ---------------------------------------------------------------------------

def run(live: bool = False):
    mode = "LIVE" if live else "PAPER"
    safe_print(f"\n{'='*70}")
    safe_print(f"  Copy Size Conviction Trader [{mode}]")
    safe_print(f"  {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    safe_print(f"  Concentration threshold: {MIN_CONCENTRATION:.0%}  "
               f"Multiplier cap: {CONCENTRATION_MULT:.1f}x  "
               f"Wallets: {LEADERBOARD_LIMIT}")
    safe_print(f"{'='*70}")

    client = get_client(live)

    # Context check
    if not context_ok(client):
        safe_print("\nAborted: portfolio context check failed.")
        return

    # Step 1: Fetch leaderboard
    safe_print(f"\n[1/5] Fetching top {LEADERBOARD_LIMIT} wallets from leaderboard...")
    traders = fetch_leaderboard(limit=LEADERBOARD_LIMIT)
    if not traders:
        safe_print("  No traders found on leaderboard. Exiting.")
        return

    # Step 2: Fetch activity and compute concentration per wallet
    safe_print(f"\n[2/5] Analyzing portfolio concentration for {len(traders)} wallets...")
    all_wallet_portfolios: dict[str, list[tuple[str, str, float, float]]] = {}

    for i, t in enumerate(traders):
        wallet = (
            t.get("address")
            or t.get("wallet")
            or t.get("id", "unknown")
        )
        wallet = str(wallet)
        safe_print(f"  [{i+1}/{len(traders)}] {wallet[:12]}...")

        activities = fetch_wallet_activity(wallet, limit=80)
        if not activities:
            safe_print(f"    No activity found, skipping")
            continue

        portfolio = compute_portfolio_concentration(activities)
        if portfolio:
            all_wallet_portfolios[wallet] = portfolio
            top_conc = portfolio[0]
            safe_print(f"    {len(portfolio)} positions, top: {top_conc[0][:40]} "
                       f"({top_conc[3]:.0%} of portfolio)")
        else:
            safe_print(f"    No open positions detected")

    if not all_wallet_portfolios:
        safe_print("  No wallet portfolios could be reconstructed. Exiting.")
        return

    # Step 3: Find high-conviction positions
    safe_print(f"\n[3/5] Identifying high-conviction positions "
               f"(concentration >= {MIN_CONCENTRATION:.0%})...")
    high_conviction = find_high_conviction_positions(
        all_wallet_portfolios, MIN_CONCENTRATION
    )

    if not high_conviction:
        safe_print("  No positions meet concentration threshold. Exiting.")
        return

    # Print conviction dashboard
    safe_print(f"\n{'='*70}")
    safe_print(f"  HIGH-CONVICTION POSITIONS ({len(high_conviction)} markets)")
    safe_print(f"{'='*70}")
    safe_print(f"  {'Market':<35} | {'Whale':<12} | {'Conc':>5} | {'Side':<4} | {'Size':>7}")
    safe_print(f"  {'-'*35}-+-{'-'*12}-+-{'-'*5}-+-{'-'*4}-+-{'-'*7}")

    for title, whale_entries in high_conviction:
        for wallet, side, conc, cost in whale_entries:
            safe_print(
                f"  {title[:35]:<35} | {wallet[:12]:<12} | "
                f"{conc:>4.0%} | {side:<4} | ${cost:>6.0f}"
            )

    # Step 4: Match to Simmer markets, signal, trade
    safe_print(f"\n[4/5] Matching to Simmer markets and computing signals...")
    trades_executed = 0
    trades_skipped = 0
    trades_failed = 0

    for title, whale_entries in high_conviction:
        if trades_executed >= MAX_POSITIONS:
            safe_print(f"  [GATE] Reached {MAX_POSITIONS} trades, stopping")
            break

        market = find_matching_market(client, title)
        if market is None:
            safe_print(f"  [SKIP] No match: {title[:50]}")
            trades_skipped += 1
            continue

        # Check volume
        vol = getattr(market, "volume", 0) or 0
        if vol < MIN_VOLUME:
            safe_print(f"  [SKIP] Low volume ${vol:.0f} < ${MIN_VOLUME:.0f}: {title[:50]}")
            trades_skipped += 1
            continue

        # Use the highest-concentration whale's side
        top_wallet, top_side, top_conc, top_cost = whale_entries[0]
        num_whales = len(whale_entries)

        side, size, reasoning = compute_concentration_signal(
            market, top_side, top_conc, num_whales
        )

        if side is None:
            safe_print(f"  [SKIP] {reasoning}")
            trades_skipped += 1
            continue

        safe_print(f"  [SIGNAL] {reasoning}")

        sig = {
            "edge": round(top_conc, 4),
            "confidence": round(size / MAX_POSITION, 4),
            "signal_source": "copy_size_conviction",
            "num_whales": num_whales,
            "top_concentration": round(top_conc, 4),
        }

        try:
            r = client.trade(
                market_id=market.id,
                side=side,
                amount=size,
                source=TRADE_SOURCE,
                skill_slug=SKILL_SLUG,
                reasoning=reasoning,
                signal_data=sig,
            )
            tag = "(sim)" if getattr(r, "simulated", not live) else "(live)"
            status = "OK" if getattr(r, "success", True) else f"FAIL:{getattr(r, 'error', '?')}"
            safe_print(f"  [TRADE] {side.upper()} ${size:.2f} {tag} {status} on {market.question[:60]}")
            if getattr(r, "success", True):
                trades_executed += 1
            else:
                trades_failed += 1
        except Exception as exc:
            safe_print(f"  [ERROR] Trade failed: {exc}")
            trades_failed += 1

    # Step 5: Summary
    safe_print(f"\n[5/5] Summary")
    safe_print(f"{'='*70}")
    safe_print(f"  Wallets analyzed:         {len(all_wallet_portfolios)}")
    safe_print(f"  High-conviction markets:  {len(high_conviction)}")
    safe_print(f"  Trades executed:          {trades_executed}")
    safe_print(f"  Trades skipped:           {trades_skipped}")
    safe_print(f"  Trades failed:            {trades_failed}")
    safe_print(f"{'='*70}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Copy Size Conviction Trader")
    parser.add_argument("--live", action="store_true", help="Execute real trades (default: paper)")
    args = parser.parse_args()
    run(live=args.live)
