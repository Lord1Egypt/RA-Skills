---
name: "Bmw"
category: "Automotive"
description: "Luxury automotive. Dark premium surfaces, precise German engineering aesthetic."
colors:
  primary: "#ffffff"
  secondary: "#6B7280"
  accent: "#1C69D4"
  background: "#ffffff"
  surface: "#F8F9FA"
  muted: "#6B7280"
  border: "#E5E7EB"
typography:
  display:
    fontFamily: BMWTypeNextLatin Light
    fontSize: 3rem
    fontWeight: 700
    letterSpacing: -0.02em
  body:
    fontFamily: BMWTypeNextLatin
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
  sm: 4px
  md: 8px
  lg: 16px
ppt:
  scenes: ["产品发布"]
  posture: "紧凑"
  accentBudget: 2
---

## Overview
BMW's website is automotive engineering made visual — a design system that communicates precision, performance, and German industrial confidence.

## Colors
primary(`#ffffff`)标题 | accent(`#1C69D4`)强调 | bg(`#ffffff`)底色 | surface(`#F8F9FA`)卡片

## Typography
Display: BMWTypeNextLatin Light | Body: BMWTypeNextLatin Light | Mono: Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 60px | 300 | 1.30 | 1.30px | 首页主标题 |
| 章节标题 | 32px | 400 | 1.30 | 1.30px | 分章标题 |
| 卡片标题 | 24px | 500 | 1.2 | -0.2px | 内容卡标题 |
| 正文 | 16px | 400 | 1.15 | 1.15px | 主要阅读 |
| 辅助文字 | 18px | 900 | 1.30 | 1.30px | 标注/脚注 |
| 数据标签 | 12px | 500 | 1.3 | normal | 图表标签 |

## Layout & Shapes
间距风格紧凑，圆角直角/极小圆角。 小圆角矩形，保持克制的几何感。

## Elevation
扁平，不使用阴影。

## Components
标题卡(accent左边框) | 数据卡(surface底+数字突出) | 引用块(muted底+斜体)

## Do's and Don'ts
✅ accent≤2处/页，大面积留白 | ❌ 禁混用3+强调色，禁过度装饰

## Agent Prompt Guide

### 快速色板
- 标题: `#ffffff` | 正文: `#6B7280` | 强调: `#1C69D4`
- 底色: `#ffffff` | 卡片: `#F8F9FA` | 边框: `#E5E7EB`

### SVG 组件示例
- "封面：`#ffffff`底，标题48px BMWTypeNextLatin Light weight 700，色`#ffffff`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#F8F9FA`底+`#E5E7EB`边框+8px圆角。标题24px weight 500 色`#ffffff`。正文18px weight 400 色`#6B7280`。"

### 品牌铁律
1. Zero border-radius — every corner is sharp, no exceptions
2. Weight extremes: 300 (display), 400 (body), 700 (buttons), 900 (nav)
3. BMW Blue for interactive only — never as background or decoration
