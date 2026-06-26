#!/usr/bin/env python3
import json
import sys

stage = (sys.argv[1] if len(sys.argv) > 1 else "").strip().lower()

checklists = {
    "stage 1": ["明确研究对象", "列出3-5个选题", "补现实问题背景", "补学术问题", "论证研究意义"],
    "stage 2": ["建立关键词池", "扩展中英文文献", "整理文献矩阵", "完成概念界定", "写研究不足"],
    "stage 3": ["明确研究问题", "提出假设/分析维度", "定义变量或类目", "设计方法与样本", "写技术路线"],
    "stage 4": ["整理结果/发现", "按问题写分析", "解释图表或编码结果", "回扣研究问题", "提炼阶段结论"],
    "stage 5": ["总结核心结论", "写理论与实践意义", "写研究不足", "写未来展望", "整理摘要素材"]
}

items = checklists.get(stage, ["先判断阶段", "补充缺失信息", "确定本轮目标"])
print(json.dumps({"stage": stage or "unknown", "checklist": items}, ensure_ascii=False))
