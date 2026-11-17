---
name: "Shopify"
category: "E-Commerce & Retail"
description: "E-commerce platform. Dark-first cinematic, neon green accent, ultra-light type."
colors:
  primary: "#061A1C"
  secondary: "#A1A1AA"
  accent: "#008060"
  background: "#FFFFFF"
  surface: "#1E2C31"
  muted: "#A1A1AA"
  border: "#1E2C31"
typography:
  display:
    fontFamily: system-ui, sans-serif
    fontSize: 3rem
    fontWeight: 300
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
  sm: 8px
  md: 16px
  lg: 32px
ppt:
  scenes: ["技术演讲", "商业提案", "零售营销"]
  posture: "宽松"
  accentBudget: 2
---

## Overview
Shopify.com is a dark-first digital theatre — a website that stages its commerce platform like a cinematic premiere.

## Colors
primary(`#061A1C`)标题 | accent(`#008060`)强调 | bg(`#FFFFFF`)底色 | surface(`#1E2C31`)卡片

## Typography
Display: NeueHaasGrotesk | Body: NeueHaasGrotesk | Mono: Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 96px | 400 | 1.00 | normal | 首页主标题 |
| 章节标题 | 70px | 330 | 1.00 | normal | 分章标题 |
| 卡片标题 | 55px | 330 | 1.16 | normal | 内容卡标题 |
| 正文 | 20px | 500 | 1.40 | 0.3px | 主要阅读 |
| 辅助文字 | 14px | 500 | 1.49 | 0.28px | 标注/脚注 |
| 数据标签 | 13px | 500 | 1.50 | -0.13px | 图表标签 |

## Layout & Shapes
间距风格宽松，圆角全圆角/胶囊。 全圆角胶囊形按钮与标签，卡片使用大圆角。

## Elevation
扁平，不使用阴影。

## Components
标题卡(accent左边框) | 数据卡(surface底+数字突出) | 引用块(muted底+斜体)

## Do's and Don'ts
✅ accent≤2处/页，大面积留白 | ❌ 禁混用3+强调色，禁过度装饰

## Agent Prompt Guide

### 快速色板
- 标题: `#061A1C` | 正文: `#A1A1AA` | 强调: `#008060`
- 底色: `#FFFFFF` | 卡片: `#1E2C31` | 边框: `#1E2C31`

### SVG 组件示例
- "封面：`#FFFFFF`底，标题48px system-ui, sans-serif weight 300，色`#061A1C`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#1E2C31`底+`#1E2C31`边框+16px圆角。标题24px weight 500 色`#061A1C`。正文18px weight 400 色`#A1A1AA`。"

### 品牌铁律
1. Focus on ONE component at a time
2. Reference specific color names and hex codes from this document
3. Remember: this is a DARK-FIRST design — light surfaces are the exception, not the rule
