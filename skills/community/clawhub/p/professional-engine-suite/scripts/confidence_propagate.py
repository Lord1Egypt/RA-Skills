#!/usr/bin/env python3
"""置信度传播计算：链可信度 = 最弱一环。
用法: python confidence_propagate.py A A B A C
依赖：Python 3 标准库，无第三方依赖；可独立执行。
输出: 最终置信等级与最弱环节位置。
"""
import sys

RANK = {"A": 3, "B": 2, "C": 1}
LABEL = {"A": "公理段", "B": "经验段", "C": "估算段"}

def main():
    steps = [s.strip().upper() for s in sys.argv[1:]]
    if not steps or any(s not in RANK for s in steps):
        print("用法: python confidence_propagate.py <各步置信标，如 A A B A C>")
        sys.exit(2)
    weakest = min(steps, key=lambda s: RANK[s])
    idx = [i + 1 for i, s in enumerate(steps) if s == weakest]
    print(f"最终置信: {weakest}（{LABEL[weakest]}）")
    print(f"最弱环节: 第 {', '.join(map(str, idx))} 步")
    if weakest == "C":
        print("提示: 含 C 级段，交付时必须标注'实验范围外不可外推'")

if __name__ == "__main__":
    main()
