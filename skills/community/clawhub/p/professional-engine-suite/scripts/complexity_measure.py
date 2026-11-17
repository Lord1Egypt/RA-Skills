#!/usr/bin/env python3
r"""复杂度实测：对函数在不同规模下计时并估计增长阶。
用法: python complexity_measure.py <impl.py> --func bsearch --sizes 1000,2000,4000,8000 [--reps 200]
依赖：Python 3 标准库，无第三方依赖；可独立执行。
impl.py 须定义: make_input(n) -> 任意输入 和 被测函数 func(input)（单参数）。
输出: 各规模耗时、log-log 回归指数、估计的复杂度阶。实测受环境（硬件/解释器）影响，须标注。
"""
import argparse, importlib.util, math, sys, time

def load(path):
    spec = importlib.util.spec_from_file_location("impl_mod", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("impl_file")
    ap.add_argument("--func", required=True)
    ap.add_argument("--sizes", default="1000,2000,4000,8000")
    ap.add_argument("--reps", type=int, default=200)
    a = ap.parse_args()
    mod = load(a.impl_file)
    fn = getattr(mod, a.func)
    sizes = [int(x) for x in a.sizes.split(",")]
    xs, ys = [], []
    for n in sizes:
        data = mod.make_input(n)
        best = float("inf")
        for _ in range(3):
            t0 = time.perf_counter()
            for _ in range(a.reps):
                fn(data)
            dt = (time.perf_counter() - t0) / a.reps
            best = min(best, dt)
        xs.append(math.log(n)); ys.append(math.log(max(best, 1e-9)))
        print(f"n={n:>8}  平均耗时={best*1e6:10.2f} µs")
    m = len(xs); xbar = sum(xs)/m; ybar = sum(ys)/m
    slope = sum((x-xbar)*(y-ybar) for x, y in zip(xs, ys)) / sum((x-xbar)**2 for x in xs)
    label = ("O(1)" if slope < 0.15 else "O(log n)" if slope < 0.5 else
             "O(n log n) 附近" if slope < 1.35 else "O(n)" if slope < 1.6 else
             "O(n²) 附近" if slope < 2.4 else f"≈O(n^{slope:.1f})")
    print(f"log-log 回归指数≈{slope:.2f} → 估计阶: {label}")
    print("注：实测受硬件/解释器影响，须随结果标注环境；理论阶以推导为准")

if __name__ == "__main__":
    main()
