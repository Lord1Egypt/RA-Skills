#!/usr/bin/env python3
"""
Aster DEX API client — read and write operations.
Supports public market data, private account reads, and authenticated order management.
Uses Binance-style HMAC-SHA256 signing (Aster Futures API compatible).
"""
import hashlib
import hmac
import json
import math
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE_URL = os.getenv("ASTER_BASE_URL", "https://fapi.asterdex.com")
API_KEY = os.getenv("ASTER_API_KEY", "")
API_SECRET = os.getenv("ASTER_API_SECRET", "")

# Exchange info cache (symbol filters for quantity/price precision)
_EXCHANGE_INFO_CACHE: dict | None = None
_EXCHANGE_INFO_TS: float = 0.0
_EXCHANGE_INFO_TTL: float = 3600.0  # 1 hour cache


# ──────────────────────────────────────────────
# Auth helpers
# ──────────────────────────────────────────────

def _sign(params: dict) -> str:
    query = urllib.parse.urlencode(params)
    return hmac.new(API_SECRET.encode(), query.encode(), hashlib.sha256).hexdigest()


def _timestamp() -> int:
    return int(time.time() * 1000)


def mask(value: str, keep: int = 4) -> str:
    if not value:
        return ""
    if len(value) <= keep:
        return "*" * len(value)
    return "*" * (len(value) - keep) + value[-keep:]


# ──────────────────────────────────────────────
# HTTP helpers
# ──────────────────────────────────────────────

def _request_with_retry(method: str, path: str, params: dict = None,
                        private: bool = False, max_retries: int = 3) -> dict:
    """HTTP request with retry on rate limits (429) and transient errors (5xx)."""
    params = dict(params or {})
    for attempt in range(max_retries + 1):
        try:
            req_params = dict(params)
            headers = {}
            if method == "GET":
                if private:
                    if not API_KEY or not API_SECRET:
                        raise RuntimeError("missing ASTER_API_KEY/ASTER_API_SECRET")
                    req_params["timestamp"] = _timestamp()
                    req_params["signature"] = _sign(req_params)
                    headers["X-MBX-APIKEY"] = API_KEY
                query = urllib.parse.urlencode(req_params)
                url = BASE_URL + path + (("?" + query) if query else "")
                req = urllib.request.Request(url, headers=headers, method="GET")
            elif method == "DELETE":
                # DELETE params must be in query string for Binance-compatible APIs
                if private:
                    if not API_KEY or not API_SECRET:
                        raise RuntimeError("missing ASTER_API_KEY/ASTER_API_SECRET")
                    req_params["timestamp"] = _timestamp()
                    req_params["signature"] = _sign(req_params)
                    headers["X-MBX-APIKEY"] = API_KEY
                query = urllib.parse.urlencode(req_params)
                url = BASE_URL + path + "?" + query
                req = urllib.request.Request(url, headers=headers, method="DELETE")
            else:
                headers["Content-Type"] = "application/x-www-form-urlencoded"
                if private:
                    if not API_KEY or not API_SECRET:
                        raise RuntimeError("missing ASTER_API_KEY/ASTER_API_SECRET")
                    req_params["timestamp"] = _timestamp()
                    req_params["signature"] = _sign(req_params)
                    headers["X-MBX-APIKEY"] = API_KEY
                body = urllib.parse.urlencode(req_params).encode()
                url = BASE_URL + path
                req = urllib.request.Request(url, data=body, headers=headers, method=method)

            with urllib.request.urlopen(req, timeout=20) as resp:
                return json.loads(resp.read().decode())

        except urllib.error.HTTPError as e:
            status = e.code
            if status == 429 and attempt < max_retries:
                # Rate limited — exponential backoff
                retry_after = int(e.headers.get("Retry-After", 2 ** (attempt + 1)))
                time.sleep(min(retry_after, 30))
                continue
            if status >= 500 and attempt < max_retries:
                # Server error — retry with backoff
                time.sleep(2 ** attempt)
                continue
            # Read error body for context
            try:
                err_body = json.loads(e.read().decode())
            except Exception:
                err_body = {"code": status, "msg": str(e)}
            raise RuntimeError(f"Aster API error {status}: {json.dumps(err_body)}") from e
        except (urllib.error.URLError, TimeoutError) as e:
            if attempt < max_retries:
                time.sleep(2 ** attempt)
                continue
            raise
    raise RuntimeError("max retries exceeded")


def _get(path: str, params: dict = None, private: bool = False) -> dict:
    return _request_with_retry("GET", path, params, private)


def _post(path: str, params: dict, private: bool = True) -> dict:
    return _request_with_retry("POST", path, params, private)


