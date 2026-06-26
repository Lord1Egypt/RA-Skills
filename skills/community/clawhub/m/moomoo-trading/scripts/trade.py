#!/usr/bin/env python3
"""Place, modify, and cancel orders via moomoo OpenAPI."""

import argparse
import sys

from _moomoo_common import (
    DEFAULT_HOST,
    DEFAULT_PORT,
    DEFAULT_UNLOCK_ENV,
    SUPPORTED_TRADE_MARKETS,
    ensure_non_negative_int,
    ensure_positive_int,
    ensure_positive_number,
    env_password,
    format_value,
    get_trade_market,
    load_openapi_module,
    normalize_market_code,
    normalize_ticker,
)


def environment_enum(api, env_name):
    return api.TrdEnv.REAL if env_name == "real" else api.TrdEnv.SIMULATE


def open_trade_context(api, args, *, ticker=None):
    return api.OpenSecTradeContext(
        host=args.host,
        port=args.port,
        filter_trdmarket=get_trade_market(api, ticker=ticker, market_code=args.market),
    )


def unlock_if_needed(ctx, api, args):
    if args.env != "real":
        return False

    password = env_password(args.unlock_password_env)
    ret, data = ctx.unlock_trade(password=password)
    if ret != api.RET_OK:
        raise RuntimeError(f"unlock_trade failed: {data}")
    return True


def relock_if_needed(ctx, api, was_unlocked):
    if not was_unlocked:
        return

    ret, data = ctx.unlock_trade(is_unlock=False)
    if ret != api.RET_OK:
        print(f"⚠️  Failed to re-lock the live trading account: {data}")


def print_account_target(args):
    if args.account_id:
        print(f"  Account: acc_id={args.account_id}")
    else:
        print(f"  Account: acc_index={args.account_index}")


def print_place_preview(args):
    label = "REAL" if args.env == "real" else "SIMULATED"
    icon = "🔴" if args.env == "real" else "🟢"
    market = args.market or args.ticker.split(".", 1)[0]
    print(f"{icon} {label} ORDER")
    print(f"  Market:  {market}")
    print(f"  Action:  {args.action.upper()}")
    print(f"  Ticker:  {args.ticker}")
    print(f"  Qty:     {format_value(args.qty)}")
    print(f"  Type:    {args.type.upper()}")
    if args.type == "limit":
        print(f"  Price:   {format_value(args.price)}")
    if args.remark:
        print(f"  Remark:  {args.remark}")
    print_account_target(args)
    print()


def place_order(api, args):
    trd_env = environment_enum(api, args.env)
    side = api.TrdSide.BUY if args.action == "buy" else api.TrdSide.SELL
    order_type = api.OrderType.MARKET if args.type == "market" else api.OrderType.NORMAL

    ctx = None
    unlocked = False
    try:
        ctx = open_trade_context(api, args, ticker=args.ticker)
        unlocked = unlock_if_needed(ctx, api, args)
        print_place_preview(args)

        ret, data = ctx.place_order(
            price=0 if args.type == "market" else args.price,
            qty=args.qty,
            code=args.ticker,
            trd_side=side,
            order_type=order_type,
            trd_env=trd_env,
            acc_id=args.account_id,
            acc_index=args.account_index,
            remark=args.remark or None,
        )
        if ret != api.RET_OK:
            print(f"❌ Order failed: {data}")
            return 1

        print("✅ Order placed successfully:")
        print(data.to_string(index=False) if hasattr(data, "to_string") else data)
        return 0
    except Exception as exc:
        print(f"Error: {exc}")
        return 1
    finally:
        if ctx:
            relock_if_needed(ctx, api, unlocked)
            ctx.close()


def cancel_order(api, args):
    trd_env = environment_enum(api, args.env)

    ctx = None
    unlocked = False
    try:
        ctx = open_trade_context(api, args, ticker=args.ticker)
        unlocked = unlock_if_needed(ctx, api, args)
        print(f"{'🔴 REAL' if args.env == 'real' else '🟢 SIMULATED'} CANCEL")
        print(f"  Order ID: {args.order_id}")
        print(f"  Market:   {args.market or args.ticker.split('.', 1)[0]}")
        print_account_target(args)
        print()

        ret, data = ctx.modify_order(
            modify_order_op=api.ModifyOrderOp.CANCEL,
            order_id=args.order_id,
            price=0,
            qty=0,
            trd_env=trd_env,
            acc_id=args.account_id,
            acc_index=args.account_index,
        )
        if ret != api.RET_OK:
            print(f"❌ Cancel failed: {data}")
            return 1

        print(f"✅ Order {args.order_id} cancelled.")
        print(data.to_string(index=False) if hasattr(data, "to_string") else data)
        return 0
    except Exception as exc:
        print(f"Error: {exc}")
        return 1
    finally:
        if ctx:
            relock_if_needed(ctx, api, unlocked)
            ctx.close()


