#!/usr/bin/env python3
"""Monitor tickers for price alerts via moomoo OpenAPI."""

import argparse
import sys
import time

from _moomoo_common import (
    DEFAULT_HOST,
    DEFAULT_PORT,
    SUPPORTED_QUOTE_MARKETS,
    ensure_positive_int,
    format_value,
    load_openapi_module,
    parse_ticker_list,
)


def print_alert(code, name, price, threshold, direction):
    comparator = ">=" if direction == "above" else "<="
    print(
        f"🔔 ALERT: {code} ({name}) at {format_value(price)} "
        f"{comparator} {format_value(threshold)} ({direction.upper()})"
    )


def main():
    parser = argparse.ArgumentParser(description="Monitor moomoo price alerts")
    parser.add_argument("--tickers", required=True, help="Comma-separated tickers (e.g., US.AAPL,US.TSLA)")
    parser.add_argument("--above", type=float, help="Alert when price goes above this level")
    parser.add_argument("--below", type=float, help="Alert when price goes below this level")
    parser.add_argument("--interval", type=int, default=10, help="Poll interval in seconds (default: 10)")
    parser.add_argument("--once", action="store_true", help="Check once and exit (no loop)")
    parser.add_argument("--repeat-alerts", action="store_true", help="Repeat alerts every polling cycle instead of only on state changes")
    parser.add_argument("--quit-on-alert", action="store_true", help="Exit after the first triggered alert")
    parser.add_argument("--max-checks", type=int, help="Maximum polling cycles before exit")
    parser.add_argument("--host", default=DEFAULT_HOST, help=f"OpenD host (default: {DEFAULT_HOST})")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"OpenD port (default: {DEFAULT_PORT})")
    args = parser.parse_args()

    if args.above is None and args.below is None:
        parser.error("At least one of --above or --below is required.")
    if args.above is not None and args.below is not None and args.above <= args.below:
        parser.error("--above must be greater than --below when both thresholds are set.")

    try:
        ensure_positive_int(args.interval, "interval")
        ensure_positive_int(args.port, "port")
        if args.max_checks is not None:
            ensure_positive_int(args.max_checks, "max-checks")
        tickers = parse_ticker_list([args.tickers], allowed_markets=SUPPORTED_QUOTE_MARKETS)
    except ValueError as exc:
        parser.error(str(exc))

    try:
        api, module_name = load_openapi_module()
    except ImportError as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)

    last_state = {}
    checks = 0
    ctx = None
    try:
        print(f"Using SDK '{module_name}'.")
        ctx = api.OpenQuoteContext(host=args.host, port=args.port)
        print(f"Monitoring: {', '.join(tickers)}")
        if args.above is not None:
            print(f"  Alert above: {format_value(args.above)}")
        if args.below is not None:
            print(f"  Alert below: {format_value(args.below)}")
        if not args.once:
            print(f"  Interval: {args.interval}s")
        print()

        while True:
            checks += 1
            ret, data = ctx.get_market_snapshot(tickers)
            if ret != api.RET_OK:
                print(f"Error fetching data: {data}")
                if args.once or (args.max_checks is not None and checks >= args.max_checks):
                    break
                time.sleep(args.interval)
                continue

            if data.empty:
                print("No data returned.")
                if args.once or (args.max_checks is not None and checks >= args.max_checks):
                    break
                time.sleep(args.interval)
                continue

            any_alert = False
            timestamp = time.strftime("%H:%M:%S")
            for _, row in data.iterrows():
                code = row.get("code", "?")
                name = row.get("name", "")
                price = row.get("last_price")
                if price is None:
                    print(f"  [{timestamp}] {code}: price unavailable")
                    continue

                current_state = {
                    "above": args.above is not None and price >= args.above,
                    "below": args.below is not None and price <= args.below,
                }
                previous_state = last_state.get(code, {"above": False, "below": False})

                if current_state["above"] and (args.repeat_alerts or not previous_state["above"]):
                    print_alert(code, name, price, args.above, "above")
                    any_alert = True
                if current_state["below"] and (args.repeat_alerts or not previous_state["below"]):
                    print_alert(code, name, price, args.below, "below")
                    any_alert = True
                if not current_state["above"] and not current_state["below"]:
                    print(f"  [{timestamp}] {code}: {format_value(price)}")

                last_state[code] = current_state

            if args.once:
                break
            if args.quit_on_alert and any_alert:
                break
            if args.max_checks is not None and checks >= args.max_checks:
                break
            time.sleep(args.interval)

    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
    except Exception as exc:
        print(f"Error: {exc}")
        sys.exit(1)
    finally:
        if ctx:
            ctx.close()


if __name__ == "__main__":
    main()
