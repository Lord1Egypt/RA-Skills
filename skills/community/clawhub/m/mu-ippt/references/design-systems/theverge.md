---
name: "Theverge"
category: "Media & Consumer"
description: "Tech editorial media. Acid-mint and ultraviolet accents, Manuka display, rave-flyer story tiles."
colors:
  primary: "#3860be"
  secondary: "#949494"
  accent: "#ffffff"
  background: "#131313"
  surface: "#2d2d2d"
  muted: "#949494"
  border: "#309875"
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
The Verge's 2024 redesign feels like somebody wired a Condé Nast magazine to a chiptune soundboard.

## Colors
primary(`#3860be`)标题 | accent(`#ffffff`)强调 | bg(`#131313`)底色 | surface(`#2d2d2d`)卡片

## Typography
Display: Manuka | Body: Manuka | Mono: Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 48px | 600 | 1.0 | -1.0px | 首页主标题 |
| 章节标题 | 32px | 500 | 1.1 | -0.5px | 分章标题 |
| 卡片标题 | 24px | 500 | 1.2 | -0.2px | 内容卡标题 |
| 正文 | 18px | 400 | 1.5 | normal | 主要阅读 |
| 辅助文字 | 14px | 400 | 1.4 | normal | 标注/脚注 |
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
- 标题: `#3860be` | 正文: `#949494` | 强调: `#ffffff`
- 底色: `#131313` | 卡片: `#2d2d2d` | 边框: `#309875`

### SVG 组件示例
- "封面：`#131313`底，标题48px system-ui, sans-serif weight 600，色`#3860be`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#2d2d2d`底+`#309875`边框+16px圆角。标题24px weight 500 色`#3860be`。正文18px weight 400 色`#949494`。"

### 品牌铁律
1. **Audit the canvas.** If you see a light background anywhere on the homepage, flatten it to `#131313`. There is no light mode.
2. **Audit corners.** Every rectangle should land on 2/3/4/20/24/30/40px or 50%. Square corners break the voice.
3. **Audit shadows.** Strip every `box-shadow` that isn't a 1px inset underline or a 1px hazard-color border. The Verge uses color for elevation, not shadow.
