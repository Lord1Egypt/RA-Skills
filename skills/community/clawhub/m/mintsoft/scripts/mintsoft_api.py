#!/usr/bin/env python3
"""Mintsoft API CLI — lightweight wrapper for agent tool use.

Authentication
--------------

Two supported modes (in priority order):

1. **Env var ``MINTSOFT_API_KEY``** — pre-issued Mintsoft API key passed as
   ``ms-apikey`` on every request. Most reliable for headless agents.

2. **Cached token from ``mintsoft_api.py auth``** — runs the Mintsoft
   ``/Auth`` flow with username/password and caches the returned key to
   ``~/.config/mintsoft-skill/token.json`` (mode 0600) with a 24-hour TTL.
   Subsequent commands reuse the cached key transparently. Credentials
   come from ``--username``/``--password`` flags or
   ``MINTSOFT_USERNAME``/``MINTSOFT_PASSWORD`` env vars.

Output
------

JSON to stdout. Use ``--summary`` on any list command for a compact,
context-friendly projection.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

import httpx

API_BASE = "https://api.mintsoft.co.uk/api"
TIMEOUT = 30
MAX_RETRIES = 3
PAGE_SIZE = 100
TOKEN_TTL_SECONDS = 24 * 60 * 60  # Mintsoft API keys are valid 24h

CONFIG_DIR = Path(
    os.environ.get("MINTSOFT_CONFIG_DIR")
    or (Path.home() / ".config" / "mintsoft-skill")
)
TOKEN_PATH = CONFIG_DIR / "token.json"

# Global deadline for long-running pagination (seconds). 0 = no limit.
_DEADLINE: float = 0
_START_TIME: float = 0


def _set_deadline(seconds: int) -> None:
    global _DEADLINE, _START_TIME
    _START_TIME = time.time()
    _DEADLINE = seconds


def _time_remaining() -> float:
    if not _DEADLINE:
        return float("inf")
    return _DEADLINE - (time.time() - _START_TIME)


def _deadline_exceeded() -> bool:
    return _DEADLINE > 0 and _time_remaining() <= 5  # 5s buffer for output


def _load_cached_token() -> str | None:
    """Return a cached API key if it exists and hasn't expired, else None."""
    try:
        if not TOKEN_PATH.exists():
            return None
        with TOKEN_PATH.open() as fh:
            data = json.load(fh)
        key = data.get("api_key")
        issued_at = data.get("issued_at", 0)
        if not key:
            return None
        if time.time() - issued_at > TOKEN_TTL_SECONDS:
            return None
        return key
    except (OSError, json.JSONDecodeError):
        return None


