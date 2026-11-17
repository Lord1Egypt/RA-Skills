---
name: "Spotify"
category: "Media & Consumer"
description: "Music streaming. Vibrant green on dark, bold type, album-art-driven."
colors:
  primary: "#181818"
  secondary: "#6B7280"
  accent: "#1DB954"
  background: "#ffffff"
  surface: "#181818"
  muted: "#6B7280"
  border: "#4d4d4d"
typography:
  display:
    fontFamily: system-ui, sans-serif
    fontSize: 3rem
    fontWeight: 700
    letterSpacing: -0.02em
  body:
    fontFamily: SpotifyMixUI
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
Spotify's web interface is a dark, immersive music player that wraps listeners in a near-black cocoon (`#121212`, `#181818`, `#1f1f1f`) where album art and c...

## Colors
primary(`#181818`)标题 | accent(`#1DB954`)强调 | bg(`#ffffff`)底色 | surface(`#181818`)卡片

## Typography
Display: SpotifyMixUITitle | Body: SpotifyMixUI | Mono: Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 48px | 600 | 1.0 | -1.0px | 首页主标题 |
| 章节标题 | 32px | 500 | 1.1 | -0.5px | 分章标题 |
| 卡片标题 | 24px | 500 | 1.2 | -0.2px | 内容卡标题 |
| 正文 | 16px | 400 | 1.5 | normal | 主要阅读 |
| 辅助文字 | 12px | 400 | 1.5 | normal | 标注/脚注 |
| 数据标签 | 10px | 400 | 1.5 | normal | 图表标签 |

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
- 标题: `#181818` | 正文: `#6B7280` | 强调: `#1DB954`
- 底色: `#ffffff` | 卡片: `#181818` | 边框: `#4d4d4d`

### SVG 组件示例
- "封面：`#ffffff`底，标题48px system-ui, sans-serif weight 700，色`#181818`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#181818`底+`#4d4d4d`边框+16px圆角。标题24px weight 500 色`#181818`。正文18px weight 400 色`#6B7280`。"

### 品牌铁律
1. Start with #121212 — everything lives in near-black darkness
2. Spotify Green for functional highlights only (play, active, CTA)
3. Pill everything — 500px for large, 9999px for small, 50% for circular
