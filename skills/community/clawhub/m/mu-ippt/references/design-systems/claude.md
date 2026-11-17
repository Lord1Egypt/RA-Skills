---
name: "Claude"
category: "AI & LLM"
description: "Anthropic's AI assistant. Warm terracotta accent, clean editorial layout."
colors:
  primary: "#30302e"
  secondary: "#6B7280"
  accent: "#D97757"
  background: "#ffffff"
  surface: "#30302e"
  muted: "#6B7280"
  border: "#f0eee6"
typography:
  display:
    fontFamily: Anthropic Serif
    fontSize: 3rem
    fontWeight: 600
    letterSpacing: -0.02em
  body:
    fontFamily: Anthropic Sans
    fontSize: 1rem
    fontWeight: 400
  mono:
    fontFamily: Anthropic Mono
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
  scenes: ["技术演讲", "编辑风格汇报"]
  posture: "宽松"
  accentBudget: 2
---

## Overview
Claude's interface is a literary salon reimagined as a product page — warm, unhurried, and quietly intellectual.

## Colors
primary(`#30302e`)标题 | accent(`#D97757`)强调 | bg(`#ffffff`)底色 | surface(`#30302e`)卡片

## Typography
Display: Anthropic Serif | Body: Anthropic Serif | Mono: Anthropic Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 48px | 600 | 1.0 | -1.0px | 首页主标题 |
| 章节标题 | 52px | 500 | 1.20 | normal | 分章标题 |
| 卡片标题 | 32px | 500 | 1.10 | normal | 内容卡标题 |
| 正文 | 20px | 400 | 1.60 | normal | 主要阅读 |
| 辅助文字 | 14px | 400 | 1.43 | normal | 标注/脚注 |
| 数据标签 | 6px | 400 | 1.60 | 0.096px | 图表标签 |

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
- 标题: `#30302e` | 正文: `#6B7280` | 强调: `#D97757`
- 底色: `#ffffff` | 卡片: `#30302e` | 边框: `#f0eee6`

### SVG 组件示例
- "封面：`#ffffff`底，标题48px Anthropic Serif weight 600，色`#30302e`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#30302e`底+`#f0eee6`边框+8px圆角。标题24px weight 500 色`#30302e`。正文18px weight 400 色`#6B7280`。"

### 品牌铁律
1. Focus on ONE component at a time
2. Reference specific color names — "use Olive Gray (#5e5d59)" not "make it gray"
3. Always specify warm-toned variants — no cool grays
