---
name: "Superhuman"
category: "Developer Tools"
description: "Fast email client. Premium dark UI, keyboard-first, purple glow."
colors:
  primary: "#292827"
  secondary: "#6B7280"
  accent: "#3B82F6"
  background: "#ffffff"
  surface: "#F8F9FA"
  muted: "#6B7280"
  border: "#dcd7d3"
typography:
  display:
    fontFamily: Super Sans VF
    fontSize: 3rem
    fontWeight: 700
    letterSpacing: -0.02em
  body:
    fontFamily: Super Sans VF
    fontSize: 1rem
    fontWeight: 400
  mono:
    fontFamily: Messina Mono
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
Superhuman's website feels like opening a luxury envelope — predominantly white, immaculately clean, with a single dramatic gesture of color that commands at...

## Colors
primary(`#292827`)标题 | accent(`#3B82F6`)强调 | bg(`#ffffff`)底色 | surface(`#F8F9FA`)卡片

## Typography
Display: Super Sans VF | Body: Super Sans VF | Mono: Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 64px | 540 | 0.96 | 0px | 首页主标题 |
| 章节标题 | 48px | 460 | 0.96 | 0px | 分章标题 |
| 卡片标题 | 28px | 540 | 1.14 | -0.63px | 内容卡标题 |
| 正文 | 16px | 460 | 1.50 | 0px | 主要阅读 |
| 辅助文字 | 14px | 500 | 1.20 | -0.315px | 标注/脚注 |
| 数据标签 | 12px | 700 | 1.50 | 0px | 图表标签 |

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
- 标题: `#292827` | 正文: `#6B7280` | 强调: `#3B82F6`
- 底色: `#ffffff` | 卡片: `#F8F9FA` | 边框: `#dcd7d3`

### SVG 组件示例
- "封面：`#ffffff`底，标题48px Super Sans VF weight 700，色`#292827`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#F8F9FA`底+`#dcd7d3`边框+16px圆角。标题24px weight 500 色`#292827`。正文18px weight 400 色`#6B7280`。"

### 品牌铁律
1. Verify font weight is 460 (not 400 or 500) for body and 540 for display — the non-standard weights are essential
2. Check that display line-height is 0.96 — if headlines look too spaced, they're wrong
3. Ensure buttons use Warm Cream (#e9e5dd) not pure white or gray — the warmth is subtle but critical
