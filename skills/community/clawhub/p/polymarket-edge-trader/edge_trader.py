#!/usr/bin/env python3
"""
Polymarket Edge Trader Skill

A remixable AION trading skill that:
- Scans Polymarket for high-edge opportunities
- Uses your fair probability estimate as the signal
- Applies Kelly-fraction sizing with configurable risk multiplier
- Checks market context safeguards before execution
- Auto-redeems resolved markets
- Defaults to dry-run mode (--live for real trades)
"""

import argparse
import json
import os
import random
import sys
import time
from typing import Any, Dict, List, Optional

from aion_sdk import AionMarketClient

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(line_buffering=True)

SKILL_SLUG = "polymarket-edge-trader"
TRADE_SOURCE = "sdk:polymarket-edge-trader"
VENUE = "polymarket"

# Defaults
DEFAULT_QUERY = "bitcoin"
DEFAULT_PROBABILITY = 0.60
DEFAULT_MAX_MARKETS = 25
DEFAULT_MAX_STAKE_USD = 50.0
DEFAULT_MIN_EDGE = 0.03
DEFAULT_MAX_SLIPPAGE_PCT = 0.15
DEFAULT_STARTING_BALANCE_USD = 1000.0
DEFAULT_KELLY_MULTIPLIER = 0.25
DEFAULT_MIN_EV = 0.03

_client = None


def get_client() -> AionMarketClient:
    """Get or create AionMarketClient singleton."""
    global _client
    if _client is None:
        api_key = os.getenv("AION_API_KEY")
        if not api_key:
            raise ValueError("AION_API_KEY environment variable is required")
        base_url = os.getenv("AION_BASE_URL", "https://pm-t1.bxingupdate.com/bvapi")
        _client = AionMarketClient(api_key=api_key, base_url=base_url)
    return _client


def env_float(name: str, default: float) -> float:
    """Parse float from environment variable."""
    value = os.getenv(name, "").strip()
    if not value:
        return default
    try:
        return float(value)
    except ValueError:
        return default


def env_int(name: str, default: int) -> int:
    """Parse int from environment variable."""
    value = os.getenv(name, "").strip()
    if not value:
        return default
    try:
        return int(value)
    except ValueError:
        return default


def clamp_probability(p: float) -> float:
    """Clamp probability to [0.001, 0.999]."""
    return max(0.001, min(0.999, float(p)))


def kelly_fraction(
    p_win: float, market_price: float, kelly_multiplier: float = 0.25, min_ev: float = 0.03
) -> float:
    """
    Compute Kelly-fraction sized position.
    
    Args:
        p_win: Estimated win probability (0-1)
        market_price: Current market price (0-1)
        kelly_multiplier: Fraction of full Kelly to use (risk control)
        min_ev: Minimum expected value threshold
    
    Returns:
        Fraction of bankroll to stake (0-1)
    """
    p_win = clamp_probability(p_win)
    market_price = clamp_probability(market_price)
    
    edge = p_win - market_price
    if edge < min_ev:
        return 0.0
    
    # Full Kelly: (bp - q) / b where b = odds ratio - 1; simplified for binary:
    # kelly = (p * (1-q) - q * p) / (1 - q) = (p - q) / (1 - q)
    kelly = edge / max(1.0 - market_price, 0.001)
    kelly = max(0.0, min(1.0, kelly))
    return kelly * kelly_multiplier


def auto_redeem_if_possible() -> None:
    """Auto-redeem resolved markets per AION best practices."""
    try:
        client = get_client()
        results = client.auto_redeem()
    except Exception as exc:
        print(f"Auto-redeem skipped: {exc}")
        return
    
    if not isinstance(results, list):
        return
    
    redeemed = [r for r in results if r.get("success")]
    if redeemed:
        for item in redeemed:
            market_id = item.get("market_id")
            tx_hash = item.get("tx_hash")
            print(f"Redeemed {market_id}: tx={tx_hash}")


def discover_markets(query: str, max_markets: int) -> List[Dict[str, Any]]:
    """Discover active markets matching query."""
    try:
        client = get_client()
        response = client.get_markets(q=query, limit=max_markets, venue=VENUE)
    except Exception as exc:
        print(f"Market discovery failed: {exc}")
        return []
    
    if isinstance(response, list):
        return response
    if isinstance(response, dict):
        for key in ("markets", "items", "results", "data"):
            if isinstance(response.get(key), list):
                return response.get(key) or []
    return []


