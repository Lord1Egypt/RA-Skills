#!/usr/bin/env python3
"""Check OpenD connectivity, account discovery, and simulated-trading access."""

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
)


def show_accounts(ctx, api):
    """Show available trading accounts."""
    ret, data = ctx.get_acc_list()
    if ret != api.RET_OK:
        print(f"\n⚠️  Could not fetch trading accounts: {data}")
        return

    if data.empty:
        print("\n⚠️  No trading accounts returned by OpenD.")
        return

    cols = ["acc_id", "trd_env", "acc_type", "card_num", "uni_card_num", "sim_acc_type"]
    available = [column for column in cols if column in data.columns]
    print("\nTrading accounts")
    print("-" * 60)
    print((data[available] if available else data).to_string(index=False))


def main():
    parser = argparse.ArgumentParser(
        description="Check moomoo/OpenD connectivity and show account access"
    )
    parser.add_argument("--host", default=DEFAULT_HOST, help=f"OpenD host (default: {DEFAULT_HOST})")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"OpenD port (default: {DEFAULT_PORT})")
    parser.add_argument(
        "--market",
        default="US",
        choices=SUPPORTED_TRADE_MARKETS,
        help="Trade market used for account checks (default: US)",
    )
    parser.add_argument(
        "--account-id",
        type=int,
        default=0,
        help="Trade account ID. 0 means use --account-index (default: 0)",
    )
    parser.add_argument(
        "--account-index",
        type=int,
        default=0,
        help="Trade account index fallback when --account-id is 0 (default: 0)",
    )
    args = parser.parse_args()

    try:
        ensure_positive_int(args.port, "port")
        ensure_non_negative_int(args.account_id, "account-id")
        ensure_non_negative_int(args.account_index, "account-index")
    except ValueError as exc:
        parser.error(str(exc))

    try:
        api, module_name = load_openapi_module()
    except ImportError as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)

    print(f"Connecting to OpenD at {args.host}:{args.port} using '{module_name}' ...")

    quote_ctx = None
    try:
        quote_ctx = api.OpenQuoteContext(host=args.host, port=args.port)
        ret, data = quote_ctx.get_global_state()
        if ret != api.RET_OK:
            print(f"\n❌ Quote connection failed: {data}")
            sys.exit(1)

        print("\n✅ Quote connection: OK")
        print(f"  Program status: {data.get('program_status_type', 'N/A')}")
        print(f"  Quote login:    {data.get('qot_logined', 'N/A')}")
        print(f"  Trade login:    {data.get('trd_logined', 'N/A')}")
        print(f"  Market (US):    {data.get('market_us', 'N/A')}")
        print(f"  Market (HK):    {data.get('market_hk', 'N/A')}")
        print(f"  Server version: {data.get('server_ver', 'N/A')}")
    except Exception as exc:
        print(f"\n❌ Cannot connect to OpenD quote service: {exc}")
        print("\nMake sure OpenD is running and logged in. See references/setup-guide.md")
        sys.exit(1)
    finally:
        if quote_ctx:
            quote_ctx.close()

    trade_ctx = None
    try:
        trade_ctx = api.OpenSecTradeContext(
            host=args.host,
            port=args.port,
            filter_trdmarket=get_trade_market(api, market_code=args.market),
        )
        show_accounts(trade_ctx, api)

        ret, data = trade_ctx.accinfo_query(
            trd_env=api.TrdEnv.SIMULATE,
            acc_id=args.account_id,
            acc_index=args.account_index,
        )
        if ret == api.RET_OK:
            print("\n✅ Trade connection (simulated): OK")
            if not data.empty:
                row = data.iloc[0]
                print(f"  Cash:         {format_value(row.get('cash'))}")
                print(f"  Total assets: {format_value(row.get('total_assets'))}")
                print(f"  Buying power: {format_value(row.get('power'))}")
        else:
            print(f"\n⚠️  Simulated trade account check failed: {data}")
    except Exception as exc:
        print(f"\n⚠️  Trade connection test failed: {exc}")
    finally:
        if trade_ctx:
            trade_ctx.close()

    print("\n✅ Setup check complete.")


if __name__ == "__main__":
    main()