def _delete(path: str, params: dict, private: bool = True) -> dict:
    return _request_with_retry("DELETE", path, params, private)


# ──────────────────────────────────────────────
# Market data (public)
# ──────────────────────────────────────────────

def get_ticker(symbol: str) -> dict:
    return _get("/fapi/v1/ticker/price", {"symbol": symbol})


def get_mark_price(symbol: str) -> dict:
    """Returns markPrice, indexPrice, estimatedSettlePrice, lastFundingRate, nextFundingTime."""
    return _get("/fapi/v1/premiumIndex", {"symbol": symbol})


def get_depth(symbol: str, limit: int = 5) -> dict:
    return _get("/fapi/v1/depth", {"symbol": symbol, "limit": limit})


def get_klines(symbol: str, interval: str, limit: int = 100) -> list:
    """
    Fetch OHLCV candles.
    interval: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
    Returns list of [open_time, open, high, low, close, volume, ...]
    """
    return _get("/fapi/v1/klines", {"symbol": symbol, "interval": interval, "limit": limit})


def get_funding_rate(symbol: str) -> dict:
    data = _get("/fapi/v1/fundingRate", {"symbol": symbol, "limit": 1})
    return data[0] if data else {}


def get_exchange_info() -> dict:
    return _get("/fapi/v1/exchangeInfo")


def get_exchange_info_cached() -> dict:
    """Get exchange info with 1-hour cache to avoid repeated calls."""
    global _EXCHANGE_INFO_CACHE, _EXCHANGE_INFO_TS
    now = time.time()
    if _EXCHANGE_INFO_CACHE is None or (now - _EXCHANGE_INFO_TS) > _EXCHANGE_INFO_TTL:
        _EXCHANGE_INFO_CACHE = get_exchange_info()
        _EXCHANGE_INFO_TS = now
    return _EXCHANGE_INFO_CACHE


def get_symbol_filters(symbol: str) -> dict:
    """Get LOT_SIZE and PRICE_FILTER for a symbol."""
    info = get_exchange_info_cached()
    for s in info.get("symbols", []):
        if s.get("symbol") == symbol:
            filters = {}
            for f in s.get("filters", []):
                if f.get("filterType") == "LOT_SIZE":
                    filters["step_size"] = float(f.get("stepSize", "0.001"))
                    filters["min_qty"] = float(f.get("minQty", "0.001"))
                    filters["max_qty"] = float(f.get("maxQty", "9999999"))
                elif f.get("filterType") == "PRICE_FILTER":
                    filters["tick_size"] = float(f.get("tickSize", "0.01"))
                    filters["min_price"] = float(f.get("minPrice", "0.01"))
                elif f.get("filterType") == "MIN_NOTIONAL":
                    filters["min_notional"] = float(f.get("notional", "5"))
            filters["quantity_precision"] = int(s.get("quantityPrecision", 3))
            filters["price_precision"] = int(s.get("pricePrecision", 2))
            return filters
    return {"step_size": 0.001, "min_qty": 0.001, "tick_size": 0.01,
            "quantity_precision": 3, "price_precision": 2, "min_notional": 5}


def round_quantity(symbol: str, quantity: float) -> float:
    """Round quantity to the exchange's step size for a symbol."""
    filters = get_symbol_filters(symbol)
    step = filters["step_size"]
    if step <= 0:
        return quantity
    precision = filters["quantity_precision"]
    # Floor to step size (exchange rejects rounding up)
    rounded = math.floor(quantity / step) * step
    return round(rounded, precision)


def round_price(symbol: str, price: float) -> float:
    """Round price to the exchange's tick size for a symbol."""
    filters = get_symbol_filters(symbol)
    tick = filters["tick_size"]
    if tick <= 0:
        return price
    precision = filters["price_precision"]
    rounded = round(round(price / tick) * tick, precision)
    return rounded


# ──────────────────────────────────────────────
# Account (private reads)
# ──────────────────────────────────────────────

def get_account() -> dict:
    return _get("/fapi/v2/account", private=True)


def get_positions(symbol: str = None) -> list:
    params = {}
    if symbol:
        params["symbol"] = symbol
    return _get("/fapi/v2/positionRisk", params, private=True)


def get_open_orders(symbol: str = None) -> list:
    params = {}
    if symbol:
        params["symbol"] = symbol
    return _get("/fapi/v1/openOrders", params, private=True)


def get_income_history(symbol: str = None, limit: int = 100) -> list:
    params = {"limit": limit}
    if symbol:
        params["symbol"] = symbol
    return _get("/fapi/v1/income", params, private=True)


