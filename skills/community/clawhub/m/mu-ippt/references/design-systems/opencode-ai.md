---
name: "Opencode Ai"
category: "AI & LLM"
description: "AI coding platform. Developer-centric dark theme."
colors:
  primary: "#201d1d"
  secondary: "#6e6e73"
  accent: "#007aff"
  background: "#fdfcfc"
  surface: "#302c2c"
  muted: "#6e6e73"
  border: "#646262"
typography:
  display:
    fontFamily: IBM Plex Mono, ui-monospace, SFMono-Regular, Menlo
    fontSize: 3rem
    fontWeight: 600
    letterSpacing: -0.02em
  body:
    fontFamily: IBM Plex Mono, ui-monospace, SFMono-Regular, Menlo
    fontSize: 1rem
    fontWeight: 400
  mono:
    fontFamily: Berkeley Mono
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
OpenCode's website embodies a terminal-native, monospace-first aesthetic that reflects its identity as an open source AI coding agent.

## Colors
primary(`#201d1d`)标题 | accent(`#007aff`)强调 | bg(`#fdfcfc`)底色 | surface(`#302c2c`)卡片

## Typography
Display: Berkeley Mono | Body: Berkeley Mono | Mono: Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 48px | 600 | 1.0 | -1.0px | 首页主标题 |
| 章节标题 | 38px | 700 | 1.50 | normal | 分章标题 |
| 卡片标题 | 16px | 700 | 1.50 | normal | 内容卡标题 |
| 正文 | 16px | 400 | 1.50 | normal | 主要阅读 |
| 辅助文字 | 14px | 400 | 2.00 | normal | 标注/脚注 |
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
- 标题: `#201d1d` | 正文: `#6e6e73` | 强调: `#007aff`
- 底色: `#fdfcfc` | 卡片: `#302c2c` | 边框: `#646262`

### SVG 组件示例
- "封面：`#fdfcfc`底，标题48px IBM Plex Mono, ui-monospace, SFMono-Regular, Menlo weight 600，色`#201d1d`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#302c2c`底+`#646262`边框+16px圆角。标题24px weight 500 色`#201d1d`。正文18px weight 400 色`#6e6e73`。"

### 品牌铁律
1. Berkeley Mono is the only font -- never introduce a second typeface. Size and weight create all hierarchy.
2. Keep surfaces flat: no shadows, no gradients, no blur effects. Use borders and background shifts only.
3. The warm undertone matters: use `#201d1d` not `#000000`, use `#fdfcfc` not `#ffffff`. The reddish warmth is subtle but essential.
