#!/usr/bin/env python3
"""Get real-time quotes, K-lines, and market snapshots via moomoo OpenAPI."""

import argparse
import sys

from _moomoo_common import (
    DEFAULT_HOST,
    DEFAULT_PORT,
    SUPPORTED_QUOTE_MARKETS,
    ensure_positive_int,
    load_openapi_module,
    parse_ticker_list,
)


def render_table(data, columns):
    available = [column for column in columns if column in data.columns]
    if available:
        return data[available].to_string(index=False)
    return data.to_string(index=False)


def get_quotes(ctx, api, tickers):
    """Get real-time quote data for tickers."""
    ret, data = ctx.get_market_snapshot(tickers)
    if ret != api.RET_OK:
        print(f"Error fetching quotes: {data}")
        return False
    if data.empty:
        print("No data returned.")
        return False

    cols = [
        "code",
        "name",
        "last_price",
        "open_price",
        "high_price",
        "low_price",
        "volume",
        "turnover",
        "price_spread",
    ]
    print(render_table(data, cols))
    return True


def get_klines(ctx, api, ticker, ktype, count, start="", end="", extended_time=False):
    """Get historical K-line data."""
    ktype_names = [
        "K_1M",
        "K_5M",
        "K_15M",
        "K_30M",
        "K_60M",
        "K_DAY",
        "K_WEEK",
        "K_MON",
        "K_QUARTER",
        "K_YEAR",
    ]
    ktype_map = {
        name: getattr(api.KLType, name)
        for name in ktype_names
        if hasattr(api.KLType, name)
    }
    kl = ktype_map.get(ktype.upper())
    if not kl:
        print(f"Invalid ktype '{ktype}'. Options: {', '.join(ktype_map.keys())}")
        return False

    request_kwargs = {"ktype": kl, "max_count": count}
    if start:
        request_kwargs["start"] = start
    if end:
        request_kwargs["end"] = end
    if extended_time:
        request_kwargs["extended_time"] = True

    ret, data, _ = ctx.request_history_kline(ticker, **request_kwargs)
    if ret != api.RET_OK:
        print(f"Error fetching K-lines: {data}")
        return False

    cols = ["time_key", "open", "close", "high", "low", "volume", "turnover"]
    print(f"\nK-line ({ktype.upper()}) for {ticker} (last {count}):")
    print(render_table(data, cols))
    return True


def get_snapshot(ctx, api, tickers):
    """Get market snapshot with extended data."""
    ret, data = ctx.get_market_snapshot(tickers)
    if ret != api.RET_OK:
        print(f"Error fetching snapshot: {data}")
        return False
    if data.empty:
        print("No data returned.")
        return False

    for _, row in data.iterrows():
        market_cap = row.get("total_market_val", row.get("market_val", "N/A"))
        high_52 = row.get("highest52weeks_price", row.get("high52w", "N/A"))
        low_52 = row.get("lowest52weeks_price", row.get("low52w", "N/A"))
        print(f"\n{'=' * 50}")
        print(f"  {row.get('code', '?')} - {row.get('name', '?')}")
        print(f"{'=' * 50}")
        print(f"  Last Price:    {row.get('last_price', 'N/A')}")
        print(f"  Open:          {row.get('open_price', 'N/A')}")
        print(f"  High:          {row.get('high_price', 'N/A')}")
        print(f"  Low:           {row.get('low_price', 'N/A')}")
        print(f"  Prev Close:    {row.get('prev_close_price', 'N/A')}")
        print(f"  Volume:        {row.get('volume', 'N/A')}")
        print(f"  Turnover:      {row.get('turnover', 'N/A')}")
        print(f"  Market Cap:    {market_cap}")
        print(f"  PE Ratio:      {row.get('pe_ratio', 'N/A')}")
        print(f"  Turnover Rate: {row.get('turnover_rate', 'N/A')}")
        print(f"  52W High:      {high_52}")
        print(f"  52W Low:       {low_52}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Get moomoo market quotes and K-lines")
    parser.add_argument(
        "tickers",
        nargs="*",
        help="Ticker(s) in MARKET.CODE format (e.g., US.AAPL HK.00700)",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--kline", action="store_true", help="Get historical K-line data")
    mode.add_argument("--snapshot", action="store_true", help="Get detailed market snapshot")
    parser.add_argument(
        "--ktype",
        default="K_DAY",
        help=(
            "K-line type: K_1M, K_5M, K_15M, K_30M, K_60M, K_DAY, "
            "K_WEEK, K_MON, K_QUARTER, K_YEAR (default: K_DAY)"
        ),
    )
    parser.add_argument("--count", type=int, default=20, help="Number of K-line bars (default: 20)")
    parser.add_argument("--start", help="Optional K-line start date/time")
    parser.add_argument("--end", help="Optional K-line end date/time")
    parser.add_argument(
        "--extended-time",
        action="store_true",
        help="Include extended-hours data when supported by the SDK/market",
    )
    parser.add_argument("--host", default=DEFAULT_HOST, help=f"OpenD host (default: {DEFAULT_HOST})")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"OpenD port (default: {DEFAULT_PORT})")
    args = parser.parse_args()

    if not args.tickers:
        parser.print_help()
        sys.exit(1)

    if (args.start or args.end or args.extended_time) and not args.kline:
        parser.error("--start, --end, and --extended-time only apply with --kline.")

    try:
        ensure_positive_int(args.count, "count")
        ensure_positive_int(args.port, "port")
        tickers = parse_ticker_list(args.tickers, allowed_markets=SUPPORTED_QUOTE_MARKETS)
    except ValueError as exc:
        parser.error(str(exc))

    if args.kline and len(tickers) > 1:
        parser.error("K-line mode supports one ticker at a time.")

    try:
        api, module_name = load_openapi_module()
    except ImportError as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)

    ctx = None
    try:
        print(f"Using SDK '{module_name}'.")
        ctx = api.OpenQuoteContext(host=args.host, port=args.port)

        if args.kline:
            success = get_klines(
                ctx,
                api,
                tickers[0],
                args.ktype,
                args.count,
                start=args.start or "",
                end=args.end or "",
                extended_time=args.extended_time,
            )
        elif args.snapshot:
            success = get_snapshot(ctx, api, tickers)
        else:
            success = get_quotes(ctx, api, tickers)

        if not success:
            sys.exit(1)
    except Exception as exc:
        print(f"Error: {exc}")
        print(f"Make sure OpenD is running on {args.host}:{args.port}")
        sys.exit(1)
    finally:
        if ctx:
            ctx.close()


if __name__ == "__main__":
    main()
