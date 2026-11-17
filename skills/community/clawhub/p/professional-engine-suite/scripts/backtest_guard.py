#!/usr/bin/env python3
r"""回测检查：过拟合与偏差扫描（投资册工具）。
用法: python backtest_guard.py --returns "0.01,0.02,-0.01,0.03,..." [--folds 5] [--params 3]
依赖：Python 3 标准库，无第三方依赖；可独立执行。
输出: 样本内/外分割统计差、参数数-样本量比警戒、幸存者偏差与窗口敏感提示。
"""
import argparse, statistics

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--returns", required=True, help="收益率序列，逗号分隔")
    ap.add_argument("--folds", type=int, default=5, help="样本外折数")
    ap.add_argument("--params", type=int, default=0, help="策略参数个数（过拟合警戒）")
    a = ap.parse_args()
    xs = [float(x) for x in a.returns.split(",")]
    n = len(xs)
    if n < a.folds * 2:
        print("FAIL 样本量过小，无法做有意义的样本外分割"); return
    fold = n // a.folds
    in_sample, out_sample = [], []
    for i in range(a.folds):
        seg = xs[i * fold:(i + 1) * fold]
        (out_sample if i % 2 else in_sample).extend(seg)
    def stats(d):
        mean = statistics.mean(d); sd = statistics.pstdev(d) or 1e-9
        return mean, sd, mean / sd
    mi, si, shi = stats(in_sample)
    mo, so, sho = stats(out_sample)
    print(f"样本内: μ={mi:.4f} σ={si:.4f} 夏普(近似)={shi:.2f}")
    print(f"样本外: μ={mo:.4f} σ={so:.4f} 夏普(近似)={sho:.2f}")
    decay = (shi - sho) / abs(shi) if shi else float("inf")
    print(f"夏普衰减率: {decay:.1%} → {'警戒：疑似过拟合' if decay > 0.5 else '未见显著衰减'}")
    if a.params > 0 and a.params * 10 > n:
        print(f"FAIL 参数数({a.params})×10 > 样本量({n})，过拟合风险高（G-Inv3）")
    print("提示：检查幸存者偏差（股票池是否剔除退市）；窗口敏感性（换窗口重算）；相关≠因果（G-Inv1/G-Inv5）")
    print("声明：本检查仅做统计提示，样本外验证缺失时结论必须降级标注")

if __name__ == "__main__":
    main()
