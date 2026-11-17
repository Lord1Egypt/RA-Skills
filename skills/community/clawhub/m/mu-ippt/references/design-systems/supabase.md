---
name: "Supabase"
category: "Backend & Data"
description: "Open-source Firebase alternative. Dark emerald theme, code-first."
colors:
  primary: "#00c573"
  secondary: "#6B7280"
  accent: "#3ECF8E"
  background: "#efefef"
  surface: "#F8F9FA"
  muted: "#6B7280"
  border: "#242424"
typography:
  display:
    fontFamily: Source Code Pro
    fontSize: 3rem
    fontWeight: 600
    letterSpacing: -0.02em
  body:
    fontFamily: Source Code Pro
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
Supabase's website is a dark-mode-native developer platform that channels the aesthetic of a premium code editor — deep black backgrounds (`#0f0f0f`, `#17171...

## Colors
primary(`#00c573`)标题 | accent(`#3ECF8E`)强调 | bg(`#efefef`)底色 | surface(`#F8F9FA`)卡片

## Typography
Display: Circular | Body: Circular | Mono: Source Code Pro

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 72px | 400 | 1.00 | normal | 首页主标题 |
| 章节标题 | 36px | 400 | 1.25 | normal | 分章标题 |
| 卡片标题 | 24px | 400 | 1.33 | -0.16px | 内容卡标题 |
| 正文 | 16px | 400 | 1.50 | normal | 主要阅读 |
| 辅助文字 | 12px | 400 | 1.33 | normal | 标注/脚注 |
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
- 标题: `#00c573` | 正文: `#6B7280` | 强调: `#3ECF8E`
- 底色: `#efefef` | 卡片: `#F8F9FA` | 边框: `#242424`

### SVG 组件示例
- "封面：`#efefef`底，标题48px Source Code Pro weight 600，色`#00c573`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#F8F9FA`底+`#242424`边框+16px圆角。标题24px weight 500 色`#00c573`。正文18px weight 400 色`#6B7280`。"

### 品牌铁律
1. Start with #171717 background — everything is dark-mode-native
2. Green is the brand identity marker — use it for links, logo, and accent borders only
3. Depth comes from borders (#242424 → #2e2e2e → #363636), not shadows
