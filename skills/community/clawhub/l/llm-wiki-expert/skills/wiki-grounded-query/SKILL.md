---
name: wiki-grounded-query
description: 使用索引、全文检索与可选语义召回回答问题，给出 Wiki 页面依据、原始来源和明确知识缺口。
source:
  type: derived
  repo: skills-repo/llm-wiki-expert
  path: skills/wiki-grounded-query/SKILL.md
  version: 1.0.0
  updated: 2026-08-14
  url: https://skills.sh/astro-han/karpathy-llm-wiki/karpathy-llm-wiki
metadata:
  category: 有据查询
  platform: 通用
  difficulty: 专家
---

# Wiki 有据查询

> 回答“这个 Wiki 知道什么”，而不是让模型用训练记忆补齐它不知道的部分。

## 能力

- 将问题扩展为实体、别名、同义词、版本和时间约束。
- 按 Index → 全文 → 链接邻居 → 可选语义检索逐级召回。
- 综合一致、冲突和过期来源，给出页面级与原始来源级依据。
- 将一次性答案与值得晋升的长期知识区分开。

## 使用方式

```text
/wiki-grounded-query 根据 Wiki 比较 Cordis 与 OSGi 的动态组件模型
/wiki-grounded-query 这个结论在库里有哪些支持、反例和过期证据？
```

执行前读取 `../../references/retrieval-and-synthesis-playbook.md`。默认只读；除非用户明确要求归档或晋升，不修改 Wiki。

## 工作流

1. **解析问题** — 明确主体、时间、比较维度、期望证据与允许的外部知识边界。
2. **检索候选** — 先读 `wiki/index.md`，再用 `rg` 搜实体、别名和主张。
3. **扩展邻居** — 只跟随与问题相关的一层链接，避免无界图遍历。
4. **评估证据** — 检查页面状态、更新时间、来源数量、冲突和适用范围。
5. **综合回答** — 区分“Wiki 明确支持”“合理推断”“库内未知”，逐项引用页面。
6. **回到原始来源** — 高风险或精确主张继续链接到 raw，不只引用二次页面。
7. **决定留存** — 一次性输出写 `outputs/queries/`；可复用新综合经审核后晋升页面。

## 适用场景

- 基于个人或团队 Wiki 做比较、综述、时间线和决策准备。
- 检查某结论是否有来源、是否存在反例或已经过期。
- 建立查询评测集，验证全文或语义检索召回效果。
- 将高质量综合变成可复用解释页。

## 限制

- 不将模型训练知识混入 Wiki 事实；若补充外部知识必须单独标记。
- 不因一次零结果就宣布不存在，至少完成索引和全文两种检索。
- 不自动把每个答案写回 Wiki，防止自我引用和低价值内容膨胀。
