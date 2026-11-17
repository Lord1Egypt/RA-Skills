#!/usr/bin/env python3
"""量纲齐次性校验：检查等式两端 SI 量纲是否一致。
用法: python dimension_check.py --lhs "kg*m/s^2" --rhs "N"
依赖：Python 3 标准库，无第三方依赖；可独立执行。
支持基本量: kg m s A K mol cd，以及导出单位 N J W Pa V C ohm。
"""
import argparse, re, sys

DERIVED = {
    "N": {"kg": 1, "m": 1, "s": -2},
    "J": {"kg": 1, "m": 2, "s": -2},
    "W": {"kg": 1, "m": 2, "s": -3},
    "Pa": {"kg": 1, "m": -1, "s": -2},
    "V": {"kg": 1, "m": 2, "s": -3, "A": -1},
    "C": {"A": 1, "s": 1},
    "ohm": {"kg": 1, "m": 2, "s": -3, "A": -2},
    "T": {"kg": 1, "s": -2, "A": -1},
    "Hz": {"s": -1},
}
BASE = ["kg", "m", "s", "A", "K", "mol", "cd"]

def parse(expr):
    dims = {u: 0 for u in BASE}
    for seg in expr.strip().split("*"):
        for i, tok in enumerate(seg.split("/")):
            sign = 1 if i == 0 else -1
            if not tok or tok == "1":
                continue
            m = re.match(r"^([A-Za-z]+)(?:\^?(-?\d+(?:\.\d+)?))?$", tok)
            if not m:
                return None, f"无法解析因子: {tok}"
            unit, exp = m.group(1), float(m.group(2) or 1) * sign
            if unit not in DERIVED and unit not in BASE:
                return None, f"未知单位: {unit}"
            src = DERIVED.get(unit, {unit: 1})
            for k, v in src.items():
                dims[k] += v * exp
    return {k: v for k, v in dims.items() if abs(v) > 1e-9}, None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lhs", required=True)
    ap.add_argument("--rhs", required=True)
    a = ap.parse_args()
    dl, e1 = parse(a.lhs)
    dr, e2 = parse(a.rhs)
    if e1 or e2:
        print("FAIL", e1 or e2); sys.exit(1)
    if dl == dr:
        print(f"PASS 量纲一致: {dl}")
        sys.exit(0)
    print(f"FAIL 量纲不一致: LHS={dl} RHS={dr}")
    sys.exit(1)

if __name__ == "__main__":
    main()
