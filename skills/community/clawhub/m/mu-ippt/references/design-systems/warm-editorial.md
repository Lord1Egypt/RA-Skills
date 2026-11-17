---
name: "Warm Editorial"
category: "Starter"
description: "A serif-led magazine aesthetic. Terracotta accent on warm off-white paper —"
colors:
  primary: "#1C1A17"
  secondary: "#8A817A"
  accent: "#C0512F"
  background: "#FAF7F2"
  surface: "#FFFFFF"
  muted: "#8A817A"
  border: "#E5E7EB"
typography:
  display:
    fontFamily: system-ui, sans-serif
    fontSize: 3rem
    fontWeight: 600
    letterSpacing: -0.02em
  body:
    fontFamily: system-ui, sans-serif
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
  sm: 8px
  md: 16px
  lg: 32px
ppt:
  scenes: ["品牌演示", "科技主题演讲"]
  posture: "宽松"
  accentBudget: 2
---

## Overview
衬线主导的杂志美学，赤陶色accent点缀暖白纸面，营造编辑质感。

## Colors
primary(`#1C1A17`)标题 | accent(`#C0512F`)强调 | bg(`#FAF7F2`)底色 | surface(`#FFFFFF`)卡片

## Typography
Display: Inter | Body: Inter | Mono: Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 48px | 600 | 1.0 | -1.0px | 首页主标题 |
| 章节标题 | 32px | 500 | 1.1 | -0.5px | 分章标题 |
| 卡片标题 | 24px | 500 | 1.2 | -0.2px | 内容卡标题 |
| 正文 | 18px | 400 | 1.5 | normal | 主要阅读 |
| 辅助文字 | 14px | 400 | 1.4 | normal | 标注/脚注 |
| 数据标签 | 12px | 500 | 1.3 | normal | 图表标签 |

## Layout & Shapes
间距风格宽松，圆角小圆角（4-8px）。 小圆角矩形，保持克制的几何感。

## Elevation
扁平，不使用阴影。

## Components
标题卡(accent左边框) | 数据卡(surface底+数字突出) | 引用块(muted底+斜体)

## Do's and Don'ts
✅ accent≤2处/页，大面积留白 | ❌ 禁混用3+强调色，禁过度装饰

## Agent Prompt Guide

### 快速色板
- 标题: `#1C1A17` | 正文: `#8A817A` | 强调: `#C0512F`
- 底色: `#FAF7F2` | 卡片: `#FFFFFF` | 边框: `#E5E7EB`

### SVG 组件示例
- "封面：`#FAF7F2`底，标题48px system-ui, sans-serif weight 600，色`#1C1A17`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#FFFFFF`底+`#E5E7EB`边框+8px圆角。标题24px weight 500 色`#1C1A17`。正文18px weight 400 色`#8A817A`。"

### 品牌铁律
1. 强调色(`#C0512F`)每页不超过2处使用
2. 排版层次清晰，标题与正文对比明确
3. 保持品牌调性一致，避免混用风格
