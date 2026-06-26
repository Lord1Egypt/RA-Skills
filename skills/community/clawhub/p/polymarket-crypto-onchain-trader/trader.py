"""
polymarket-crypto-onchain-trader
Trades crypto price milestone, ETF flow, and on-chain protocol markets on Polymarket.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag.
"""
import os
import argparse
from datetime import datetime, timezone
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-crypto-onchain-trader"
SKILL_SLUG   = "polymarket-crypto-onchain-trader"

KEYWORDS = [
    'Bitcoin', 'BTC', 'Ethereum', 'ETH', 'Solana', 'SOL', 'crypto',
    'ETF', 'halving', 'all-time high', 'ATH', '$100k', '$200k',
    'stablecoin', 'USDC', 'Tether', 'DeFi', 'Uniswap', 'Aave',
    'Layer 2', 'Arbitrum', 'Base', 'BlackRock', 'spot ETF', 'inflows',
    'hash rate', 'mempool', 'TVL', 'total value locked', 'EIP',
    'hard fork', 'upgrade', 'Pectra', 'Dencun', 'funding rate',
    'open interest', 'exchange outflow', 'whale', 'on-chain',
]

# Risk parameters — declared as tunables in clawhub.json, adjustable from Simmer UI.
# Named SIMMER_* so apply_skill_config() can load automaton-managed overrides.
MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  "35"))
MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    "1000"))
MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.06"))
MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      "0"))
MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "8"))
# Signal thresholds — buy YES below YES_THRESHOLD, sell NO above NO_THRESHOLD.
# Position size scales with conviction, adjusted by on-chain instrument type and cycle phase.
YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.42"))
NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",  "0.58"))
MIN_TRADE      = float(os.environ.get("SIMMER_MIN_TRADE",     "5"))

# Bitcoin halving dates — the cycle is mathematically deterministic (~210,000 blocks).
# Last halving: April 19, 2024 (block 840,000). Next: ~April 2028.
_LAST_BTC_HALVING = datetime(2024, 4, 19, tzinfo=timezone.utc)
_NEXT_BTC_HALVING = datetime(2028, 4, 18, tzinfo=timezone.utc)  # approximate

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
            if m.id not in seen and any(w in q for w in ("bitcoin", "btc", "ethereum", "eth ", "solana", "crypto", "defi")):
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
            if m.id not in seen and any(w in q for w in ("bitcoin", "btc", "ethereum", "eth ", "solana", "crypto", "defi")):
                seen.add(m.id)
                unique.append(m)
    except Exception:
        pass

    return unique


def _btc_cycle_mult() -> float:
    """
    Returns a BTC halving cycle phase multiplier based on days since last halving.

    The Bitcoin halving reduces miner reward by 50% every ~210,000 blocks (~4 years).
    Historical price cycle relative to halving (documented across 2012, 2016, 2020, 2024):

      Days 0–180   post-halving: Consolidation — miners selling, market absorbing. Mild.
      Days 181–540 post-halving: Bull phase — supply shock hits, institutional FOMO peaks.
                                  Historically strongest 12-month returns.
      Days 541–900 post-halving: Distribution — late retail arrival, price peaks, reversal.
                                  High variance; direction uncertain.
      Days 901+    post-halving: Bear phase — drawdown until next halving cycle.
                                  Fade bullish price targets.
    """
    days = (datetime.now(timezone.utc) - _LAST_BTC_HALVING).days
    if days < 181:
        return 1.05   # Early post-halving consolidation — mild bullish lean
    elif days < 541:
        return 1.20   # Peak bull window — historically strongest price gains
    elif days < 901:
        return 1.0    # Distribution/transition — uncertain, no directional boost
    else:
        return 0.85   # Bear market phase — fade BTC bullish price targets


