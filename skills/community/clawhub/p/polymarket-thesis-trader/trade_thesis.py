import argparse
import os
import sys
from typing import Any

from aion_sdk import AionClient


SKILL_SLUG = "polymarket-thesis-trader"
TRADE_SOURCE = f"sdk:{SKILL_SLUG}"
VENUE = "polymarket"

_client = None


def get_client() -> AionClient:
    global _client
    if _client is None:
        _client = AionClient(api_key=os.environ["AION_API_KEY"], venue=VENUE)
    return _client


def env_str(name: str, default: str) -> str:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip() or default


def env_float(name: str, default: float) -> float:
    value = os.getenv(name)
    if value in (None, ""):
        return default
    return float(value)


def env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value in (None, ""):
        return default
    return int(value)


def env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Trade Polymarket markets when a configured thesis probability has enough edge."
    )
    parser.add_argument("--query", default=env_str("MARKET_QUERY", "bitcoin"))
    parser.add_argument(
        "--thesis-probability",
        type=float,
        default=env_float("THESIS_PROBABILITY", 0.60),
        help="Fair probability from 0 to 1.",
    )
    parser.add_argument(
        "--min-edge",
        type=float,
        default=env_float("MIN_EDGE", 0.07),
        help="Minimum required edge before trading.",
    )
    parser.add_argument(
        "--trade-amount",
        type=float,
        default=env_float("TRADE_AMOUNT_USD", 5.0),
        help="Trade size in USD.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=env_int("MARKET_LIMIT", 8),
        help="Maximum number of matching markets to scan.",
    )
    parser.add_argument(
        "--max-price",
        type=float,
        default=env_float("MAX_ENTRY_PRICE", 0.85),
        help="Skip entries above this price.",
    )
    parser.add_argument(
        "--min-price",
        type=float,
        default=env_float("MIN_ENTRY_PRICE", 0.10),
        help="Skip entries below this price.",
    )
    parser.add_argument(
        "--auto-redeem",
        action="store_true",
        default=env_bool("AUTO_REDEEM", False),
        help="Redeem resolved positions after trading.",
    )
    parser.add_argument(
        "--live",
        action="store_true",
        default=env_bool("RUN_LIVE", False),
        help="Execute real trades. Default mode is dry-run.",
    )
    return parser.parse_args()


def validate_args(args: argparse.Namespace) -> None:
    if not 0.0 <= args.thesis_probability <= 1.0:
        raise ValueError("--thesis-probability must be between 0 and 1")
    if not 0.0 <= args.min_edge <= 1.0:
        raise ValueError("--min-edge must be between 0 and 1")
    if not 0.0 <= args.min_price <= 1.0:
        raise ValueError("--min-price must be between 0 and 1")
    if not 0.0 <= args.max_price <= 1.0:
        raise ValueError("--max-price must be between 0 and 1")
    if args.min_price > args.max_price:
        raise ValueError("--min-price cannot be greater than --max-price")
    if args.trade_amount <= 0:
        raise ValueError("--trade-amount must be positive")
    if args.limit <= 0:
        raise ValueError("--limit must be positive")