def get_user_trades(symbol: str, limit: int = 50) -> list:
    """Fetch recent user trade fills for a symbol (filled orders with actual prices/quantities)."""
    return _get("/fapi/v1/userTrades", {"symbol": symbol, "limit": limit}, private=True)


def get_account_bundle(symbol: str = None) -> dict:
    account = get_account()
    positions = get_positions(symbol)
    orders = get_open_orders(symbol)
    return {"account": account, "positions": positions, "orders": orders}


# ──────────────────────────────────────────────
# Trade management (private writes)
# ──────────────────────────────────────────────

def set_leverage(symbol: str, leverage: int) -> dict:
    """Set leverage for a symbol. Returns {"symbol": ..., "leverage": ..., "maxNotionalValue": ...}"""
    return _post("/fapi/v1/leverage", {"symbol": symbol, "leverage": leverage})


def set_margin_type(symbol: str, margin_type: str = "ISOLATED") -> dict:
    """Set margin type: ISOLATED or CROSSED."""
    try:
        return _post("/fapi/v1/marginType", {"symbol": symbol, "marginType": margin_type})
    except Exception as e:
        # -4046: No need to change margin type (already set)
        return {"msg": str(e), "skipped": True}


def place_order(
    symbol: str,
    side: str,           # BUY or SELL
    quantity: float,
    order_type: str = "MARKET",
    price: float = None,
    stop_price: float = None,
    reduce_only: bool = False,
    time_in_force: str = "GTC",
    close_position: bool = False,
    working_type: str = "MARK_PRICE",
) -> dict:
    """
    Place a futures order.
    - For MARKET: side + quantity
    - For STOP_MARKET / TAKE_PROFIT_MARKET: stopPrice required, usually reduceOnly=True
    - For LIMIT: price + timeInForce required
    Automatically rounds quantity and price to exchange precision.
    """
    # Round to exchange precision
    qty_rounded = round_quantity(symbol, quantity)
    params = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": f"{qty_rounded:.8f}".rstrip("0").rstrip("."),
        "workingType": working_type,
    }
    if price is not None:
        price_rounded = round_price(symbol, price)
        params["price"] = f"{price_rounded:.8f}".rstrip("0").rstrip(".")
        params["timeInForce"] = time_in_force
    if stop_price is not None:
        sp_rounded = round_price(symbol, stop_price)
        params["stopPrice"] = f"{sp_rounded:.8f}".rstrip("0").rstrip(".")
    if reduce_only:
        params["reduceOnly"] = "true"
    if close_position:
        params["closePosition"] = "true"
        params.pop("quantity", None)
    return _post("/fapi/v1/order", params)


def cancel_order(symbol: str, order_id: int) -> dict:
    return _delete("/fapi/v1/order", {"symbol": symbol, "orderId": order_id})


def cancel_all_orders(symbol: str) -> dict:
    return _delete("/fapi/v1/allOpenOrders", {"symbol": symbol})


def close_position_market(symbol: str, side: str, quantity: float) -> dict:
    """
    Close a position with a market order.
    If long (side=BUY), close with side=SELL, reduceOnly=True.
    If short (side=SELL), close with side=BUY, reduceOnly=True.
    """
    close_side = "SELL" if side.upper() == "BUY" else "BUY"
    return place_order(symbol=symbol, side=close_side, quantity=quantity, reduce_only=True)


