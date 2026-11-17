---
name: "Clay"
category: "Design & Creative"
description: "Creative agency. Organic shapes, soft gradients, art-directed layout."
colors:
  primary: "#333333"
  secondary: "#6B7280"
  accent: "#3B82F6"
  background: "#ffffff"
  surface: "#F8F9FA"
  muted: "#6B7280"
  border: "#dad4c8"
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
    fontFamily: Space Mono
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
  scenes: ["设计提案", "编辑风格汇报"]
  posture: "紧凑"
  accentBudget: 2
---

## Overview
Clay's website is a warm, playful celebration of color that treats B2B data enrichment like a craft rather than an enterprise chore.

## Colors
primary(`#333333`)标题 | accent(`#3B82F6`)强调 | bg(`#ffffff`)底色 | surface(`#F8F9FA`)卡片

## Typography
Display: Roobert | Body: Roobert | Mono: Space Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 80px | 600 | 1.00 | -3.2px | 首页主标题 |
| 章节标题 | 44px | 600 | 1.10 | -0.88px | 分章标题 |
| 卡片标题 | 20px | 500 | 1.50 | -0.16px | 内容卡标题 |
| 正文 | 20px | 400 | 1.40 | normal | 主要阅读 |
| 辅助文字 | 12px | 400 | 1.50 | normal | 标注/脚注 |
| 数据标签 | 6px | 600 | 1.5 | normal | 图表标签 |

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
- 标题: `#333333` | 正文: `#6B7280` | 强调: `#3B82F6`
- 底色: `#ffffff` | 卡片: `#F8F9FA` | 边框: `#dad4c8`

### SVG 组件示例
- "封面：`#ffffff`底，标题48px system-ui, sans-serif weight 600，色`#333333`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#F8F9FA`底+`#dad4c8`边框+16px圆角。标题24px weight 500 色`#333333`。正文18px weight 400 色`#6B7280`。"

### 品牌铁律
1. Start with warm cream (#faf9f7) — never cool white
2. Swatch colors are for full sections, not small accents — go bold with matcha, slushie, ube
3. Oat borders (#dad4c8) everywhere — dashed variants for decoration
