"""
polymarket-whale-momentum-trader
Detects when multiple top-performing whale wallets independently enter the same
Polymarket market in the same direction within a configurable time window.
When 2+ whales agree on a side, trades with conviction-boosted sizing.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag.
"""
import os
import sys
import argparse
import json
import statistics
from datetime import datetime, timezone, timedelta
from simmer_sdk import SimmerClient
from urllib.request import urlopen, Request

TRADE_SOURCE = "sdk:polymarket-whale-momentum-trader"
SKILL_SLUG   = "polymarket-whale-momentum-trader"

LEADERBOARD_URL = "https://predicting.top/api/leaderboard"
DATA_API        = "https://data-api.polymarket.com"

# Risk parameters — declared as tunables in clawhub.json, adjustable from Simmer UI.
# Named SIMMER_* so apply_skill_config() can load automaton-managed overrides.
MAX_POSITION       = float(os.environ.get("SIMMER_MAX_POSITION",      "40"))
MIN_VOLUME         = float(os.environ.get("SIMMER_MIN_VOLUME",        "3000"))
MAX_SPREAD         = float(os.environ.get("SIMMER_MAX_SPREAD",        "0.10"))
MIN_DAYS           = int(os.environ.get(  "SIMMER_MIN_DAYS",          "5"))
MAX_POSITIONS      = int(os.environ.get(  "SIMMER_MAX_POSITIONS",     "8"))
# Signal thresholds — buy YES below YES_THRESHOLD, sell NO above NO_THRESHOLD.
YES_THRESHOLD      = float(os.environ.get("SIMMER_YES_THRESHOLD",     "0.38"))
NO_THRESHOLD       = float(os.environ.get("SIMMER_NO_THRESHOLD",      "0.62"))
MIN_TRADE          = float(os.environ.get("SIMMER_MIN_TRADE",         "5"))
# Whale momentum parameters
MIN_WHALES         = int(os.environ.get(  "SIMMER_MIN_WHALES",        "2"))
LOOKBACK_HOURS     = int(os.environ.get(  "SIMMER_LOOKBACK_HOURS",    "48"))
LEADERBOARD_LIMIT  = int(os.environ.get(  "SIMMER_LEADERBOARD_LIMIT", "15"))

_client: SimmerClient | None = None


def safe_print(*args, **kwargs):
    """Print that never raises on encoding errors."""
    try:
        print(*args, **kwargs)
    except (UnicodeEncodeError, OSError):
        text = " ".join(str(a) for a in args)
        print(text.encode("ascii", "replace").decode(), **kwargs)


def get_client(live: bool = False) -> SimmerClient:
    """
    live=False -> venue="sim"  (paper trades -- safe default).
    live=True  -> venue="polymarket" (real trades, only with --live flag).
    """
    global _client, MAX_POSITION, MIN_VOLUME, MAX_SPREAD, MIN_DAYS, MAX_POSITIONS
    global YES_THRESHOLD, NO_THRESHOLD, MIN_TRADE, MIN_WHALES, LOOKBACK_HOURS, LEADERBOARD_LIMIT
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
        except (AttributeError, Exception):
            pass  # apply_skill_config only available in Simmer runtime
        # Re-read params in case apply_skill_config updated os.environ.
        MAX_POSITION       = float(os.environ.get("SIMMER_MAX_POSITION",      str(MAX_POSITION)))
        MIN_VOLUME         = float(os.environ.get("SIMMER_MIN_VOLUME",        str(MIN_VOLUME)))
        MAX_SPREAD         = float(os.environ.get("SIMMER_MAX_SPREAD",        str(MAX_SPREAD)))
        MIN_DAYS           = int(os.environ.get(  "SIMMER_MIN_DAYS",          str(MIN_DAYS)))
        MAX_POSITIONS      = int(os.environ.get(  "SIMMER_MAX_POSITIONS",     str(MAX_POSITIONS)))
        YES_THRESHOLD      = float(os.environ.get("SIMMER_YES_THRESHOLD",     str(YES_THRESHOLD)))
        NO_THRESHOLD       = float(os.environ.get("SIMMER_NO_THRESHOLD",      str(NO_THRESHOLD)))
        MIN_TRADE          = float(os.environ.get("SIMMER_MIN_TRADE",         str(MIN_TRADE)))
        MIN_WHALES         = int(os.environ.get(  "SIMMER_MIN_WHALES",        str(MIN_WHALES)))
        LOOKBACK_HOURS     = int(os.environ.get(  "SIMMER_LOOKBACK_HOURS",    str(LOOKBACK_HOURS)))
        LEADERBOARD_LIMIT  = int(os.environ.get(  "SIMMER_LEADERBOARD_LIMIT", str(LEADERBOARD_LIMIT)))
    return _client


