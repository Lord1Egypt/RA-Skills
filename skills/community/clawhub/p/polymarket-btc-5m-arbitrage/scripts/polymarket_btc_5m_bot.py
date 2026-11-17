#!/usr/bin/env python3
"""Read-only Polymarket BTC 5-minute market scanner.

This module intentionally has no order, wallet, payment, or secret-handling
code. It uses public GET endpoints and reports observations for human review.
"""

from __future__ import annotations

import argparse
import json
import logging
import time
from datetime import datetime, timezone
from http.client import IncompleteRead
from typing import Any, Dict, Iterable, List, Optional, Tuple
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

GAMMA_API = "https://gamma-api.polymarket.com"
CLOB_API = "https://clob.polymarket.com"
DEFAULT_MIN_LIQUIDITY = 1000.0
DEFAULT_MAX_MARKETS = 5
DEFAULT_FEE_BUFFER = 0.01
DEFAULT_TIMEOUT = 10.0
DEFAULT_INTERVAL = 30.0

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - polymarket_btc_5m_scanner - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class PublicApiError(RuntimeError):
    """Raised when a read-only public API request cannot be completed."""


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def parse_json_list(value: Any) -> List[Any]:
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
        except (TypeError, ValueError):
            return []
        return parsed if isinstance(parsed, list) else []
    return []


def first_level(levels: Iterable[Any]) -> Optional[Dict[str, float]]:
    for level in levels:
        if not isinstance(level, dict):
            continue
        price = safe_float(level.get("price"))
        size = safe_float(level.get("size"))
        if price > 0 and size > 0:
            return {"price": price, "size": size}
    return None


def market_is_btc_5m(market: Dict[str, Any]) -> bool:
    text = " ".join(
        str(market.get(field, "")).lower()
        for field in ("slug", "question", "seriesSlug")
    )
    has_btc = "btc" in text or "bitcoin" in text
    has_window = any(
        marker in text
        for marker in ("5m", "5-min", "5 min", "5-minute", "5 minute", "updown")
    )
    return has_btc and has_window


def find_up_down_tokens(
    token_ids: List[Any], outcomes: List[Any]
) -> Optional[Tuple[str, str]]:
    clean_ids = [str(token_id) for token_id in token_ids if token_id]
    if len(clean_ids) < 2:
        return None

    up_index: Optional[int] = None
    down_index: Optional[int] = None
    for index, outcome in enumerate(outcomes[: len(clean_ids)]):
        label = str(outcome).strip().lower()
        if up_index is None and (label == "up" or label == "yes" or "up" in label):
            up_index = index
        if down_index is None and (
            label == "down" or label == "no" or "down" in label
        ):
            down_index = index

    if up_index is not None and down_index is not None:
        return clean_ids[up_index], clean_ids[down_index]

    if not outcomes and len(clean_ids) == 2:
        logger.warning("Market has no outcome labels; using returned token order")
        return clean_ids[0], clean_ids[1]

    return None


class ReadOnlyPolymarketClient:
    """Client restricted to public market-data GET requests."""

    def __init__(self, timeout: float = DEFAULT_TIMEOUT) -> None:
        self.timeout = timeout

    def _get_json(self, base_url: str, params: Dict[str, str]) -> Any:
        url = f"{base_url}?{urlencode(params)}"
        last_error: Optional[BaseException] = None
        for attempt in range(2):
            request = Request(
                url,
                headers={
                    "Accept": "application/json",
                    "User-Agent": "polymarket-btc-5m-read-only-scanner/1.0.2",
                },
                method="GET",
            )
            try:
                with urlopen(request, timeout=self.timeout) as response:
                    return json.loads(response.read().decode("utf-8"))
            except (
                HTTPError,
                IncompleteRead,
                URLError,
                TimeoutError,
                ValueError,
            ) as exc:
                last_error = exc
                if attempt == 0:
                    time.sleep(0.25)
        raise PublicApiError(str(last_error)) from last_error

    def get_active_markets(self) -> List[Dict[str, Any]]:
        payload = self._get_json(
            f"{GAMMA_API}/markets",
            {"active": "true", "closed": "false", "limit": "100"},
        )
        return payload if isinstance(payload, list) else []

    def get_order_book(self, token_id: str) -> Dict[str, Any]:
        payload = self._get_json(f"{CLOB_API}/book", {"tokenId": token_id})
        return payload if isinstance(payload, dict) else {}


