#!/usr/bin/env python3
"""
房贷/税费计算器
用法:
  python3 mortgage_calc.py 月供 5000 30 3.9     # 根据月供反推可贷金额
  python3 mortgage_calc.py 贷款 200 30 3.9     # 计算贷款月供
  python3 mortgage_calc.py 总价 200 30 3.9 30  # 计算总价+税费+月供
  python3 mortgage_calc.py 税费 200 90 1 0     # 税费计算
"""

import sys
import math

def calc_monthly_payment(principal: float, years: int, annual_rate: float) -> float:
    """等额本息月供计算"""
    monthly_rate = annual_rate / 100 / 12
    n = years * 12
    if monthly_rate == 0:
        return principal / n
    payment = principal * monthly_rate * (1 + monthly_rate)**n / ((1 + monthly_rate)**n - 1)
    return payment

def calc_total_interest(principal: float, years: int, annual_rate: float) -> float:
    monthly = calc_monthly_payment(principal, years, annual_rate)
    total = monthly * years * 12
    return total - principal

def calc_affordable_household(monthly_income: float, annual_rate: float = 3.9,
                                years: int = 30, down_ratio: float = 0.3) -> dict:
    """计算可负担房屋"""
    # 月供上限 = 月收入 × 40%
    max_monthly = monthly_income * 0.4
    monthly_rate = annual_rate / 100 / 12
    n = years * 12

    # 可贷金额反算
    if monthly_rate > 0:
        affordable_loan = max_monthly * ((1 + monthly_rate)**n - 1) / (monthly_rate * (1 + monthly_rate)**n)
    else:
        affordable_loan = max_monthly * n

    affordable_house = affordable_loan / down_ratio
    return {
        "可贷金额": round(affordable_loan, 2),
        "可负担总价": round(affordable_house, 2),
        "月供上限": round(max_monthly, 2),
        "所需首付": round(affordable_house * down_ratio, 2),
        "总利息": round(affordable_loan - affordable_loan, 2),  # will recalc
    }

def calc_deed_tax(price: float, area: float, is_first: bool,
                   is_new: bool = True, years_owned: int = 0) -> dict:
    """计算房产交易税费"""
    # 契税
    if is_first and area <= 90:
        deed_rate = 0.01
        deed_label = "首套90㎡以下 1%"
    elif is_first and area > 90:
        deed_rate = 0.015
        deed_label = "首套90㎡以上 1.5%"
    elif not is_first and area <= 90:
        deed_rate = 0.01
        deed_label = "二套90㎡以下 1%"
    else:
        deed_rate = 0.02
        deed_label = "二套/非普通住宅 2%"

    deed_tax = price * deed_rate

    # 增值税（增值税附加）
    vat_rate = 0.053
    if years_owned >= 2:
        vat = 0
        vat_label = "满2年，免征增值税"
    else:
        vat = price * vat_rate
        vat_label = f"不满2年，增值税{vat_rate*100:.1f}%"

    # 个税
    if years_owned >= 5:
        # 满五唯一免征
        personal_income = 0
        income_label = "满5唯一住房，免征个税"
    else:
        personal_income = price * 0.01
        income_label = f"非满5唯一，个税1%"

    return {
        "契税": round(deed_tax, 2),
        "契税说明": deed_label,
        "增值税": round(vat, 2),
        "增值税说明": vat_label,
        "个人所得税": round(personal_income, 2),
        "个税说明": income_label,
        "税费合计": round(deed_tax + vat + personal_income, 2),
    }

def mortgage_calc(loan_amount: float, years: int, annual_rate: float):
    """完整房贷计算"""
    monthly = calc_monthly_payment(loan_amount, years, annual_rate)
    total_interest = calc_total_interest(loan_amount, years, annual_rate)
    total = monthly * years * 12

    print(f"\n{'='*45}")
    print(f"  🏦 贷款计算结果")
    print(f"{'='*45}")
    print(f"  贷款金额: {loan_amount:.0f} 万元")
    print(f"  贷款年限: {years} 年 ({years*12} 期)")
    print(f"  年利率:   {annual_rate}%")
    print(f"  还款方式: 等额本息")
    print(f"\n  {'─'*40}")
    print(f"  月供:     {monthly:.2f} 元/月")
    print(f"  总还款:   {total:.2f} 元")
    print(f"  总利息:   {total_interest:.2f} 元")
    print(f"  利息占比: {total_interest/total*100:.1f}%")
    print(f"\n  {'─'*40}")
    print(f"  每月本息分解（前3期示例）：")
    for i in range(1, 4):
        interest = loan_amount * annual_rate/100/12
        principal = monthly - interest
        balance = loan_amount - principal * i
        print(f"    第{i:2d}期: 本金{principal:,.0f}元 + 利息{interest:,.0f}元 = {monthly:,.0f}元 (剩余{balance:,.0f}元)")
    print(f"{'='*45}\n")