def fetch_leaderboard() -> list[dict]:
    """
    Fetch top wallets from predicting.top leaderboard API.
    Returns list of dicts with at least 'address' key.
    """
    try:
        req = Request(
            f"{LEADERBOARD_URL}?limit={LEADERBOARD_LIMIT}",
            headers={"User-Agent": "polymarket-whale-momentum-trader/1.0"},
        )
        with urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
        # API may return list directly or nested under a key
        if isinstance(data, list):
            wallets = data[:LEADERBOARD_LIMIT]
        elif isinstance(data, dict):
            # Try common keys
            for key in ("traders", "data", "leaderboard", "results", "users"):
                if key in data and isinstance(data[key], list):
                    wallets = data[key][:LEADERBOARD_LIMIT]
                    break
            else:
                safe_print(f"[leaderboard] Unexpected response shape: {list(data.keys())}")
                return []
        else:
            return []
        safe_print(f"[leaderboard] Fetched {len(wallets)} top wallets")
        return wallets
    except Exception as e:
        safe_print(f"[leaderboard] Error fetching: {e}")
        return []


def _extract_wallet_address(wallet: dict) -> str | None:
    """Extract address from a leaderboard wallet entry."""
    for key in ("address", "wallet", "wallet_address", "user", "id"):
        if key in wallet and isinstance(wallet[key], str) and len(wallet[key]) >= 10:
            return wallet[key]
    return None


def fetch_recent_activity(wallet_address: str, hours: int = 48) -> list[dict]:
    """
    Fetch recent trading activity for a wallet from the Polymarket data API.
    Filters to trades within the last `hours` hours.
    Returns list of activity dicts with market info, side, and amount.
    """
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    activities = []
    try:
        url = f"{DATA_API}/activity?user={wallet_address}&limit=100"
        req = Request(url, headers={"User-Agent": "polymarket-whale-momentum-trader/1.0"})
        with urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())

        items = data if isinstance(data, list) else data.get("data", data.get("history", []))
        if not isinstance(items, list):
            return []

        for item in items:
            # Parse timestamp
            ts_raw = item.get("timestamp") or item.get("created_at") or item.get("time")
            if not ts_raw:
                continue
            try:
                if isinstance(ts_raw, (int, float)):
                    ts = datetime.fromtimestamp(ts_raw if ts_raw < 1e12 else ts_raw / 1000, tz=timezone.utc)
                else:
                    ts = datetime.fromisoformat(str(ts_raw).replace("Z", "+00:00"))
            except Exception:
                continue

            if ts < cutoff:
                continue

            # Extract market title and side
            title = (item.get("title") or item.get("market_title") or
                     item.get("question") or item.get("market", {}).get("question", ""))
            side = (item.get("side") or item.get("outcome") or "").lower()
            amount = float(item.get("amount") or item.get("size") or item.get("usd_amount") or 0)

            if title and side in ("yes", "no"):
                activities.append({
                    "title": title,
                    "side": side,
                    "amount": amount,
                    "timestamp": ts.isoformat(),
                    "wallet": wallet_address,
                })
    except Exception as e:
        safe_print(f"[activity] {wallet_address[:10]}...: {e}")

    return activities


