---
name: "hopola-search"
description: "执行网页检索与信息提炼。Invoke when user asks for trend research, source collection, or evidence grounding before generation."
---

# Hopola Search

## 作用
负责完成网页检索、来源筛选、事实提炼，为后续生成阶段提供可引用信息。

## 触发时机
- 需要先搜集事实再生图/生视频/生成3D。
- 需要给报告提供可追溯来源摘要。

## 输入
- `query`
- `search_scope`
- `max_sources`

## 输出
- `summary`
- `sources`
- `key_points`

## 规则
- 优先使用 web-access 的策略化检索与读取能力。
- 结果需可追溯，保留标题、链接、摘要。
- 输出采用结构化字段，供主技能拼装 Markdown。
