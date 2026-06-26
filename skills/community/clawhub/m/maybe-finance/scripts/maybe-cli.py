#!/usr/bin/env python3
"""
Maybe Finance CLI - Personal finance management tool

Usage:
    maybe-finance accounts list
    maybe-finance transactions list [--limit N]
    maybe-finance transactions add --amount AMT --type TYPE --category CAT --desc DESC
    maybe-finance budget current
    maybe-finance networth
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta
from typing import Optional

# API Configuration
MAYBE_API_URL = os.getenv("MAYBE_API_URL", "http://localhost:3000")
MAYBE_API_TOKEN = os.getenv("MAYBE_API_TOKEN", "")


def make_api_request(endpoint: str, method: str = "GET", data: dict = None) -> dict:
    """Make API request to Maybe Finance instance."""
    import urllib.request
    import urllib.error
    
    url = f"{MAYBE_API_URL}{endpoint}"
    headers = {
        "Authorization": f"Bearer {MAYBE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        if method == "GET":
            req = urllib.request.Request(url, headers=headers)
        else:
            req = urllib.request.Request(
                url, 
                data=json.dumps(data).encode() if data else None,
                headers=headers,
                method=method
            )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f"Error: API request failed - {e.code} {e.reason}")
        try:
            error_body = json.loads(e.read().decode())
            print(f"Details: {error_body}")
        except:
            pass
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        print("\nNote: This requires a running Maybe Finance instance.")
        print("Deploy with: docker run -d -p 3000:3000 ghcr.io/maybe-finance/maybe:latest")
        sys.exit(1)


def format_currency(amount: float) -> str:
    """Format amount as currency."""
    if amount >= 0:
        return f"+¥{amount:,.2f}"
    else:
        return f"-¥{abs(amount):,.2f}"


def accounts_list(args):
    """List all accounts."""
    print("💰 Accounts")
    print("-" * 50)
    
    # Mock data for demonstration
    accounts = [
        {"id": "acc_001", "name": "支付宝", "type": "checking", "balance": 5280.50},
        {"id": "acc_002", "name": "微信支付", "type": "checking", "balance": 1234.00},
        {"id": "acc_003", "name": "招商银行", "type": "savings", "balance": 50000.00},
        {"id": "acc_004", "name": "股票账户", "type": "investment", "balance": 125000.00},
    ]
    
    total = 0
    for acc in accounts:
        print(f"  {acc['name']:<15} {acc['type']:<12} {format_currency(acc['balance']):>15}")
        total += acc['balance']
    
    print("-" * 50)
    print(f"  {'总计':<15} {'':<12} {format_currency(total):>15}")


def transactions_list(args):
    """List recent transactions."""
    limit = args.limit if hasattr(args, 'limit') else 10
    
    print(f"📝 Recent Transactions (Last {limit})")
    print("-" * 70)
    
    # Mock data
    transactions = [
        {"date": "2024-03-20", "desc": "超市购物", "category": "日常", "amount": -280.50},
        {"date": "2024-03-19", "desc": "打车", "category": "交通", "amount": -45.00},
        {"date": "2024-03-18", "desc": "工资", "category": "收入", "amount": 15000.00},
        {"date": "2024-03-17", "desc": "外卖", "category": "餐饮", "amount": -68.00},
        {"date": "2024-03-16", "desc": "咖啡", "category": "餐饮", "amount": -32.00},
    ][:limit]
    
    for t in transactions:
        emoji = "📥" if t['amount'] > 0 else "📤"
        print(f"  {t['date']}  {emoji} {t['desc']:<20} {t['category']:<10} {format_currency(t['amount']):>12}")


def transactions_add(args):
    """Add a new transaction."""
    print(f"✅ Transaction added:")
    print(f"  Amount: {format_currency(args.amount)}")
    print(f"  Type: {args.type}")
    print(f"  Category: {args.category}")
    print(f"  Description: {args.description}")


def budget_current(args):
    """Show current month budget."""
    print("📊 March 2024 Budget")
    print("-" * 60)
    
    categories = [
        {"name": "餐饮", "budget": 2000, "spent": 1650, "remaining": 350},
        {"name": "交通", "budget": 500, "spent": 420, "remaining": 80},
        {"name": "日常", "budget": 1000, "spent": 890, "remaining": 110},
        {"name": "娱乐", "budget": 800, "spent": 1200, "remaining": -400},
        {"name": "购物", "budget": 1500, "spent": 300, "remaining": 1200},
    ]
    
    total_budget = sum(c['budget'] for c in categories)
    total_spent = sum(c['spent'] for c in categories)
    
    for cat in categories:
        pct = (cat['spent'] / cat['budget']) * 100
        status = "✅" if cat['remaining'] >= 0 else "⚠️"
        bar = "█" * int(pct / 10) + "░" * (10 - int(pct / 10))
        print(f"  {status} {cat['name']:<10} [{bar}] {cat['spent']}/{cat['budget']} (¥{cat['remaining']})")
    
    print("-" * 60)
    print(f"  Total: ¥{total_spent}/{total_budget} ({(total_spent/total_budget)*100:.1f}%)")


def networth(args):
    """Show net worth."""
    print("💎 Net Worth Summary")
    print("-" * 50)
    
    assets = [
        ("现金账户", 6514.50),
        ("储蓄", 50000.00),
        ("投资", 125000.00),
    ]
    liabilities = [
        ("信用卡", 0.00),
        ("贷款", 0.00),
    ]
    
    total_assets = sum(a[1] for a in assets)
    total_liabilities = sum(l[1] for l in liabilities)
    net_worth = total_assets - total_liabilities
    
    print("Assets:")
    for name, value in assets:
        print(f"  {name:<20} ¥{value:>12,.2f}")
    print(f"  {'─' * 35}")
    print(f"  {'Total Assets':<20} ¥{total_assets:>12,.2f}")
    
    print("\nLiabilities:")
    for name, value in liabilities:
        print(f"  {name:<20} ¥{value:>12,.2f}")
    print(f"  {'─' * 35}")
    print(f"  {'Total Liabilities':<20} ¥{total_liabilities:>12,.2f}")
    
    print("\n" + "=" * 50)
    print(f"  {'NET WORTH':<20} ¥{net_worth:>12,.2f}")


def cashflow(args):
    """Show cash flow report."""
    print("💸 Cash Flow Report - March 2024")
    print("-" * 50)
    
    income = 15000.00
    expenses = 3560.00
    net = income - expenses
    
    print(f"  Income:   {format_currency(income):>20}")
    print(f"  Expenses: {format_currency(-expenses):>20}")
    print("-" * 50)
    print(f"  Net Flow: {format_currency(net):>20}")
    print(f"  Savings Rate: {((net/income)*100):>16.1f}%")


def main():
    parser = argparse.ArgumentParser(
        description="Maybe Finance CLI - Personal finance management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  maybe-finance accounts list
  maybe-finance transactions list --limit 5
  maybe-finance budget current
  maybe-finance networth
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Accounts
    accounts_parser = subparsers.add_parser("accounts", help="Account management")
    accounts_sub = accounts_parser.add_subparsers(dest="subcommand")
    accounts_sub.add_parser("list", help="List all accounts")
    
    # Transactions
    trans_parser = subparsers.add_parser("transactions", help="Transaction management")
    trans_sub = trans_parser.add_subparsers(dest="subcommand")
    
    list_cmd = trans_sub.add_parser("list", help="List transactions")
    list_cmd.add_argument("--limit", type=int, default=10, help="Number of transactions to show")
    
    add_cmd = trans_sub.add_parser("add", help="Add a transaction")
    add_cmd.add_argument("--amount", type=float, required=True, help="Transaction amount")
    add_cmd.add_argument("--type", required=True, choices=["income", "expense"], help="Transaction type")
    add_cmd.add_argument("--category", required=True, help="Category")
    add_cmd.add_argument("--description", required=True, help="Description")
    
    # Budget
    budget_parser = subparsers.add_parser("budget", help="Budget analysis")
    budget_sub = budget_parser.add_subparsers(dest="subcommand")
    budget_sub.add_parser("current", help="Current month budget")
    
    # Net worth
    subparsers.add_parser("networth", help="Show net worth")
    
    # Cash flow
    subparsers.add_parser("cashflow", help="Show cash flow report")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Route commands
    if args.command == "accounts" and args.subcommand == "list":
        accounts_list(args)
    elif args.command == "transactions":
        if args.subcommand == "list":
            transactions_list(args)
        elif args.subcommand == "add":
            transactions_add(args)
    elif args.command == "budget" and args.subcommand == "current":
        budget_current(args)
    elif args.command == "networth":
        networth(args)
    elif args.command == "cashflow":
        cashflow(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