def household_calc(monthly_income: float, spouse_income: float = 0,
                  years: int = 30, rate: float = 3.9, down: float = 0.3):
    """家庭可负担计算"""
    total_income = monthly_income + spouse_income
    # 月供上限：总收入×40%（无孩）或×30%（有孩）
    max_monthly = total_income * 0.4
    max_monthly_kid = total_income * 0.3
    monthly_rate = rate / 100 / 12
    n = years * 12

    if monthly_rate > 0:
        loan_40 = max_monthly * ((1+monthly_rate)**n - 1) / (monthly_rate * (1+monthly_rate)**n)
        loan_30 = max_monthly_kid * ((1+monthly_rate)**n - 1) / (monthly_rate * (1+monthly_rate)**n)
    else:
        loan_40 = max_monthly * n
        loan_30 = max_monthly_kid * n

    print(f"\n{'='*50}")
    print(f"  🏠 家庭可负担房屋计算")
    print(f"{'='*50}")
    print(f"  家庭月收入: {total_income:.0f} 元")
    print(f"  月供上限（无孩）: {max_monthly:.0f} 元")
    print(f"  月供上限（有孩）: {max_monthly_kid:.0f} 元")
    print(f"\n  {'─'*47}")
    print(f"  【无孩家庭，月供≤40%】")
    print(f"    可贷金额:    {loan_40/10000:.1f} 万元")
    print(f"    可负担总价:  {loan_40/10000/0.3:.1f} 万元")
    print(f"    所需首付:    {loan_40/10000/0.3*0.3:.1f} 万元")
    print(f"\n  {'─'*47}")
    print(f"  【有孩家庭，月供≤30%】")
    print(f"    可贷金额:    {loan_30/10000:.1f} 万元")
    print(f"    可负担总价:  {loan_30/10000/0.3:.1f} 万元")
    print(f"    所需首付:    {loan_30/10000/0.3*0.3:.1f} 万元")
    print(f"\n  💡 月供{round(loan_30):,}元时的月供构成：")
    monthly = calc_monthly_payment(loan_30/10000*10000, years, rate)
    print(f"     贷款{loan_30/10000*10000/10000:.1f}万，月供{monthly:.0f}元/月")
    # 公积金冲抵估算
    print(f"     若有公积金冲抵2000元/月，实际商贷月供约{monthly-2000:.0f}元")
    print(f"{'='*50}\n")

def tax_calc(price: float, area: float = 90, is_first: bool = True,
             is_new: bool = True, years_owned: int = 0):
    """税费计算"""
    tax = calc_deed_tax(price, area, is_first, is_new, years_owned)
    print(f"\n{'='*45}")
    print(f"  🧾 税费计算结果")
    print(f"{'='*45}")
    print(f"  成交价: {price:.0f} 万元")
    print(f"  面积:   {area:.0f} ㎡")
    print(f"  类型:   {'新房' if is_new else '二手房'}")
    print(f"  买家:   {'首套' if is_first else '二套'}")
    if not is_new:
        print(f"  持有:   {'满'+str(years_owned)+'年' if years_owned >= 2 else '不满'+str(years_owned)+'年'}")
    print(f"\n  {'─'*40}")
    print(f"  契税:        {tax['契税']:>10,.0f} 元  ({tax['契税说明']})")
    if not is_new:
        print(f"  增值税:      {tax['增值税']:>10,.0f} 元  ({tax['增值税说明']})")
        print(f"  个人所得税:  {tax['个人所得税']:>10,.0f} 元  ({tax['个税说明']})")
    # 维修基金（新房）
    if is_new:
        repair = area * 120  # 有电梯标准
        print(f"  维修基金:    {repair:>10,.0f} 元  (有电梯约120/㎡)")
    # 中介费（二手房）
    if not is_new:
        agency = price * 10000 * 0.02  # 2%
        print(f"  中介费:      {agency:>10,.0f} 元  (约2%，可谈)")
    print(f"\n  {'─'*40}")
    print(f"  【税费合计】:  {tax['税费合计']:>8,.0f} 元")
    if not is_new:
        agency = price * 10000 * 0.02
        print(f"  【中介费】:    {agency:>8,.0f} 元")
        print(f"  {'─'*40}")
        print(f"  【总费用】:    {tax['税费合计']+agency:>8,.0f} 元")
        print(f"  (不含首付 {price*10000*0.3/10000:.0f} 万元)")
    print(f"{'='*45}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法:")
        print("  python3 mortgage_calc.py 月供 5000 30 3.9      # 根据月供反推可贷")
        print("  python3 mortgage_calc.py 贷款 100 30 3.9        # 贷款月供计算")
        print("  python3 mortgage_calc.py 家庭 20000 10000 30 3.9  # 家庭可负担")
        print("  python3 mortgage_calc.py 税费 200 90 1 0        # 税费计算")
        print("  python3 mortgage_calc.py 税费 200 90 0 0 1      # 二手房，满1年")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "贷款":
        loan = float(sys.argv[2]) * 10000  # 万元→元
        years = int(sys.argv[3])
        rate = float(sys.argv[4])
        mortgage_calc(loan, years, rate)

    elif cmd == "月供":
        monthly = float(sys.argv[2])
        years = int(sys.argv[3])
        rate = float(sys.argv[4])
        monthly_rate = rate / 100 / 12
        n = years * 12
        loan = monthly * ((1+monthly_rate)**n - 1) / (monthly_rate * (1+monthly_rate)**n)
        print(f"\n  月供 {monthly:.0f}元 × {years}年 = 总还 {monthly*years*12/10000:.1f}万")
        print(f"  可贷金额约: {loan/10000:.1f} 万元")
        print(f"  可购房屋约: {loan/10000/0.3:.1f} 万元（首付30%）\n")
        mortgage_calc(loan, years, rate)

    elif cmd == "家庭":
        income1 = float(sys.argv[2])
        income2 = float(sys.argv[3]) if len(sys.argv) > 3 else 0
        years = int(sys.argv[4]) if len(sys.argv) > 4 else 30
        rate = float(sys.argv[5]) if len(sys.argv) > 5 else 3.9
        household_calc(income1, income2, years, rate)

    elif cmd == "税费":
        price = float(sys.argv[2])  # 万元
        area = float(sys.argv[3]) if len(sys.argv) > 3 else 90
        is_first = int(sys.argv[4]) if len(sys.argv) > 4 else 1
        is_new = int(sys.argv[5]) if len(sys.argv) > 5 else 1
        years_owned = int(sys.argv[6]) if len(sys.argv) > 6 else 0
        tax_calc(price, area, bool(is_first), bool(is_new), years_owned)
