---
name: "Zapier"
category: "Productivity & SaaS"
description: "Automation platform. Warm orange, friendly illustration-driven."
colors:
  primary: "#36342e"
  secondary: "#6B7280"
  accent: "#ff4f00"
  background: "#fffefb"
  surface: "#fffefb"
  muted: "#6B7280"
  border: "#E5E7EB"
typography:
  display:
    fontFamily: Degular Display
    fontSize: 3rem
    fontWeight: 600
    letterSpacing: -0.02em
  body:
    fontFamily: Degular Display
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
  scenes: ["产品介绍", "效率工具演示", "科技主题演讲"]
  posture: "宽松"
  accentBudget: 2
---

## Overview
Zapier's website radiates warm, approachable professionalism.

## Colors
primary(`#36342e`)标题 | accent(`#ff4f00`)强调 | bg(`#fffefb`)底色 | surface(`#fffefb`)卡片

## Typography
Display: Degular Display | Body: Degular Display | Mono: Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 80px | 500 | 0.90 | normal | 首页主标题 |
| 章节标题 | 48px | 500 | 1.04 | normal | 分章标题 |
| 卡片标题 | 24px | 600 | 1.5 | -0.48px | 内容卡标题 |
| 正文 | 20px | 400 | 1.00 | -0.2px | 主要阅读 |
| 辅助文字 | 14px | 500 | 1.25 | normal | 标注/脚注 |
| 数据标签 | 12px | 600 | 0.90 | 0.5px | 图表标签 |

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
- 标题: `#36342e` | 正文: `#6B7280` | 强调: `#ff4f00`
- 底色: `#fffefb` | 卡片: `#fffefb` | 边框: `#E5E7EB`

### SVG 组件示例
- "封面：`#fffefb`底，标题48px Degular Display weight 600，色`#36342e`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#fffefb`底+`#E5E7EB`边框+16px圆角。标题24px weight 500 色`#36342e`。正文18px weight 400 色`#6B7280`。"

### 品牌铁律
1. Always use warm cream (`#fffefb`) background, never pure white -- the warmth defines Zapier
2. Borders (`1px solid #c5c0b1`) are the structural backbone -- avoid shadow elevation
3. Zapier Orange (`#ff4f00`) is the only accent color; everything else is warm neutrals
