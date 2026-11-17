#!/usr/bin/env python3
r"""货币时间价值计算：现值/终值/年金/名义实际换算（投资册工具）。
用法: python tvm_calc.py pv --fv 1000000 --rate 0.05 --years 3 [--m 12]
      python tvm_calc.py fv --pv 1000000 --rate 0.05 --years 3
      python tvm_calc.py annuity --pmt 10000 --rate 0.05 --years 10 [--due]
      python tvm_calc.py fisher --nominal 0.05 --inflation 0.02
依赖：Python 3 标准库，无第三方依赖；可独立执行。
输出: 计算结果；计息约定（年计息/月计息/连续复利）须与报告约定一致。
"""
import argparse

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["pv", "fv", "annuity", "fisher"])
    ap.add_argument("--pv", type=float, default=None)
    ap.add_argument("--fv", type=float, default=None)
    ap.add_argument("--pmt", type=float, default=None)
    ap.add_argument("--rate", type=float, required=True)
    ap.add_argument("--years", type=float, default=None)
    ap.add_argument("--m", type=int, default=1, help="年计息次数（1=年计息）")
    ap.add_argument("--due", action="store_true", help="预付年金")
    ap.add_argument("--nominal", type=float, default=None)
    ap.add_argument("--inflation", type=float, default=None)
    a = ap.parse_args()
    if a.mode == "pv":
        r = a.rate / a.m
        v = a.fv / (1 + r) ** (a.years * a.m)
        print(f"PV = {a.fv}/(1+{a.rate}/{a.m})^({a.years}×{a.m}) = {v:.2f}")
    elif a.mode == "fv":
        r = a.rate / a.m
        v = a.pv * (1 + r) ** (a.years * a.m)
        print(f"FV = {a.pv}×(1+{a.rate}/{a.m})^({a.years}×{a.m}) = {v:.2f}")
    elif a.mode == "annuity":
        r, n = a.rate, a.years
        v = a.pmt * (1 - (1 + r) ** -n) / r * (1 + r if a.due else 1)
        print(f"年金现值({'预付' if a.due else '普通'}, r={r}, n={n}) = {v:.2f}")
    else:
        real = (1 + a.nominal) / (1 + a.inflation) - 1
        print(f"实际利率（费雪）= (1+{a.nominal})/(1+{a.inflation})-1 = {real:.4f}")
        print("通胀假设须随报告标注；名义/实际口径全程一致")

if __name__ == "__main__":
    main()
