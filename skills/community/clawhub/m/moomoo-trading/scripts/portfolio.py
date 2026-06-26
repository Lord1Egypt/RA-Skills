#!/usr/bin/env python3
"""View positions, balances, orders, and deals via moomoo OpenAPI."""

import argparse
import sys

from _moomoo_common import (
    DEFAULT_HOST,
    DEFAULT_PORT,
    SUPPORTED_TRADE_MARKETS,
    ensure_non_negative_int,
    ensure_positive_int,
    format_value,
    get_trade_market,
    load_openapi_module,
    normalize_market_code,
    normalize_ticker,
)


def trade_env(api, env_name):
    return api.TrdEnv.REAL if env_name == "real" else api.TrdEnv.SIMULATE


def render_table(data, columns):
    available = [column for column in columns if column in data.columns]
    if available:
        return data[available].to_string(index=False)
    return data.to_string(index=False)


def show_positions(ctx, api, args, trade_market):
    env = trade_env(api, args.env)
    ret, data = ctx.position_list_query(
        code=args.ticker or "",
        position_market=trade_market,
        trd_env=env,
        acc_id=args.account_id,
        acc_index=args.account_index,
        refresh_cache=args.refresh_cache,
    )
    if ret != api.RET_OK:
        print(f"Error fetching positions: {data}")
        return 1

    if data.empty:
        print("No open positions.")
        return 0

    cols = [
        "code",
        "stock_name",
        "qty",
        "cost_price",
        "market_val",
        "pl_val",
        "pl_ratio",
        "today_pl_val",
    ]
    print(f"\n{'🔴 REAL' if args.env == 'real' else '🟢 SIMULATED'} POSITIONS")
    print("=" * 60)
    print(render_table(data, cols))

    if "pl_val" in data.columns:
        print(f"\nTotal P&L: {format_value(data['pl_val'].sum())}")
    if "market_val" in data.columns:
        print(f"Total Market Value: {format_value(data['market_val'].sum())}")
    return 0


def show_account(ctx, api, args):
    env = trade_env(api, args.env)
    ret, data = ctx.accinfo_query(
        trd_env=env,
        acc_id=args.account_id,
        acc_index=args.account_index,
        refresh_cache=args.refresh_cache,
    )
    if ret != api.RET_OK:
        print(f"Error fetching account info: {data}")
        return 1

    if data.empty:
        print("No account data.")
        return 0

    row = data.iloc[0]
    print(f"\n{'🔴 REAL' if args.env == 'real' else '🟢 SIMULATED'} ACCOUNT")
    print("=" * 40)
    print(f"  Cash:           {format_value(row.get('cash'))}")
    print(f"  Total Assets:   {format_value(row.get('total_assets'))}")
    print(f"  Market Value:   {format_value(row.get('market_val'))}")
    print(f"  Buying Power:   {format_value(row.get('power'))}")
    print(f"  Frozen Cash:    {format_value(row.get('frozen_cash'))}")
    print(f"  Risk Level:     {format_value(row.get('risk_level'))}")
    return 0


def show_open_orders(ctx, api, args, trade_market):
    env = trade_env(api, args.env)
    ret, data = ctx.order_list_query(
        code=args.ticker or "",
        order_market=trade_market,
        trd_env=env,
        acc_id=args.account_id,
        acc_index=args.account_index,
        refresh_cache=args.refresh_cache,
    )
    if ret != api.RET_OK:
        print(f"Error fetching open orders: {data}")
        return 1

    if data.empty:
        print("No open orders found.")
        return 0

    cols = [
        "order_id",
        "code",
        "stock_name",
        "trd_side",
        "order_type",
        "price",
        "qty",
        "dealt_qty",
        "order_status",
        "create_time",
    ]
    print(f"\n{'🔴 REAL' if args.env == 'real' else '🟢 SIMULATED'} OPEN ORDERS")
    print("=" * 80)
    print(render_table(data, cols))
    return 0


def show_history_orders(ctx, api, args, trade_market):
    env = trade_env(api, args.env)
    ret, data = ctx.history_order_list_query(
        code=args.ticker or "",
        order_market=trade_market,
        start=args.start or "",
        end=args.end or "",
        trd_env=env,
        acc_id=args.account_id,
        acc_index=args.account_index,
    )
    if ret != api.RET_OK:
        print(f"Error fetching historical orders: {data}")
        return 1

    if data.empty:
        print("No historical orders found.")
        return 0

    cols = [
        "order_id",
        "code",
        "stock_name",
        "trd_side",
        "order_type",
        "price",
        "qty",
        "dealt_qty",
        "order_status",
        "create_time",
        "updated_time",
    ]
    print(f"\n{'🔴 REAL' if args.env == 'real' else '🟢 SIMULATED'} HISTORICAL ORDERS")
    print("=" * 90)
    print(render_table(data, cols))
    return 0


