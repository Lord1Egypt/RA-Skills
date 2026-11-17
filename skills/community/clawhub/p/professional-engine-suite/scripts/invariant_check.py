#!/usr/bin/env python3
r"""不变量轨迹校验：对执行轨迹逐状态校验不变量集。
用法: python invariant_check.py <trace.json> <invariants.py>
依赖：Python 3 标准库，无第三方依赖；可独立执行。
trace.json: [{"lo":0,"hi":9}, ...]（状态序列，每个状态为 dict）
invariants.py 须定义: INVARIANTS = [("区间合法性", lambda s: 0 <= s["lo"]), ...]
输出: 逐状态结果；首个违规状态与索引；违规即停。
"""
import importlib.util, json, sys

def load_invariants(path):
    spec = importlib.util.spec_from_file_location("inv_mod", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.INVARIANTS

def main():
    if len(sys.argv) != 3:
        print("用法: python invariant_check.py <trace.json> <invariants.py>"); sys.exit(2)
    trace = json.load(open(sys.argv[1], encoding="utf-8"))
    invariants = load_invariants(sys.argv[2])
    for i, state in enumerate(trace):
        for name, fn in invariants:
            if not fn(state):
                print(f"FAIL 第 {i} 状态违规: {name}  状态={state}")
                sys.exit(1)
    print(f"PASS 轨迹 {len(trace)} 个状态 × {len(invariants)} 项不变量，全部通过")

if __name__ == "__main__":
    main()