def build_momentum_map(activities_per_wallet: dict[str, list[dict]]) -> dict:
    """
    Build a momentum map across all wallets.
    For each market title, count how many distinct wallets bought YES vs NO.

    Returns dict: market_title -> {
        yes_wallets: set, no_wallets: set,
        yes_volume: float, no_volume: float
    }
    """
    momentum: dict[str, dict] = {}

    for wallet, activities in activities_per_wallet.items():
        for act in activities:
            title = act["title"]
            side = act["side"]
            amount = act.get("amount", 0)

            if title not in momentum:
                momentum[title] = {
                    "yes_wallets": set(),
                    "no_wallets": set(),
                    "yes_volume": 0.0,
                    "no_volume": 0.0,
                }

            entry = momentum[title]
            if side == "yes":
                entry["yes_wallets"].add(wallet)
                entry["yes_volume"] += amount
            elif side == "no":
                entry["no_wallets"].add(wallet)
                entry["no_volume"] += amount

    return momentum


def find_momentum_signals(momentum_map: dict, min_whales: int) -> list[tuple[str, str, int, float]]:
    """
    Filter momentum map to markets where min_whales+ distinct wallets agree on a direction.

    Returns list of (market_title, direction, whale_count, total_volume)
    sorted by whale_count descending.
    """
    signals = []

    for title, data in momentum_map.items():
        yes_count = len(data["yes_wallets"])
        no_count = len(data["no_wallets"])

        if yes_count >= min_whales:
            signals.append((title, "yes", yes_count, data["yes_volume"]))
        if no_count >= min_whales:
            signals.append((title, "no", no_count, data["no_volume"]))

    # Sort by whale count descending, then volume descending
    signals.sort(key=lambda x: (x[2], x[3]), reverse=True)
    return signals


def find_matching_market(client: SimmerClient, keyword: str):
    """
    Search Simmer markets for a keyword match.
    Returns the first matching market or None.
    """
    # Use first few significant words as search query
    words = keyword.split()
    # Try progressively shorter queries to find a match
    for length in (min(6, len(words)), min(4, len(words)), min(2, len(words))):
        query = " ".join(words[:length])
        try:
            results = client.find_markets(query)
            if results:
                # Return best match — first result from the SDK
                return results[0]
        except Exception:
            continue
    return None


def compute_signal(market) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).
    Standard conviction-based sizing per CLAUDE.md.
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

    if p <= YES_THRESHOLD:
        conviction = (YES_THRESHOLD - p) / YES_THRESHOLD
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = YES_THRESHOLD - p
        return "yes", size, f"YES {p:.0%} edge={edge:.0%} size=${size} — {q[:70]}"

    if p >= NO_THRESHOLD:
        conviction = (p - NO_THRESHOLD) / (1 - NO_THRESHOLD)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = p - NO_THRESHOLD
        return "no", size, f"NO YES={p:.0%} edge={edge:.0%} size=${size} — {q[:70]}"

    return None, 0, f"Neutral at {p:.1%} (outside {YES_THRESHOLD:.0%}/{NO_THRESHOLD:.0%} bands)"


