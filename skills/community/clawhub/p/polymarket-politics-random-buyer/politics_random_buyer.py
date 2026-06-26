from __future__ import annotations

import argparse
import ast
import json
import os
import random
import sys
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from eth_account import Account

try:
    from aion_sdk import AionClient
except ImportError as exc:
    raise SystemExit(
        "aion-sdk is required. Install dependencies from clawhub.json before running this skill."
    ) from exc


SKILL_SLUG = "polymarket-politics-random-buyer"
TRADE_SOURCE = f"sdk:{SKILL_SLUG}"
VENUE = "polymarket"
ENV_PATH = Path(__file__).with_name(".env")
DEFAULT_QUERIES = ["election", "president", "senate", "house", "governor", "politics"]
POLITICS_KEYWORDS = {
    "election",
    "president",
    "presidential",
    "senate",
    "house",
    "congress",
    "governor",
    "mayor",
    "politic",
    "white house",
    "parliament",
    "prime minister",
    "campaign",
    "vote",
    "voter",
    "ballot",
    "gop",
    "democrat",
    "republican",
    "trump",
    "biden",
}


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


def parse_float(value: str, default: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def parse_int(value: str, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Random politics market buyer for AION / Polymarket")
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--amount", type=float, default=parse_float(env_first("TRADE_SIZE", default="1.0"), 1.0))
    parser.add_argument(
        "--side",
        default=env_first("TRADE_SIDE", default="yes").lower(),
        choices=["yes", "no"],
    )
    parser.add_argument(
        "--queries",
        default=env_first("SEARCH_QUERIES", default=",".join(DEFAULT_QUERIES)),
        help="Comma-separated search queries for politics markets.",
    )
    parser.add_argument(
        "--max-markets",
        type=int,
        default=parse_int(env_first("MAX_MARKETS", default="40"), 40),
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=parse_int(env_first("RANDOM_SEED", default=""), -1),
    )
    parser.add_argument(
        "--reasoning-prefix",
        default=env_first(
            "REASONING_PREFIX",
            default="Random politics market template selected a valid market after context checks",
        ),
    )
    parser.add_argument("--auto-redeem", action="store_true")
    return parser.parse_args()


def validate_args(args: argparse.Namespace) -> None:
    if args.amount <= 0:
        raise SystemExit("amount must be positive.")
    if args.max_markets <= 0:
        raise SystemExit("max-markets must be positive.")


def get_client() -> AionClient:
    api_key = require_env("AION_API_KEY", "AIONMARKET_API_KEY")
    return AionClient(api_key=api_key, venue=VENUE)


def derive_wallet_address() -> str:
    private_key = require_env("WALLET_PRIVATE_KEY")
    try:
        account = Account.from_key(private_key)
    except Exception as exc:
        raise SystemExit(f"Failed to parse WALLET_PRIVATE_KEY: {exc}") from exc
    return account.address


def normalize_results(raw: Any) -> list[dict[str, Any]]:
    if isinstance(raw, list):
        return [item for item in raw if isinstance(item, dict)]
    if isinstance(raw, dict):
        for key in ("data", "markets", "events", "results", "items"):
            value = raw.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
    return []


def fetch_events(client: AionClient, query: str, limit: int) -> list[dict[str, Any]]:
    kwargs = {"q": query, "limit": limit}
    try:
        return normalize_results(client.get_markets(venue=VENUE, **kwargs))
    except TypeError:
        return normalize_results(client.get_markets(**kwargs))


def parse_maybe_json_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if not value:
        return []
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            try:
                parsed = ast.literal_eval(value)
            except (SyntaxError, ValueError):
                return []
        return parsed if isinstance(parsed, list) else []
    return []


def is_politics_market(event: dict[str, Any], submarket: dict[str, Any]) -> bool:
    fields = [
        event.get("title"),
        event.get("question"),
        event.get("slug"),
        event.get("category"),
        submarket.get("question"),
        submarket.get("title"),
        submarket.get("subtitle"),
        submarket.get("description"),
        submarket.get("category"),
    ]
    haystack = " ".join(str(item).lower() for item in fields if item)
    return any(keyword in haystack for keyword in POLITICS_KEYWORDS)


def resolve_market_id(submarket: dict[str, Any]) -> str:
    for key in ("id", "marketId", "market_id", "conditionId"):
        value = submarket.get(key)
        if value:
            return str(value)
    return ""


def extract_yes_price(submarket: dict[str, Any]) -> float | None:
    for key in ("yesPrice", "bestAsk", "lastTradePrice"):
        value = submarket.get(key)
        if value not in (None, ""):
            try:
                price = float(value)
                return price / 100.0 if price > 1 else price
            except (TypeError, ValueError):
                pass

    prices = parse_maybe_json_list(submarket.get("outcomePrices"))
    if prices:
        try:
            price = float(prices[0])
            return price / 100.0 if price > 1 else price
        except (TypeError, ValueError):
            return None
    return None


def build_candidates(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    seen_ids: set[str] = set()

    for event in events:
        for submarket in event.get("markets", []) or []:
            if not isinstance(submarket, dict):
                continue
            if not is_politics_market(event, submarket):
                continue

            market_id = resolve_market_id(submarket)
            if not market_id or market_id in seen_ids:
                continue

            question = str(
                submarket.get("question")
                or submarket.get("title")
                or event.get("title")
                or market_id
            )
            yes_price = extract_yes_price(submarket)
            if yes_price is not None and (yes_price <= 0.01 or yes_price >= 0.99):
                continue

            candidates.append(
                {
                    "market_id": market_id,
                    "question": question,
                    "event_title": str(event.get("title") or ""),
                    "category": str(submarket.get("category") or event.get("category") or ""),
                    "yes_price": yes_price,
                }
            )
            seen_ids.add(market_id)

    return candidates


def nested_get(data: Any, paths: list[tuple[str, ...]]) -> Any:
    for path in paths:
        current = data
        found = True
        for key in path:
            if not isinstance(current, dict) or key not in current:
                found = False
                break
            current = current[key]
        if found and current not in (None, ""):
            return current
    return None


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
    elif flip_flop:
        alerts.append("flip_flop_warning")

    return alerts


def choose_market(
    client: AionClient,
    wallet_address: str,
    candidates: list[dict[str, Any]],
    seed: int,
) -> tuple[dict[str, Any] | None, dict[str, Any] | None, list[str]]:
    rng = random.Random(None if seed < 0 else seed)
    shuffled = list(candidates)
    rng.shuffle(shuffled)

    skipped: list[str] = []
    for candidate in shuffled:
        context = client.get_market_context(candidate["market_id"], venue=VENUE, user=wallet_address)
        alerts = extract_risk_alerts(context)
        if alerts:
            skipped.append(f"{candidate['market_id']}: {'; '.join(alerts)}")
            continue
        return candidate, context, skipped

    return None, None, skipped


def print_summary(
    wallet_address: str,
    total_candidates: int,
    chosen: dict[str, Any] | None,
    skipped: list[str],
    side: str,
    amount: float,
    live: bool,
    reasoning: str,
) -> None:
    print(f"Skill: {SKILL_SLUG}")
    print(f"Venue: {VENUE}")
    print(f"Wallet: {wallet_address}")
    print(f"Scanned markets: {total_candidates}")
    print()
    print("Decision:")
    if chosen is None:
        print("- HOLD no politics market passed context checks")
    else:
        mode = "live" if live else "dry-run"
        print(
            f"- TRADE {side.upper()} size={amount:.2f} market={chosen['question']} "
            f"market_id={chosen['market_id']} mode={mode}"
        )
    print()
    print("Risk alerts:")
    if skipped:
        for item in skipped[:10]:
            print(f"- {item}")
    else:
        print("- none")
    print()
    print(f"Reasoning: {reasoning}")


def main() -> int:
    load_env()
    args = parse_args()
    validate_args(args)

    wallet_address = derive_wallet_address()
    client = get_client()

    if args.auto_redeem:
        client.auto_redeem()

    queries = [item.strip() for item in args.queries.split(",") if item.strip()]
    if not queries:
        queries = list(DEFAULT_QUERIES)

    all_events: list[dict[str, Any]] = []
    for query in queries:
        all_events.extend(fetch_events(client, query, args.max_markets))

    candidates = build_candidates(all_events)
    if not candidates:
        raise SystemExit("No politics market candidates found from the configured queries.")

    chosen, _, skipped = choose_market(client, wallet_address, candidates, args.seed)
    reasoning = (
        f"{args.reasoning_prefix} -- candidates={len(candidates)}, side={args.side.upper()}, "
        f"amount={args.amount:.2f}, wallet={wallet_address}"
    )

    print_summary(wallet_address, len(candidates), chosen, skipped, args.side, args.amount, args.live, reasoning)

    if chosen is None:
        return 0

    if not args.live:
        print("\nDry-run only. Re-run with --live to execute the trade.")
        return 0

    result = client.trade(
        market_id=chosen["market_id"],
        side=args.side,
        amount=args.amount,
        source=TRADE_SOURCE,
        skill_slug=SKILL_SLUG,
        reasoning=reasoning,
    )
    print("\nTrade result:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("Interrupted", file=sys.stderr)
        raise SystemExit(130)