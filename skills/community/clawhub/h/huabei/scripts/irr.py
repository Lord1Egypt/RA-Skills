#!/usr/bin/env python3
"""消费分期真实年化利率(IRR)计算器（零依赖，仅标准库）。

分期"每期费率"具有欺骗性：本金逐月归还但手续费按全额收，
真实年化约为表面年化的 1.8 倍。本工具用 IRR 算真实成本。

用法:
    python3 irr.py fee <本金> <期数> <每期费率%>     # 按每期费率（花呗分期常见）
    python3 irr.py total <本金> <期数> <总手续费>    # 按总手续费
    python3 irr.py daily <日利率万分之几>            # 日利率转年化（借呗常见）

示例:
    python3 irr.py fee 12000 12 0.6    # 12000元分12期，每期费率0.6%
    python3 irr.py daily 5             # 日利率万5
"""
import sys


def irr_monthly(principal: float, months: int, pay_per_month: float) -> float:
    """二分法解每月等额还款的月内部收益率。"""
    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        # 现值 = sum(月供 / (1+r)^k) - 本金
        pv = sum(pay_per_month / (1 + mid) ** k for k in range(1, months + 1))
        if pv > principal:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def show(principal: float, months: int, total_fee: float) -> None:
    pay = (principal + total_fee) / months
    r = irr_monthly(principal, months, pay)
    apr = r * 12 * 100          # 名义年化(月率×12)
    surface = total_fee / principal / months * 12 * 100
    print(f"本金 {principal:.2f} 元，分 {months} 期，总手续费 {total_fee:.2f} 元")
    print(f"每期还款: {pay:.2f} 元")
    print(f"表面年化(费率×12): {surface:.2f}%")
    print(f"真实年化(IRR):     {apr:.2f}%   ← 决策看这个")
    print(f"倍数: {apr / surface:.2f}x" if surface else "")


def main() -> None:
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        sys.exit(1)
    try:
        if a[0] == "fee" and len(a) == 4:
            p, n, rate = float(a[1]), int(a[2]), float(a[3]) / 100
            show(p, n, p * rate * n)
        elif a[0] == "total" and len(a) == 4:
            show(float(a[1]), int(a[2]), float(a[3]))
        elif a[0] == "daily" and len(a) == 2:
            wan = float(a[1])
            print(f"日利率 万{wan:g} = {wan/100:.3f}%/日")
            print(f"年化(单利×365): {wan * 365 / 100:.2f}%")
        else:
            print(__doc__)
            sys.exit(1)
    except ValueError:
        print("参数须为数字", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
