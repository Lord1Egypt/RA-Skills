#!/usr/bin/env python3
"""
MistTrack single-address risk score check script

Usage:
    export MISTTRACK_API_KEY=YOUR_KEY
    python risk_check.py --address 0x... --coin ETH
    python risk_check.py --txid 0x... --coin ETH

    # API key can also be passed via command line (lower priority than env var)
    python risk_check.py --address 0x... --coin ETH --api-key YOUR_KEY
"""

import argparse
import json
import os
import sys

import requests


BASE_URL = "https://openapi.misttrack.io"

RISK_LEVEL_COLOR = {
    "Low": "\033[32m",       # green
    "Moderate": "\033[33m",  # yellow
    "High": "\033[91m",      # orange-red
    "Severe": "\033[31m",    # red
}
RESET = "\033[0m"


def get_risk_score(coin: str, api_key: str, address: str = None, txid: str = None) -> dict:
    """Call v2/risk_score to get risk score"""
    params = {"coin": coin, "api_key": api_key}
    if address:
        params["address"] = address
    elif txid:
        params["txid"] = txid
    else:
        raise ValueError("at least one of address or txid is required")

    response = requests.get(f"{BASE_URL}/v2/risk_score", params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def get_address_labels(coin: str, address: str, api_key: str) -> dict:
    """Call v1/address_labels to get address labels"""
    params = {"coin": coin, "address": address, "api_key": api_key}
    response = requests.get(f"{BASE_URL}/v1/address_labels", params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def print_risk_report(data: dict, target: str):
    """Format and print risk report"""
    score = data.get("score", 0)
    risk_level = data.get("risk_level", "Unknown")
    hacking_event = data.get("hacking_event", "")
    detail_list = data.get("detail_list", [])
    risk_detail = data.get("risk_detail", [])
    risk_report_url = data.get("risk_report_url", "")

    color = RISK_LEVEL_COLOR.get(risk_level, "")

    print(f"\n{'='*60}")
    print(f"  MistTrack AML Risk Analysis Report")
    print(f"{'='*60}")
    print(f"  Target address/tx: {target}")
    print(f"  Risk score:        {color}{score}{RESET}")
    print(f"  Risk level:        {color}{risk_level}{RESET}")

    if hacking_event:
        print(f"  Security event:    {hacking_event}")

    if detail_list:
        print(f"\n  Risk description:")
        for item in detail_list:
            print(f"    • {item}")

    if risk_detail:
        print(f"\n  Risk details:")
        print(f"  {'Entity':<25} {'Risk Type':<20} {'Exposure':<10} {'Hops':<6} {'Amount(USD)':<15} {'Percent%'}")
        print(f"  {'-'*90}")
        for item in risk_detail:
            entity = item.get("entity", "")[:24]
            risk_type = item.get("risk_type", "")
            exposure = item.get("exposure_type", "")
            hop_num = item.get("hop_num", 0)
            volume = item.get("volume", 0)
            percent = item.get("percent", 0)
            print(f"  {entity:<25} {risk_type:<20} {exposure:<10} {hop_num:<6} {volume:<15,.2f} {percent:.3f}%")

    if risk_report_url:
        print(f"\n  PDF report: {risk_report_url}")

    print(f"{'='*60}")

    # Recommendation based on risk level
    recommendations = {
        "Severe": "⛔ Recommendation: Block withdrawals and transactions, report this address immediately!",
        "High":   "⚠️  Recommendation: High vigilance required, manual review before proceeding.",
        "Moderate": "⚡ Recommendation: Moderate monitoring, further investigation of transaction source advised.",
        "Low":    "✅ Recommendation: Low risk, normal processing allowed.",
    }
    if risk_level in recommendations:
        print(f"\n  {recommendations[risk_level]}\n")


def main():
    parser = argparse.ArgumentParser(description="MistTrack address risk score check tool")
    parser.add_argument("--address", help="Address to query")
    parser.add_argument("--txid", help="Transaction hash to query")
    parser.add_argument("--coin", required=True, help="Token type (e.g. ETH, BTC, TRX, USDT-TRC20)")
    parser.add_argument("--api-key", dest="api_key", help="MistTrack API Key (env var MISTTRACK_API_KEY takes priority)")
    parser.add_argument("--with-labels", action="store_true", help="Also fetch address label information")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Output raw JSON data")

    args = parser.parse_args()

    # Env var takes priority over --api-key
    api_key = os.environ.get("MISTTRACK_API_KEY") or args.api_key
    if not api_key:
        print("Error: set MISTTRACK_API_KEY env var or use --api-key", file=sys.stderr)
        sys.exit(1)

    if not args.address and not args.txid:
        print("Error: provide at least one of --address or --txid", file=sys.stderr)
        sys.exit(1)

    target = args.address or args.txid

    try:
        # Fetch address labels (optional)
        if args.with_labels and args.address:
            print(f"Fetching address labels: {args.address}...")
            label_result = get_address_labels(args.coin, args.address, api_key)
            if label_result.get("success"):
                label_data = label_result.get("data", {})
                print(f"Labels: {label_data.get('label_list', [])}, Type: {label_data.get('label_type', '')}")
            else:
                print(f"Label lookup failed: {label_result.get('msg')}")

        # Fetch risk score
        print(f"Querying risk score: {target}...")
        result = get_risk_score(
            coin=args.coin,
            api_key=api_key,
            address=args.address,
            txid=args.txid,
        )

        if args.json_output:
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return

        if not result.get("success"):
            print(f"Query failed: {result.get('msg')}", file=sys.stderr)
            sys.exit(1)

        print_risk_report(result.get("data", {}), target)

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 402:
            print("Error: MistTrack subscription has expired, please renew.", file=sys.stderr)
        elif e.response.status_code == 429:
            print("Error: Rate limit exceeded, please reduce request frequency.", file=sys.stderr)
        else:
            print(f"HTTP error: {e}", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Network request error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