def get_market_context(market_id: str, my_probability: float) -> Optional[Dict[str, Any]]:
    """Fetch market context with safeguards."""
    try:
        client = get_client()
        return client.get_market_context(
            market_id=str(market_id), 
            venue=VENUE, 
            my_probability=my_probability
        )
    except Exception as exc:
        print(f"Context fetch failed for {market_id}: {exc}")
        return None


def get_yes_price(market: Dict[str, Any], context: Optional[Dict[str, Any]]) -> Optional[float]:
    """Extract YES price from market or context."""
    candidates = []
    if context and isinstance(context.get("market"), dict):
        candidates.append(context["market"])
    candidates.append(market)
    
    for source in candidates:
        for key in ("yesPrice", "yes_price", "current_probability", "price_yes"):
            value = source.get(key)
            if isinstance(value, (int, float)):
                return clamp_probability(float(value))
    return None


def has_warnings(context: Optional[Dict[str, Any]]) -> bool:
    """Check if context has trading warnings."""
    if not context:
        return False
    
    warnings = context.get("warnings") or []
    if warnings:
        return True
    
    trading = context.get("trading") or {}
    if trading.get("flip_flop_warning"):
        return True
    
    return False


def extract_slippage_pct(context: Optional[Dict[str, Any]]) -> float:
    """Extract slippage percentage from context."""
    if not context:
        return 0.0
    
    warnings = context.get("warnings") or []
    for warning in warnings:
        for key in ("slippagePct", "slippage_pct"):
            value = warning.get(key)
            if isinstance(value, (int, float)):
                return float(value)
    
    slippage = context.get("slippage") or {}
    for key in ("slippagePct", "slippage_pct"):
        value = slippage.get(key)
        if isinstance(value, (int, float)):
            return float(value)
    
    return 0.0


def get_question(market: Dict[str, Any]) -> str:
    """Extract market question/title."""
    for key in ("question", "title", "marketQuestion"):
        value = market.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return str(market.get("id", "unknown"))


def get_condition_id(market: Dict[str, Any]) -> Optional[str]:
    """Extract condition ID for order submission."""
    for key in ("conditionId", "condition_id"):
        value = market.get(key)
        if isinstance(value, str) and value:
            return value
    return None


def get_briefing(wallet_address: Optional[str]) -> Dict[str, Any]:
    """Fetch operator briefing with risk alerts and opportunity markets."""
    try:
        client = get_client()
        return client.get_briefing(
            venue=VENUE, 
            include_markets=True, 
            user=wallet_address or None
        ) or {}
    except Exception as exc:
        print(f"Briefing fetch failed: {exc}")
        return {}


def get_risk_alerts(briefing: Dict[str, Any]) -> List[str]:
    """Extract risk alerts from briefing."""
    alerts = briefing.get("riskAlerts") or briefing.get("risk_alerts") or []
    results = []
    for alert in alerts:
        if isinstance(alert, str):
            results.append(alert)
        elif isinstance(alert, dict):
            msg = alert.get("message") or alert.get("alert") or alert.get("type")
            if isinstance(msg, str):
                results.append(msg)
    return results


def get_bankroll(briefing: Dict[str, Any], fallback: float) -> float:
    """Extract current bankroll from briefing."""
    venues = briefing.get("venues") or {}
    venue_data = venues.get(VENUE) or {}
    balance = venue_data.get("balance")
    if isinstance(balance, (int, float)) and balance > 0:
        return float(balance)
    
    for key in ("balanceUsdc", "balance"):
        value = briefing.get(key)
        if isinstance(value, (int, float)) and value > 0:
            return float(value)
    
    return fallback


def score_markets(
    markets: List[Dict[str, Any]],
    fair_probability: float,
    min_edge: float,
) -> List[Dict[str, Any]]:
    """Score markets and return ranked candidates."""
    candidates = []
    
    for market in markets:
        market_id = market.get("id")
        if not market_id:
            continue
        
        context = get_market_context(str(market_id), fair_probability)
        
        yes_price = get_yes_price(market, context)
        if yes_price is None:
            continue
        
        edge = fair_probability - yes_price
        abs_edge = abs(edge)
        
        if abs_edge < min_edge:
            continue
        
        side = "YES" if edge > 0 else "NO"
        side_prob = fair_probability if side == "YES" else 1 - fair_probability
        
        candidates.append({
            "market": market,
            "context": context,
            "market_id": str(market_id),
            "yes_price": yes_price,
            "side": side,
            "edge": abs_edge,
            "side_probability": clamp_probability(side_prob),
        })
    
    # Sort by edge descending
    candidates.sort(key=lambda c: c["edge"], reverse=True)
    return candidates


