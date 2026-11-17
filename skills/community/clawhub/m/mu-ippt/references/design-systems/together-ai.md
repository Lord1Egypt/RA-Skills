---
name: "Together Ai"
category: "AI & LLM"
description: "Open-source AI infrastructure. Technical, blueprint-style design."
colors:
  primary: "#010120"
  secondary: "#6B7280"
  accent: "#ef2cc1"
  background: "#ffffff"
  surface: "#bdbbff"
  muted: "#6B7280"
  border: "#E5E7EB"
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
    fontFamily: PP Neue Montreal Mono
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
  scenes: ["技术演讲", "科技主题演讲"]
  posture: "宽松"
  accentBudget: 2
---

## Overview
Together AI's interface is a pastel-gradient dreamscape built for enterprise AI infrastructure — a design that somehow makes GPU clusters and model inference...

## Colors
primary(`#010120`)标题 | accent(`#ef2cc1`)强调 | bg(`#ffffff`)底色 | surface(`#bdbbff`)卡片

## Typography
Display: The Future | Body: The Future | Mono: Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 48px | 600 | 1.0 | -1.0px | 首页主标题 |
| 章节标题 | 40px | 500 | 1.20 | -0.8px | 分章标题 |
| 卡片标题 | 28px | 500 | 1.15 | -0.42px | 内容卡标题 |
| 正文 | 18px | 400 | 1.30 | -0.18px | 主要阅读 |
| 辅助文字 | 14px | 400 | 1.40 | normal | 标注/脚注 |
| 数据标签 | 12px | 500 | 1.3 | normal | 图表标签 |

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
- 标题: `#010120` | 正文: `#6B7280` | 强调: `#ef2cc1`
- 底色: `#ffffff` | 卡片: `#bdbbff` | 边框: `#E5E7EB`

### SVG 组件示例
- "封面：`#ffffff`底，标题48px system-ui, sans-serif weight 600，色`#010120`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#bdbbff`底+`#E5E7EB`边框+16px圆角。标题24px weight 500 色`#010120`。正文18px weight 400 色`#6B7280`。"

### 品牌铁律
1. Always specify negative letter-spacing for "The Future" — it's scaled by size
2. Dark sections use #010120 (midnight blue), never generic black
3. Shadows are always dark-blue-tinted: rgba(1, 1, 32, 0.1)
