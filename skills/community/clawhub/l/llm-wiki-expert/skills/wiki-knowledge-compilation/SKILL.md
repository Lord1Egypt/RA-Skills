---
name: wiki-knowledge-compilation
description: 把 raw 来源编译为概念、实体、摘要、解释和决策页面，并维护可导航的索引与链接图。
source:
  type: derived
  repo: skills-repo/llm-wiki-expert
  path: skills/wiki-knowledge-compilation/SKILL.md
  version: 1.0.0
  updated: 2026-08-14
  url: https://skills.sh/astro-han/karpathy-llm-wiki/karpathy-llm-wiki
metadata:
  category: 知识编译
  platform: Markdown
  difficulty: 专家
---

# Wiki 知识编译

> 来源按“从哪里来”保存，知识按“用户要理解什么”重新组织。

## 能力

- 将单份或多份来源拆解为概念、实体、解释、决策和来源摘要页面。
- 依据核心命题判断合并、拆分、交叉引用或新建页面。
- 把 Tutorial、How-to、Reference、Explanation 等不同用户需求分开表达。
- 维护索引、反向链接、页面状态和来源字段的一致性。

## 使用方式

```text
/wiki-knowledge-compilation 编译刚加入的三份来源，先给页面影响计划
/wiki-knowledge-compilation 拆分这个超长页面并修复索引和交叉链接
```

先读取 `../../references/information-architecture-playbook.md` 和 `../../references/source-grounding-playbook.md` 中与当前页面类型相关的段落。

## 工作流

1. **读取宪章** — 确认范围、页面类型、命名与来源政策。
2. **影响分析** — 搜索来源实体、别名和关键主张，列出新建/更新/冲突页面。
3. **选择页面类型** — 同一核心命题合并，新概念新建，不同用户任务拆页。
4. **定位证据** — 精确数字、日期、引语写入前先在 raw 中定位。
5. **编写与链接** — 使用 `assets/article.template.md`，补齐 Sources、Related 和 Status。
6. **级联更新** — 修订所有受影响非归档页面；旧结论标 Outdated/Disputed，不静默改写。
7. **更新索引和日志** — 每页只在 index 出现一次，并记录本次编译的页面集合。
8. **机械验证** — 运行 `build_manifest.py` 和 `audit_wiki.py`；人工判断脚本报告的语义问题。

## 适用场景

- 将新来源融入现有知识，而不是只生成一篇孤立摘要。
- 页面过长、重复或混合了教程、参考和解释内容。
- 多来源支持或反驳同一主张，需要显式证据结构。
- 重建 Wiki 的概念树、实体页和入口索引。

## 限制

- 不将无法定位的精确事实写成确定结论。
- 不为了链接密度创建空壳页；缺失概念先进入 backlog。
- 不自动裁决来源冲突；只呈现证据、时间和适用条件。
