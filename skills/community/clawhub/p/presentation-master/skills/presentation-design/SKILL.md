---
name: presentation-design
description: 演示设计：视觉层级、信息图表、排版美学、配色方案
source:
  type: derived
  repo: skills-repo/presentation-master
  path: skills/presentation-design/SKILL.md
  url: https://skills.sh/jwynia/agent-skills/presentation-design
  version: 1.0.0
  updated: 2026-07-31
metadata:
  author: hope
  category: 演示
  platform: 通用
  difficulty: 进阶
  version: 1.0.0
  created: 2026-07-31
tags:
  - presentation
  - design
  - visual
  - slides
  - typography
---

# Presentation Design — 演示设计

> 让演示文稿不仅内容好，而且看着专业。覆盖视觉层级、信息图表、排版和配色，从"能用"到"好看"。

## 能力

- **视觉层级**：用大小、颜色、位置建立信息优先级，引导观众视线
- **信息图表**：将数据转化为直观的图表（柱状图、趋势线、对比图），避免信息过载
- **排版美学**：字体搭配、行距字距、文字密度控制，确保可读性
- **配色方案**：基于品牌色或主题色设计配色，确保对比度和视觉一致性
- **Slide 布局**：标题页、内容页、过渡页、总结页的差异化布局设计

## 使用方式

在 Claude Code 中使用 `/presentation-design` 调用。

```
/presentation-design 为这个 Pitch Deck 设计一套配色方案
/presentation-design 把这段数据做成有说服力的图表
/presentation-design 审查这个演示的视觉一致性
/presentation-design 设计一套适合科技产品的 Slide 模板
```

## 工作流

1. **确定风格** — 根据演示场景（路演/汇报/教学）确定视觉风格
2. **设计配色** — 选择主色、辅助色和背景色，确保可读性对比度
3. **信息图表化** — 将文字和数据转化为图表、流程图、时间线
4. **排版优化** — 统一字体、调整间距、控制每页文字量
5. **一致性审查** — 检查所有 Slide 的视觉一致性

## 适用场景

- 投资人路演 Pitch Deck 的视觉设计
- 产品发布会的演示设计
- 季度汇报的数据可视化
- 教学课件的视觉优化

## 限制

- 不涉及 PPT 软件的具体操作技巧
- 复杂动画和多媒体的设计需额外工具支持
- 最终效果依赖演示软件（Keynote/PowerPoint）的渲染能力
- 品牌设计深度参考 visual-designer 仓库

## 相关参考（Playbook）

- [visual-design-principles](../../references/visual-design-principles.md)：字号阶梯、图表选型矩阵、对比度 ≥4.5:1、12 列栅格，量化其「视觉层级 / 配色方案」能力。
- [slide-content-rules](../../references/slide-content-rules.md)：信息密度与排版，与「排版美学」互补。
- 相关资产：[assets/presentation_rules.json](../../assets/presentation_rules.json)（密度 / 对比度阈值源）。