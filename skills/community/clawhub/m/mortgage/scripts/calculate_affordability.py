#!/usr/bin/env python3
"""Calculate home affordability."""
import json
import os
import argparse

MORTGAGE_DIR = os.path.expanduser("~/.openclaw/workspace/memory/mortgage")

def ensure_dir():
    os.makedirs(MORTGAGE_DIR, exist_ok=True)

def main():
    parser = argparse.ArgumentParser(description='Calculate home affordability')
    parser.add_argument('--income', type=float, required=True, help='Annual gross income')
    parser.add_argument('--debts', type=float, default=0, help='Monthly debt payments')
    parser.add_argument('--down-payment', type=float, default=0, help='Down payment amount')
    
    args = parser.parse_args()
    
    monthly_income = args.income / 12
    
    # 28% rule for housing payment
    max_housing_payment = monthly_income * 0.28
    
    # 36% rule for total debt
    max_total_debt = monthly_income * 0.36
    max_mortgage_payment = max_total_debt - args.debts
    
    # Use the more conservative of the two
    affordable_payment = min(max_housing_payment, max_mortgage_payment)
    
    # Estimate mortgage amount (rough calculation at 7% interest, 30 years)
    # Monthly payment = P * (r(1+r)^n) / ((1+r)^n - 1)
    # Simplified: roughly $150/month per $25K borrowed at 7%
    estimated_loan = (affordable_payment / 150) * 25000
    
    # Add down payment for total home price
    affordable_price = estimated_loan + args.down_payment
    
    print("\n🏠 HOME AFFORDABILITY ESTIMATE")
    print("=" * 50)
    print(f"Annual Income: ${args.income:,.2f}")
    print(f"Monthly Income: ${monthly_income:,.2f}")
    print(f"Monthly Debts: ${args.debts:,.2f}")
    print(f"Down Payment: ${args.down_payment:,.2f}")
    print()
    print(f"Max Housing Payment (28% rule): ${max_housing_payment:,.2f}")
    print(f"Max Mortgage Payment (36% rule): ${max_mortgage_payment:,.2f}")
    print()
    print(f"✓ Recommended Payment: ${affordable_payment:,.2f}/month")
    print(f"✓ Estimated Home Price: ${affordable_price:,.0f}")
    print()
    print("⚠️  This is an estimate only. Actual affordability depends on:")
    print("   - Credit score and interest rates")
    print("   - Property taxes and insurance")
    print("   - HOA fees and other costs")
    print("   - Lender qualification requirements")

if __name__ == '__main__':
    main()
