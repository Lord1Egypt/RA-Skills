---
name: "Apple"
category: "Media & Consumer"
description: "Consumer electronics. Premium white space, SF Pro, cinematic imagery."
colors:
  primary: "#1d1d1f"
  secondary: "#0066cc"
  accent: "#0071E3"
  background: "#ffffff"
  surface: "#272729"
  muted: "#0066cc"
  border: "#d2d2d7"
typography:
  display:
    fontFamily: SF Pro Display
    fontSize: 3rem
    fontWeight: 700
    letterSpacing: -0.02em
  body:
    fontFamily: SF Pro Text
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
Apple's web language is a precision editorial system that alternates between gallery-like calm and retail-density information blocks.

## Colors
primary(`#1d1d1f`)标题 | accent(`#0071E3`)强调 | bg(`#ffffff`)底色 | surface(`#272729`)卡片

## Typography
Display: SF Pro Display | Body: SF Pro Text | Mono: Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 80px | 600 | 1.00 | -1.2px | 首页主标题 |
| 章节标题 | 40px | 600 | 1.10 | normal | 分章标题 |
| 卡片标题 | 28px | 600 | 1.14 | 0.196px | 内容卡标题 |
| 正文 | 17px | 400 | 1.47 | -0.374px | 主要阅读 |
| 辅助文字 | 14px | 400 | 1.29 | -0.224px | 标注/脚注 |
| 数据标签 | 12px | 400 | 1.00 | -0.12px | 图表标签 |

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
- 标题: `#1d1d1f` | 正文: `#0066cc` | 强调: `#0071E3`
- 底色: `#ffffff` | 卡片: `#272729` | 边框: `#d2d2d7`

### SVG 组件示例
- "封面：`#ffffff`底，标题48px SF Pro Display weight 700，色`#1d1d1f`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#272729`底+`#d2d2d7`边框+16px圆角。标题24px weight 500 色`#1d1d1f`。正文18px weight 400 色`#0066cc`。"

### 品牌铁律
1. Lock the neutral foundation first (`#000000`, `#f5f5f7`, `#ffffff`) before tuning accents.
2. Keep blue accents scarce and purposeful; if everything is blue, hierarchy collapses.
3. Tune typography in this order: display scale, body readability, then micro labels.