def print_operator_summary(
    risk_alerts: List[str],
    decisions: List[str],
    order_updates: List[str],
) -> None:
    """Print operator-facing summary per AION best practices."""
    print(f"\nSkill: {SKILL_SLUG}")
    print(f"Venue: {VENUE}")
    
    print("Risk alerts:")
    if risk_alerts:
        for alert in risk_alerts:
            print(f"  - {alert}")
    else:
        print("  - none")
    
    print("Decisions:")
    for decision in decisions:
        print(f"  - {decision}")
    
    print("Order updates:")
    if order_updates:
        for update in order_updates:
            print(f"  - {update}")
    else:
        print("  - none")
    print()


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Polymarket Edge Trader — template for remixing"
    )
    parser.add_argument(
        "--query",
        default=os.getenv("MARKET_QUERY", DEFAULT_QUERY),
        help="Market search query (default: bitcoin)",
    )
    parser.add_argument(
        "--probability",
        type=float,
        default=env_float("MODEL_PROBABILITY", DEFAULT_PROBABILITY),
        help="Fair YES probability 0-1 (default: 0.60)",
    )
    parser.add_argument(
        "--max-markets",
        type=int,
        default=env_int("MAX_MARKETS", DEFAULT_MAX_MARKETS),
        help="Max markets to scan (default: 25)",
    )
    parser.add_argument(
        "--max-stake-usd",
        type=float,
        default=env_float("MAX_STAKE_USD", DEFAULT_MAX_STAKE_USD),
        help="Max stake per trade in USD (default: 50)",
    )
    parser.add_argument(
        "--min-edge",
        type=float,
        default=env_float("MIN_EDGE", DEFAULT_MIN_EDGE),
        help="Minimum edge threshold (default: 0.03)",
    )
    parser.add_argument(
        "--max-slippage-pct",
        type=float,
        default=env_float("MAX_SLIPPAGE_PCT", DEFAULT_MAX_SLIPPAGE_PCT),
        help="Max slippage tolerance (default: 0.15)",
    )
    parser.add_argument(
        "--starting-balance-usd",
        type=float,
        default=env_float("STARTING_BALANCE_USD", DEFAULT_STARTING_BALANCE_USD),
        help="Fallback bankroll (default: 1000)",
    )
    parser.add_argument(
        "--wallet-address",
        default=os.getenv("WALLET_ADDRESS", "").strip(),
        help="Wallet address (for briefing, context, live orders)",
    )
    parser.add_argument(
        "--show-candidates",
        action="store_true",
        help="Print ranked candidates before trading",
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Submit live orders (default: dry-run only)",
    )
    parser.add_argument(
        "--daemon",
        action="store_true",
        help="Run in loop with jitter (for cron/automaton)",
    )
    parser.add_argument(
        "--poll-interval",
        type=int,
        default=60,
        help="Base poll interval seconds (default: 60)",
    )
    return parser.parse_args()


