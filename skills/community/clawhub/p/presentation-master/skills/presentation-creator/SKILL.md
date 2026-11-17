---
name: presentation-creator
description: 演示创建：大纲构思、内容组织、Slide 编写、全流程
source:
  type: derived
  repo: skills-repo/presentation-master
  path: skills/presentation-creator/SKILL.md
  url: https://skills.sh/getsentry/skills/presentation-creator
  version: 1.0.0
  updated: 2026-07-31
metadata:
  author: hope
  category: 演示
  platform: 通用
  difficulty: 入门
  version: 1.0.0
  created: 2026-07-31
tags:
  - presentation
  - content
  - slides
  - outline
  - storytelling
---

# Presentation Creator — 演示创建

> 从零开始创建完整的演示文稿。覆盖大纲构思、内容组织、Slide 编写和全流程管理，帮你高效产出专业演示。

## 能力

- **大纲构思**：根据演示目标和受众，设计 Slide-by-Slide 大纲
- **内容组织**：将复杂信息分解为清晰的 Slide 单元，每页一个核心信息点
- **Slide 编写**：为每页撰写精炼的标题、要点和备注，控制信息密度
- **故事线**：贯穿全篇的叙事线索，确保逻辑连贯和信息递进
- **全流程管理**：从初稿到终稿的迭代优化，适应不同时间限制（5 分钟/15 分钟/30 分钟）

## 使用方式

在 Claude Code 中使用 `/presentation-creator` 调用。

```
/presentation-creator 帮我写一个 10 页的产品发布会演示
/presentation-creator 为这个季度汇报创建 Slide 大纲
/presentation-creator 把这个技术文档改成面向客户的演示
/presentation-creator 把我的 30 分钟演讲压缩成 5 分钟的 Lightning Talk
```

## 工作流

1. **需求分析** — 明确演示目标、受众、时长和场合
2. **大纲设计** — 创建 Slide-by-Slide 大纲，标注每页目标
3. **内容编写** — 为每页撰写标题、要点和备注脚本
4. **故事线检查** — 验证逻辑连贯性、信息递进和行动号召
5. **迭代优化** — 根据反馈调整内容、精简冗余、强化核心信息

## 适用场景

- 产品发布会和 Demo Day 演示
- 投资人路演和融资 Pitch
- 团队周报和季度汇报
- 技术分享和会议演讲

## 限制

- 不涉及 Slide 的视觉设计（参考 presentation-design）
- 不涉及 PPT 模板制作（参考 ppt-template-creator）
- 内容质量取决于输入信息的完整性
- 行业特定术语和概念需要你自己补充

## 相关参考（Playbook）

- [deck-structure-playbook](../../references/deck-structure-playbook.md)：用时长倒推页数、四段法骨架、每页一主张、钩子/CTA 模板。
- [slide-content-rules](../../references/slide-content-rules.md)：每页字数红线（标题 20 / 内容 120 / 图表 60 / 收尾 40）、标题层级统一、要点化密度。
- 相关资产：[assets/presentation-outline.example.md](../../assets/presentation-outline.example.md)（示例大纲）、[assets/presentation_rules.json](../../assets/presentation_rules.json)（密度阈值源）。