def _save_cached_token(api_key: str) -> None:
    """Persist the API key to disk with restrictive permissions."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    payload = {"api_key": api_key, "issued_at": int(time.time())}
    TOKEN_PATH.write_text(json.dumps(payload))
    try:
        os.chmod(TOKEN_PATH, 0o600)
    except OSError:
        # Best-effort on filesystems that don't support chmod.
        pass


def _resolve_api_key() -> str:
    """Find a usable Mintsoft API key — env first, then disk cache."""
    key = os.environ.get("MINTSOFT_API_KEY")
    if key:
        return key
    cached = _load_cached_token()
    if cached:
        return cached
    print(
        json.dumps(
            {
                "error": (
                    "no Mintsoft credentials available — set MINTSOFT_API_KEY, "
                    "or run `mintsoft_api.py auth` once with --username/--password "
                    "(or MINTSOFT_USERNAME/MINTSOFT_PASSWORD env vars) to cache a key."
                )
            }
        )
    )
    sys.exit(1)


def _headers() -> dict:
    return {"ms-apikey": _resolve_api_key(), "Accept": "application/json"}


def _get(endpoint: str, params: dict | None = None) -> dict | list:
    """GET with retry on 429."""
    for _ in range(MAX_RETRIES):
        with httpx.Client(timeout=TIMEOUT) as c:
            resp = c.get(f"{API_BASE}{endpoint}", params=params, headers=_headers())
        if resp.status_code == 429:
            wait = int(resp.headers.get("Retry-After", "10"))
            time.sleep(wait)
            continue
        resp.raise_for_status()
        return resp.json()
    raise RuntimeError("Rate limit exceeded after retries")


def _paginate(endpoint: str, params: dict | None = None, limit: int = 0) -> list:
    """Fetch all pages from a paginated endpoint (PageNo/Limit)."""
    params = dict(params or {})
    page = 1
    results: list = []
    truncated = False
    while True:
        if _deadline_exceeded():
            truncated = True
            break
        params["PageNo"] = page
        params["Limit"] = PAGE_SIZE
        data = _get(endpoint, params)
        items = data if isinstance(data, list) else []
        if not items:
            break
        results.extend(items)
        if limit and len(results) >= limit:
            results = results[:limit]
            break
        if len(items) < PAGE_SIZE:
            break
        page += 1
        time.sleep(0.3)
    if truncated:
        print(
            json.dumps(
                {"warning": f"deadline approaching — returned {len(results)} partial results"}
            ),
            file=sys.stderr,
        )
    return results


def _out(data) -> None:
    """Print JSON output."""
    print(json.dumps(data, indent=2, default=str))


# -- Commands ----------------------------------------------------------------


def cmd_auth(args) -> None:
    """Authenticate and cache an API key (Mintsoft tokens are valid 24h)."""
    username = args.username or os.environ.get("MINTSOFT_USERNAME")
    password = args.password or os.environ.get("MINTSOFT_PASSWORD")
    if not username or not password:
        _out(
            {
                "error": (
                    "username and password required — pass --username/--password "
                    "or set MINTSOFT_USERNAME / MINTSOFT_PASSWORD."
                )
            }
        )
        sys.exit(1)
    with httpx.Client(timeout=15) as c:
        resp = c.post(
            f"{API_BASE}/Auth", json={"Username": username, "Password": password}
        )
    if resp.status_code == 200:
        key = resp.json()
        if isinstance(key, str):
            _save_cached_token(key)
            _out(
                {
                    "ok": True,
                    "cached_at": str(TOKEN_PATH),
                    "ttl_hours": TOKEN_TTL_SECONDS // 3600,
                }
            )
            return
    _out({"error": f"auth failed (HTTP {resp.status_code})", "detail": resp.text[:200]})
    sys.exit(1)


def cmd_whoami(args) -> None:
    """Sanity check — confirm the API key is set and accepted."""
    source = (
        "MINTSOFT_API_KEY env"
        if os.environ.get("MINTSOFT_API_KEY")
        else (f"cache ({TOKEN_PATH})" if _load_cached_token() else "none")
    )
    if source == "none":
        _out({"authenticated": False, "source": None})
        sys.exit(1)
    try:
        data = _get("/Warehouse")
        warehouses = data if isinstance(data, list) else [data]
        _out(
            {
                "authenticated": True,
                "source": source,
                "warehouse_count": len(warehouses),
            }
        )
    except httpx.HTTPStatusError as exc:
        _out(
            {
                "authenticated": False,
                "source": source,
                "error": f"HTTP {exc.response.status_code}",
            }
        )
        sys.exit(1)


def cmd_warehouses(args) -> None:
    data = _get("/Warehouse")
    warehouses = data if isinstance(data, list) else [data]
    if args.summary:
        summary = [
            {
                "ID": w.get("ID") or w.get("Id"),
                "Name": w.get("Name"),
                "AddressLine1": w.get("AddressLine1"),
                "City": w.get("City"),
                "PostCode": w.get("PostCode"),
                "Country": w.get("Country"),
            }
            for w in warehouses
        ]
        _out({"count": len(summary), "warehouses": summary})
    else:
        _out({"count": len(warehouses), "warehouses": warehouses})


def cmd_orders(args) -> None:
    params = {}
    if args.status:
        params["Status"] = args.status
    if args.since:
        params["SinceDate"] = args.since
    if args.include_items:
        params["IncludeOrderItems"] = "true"

    orders = _paginate("/Order/List", params, limit=args.limit)

    if args.summary:
        summary = [
            {
                "ID": o.get("ID") or o.get("Id"),
                "OrderNumber": o.get("OrderNumber"),
                "ExternalRef": o.get("ExternalReference"),
                "Status": o.get("OrderStatus"),
                "CustomerName": o.get("CustomerName"),
                "OrderDate": o.get("ReceivedDate") or o.get("OrderDate"),
                "TotalWeight": o.get("TotalWeight"),
                "ItemCount": len(o.get("OrderItems", [])) if o.get("OrderItems") else None,
            }
            for o in orders
        ]
        _out({"count": len(summary), "orders": summary})
    else:
        _out({"count": len(orders), "orders": orders})


def cmd_order_detail(args) -> None:
    data = _get(f"/Order/{args.order_id}")
    _out(data)


def cmd_stock_levels(args) -> None:
    params = {}
    if args.breakdown:
        params["Breakdown"] = "true"

    data = _get("/Product/StockLevels", params)
    items = data if isinstance(data, list) else [data] if data else []

    if args.summary:
        summary = [
            {
                "SKU": p.get("SKU"),
                "Name": p.get("Name"),
                "Available": p.get("Available"),
                "Allocated": p.get("Allocated"),
                "OnHand": p.get("OnHand"),
            }
            for p in items
        ]
        _out({"count": len(summary), "stock_levels": summary})
    else:
        _out({"count": len(items), "stock_levels": items})


def cmd_inventory(args) -> None:
    params = {"WarehouseId": args.warehouse}
    if args.since:
        params["LastUpdatedSince"] = args.since

    data = _get("/Product/StockLevelsByWarehouse", params)
    items = data if isinstance(data, list) else [data] if data else []

    if args.summary:
        summary = [
            {
                "SKU": p.get("SKU"),
                "Name": p.get("Name"),
                "Available": p.get("Available"),
                "Allocated": p.get("Allocated"),
                "OnHand": p.get("OnHand"),
            }
            for p in items
        ]
        _out({"count": len(summary), "inventory": summary})
    else:
        _out({"count": len(items), "inventory": items})


def cmd_products(args) -> None:
    products = _paginate("/Product/List", limit=args.limit)

    if args.summary:
        summary = [
            {
                "ID": p.get("ID") or p.get("Id"),
                "SKU": p.get("SKU"),
                "Name": p.get("Name"),
                "Barcode": p.get("Barcode"),
                "Weight": p.get("Weight"),
                "Price": p.get("Price"),
            }
            for p in products
        ]
        _out({"count": len(summary), "products": summary})
    else:
        _out({"count": len(products), "products": products})


def cmd_product_detail(args) -> None:
    data = _get(f"/Product/{args.product_id}")
    _out(data)


def cmd_asn_list(args) -> None:
    """ASN list — fetch Advanced Shipping Notices within a date range."""
    params = {"IncludeASNItems": "true"}
    if args.from_date:
        params["BookedInStartInterval"] = args.from_date
    if args.to_date:
        params["BookedInEndInterval"] = args.to_date
    if args.status:
        params["ASNStatusId"] = args.status
    if args.warehouse:
        params["WarehouseId"] = args.warehouse
    if args.client:
        params["ClientId"] = args.client

    page = 1
    results: list = []
    while True:
        if _deadline_exceeded():
            break
        params["PageNo"] = page
        params["Limit"] = 100
        data = _get("/ASN/List", params)
        items = data if isinstance(data, list) else []
        if not items:
            break
        results.extend(items)
        if args.limit and len(results) >= args.limit:
            results = results[: args.limit]
            break
        if len(items) < 100:
            break
        page += 1
        time.sleep(0.3)

    if args.summary:
        summary = []
        for a in results:
            asn_items = a.get("Items") or []
            summary.append(
                {
                    "ID": a.get("ID"),
                    "POReference": a.get("POReference"),
                    "Supplier": a.get("Supplier") or a.get("ProductSupplier"),
                    "Status": (a.get("ASNStatus") or {}).get("Name"),
                    "Warehouse": a.get("WarehouseId"),
                    "EstimatedDelivery": a.get("EstimatedDelivery"),
                    "BookedInDate": a.get("BookedInDate"),
                    "Quantity": a.get("Quantity"),
                    "ItemCount": len(asn_items),
                    "Items": [
                        {
                            "SKU": i.get("SKU"),
                            "QuantityExpected": i.get("QuantityExpected"),
                            # Mintsoft API typo preserved (Receieved) for compatibility
                            "QuantityReceived": i.get("QuantityReceieved"),
                            "QuantityBooked": i.get("QuantityBooked"),
                        }
                        for i in asn_items
                    ],
                }
            )
        _out({"count": len(summary), "asns": summary})
    else:
        _out({"count": len(results), "asns": results})


def cmd_asn_detail(args) -> None:
    data = _get(f"/ASN/{args.asn_id}")
    _out(data)


def cmd_product_usage(args) -> None:
    """Product Usage Report — stock flow data with filtering."""
    params = {}
    if args.flow:
        params["flow"] = args.flow
    if args.from_date:
        params["fromDate"] = args.from_date
    if args.to_date:
        params["toDate"] = args.to_date
    if args.warehouse:
        params["warehouseId"] = args.warehouse
    if args.client:
        params["clientId"] = args.client
    if args.product:
        params["productId"] = args.product
    if args.search:
        params["search"] = args.search
    if args.include_details:
        params["includeDetails"] = "true"

    page = 1
    results: list = []
    while True:
        if _deadline_exceeded():
            break
        params["pageNo"] = page
        params["limit"] = 1000
        data = _get("/Reports/ProductUsageReport", params)
        items = data if isinstance(data, list) else []
        if not items:
            break
        results.extend(items)
        if args.limit and len(results) >= args.limit:
            results = results[: args.limit]
            break
        if len(items) < 1000:
            break
        page += 1
        time.sleep(0.3)

    if args.summary:
        summary = [
            {
                "ID": r.get("ID"),
                "SKU": r.get("SKU"),
                "Quantity": r.get("Quantity"),
                "Flow": r.get("Flow"),
                "Reason": r.get("Reason"),
                "Date": r.get("Date"),
                "Warehouse": r.get("Warehouse"),
            }
            for r in results
        ]
        _out({"count": len(summary), "product_usage": summary})
    else:
        _out({"count": len(results), "product_usage": results})


# -- CLI ---------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Mintsoft warehouse-management API wrapper. "
            "See https://api.mintsoft.co.uk/swagger/index.html for endpoint docs."
        )
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=90,
        help="Max runtime in seconds for pagination (default 90, 0 = unlimited).",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # auth
    p = sub.add_parser("auth", help="Cache a Mintsoft API key (valid 24h).")
    p.add_argument("--username", help="Mintsoft username (or MINTSOFT_USERNAME env var).")
    p.add_argument("--password", help="Mintsoft password (or MINTSOFT_PASSWORD env var).")

    # whoami
    sub.add_parser("whoami", help="Show which credential source is in use and ping the API.")

    # warehouses
    p = sub.add_parser("warehouses", help="List all warehouses configured on the tenant.")
    p.add_argument("--summary", action="store_true", help="Compact output.")

    # orders
    p = sub.add_parser("orders", help="List orders, with optional filters.")
    p.add_argument("--status", help="Filter by order status string (e.g. Dispatched).")
    p.add_argument("--since", help="Orders since date (YYYY-MM-DD).")
    p.add_argument("--include-items", action="store_true", help="Include order line items in each result.")
    p.add_argument("--limit", type=int, default=0, help="Max records (0 = no cap).")
    p.add_argument("--summary", action="store_true", help="Compact output.")

    p = sub.add_parser("order", help="Fetch a single order by ID with full detail.")
    p.add_argument("order_id", help="Order ID.")

    # stock levels
    p = sub.add_parser(
        "stock-levels", help="Aggregate stock levels across all warehouses."
    )
    p.add_argument(
        "--breakdown",
        action="store_true",
        help="Include per-warehouse breakdown per SKU.",
    )
    p.add_argument("--summary", action="store_true", help="Compact output.")

    # inventory (per-warehouse)
    p = sub.add_parser(
        "inventory", help="Stock levels for a specific warehouse."
    )
    p.add_argument("--warehouse", required=True, help="Warehouse ID (required).")
    p.add_argument("--since", help="Last-updated-since date (YYYY-MM-DD).")
    p.add_argument("--summary", action="store_true", help="Compact output.")

    # products
    p = sub.add_parser("products", help="List products.")
    p.add_argument("--limit", type=int, default=0, help="Max records.")
    p.add_argument("--summary", action="store_true", help="Compact output.")

    p = sub.add_parser("product", help="Fetch a single product by ID.")
    p.add_argument("product_id", help="Product ID.")

    # asn
    p = sub.add_parser(
        "asn-list",
        help="List Advanced Shipping Notices, optionally filtered by date / status / warehouse.",
    )
    p.add_argument(
        "--from-date", help="Start date (YYYY-MM-DD) — filters by BookedInDate."
    )
    p.add_argument(
        "--to-date", help="End date (YYYY-MM-DD) — filters by BookedInDate."
    )
    p.add_argument(
        "--status",
        help="ASN status ID(s), semicolon-separated (e.g. '1;2'). 1=Pending, 2=Confirmed.",
    )
    p.add_argument("--warehouse", type=int, help="Warehouse ID.")
    p.add_argument("--client", type=int, help="Client ID.")
    p.add_argument("--limit", type=int, default=0, help="Max records.")
    p.add_argument("--summary", action="store_true", help="Compact output.")

    p = sub.add_parser("asn", help="Fetch a single ASN by ID.")
    p.add_argument("asn_id", help="ASN ID.")

    # product-usage
    p = sub.add_parser(
        "product-usage",
        help="Stock-flow report (same data as Mintsoft Reports → Product Usage Report).",
    )
    p.add_argument("--flow", help="Flow type: IN, OUT, ALLOCATE, UNALLOCATE.")
    p.add_argument("--from-date", help="Start date (YYYY-MM-DD).")
    p.add_argument("--to-date", help="End date (YYYY-MM-DD).")
    p.add_argument("--warehouse", type=int, help="Warehouse ID.")
    p.add_argument("--client", type=int, help="Client ID.")
    p.add_argument("--product", type=int, help="Product ID.")
    p.add_argument(
        "--search",
        help="Free-text search across reason, user, SKU, batch numbers.",
    )
    p.add_argument(
        "--include-details",
        action="store_true",
        help="Include location/batch/serial breakdown.",
    )
    p.add_argument("--limit", type=int, default=0, help="Max records.")
    p.add_argument("--summary", action="store_true", help="Compact output.")

    args = parser.parse_args()

    if args.timeout:
        _set_deadline(args.timeout)

    commands = {
        "auth": cmd_auth,
        "whoami": cmd_whoami,
        "warehouses": cmd_warehouses,
        "orders": cmd_orders,
        "order": cmd_order_detail,
        "stock-levels": cmd_stock_levels,
        "inventory": cmd_inventory,
        "products": cmd_products,
        "product": cmd_product_detail,
        "asn-list": cmd_asn_list,
        "asn": cmd_asn_detail,
        "product-usage": cmd_product_usage,
    }

    try:
        commands[args.command](args)
    except httpx.HTTPStatusError as e:
        _out({"error": f"HTTP {e.response.status_code}", "detail": e.response.text[:500]})
        sys.exit(1)
    except Exception as e:  # noqa: BLE001 — top-level CLI error reporter
        _out({"error": str(e)})
        sys.exit(1)


if __name__ == "__main__":
    main()
