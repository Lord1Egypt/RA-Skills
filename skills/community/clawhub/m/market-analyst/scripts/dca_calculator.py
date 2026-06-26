#!/usr/bin/env python3
"""
DCA Calculator — Calculate monthly accumulation returns
Usage: python3 dca_calculator.py [monthly_vnd] [years]
Example: python3 dca_calculator.py 2000000 10
"""
import sys

def dca_simulate(monthly, annual_return, years):
    monthly_return = (1 + annual_return) ** (1/12) - 1
    total = 0
    for _ in range(years * 12):
        total = (total + monthly) * (1 + monthly_return)
    invested = monthly * 12 * years
    return total, invested

def format_vnd(amount):
    if amount >= 1e9:
        return f"{amount/1e9:.2f} tỷ"
    return f"{amount/1e6:.1f}tr"

def main():
    monthly = float(sys.argv[1]) if len(sys.argv) > 1 else 1_000_000
    years = int(sys.argv[2]) if len(sys.argv) > 2 else 10

    assets = [
        ("Gửi ngân hàng (5.5%)", 0.055),
        ("S&P 500 ETF (18%)", 0.18),
        ("Nikkei 225 (16%)", 0.16),
        ("Vàng (15%/năm est.)", 0.15),
        ("VN Cổ phiếu tốt (25%)", 0.25),
        ("Portfolio mix (22%)", 0.22),
        ("Bitcoin conservative (30%)", 0.30),
    ]

    print(f"\n{'='*65}")
    print(f"  💰 DCA CALCULATOR")
    print(f"  Accumulation: {format_vnd(monthly)}/tháng × {years} năm")
    print(f"  Total invested: {format_vnd(monthly * 12 * years)}")
    print(f"{'='*65}")
    print(f"  {'Asset':<28} {'Result':>10} {'Net profit':>10} {'x Gốc':>8}")
    print(f"  {'-'*60}")

    bank_val = None
    for name, rate in assets:
        val, inv = dca_simulate(monthly, rate, years)
        profit = val - inv
        mult = val / inv
        if name.startswith("Gửi"):
            bank_val = val
        vs_bank = f"(+{format_vnd(val-bank_val)} vs NH)" if bank_val and val > bank_val else ""
        print(f"  {name:<28} {format_vnd(val):>10} {format_vnd(profit):>10} {mult:>7.1f}x  {vs_bank}")

    print(f"\n{'='*65}")
    print(f"  📈 Growth timeline (Portfolio Mix 22%):")
    print(f"  {'Year':>6} {'Invested':>12} {'Result':>12} {'Growth':>12}")
    print(f"  {'-'*50}")
    for yr in [1, 3, 5, 10, 15, 20]:
        if yr <= years + 2:
            val, inv = dca_simulate(monthly, 0.22, yr)
            growth = (val/inv - 1) * 100
            print(f"  {yr:>5} năm  {format_vnd(monthly*12*yr):>12} {format_vnd(val):>12} {growth:>10.0f}%")

    print(f"\n  ⚠️  These are estimates based on history. Not guaranteed returns.")
    print(f"{'='*65}\n")

if __name__ == "__main__":
    main()
