"""CLI: python -m package_tracker track <ShipperCode> <LogisticCode> [--order-code] [--customer-name] [--sandbox]."""

import argparse
import json
import sys


def main() -> None:
    parser = argparse.ArgumentParser(description="Package Tracker")
    sub = parser.add_subparsers(dest="command", required=True)
    track_parser = sub.add_parser("track", help="Track by shipper code and logistic code")
    track_parser.add_argument("shipper_code", help="e.g. ZTO, SF, YTO")
    track_parser.add_argument("logistic_code", help="Tracking number")
    track_parser.add_argument("--order-code", default="", help="Optional order reference")
    track_parser.add_argument(
        "--customer-name",
        default="",
        help="For SF (顺丰): last 4 digits of phone",
    )
    track_parser.add_argument("--provider", default="", help="Provider name (default from config)")
    track_parser.add_argument("--config", default="", help="Config file path (JSON)")
    track_parser.add_argument("--sandbox", action="store_true", help="Use Kdniao sandbox")
    track_parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw JSON only",
    )
    args = parser.parse_args()

    try:
        from package_tracker import get_tracker

        tracker = get_tracker(
            provider=args.provider or None,
            config_path=args.config or None,
            sandbox=args.sandbox,
        )
        result = tracker.track(
            shipper_code=args.shipper_code,
            logistic_code=args.logistic_code,
            order_code=args.order_code or "",
            customer_name=args.customer_name or "",
        )
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    # Human-friendly summary
    success = result.get("Success", False)
    if not success:
        reason = result.get("Reason") or result.get("ReasonCode") or "Unknown"
        print(f"查询失败: {reason}")
        if result.get("ResultCode") is not None:
            print(f"ResultCode: {result.get('ResultCode')}")
        sys.exit(1)

    state = result.get("State")
    traces = result.get("Traces") or []
    print(f"状态: {state}")
    print("轨迹:")
    for t in reversed(traces):
        accept_time = t.get("AcceptTime", "")
        accept_station = t.get("AcceptStation", "")
        remark = t.get("Remark", "")
        line = f"  {accept_time}  {accept_station}"
        if remark:
            line += f"  ({remark})"
        print(line)


if __name__ == "__main__":
    main()

