#!/usr/bin/env python3
"""
Enable Banking — Autonomous Data Fetch
Fetches balances and transactions for mandant accounts.

Usage:
    python fetch.py --mandant-id mueller
    python fetch.py --all
    python fetch.py --mandant-id mueller --date-from 2026-03-01 --date-to 2026-03-10
    python fetch.py --mandant-id mueller --balances-only
    python fetch.py --mandant-id mueller --transactions-only
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Add parent to path for lib imports
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.auth import (
    load_config,
    generate_jwt,
    api_request,
    load_mandant,
    save_mandant,
    list_mandanten,
    DATA_DIR,
)


# ---------------------------------------------------------------------------
# Date helpers
# ---------------------------------------------------------------------------

def validate_date(date_str: str, field_name: str) -> str:
    """Validate and normalize date string to ISO format."""
    formats = ["%Y-%m-%d", "%d.%m.%Y", "%d/%m/%Y"]
    for fmt in formats:
        try:
            d = datetime.strptime(date_str, fmt)
            return d.strftime("%Y-%m-%d")
        except ValueError:
            continue
    print(f"❌ Invalid date format for --{field_name}: '{date_str}'", file=sys.stderr)
    print(f"  Expected: YYYY-MM-DD (e.g. 2026-03-01)", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Fetch functions
# ---------------------------------------------------------------------------

def fetch_balances(account_uid: str, token: str) -> list:
    """GET /accounts/{uid}/balances."""
    result = api_request("GET", f"/accounts/{account_uid}/balances", token)
    if result is None:
        return []
    return result.get("balances", result) if isinstance(result, dict) else result


def fetch_transactions(
    account_uid: str,
    token: str,
    date_from: str | None = None,
    date_to: str | None = None,
) -> list:
    """GET /accounts/{uid}/transactions with pagination via continuation_key."""
    all_transactions = []
    params: dict = {}

    if date_from:
        params["date_from"] = date_from
    if date_to:
        params["date_to"] = date_to

    continuation_key = None
    page = 1

    while True:
        if continuation_key:
            params["continuation_key"] = continuation_key

        print(f"    Page {page}...", end="\r", file=sys.stderr)
        result = api_request("GET", f"/accounts/{account_uid}/transactions", token, params=params)

        if result is None:
            break

        transactions = result.get("transactions", []) if isinstance(result, dict) else result
        if isinstance(transactions, list):
            all_transactions.extend(transactions)

        # Check for next page
        continuation_key = result.get("continuation_key") if isinstance(result, dict) else None

        if not continuation_key:
            break

        page += 1
        time.sleep(0.5)  # Rate limit courtesy

    return all_transactions


def normalize_transaction(tx: dict) -> dict:
    """Normalize transaction to a consistent format."""
    # Amount handling
    amount_data = tx.get("transaction_amount") or tx.get("amount") or {}
    if isinstance(amount_data, dict):
        amount = amount_data.get("amount", "0")
        currency = amount_data.get("currency", "EUR")
    else:
        amount = str(amount_data)
        currency = tx.get("currency", "EUR")

    # Counterparty
    counterparty = (
        tx.get("creditor_name")
        or tx.get("debtor_name")
        or ""
    )

    # Description
    description = tx.get("remittance_information_unstructured") or ""
    if isinstance(description, list):
        description = " | ".join(description)

    return {
        "date": tx.get("booking_date") or tx.get("value_date") or "",
        "amount": str(amount),
        "currency": currency,
        "creditDebit": tx.get("credit_debit_indicator", ""),
        "counterparty": counterparty,
        "description": str(description),
        "bookingDate": tx.get("booking_date", ""),
        "valueDate": tx.get("value_date", ""),
    }


def normalize_balance(bal: dict) -> dict:
    """Normalize balance to a consistent format."""
    amount_data = bal.get("balance_amount") or bal.get("amount") or {}
    if isinstance(amount_data, dict):
        amount = amount_data.get("amount", "0")
        currency = amount_data.get("currency", "EUR")
    else:
        amount = str(amount_data)
        currency = bal.get("currency", "EUR")

    return {
        "type": bal.get("balance_type", ""),
        "amount": str(amount),
        "currency": currency,
        "date": bal.get("reference_date", bal.get("date", "")),
    }


# ---------------------------------------------------------------------------
# Fetch for one mandant
# ---------------------------------------------------------------------------

def fetch_mandant(
    mandant_id: str,
    token: str,
    date_from: str | None,
    date_to: str | None,
    balances_only: bool = False,
    transactions_only: bool = False,
    output_dir: Path | None = None,
) -> dict | None:
    """Fetch data for a single mandant. Returns structured result or None on error."""
    mandant = load_mandant(mandant_id)

    # Check session validity
    valid_until = mandant.get("validUntil", "")
    if valid_until:
        try:
            expiry = datetime.fromisoformat(valid_until.replace("Z", "+00:00"))
            if expiry < datetime.now(timezone.utc):
                print(f"⚠️  Session for '{mandant_id}' expired on {valid_until}", file=sys.stderr)
                print(f"   Run: python renew.py --mandant-id {mandant_id}", file=sys.stderr)
                sys.exit(2)
        except (ValueError, TypeError):
            pass

    session_id = mandant.get("sessionId")
    if not session_id:
        print(f"❌ No sessionId for mandant '{mandant_id}'", file=sys.stderr)
        return None

    accounts = mandant.get("accounts", [])
    if not accounts:
        print(f"⚠️  No accounts for mandant '{mandant_id}'", file=sys.stderr)
        return None

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    result = {
        "mandantId": mandant_id,
        "fetchedAt": now,
        "accounts": [],
    }

    for acc in accounts:
        uid = acc.get("uid", "")
        iban = acc.get("iban", "")
        name = acc.get("name", "")

        print(f"  📡 {iban or uid[:16]}...", file=sys.stderr)

        account_result: dict = {
            "uid": uid,
            "iban": iban,
            "name": name,
        }

        # Fetch balances
        if not transactions_only:
            raw_balances = fetch_balances(uid, token)
            account_result["balances"] = [normalize_balance(b) for b in raw_balances]
            print(f"    ✅ {len(account_result['balances'])} balance(s)", file=sys.stderr)

        # Fetch transactions
        if not balances_only:
            raw_transactions = fetch_transactions(uid, token, date_from, date_to)
            account_result["transactions"] = [normalize_transaction(t) for t in raw_transactions]
            print(f"    ✅ {len(account_result['transactions'])} transaction(s)", file=sys.stderr)

        result["accounts"].append(account_result)

    # Save to data directory
    data_dir = output_dir or DATA_DIR
    mandant_data_dir = data_dir / mandant_id
    mandant_data_dir.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    data_file = mandant_data_dir / f"{today}.json"
    with open(data_file, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    os.chmod(data_file, 0o600)
    print(f"  💾 Saved to {data_file}", file=sys.stderr)

    # Update lastFetch in mandant
    mandant["lastFetch"] = now
    save_mandant(mandant_id, mandant)

    return result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Enable Banking — Autonomous Data Fetch")
    parser.add_argument("--mandant-id", help="Fetch for a single mandant")
    parser.add_argument("--all", action="store_true", help="Fetch for all mandanten")
    parser.add_argument("--date-from", help="Transaction start date (YYYY-MM-DD)")
    parser.add_argument("--date-to", help="Transaction end date (YYYY-MM-DD)")
    parser.add_argument("--balances-only", action="store_true", help="Only fetch balances")
    parser.add_argument("--transactions-only", action="store_true", help="Only fetch transactions")
    parser.add_argument("--output-dir", help="Override data/ directory")
    args = parser.parse_args()

    if not args.mandant_id and not args.all:
        print("❌ Specify --mandant-id <id> or --all", file=sys.stderr)
        sys.exit(1)

    # Validate dates
    date_from = validate_date(args.date_from, "date-from") if args.date_from else None
    date_to = validate_date(args.date_to, "date-to") if args.date_to else None

    # Default date range: last 30 days
    if not date_from and not date_to and not args.balances_only:
        date_from = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        print(f"ℹ️  Default date range: {date_from} → today", file=sys.stderr)

    if date_from and date_to and date_from > date_to:
        print(f"❌ --date-from ({date_from}) must be before --date-to ({date_to})", file=sys.stderr)
        sys.exit(1)

    output_dir = Path(args.output_dir) if args.output_dir else None

    config = load_config()
    token = generate_jwt(config)

    # Determine mandant list
    if args.all:
        mandant_ids = list_mandanten()
        if not mandant_ids:
            print("ℹ️  No mandanten found in mandanten/", file=sys.stderr)
            sys.exit(0)
        print(f"📋 Fetching data for {len(mandant_ids)} mandant(en)...", file=sys.stderr)
    else:
        mandant_ids = [args.mandant_id]

    all_results = []

    for mid in mandant_ids:
        print(f"\n🏦 Mandant: {mid}", file=sys.stderr)
        try:
            result = fetch_mandant(
                mandant_id=mid,
                token=token,
                date_from=date_from,
                date_to=date_to,
                balances_only=args.balances_only,
                transactions_only=args.transactions_only,
                output_dir=output_dir,
            )
            if result:
                all_results.append(result)
        except SystemExit as e:
            if e.code == 2:
                # Session expired — skip but don't abort all
                if args.all:
                    continue
                raise
            raise

    # Output to stdout
    if len(all_results) == 1:
        print(json.dumps(all_results[0], indent=2, ensure_ascii=False))
    else:
        print(json.dumps(all_results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
