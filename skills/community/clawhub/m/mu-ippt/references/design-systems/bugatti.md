---
name: "Bugatti"
category: "Automotive"
description: "Hypercar brand. Cinema-black canvas, monochrome austerity, monumental display type."
colors:
  primary: "#ffffff"
  secondary: "#999999"
  accent: "#ffffff"
  background: "#ffffff"
  surface: "#999999"
  muted: "#999999"
  border: "#E5E7EB"
typography:
  display:
    fontFamily: Bugatti Display
    fontSize: 3rem
    fontWeight: 600
    letterSpacing: -0.02em
  body:
    fontFamily: Bugatti Text Regular
    fontSize: 1rem
    fontWeight: 400
  mono:
    fontFamily: Bugatti Monospace
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
  scenes: ["产品发布", "科技主题演讲"]
  posture: "紧凑"
  accentBudget: 2
---

## Overview
Bugatti.com does not behave like a website — it behaves like a feature-length car film that a visitor happens to be standing inside.

## Colors
primary(`#ffffff`)标题 | accent(`#ffffff`)强调 | bg(`#ffffff`)底色 | surface(`#999999`)卡片

## Typography
Display: Bugatti Display | Body: Bugatti Display | Mono: Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 288px | 400 | 1.00 | normal | 首页主标题 |
| 章节标题 | 36px | 400 | 1.11 | normal | 分章标题 |
| 卡片标题 | 24px | 500 | 1.2 | -0.2px | 内容卡标题 |
| 正文 | 18px | 400 | 1.5 | normal | 主要阅读 |
| 辅助文字 | 16px | 400 | 1.50 | normal | 标注/脚注 |
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
- 标题: `#ffffff` | 正文: `#999999` | 强调: `#ffffff`
- 底色: `#ffffff` | 卡片: `#999999` | 边框: `#E5E7EB`

### SVG 组件示例
- "封面：`#ffffff`底，标题48px Bugatti Display weight 600，色`#ffffff`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#999999`底+`#E5E7EB`边框+16px圆角。标题24px weight 500 色`#ffffff`。正文18px weight 400 色`#999999`。"

### 品牌铁律
1. **Audit the canvas.** If the background isn't pure `#000000`, change it. Bugatti does not tolerate off-black.
2. **Audit the palette.** Any color that isn't `#000000`, `#ffffff`, or `#999999` is drift. Remove it — that includes ALL accent colors, including common defaults like `#0070cc` Tailwind blue.
3. **Audit display scale.** If the largest headline on a page is smaller than 60px, it's under-scaled. Bugatti's minimum "monumental moment" is 60px; the maximum is 288px. Aim for the upper half.
