---
name: "Webflow"
category: "Design & Creative"
description: "Visual web builder. Blue-accented, polished marketing site aesthetic."
colors:
  primary: "#ed52cb"
  secondary: "#222222"
  accent: "#4353FF"
  background: "#ff6b00"
  surface: "#F8F9FA"
  muted: "#222222"
  border: "#d8d8d8"
typography:
  display:
    fontFamily: WF Visual Sans Variable
    fontSize: 3rem
    fontWeight: 600
    letterSpacing: -0.02em
  body:
    fontFamily: WF Visual Sans Variable
    fontSize: 1rem
    fontWeight: 400
  mono:
    fontFamily: ui-monospace, monospace
    fontSize: 0.875rem
rounded:
  sm: 4px
  md: 8px
  lg: 16px
spacing:
  sm: 6px
  md: 12px
  lg: 24px
ppt:
  scenes: ["设计提案", "科技主题演讲"]
  posture: "平衡"
  accentBudget: 2
---

## Overview
Webflow's website is a visually rich, tool-forward platform that communicates "design without code" through clean white surfaces, the signature Webflow Blue ...

## Colors
primary(`#ed52cb`)标题 | accent(`#4353FF`)强调 | bg(`#ff6b00`)底色 | surface(`#F8F9FA`)卡片

## Typography
Display: Inter | Body: Inter | Mono: Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 80px | 600 | 1.04 | -0.8px | 首页主标题 |
| 章节标题 | 56px | 600 | 1.04 | normal | 分章标题 |
| 卡片标题 | 32px | 500 | 1.30 | normal | 内容卡标题 |
| 正文 | 20px | 400 | 1.40 | normal | 主要阅读 |
| 辅助文字 | 14px | 400 | 1.40 | normal | 标注/脚注 |
| 数据标签 | 10px | 500 | 1.30 | 1px | 图表标签 |

## Layout & Shapes
间距风格平衡，圆角直角/极小圆角。 小圆角矩形，保持克制的几何感。

## Elevation
扁平，不使用阴影。

## Components
标题卡(accent左边框) | 数据卡(surface底+数字突出) | 引用块(muted底+斜体)

## Do's and Don'ts
✅ accent≤2处/页，大面积留白 | ❌ 禁混用3+强调色，禁过度装饰

## Agent Prompt Guide

### 快速色板
- 标题: `#ed52cb` | 正文: `#222222` | 强调: `#4353FF`
- 底色: `#ff6b00` | 卡片: `#F8F9FA` | 边框: `#d8d8d8`

### SVG 组件示例
- "封面：`#ff6b00`底，标题48px WF Visual Sans Variable weight 600，色`#ed52cb`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#F8F9FA`底+`#d8d8d8`边框+8px圆角。标题24px weight 500 色`#ed52cb`。正文18px weight 400 色`#222222`。"

### 品牌铁律
1. 强调色(`#4353FF`)每页不超过2处使用
2. 排版层次清晰，标题与正文对比明确
3. 保持品牌调性一致，避免混用风格