def show_deals(ctx, api, args, trade_market):
    if args.env != "real":
        print("Deal queries are only available for real trading accounts.")
        return 1

    env = trade_env(api, args.env)
    if args.start or args.end:
        ret, data = ctx.history_deal_list_query(
            code=args.ticker or "",
            deal_market=trade_market,
            start=args.start or "",
            end=args.end or "",
            trd_env=env,
            acc_id=args.account_id,
            acc_index=args.account_index,
        )
        title = "HISTORICAL DEALS"
    else:
        ret, data = ctx.deal_list_query(
            code=args.ticker or "",
            deal_market=trade_market,
            trd_env=env,
            acc_id=args.account_id,
            acc_index=args.account_index,
            refresh_cache=args.refresh_cache,
        )
        title = "TODAY'S DEALS"

    if ret != api.RET_OK:
        print(f"Error fetching deals: {data}")
        return 1

    if data.empty:
        print("No deals found.")
        return 0

    cols = [
        "deal_id",
        "order_id",
        "code",
        "stock_name",
        "trd_side",
        "price",
        "qty",
        "create_time",
        "updated_time",
    ]
    print(f"\n🔴 REAL {title}")
    print("=" * 90)
    print(render_table(data, cols))
    return 0


def main():
    parser = argparse.ArgumentParser(description="View moomoo portfolio, balance, orders, and deals")
    parser.add_argument("--env", choices=["sim", "real"], default="sim", help="Environment: sim or real (default: sim)")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--account", action="store_true", help="Show account balance and buying power")
    mode.add_argument("--orders", action="store_true", help="Show open orders")
    mode.add_argument("--history-orders", action="store_true", help="Show historical orders")
    mode.add_argument("--deals", action="store_true", help="Show today's deals, or historical deals when --start/--end is set")
    parser.add_argument("--ticker", help="Optional ticker filter in MARKET.CODE format")
    parser.add_argument("--start", help="Start date for --history-orders or historical --deals (YYYY-MM-DD)")
    parser.add_argument("--end", help="End date for --history-orders or historical --deals (YYYY-MM-DD)")
    parser.add_argument("--refresh-cache", action="store_true", help="Ask OpenD to refresh cached data before querying")
    parser.add_argument("--market", default="US", choices=SUPPORTED_TRADE_MARKETS, help="Trade market (default: US)")
    parser.add_argument("--account-id", type=int, default=0, help="Trade account ID. 0 means use --account-index (default: 0)")
    parser.add_argument("--account-index", type=int, default=0, help="Trade account index fallback when --account-id is 0 (default: 0)")
    parser.add_argument("--host", default=DEFAULT_HOST, help=f"OpenD host (default: {DEFAULT_HOST})")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"OpenD port (default: {DEFAULT_PORT})")
    args = parser.parse_args()

    try:
        ensure_positive_int(args.port, "port")
        ensure_non_negative_int(args.account_id, "account-id")
        ensure_non_negative_int(args.account_index, "account-index")
        args.market = normalize_market_code(args.market, SUPPORTED_TRADE_MARKETS)
        if args.ticker:
            args.ticker = normalize_ticker(args.ticker, allowed_markets=SUPPORTED_TRADE_MARKETS)
    except ValueError as exc:
        parser.error(str(exc))

    if args.ticker and args.market != args.ticker.split(".", 1)[0]:
        parser.error("--market does not match the ticker prefix.")

    if (args.start or args.end) and not (args.history_orders or args.deals):
        parser.error("--start/--end require --history-orders or --deals.")

    try:
        api, module_name = load_openapi_module()
    except ImportError as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)

    trade_market = get_trade_market(api, market_code=args.market)
    ctx = None
    try:
        print(f"Using SDK '{module_name}'.")
        ctx = api.OpenSecTradeContext(
            host=args.host,
            port=args.port,
            filter_trdmarket=trade_market,
        )

        if args.account:
            status = show_account(ctx, api, args)
        elif args.orders:
            status = show_open_orders(ctx, api, args, trade_market)
        elif args.history_orders:
            status = show_history_orders(ctx, api, args, trade_market)
        elif args.deals:
            status = show_deals(ctx, api, args, trade_market)
        else:
            status = show_positions(ctx, api, args, trade_market)
        sys.exit(status)
    except Exception as exc:
        print(f"Error: {exc}")
        print(f"Make sure OpenD is running on {args.host}:{args.port}")
        sys.exit(1)
    finally:
        if ctx:
            ctx.close()


if __name__ == "__main__":
    main()
