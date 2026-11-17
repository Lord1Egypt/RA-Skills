---
name: "Airbnb"
category: "E-Commerce & Retail"
description: "Travel marketplace. Warm coral accent, photography-driven, rounded UI."
colors:
  primary: "#222222"
  secondary: "#6a6a6a"
  accent: "#ff385c"
  background: "#ffffff"
  surface: "#f7f7f7"
  muted: "#6a6a6a"
  border: "#dddddd"
typography:
  display:
    fontFamily: Airbnb Cereal VF
    fontSize: 3rem
    fontWeight: 600
    letterSpacing: -0.02em
  body:
    fontFamily: Airbnb Cereal VF
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
Airbnb's 2026 design feels like a travel magazine that happens to be an app — pristine white canvases give way to full-bleed photography, and the interface i...

## Colors
primary(`#222222`)标题 | accent(`#ff385c`)强调 | bg(`#ffffff`)底色 | surface(`#f7f7f7`)卡片

## Typography
Display: Circular | Body: Circular | Mono: Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 48px | 600 | 1.0 | -1.0px | 首页主标题 |
| 章节标题 | 28px | 700 | 1.43 | normal | 分章标题 |
| 卡片标题 | 16px | 600 | 1.25 | normal | 内容卡标题 |
| 正文 | 16px | 500 | 1.25 | normal | 主要阅读 |
| 辅助文字 | 14px | 400 | 1.4 | normal | 标注/脚注 |
| 数据标签 | 12px | 400 | 1.33 | normal | 图表标签 |

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
- 标题: `#222222` | 正文: `#6a6a6a` | 强调: `#ff385c`
- 底色: `#ffffff` | 卡片: `#f7f7f7` | 边框: `#dddddd`

### SVG 组件示例
- "封面：`#ffffff`底，标题48px Airbnb Cereal VF weight 600，色`#222222`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#f7f7f7`底+`#dddddd`边框+16px圆角。标题24px weight 500 色`#222222`。正文18px weight 400 色`#6a6a6a`。"

### 品牌铁律
1. Focus on ONE component at a time.
2. Reference specific color names and hex codes from this document (e.g., "Ink Black #222222", not "dark gray").
3. Use natural language descriptions alongside measurements ("subtle three-layer elevation" rather than a long shadow string).
