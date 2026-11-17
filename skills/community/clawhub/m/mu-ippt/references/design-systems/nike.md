---
name: "Nike"
category: "E-Commerce & Retail"
description: "Athletic retail. Monochrome UI, massive uppercase type, full-bleed photography."
colors:
  primary: "#28282A"
  secondary: "#707072"
  accent: "#000000"
  background: "#FFFFFF"
  surface: "#28282A"
  muted: "#707072"
  border: "#707072"
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
Nike.com is a kinetic retail cathedral — a site that channels the explosive energy of sport into a digital shopping experience.

## Colors
primary(`#28282A`)标题 | accent(`#000000`)强调 | bg(`#FFFFFF`)底色 | surface(`#28282A`)卡片

## Typography
Display: Nike Futura ND | Body: Nike Futura ND | Mono: Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 96px | 500 | 0.90 | normal | 首页主标题 |
| 章节标题 | 32px | 500 | 1.20 | normal | 分章标题 |
| 卡片标题 | 24px | 500 | 1.20 | normal | 内容卡标题 |
| 正文 | 16px | 400 | 1.75 | normal | 主要阅读 |
| 辅助文字 | 12px | 500 | 1.50 | normal | 标注/脚注 |
| 数据标签 | 12px | 400 | 1.50 | normal | 图表标签 |

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
- 标题: `#28282A` | 正文: `#707072` | 强调: `#000000`
- 底色: `#FFFFFF` | 卡片: `#28282A` | 边框: `#707072`

### SVG 组件示例
- "封面：`#FFFFFF`底，标题48px system-ui, sans-serif weight 600，色`#28282A`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#28282A`底+`#707072`边框+16px圆角。标题24px weight 500 色`#28282A`。正文18px weight 400 色`#707072`。"

### 品牌铁律
1. Focus on ONE component at a time
2. Reference specific color names and hex codes from this document
3. Remember: product photography is the color — UI stays monochromatic
