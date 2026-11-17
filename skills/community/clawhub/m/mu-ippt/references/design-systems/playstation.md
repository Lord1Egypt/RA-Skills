---
name: "Playstation"
category: "Media & Consumer"
description: "Gaming console retail. Three-surface channel layout, quiet-authority display type, cyan hover-scale."
colors:
  primary: "#ffffff"
  secondary: "#6b6b6b"
  accent: "#ffffff"
  background: "#ffffff"
  surface: "#F8F9FA"
  muted: "#6b6b6b"
  border: "#0070cc"
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
  sm: 8px
  md: 16px
  lg: 32px
ppt:
  scenes: ["内容营销", "消费品推广", "科技主题演讲"]
  posture: "宽松"
  accentBudget: 2
---

## Overview
PlayStation.com carries itself like the marketing wing of a premium consumer-electronics brand that happens to sell entertainment.

## Colors
primary(`#ffffff`)标题 | accent(`#ffffff`)强调 | bg(`#ffffff`)底色 | surface(`#F8F9FA`)卡片

## Typography
Display: Arial | Body: Arial | Mono: Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 54px | 300 | 1.25 | -0.1px | 首页主标题 |
| 章节标题 | 32px | 500 | 1.1 | -0.5px | 分章标题 |
| 卡片标题 | 24px | 500 | 1.2 | -0.2px | 内容卡标题 |
| 正文 | 18px | 400 | 1.5 | normal | 主要阅读 |
| 辅助文字 | 14px | 400 | 1.4 | normal | 标注/脚注 |
| 数据标签 | 12px | 500 | 1.50 | normal | 图表标签 |

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
- 标题: `#ffffff` | 正文: `#6b6b6b` | 强调: `#ffffff`
- 底色: `#ffffff` | 卡片: `#F8F9FA` | 边框: `#0070cc`

### SVG 组件示例
- "封面：`#ffffff`底，标题48px system-ui, sans-serif weight 600，色`#ffffff`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#F8F9FA`底+`#0070cc`边框+16px圆角。标题24px weight 500 色`#ffffff`。正文18px weight 400 色`#6b6b6b`。"

### 品牌铁律
1. **Audit display weight.** Every headline 22px and above should be SST weight 300. If you see weight 500 or 700 at hero scale, you've lost the PlayStation voice.
2. **Audit the hover treatment.** Every primary button must scale 1.2× on hover with the cyan-fill + white-border + blue-ring combination. Miss any of those four and the interaction signature breaks.
3. **Audit corners.** Every container and button should land on 2, 3, 6, 12, 13, 19, 20, 24, 36, 48, or 999px / 100%. Square corners break the voice.
