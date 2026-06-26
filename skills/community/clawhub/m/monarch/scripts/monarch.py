#!/usr/bin/env python3
"""
Monarch Money CLI Wrapper for OpenClaw

Query Monarch Money for accounts, transactions, budgets, and cashflow.
Requires prior authentication via login_setup.py.

Usage:
    python3 monarch.py accounts
    python3 monarch.py transactions [--start DATE] [--end DATE] [--limit N]
    python3 monarch.py budgets
    python3 monarch.py cashflow [--month YYYY-MM]
    python3 monarch.py refresh
"""

import argparse
import asyncio
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

try:
    from monarchmoney import MonarchMoney
except ImportError:
    print(json.dumps({"error": "monarchmoney library not installed. Run: pip install monarchmoney"}))
    sys.exit(1)


SESSION_FILE = Path.home() / ".monarchmoney" / "mm_session.pickle"


async def get_authenticated_client() -> MonarchMoney:
    """Load saved session and return authenticated client."""
    if not SESSION_FILE.exists():
        raise RuntimeError(
            f"Not authenticated. Run login_setup.py first. "
            f"Session file not found: {SESSION_FILE}"
        )

    mm = MonarchMoney()
    mm.load_session(str(SESSION_FILE))
    return mm


async def get_accounts():
    """Fetch all accounts with balances."""
    mm = await get_authenticated_client()
    data = await mm.get_accounts()

    accounts = data.get("accounts", [])

    result = []
    for acc in accounts:
        result.append({
            "id": acc.get("id"),
            "displayName": acc.get("displayName"),
            "type": acc.get("type", {}).get("display") if isinstance(acc.get("type"), dict) else acc.get("type"),
            "subtype": acc.get("subtype", {}).get("display") if isinstance(acc.get("subtype"), dict) else acc.get("subtype"),
            "currentBalance": acc.get("currentBalance"),
            "displayBalance": acc.get("displayBalance"),
            "institution": acc.get("credential", {}).get("institution", {}).get("name") if acc.get("credential") else None,
            "isHidden": acc.get("isHidden", False),
            "includeInNetWorth": acc.get("includeInNetWorth", True),
        })

    return result


async def get_transactions(start_date: str = None, end_date: str = None, limit: int = 100):
    """Fetch transactions within date range."""
    mm = await get_authenticated_client()

    if not end_date:
        end_date = datetime.now().strftime("%Y-%m-%d")
    if not start_date:
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

    data = await mm.get_transactions(
        start_date=start_date,
        end_date=end_date,
        limit=limit
    )

    transactions = data.get("allTransactions", {}).get("results", [])

    result = []
    for tx in transactions:
        result.append({
            "id": tx.get("id"),
            "date": tx.get("date"),
            "amount": tx.get("amount"),
            "merchant": tx.get("merchant", {}).get("name") if tx.get("merchant") else tx.get("plaidName"),
            "category": tx.get("category", {}).get("name") if tx.get("category") else None,
            "categoryIcon": tx.get("category", {}).get("icon") if tx.get("category") else None,
            "account": tx.get("account", {}).get("displayName") if tx.get("account") else None,
            "notes": tx.get("notes"),
            "isPending": tx.get("isPending", False),
            "isRecurring": tx.get("isRecurring", False),
        })

    return result


async def get_budgets():
    """Fetch current budget information."""
    mm = await get_authenticated_client()
    data = await mm.get_budgets()

    budget_data = data.get("budgetData", {})

    result = {
        "monthlyBudget": budget_data.get("monthlyBudget"),
        "totalSpent": budget_data.get("totalSpent"),
        "categories": []
    }

    for cat in budget_data.get("budgetCategories", []):
        result["categories"].append({
            "name": cat.get("category", {}).get("name") if cat.get("category") else None,
            "budgetAmount": cat.get("budgetAmount"),
            "spentAmount": cat.get("spentAmount"),
            "remainingAmount": cat.get("remainingAmount"),
        })

    return result


async def get_cashflow(month: str = None):
    """Fetch cashflow summary for a month."""
    mm = await get_authenticated_client()

    if not month:
        month = datetime.now().strftime("%Y-%m")

    year, mon = month.split("-")
    start_date = f"{year}-{mon}-01"

    if int(mon) == 12:
        end_date = f"{int(year)+1}-01-01"
    else:
        end_date = f"{year}-{int(mon)+1:02d}-01"

    data = await mm.get_cashflow(
        start_date=start_date,
        end_date=end_date
    )

    summary = data.get("summary", [{}])[0] if data.get("summary") else {}

    return {
        "month": month,
        "income": summary.get("sumIncome"),
        "expenses": summary.get("sumExpense"),
        "savings": summary.get("savings"),
        "savingsRate": summary.get("savingsRate"),
    }


async def refresh_accounts():
    """Trigger account refresh with connected institutions."""
    mm = await get_authenticated_client()

    data = await mm.get_accounts()
    accounts = data.get("accounts", [])

    credential_ids = set()
    for acc in accounts:
        cred = acc.get("credential")
        if cred and cred.get("id"):
            credential_ids.add(cred["id"])

    results = []
    for cred_id in credential_ids:
        try:
            await mm.request_accounts_refresh(cred_id)
            results.append({"credentialId": cred_id, "status": "refresh_requested"})
        except Exception as e:
            results.append({"credentialId": cred_id, "status": "error", "message": str(e)})

    return {"refreshed": len(results), "results": results}


def main():
    parser = argparse.ArgumentParser(description="Query Monarch Money")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    subparsers.add_parser("accounts", help="List all accounts")

    tx_parser = subparsers.add_parser("transactions", help="List transactions")
    tx_parser.add_argument("--start", help="Start date (YYYY-MM-DD)")
    tx_parser.add_argument("--end", help="End date (YYYY-MM-DD)")
    tx_parser.add_argument("--limit", type=int, default=100, help="Max transactions")

    subparsers.add_parser("budgets", help="Get budget summary")

    cf_parser = subparsers.add_parser("cashflow", help="Get cashflow summary")
    cf_parser.add_argument("--month", help="Month (YYYY-MM)")

    subparsers.add_parser("refresh", help="Refresh account data")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == "accounts":
            result = asyncio.run(get_accounts())
        elif args.command == "transactions":
            result = asyncio.run(get_transactions(args.start, args.end, args.limit))
        elif args.command == "budgets":
            result = asyncio.run(get_budgets())
        elif args.command == "cashflow":
            result = asyncio.run(get_cashflow(args.month))
        elif args.command == "refresh":
            result = asyncio.run(refresh_accounts())
        else:
            parser.print_help()
            sys.exit(1)

        print(json.dumps(result, indent=2, default=str))

    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