def analyze_market(
    client: ReadOnlyPolymarketClient,
    market: Dict[str, Any],
    fee_buffer: float,
) -> Optional[Dict[str, Any]]:
    token_ids = parse_json_list(market.get("clobTokenIds"))
    outcomes = parse_json_list(market.get("outcomes"))
    pair = find_up_down_tokens(token_ids, outcomes)
    if pair is None:
        logger.info("Skipping market without an identifiable Up/Down token pair")
        return None

    up_token, down_token = pair
    try:
        up_book = client.get_order_book(up_token)
        down_book = client.get_order_book(down_token)
    except PublicApiError as exc:
        logger.warning("Order-book request failed: %s", exc)
        return None

    up_ask = first_level(up_book.get("asks", []))
    down_ask = first_level(down_book.get("asks", []))
    up_bid = first_level(up_book.get("bids", []))
    down_bid = first_level(down_book.get("bids", []))
    if up_ask is None or down_ask is None:
        return {
            "slug": market.get("slug", ""),
            "question": market.get("question", ""),
            "liquidity": safe_float(market.get("liquidity")),
            "candidate": False,
            "reason": "missing_up_or_down_ask",
        }

    combined_ask = up_ask["price"] + down_ask["price"]
    candidate_edge = 1.0 - combined_ask - fee_buffer
    available_size = min(up_ask["size"], down_ask["size"])
    return {
        "slug": market.get("slug", ""),
        "question": market.get("question", ""),
        "liquidity": safe_float(market.get("liquidity")),
        "end_date": market.get("endDate"),
        "up": {
            "ask": up_ask,
            "bid": up_bid,
        },
        "down": {
            "ask": down_ask,
            "bid": down_bid,
        },
        "combined_ask": round(combined_ask, 6),
        "fee_buffer": fee_buffer,
        "candidate_edge": round(candidate_edge, 6),
        "available_size": round(available_size, 6),
        "candidate": candidate_edge > 0 and available_size > 0,
        "reason": "displayed_ask_sum_below_one_after_buffer"
        if candidate_edge > 0
        else "no_positive_displayed_edge",
    }


def scan_once(
    client: ReadOnlyPolymarketClient,
    min_liquidity: float,
    max_markets: int,
    fee_buffer: float,
) -> Dict[str, Any]:
    try:
        all_markets = client.get_active_markets()
    except PublicApiError as exc:
        logger.error("Market-data request failed: %s", exc)
        return {
            "scanned_at": datetime.now(timezone.utc).isoformat(),
            "markets_seen": 0,
            "markets_analyzed": 0,
            "candidates": [],
            "observations": [],
            "error": "market_data_request_failed",
        }

    markets = [
        market
        for market in all_markets
        if isinstance(market, dict)
        and market_is_btc_5m(market)
        and safe_float(market.get("liquidity")) >= min_liquidity
    ][:max_markets]

    observations: List[Dict[str, Any]] = []
    for market in markets:
        observation = analyze_market(client, market, fee_buffer)
        if observation is not None:
            observations.append(observation)

    return {
        "scanned_at": datetime.now(timezone.utc).isoformat(),
        "markets_seen": len(all_markets),
        "markets_analyzed": len(observations),
        "candidates": [item for item in observations if item.get("candidate")],
        "observations": observations,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Read-only BTC 5-minute Polymarket market scanner"
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run one scan and exit; this is the default when --interval is omitted",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=None,
        help="Repeat scans every N seconds; no orders are ever placed",
    )
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    parser.add_argument(
        "--min-liquidity", type=float, default=DEFAULT_MIN_LIQUIDITY
    )
    parser.add_argument("--max-markets", type=int, default=DEFAULT_MAX_MARKETS)
    parser.add_argument("--fee-buffer", type=float, default=DEFAULT_FEE_BUFFER)
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT)
    return parser


def print_result(result: Dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print(
        f"Scanned {result['markets_analyzed']} BTC 5m markets "
        f"(saw {result['markets_seen']} active markets)."
    )
    candidates = result.get("candidates", [])
    if not candidates:
        print("No candidate complementary-price edge found.")
        return
    for item in candidates:
        print(
            f"- {item.get('slug')}: edge={item.get('candidate_edge'):.4f}, "
            f"available_size={item.get('available_size')}"
        )
    print("Read-only observation only; no order was submitted.")


def main() -> int:
    args = build_parser().parse_args()
    if args.max_markets < 1 or args.fee_buffer < 0 or args.timeout <= 0:
        raise SystemExit("max-markets must be positive; fee-buffer must be non-negative")

    client = ReadOnlyPolymarketClient(timeout=args.timeout)
    interval = args.interval
    if interval is None or args.once:
        print_result(
            scan_once(
                client,
                min_liquidity=args.min_liquidity,
                max_markets=args.max_markets,
                fee_buffer=args.fee_buffer,
            ),
            args.json,
        )
        return 0

    if interval <= 0:
        raise SystemExit("interval must be positive")
    while True:
        print_result(
            scan_once(
                client,
                min_liquidity=args.min_liquidity,
                max_markets=args.max_markets,
                fee_buffer=args.fee_buffer,
            ),
            args.json,
        )
        time.sleep(interval)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        logger.info("Scanner stopped")