def safe_float(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def get_market_id(market: dict[str, Any]) -> str:
    return str(
        market.get("id")
        or market.get("marketId")
        or market.get("market_id")
        or market.get("conditionId")
        or market.get("condition_id")
    )


def get_market_title(market: dict[str, Any]) -> str:
    return (
        market.get("question")
        or market.get("title")
        or market.get("marketQuestion")
        or market.get("name")
        or "untitled market"
    )


def get_yes_price(market: dict[str, Any]) -> float | None:
    for key in ("yesPrice", "yes_price", "price", "lastPrice"):
        price = safe_float(market.get(key))
        if price is not None:
            return price
    outcomes = market.get("outcomes")
    if isinstance(outcomes, list) and outcomes:
        first = outcomes[0]
        if isinstance(first, dict):
            return safe_float(first.get("price"))
    return None


def get_no_price(market: dict[str, Any], yes_price: float | None) -> float | None:
    for key in ("noPrice", "no_price"):
        price = safe_float(market.get(key))
        if price is not None:
            return price
    if yes_price is None:
        return None
    return round(1.0 - yes_price, 4)


def get_markets(query: str, limit: int) -> list[dict[str, Any]]:
    client = get_client()
    if hasattr(client, "get_markets"):
        markets = client.get_markets(q=query, limit=limit, venue=VENUE)
        return list(markets or [])

    if hasattr(client, "get_briefing"):
        briefing = client.get_briefing(venue=VENUE, include_markets=True)
        markets = briefing.get("opportunityMarkets", [])
        query_lower = query.lower()
        filtered = [
            market
            for market in markets
            if query_lower in get_market_title(market).lower()
        ]
        return filtered[:limit]

    raise RuntimeError("Installed aion-sdk does not expose get_markets() or get_briefing()")


def get_market_context(market_id: str, my_probability: float) -> dict[str, Any]:
    client = get_client()
    try:
        return client.get_market_context(
            market_id,
            my_probability=my_probability,
            venue=VENUE,
        )
    except TypeError:
        return client.get_market_context(market_id, my_probability=my_probability)


def get_risk_alerts() -> list[str]:
    client = get_client()
    if not hasattr(client, "get_briefing"):
        return []
    try:
        briefing = client.get_briefing(venue=VENUE, include_markets=False)
    except TypeError:
        briefing = client.get_briefing()
    alerts = briefing.get("riskAlerts", [])
    return [str(alert) for alert in alerts]


def should_skip_context(context: dict[str, Any]) -> tuple[bool, str]:
    trading = context.get("trading", {}) if isinstance(context, dict) else {}
    warnings = context.get("warnings", []) if isinstance(context, dict) else []
    if trading.get("flip_flop_warning"):
        return True, "flip-flop warning"
    if warnings:
        warning_text = "; ".join(str(item) for item in warnings)
        return True, f"context warnings: {warning_text}"
    return False, ""


def build_reasoning(query: str, side: str, edge: float, thesis_probability: float, price: float) -> str:
    fair_value = thesis_probability if side == "yes" else 1.0 - thesis_probability
    return (
        f"Thesis '{query}' implies fair value {fair_value:.2%} on {side.upper()}; "
        f"market entry {price:.2%} offers edge {edge:.2%}"
    )


def print_summary(
    args: argparse.Namespace,
    alerts: list[str],
    decisions: list[str],
    order_updates: list[str],
) -> None:
    print(f"Skill: {SKILL_SLUG}")
    print(f"Venue: {VENUE}")
    print(f"Mode: {'live' if args.live else 'dry-run'}")
    print(f"Query: {args.query}")
    print(f"Thesis probability: {args.thesis_probability:.2%}")
    print("")
    print("Risk alerts:")
    if alerts:
        for alert in alerts:
            print(f"- {alert}")
    else:
        print("- none")
    print("")
    print("Decisions:")
    if decisions:
        for decision in decisions:
            print(f"- {decision}")
    else:
        print("- none")
    print("")
    print("Order updates:")
    if order_updates:
        for update in order_updates:
            print(f"- {update}")
    else:
        print("- none")


def run() -> int:
    args = parse_args()
    validate_args(args)

    alerts = get_risk_alerts()
    decisions: list[str] = []
    order_updates: list[str] = []

    markets = get_markets(args.query, args.limit)
    if not markets:
        decisions.append("No matching markets found")
        print_summary(args, alerts, decisions, order_updates)
        return 0

    for market in markets:
        market_id = get_market_id(market)
        title = get_market_title(market)
        yes_price = get_yes_price(market)
        no_price = get_no_price(market, yes_price)

        if not market_id or yes_price is None or no_price is None:
            decisions.append(f"{title}: SKIP (missing id or price data)")
            continue

        yes_edge = args.thesis_probability - yes_price
        no_edge = (1.0 - args.thesis_probability) - no_price

        if yes_edge >= args.min_edge:
            side = "yes"
            price = yes_price
            edge = yes_edge
        elif no_edge >= args.min_edge:
            side = "no"
            price = no_price
            edge = no_edge
        else:
            best_edge = max(yes_edge, no_edge)
            decisions.append(f"{title}: HOLD (edge {best_edge:.2%} below threshold)")
            continue

        if not args.min_price <= price <= args.max_price:
            decisions.append(
                f"{title}: HOLD ({side.upper()} price {price:.2%} outside entry band)"
            )
            continue

        context = get_market_context(market_id, my_probability=args.thesis_probability)
        skip, reason = should_skip_context(context)
        if skip:
            decisions.append(f"{title}: SKIP ({reason})")
            continue

        reasoning = build_reasoning(args.query, side, edge, args.thesis_probability, price)

        if args.live:
            result = get_client().trade(
                market_id=market_id,
                side=side,
                amount=args.trade_amount,
                source=TRADE_SOURCE,
                skill_slug=SKILL_SLUG,
                reasoning=reasoning,
            )
            order_id = result.get("order_id") or result.get("id") or "submitted"
            decisions.append(
                f"{title}: TRADE {side.upper()} size={args.trade_amount:.2f} edge={edge:.2%}"
            )
            order_updates.append(f"submitted {order_id} on {market_id}")
        else:
            decisions.append(
                f"{title}: DRY-RUN {side.upper()} size={args.trade_amount:.2f} edge={edge:.2%}"
            )

    if args.live and args.auto_redeem and hasattr(get_client(), "auto_redeem"):
        for result in get_client().auto_redeem():
            if result.get("success"):
                market_id = result.get("market_id", "unknown-market")
                tx_hash = result.get("tx_hash", "unknown-tx")
                order_updates.append(f"redeemed {market_id}: tx={tx_hash}")

    print_summary(args, alerts, decisions, order_updates)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(run())
    except KeyError as exc:
        print(f"Missing required environment variable: {exc.args[0]}", file=sys.stderr)
        raise SystemExit(2)
    except Exception as exc:
        print(f"Skill execution failed: {exc}", file=sys.stderr)
        raise SystemExit(1)