def place_bracket(
    symbol: str,
    entry_side: str,
    quantity: float,
    stop_loss_price: float,
    take_profit_price: float,
    leverage: int,
) -> dict:
    """
    Full bracket trade:
    1. Set leverage
    2. Set margin type (ISOLATED)
    3. Place entry MARKET order
    4. Place STOP_MARKET order (reduce-only)
    5. Place TAKE_PROFIT_MARKET order (reduce-only)
    Returns a dict with all results.
    """
    lev_result = set_leverage(symbol, leverage)
    margin_result = set_margin_type(symbol, "ISOLATED")

    # Entry
    entry_result = place_order(symbol=symbol, side=entry_side, quantity=quantity)

    # Stop-loss (opposite side, reduce-only)
    close_side = "SELL" if entry_side.upper() == "BUY" else "BUY"
    sl_result = place_order(
        symbol=symbol, side=close_side, quantity=quantity,
        order_type="STOP_MARKET", stop_price=stop_loss_price, reduce_only=True,
    )

    # Take-profit (opposite side, reduce-only)
    tp_result = place_order(
        symbol=symbol, side=close_side, quantity=quantity,
        order_type="TAKE_PROFIT_MARKET", stop_price=take_profit_price, reduce_only=True,
    )

    return {
        "leverage": lev_result,
        "margin_type": margin_result,
        "entry": entry_result,
        "stop_loss": sl_result,
        "take_profit": tp_result,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ──────────────────────────────────────────────
# Composite helpers
# ──────────────────────────────────────────────

def get_market_bundle(symbol: str) -> dict:
    """Full market snapshot: ticker, mark price, depth, klines (1h and 4h)."""
    ticker = get_ticker(symbol)
    mark = get_mark_price(symbol)
    depth = get_depth(symbol, 5)
    klines_5m = get_klines(symbol, "5m", 50)
    klines_1h = get_klines(symbol, "1h", 100)
    klines_4h = get_klines(symbol, "4h", 100)
    return {
        "symbol": symbol,
        "ticker": ticker,
        "mark_price": mark,
        "depth": depth,
        "klines_5m": klines_5m,
        "klines_1h": klines_1h,
        "klines_4h": klines_4h,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
    }


# ──────────────────────────────────────────────
# CLI interface
# ──────────────────────────────────────────────

def main() -> int:
    if len(sys.argv) < 2:
        print(
            "usage:\n"
            "  aster_readonly_client.py market <SYMBOL>\n"
            "  aster_readonly_client.py market_bundle <SYMBOL>\n"
            "  aster_readonly_client.py klines <SYMBOL> <INTERVAL> [LIMIT]\n"
            "  aster_readonly_client.py account [SYMBOL]\n"
            "  aster_readonly_client.py mark_price <SYMBOL>\n"
            "  aster_readonly_client.py funding <SYMBOL>\n"
            "  aster_readonly_client.py set_leverage <SYMBOL> <LEVERAGE>\n"
            "  aster_readonly_client.py cancel_all <SYMBOL>\n",
            file=sys.stderr,
        )
        return 2

    mode = sys.argv[1]

    if mode == "market":
        if len(sys.argv) != 3:
            print("usage: aster_readonly_client.py market <SYMBOL>", file=sys.stderr)
            return 2
        ticker = get_ticker(sys.argv[2])
        depth = get_depth(sys.argv[2])
        print(json.dumps({"ticker": ticker, "depth": depth}, indent=2))
        return 0

    if mode == "market_bundle":
        if len(sys.argv) != 3:
            print("usage: aster_readonly_client.py market_bundle <SYMBOL>", file=sys.stderr)
            return 2
        print(json.dumps(get_market_bundle(sys.argv[2]), indent=2))
        return 0

    if mode == "klines":
        if len(sys.argv) < 4:
            print("usage: aster_readonly_client.py klines <SYMBOL> <INTERVAL> [LIMIT]", file=sys.stderr)
            return 2
        limit = int(sys.argv[4]) if len(sys.argv) > 4 else 100
        print(json.dumps(get_klines(sys.argv[2], sys.argv[3], limit), indent=2))
        return 0

    if mode == "account":
        symbol = sys.argv[2] if len(sys.argv) > 2 else None
        print(json.dumps(get_account_bundle(symbol), indent=2))
        return 0

    if mode == "mark_price":
        if len(sys.argv) != 3:
            print("usage: aster_readonly_client.py mark_price <SYMBOL>", file=sys.stderr)
            return 2
        print(json.dumps(get_mark_price(sys.argv[2]), indent=2))
        return 0

    if mode == "funding":
        if len(sys.argv) != 3:
            print("usage: aster_readonly_client.py funding <SYMBOL>", file=sys.stderr)
            return 2
        print(json.dumps(get_funding_rate(sys.argv[2]), indent=2))
        return 0

    if mode == "set_leverage":
        if len(sys.argv) != 4:
            print("usage: aster_readonly_client.py set_leverage <SYMBOL> <LEVERAGE>", file=sys.stderr)
            return 2
        print(json.dumps(set_leverage(sys.argv[2], int(sys.argv[3])), indent=2))
        return 0

    if mode == "cancel_all":
        if len(sys.argv) != 3:
            print("usage: aster_readonly_client.py cancel_all <SYMBOL>", file=sys.stderr)
            return 2
        print(json.dumps(cancel_all_orders(sys.argv[2]), indent=2))
        return 0

    if mode == "income":
        symbol = sys.argv[2] if len(sys.argv) > 2 else None
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 100
        print(json.dumps(get_income_history(symbol, limit), indent=2))
        return 0

    if mode == "trades":
        if len(sys.argv) < 3:
            print("usage: aster_readonly_client.py trades <SYMBOL> [LIMIT]", file=sys.stderr)
            return 2
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 50
        print(json.dumps(get_user_trades(sys.argv[2], limit), indent=2))
        return 0

    if mode == "positions":
        symbol = sys.argv[2] if len(sys.argv) > 2 else None
        print(json.dumps(get_positions(symbol), indent=2))
        return 0

    print(f"unknown mode: {mode}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
