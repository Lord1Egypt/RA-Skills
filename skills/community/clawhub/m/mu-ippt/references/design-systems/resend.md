---
name: "Resend"
category: "Productivity & SaaS"
description: "Email API. Minimal dark theme, monospace accents."
colors:
  primary: "#464a4d"
  secondary: "#6B7280"
  accent: "#000000"
  background: "#f0f0f0"
  surface: "#e5e6e6"
  muted: "#6B7280"
  border: "#eaeaea"
typography:
  display:
    fontFamily: domaine
    fontSize: 3rem
    fontWeight: 600
    letterSpacing: -0.02em
  body:
    fontFamily: inter
    fontSize: 1rem
    fontWeight: 400
  mono:
    fontFamily: commitMono
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
  scenes: ["产品介绍", "效率工具演示", "编辑风格汇报"]
  posture: "紧凑"
  accentBudget: 2
---

## Overview
Resend's website is a dark, cinematic canvas that treats email infrastructure like a luxury product.

## Colors
primary(`#464a4d`)标题 | accent(`#000000`)强调 | bg(`#f0f0f0`)底色 | surface(`#e5e6e6`)卡片

## Typography
Display: domaine | Body: Helvetica | Mono: commitMono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 96px | 400 | 1.00 | -0.96px | 首页主标题 |
| 章节标题 | 56px | 400 | 1.20 | -2.8px | 分章标题 |
| 卡片标题 | 20px | 400 | 1.30 | normal | 内容卡标题 |
| 正文 | 18px | 400 | 1.50 | normal | 主要阅读 |
| 辅助文字 | 12px | 400 | 1.33 | normal | 标注/脚注 |
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
- 标题: `#464a4d` | 正文: `#6B7280` | 强调: `#000000`
- 底色: `#f0f0f0` | 卡片: `#e5e6e6` | 边框: `#eaeaea`

### SVG 组件示例
- "封面：`#f0f0f0`底，标题48px domaine weight 600，色`#464a4d`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#e5e6e6`底+`#eaeaea`边框+16px圆角。标题24px weight 500 色`#464a4d`。正文18px weight 400 色`#6B7280`。"

### 品牌铁律
1. Start with pure black — everything floats in the void
2. Frost borders (`rgba(214, 235, 253, 0.19)`) are the universal structural element — not gray, not neutral
3. Three fonts, three roles: Domaine (hero), ABC Favorit (sections), Inter (body) — never cross
