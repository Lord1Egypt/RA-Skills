---
name: "Sentry"
category: "Backend & Data"
description: "Error monitoring. Dark dashboard, data-dense, pink-purple accent."
colors:
  primary: "#150f23"
  secondary: "#79628c"
  accent: "#362D59"
  background: "#ffffff"
  surface: "#F8F9FA"
  muted: "#79628c"
  border: "#362d59"
typography:
  display:
    fontFamily: Dammit Sans
    fontSize: 3rem
    fontWeight: 600
    letterSpacing: -0.02em
  body:
    fontFamily: Dammit Sans
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
  scenes: ["品牌演示", "科技主题演讲"]
  posture: "宽松"
  accentBudget: 2
---

## Overview
Sentry's website is a dark-mode-first developer tool interface that speaks the language of code editors and terminal windows.

## Colors
primary(`#150f23`)标题 | accent(`#362D59`)强调 | bg(`#ffffff`)底色 | surface(`#F8F9FA`)卡片

## Typography
Display: Dammit Sans | Body: Dammit Sans | Mono: Monaco

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 88px | 700 | 1.20 | normal | 首页主标题 |
| 章节标题 | 30px | 400 | 1.20 | normal | 分章标题 |
| 卡片标题 | 24px | 500 | 1.25 | normal | 内容卡标题 |
| 正文 | 16px | 400 | 1.50 | normal | 主要阅读 |
| 辅助文字 | 14px | 500 | 1.00 | 0.2px | 标注/脚注 |
| 数据标签 | 10px | 600 | 1.80 | 0.25px | 图表标签 |

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
- 标题: `#150f23` | 正文: `#79628c` | 强调: `#362D59`
- 底色: `#ffffff` | 卡片: `#F8F9FA` | 边框: `#362d59`

### SVG 组件示例
- "封面：`#ffffff`底，标题48px Dammit Sans weight 600，色`#150f23`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#F8F9FA`底+`#362d59`边框+16px圆角。标题24px weight 500 色`#150f23`。正文18px weight 400 色`#79628c`。"

### 品牌铁律
1. Always start with the dark purple background — the color palette is built FOR dark mode
2. Use inset shadows on buttons, ambient purple glows on hero sections
3. Uppercase + letter-spacing is the systematic pattern for labels, buttons, and captions
