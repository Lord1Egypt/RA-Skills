---
name: "Ibm"
category: "Media & Consumer"
description: "Enterprise technology. Carbon design system, structured blue palette."
colors:
  primary: "#f4f4f4"
  secondary: "#161616"
  accent: "#f4f4f4"
  background: "#ffffff"
  surface: "#F8F9FA"
  muted: "#161616"
  border: "#393939"
typography:
  display:
    fontFamily: IBM Plex Sans
    fontSize: 3rem
    fontWeight: 600
    letterSpacing: -0.02em
  body:
    fontFamily: IBM Plex Mono
    fontSize: 1rem
    fontWeight: 400
  mono:
    fontFamily: IBM Plex Mono
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
IBM's website is the digital embodiment of enterprise authority built on the Carbon Design System — a design language so methodically structured it reads lik...

## Colors
primary(`#f4f4f4`)标题 | accent(`#f4f4f4`)强调 | bg(`#ffffff`)底色 | surface(`#F8F9FA`)卡片

## Typography
Display: IBM Plex Sans | Body: IBM Plex Sans | Mono: IBM Plex Mono

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
- 标题: `#f4f4f4` | 正文: `#161616` | 强调: `#f4f4f4`
- 底色: `#ffffff` | 卡片: `#F8F9FA` | 边框: `#393939`

### SVG 组件示例
- "封面：`#ffffff`底，标题48px IBM Plex Sans weight 600，色`#f4f4f4`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#F8F9FA`底+`#393939`边框+16px圆角。标题24px weight 500 色`#f4f4f4`。正文18px weight 400 色`#161616`。"

### 品牌铁律
1. Always use 0px border-radius on buttons, inputs, and cards — this is non-negotiable in Carbon
2. Letter-spacing only at small sizes: 0.16px at 14px, 0.32px at 12px — never on display text
3. Three weights: 300 (display), 400 (body), 600 (emphasis) — no bold
