---
name: "X Ai"
category: "AI & LLM"
description: "Elon Musk's AI lab. Stark monochrome, futuristic minimalism."
colors:
  primary: "#1f2228"
  secondary: "#6B7280"
  accent: "#ffffff"
  background: "#ffffff"
  surface: "#F8F9FA"
  muted: "#6B7280"
  border: "#E5E7EB"
typography:
  display:
    fontFamily: GeistMono
    fontSize: 3rem
    fontWeight: 600
    letterSpacing: -0.02em
  body:
    fontFamily: universalSans
    fontSize: 1rem
    fontWeight: 400
  mono:
    fontFamily: universalSans
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
  scenes: ["技术演讲", "科技主题演讲"]
  posture: "宽松"
  accentBudget: 2
---

## Overview
xAI's website is a masterclass in dark-first, monospace-driven brutalist minimalism -- a design system that feels like it was built by engineers who understa...

## Colors
primary(`#1f2228`)标题 | accent(`#ffffff`)强调 | bg(`#ffffff`)底色 | surface(`#F8F9FA`)卡片

## Typography
Display: GeistMono | Body: GeistMono | Mono: Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 320px | 300 | 1.50 | normal | 首页主标题 |
| 章节标题 | 30px | 400 | 1.20 | normal | 分章标题 |
| 卡片标题 | 24px | 500 | 1.2 | -0.2px | 内容卡标题 |
| 正文 | 16px | 400 | 1.50 | normal | 主要阅读 |
| 辅助文字 | 14px | 400 | 1.4 | normal | 标注/脚注 |
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
- 标题: `#1f2228` | 正文: `#6B7280` | 强调: `#ffffff`
- 底色: `#ffffff` | 卡片: `#F8F9FA` | 边框: `#E5E7EB`

### SVG 组件示例
- "封面：`#ffffff`底，标题48px GeistMono weight 600，色`#1f2228`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#F8F9FA`底+`#E5E7EB`边框+16px圆角。标题24px weight 500 色`#1f2228`。正文18px weight 400 色`#6B7280`。"

### 品牌铁律
1. Always start with `#1f2228` background -- never use pure black or gray backgrounds
2. GeistMono for display and buttons, universalSans for everything else -- never mix these roles
3. All buttons must be GeistMono uppercase with 1.4px letter-spacing -- this is non-negotiable
