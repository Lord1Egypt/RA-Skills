#!/usr/bin/env python3
"""
MistTrack full address investigation script

Performs a comprehensive AML investigation on the specified address by calling:
1. v1/address_labels    - Address labels (entity identity)
2. v1/address_overview  - Address overview (balance/transaction stats)
3. v2/risk_score        - Risk score (KYT/KYA)
4. v1/address_trace     - Address profile (platform interactions/malicious events/relations)
5. v1/transactions_investigation - Transaction investigation (inbound/outbound details)
6. v1/address_counterparty       - Counterparty analysis

Usage:
    export MISTTRACK_API_KEY=YOUR_KEY
    python address_investigation.py --address 0x... --coin ETH
    python address_investigation.py --address 0x... --coin ETH --json

    # API key can also be passed via command line (lower priority than env var)
    python address_investigation.py --address 0x... --coin ETH --api-key YOUR_KEY
"""

import argparse
import json
import os
import sys
from datetime import datetime
from typing import Optional

import requests


BASE_URL = "https://openapi.misttrack.io"


def api_get(endpoint: str, params: dict) -> dict:
    """Send GET request and return JSON response"""
    response = requests.get(f"{BASE_URL}/{endpoint}", params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def investigate_address(coin: str, address: str, api_key: str) -> dict:
    """
    Perform a comprehensive investigation on an address, aggregating all API results

    Returns:
        Dict containing all investigation results
    """
    base_params = {"coin": coin, "address": address, "api_key": api_key}
    report = {"address": address, "coin": coin}

    # 1. Address labels
    print("  [1/6] Fetching address labels...")
    try:
        result = api_get("v1/address_labels", base_params)
        report["labels"] = result.get("data") if result.get("success") else {"error": result.get("msg")}
    except Exception as e:
        report["labels"] = {"error": str(e)}

    # 2. Address overview
    print("  [2/6] Fetching address overview...")
    try:
        result = api_get("v1/address_overview", base_params)
        report["overview"] = result.get("data") if result.get("success") else {"error": result.get("msg")}
    except Exception as e:
        report["overview"] = {"error": str(e)}

    # 3. Risk score
    print("  [3/6] Fetching risk score...")
    try:
        result = api_get("v2/risk_score", base_params)
        report["risk_score"] = result.get("data") if result.get("success") else {"error": result.get("msg")}
    except Exception as e:
        report["risk_score"] = {"error": str(e)}

    # 4. Address profile
    print("  [4/6] Fetching address profile...")
    try:
        result = api_get("v1/address_trace", base_params)
        report["address_trace"] = result.get("data") if result.get("success") else {"error": result.get("msg")}
    except Exception as e:
        report["address_trace"] = {"error": str(e)}

    # 5. Transaction investigation
    print("  [5/6] Fetching transaction investigation (page 1)...")
    try:
        params = dict(base_params)
        params["page"] = 1
        result = api_get("v1/transactions_investigation", params)
        report["transactions"] = result.get("data") if result.get("success") else {"error": result.get("msg")}
    except Exception as e:
        report["transactions"] = {"error": str(e)}

    # 6. Counterparty analysis
    print("  [6/6] Fetching counterparty analysis...")
    try:
        result = api_get("v1/address_counterparty", base_params)
        if result.get("success"):
            report["counterparty"] = result.get("address_counterparty_list", [])
        else:
            report["counterparty"] = {"error": result.get("msg")}
    except Exception as e:
        report["counterparty"] = {"error": str(e)}

    return report


def format_timestamp(ts: Optional[int]) -> str:
    """Convert Unix timestamp to human-readable time"""
    if not ts:
        return "N/A"
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")


def print_investigation_report(report: dict):
    """Format and print investigation report"""
    address = report.get("address", "")
    coin = report.get("coin", "")

    print(f"\n{'='*70}")
    print(f"  MistTrack Full Address Investigation Report")
    print(f"{'='*70}")
    print(f"  Address: {address}")
    print(f"  Token:   {coin}")

    # Labels
    labels = report.get("labels", {})
    if not labels.get("error"):
        print(f"\n  📋 Address Labels")
        print(f"  {'-'*50}")
        label_list = labels.get("label_list", [])
        label_type = labels.get("label_type", "")
        print(f"  Labels: {', '.join(label_list) if label_list else 'None'}")
        if label_type:
            print(f"  Type: {label_type}")

    # Overview
    overview = report.get("overview", {})
    if not overview.get("error"):
        print(f"\n  📊 Address Overview")
        print(f"  {'-'*50}")
        print(f"  Balance:         {overview.get('balance', 0):,.4f} {coin}")
        print(f"  Total txs:       {overview.get('txs_count', 0):,}")
        print(f"  Total received:  {overview.get('total_received', 0):,.4f}")
        print(f"  Total sent:      {overview.get('total_spent', 0):,.4f}")
        print(f"  First seen:      {format_timestamp(overview.get('first_seen'))}")
        print(f"  Last seen:       {format_timestamp(overview.get('last_seen'))}")

    # Risk score
    risk = report.get("risk_score", {})
    if not risk.get("error"):
        score = risk.get("score", 0)
        risk_level = risk.get("risk_level", "Unknown")
        detail_list = risk.get("detail_list", [])
        hacking_event = risk.get("hacking_event", "")

        level_emoji = {"Low": "✅", "Moderate": "⚡", "High": "⚠️", "Severe": "⛔"}.get(risk_level, "❓")
        print(f"\n  🔍 Risk Score (AML)")
        print(f"  {'-'*50}")
        print(f"  Score:  {score}/100")
        print(f"  Level:  {level_emoji} {risk_level}")
        if hacking_event:
            print(f"  Security event: {hacking_event}")
        if detail_list:
            print(f"  Risk description:")
            for item in detail_list:
                print(f"    • {item}")

        # Risk details (Top 5)
        risk_detail = risk.get("risk_detail", [])
        if risk_detail:
            print(f"  Risk-associated entities (Top 5):")
            for item in risk_detail[:5]:
                entity = item.get("entity", "")
                risk_type = item.get("risk_type", "")
                volume = item.get("volume", 0)
                hop_num = item.get("hop_num", 0)
                exposure_type = item.get("exposure_type", "")
                percent = item.get("percent", 0)
                print(f"    • {entity} [{risk_type}] {exposure_type} {hop_num} hop(s) ${volume:,.2f} ({percent:.2f}%)")

    # Address profile
    trace = report.get("address_trace", {})
    if trace and not trace.get("error"):
        print(f"\n  🔗 Address Profile")
        print(f"  {'-'*50}")
        first_address = trace.get("first_address", "")
        if first_address:
            print(f"  Gas source: {first_address}")

        use_platform = trace.get("use_platform", {})
        for platform_type in ["exchange", "dex", "mixer", "nft"]:
            platform = use_platform.get(platform_type, {})
            count = platform.get("count", 0)
            if count > 0:
                items = platform.get(f"{platform_type}_list", [])
                print(f"  {platform_type.upper()} ({count}): {', '.join(items[:5])}")

        malicious_event = trace.get("malicious_event", {})
        has_malicious = any(
            malicious_event.get(k, {}).get("count", 0) > 0
            for k in ["phishing", "ransom", "stealing", "laundering"]
        )
        if has_malicious:
            print(f"  ⚠️ Malicious events:")
            for event_type in ["phishing", "ransom", "stealing", "laundering"]:
                event = malicious_event.get(event_type, {})
                if event.get("count", 0) > 0:
                    items = event.get(f"{event_type}_list", [])
                    print(f"    - {event_type}: {', '.join(items[:3])}")

        relation_info = trace.get("relation_info", {})
        ens_list = relation_info.get("ens", {}).get("ens_list", [])
        twitter_list = relation_info.get("twitter", {}).get("twitter_list", [])
        if ens_list:
            print(f"  ENS: {', '.join(ens_list)}")
        if twitter_list:
            print(f"  Twitter: {', '.join(twitter_list)}")

    # Transaction summary
    transactions = report.get("transactions", {})
    if transactions and not transactions.get("error"):
        print(f"\n  💸 Transaction Investigation")
        print(f"  {'-'*50}")
        total_pages = transactions.get("total_pages", 1)
        transactions_on_page = transactions.get("transactions_on_page", 0)
        print(f"  Total pages: {total_pages}, Entries on page: {transactions_on_page}")

        out_txs = transactions.get("out", [])
        if out_txs:
            print(f"  Outbound targets (Top 5):")
            for tx in out_txs[:5]:
                label = tx.get("label") or tx.get("address", "")[:20]
                amount = tx.get("amount", 0)
                tx_type = tx.get("type", 1)
                type_labels = {1: "normal", 2: "malicious", 3: "entity", 4: "contract"}
                type_str = type_labels.get(tx_type, "")
                print(f"    → {label} [{type_str}] {amount:,.4f}")

        in_txs = transactions.get("in", [])
        if in_txs:
            print(f"  Inbound sources (Top 5):")
            for tx in in_txs[:5]:
                label = tx.get("label") or tx.get("address", "")[:20]
                amount = tx.get("amount", 0)
                tx_type = tx.get("type", 1)
                type_labels = {1: "normal", 2: "malicious", 3: "entity", 4: "contract"}
                type_str = type_labels.get(tx_type, "")
                print(f"    ← {label} [{type_str}] {amount:,.4f}")

    # Counterparties
    counterparty = report.get("counterparty", [])
    if counterparty and isinstance(counterparty, list):
        print(f"\n  🤝 Top Counterparties (Top 5)")
        print(f"  {'-'*50}")
        for item in counterparty[:5]:
            name = item.get("name", "")
            amount = item.get("amount", 0)
            percent = item.get("percent", 0)
            print(f"  {name:<25} ${amount:>15,.2f}  ({percent:.3f}%)")

    # Risk report link
    risk_report_url = report.get("risk_score", {}).get("risk_report_url", "")
    if risk_report_url:
        print(f"\n  📄 PDF Risk Report: {risk_report_url}")

    print(f"\n{'='*70}\n")


def main():
    parser = argparse.ArgumentParser(description="MistTrack full address investigation tool")
    parser.add_argument("--address", required=True, help="Address to investigate")
    parser.add_argument("--coin", required=True, help="Token type (e.g. ETH, BTC, TRX)")
    parser.add_argument("--api-key", dest="api_key", help="MistTrack API Key (env var MISTTRACK_API_KEY takes priority)")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Output raw JSON data")
    parser.add_argument("--output", "-o", help="Save JSON result to file")

    args = parser.parse_args()

    # Env var takes priority over --api-key
    api_key = os.environ.get("MISTTRACK_API_KEY") or args.api_key
    if not api_key:
        print("Error: set MISTTRACK_API_KEY env var or use --api-key", file=sys.stderr)
        sys.exit(1)

    print(f"\nRunning full investigation on address: {args.address}")
    print(f"Token: {args.coin}")
    print(f"{'='*60}")

    try:
        report = investigate_address(
            coin=args.coin,
            address=args.address,
            api_key=api_key,
        )

        if args.json_output or args.output:
            json_str = json.dumps(report, indent=2, ensure_ascii=False)
            if args.output:
                with open(args.output, "w", encoding="utf-8") as f:
                    f.write(json_str)
                print(f"\nResult saved to: {args.output}")
            if args.json_output:
                print(json_str)
        else:
            print_investigation_report(report)

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
