---
name: "Pinterest"
category: "Media & Consumer"
description: "Visual discovery. Red accent, masonry grid, image-first."
colors:
  primary: "#2b48d4"
  secondary: "#6B7280"
  accent: "#E60023"
  background: "#ffffff"
  surface: "#33332e"
  muted: "#6B7280"
  border: "#c8c8c1"
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
  scenes: ["内容营销", "消费品推广", "科技主题演讲"]
  posture: "紧凑"
  accentBudget: 2
---

## Overview
Pinterest's website is a warm, inspiration-driven canvas that treats visual discovery like a lifestyle magazine.

## Colors
primary(`#2b48d4`)标题 | accent(`#E60023`)强调 | bg(`#ffffff`)底色 | surface(`#33332e`)卡片

## Typography
Display: Pin Sans | Body: Pin Sans | Mono: Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 70px | 600 | 1.5 | normal | 首页主标题 |
| 章节标题 | 28px | 700 | 1.5 | -1.2px | 分章标题 |
| 卡片标题 | 24px | 500 | 1.2 | -0.2px | 内容卡标题 |
| 正文 | 16px | 400 | 1.40 | normal | 主要阅读 |
| 辅助文字 | 12px | 400 | 1.50 | normal | 标注/脚注 |
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
- 标题: `#2b48d4` | 正文: `#6B7280` | 强调: `#E60023`
- 底色: `#ffffff` | 卡片: `#33332e` | 边框: `#c8c8c1`

### SVG 组件示例
- "封面：`#ffffff`底，标题48px system-ui, sans-serif weight 600，色`#2b48d4`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#33332e`底+`#c8c8c1`边框+16px圆角。标题24px weight 500 色`#2b48d4`。正文18px weight 400 色`#6B7280`。"

### 品牌铁律
1. Warm neutrals everywhere — olive/sand grays, never cool steel
2. Pinterest Red for CTAs only — bold and singular
3. 16px radius on buttons/inputs, 20px+ on cards — generous but not pill