def modify_order(api, args):
    trd_env = environment_enum(api, args.env)

    ctx = None
    unlocked = False
    try:
        ctx = open_trade_context(api, args, ticker=args.ticker)
        unlocked = unlock_if_needed(ctx, api, args)
        print(f"{'🔴 REAL' if args.env == 'real' else '🟢 SIMULATED'} MODIFY")
        print(f"  Order ID: {args.order_id}")
        print(f"  Market:   {args.market or args.ticker.split('.', 1)[0]}")
        print(f"  Qty:      {format_value(args.qty)}")
        print(f"  Price:    {format_value(args.price)}")
        print_account_target(args)
        print()

        ret, data = ctx.modify_order(
            modify_order_op=api.ModifyOrderOp.NORMAL,
            order_id=args.order_id,
            price=args.price,
            qty=args.qty,
            trd_env=trd_env,
            acc_id=args.account_id,
            acc_index=args.account_index,
        )
        if ret != api.RET_OK:
            print(f"❌ Modify failed: {data}")
            return 1

        print(f"✅ Order {args.order_id} modified:")
        print(data.to_string(index=False) if hasattr(data, "to_string") else data)
        return 0
    except Exception as exc:
        print(f"Error: {exc}")
        return 1
    finally:
        if ctx:
            relock_if_needed(ctx, api, unlocked)
            ctx.close()


def validate_args(parser, args):
    try:
        ensure_positive_int(args.port, "port")
        ensure_non_negative_int(args.account_id, "account-id")
        ensure_non_negative_int(args.account_index, "account-index")
    except ValueError as exc:
        parser.error(str(exc))

    if args.market:
        try:
            args.market = normalize_market_code(args.market, SUPPORTED_TRADE_MARKETS)
        except ValueError as exc:
            parser.error(str(exc))

    if args.ticker:
        try:
            args.ticker = normalize_ticker(args.ticker, allowed_markets=SUPPORTED_TRADE_MARKETS)
        except ValueError as exc:
            parser.error(str(exc))

    if args.market and args.ticker and args.market != args.ticker.split(".", 1)[0]:
        parser.error("--market does not match the ticker prefix.")

    if args.env == "real" and not args.confirm:
        parser.error("Real trading actions require --confirm.")

    if args.cancel:
        if not args.order_id:
            parser.error("--order-id is required for cancel.")
        if not args.market and not args.ticker:
            parser.error("Cancel requires --market or --ticker to select the correct trade context.")
        return

    if args.modify:
        if not args.order_id:
            parser.error("--order-id is required for modify.")
        if not args.market and not args.ticker:
            parser.error("Modify requires --market or --ticker to select the correct trade context.")
        if args.price is None or args.qty is None:
            parser.error("--price and --qty are required for modify.")
        try:
            ensure_positive_number(args.price, "price")
            ensure_positive_number(args.qty, "qty")
        except ValueError as exc:
            parser.error(str(exc))
        return

    if not args.ticker or not args.action or args.qty is None:
        parser.error("--ticker, --action, and --qty are required for placing orders.")

    try:
        ensure_positive_number(args.qty, "qty")
    except ValueError as exc:
        parser.error(str(exc))

    if args.type == "limit":
        if args.price is None:
            parser.error("--price is required for limit orders.")
        try:
            ensure_positive_number(args.price, "price")
        except ValueError as exc:
            parser.error(str(exc))
    elif args.price is not None:
        parser.error("Do not pass --price for market orders.")


def main():
    parser = argparse.ArgumentParser(description="Place, modify, and cancel moomoo orders")

    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--cancel", action="store_true", help="Cancel an order")
    mode.add_argument("--modify", action="store_true", help="Modify an order")

    parser.add_argument("--ticker", help="Ticker in MARKET.CODE format (e.g., US.AAPL)")
    parser.add_argument("--market", choices=SUPPORTED_TRADE_MARKETS, help="Trade market. Required for cancel/modify when --ticker is omitted")
    parser.add_argument("--action", choices=["buy", "sell"], help="Buy or sell")
    parser.add_argument("--qty", type=float, help="Quantity of shares")
    parser.add_argument("--price", type=float, help="Price (required for limit orders and modify)")
    parser.add_argument("--type", choices=["market", "limit"], default="limit", help="Order type (default: limit)")
    parser.add_argument("--env", choices=["sim", "real"], default="sim", help="Environment: sim or real (default: sim)")
    parser.add_argument("--confirm", action="store_true", help="Required for all real-trading actions")
    parser.add_argument("--unlock-password-env", default=DEFAULT_UNLOCK_ENV, help=f"Env var holding the live-trading unlock password (default: {DEFAULT_UNLOCK_ENV})")
    parser.add_argument("--remark", help="Optional order remark")
    parser.add_argument("--order-id", help="Order ID (for cancel/modify)")
    parser.add_argument("--account-id", type=int, default=0, help="Trade account ID. 0 means use --account-index (default: 0)")
    parser.add_argument("--account-index", type=int, default=0, help="Trade account index fallback when --account-id is 0 (default: 0)")
    parser.add_argument("--host", default=DEFAULT_HOST, help=f"OpenD host (default: {DEFAULT_HOST})")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"OpenD port (default: {DEFAULT_PORT})")
    args = parser.parse_args()

    validate_args(parser, args)

    try:
        api, module_name = load_openapi_module()
    except ImportError as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)

    print(f"Using SDK '{module_name}'.")

    if args.cancel:
        sys.exit(cancel_order(api, args))
    if args.modify:
        sys.exit(modify_order(api, args))
    sys.exit(place_order(api, args))


if __name__ == "__main__":
    main()
