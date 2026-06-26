---
title: report-creator 技术使用说明
theme: dark-tech
author: 技术团队
date: 2024-10-08
lang: zh
abstract: report-creator Skill 的完整使用说明，包含 IR 格式规范、CLI 接口和 Agent 集成指南。
---

## 系统架构

:::diagram type=sequence
actors: [用户/Agent, Claude, 文件系统]
steps:
  - from: 用户/Agent
    to: Claude
    msg: /report --plan "季度报告"
  - from: Claude
    to: 文件系统
    msg: 写入 report.report.md
  - from: 用户/Agent
    to: Claude
    msg: /report --generate report.report.md
  - from: Claude
    to: 文件系统
    msg: 写入 report.html
:::

## 快速开始

:::code lang=bash title=基本用法
# 两步式（推荐）
/report --plan "2024年度技术复盘"
/report --generate report-2024.report.md

# 一步直出
/report "产品上线后30天数据报告"

# 指定主题
/report --theme minimal "市场调研报告"
:::

## 支持的组件

:::list
- `:::kpi` — KPI指标卡，支持滚动计数动画
- `:::chart` — 图表（bar/line/pie/scatter/radar）
- `:::table` — 数据表格
- `:::timeline` — 时间轴 / 里程碑
- `:::diagram` — 序列图/流程图/树图（SVG）
- `:::code` — 语法高亮代码块
- `:::callout` — 提示/警告块（note/tip/warning/danger）
- `:::image` — 图文混排（left/right/full）
:::

## 注意事项

:::callout type=danger
`--bundle` 模式会将所有外部库内联到 HTML 中，文件体积可能达到 2-4MB。仅在需要完全离线运行时使用。
:::

:::callout type=note
当作为 Agent 下游节点使用时，上游 Agent 只需将 IR 内容放入 context，然后调用 `/report --generate` 即可完成渲染，无需额外传参。
:::
