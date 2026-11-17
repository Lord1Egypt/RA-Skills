---
name: "Spacex"
category: "Media & Consumer"
description: "Space technology. Stark black and white, full-bleed imagery, futuristic."
colors:
  primary: "#1A1A1A"
  secondary: "#6B7280"
  accent: "#005288"
  background: "#f0f0fa"
  surface: "#F8F9FA"
  muted: "#6B7280"
  border: "#E5E7EB"
typography:
  display:
    fontFamily: D-DIN-Bold
    fontSize: 3rem
    fontWeight: 600
    letterSpacing: -0.02em
  body:
    fontFamily: D-DIN
    fontSize: 1rem
    fontWeight: 400
  mono:
    fontFamily: ui-monospace, monospace
    fontSize: 0.875rem
rounded:
  sm: 6px
  md: 12px
  lg: 20px
spacing:
  sm: 6px
  md: 12px
  lg: 24px
ppt:
  scenes: ["内容营销", "消费品推广"]
  posture: "平衡"
  accentBudget: 2
---

## Overview
SpaceX's website is a full-screen cinematic experience that treats aerospace engineering like a film — every section is a scene, every photograph is a frame,...

## Colors
primary(`#1A1A1A`)标题 | accent(`#005288`)强调 | bg(`#f0f0fa`)底色 | surface(`#F8F9FA`)卡片

## Typography
Display: D-DIN-Bold | Body: D-DIN-Bold | Mono: Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 48px | 700 | 1.00 | 0.96px | 首页主标题 |
| 章节标题 | 32px | 500 | 1.1 | -0.5px | 分章标题 |
| 卡片标题 | 24px | 500 | 1.2 | -0.2px | 内容卡标题 |
| 正文 | 16px | 400 | 1.50 | normal | 主要阅读 |
| 辅助文字 | 12px | 400 | 1.00 | normal | 标注/脚注 |
| 数据标签 | 10px | 400 | 0.94 | 1px | 图表标签 |

## Layout & Shapes
间距风格平衡，圆角大圆角（16px+）。 小圆角矩形，保持克制的几何感。

## Elevation
扁平，不使用阴影。

## Components
标题卡(accent左边框) | 数据卡(surface底+数字突出) | 引用块(muted底+斜体)

## Do's and Don'ts
✅ accent≤2处/页，大面积留白 | ❌ 禁混用3+强调色，禁过度装饰

## Agent Prompt Guide

### 快速色板
- 标题: `#1A1A1A` | 正文: `#6B7280` | 强调: `#005288`
- 底色: `#f0f0fa` | 卡片: `#F8F9FA` | 边框: `#E5E7EB`

### SVG 组件示例
- "封面：`#f0f0fa`底，标题48px D-DIN-Bold weight 600，色`#1A1A1A`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#F8F9FA`底+`#E5E7EB`边框+12px圆角。标题24px weight 500 色`#1A1A1A`。正文18px weight 400 色`#6B7280`。"

### 品牌铁律
1. Start with photography — the image IS the design
2. All text is uppercase with positive letter-spacing — no exceptions
3. Only two colors: black and spectral white (#f0f0fa)
