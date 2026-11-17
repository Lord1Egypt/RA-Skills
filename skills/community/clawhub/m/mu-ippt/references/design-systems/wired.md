---
name: "Wired"
category: "Media & Consumer"
description: "Tech magazine. Paper-white broadsheet density, custom serif display, mono kickers, ink-blue links."
colors:
  primary: "#1a1a1a"
  secondary: "#1a1a1a"
  accent: "#057dbc"
  background: "#ffffff"
  surface: "#F8F9FA"
  muted: "#1a1a1a"
  border: "#e2e8f0"
typography:
  display:
    fontFamily: Monaco, Courier New, Courier
    fontSize: 3rem
    fontWeight: 600
    letterSpacing: -0.02em
  body:
    fontFamily: Monaco, Courier New, Courier
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
WIRED's homepage feels like a printed broadsheet that someone has plugged into a wall socket.

## Colors
primary(`#1a1a1a`)标题 | accent(`#057dbc`)强调 | bg(`#ffffff`)底色 | surface(`#F8F9FA`)卡片

## Typography
Display: helvetica | Body: helvetica | Mono: Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 48px | 600 | 1.0 | -1.0px | 首页主标题 |
| 章节标题 | 20px | 700 | 1.20 | -0.28px | 分章标题 |
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
- 标题: `#1a1a1a` | 正文: `#1a1a1a` | 强调: `#057dbc`
- 底色: `#ffffff` | 卡片: `#F8F9FA` | 边框: `#e2e8f0`

### SVG 组件示例
- "封面：`#ffffff`底，标题48px Monaco, Courier New, Courier weight 600，色`#1a1a1a`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#F8F9FA`底+`#e2e8f0`边框+16px圆角。标题24px weight 500 色`#1a1a1a`。正文18px weight 400 色`#1a1a1a`。"

### 品牌铁律
1. **Audit corners first.** If you see any `border-radius` other than `0`, `50%` (icons/avatars), or `1920px` (text pills), flatten it. Round corners are the single most common mistake.
2. **Audit shadows.** Strip every `box-shadow`. If a tile needs to feel "lifted", use a 2px black border or a hairline rule instead.
3. **Audit typeface roles.** Make sure WiredDisplay only sets headlines, BreveText only sets reading body, Apercu only sets UI, WiredMono only sets ALL-CAPS labels. Swapping roles breaks the voice instantly.
