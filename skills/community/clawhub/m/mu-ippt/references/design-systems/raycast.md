---
name: "Raycast"
category: "Developer Tools"
description: "Productivity launcher. Sleek dark chrome, vibrant gradient accents."
colors:
  primary: "#18191a"
  secondary: "#6B7280"
  accent: "#3B82F6"
  background: "#ffffff"
  surface: "#101111"
  muted: "#6B7280"
  border: "#252829"
typography:
  display:
    fontFamily: Inter
    fontSize: 3rem
    fontWeight: 600
    letterSpacing: -0.02em
  body:
    fontFamily: Inter Fallback
    fontSize: 1rem
    fontWeight: 400
  mono:
    fontFamily: ui-monospace
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
  scenes: ["技术演讲", "科技主题演讲"]
  posture: "紧凑"
  accentBudget: 2
---

## Overview
Raycast's marketing site feels like the dark interior of a precision instrument — a Swiss watch case carved from obsidian.

## Colors
primary(`#18191a`)标题 | accent(`#3B82F6`)强调 | bg(`#ffffff`)底色 | surface(`#101111`)卡片

## Typography
Display: Inter | Body: Inter | Mono: GeistMono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 64px | 600 | 1.10 | 0px | 首页主标题 |
| 章节标题 | 24px | 500 | 1.5 | 0.2px | 分章标题 |
| 卡片标题 | 20px | 500 | 1.60 | 0.2px | 内容卡标题 |
| 正文 | 18px | 400 | 1.15 | 0.2px | 主要阅读 |
| 辅助文字 | 12px | 600 | 1.33 | 0px | 标注/脚注 |
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
- 标题: `#18191a` | 正文: `#6B7280` | 强调: `#3B82F6`
- 底色: `#ffffff` | 卡片: `#101111` | 边框: `#252829`

### SVG 组件示例
- "封面：`#ffffff`底，标题48px Inter weight 600，色`#18191a`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#101111`底+`#252829`边框+16px圆角。标题24px weight 500 色`#18191a`。正文18px weight 400 色`#6B7280`。"

### 品牌铁律
1. Check the background is `#07080a` not pure black — the blue tint is critical
2. Verify letter-spacing is positive (+0.2px) on body text — negative spacing breaks the Raycast aesthetic
3. Ensure shadows have both outer and inset layers — single-layer shadows look flat and wrong
