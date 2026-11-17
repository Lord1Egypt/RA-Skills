---
name: "Mongodb"
category: "Backend & Data"
description: "Document database. Green leaf branding, developer documentation focus."
colors:
  primary: "#00684a"
  secondary: "#6B7280"
  accent: "#00684A"
  background: "#ffffff"
  surface: "#F8F9FA"
  muted: "#6B7280"
  border: "#E5E7EB"
typography:
  display:
    fontFamily: MongoDB Value Serif
    fontSize: 3rem
    fontWeight: 600
    letterSpacing: -0.02em
  body:
    fontFamily: Euclid Circular A
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
  scenes: ["品牌演示", "科技主题演讲"]
  posture: "紧凑"
  accentBudget: 2
---

## Overview
MongoDB's website is a deep-forest-meets-terminal experience — a design system rooted in the darkest teal-black (`#001e2b`) that evokes both the density of a...

## Colors
primary(`#00684a`)标题 | accent(`#00684A`)强调 | bg(`#ffffff`)底色 | surface(`#F8F9FA`)卡片

## Typography
Display: MongoDB Value Serif | Body: MongoDB Value Serif | Mono: Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 96px | 400 | 1.20 | normal | 首页主标题 |
| 章节标题 | 36px | 500 | 1.33 | normal | 分章标题 |
| 卡片标题 | 24px | 500 | 1.33 | normal | 内容卡标题 |
| 正文 | 20px | 400 | 1.60 | normal | 主要阅读 |
| 辅助文字 | 11px | 600 | 1.82 | 0.2px | 标注/脚注 |
| 数据标签 | 12px | 500 | 1.3 | normal | 图表标签 |

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
- 标题: `#00684a` | 正文: `#6B7280` | 强调: `#00684A`
- 底色: `#ffffff` | 卡片: `#F8F9FA` | 边框: `#E5E7EB`

### SVG 组件示例
- "封面：`#ffffff`底，标题48px MongoDB Value Serif weight 600，色`#00684a`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#F8F9FA`底+`#E5E7EB`边框+16px圆角。标题24px weight 500 色`#00684a`。正文18px weight 400 色`#6B7280`。"

### 品牌铁律
1. Start with the mode decision: dark (#001e2b) for hero/features, white for content
2. MongoDB Green (#00ed64) is electric — use once per section for maximum impact
3. Serif headlines (MongoDB Value Serif) create the editorial authority — never use for body