def run_once(args: argparse.Namespace) -> int:
    """Execute one trading cycle."""
    try:
        client = get_client()
    except ValueError as exc:
        print(f"Client error: {exc}")
        return 1
    
    # Auto-redeem any claimable positions
    auto_redeem_if_possible()
    
    # Get briefing and risk alerts
    briefing = get_briefing(args.wallet_address)
    risk_alerts = get_risk_alerts(briefing)
    
    decisions = []
    order_updates = []
    
    # Check risk alerts
    if risk_alerts:
        decisions.append("SKIP: Risk alerts active; running de-risk logic instead")
        print_operator_summary(risk_alerts, decisions, order_updates)
        return 0
    
    # Discover markets
    markets = discover_markets(args.query, args.max_markets)
    if not markets:
        decisions.append(f"HOLD: No markets matched query '{args.query}'")
        print_operator_summary(risk_alerts, decisions, order_updates)
        return 0
    
    # Score and rank
    candidates = score_markets(markets, args.probability, args.min_edge)
    
    if args.show_candidates and candidates:
        print("Ranked candidates:")
        for i, c in enumerate(candidates[:5], 1):
            q = get_question(c["market"])[:60]
            print(f"  {i}. {c['side']} | YES={c['yes_price']:.3f} | edge={c['edge']:.3f} | {q}")
    
    if not candidates:
        decisions.append("HOLD: No candidates cleared edge threshold")
        print_operator_summary(risk_alerts, decisions, order_updates)
        return 0
    
    # Select best candidate
    best = candidates[0]
    
    # Check for warnings
    context = best["context"]
    if has_warnings(context):
        decisions.append(f"SKIP: Market {best['market_id']} has trading warnings")
        print_operator_summary(risk_alerts, decisions, order_updates)
        return 0
    
    # Check slippage
    slippage = extract_slippage_pct(context)
    if slippage > args.max_slippage_pct:
        decisions.append(
            f"SKIP: Slippage {slippage:.1%} exceeds {args.max_slippage_pct:.1%}"
        )
        print_operator_summary(risk_alerts, decisions, order_updates)
        return 0
    
    # Size position
    bankroll = get_bankroll(briefing, args.starting_balance_usd)
    kelly_mult = env_float("AION_KELLY_MULTIPLIER", DEFAULT_KELLY_MULTIPLIER)
    min_ev = env_float("AION_MIN_EV", DEFAULT_MIN_EV)
    size_fraction = kelly_fraction(best["side_probability"], best["yes_price"], kelly_mult, min_ev)
    amount_usd = bankroll * size_fraction
    amount_usd = min(amount_usd, args.max_stake_usd)
    
    if amount_usd <= 0:
        decisions.append(f"HOLD: Kelly sizing returned {amount_usd:.2f}; below minimum")
        print_operator_summary(risk_alerts, decisions, order_updates)
        return 0
    
    # Build reasoning
    reasoning = (
        f"Edge signal: {best['side']} at {best['yes_price']:.1%} "
        f"vs fair {args.probability:.1%} (edge {best['edge']:.1%}); "
        f"Kelly sizing {size_fraction:.1%} of {bankroll:.0f} USDC"
    )
    
    # Dry-run
    if not args.live:
        decisions.append(
            f"TRADE {best['side']} {best['market_id']} ~ ${amount_usd:.2f}"
        )
        order_updates.append(
            f"DRY-RUN ONLY — pass --live with WALLET_ADDRESS and AION_SIGNED_ORDER_JSON to submit"
        )
        print_operator_summary(risk_alerts, decisions, order_updates)
        return 0
    
    # Live trade
    wallet_address = args.wallet_address
    if not wallet_address:
        decisions.append("SKIP: --live requires WALLET_ADDRESS")
        print_operator_summary(risk_alerts, decisions, order_updates)
        return 1
    
    signed_order_json = os.getenv("AION_SIGNED_ORDER_JSON", "").strip()
    if not signed_order_json:
        decisions.append("SKIP: --live requires AION_SIGNED_ORDER_JSON")
        print_operator_summary(risk_alerts, decisions, order_updates)
        return 1
    
    try:
        order_payload = json.loads(signed_order_json)
    except json.JSONDecodeError as exc:
        decisions.append(f"SKIP: Invalid AION_SIGNED_ORDER_JSON: {exc}")
        print_operator_summary(risk_alerts, decisions, order_updates)
        return 1
    
    condition_id = get_condition_id(best["market"])
    if not condition_id:
        decisions.append("SKIP: No condition ID for trade payload")
        print_operator_summary(risk_alerts, decisions, order_updates)
        return 1
    
    payload = {
        "venue": VENUE,
        "marketConditionId": condition_id,
        "marketQuestion": get_question(best["market"]),
        "outcome": best["side"],
        "orderSize": round(amount_usd, 2),
        "price": round(best["yes_price"], 4),
        "isLimitOrder": True,
        "orderType": "GTC",
        "walletAddress": wallet_address,
        "reasoning": reasoning,
        "source": TRADE_SOURCE,
        "skill_slug": SKILL_SLUG,
        "order": order_payload,
    }
    
    try:
        result = client.trade(payload)
    except Exception as exc:
        decisions.append(f"SKIP: Trade submission failed: {exc}")
        print_operator_summary(risk_alerts, decisions, order_updates)
        return 1
    
    order_id = result.get("orderId") or result.get("id") or "unknown"
    order_status = result.get("orderStatus") or result.get("status") or "submitted"
    
    decisions.append(
        f"TRADE {best['side']} {best['market_id']} ~ ${amount_usd:.2f}"
    )
    order_updates.append(f"submitted {order_id} status={order_status}")
    print_operator_summary(risk_alerts, decisions, order_updates)
    return 0


def main() -> int:
    """Main entry point."""
    args = parse_args()
    
    if not args.daemon:
        return run_once(args)
    
    # Daemon mode with jitter
    base_interval = args.poll_interval
    jitter_range = min(8, base_interval // 8)
    
    while True:
        run_once(args)
        sleep_time = max(15, base_interval + random.randint(-jitter_range, jitter_range))
        time.sleep(sleep_time)


if __name__ == "__main__":
    sys.exit(main())
