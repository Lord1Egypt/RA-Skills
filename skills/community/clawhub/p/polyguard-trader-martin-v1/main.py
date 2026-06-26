"""
PolyGuard Martin Pro - Free, open-source Polymarket automation skill.
No data collection; no hidden backdoors.
"""

import logging
import time
import hmac
import hashlib
import json
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests
import yaml

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

CONFIG_PATH = "config.yaml"
POLYMARKET_BASE_URL = "https://api.polymarket.com"


@dataclass
class SkillConfig:
    """User configuration for Polymarket trading. Flat keys only."""

    api_key: str
    market_id: str
    side: str
    size: float
    max_price: float
    poll_interval_seconds: float


def load_config(path: str = CONFIG_PATH) -> SkillConfig:
    """Load and validate config from YAML. Reads only top-level keys."""
    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}

    api_key = str(raw.get("api_key") or "").strip()
    if not api_key or api_key == "YOUR_API_KEY_HERE":
        raise ValueError("config.yaml: api_key must be set to your Polymarket API key.")

    market_id = str(raw.get("market_id") or "").strip()
    if not market_id or market_id == "YOUR_MARKET_ID_HERE":
        raise ValueError("config.yaml: market_id must be set to your target market ID.")

    return SkillConfig(
        api_key=api_key,
        market_id=market_id,
        side=str(raw.get("side") or "buy").lower(),
        size=float(raw.get("size", 0)),
        max_price=float(raw.get("max_price", 0)),
        poll_interval_seconds=float(raw.get("poll_interval_seconds", 5)),
    )


def get_polymarket_price(cfg: SkillConfig) -> Optional[float]:
    """
    Fetch the current best quote for the configured market.
    Returns None on API failure or empty book; caller should retry later.
    """
    url = f"{POLYMARKET_BASE_URL}/v1/trading/markets/{cfg.market_id}/orderbook"
    headers = {
        "Authorization": f"Bearer {cfg.api_key}",
        "Content-Type": "application/json",
    }
    try:
        resp = requests.get(url, headers=headers, timeout=15)
    except requests.RequestException as e:
        logger.warning("Orderbook request failed: %s", e)
        return None

    if resp.status_code != 200:
        logger.warning(
            "Orderbook returned %s: %s",
            resp.status_code,
            resp.text[:200] if resp.text else "",
        )
        return None

    try:
        ob = resp.json()
    except ValueError:
        logger.warning("Invalid JSON from orderbook endpoint.")
        return None

    bids = ob.get("bids", [])
    asks = ob.get("asks", [])

    if cfg.side == "buy":
        if not asks:
            return None
        try:
            return float(asks[0]["price"])
        except (KeyError, TypeError, ValueError):
            return None
    else:
        if not bids:
            return None
        try:
            return float(bids[0]["price"])
        except (KeyError, TypeError, ValueError):
            return None


def sign_polymarket_order(api_secret: str, body: Dict[str, Any]) -> str:
    """Sign the order body with HMAC-SHA256 per Polymarket API requirements."""
    payload = json.dumps(body, separators=(",", ":"), sort_keys=True)
    return hmac.new(
        api_secret.encode("utf-8"),
        payload.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def place_polymarket_order(cfg: SkillConfig, price: float) -> Dict[str, Any]:
    """
    Place a single order on Polymarket. Raises on API error or insufficient balance.
    """
    order_body = {
        "marketId": cfg.market_id,
        "side": cfg.side.upper(),
        "price": price,
        "size": cfg.size,
        "timeInForce": "GTC",
    }

    signature = sign_polymarket_order(cfg.api_key, order_body)
    headers = {
        "Authorization": f"Bearer {cfg.api_key}",
        "X-Signature": signature,
        "Content-Type": "application/json",
    }

    url = f"{POLYMARKET_BASE_URL}/v1/trading/orders"
    try:
        resp = requests.post(url, headers=headers, json=order_body, timeout=15)
    except requests.RequestException as e:
        raise RuntimeError(f"Order request failed: {e}") from e

    if resp.status_code == 402:
        raise RuntimeError(
            "Insufficient balance. Fund your Polymarket account and try again."
        )
    if resp.status_code == 401:
        raise RuntimeError("Invalid or expired API key. Check api_key in config.yaml.")
    if resp.status_code != 200:
        try:
            err_body = resp.json()
            msg = err_body.get("message", err_body.get("error", resp.text))
        except ValueError:
            msg = resp.text[:200] if resp.text else "Unknown error"
        raise RuntimeError(f"Polymarket order failed ({resp.status_code}): {msg}")

    return resp.json()


def should_place_order(cfg: SkillConfig, price: float) -> bool:
    """True if current price meets the configured threshold for the chosen side."""
    if cfg.side == "buy":
        return price <= cfg.max_price
    return price >= cfg.max_price


def main() -> None:
    """Run the monitoring loop: poll price, place order when condition is met."""
    try:
        cfg = load_config()
    except (FileNotFoundError, ValueError) as e:
        logger.error("Configuration error: %s", e)
        raise SystemExit(1) from e

    logger.info("Config loaded. Monitoring Polymarket (market_id=%s).", cfg.market_id)

    while True:
        try:
            price = get_polymarket_price(cfg)
            if price is None:
                logger.info("No price available; retrying later.")
            else:
                logger.info("Current price: %s", price)
                if should_place_order(cfg, price):
                    logger.info("Price condition met; placing order.")
                    try:
                        result = place_polymarket_order(cfg, price)
                        logger.info("Order placed: %s", json.dumps(result))
                    except RuntimeError as e:
                        logger.error("Order failed: %s", e)
                else:
                    logger.debug("Condition not met; no order placed.")
        except requests.RequestException as e:
            logger.warning("Network error: %s", e)
        except Exception as e:
            logger.exception("Unexpected error: %s", e)

        time.sleep(cfg.poll_interval_seconds)


if __name__ == "__main__":
    main()
