import argparse
import ast
import os
import time
from dataclasses import asdict, dataclass, is_dataclass
from typing import Any

from dotenv import load_dotenv

from aion_sdk import AionMarketClient, ApiError
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import ApiCreds, CreateOrderOptions, OrderArgs

SKILL_SLUG = "polymarket-5m-trading"
TRADE_SOURCE = f"sdk:{SKILL_SLUG}"
POLYMARKET_HOST = "https://clob.polymarket.com"
POLYGON_CHAIN_ID = 137


@dataclass
class CycleLog:
    step: str
    status: str
    detail: str
    result: dict[str, Any] | None = None


def env(name: str, default: str | None = None) -> str | None:
    return os.getenv(name, default)


def require_env(name: str) -> str:
    value = env(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def get_api_key() -> str:
    if env("AION_API_KEY"):
        return require_env("AION_API_KEY")
    return require_env("AIONMARKET_API_KEY")


def get_client() -> AionMarketClient:
    base_url = env("AIONMARKET_BASE_URL")
    if base_url:
        return AionMarketClient(api_key=get_api_key(), base_url=base_url)
    return AionMarketClient(api_key=get_api_key())


def to_float(value: Any, default: float | None = None) -> float | None:
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def parse_jsonish(value: Any, default: Any) -> Any:
    if value is None:
        return default
    if isinstance(value, (list, dict)):
        return value
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return default
        try:
            return ast.literal_eval(text)
        except Exception:
            return default
    return default


def maybe_dict(value: Any) -> dict[str, Any]:
    if hasattr(value, "model_dump"):
        return value.model_dump()
    if hasattr(value, "dict"):
        return value.dict()
    if is_dataclass(value):
        return asdict(value)
    if isinstance(value, dict):
        return value
    raise TypeError(f"Unsupported object type: {type(value)!r}")


def unwrap_collection(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if isinstance(payload, dict):
        if payload.get("success") is False:
            raise RuntimeError(str(payload.get("error") or payload))
        for key in ("data", "items", "events", "markets", "results"):
            value = payload.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
    raise RuntimeError(f"Unexpected collection payload: {payload}")


def build_clob_client(private_key: str, creds: ApiCreds | None = None) -> ClobClient:
    return ClobClient(
        POLYMARKET_HOST,
        chain_id=POLYGON_CHAIN_ID,
        key=private_key,
        creds=creds,
    )


def derive_wallet_bundle(private_key: str) -> tuple[str, ApiCreds]:
    clob = build_clob_client(private_key)
    creds = clob.create_or_derive_api_creds()
    wallet = clob.get_address()
    return wallet, creds


def resolve_wallet_address(live: bool) -> str | None:
    private_key = env("WALLET_PRIVATE_KEY")
    if not private_key:
        if live:
            raise RuntimeError("WALLET_PRIVATE_KEY is required for --live")
        return None
    wallet, _ = derive_wallet_bundle(private_key)
    return wallet


def ensure_wallet_credentials(client: AionMarketClient, private_key: str) -> tuple[str, ApiCreds]:
    wallet, creds = derive_wallet_bundle(private_key)
    status = client.check_wallet_credentials(wallet)
    if isinstance(status, dict) and status.get("success") is False:
        raise RuntimeError(str(status.get("error") or status))
    if not status.get("hasCredentials"):
        client.register_wallet_credentials(
            wallet_address=wallet,
            api_key=creds.api_key,
            api_secret=creds.api_secret,
            api_passphrase=creds.api_passphrase,
        )
    return wallet, creds


def extract_market_id(market: dict[str, Any]) -> str:
    return str(market.get("conditionId") or market.get("marketConditionId") or market.get("id") or "")


def extract_question(market: dict[str, Any]) -> str:
    return str(market.get("question") or market.get("title") or market.get("eventTitle") or extract_market_id(market))


def extract_yes_price(market: dict[str, Any]) -> float | None:
    for key in ("yesPrice", "bestAsk", "lastPrice"):
        value = to_float(market.get(key))
        if value is not None:
            return value
    prices = parse_jsonish(market.get("outcomePrices"), [])
    if isinstance(prices, list) and prices:
        return to_float(prices[0])
    return None


def extract_token_ids(market: dict[str, Any]) -> list[str]:
    token_ids = parse_jsonish(market.get("clobTokenIds"), [])
    if isinstance(token_ids, list):
        return [str(token_id) for token_id in token_ids]
    return []


def extract_tick_size(market: dict[str, Any]) -> str:
    return str(market.get("orderPriceMinTickSize") or "0.01")


def extract_min_size(market: dict[str, Any]) -> float:
    return to_float(market.get("orderMinSize"), 1.0) or 1.0


def extract_volume(market: dict[str, Any]) -> float:
    keys = [
        "volume",
        "volume24hr",
        "volume24Hr",
        "volume24h",
        "oneDayVolume",
        "totalVolume",
        "liquidity",
        "liquidityNum",
        "volumeNum",
        "eventVolume",
        "eventLiquidity",
    ]
    for key in keys:
        value = to_float(market.get(key))
        if value is not None:
            return value
    return 0.0


def flatten_market_search(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    flattened: list[dict[str, Any]] = []
    for item in items:
        sub_markets = item.get("markets")
        if isinstance(sub_markets, list) and sub_markets:
            for sub_market in sub_markets:
                if not isinstance(sub_market, dict):
                    continue
                merged = dict(sub_market)
                merged.setdefault("eventTitle", item.get("title"))
                merged.setdefault("eventQuestion", item.get("question"))
                merged.setdefault("eventVolume", item.get("volume"))
                merged.setdefault("eventLiquidity", item.get("liquidity"))
                flattened.append(merged)
        else:
            flattened.append(item)
    return flattened


def is_btc_market(market: dict[str, Any]) -> bool:
    text = " ".join(
        [
            str(market.get("question") or ""),
            str(market.get("title") or ""),
            str(market.get("eventTitle") or ""),
            str(market.get("eventQuestion") or ""),
        ]
    ).lower()
    return "btc" in text or "bitcoin" in text


def search_btc_market(client: AionMarketClient, buy_usd: float, search_limit: int) -> dict[str, Any]:
    search_payload = client.get_markets(
        q="BTC",
        limit=search_limit,
        page=1,
        venue="polymarket",
        events_status="active",
    )
    candidates = flatten_market_search(unwrap_collection(search_payload))

    filtered: list[dict[str, Any]] = []
    for market in candidates:
        if not is_btc_market(market):
            continue
        market_id = extract_market_id(market)
        yes_price = extract_yes_price(market)
        if not market_id or yes_price is None:
            continue
        if yes_price < 0.40 or yes_price > 0.60:
            continue
        if yes_price <= 0:
            continue
        min_size = extract_min_size(market)
        target_shares = round(buy_usd / yes_price, 4)
        if min_size > target_shares:
            continue
        filtered.append(market)

    if not filtered:
        raise RuntimeError("No BTC market matched the 40%-60% band and the 1 USD size constraint")

    filtered.sort(key=lambda market: (extract_volume(market), extract_yes_price(market) or 0.0), reverse=True)
    return filtered[0]


def refresh_market_snapshot(client: AionMarketClient, selected_market: dict[str, Any], search_limit: int) -> dict[str, Any]:
    selected_id = extract_market_id(selected_market)
    search_payload = client.get_markets(
        q="BTC",
        limit=search_limit,
        page=1,
        venue="polymarket",
        events_status="active",
    )
    candidates = flatten_market_search(unwrap_collection(search_payload))
    for candidate in candidates:
        if extract_market_id(candidate) == selected_id:
            return candidate
    return selected_market


def get_market_style_price(yes_price: float, side: str, buffer_size: float) -> float:
    if side == "BUY":
        return min(0.99, round(yes_price + buffer_size, 4))
    return max(0.01, round(yes_price - buffer_size, 4))


def build_signed_order(
    private_key: str,
    creds: ApiCreds,
    market: dict[str, Any],
    price: float,
    size: float,
    side: str,
) -> dict[str, Any]:
    token_ids = extract_token_ids(market)
    if not token_ids:
        raise RuntimeError("Selected market is missing clobTokenIds")

    clob = build_clob_client(private_key, creds=creds)
    signed_order = clob.create_order(
        OrderArgs(
            token_id=token_ids[0],
            price=price,
            size=size,
            side=side,
        ),
        options=CreateOrderOptions(
            tick_size=extract_tick_size(market),
            neg_risk=bool(market.get("negRisk", False)),
        ),
    )
    return maybe_dict(signed_order)


def log_summary(logs: list[CycleLog]) -> str:
    lines = [
        f"Skill: {SKILL_SLUG}",
        "Venue: polymarket",
        "",
        "Execution log:",
    ]
    for log in logs:
        lines.append(f"- {log.step}: {log.status} - {log.detail}")
    return "\n".join(lines)


def maybe_wait(seconds: int, live: bool, logs: list[CycleLog], label: str) -> None:
    if seconds <= 0:
        return
    if live:
        logs.append(CycleLog(step=label, status="WAIT", detail=f"sleeping {seconds}s"))
        time.sleep(seconds)
        return
    logs.append(CycleLog(step=label, status="DRY-RUN", detail=f"would sleep {seconds}s"))


def validate_buy_context(client: AionMarketClient, market: dict[str, Any], wallet: str | None) -> None:
    context = client.get_market_context(
        market_id=extract_market_id(market),
        venue="polymarket",
        user=wallet,
    )
    warnings = context.get("warnings") or []
    if warnings:
        raise RuntimeError(f"Selected market has warnings: {warnings}")


def execute_trade(
    client: AionMarketClient,
    market: dict[str, Any],
    private_key: str,
    creds: ApiCreds,
    wallet: str,
    side: str,
    order_size: float,
    price: float,
    reasoning: str,
) -> dict[str, Any]:
    order = build_signed_order(
        private_key=private_key,
        creds=creds,
        market=market,
        price=price,
        size=order_size,
        side=side,
    )
    payload = {
        "venue": "polymarket",
        "marketConditionId": extract_market_id(market),
        "marketQuestion": extract_question(market),
        "outcome": "YES",
        "orderSize": order_size,
        "price": price,
        "isLimitOrder": False,
        "walletAddress": wallet,
        "order": order,
        "reasoning": reasoning,
        "source": TRADE_SOURCE,
        "skillSlug": SKILL_SLUG,
    }
    return client.trade(payload)


def run_strategy(live: bool, hold_seconds: int, max_buys: int, buy_usd: float, search_limit: int) -> int:
    client = get_client()
    wallet = resolve_wallet_address(live=live)
    logs: list[CycleLog] = []

    target_market = search_btc_market(client, buy_usd=buy_usd, search_limit=search_limit)
    target_id = extract_market_id(target_market)
    target_question = extract_question(target_market)
    target_price = extract_yes_price(target_market)
    target_volume = extract_volume(target_market)
    logs.append(
        CycleLog(
            step="select-market",
            status="OK",
            detail=(
                f"selected {target_id} question={target_question} yes={target_price:.4f} volume={target_volume:.2f}"
                if target_price is not None
                else f"selected {target_id} question={target_question}"
            ),
        )
    )

    private_key = env("WALLET_PRIVATE_KEY")
    creds: ApiCreds | None = None
    if live:
        private_key = require_env("WALLET_PRIVATE_KEY")
        wallet, creds = ensure_wallet_credentials(client, private_key)

    price_buffer = to_float(env("MARKET_PRICE_BUFFER"), 0.03) or 0.03

    for buy_index in range(1, max_buys + 1):
        current_market = refresh_market_snapshot(client, target_market, search_limit=search_limit)
        current_yes_price = extract_yes_price(current_market)
        if current_yes_price is None:
            raise RuntimeError("Selected market no longer exposes a YES price")

        validate_buy_context(client, current_market, wallet)
        target_shares = round(buy_usd / current_yes_price, 4)
        min_size = extract_min_size(current_market)
        if target_shares < min_size:
            raise RuntimeError(
                f"Cycle {buy_index}: market minimum size {min_size} is larger than the requested 1 USD notional size {target_shares}"
            )

        buy_price = get_market_style_price(current_yes_price, side="BUY", buffer_size=price_buffer)
        buy_reason = f"BTC 5m cycle buy #{buy_index}: market-style 1 USD entry"

        if live:
            buy_result = execute_trade(
                client=client,
                market=current_market,
                private_key=private_key,
                creds=creds,
                wallet=wallet,
                side="BUY",
                order_size=target_shares,
                price=buy_price,
                reasoning=buy_reason,
            )
            logs.append(
                CycleLog(
                    step=f"buy-{buy_index}",
                    status="TRADE",
                    detail=f"bought YES size={target_shares} cap={buy_price:.4f}",
                    result=buy_result,
                )
            )
        else:
            logs.append(
                CycleLog(
                    step=f"buy-{buy_index}",
                    status="DRY-RUN",
                    detail=f"would buy YES size={target_shares} cap={buy_price:.4f}",
                )
            )

        maybe_wait(hold_seconds, live=live, logs=logs, label=f"hold-after-buy-{buy_index}")

        current_market = refresh_market_snapshot(client, target_market, search_limit=search_limit)
        current_yes_price = extract_yes_price(current_market)
        if current_yes_price is None:
            raise RuntimeError("Selected market no longer exposes a YES price before sell")

        sell_price = get_market_style_price(current_yes_price, side="SELL", buffer_size=price_buffer)
        sell_reason = f"BTC 5m cycle sell #{buy_index}: exit after hold window"

        if live:
            sell_result = execute_trade(
                client=client,
                market=current_market,
                private_key=private_key,
                creds=creds,
                wallet=wallet,
                side="SELL",
                order_size=target_shares,
                price=sell_price,
                reasoning=sell_reason,
            )
            logs.append(
                CycleLog(
                    step=f"sell-{buy_index}",
                    status="TRADE",
                    detail=f"sold YES size={target_shares} floor={sell_price:.4f}",
                    result=sell_result,
                )
            )
        else:
            logs.append(
                CycleLog(
                    step=f"sell-{buy_index}",
                    status="DRY-RUN",
                    detail=f"would sell YES size={target_shares} floor={sell_price:.4f}",
                )
            )

        if buy_index < max_buys:
            maybe_wait(hold_seconds, live=live, logs=logs, label=f"pause-before-next-buy-{buy_index}")

    logs.append(CycleLog(step="complete", status="DONE", detail=f"finished after {max_buys} buy cycles"))
    print(log_summary(logs))
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Polymarket 5m BTC trading skill.")
    parser.add_argument("--live", action="store_true", help="Execute real trades instead of dry-run planning.")
    parser.add_argument("--hold-seconds", type=int, default=int(env("HOLD_SECONDS", "300")), help="Hold and pause duration between trade legs.")
    parser.add_argument("--max-buys", type=int, default=int(env("MAX_BUYS", "10")), help="Total number of buy cycles before the strategy stops.")
    parser.add_argument("--buy-usd", type=float, default=to_float(env("BUY_USD"), 1.0) or 1.0, help="USD notional target for each buy cycle.")
    parser.add_argument("--search-limit", type=int, default=int(env("SEARCH_LIMIT", "50")), help="Maximum BTC search results to inspect.")
    return parser.parse_args()


def main() -> int:
    load_dotenv(".env")
    args = parse_args()

    try:
        return run_strategy(
            live=args.live,
            hold_seconds=args.hold_seconds,
            max_buys=args.max_buys,
            buy_usd=args.buy_usd,
            search_limit=args.search_limit,
        )
    except ApiError as error:
        print(f"API Error {error.code}: {error.message}")
        return 1
    except RuntimeError as error:
        print(str(error))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())