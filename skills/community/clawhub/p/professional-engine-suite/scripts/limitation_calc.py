#!/usr/bin/env python3
r"""诉讼时效与期间计算（法律册工具）。
用法: python limitation_calc.py --start 2025-06-30 --years 3 [--interrupt 2026-01-15,2027-03-01]
依赖：Python 3 标准库，无第三方依赖；可独立执行。
输出: 期间届满日（按中断事件顺延）；期间依据须由报告核对现行法版本（G-Law1）。
"""
import argparse
from datetime import date, timedelta

def parse(s):
    y, m, d = (int(x) for x in s.split("-"))
    return date(y, m, d)

def add_years(d, years):
    try:
        return d.replace(year=d.year + years)
    except ValueError:
        return d.replace(year=d.year + years, day=28)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", required=True, help="起算日 YYYY-MM-DD")
    ap.add_argument("--years", type=float, default=3.0)
    ap.add_argument("--interrupt", default="", help="中断事件日期列表，逗号分隔（中断后重新起算）")
    a = ap.parse_args()
    cur = parse(a.start)
    events = [e.strip() for e in a.interrupt.split(",") if e.strip()]
    print(f"起算日: {cur}（起算规则见 [LR-02]，须核现行法版本）")
    base_years = int(a.years)
    expires = add_years(cur, base_years) + timedelta(days=(a.years - base_years) * 365)
    for e in events:
        ed = parse(e)
        print(f"中断事件 {ed} → 自中断事由终止之日重新起算（此处按中断日近似）")
        expires = add_years(ed, base_years) + timedelta(days=(a.years - base_years) * 365)
    print(f"期间届满日（近似）: {expires}（{a.years} 年）")
    print("注：中断/中止、最长保护期间等规则须逐项核对；本计算不构成法律意见")
if __name__ == "__main__":
    main()
