from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

try:
    from simmer_sdk import SimmerClient
except ImportError as exc:
    raise SystemExit(
        "simmer-sdk is required. Install dependencies from clawhub.json before running this skill."
    ) from exc


SKILL_SLUG = "polymarket-divergence-trader"
TRADE_SOURCE = f"sdk:{SKILL_SLUG}"
ENV_PATH = Path(__file__).with_name(".env")
DRY_RUN_VENUE = "sim"
DEFAULT_LIVE_VENUE = "polymarket"


def load_env() -> None:
    load_dotenv(ENV_PATH)


def env_first(*names: str, default: str = "") -> str:
    for name in names:
        value = os.environ.get(name, "").strip()
        if value:
            return value
    return default


def require_env(*names: str) -> str:
    value = env_first(*names)
    if value:
        return value
    raise SystemExit(f"Missing required environment variable. Tried: {', '.join(names)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simmer divergence-based trading skill")
    parser.add_argument("--market-id", default=env_first("MARKET_ID"), required=False)
    parser.add_argument(
        "--my-probability",
        type=float,
        default=float(env_first("MY_PROBABILITY", default="nan")),
        required=False,
    )
    parser.add_argument("--amount", type=float, default=float(env_first("TRADE_SIZE", default="5.0")))
    parser.add_argument("--min-edge", type=float, default=float(env_first("MIN_EDGE", default="0.05")))
    parser.add_argument(
        "--reasoning-prefix",
        default=env_first("REASONING_PREFIX", default="Probability divergence signal"),
    )
    parser.add_argument(
        "--live-venue",
        default=env_first("LIVE_VENUE", default=DEFAULT_LIVE_VENUE),
        choices=["polymarket", "kalshi", "sim"],
    )
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--auto-redeem", action="store_true")
    return parser.parse_args()


def is_nan(value: float) -> bool:
    return value != value


def validate_args(args: argparse.Namespace) -> None:
    if not args.market_id:
        raise SystemExit("Missing market id. Pass --market-id or set MARKET_ID.")
    if is_nan(args.my_probability):
        raise SystemExit("Missing probability estimate. Pass --my-probability or set MY_PROBABILITY.")
    if not 0.0 <= args.my_probability <= 1.0:
        raise SystemExit("my_probability must be between 0 and 1.")
    if args.amount <= 0:
        raise SystemExit("amount must be positive.")
    if args.min_edge <= 0:
        raise SystemExit("min_edge must be positive.")


def get_client(venue: str) -> SimmerClient:
    api_key = require_env("SIMMER_API_KEY")
    return SimmerClient(api_key=api_key, venue=venue)


def nested_get(data: Any, paths: list[tuple[str, ...]]) -> Any:
    for path in paths:
        current = data
        found = True
        for key in path:
            if not isinstance(current, dict) or key not in current:
                found = False
                break
            current = current[key]
        if found and current is not None:
            return current
    return None


def extract_market_probability(context: dict[str, Any]) -> float:
    candidate = nested_get(
        context,
        [
            ("edge_analysis", "market_probability"),
            ("edgeAnalysis", "marketProbability"),
            ("market", "probability"),
            ("market_probability",),
            ("marketProbability",),
            ("yes_price",),
            ("yesPrice",),
            ("price",),
        ],
    )
    if candidate is None:
        raise SystemExit("Could not extract market probability from market context.")
    probability = float(candidate)
    if probability > 1:
        probability = probability / 100.0
    return probability


def extract_risk_alerts(context: dict[str, Any]) -> list[str]:
    alerts: list[str] = []

    warnings = nested_get(context, [("warnings",), ("trading", "warnings")])
    if isinstance(warnings, list):
        alerts.extend(str(item) for item in warnings if item)
    elif isinstance(warnings, str) and warnings:
        alerts.append(warnings)

    flip_flop = nested_get(context, [("trading", "flip_flop_warning"), ("flip_flop_warning",)])
    if isinstance(flip_flop, str) and flip_flop:
        alerts.append(flip_flop)

    slippage_pct = nested_get(context, [("slippage", "slippage_pct"), ("slippage", "slippagePct")])
    if slippage_pct is not None and float(slippage_pct) > 0.15:
        alerts.append(f"slippage_too_high:{float(slippage_pct):.3f}")

    return alerts


def decide_outcome(my_probability: float, market_probability: float, min_edge: float) -> tuple[str, float]:
    edge = my_probability - market_probability
    if edge >= min_edge:
        return "YES", edge
    if edge <= -min_edge:
        return "NO", edge
    return "HOLD", edge


def build_reasoning(prefix: str, my_probability: float, market_probability: float, edge: float) -> str:
    return (
        f"{prefix} -- model={my_probability:.3f}, market={market_probability:.3f}, "
        f"edge={edge:+.3f}"
    )


def print_summary(
    venue: str,
    market_id: str,
    alerts: list[str],
    outcome: str,
    amount: float,
    edge: float,
    live: bool,
    reasoning: str,
) -> None:
    print(f"Skill: {SKILL_SLUG}")
    print(f"Venue: {venue}")
    print("Risk alerts:")
    if alerts:
        for alert in alerts:
            print(f"- {alert}")
    else:
        print("- none")
    print()
    print("Decision:")
    action = "TRADE" if outcome != "HOLD" else "HOLD"
    live_label = "live" if live and outcome != "HOLD" else "dry-run"
    print(
        f"- {market_id}: {action} {outcome} size={amount:.2f} "
        f"mode={live_label} edge={edge:+.2%} reason={reasoning}"
    )


def main() -> int:
    load_env()
    args = parse_args()
    validate_args(args)

    venue = args.live_venue if args.live else DRY_RUN_VENUE
    client = get_client(venue)
    context = client.get_market_context(args.market_id, my_probability=args.my_probability)
    market_probability = extract_market_probability(context)
    alerts = extract_risk_alerts(context)
    outcome, edge = decide_outcome(args.my_probability, market_probability, args.min_edge)
    reasoning = build_reasoning(args.reasoning_prefix, args.my_probability, market_probability, edge)

    if alerts:
        outcome = "HOLD"

    print_summary(venue, args.market_id, alerts, outcome, args.amount, edge, args.live, reasoning)

    if outcome == "HOLD":
        return 0

    if not args.live:
        print("\nDry-run only. Re-run with --live to execute the trade.")
        return 0

    result = client.trade(
        market_id=args.market_id,
        side="BUY",
        outcome=outcome,
        amount=args.amount,
        source=TRADE_SOURCE,
        skill_slug=SKILL_SLUG,
        reasoning=reasoning,
    )
    print("\nTrade result:")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    if args.auto_redeem:
        redemption = client.auto_redeem()
        print("\nAuto redeem:")
        print(json.dumps(redemption, indent=2, ensure_ascii=False))

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("Interrupted", file=sys.stderr)
        raise SystemExit(130)