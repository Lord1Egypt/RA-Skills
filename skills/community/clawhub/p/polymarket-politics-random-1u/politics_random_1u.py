#!/usr/bin/env python3

import argparse
import os
import random
from typing import Any, Dict, Iterable, List

try:
    from aion_sdk import AionClient  # type: ignore
except ImportError:
    from aion_sdk import AionMarketClient as AionClient  # type: ignore


SKILL_SLUG = "polymarket-politics-random-1u"
TRADE_SOURCE = "sdk:polymarket-politics-random-1u"
DEFAULT_QUERIES = ["politics", "election", "president", "senate", "congress", "vote"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Random 1 USD politics-market trade template for AION SDK.")
    parser.add_argument("--live", action="store_true", help="Enable live trading.")
    parser.add_argument("--side", choices=["yes", "no"], default="yes", help="Default trade side.")
    parser.add_argument("--query", help="Optional primary market search query.")
    parser.add_argument("--limit", type=int, default=20, help="Per-query market limit.")
    return parser.parse_args()


def env_flag(name: str) -> bool:
    value = os.getenv(name, "").strip().lower()
    return value in {"1", "true", "yes", "on"}


def get_api_key() -> str:
    api_key = os.getenv("AION_API_KEY") or os.getenv("AIONMARKET_API_KEY")
    if not api_key:
        raise RuntimeError("Missing AION_API_KEY or AIONMARKET_API_KEY")
    return api_key


def get_client() -> Any:
    api_key = get_api_key()
    base_url = os.getenv("AIONMARKET_BASE_URL")
    try:
        return AionClient(api_key=api_key, venue="polymarket")
    except TypeError:
        kwargs: Dict[str, Any] = {"api_key": api_key}
        if base_url:
            kwargs["base_url"] = base_url
        return AionClient(**kwargs)


def normalize_market_response(result: Any) -> List[Dict[str, Any]]:
    if isinstance(result, dict):
        items = result.get("items")
        if isinstance(items, list):
            return [item for item in items if isinstance(item, dict)]
        return []
    if isinstance(result, list):
        return [item for item in result if isinstance(item, dict)]
    return []


def politics_keywords() -> List[str]:
    primary = os.getenv("POLITICS_QUERY", "").strip()
    return [primary] + DEFAULT_QUERIES if primary else list(DEFAULT_QUERIES)


def market_text(market: Dict[str, Any]) -> str:
    parts = [
        str(market.get("title", "")),
        str(market.get("question", "")),
        str(market.get("category", "")),
    ]
    return " ".join(parts).lower()


def looks_political(market: Dict[str, Any]) -> bool:
    text = market_text(market)
    markers = ["politic", "election", "president", "senate", "congress", "vote", "government", "trump", "biden"]
    return any(marker in text for marker in markers)


def is_active(market: Dict[str, Any]) -> bool:
    if isinstance(market.get("active"), bool):
        return market["active"]
    status = str(market.get("status", "")).lower()
    return status in {"active", "open", "live", ""}


def unique_by_id(markets: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen = set()
    result = []
    for market in markets:
        market_id = str(market.get("id", ""))
        if not market_id or market_id in seen:
            continue
        seen.add(market_id)
        result.append(market)
    return result


def search_candidates(client: Any, limit: int, query_override: str = "") -> List[Dict[str, Any]]:
    queries = [query_override] if query_override else politics_keywords()
    candidates: List[Dict[str, Any]] = []
    for query in queries:
        if not query:
            continue
        markets = normalize_market_response(
            client.get_markets(q=query, limit=limit, venue="polymarket")
        )
        for market in markets:
            if is_active(market) and looks_political(market):
                candidates.append(market)
    return unique_by_id(candidates)


def get_context(client: Any, market_id: str, wallet: str = "") -> Dict[str, Any]:
    kwargs: Dict[str, Any] = {"market_id": market_id, "venue": "polymarket"}
    if wallet:
        kwargs["user"] = wallet
    result = client.get_market_context(**kwargs)
    return result if isinstance(result, dict) else {}


def choose_market(markets: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not markets:
        raise RuntimeError("No active politics markets found")
    return random.choice(markets)


def build_reasoning(market: Dict[str, Any], side: str, amount: float) -> str:
    title = market.get("title") or market.get("question") or market.get("id")
    return (
        f"Template random-entry strategy selected an active politics market at random and "
        f"is placing a {amount:.2f} USD {side.upper()} trade on {title}."
    )


def run_once(live: bool, side: str, query: str, limit: int) -> Dict[str, Any]:
    client = get_client()
    wallet = os.getenv("WALLET_ADDRESS", "").strip()
    amount = float(os.getenv("TRADE_AMOUNT_USD", "1"))
    candidates = search_candidates(client, limit=limit, query_override=query)
    market = choose_market(candidates)
    market_id = str(market.get("id", ""))
    context = get_context(client, market_id=market_id, wallet=wallet)
    warnings = context.get("warnings") or []
    trading = context.get("trading") or {}

    summary = {
        "skill": SKILL_SLUG,
        "mode": "live" if live else "dry-run",
        "selectedMarket": {
            "id": market_id,
            "title": market.get("title") or market.get("question"),
            "conditionId": market.get("conditionId"),
            "yesPrice": market.get("yesPrice"),
            "noPrice": market.get("noPrice"),
        },
        "warnings": warnings,
    }

    if warnings or trading.get("flip_flop_warning"):
        summary["status"] = "skipped"
        summary["reason"] = "market context reported warnings"
        return summary

    reasoning = build_reasoning(market, side=side, amount=amount)
    summary["proposedTrade"] = {
        "market_id": market_id,
        "side": side,
        "amount": amount,
        "source": TRADE_SOURCE,
        "skill_slug": SKILL_SLUG,
        "reasoning": reasoning,
    }

    if not live:
        summary["status"] = "dry-run"
        return summary

    result = client.trade(
        market_id=market_id,
        side=side,
        amount=amount,
        source=TRADE_SOURCE,
        skill_slug=SKILL_SLUG,
        reasoning=reasoning,
    )
    summary["status"] = "submitted"
    summary["tradeResult"] = result
    return summary


def main() -> None:
    args = parse_args()
    live = args.live or env_flag("RUN_LIVE")
    result = run_once(live=live, side=args.side, query=args.query or "", limit=args.limit)
    print(result)


if __name__ == "__main__":
    main()