"""
polymarket-whale-contrarian-trader
Detects smart money divergence: when top-performing whale wallets take
positions opposite to retail consensus at probability extremes.

THE EDGE:
  Whale wallets on Polymarket leaderboards have demonstrated sustained
  profitability — their edge comes from superior information, better models,
  or deeper domain expertise. When a market sits at a probability extreme
  (>70% or <30%), it reflects heavy retail positioning in one direction.

  If multiple top whales are simultaneously betting AGAINST that retail
  consensus, it is a strong signal that the market is mispriced:

  1. Fetch the public Polymarket leaderboard → top wallet addresses.
  2. Fetch recent trading activity for each whale wallet.
  3. Identify markets at probability extremes (retail consensus).
  4. Check if whales are taking the opposite side → contrarian signal.
  5. Trade in the whale's direction with conviction-boosted sizing.

  The more whales that independently take the contrarian side, the stronger
  the signal — each additional whale adds conviction via a multiplier.

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
from simmer_sdk import SimmerClient
import urllib.request

TRADE_SOURCE = "sdk:polymarket-whale-contrarian-trader"
SKILL_SLUG   = "polymarket-whale-contrarian-trader"

# Public APIs
LEADERBOARD_URL = "https://predicting.top/api/leaderboard"
DATA_API        = "https://data-api.polymarket.com"

# Risk parameters
MAX_POSITION  = float(os.environ.get("SIMMER_MAX_POSITION",  "40"))
MIN_VOLUME    = float(os.environ.get("SIMMER_MIN_VOLUME",    "5000"))
MAX_SPREAD    = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.08"))
MIN_DAYS      = int(os.environ.get(  "SIMMER_MIN_DAYS",      "7"))
MAX_POSITIONS = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "6"))
YES_THRESHOLD = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.38"))
NO_THRESHOLD  = float(os.environ.get("SIMMER_NO_THRESHOLD",  "0.62"))
MIN_TRADE     = float(os.environ.get("SIMMER_MIN_TRADE",     "5"))

# Skill-specific parameters
CONTRARIAN_THRESHOLD    = float(os.environ.get("SIMMER_CONTRARIAN_THRESHOLD",    "0.70"))
MIN_WHALE_OPPOSITION    = int(os.environ.get(  "SIMMER_MIN_WHALE_OPPOSITION",    "2"))

_client: SimmerClient | None = None


def safe_print(*args, **kwargs):
    """Print that never crashes on encoding issues."""
    try:
        print(*args, **kwargs)
    except (UnicodeEncodeError, OSError):
        try:
            msg = " ".join(str(a) for a in args)
            print(msg.encode("ascii", errors="replace").decode(), **kwargs)
        except Exception:
            pass


def get_client(live: bool = False) -> SimmerClient:
    """
    live=False -> venue="sim"  (paper trades -- safe default).
    live=True  -> venue="polymarket" (real trades, only with --live flag).
    """
    global _client
    global MAX_POSITION, MIN_VOLUME, MAX_SPREAD, MIN_DAYS, MAX_POSITIONS
    global YES_THRESHOLD, NO_THRESHOLD, MIN_TRADE
    global CONTRARIAN_THRESHOLD, MIN_WHALE_OPPOSITION
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
        MAX_POSITION         = float(os.environ.get("SIMMER_MAX_POSITION",         str(MAX_POSITION)))
        MIN_VOLUME           = float(os.environ.get("SIMMER_MIN_VOLUME",           str(MIN_VOLUME)))
        MAX_SPREAD           = float(os.environ.get("SIMMER_MAX_SPREAD",           str(MAX_SPREAD)))
        MIN_DAYS             = int(os.environ.get(  "SIMMER_MIN_DAYS",             str(MIN_DAYS)))
        MAX_POSITIONS        = int(os.environ.get(  "SIMMER_MAX_POSITIONS",        str(MAX_POSITIONS)))
        YES_THRESHOLD        = float(os.environ.get("SIMMER_YES_THRESHOLD",        str(YES_THRESHOLD)))
        NO_THRESHOLD         = float(os.environ.get("SIMMER_NO_THRESHOLD",         str(NO_THRESHOLD)))
        MIN_TRADE            = float(os.environ.get("SIMMER_MIN_TRADE",            str(MIN_TRADE)))
        CONTRARIAN_THRESHOLD = float(os.environ.get("SIMMER_CONTRARIAN_THRESHOLD", str(CONTRARIAN_THRESHOLD)))
        MIN_WHALE_OPPOSITION = int(os.environ.get(  "SIMMER_MIN_WHALE_OPPOSITION", str(MIN_WHALE_OPPOSITION)))
    return _client


def fetch_leaderboard(limit: int = 50) -> list[str]:
    """
    Fetch top wallet addresses from the public Polymarket leaderboard.
    Returns a list of wallet address strings.
    """
    try:
        url = f"{LEADERBOARD_URL}?limit={limit}"
        req = urllib.request.Request(url, headers={"User-Agent": "polymarket-whale-contrarian-trader/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
        wallets = []
        entries = data if isinstance(data, list) else data.get("traders", data.get("leaderboard", data.get("data", [])))
        for entry in entries:
            addr = entry.get("address") or entry.get("wallet") or entry.get("user")
            if addr and isinstance(addr, str) and len(addr) > 10:
                wallets.append(addr.lower())
        safe_print(f"  [leaderboard] fetched {len(wallets)} whale wallets")
        return wallets
    except Exception as e:
        safe_print(f"  [leaderboard] error: {e}")
        return []


def fetch_wallet_activity(wallet: str, limit: int = 100) -> list[dict]:
    """
    Fetch recent trading activity for a wallet from the public data API.
    Returns list of trade dicts with at minimum: market_id/condition_id, side, size.
    """
    try:
        url = f"{DATA_API}/activity?user={wallet}&limit={limit}"
        req = urllib.request.Request(url, headers={"User-Agent": "polymarket-whale-contrarian-trader/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
        trades = data if isinstance(data, list) else data.get("trades", data.get("data", []))
        return trades
    except Exception as e:
        safe_print(f"  [activity] {wallet[:10]}...: {e}")
        return []


def find_contrarian_signals(client: SimmerClient, whale_activities: dict[str, list[dict]]) -> list[tuple]:
    """
    Cross-reference extreme-probability markets with whale activity.

    For each market at a probability extreme (retail consensus), check if
    whales are buying the opposite side. Returns list of:
        (market, whale_direction, opposing_whale_count)
    """
    try:
        markets = client.get_markets(limit=200)
    except Exception as e:
        safe_print(f"  [markets] error fetching markets: {e}")
        return []

    # Build index: market_id -> {yes_whales: set, no_whales: set}
    whale_positions: dict[str, dict[str, set]] = {}
    for wallet, trades in whale_activities.items():
        for trade in trades:
            mid = (trade.get("market_id") or trade.get("condition_id")
                   or trade.get("market") or trade.get("conditionId") or "")
            side = (trade.get("side") or trade.get("outcome") or "").lower()
            if not mid or side not in ("yes", "no", "buy", "sell"):
                continue
            # Normalize: "buy" typically means YES, "sell" means NO in Polymarket context
            if side == "buy":
                side = "yes"
            elif side == "sell":
                side = "no"
            if mid not in whale_positions:
                whale_positions[mid] = {"yes": set(), "no": set()}
            whale_positions[mid][side].add(wallet)

    signals = []
    for m in markets:
        p = m.current_probability
        mid = m.id

        # Check if market is at a probability extreme
        is_retail_yes = p > CONTRARIAN_THRESHOLD        # retail heavily says YES
        is_retail_no  = p < (1 - CONTRARIAN_THRESHOLD)  # retail heavily says NO

        if not is_retail_yes and not is_retail_no:
            continue

        wp = whale_positions.get(mid, {"yes": set(), "no": set()})

        if is_retail_yes:
            # Retail says YES (p>70%), check if whales are buying NO
            opposing_count = len(wp["no"])
            if opposing_count >= MIN_WHALE_OPPOSITION:
                signals.append((m, "no", opposing_count))
        elif is_retail_no:
            # Retail says NO (p<30%), check if whales are buying YES
            opposing_count = len(wp["yes"])
            if opposing_count >= MIN_WHALE_OPPOSITION:
                signals.append((m, "yes", opposing_count))

    safe_print(f"  [contrarian] {len(signals)} signals from {len(markets)} markets")
    return signals


def compute_signal(market) -> tuple[str | None, float, str]:
    """
    Standard conviction-based signal per CLAUDE.md.
    Returns (side, size, reasoning) or (None, 0, skip_reason).
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


