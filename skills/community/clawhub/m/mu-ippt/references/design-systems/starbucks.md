---
name: "Starbucks"
category: "E-Commerce & Retail"
description: "Global coffee retail brand. Four-tier green system, warm cream canvas, full-pill buttons."
colors:
  primary: "#1A1A1A"
  secondary: "#6B7280"
  accent: "#00704A"
  background: "#ffffff"
  surface: "#F8F9FA"
  muted: "#6B7280"
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
  sm: 8px
  md: 16px
  lg: 9999px
spacing:
  sm: 4px
  md: 8px
  lg: 16px
ppt:
  scenes: ["技术演讲", "商业提案", "零售营销"]
  posture: "紧凑"
  accentBudget: 2
---

## Overview
Starbucks' design system is a **warm, confident retail flagship** wearing the green of their storefront apron across every surface.

## Colors
primary(`#1A1A1A`)标题 | accent(`#00704A`)强调 | bg(`#ffffff`)底色 | surface(`#F8F9FA`)卡片

## Typography
Display: SoDoSans | Body: SoDoSans | Mono: Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 48px | 600 | 1.0 | -1.0px | 首页主标题 |
| 章节标题 | 24px | 600 | 36 | -0.16px | 分章标题 |
| 卡片标题 | 24px | 400 | 36 | -0.16px | 内容卡标题 |
| 正文 | 19px | 400 | 33.25 | -0.16px | 主要阅读 |
| 辅助文字 | 14px | 400 | 1.4 | normal | 标注/脚注 |
| 数据标签 | 13px | 400 | 1.5 | -0.01em | 图表标签 |

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
- 标题: `#1A1A1A` | 正文: `#6B7280` | 强调: `#00704A`
- 底色: `#ffffff` | 卡片: `#F8F9FA` | 边框: `#E5E7EB`

### SVG 组件示例
- "封面：`#ffffff`底，标题48px system-ui, sans-serif weight 600，色`#1A1A1A`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#F8F9FA`底+`#E5E7EB`边框+16px圆角。标题24px weight 500 色`#1A1A1A`。正文18px weight 400 色`#6B7280`。"

### 品牌铁律
1. Focus on ONE component at a time
2. Reference specific color names and hex codes from this document
3. Use natural language descriptions ("warm cream canvas," "four-tier green system") alongside exact values