def onchain_bias(question: str) -> float:
    """
    Returns a conviction multiplier (0.70–1.40) combining three crypto-specific
    structural edges:

    1. INSTRUMENT TYPE CONFIDENCE
       Different crypto market types have dramatically different predictability
       based on how much hard data exists before Polymarket retail prices them:

       Spot ETF inflows (BlackRock, Fidelity)     → 1.30x
         Daily flow data published by Farside/CoinGlass BEFORE Polymarket
         reprices ETF-flow threshold markets. This is the biggest information
         gap in crypto Polymarket — retail ignores public institutional data.

       BTC halving event markets                  → 1.25x
         The halving date is mathematically predictable to within ~2 weeks
         a year in advance (block ~210,000 intervals). Resolution uncertainty
         is near-zero — retail still prices these as genuinely uncertain.

       Protocol upgrade / hard fork dates         → 1.20x
         Ethereum EIP timelines, Solana upgrades — announced on GitHub and
         core dev calls weeks before. Retail prices them as uncertain when
         core devs have already agreed on a target date.

       DeFi TVL / on-chain protocol milestones    → 1.10x
         DeFiLlama tracks TVL in real-time with daily granularity. Markets
         on "will protocol X reach $Y TVL" lag the published on-chain data.

       BTC / ETH / SOL price milestones           → 1.10x  (× cycle mult for BTC)
         Directional bias from halving cycle and ETF flows, but high daily
         volatility means timing is uncertain — moderate base confidence.

       Stablecoin / regulatory milestones         → 1.05x
         SEC/CFTC regulatory calendars are partially predictable, but
         legal proceedings create ambiguity in resolution criteria.

       NFT / Ordinals market milestones           → 0.75x
         Pure narrative — no predictive on-chain data, retail-dominated.

       Memecoin / altcoin hype milestones         → 0.70x
         Zero predictive signal. Retail sentiment is the only driver.
         Conviction sizing should be minimal regardless of probability.

    2. BTC HALVING CYCLE PHASE (applied to BTC price markets only)
       For Bitcoin price milestone markets specifically, the halving cycle
       phase multiplies the base type confidence:
         Days 181–540 post-halving (bull phase)   → ×1.20
         Days 541–900 (distribution)              → ×1.00
         Days 901+    (bear phase)                → ×0.85

    3. ASIAN SESSION TIMING (regulatory / ban / approval news)
       Crypto regulatory news from South Korea, Japan, and China breaks during
       Asian business hours. Polymarket is US-dominated — repricing takes 15–30
       minutes when US retail is asleep.
         Asia active hours 01:00–09:00 UTC        → 1.15x for regulatory questions
         US prime time 13:00–21:00 UTC            → 0.95x (priced immediately)

    Combined and capped at 1.40x.
    """
    hour_utc = datetime.now(timezone.utc).hour
    q = question.lower()

    # Factor 1: instrument type confidence
    if any(w in q for w in ("etf inflow", "etf flow", "etf outflow", "blackrock",
                             "fidelity", "spot etf", "ibtc", "fbtc", "bitcoin etf",
                             "etf volume", "etf aum")):
        type_mult = 1.30  # Daily flow data published before Polymarket reprices

    elif any(w in q for w in ("halving", "halvening", "block reward", "miner reward",
                               "subsidy halving", "840000")):
        type_mult = 1.25  # Mathematically predictable date — retail misprices certainty

    elif any(w in q for w in ("upgrade", "eip", "hard fork", "pectra", "dencun",
                               "shapella", "cancun", "prague", "network upgrade",
                               "client release")):
        type_mult = 1.20  # GitHub/core dev call timelines published weeks ahead

    elif any(w in q for w in ("tvl", "total value locked", "protocol", "defi",
                               "uniswap", "aave", "compound", "curve", "maker",
                               "lido", "eigenlayer")):
        type_mult = 1.10  # DeFiLlama real-time data — markets on TVL milestones lag

    elif any(w in q for w in ("bitcoin", "btc price", "btc reach", "btc hit",
                               "btc above", "btc below")):
        # BTC price markets get halving cycle applied on top
        type_mult = 1.10 * _btc_cycle_mult()

    elif any(w in q for w in ("ethereum", "eth price", "eth reach", "solana", "sol price",
                               "all-time high", "ath", "$100k", "$200k", "$50k")):
        type_mult = 1.10  # Price milestones — on-chain data gives partial edge

    elif any(w in q for w in ("stablecoin", "usdc", "tether", "usdt", "regulation",
                               "sec crypto", "cftc crypto", "crypto bill", "crypto law")):
        type_mult = 1.05  # Regulatory calendar partially predictable

    elif any(w in q for w in ("nft", "opensea", "blur", "ordinal", "inscription",
                               "jpeg", "bored ape", "bayc")):
        type_mult = 0.75  # Narrative-driven — no on-chain predictive signal

    elif any(w in q for w in ("meme", "doge", "shib", "pepe", "memecoin",
                               "dog", "cat coin", "pump", "altcoin season")):
        type_mult = 0.70  # Pure retail sentiment — zero predictive signal

    else:
        type_mult = 1.0

    # Factor 2 (already applied above for BTC) — cycle mult baked in for BTC price markets

    # Factor 3: Asian session timing for regulatory/ban/approval news
    asia_regulatory = ("korea", "south korea", "japan", "china", "chinese",
                       "ban", "banned", "approval", "approved", "regulatory",
                       "binance", "exchange license", "crypto license")
    if any(w in q for w in asia_regulatory):
        if 1 <= hour_utc <= 9:
            timing_mult = 1.15  # Asian business hours — US retail asleep, lag window open
        elif 13 <= hour_utc <= 21:
            timing_mult = 0.95  # US prime time — reprices within minutes
        else:
            timing_mult = 1.0
    else:
        timing_mult = 1.0

    return min(1.40, type_mult * timing_mult)


def compute_signal(market) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    Conviction-based sizing with on-chain instrument type, BTC halving cycle,
    and Asian session timing adjustment:
    - Base conviction scales linearly with distance from threshold
    - onchain_bias() stacks three layers: instrument confidence (ETF flows 1.30x,
      halving 1.25x, protocol upgrades 1.20x), BTC cycle phase (×0.85–1.20 for
      BTC price markets), and Asian regulatory timing (1.15x when US is asleep)
    - Memecoins and NFTs dampened to 0.70–0.75x — low signal, trade small
    - Result capped at 1.0 so size never exceeds MAX_POSITION
    - MIN_TRADE floor prevents trivially small orders near the boundary

    Remix: feed Farside BTC ETF daily flow data into p to trade the divergence
    between published institutional flows and Polymarket retail pricing directly.
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

    bias = onchain_bias(q)

    if p <= YES_THRESHOLD:
        # conviction=0 at threshold boundary, conviction=1 at p=0 — scaled by on-chain bias
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
    days_since_halving = (datetime.now(timezone.utc) - _LAST_BTC_HALVING).days
    print(f"[polymarket-crypto-onchain-trader] mode={mode} max_pos=${MAX_POSITION} min_vol=${MIN_VOLUME} max_spread={MAX_SPREAD:.0%} min_days={MIN_DAYS} btc_cycle_day={days_since_halving}")

    client  = get_client(live=live)
    markets = find_markets(client)
    print(f"[polymarket-crypto-onchain-trader] {len(markets)} candidate markets")

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

    print(f"[polymarket-crypto-onchain-trader] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Trades crypto price milestone, ETF flow, and on-chain protocol markets on Polymarket.")
    ap.add_argument("--live", action="store_true",
                    help="Real trades on Polymarket. Default is paper (sim) mode.")
    run(live=ap.parse_args().live)
