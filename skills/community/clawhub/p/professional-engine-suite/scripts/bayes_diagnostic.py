#!/usr/bin/env python3
r"""诊断统计计算：敏感度/特异度/似然比/验前验后概率（医学册工具）。
用法: python bayes_diagnostic.py --tp 90 --fn 10 --fp 40 --tn 860 [--prevalence 0.10]
依赖：Python 3 标准库，无第三方依赖；可独立执行。
输出: 四格表指标、似然比、验后概率（验前概率来源须由使用者标注于报告）。
"""
import argparse

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tp", type=float, required=True)
    ap.add_argument("--fn", type=float, required=True)
    ap.add_argument("--fp", type=float, required=True)
    ap.add_argument("--tn", type=float, required=True)
    ap.add_argument("--prevalence", type=float, default=None)
    a = ap.parse_args()
    sens = a.tp / (a.tp + a.fn) if (a.tp + a.fn) else float("nan")
    spec = a.tn / (a.tn + a.fp) if (a.tn + a.fp) else float("nan")
    acc = (a.tp + a.tn) / (a.tp + a.fn + a.fp + a.tn)
    lr_pos = sens / (1 - spec) if spec != 1 else float("inf")
    lr_neg = (1 - sens) / spec if spec != 0 else float("inf")
    print(f"敏感度={sens:.4f}  特异度={spec:.4f}  准确度={acc:.4f}")
    print(f"LR+={lr_pos:.3f}  LR-={lr_neg:.3f}")
    if a.prevalence is not None:
        p = a.prevalence
        odds_pre = p / (1 - p)
        odds_post = odds_pre * lr_pos
        post = odds_post / (1 + odds_post)
        print(f"验前概率={p:.3f}（来源须由报告标注）→ 阳性后验后概率={post:.4f}")
        print("注：群体患病率≠个体概率（G-Med5），本值仅作换算示例")

if __name__ == "__main__":
    main()
