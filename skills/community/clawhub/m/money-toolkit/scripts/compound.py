#!/usr/bin/env python3
"""复利计算器"""
import sys

def compound(principal, monthly, annual_rate, years):
    """Calculate compound interest with monthly contributions."""
    monthly_rate = annual_rate / 100 / 12
    months = years * 12
    
    # FV = P(1+r)^n + PMT * ((1+r)^n - 1) / r
    fv_lump = principal * (1 + monthly_rate) ** months
    if monthly_rate > 0:
        fv_pmt = monthly * ((1 + monthly_rate) ** months - 1) / monthly_rate
    else:
        fv_pmt = monthly * months
    
    future_value = fv_lump + fv_pmt
    total_invested = principal + monthly * months
    total_earnings = future_value - total_invested
    
    print(f"💰 复利计算结果")
    print(f"  本金: ¥{principal:,.0f}")
    print(f"  每月定投: ¥{monthly:,.0f}")
    print(f"  年化收益率: {annual_rate}%")
    print(f"  投资年限: {years}年")
    print(f"  {'─'*40}")
    print(f"  总投入: ¥{total_invested:,.0f}")
    print(f"  终值:   ¥{future_value:,.0f}")
    print(f"  收益:   ¥{total_earnings:,.0f} ({total_earnings/total_invested*100:.1f}%)" if total_invested > 0 else "")
    
    # FIRE number
    if annual_rate > 0:
        fire_number = 25 * (monthly * 12)  # 4% rule
        years_to_fire = 0
        if monthly_rate > 0:
            from math import log
            n = log(1 + fire_number * monthly_rate / monthly) / log(1 + monthly_rate)
            years_to_fire = n / 12
        print(f"  {'─'*40}")
        print(f"  🔥 FIRE目标: ¥{fire_number:,.0f}")
        print(f"  ⏱️ 达到FIRE需: {years_to_fire:.1f}年")

def main():
    args = sys.argv[1:]
    if len(args) < 3:
        print("复利计算器: compound.py <本金> <每月定投> <年化%> [年限]")
        print("例: compound.py 10000 1000 12 10")
        return
    
    principal = float(args[0])
    monthly = float(args[1])
    rate = float(args[2])
    years = int(args[3]) if len(args) > 3 else 10
    
    compound(principal, monthly, rate, years)

if __name__ == '__main__':
    main()
