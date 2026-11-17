#!/usr/bin/env python3
r"""反例搜索：对小规模输入空间穷举/随机搜索性质谓词的反例。
用法: python counterexample_search.py <predicate.py> --ranges 0..3 --arity 2 --trials 10000 [--seed 42]
依赖：Python 3 标准库，无第三方依赖；可独立执行。
predicate.py 须定义: def predicate(x: tuple) -> bool  （返回 True 表示性质成立）
输出: 首个反例、反例计数、搜索范围声明。未找到反例不构成证明（范围有限）。
"""
import argparse, importlib.util, itertools, random, sys

def load_predicate(path):
    spec = importlib.util.spec_from_file_location("predicate_mod", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.predicate

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("predicate_file")
    ap.add_argument("--ranges", default="0..3", help="每维取值范围，如 0..3")
    ap.add_argument("--arity", type=int, default=2)
    ap.add_argument("--trials", type=int, default=10000)
    ap.add_argument("--seed", type=int, default=42)
    a = ap.parse_args()
    lo, hi = (int(x) for x in a.ranges.split(".."))
    rng = list(range(lo, hi + 1))
    pred = load_predicate(a.predicate_file)

    total = len(rng) ** a.arity
    found, count = None, 0
    if total <= a.trials:
        space = itertools.product(rng, repeat=a.arity)
        mode = f"穷举 {total} 组合"
    else:
        random.seed(a.seed)
        space = (tuple(random.choice(rng) for _ in range(a.arity)) for _ in range(a.trials))
        mode = f"随机抽样 {a.trials} 次（种子 {a.seed}），全空间 {total} 组合"
    for x in space:
        if not pred(x):
            count += 1
            if found is None:
                found = x
    print(f"搜索方式: {mode}")
    if count:
        print(f"FAIL 发现 {count} 个反例，首个: {found}")
        sys.exit(1)
    print("PASS 未发现反例（注：范围有限，不构成证明）")

if __name__ == "__main__":
    main()