def compute_whale_boosted_signal(
    market, whale_direction: str, whale_count: int
) -> tuple[str | None, float, str]:
    """
    Like compute_signal but boosts conviction based on whale consensus.

    conviction_boost = min(0.5, (whale_count - 1) * 0.15)

    Only trades if whale direction matches the signal direction from thresholds.
    This prevents fighting whale momentum — if whales buy YES but price is in
    NO territory, we skip (conflicting signals).
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

    conviction_boost = min(0.5, (whale_count - 1) * 0.15)

    if p <= YES_THRESHOLD and whale_direction == "yes":
        base_conviction = (YES_THRESHOLD - p) / YES_THRESHOLD
        conviction = min(1.0, base_conviction + conviction_boost)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = YES_THRESHOLD - p
        return "yes", size, (
            f"YES {p:.0%} edge={edge:.0%} whales={whale_count} "
            f"boost=+{conviction_boost:.0%} size=${size} — {q[:55]}"
        )

    if p >= NO_THRESHOLD and whale_direction == "no":
        base_conviction = (p - NO_THRESHOLD) / (1 - NO_THRESHOLD)
        conviction = min(1.0, base_conviction + conviction_boost)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = p - NO_THRESHOLD
        return "no", size, (
            f"NO YES={p:.0%} edge={edge:.0%} whales={whale_count} "
            f"boost=+{conviction_boost:.0%} size=${size} — {q[:55]}"
        )

    # Whale direction doesn't align with threshold signal
    if whale_direction == "yes" and p > YES_THRESHOLD:
        return None, 0, (
            f"Whale YES but p={p:.0%} > YES_THRESHOLD={YES_THRESHOLD:.0%} — no alignment"
        )
    if whale_direction == "no" and p < NO_THRESHOLD:
        return None, 0, (
            f"Whale NO but p={p:.0%} < NO_THRESHOLD={NO_THRESHOLD:.0%} — no alignment"
        )

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
            safe_print(f"  [warn] {w}")
    except Exception as e:
        safe_print(f"  [ctx] {market_id}: {e}")
    return True, "ok"


def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    safe_print(
        f"[whale-momentum] mode={mode} max_pos=${MAX_POSITION} "
        f"min_whales={MIN_WHALES} lookback={LOOKBACK_HOURS}h "
        f"top_wallets={LEADERBOARD_LIMIT}"
    )

    client = get_client(live=live)

    # Step 1: Fetch leaderboard -> top N wallets
    wallets = fetch_leaderboard()
    if not wallets:
        safe_print("[whale-momentum] No wallets fetched from leaderboard. Exiting.")
        return

    # Step 2: For each wallet, fetch recent activity
    activities_per_wallet: dict[str, list[dict]] = {}
    total_activities = 0
    for w in wallets:
        addr = _extract_wallet_address(w)
        if not addr:
            continue
        acts = fetch_recent_activity(addr, hours=LOOKBACK_HOURS)
        if acts:
            activities_per_wallet[addr] = acts
            total_activities += len(acts)
            safe_print(f"  [wallet] {addr[:10]}... {len(acts)} trades in {LOOKBACK_HOURS}h")

    safe_print(
        f"[whale-momentum] {len(activities_per_wallet)} wallets with activity, "
        f"{total_activities} total trades"
    )

    if not activities_per_wallet:
        safe_print("[whale-momentum] No recent whale activity found. Exiting.")
        return

    # Step 3: Build momentum map across all wallets
    momentum_map = build_momentum_map(activities_per_wallet)
    safe_print(f"[whale-momentum] {len(momentum_map)} distinct markets in momentum map")

    # Step 4: Find momentum signals (markets with MIN_WHALES+ agreement)
    signals = find_momentum_signals(momentum_map, MIN_WHALES)
    safe_print(f"[whale-momentum] {len(signals)} momentum signals (>={MIN_WHALES} whales)")

    if not signals:
        safe_print("[whale-momentum] No whale consensus signals found. Done.")
        return

    # Step 5-6: For each signal, find matching Simmer market and trade
    placed = 0
    for title, direction, whale_count, volume in signals:
        if placed >= MAX_POSITIONS:
            break

        safe_print(
            f"  [signal] {direction.upper()} x{whale_count} whales "
            f"vol=${volume:.0f} — {title[:60]}"
        )

        # Find matching market in Simmer
        market = find_matching_market(client, title)
        if not market:
            safe_print(f"    [skip] No matching Simmer market found")
            continue

        # Compute whale-boosted signal
        side, size, reasoning = compute_whale_boosted_signal(market, direction, whale_count)
        if not side:
            safe_print(f"    [skip] {reasoning}")
            continue

        # Context safety checks
        ok, why = context_ok(client, market.id)
        if not ok:
            safe_print(f"    [skip] {why}")
            continue

        # Place trade
        try:
            r = client.trade(
                market_id=market.id,
                side=side,
                amount=size,
                source=TRADE_SOURCE,
                skill_slug=SKILL_SLUG,
                reasoning=reasoning,
            )
            tag    = "(sim)" if r.simulated else "(live)"
            status = "OK" if r.success else f"FAIL:{r.error}"
            safe_print(f"    [trade] {side.upper()} ${size} {tag} {status} — {reasoning[:70]}")
            if r.success:
                placed += 1
        except Exception as e:
            safe_print(f"    [error] {market.id}: {e}")

    # Step 7: Summary
    safe_print(f"[whale-momentum] done. {placed} orders placed from {len(signals)} signals.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Detects whale momentum consensus on Polymarket and trades with boosted conviction."
    )
    ap.add_argument(
        "--live", action="store_true",
        help="Real trades on Polymarket. Default is paper (sim) mode.",
    )
    run(live=ap.parse_args().live)
