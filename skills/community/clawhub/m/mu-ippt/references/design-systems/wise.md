---
name: "Wise"
category: "Fintech & Crypto"
description: "Money transfer. Bright green accent, friendly and clear."
colors:
  primary: "#163300"
  secondary: "#6B7280"
  accent: "#9FE870"
  background: "#ffd11a"
  surface: "#e8ebe6"
  muted: "#6B7280"
  border: "#E5E7EB"
typography:
  display:
    fontFamily: Wise Sans
    fontSize: 3rem
    fontWeight: 600
    letterSpacing: -0.02em
  body:
    fontFamily: Inter
    fontSize: 1rem
    fontWeight: 400
  mono:
    fontFamily: ui-monospace, monospace
    fontSize: 0.875rem
rounded:
  sm: 8px
  md: 16px
  lg: 9999px
spacing:
  sm: 4px
  md: 8px
  lg: 16px
ppt:
  scenes: ["金融科技报告", "金融科技报告", "科技主题演讲"]
  posture: "紧凑"
  accentBudget: 2
---

## Overview
Wise's website is a bold, confident fintech platform that communicates "money without borders" through massive typography and a distinctive lime-green accent.

## Colors
primary(`#163300`)标题 | accent(`#9FE870`)强调 | bg(`#ffd11a`)底色 | surface(`#e8ebe6`)卡片

## Typography
Display: Wise Sans | Body: Wise Sans | Mono: Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 96px | 900 | 0.85 | normal | 首页主标题 |
| 章节标题 | 64px | 900 | 0.85 | normal | 分章标题 |
| 卡片标题 | 26px | 600 | 1.23 | -0.39px | 内容卡标题 |
| 正文 | 18px | 400 | 1.44 | 0.18px | 主要阅读 |
| 辅助文字 | 12px | 400 | 1.00 | -0.084px | 标注/脚注 |
| 数据标签 | 12px | 500 | 1.3 | normal | 图表标签 |

## Layout & Shapes
间距风格紧凑，圆角全圆角/胶囊。 全圆角胶囊形按钮与标签，卡片使用大圆角。

## Elevation
扁平，不使用阴影。

## Components
标题卡(accent左边框) | 数据卡(surface底+数字突出) | 引用块(muted底+斜体)

## Do's and Don'ts
✅ accent≤2处/页，大面积留白 | ❌ 禁混用3+强调色，禁过度装饰

## Agent Prompt Guide

### 快速色板
- 标题: `#163300` | 正文: `#6B7280` | 强调: `#9FE870`
- 底色: `#ffd11a` | 卡片: `#e8ebe6` | 边框: `#E5E7EB`

### SVG 组件示例
- "封面：`#ffd11a`底，标题48px Wise Sans weight 600，色`#163300`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#e8ebe6`底+`#E5E7EB`边框+16px圆角。标题24px weight 500 色`#163300`。正文18px weight 400 色`#6B7280`。"

### 品牌铁律
1. Wise Sans 900 at 0.85 line-height — the extreme weight IS the brand
2. Lime Green for buttons only — dark green text on green background
3. Scale animations (1.05 hover, 0.95 active) on all interactive elements
