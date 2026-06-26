#!/usr/bin/env python3
"""
Fetch open orders for the authenticated user from the Polymarket CLOB API.

Requires py-clob-client and valid API credentials.

Usage (standalone test):
    python fetch_orders.py --api-key <key> --secret <secret> --passphrase <pass>
    python fetch_orders.py --config ../config.json
"""

import argparse
import json
import os
import sys

try:
    from py_clob_client.client import ClobClient
    HAS_CLOB_CLIENT = True
except ImportError:
    HAS_CLOB_CLIENT = False


CLOB_HOST = "https://clob.polymarket.com"
CHAIN_ID = 137  # Polygon mainnet


def get_clob_client(api_key: str, secret: str, passphrase: str,
                    funder: str = None) -> "ClobClient":
    if not HAS_CLOB_CLIENT:
        raise ImportError(
            "py-clob-client is required for order monitoring. "
            "Install with: pip install py-clob-client"
        )
    creds = {
        "apiKey": api_key,
        "secret": secret,
        "passphrase": passphrase,
    }
    client = ClobClient(
        host=CLOB_HOST,
        chain_id=CHAIN_ID,
        creds=creds,
        funder=funder,
    )
    return client


def fetch_open_orders(client: "ClobClient", market: str = None) -> list:
    """Fetch all open orders, optionally filtered by market (condition_id)."""
    all_orders = []
    next_cursor = None

    while True:
        kwargs = {}
        if market:
            kwargs["market"] = market
        if next_cursor:
            kwargs["next_cursor"] = next_cursor

        try:
            response = client.get_orders(**kwargs)
        except Exception as e:
            print(f"[WARN] Failed to fetch orders: {e}", file=sys.stderr)
            break

        orders = response if isinstance(response, list) else response.get("data", [])
        if not orders:
            break
        all_orders.extend(orders)

        if isinstance(response, dict) and response.get("next_cursor"):
            next_cursor = response["next_cursor"]
        else:
            break

    return all_orders


def normalize_order(order: dict) -> dict:
    """Extract key fields from a raw order record."""
    def pf(val, default=0.0):
        try:
            return float(val)
        except (ValueError, TypeError):
            return default

    return {
        "order_id": order.get("id", order.get("orderID", "")),
        "market": order.get("market", ""),
        "asset_id": order.get("asset_id", order.get("assetID", "")),
        "side": order.get("side", ""),
        "size": pf(order.get("original_size", order.get("size"))),
        "size_matched": pf(order.get("size_matched", order.get("sizeMatched"))),
        "price": pf(order.get("price")),
        "outcome": order.get("outcome", ""),
        "status": order.get("status", ""),
        "order_type": order.get("type", order.get("orderType", "")),
        "expiration": order.get("expiration", ""),
        "created_at": order.get("created_at", order.get("createdAt", "")),
    }


def fetch_all_open_orders(api_key: str, secret: str, passphrase: str,
                          markets: list[str] = None, funder: str = None) -> list:
    """Fetch and normalize all open orders."""
    client = get_clob_client(api_key, secret, passphrase, funder)

    if markets:
        all_orders = []
        for mkt in markets:
            raw = fetch_open_orders(client, market=mkt)
            all_orders.extend(raw)
    else:
        all_orders = fetch_open_orders(client)

    return [normalize_order(o) for o in all_orders]


def load_config(config_path: str) -> dict:
    with open(os.path.expanduser(config_path)) as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description="Fetch open orders from Polymarket CLOB API")
    parser.add_argument("--config", type=str, help="Path to config.json")
    parser.add_argument("--api-key", type=str, help="CLOB API key")
    parser.add_argument("--secret", type=str, help="CLOB API secret")
    parser.add_argument("--passphrase", type=str, help="CLOB API passphrase")
    parser.add_argument("--market", type=str, nargs="*", help="Filter by condition ID(s)")
    parser.add_argument("--output", type=str, default=None, help="Output file (default: stdout)")
    args = parser.parse_args()

    if args.config:
        cfg = load_config(args.config)
        auth = cfg.get("clob_auth", {})
        api_key = auth.get("api_key", "")
        secret = auth.get("secret", "")
        passphrase = auth.get("passphrase", "")
    else:
        api_key = args.api_key or os.environ.get("POLY_API_KEY", "")
        secret = args.secret or os.environ.get("POLY_SECRET", "")
        passphrase = args.passphrase or os.environ.get("POLY_PASSPHRASE", "")

    if not all([api_key, secret, passphrase]):
        print("[ERROR] API credentials required. Use --config or --api-key/--secret/--passphrase",
              file=sys.stderr)
        sys.exit(1)

    print("[INFO] Fetching open orders...", file=sys.stderr)
    orders = fetch_all_open_orders(api_key, secret, passphrase, markets=args.market)
    print(f"[INFO] Found {len(orders)} open orders", file=sys.stderr)

    json_str = json.dumps(orders, indent=2, ensure_ascii=False)
    if args.output:
        with open(args.output, "w") as f:
            f.write(json_str)
        print(f"[INFO] Output written to {args.output}", file=sys.stderr)
    else:
        print(json_str)


if __name__ == "__main__":
    main()