def compute_contrarian_signal(market, whale_side: str, whale_count: int) -> tuple[str | None, float, str]:
    """
    Whale-enhanced contrarian signal. Trades in the whale's direction (against
    retail) with conviction boosted by the number of opposing whales.

    Conviction multiplier: 1.0 + min(0.4, (whale_count - 1) * 0.1)
      - 2 whales: 1.1x
      - 3 whales: 1.2x
      - 5+ whales: 1.4x (cap)
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

    whale_mult = 1.0 + min(0.4, (whale_count - 1) * 0.1)

    # Whale says YES — trade YES if within threshold band or trust whales at base sizing
    if whale_side == "yes":
        if p <= YES_THRESHOLD:
            # Whale direction aligns with threshold band — enhanced signal
            conviction = (YES_THRESHOLD - p) / YES_THRESHOLD
            conviction = min(1.0, conviction * whale_mult)
            size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
            edge = YES_THRESHOLD - p
            return "yes", size, (
                f"WHALE-YES {p:.0%} edge={edge:.0%} whales={whale_count} "
                f"mult={whale_mult:.1f}x size=${size} — {q[:60]}"
            )
        else:
            # Whale direction outside threshold band — trust whales with base sizing
            size = MIN_TRADE
            return "yes", size, (
                f"WHALE-TRUST-YES {p:.0%} whales={whale_count} "
                f"size=${size} (base) — {q[:60]}"
            )

    # Whale says NO — trade NO if within threshold band or trust whales at base sizing
    if whale_side == "no":
        if p >= NO_THRESHOLD:
            # Whale direction aligns with threshold band — enhanced signal
            conviction = (p - NO_THRESHOLD) / (1 - NO_THRESHOLD)
            conviction = min(1.0, conviction * whale_mult)
            size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
            edge = p - NO_THRESHOLD
            return "no", size, (
                f"WHALE-NO YES={p:.0%} edge={edge:.0%} whales={whale_count} "
                f"mult={whale_mult:.1f}x size=${size} — {q[:60]}"
            )
        else:
            # Whale direction outside threshold band — trust whales with base sizing
            size = MIN_TRADE
            return "no", size, (
                f"WHALE-TRUST-NO YES={p:.0%} whales={whale_count} "
                f"size=${size} (base) — {q[:60]}"
            )

    return None, 0, f"No valid whale side for {q[:70]}"


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


def find_markets(client: SimmerClient) -> list:
    """Fetch active markets from the SDK."""
    try:
        return client.get_markets(limit=200)
    except Exception as e:
        safe_print(f"  [markets] error: {e}")
        return []


def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    safe_print(
        f"[whale-contrarian] mode={mode} "
        f"contrarian_thresh={CONTRARIAN_THRESHOLD:.0%} "
        f"min_whales={MIN_WHALE_OPPOSITION} "
        f"max_pos=${MAX_POSITION}"
    )

    client = get_client(live=live)

    # Step 1: Fetch leaderboard -> whale wallets
    safe_print("[whale-contrarian] fetching leaderboard...")
    wallets = fetch_leaderboard(limit=50)
    if not wallets:
        safe_print("[whale-contrarian] no wallets found, aborting.")
        return

    # Step 2: Fetch activity per wallet
    safe_print(f"[whale-contrarian] fetching activity for {len(wallets)} wallets...")
    whale_activities: dict[str, list[dict]] = {}
    for w in wallets:
        trades = fetch_wallet_activity(w, limit=100)
        if trades:
            whale_activities[w] = trades
    safe_print(f"[whale-contrarian] {len(whale_activities)} wallets with activity")

    if not whale_activities:
        safe_print("[whale-contrarian] no whale activity found, aborting.")
        return

    # Step 3: Find contrarian signals
    safe_print("[whale-contrarian] scanning for contrarian signals...")
    signals = find_contrarian_signals(client, whale_activities)

    if not signals:
        safe_print("[whale-contrarian] no contrarian signals found.")
        return

    # Step 4: Trade on signals
    placed = 0
    for m, whale_side, whale_count in signals:
        if placed >= MAX_POSITIONS:
            break

        side, size, reasoning = compute_contrarian_signal(m, whale_side, whale_count)
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

    safe_print(f"[whale-contrarian] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description=(
            "Detects smart money divergence: when top whale wallets bet against "
            "retail consensus at probability extremes. Trades with the whales "
            "using conviction-boosted sizing."
        )
    )
    ap.add_argument("--live", action="store_true",
                    help="Real trades on Polymarket. Default is paper (sim) mode.")
    run(live=ap.parse_args().live)
