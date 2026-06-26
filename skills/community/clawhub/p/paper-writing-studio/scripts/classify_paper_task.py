#!/usr/bin/env python3
import json
import sys

text = " ".join(sys.argv[1:]).strip()
if not text:
    print(json.dumps({"discipline":"新闻与传播","paper_type":"待确认","stage":"待确认","reason":"no_input"}, ensure_ascii=False))
    sys.exit(0)

paper_type = "待确认"
stage = "待确认"

rules = [
    ("文献综述 研究现状 概念界定 相关研究", "文献综述型论文", "Stage 2"),
    ("研究假设 自变量 因变量 中介 调节 问卷 回归 实证", "定量实证论文", "Stage 3"),
    ("访谈 扎根 质性 定性 田野", "定性研究论文", "Stage 3"),
    ("内容分析 编码 类目 框架分析 叙事分析 样本", "内容分析论文", "Stage 3"),
    ("案例研究 个案 传播机制 出圈 路径", "案例研究论文", "Stage 3"),
    ("结论 不足 展望 启示", "待确认", "Stage 5"),
    ("选题 题目 研究意义 值不值得做", "待确认", "Stage 1"),
    ("结果分析 研究发现 数据解释", "待确认", "Stage 4"),
]

for keywords, ptype, stg in rules:
    if any(k in text for k in keywords.split()):
        if ptype != "待确认":
            paper_type = ptype
        stage = stg
        break

print(json.dumps({
    "discipline": "新闻与传播",
    "paper_type": paper_type,
    "stage": stage,
    "input": text
}, ensure_ascii=False))
