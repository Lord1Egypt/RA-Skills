---
name: "Meta"
category: "E-Commerce & Retail"
description: "Tech retail store. Photography-first, binary light/dark surfaces, Meta Blue CTAs."
colors:
  primary: "#000000"
  secondary: "#F0F2F5"
  accent: "#0668E1"
  background: "#FFFFFF"
  surface: "#F1F4F7"
  muted: "#F0F2F5"
  border: "#F2F0E6"
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
The Meta Store is a product-forward retail experience built to sell hardware — Quest VR headsets, Ray-Ban Meta smart glasses, and accessories.

## Colors
primary(`#000000`)标题 | accent(`#0668E1`)强调 | bg(`#FFFFFF`)底色 | surface(`#F1F4F7`)卡片

## Typography
Display: Optimistic VF | Body: Optimistic VF | Mono: Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 48px | 600 | 1.0 | -1.0px | 首页主标题 |
| 章节标题 | 36px | 500 | 1.28 | normal | 分章标题 |
| 卡片标题 | 28px | 300 | 1.21 | normal | 内容卡标题 |
| 正文 | 18px | 400 | 1.44 | normal | 主要阅读 |
| 辅助文字 | 12px | 400 | 1.33 | normal | 标注/脚注 |
| 数据标签 | 12px | 500 | 1.3 | normal | 图表标签 |

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
- 标题: `#000000` | 正文: `#F0F2F5` | 强调: `#0668E1`
- 底色: `#FFFFFF` | 卡片: `#F1F4F7` | 边框: `#F2F0E6`

### SVG 组件示例
- "封面：`#FFFFFF`底，标题48px system-ui, sans-serif weight 300，色`#000000`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#F1F4F7`底+`#F2F0E6`边框+16px圆角。标题24px weight 500 色`#000000`。正文18px weight 400 色`#F0F2F5`。"

### 品牌铁律
1. Focus on ONE component at a time
2. Reference specific color names and hex codes from this document
3. Use natural language descriptions, not CSS values — "pill-shaped Meta Blue button" not "border-radius: 100px; background: #0064E0"
