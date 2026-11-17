---
name: "Mistral Ai"
category: "AI & LLM"
description: "Open-weight LLM provider. French-engineered minimalism, purple-toned."
colors:
  primary: "#1A1A1A"
  secondary: "#6B7280"
  accent: "#ffd900"
  background: "#ffffff"
  surface: "#F8F9FA"
  muted: "#6B7280"
  border: "#E5E7EB"
typography:
  display:
    fontFamily: Arial
    fontSize: 3rem
    fontWeight: 600
    letterSpacing: -0.02em
  body:
    fontFamily: Arial
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
  sm: 8px
  md: 16px
  lg: 32px
ppt:
  scenes: ["技术演讲", "科技主题演讲"]
  posture: "宽松"
  accentBudget: 2
---

## Overview
Mistral AI's interface is a sun-drenched landscape rendered in code — a warm, bold, unapologetically European design that trades the typical blue-screen AI a...

## Colors
primary(`#1A1A1A`)标题 | accent(`#ffd900`)强调 | bg(`#ffffff`)底色 | surface(`#F8F9FA`)卡片

## Typography
Display: Arial | Body: Arial | Mono: Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 48px | 600 | 1.0 | -1.0px | 首页主标题 |
| 章节标题 | 56px | 400 | 0.95 | normal | 分章标题 |
| 卡片标题 | 30px | 400 | 1.20 | normal | 内容卡标题 |
| 正文 | 18px | 400 | 1.5 | normal | 主要阅读 |
| 辅助文字 | 14px | 400 | 1.4 | normal | 标注/脚注 |
| 数据标签 | 12px | 500 | 1.3 | normal | 图表标签 |

## Layout & Shapes
间距风格宽松，圆角直角/极小圆角。 小圆角矩形，保持克制的几何感。

## Elevation
扁平，不使用阴影。

## Components
标题卡(accent左边框) | 数据卡(surface底+数字突出) | 引用块(muted底+斜体)

## Do's and Don'ts
✅ accent≤2处/页，大面积留白 | ❌ 禁混用3+强调色，禁过度装饰

## Agent Prompt Guide

### 快速色板
- 标题: `#1A1A1A` | 正文: `#6B7280` | 强调: `#ffd900`
- 底色: `#ffffff` | 卡片: `#F8F9FA` | 边框: `#E5E7EB`

### SVG 组件示例
- "封面：`#ffffff`底，标题48px Arial weight 600，色`#1A1A1A`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#F8F9FA`底+`#E5E7EB`边框+8px圆角。标题24px weight 500 色`#1A1A1A`。正文18px weight 400 色`#6B7280`。"

### 品牌铁律
1. Keep the warm temperature — "shift toward amber" not "shift toward gray"
2. Use size for hierarchy — 82px → 56px → 48px → 32px → 24px → 16px
3. Never add border-radius — sharp corners only
