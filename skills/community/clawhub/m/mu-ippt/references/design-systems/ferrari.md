---
name: "Ferrari"
category: "Automotive"
description: "Luxury automotive. Chiaroscuro editorial, Ferrari Red accents, cinematic black."
colors:
  primary: "#B01E0A"
  secondary: "#6B7280"
  accent: "#DC0000"
  background: "#FFFFFF"
  surface: "#303030"
  muted: "#6B7280"
  border: "#E5E7EB"
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
Ferrari's website is a digital editorial — a curated magazine where the Prancing Horse brand is presented with the gravitas of an art institution and the pre...

## Colors
primary(`#B01E0A`)标题 | accent(`#DC0000`)强调 | bg(`#FFFFFF`)底色 | surface(`#303030`)卡片

## Typography
Display: FerrariSans | Body: Body-Font | Mono: Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 48px | 600 | 1.0 | -1.0px | 首页主标题 |
| 章节标题 | 32px | 500 | 1.1 | -0.5px | 分章标题 |
| 卡片标题 | 24px | 500 | 1.2 | -0.2px | 内容卡标题 |
| 正文 | 18px | 400 | 1.5 | normal | 主要阅读 |
| 辅助文字 | 13px | 400 | 1.50 | 0.195px | 标注/脚注 |
| 数据标签 | 12px | 700 | 1.00 | 0.96px | 图表标签 |

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
- 标题: `#B01E0A` | 正文: `#6B7280` | 强调: `#DC0000`
- 底色: `#FFFFFF` | 卡片: `#303030` | 边框: `#E5E7EB`

### SVG 组件示例
- "封面：`#FFFFFF`底，标题48px system-ui, sans-serif weight 700，色`#B01E0A`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#303030`底+`#E5E7EB`边框+16px圆角。标题24px weight 500 色`#B01E0A`。正文18px weight 400 色`#6B7280`。"

### 品牌铁律
1. Focus on ONE component at a time — Ferrari's editorial rhythm means each section is a self-contained vignette
2. Reference specific color names and hex codes from this document — the palette is small but each color has a precise role
3. Use natural language descriptions, not CSS values — "razor-sharp 2px corners" conveys intent better than "border-radius: 2px"
