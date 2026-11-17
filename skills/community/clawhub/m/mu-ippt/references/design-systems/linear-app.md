---
name: "Linear App"
category: "Productivity & SaaS"
description: "Project management. Ultra-minimal, precise, purple accent."
colors:
  primary: "#0f1011"
  secondary: "#d0d6e0"
  accent: "#5e6ad2"
  background: "#f7f8f8"
  surface: "#0f1011"
  muted: "#d0d6e0"
  border: "#23252a"
typography:
  display:
    fontFamily: Inter Variable
    fontSize: 3rem
    fontWeight: 600
    letterSpacing: -0.02em
  body:
    fontFamily: Inter Variable
    fontSize: 1rem
    fontWeight: 400
  mono:
    fontFamily: Berkeley Mono
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
  scenes: ["产品介绍", "效率工具演示", "科技主题演讲"]
  posture: "紧凑"
  accentBudget: 2
---

## Overview
Linear's website is a masterclass in dark-mode-first product design — a near-black canvas (`#08090a`) where content emerges from darkness like starlight.

## Colors
primary(`#0f1011`)标题 | accent(`#5e6ad2`)强调 | bg(`#f7f8f8`)底色 | surface(`#0f1011`)卡片

## Typography
Display: Inter Variable | Body: Inter Variable | Mono: Berkeley Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 48px | 510 | 1.00 | -1.056px | 首页主标题 |
| 章节标题 | 32px | 400 | 1.13 | -0.704px | 分章标题 |
| 卡片标题 | 24px | 400 | 1.33 | -0.288px | 内容卡标题 |
| 正文 | 18px | 400 | 1.60 | -0.165px | 主要阅读 |
| 辅助文字 | 15px | 400 | 1.60 | -0.165px | 标注/脚注 |
| 数据标签 | 11px | 510 | 1.40 | normal | 图表标签 |

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
- 标题: `#0f1011` | 正文: `#d0d6e0` | 强调: `#5e6ad2`
- 底色: `#f7f8f8` | 卡片: `#0f1011` | 边框: `#23252a`

### SVG 组件示例
- "封面：`#f7f8f8`底，标题48px Inter Variable weight 600，色`#0f1011`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#0f1011`底+`#23252a`边框+16px圆角。标题24px weight 500 色`#0f1011`。正文18px weight 400 色`#d0d6e0`。"

### 品牌铁律
1. Always set font-feature-settings `"cv01", "ss03"` on all Inter text — this is non-negotiable for Linear's look
2. Letter-spacing scales with font size: -1.584px at 72px, -1.056px at 48px, -0.704px at 32px, normal below 16px
3. Three weights: 400 (read), 510 (emphasize/navigate), 590 (announce)
