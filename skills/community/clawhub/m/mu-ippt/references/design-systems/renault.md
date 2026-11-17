---
name: "Renault"
category: "Automotive"
description: "French automotive. Vibrant aurora gradients, NouvelR typography, bold energy."
colors:
  primary: "#1A1A1A"
  secondary: "#6B7280"
  accent: "#3B82F6"
  background: "#FFFFFF"
  surface: "#F8EB4C"
  muted: "#6B7280"
  border: "#D1D1D1"
typography:
  display:
    fontFamily: system-ui, sans-serif
    fontSize: 3rem
    fontWeight: 700
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
  scenes: ["产品发布", "科技主题演讲"]
  posture: "宽松"
  accentBudget: 2
---

## Overview
Renault's website is a vibrant digital showroom that balances French automotive elegance with bold, forward-leaning energy — a departure from the monochromat...

## Colors
primary(`#1A1A1A`)标题 | accent(`#3B82F6`)强调 | bg(`#FFFFFF`)底色 | surface(`#F8EB4C`)卡片

## Typography
Display: NouvelR | Body: NouvelR | Mono: Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 48px | 600 | 1.0 | -1.0px | 首页主标题 |
| 章节标题 | 40px | 700 | 0.95 | normal | 分章标题 |
| 卡片标题 | 24px | 500 | 1.2 | -0.2px | 内容卡标题 |
| 正文 | 18px | 400 | 1.5 | normal | 主要阅读 |
| 辅助文字 | 8px | 400 | 1.10 | normal | 标注/脚注 |
| 数据标签 | 10px | 700 | 1.45 | normal | 图表标签 |

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
- 标题: `#1A1A1A` | 正文: `#6B7280` | 强调: `#3B82F6`
- 底色: `#FFFFFF` | 卡片: `#F8EB4C` | 边框: `#D1D1D1`

### SVG 组件示例
- "封面：`#FFFFFF`底，标题48px system-ui, sans-serif weight 700，色`#1A1A1A`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#F8EB4C`底+`#D1D1D1`边框+16px圆角。标题24px weight 500 色`#1A1A1A`。正文18px weight 400 色`#6B7280`。"

### 品牌铁律
1. Focus on ONE component at a time — Renault's system has clear component boundaries (PromoCard, VehicleRangeCard, CTA variants)
2. Reference specific color names and hex codes — the palette is small but each color has a precise function
3. Use natural language descriptions, not CSS values — "sharp zero-radius rectangle" conveys intent better than "border-radius: 0"
