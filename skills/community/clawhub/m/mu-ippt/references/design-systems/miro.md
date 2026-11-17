---
name: "Miro"
category: "Design & Creative"
description: "Visual collaboration. Bright yellow accent, infinite canvas aesthetic."
colors:
  primary: "#600000"
  secondary: "#6B7280"
  accent: "#FFD02F"
  background: "#ffffff"
  surface: "#F8F9FA"
  muted: "#6B7280"
  border: "#c7cad5"
typography:
  display:
    fontFamily: Roobert PRO Medium
    fontSize: 3rem
    fontWeight: 600
    letterSpacing: -0.02em
  body:
    fontFamily: Noto Sans
    fontSize: 1rem
    fontWeight: 400
  mono:
    fontFamily: ui-monospace, monospace
    fontSize: 0.875rem
rounded:
  sm: 4px
  md: 8px
  lg: 16px
spacing:
  sm: 8px
  md: 16px
  lg: 32px
ppt:
  scenes: ["设计提案", "科技主题演讲"]
  posture: "宽松"
  accentBudget: 2
---

## Overview
Miro's website is a clean, collaborative-tool-forward platform that communicates "visual thinking" through generous whitespace, pastel accent colors, and a c...

## Colors
primary(`#600000`)标题 | accent(`#FFD02F`)强调 | bg(`#ffffff`)底色 | surface(`#F8F9FA`)卡片

## Typography
Display: Roobert PRO Medium | Body: Noto Sans | Mono: Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 56px | 400 | 1.15 | -1.68px | 首页主标题 |
| 章节标题 | 48px | 400 | 1.15 | -1.44px | 分章标题 |
| 卡片标题 | 24px | 400 | 1.15 | -0.72px | 内容卡标题 |
| 正文 | 18px | 400 | 1.45 | normal | 主要阅读 |
| 辅助文字 | 12px | 400 | 1.15 | -0.36px | 标注/脚注 |
| 数据标签 | 5px | 400 | 0.90 | normal | 图表标签 |

## Layout & Shapes
间距风格宽松，圆角小圆角（4-8px）。 小圆角矩形，保持克制的几何感。

## Elevation
扁平，不使用阴影。

## Components
标题卡(accent左边框) | 数据卡(surface底+数字突出) | 引用块(muted底+斜体)

## Do's and Don'ts
✅ accent≤2处/页，大面积留白 | ❌ 禁混用3+强调色，禁过度装饰

## Agent Prompt Guide

### 快速色板
- 标题: `#600000` | 正文: `#6B7280` | 强调: `#FFD02F`
- 底色: `#ffffff` | 卡片: `#F8F9FA` | 边框: `#c7cad5`

### SVG 组件示例
- "封面：`#ffffff`底，标题48px Roobert PRO Medium weight 600，色`#600000`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#F8F9FA`底+`#c7cad5`边框+8px圆角。标题24px weight 500 色`#600000`。正文18px weight 400 色`#6B7280`。"

### 品牌铁律
1. 强调色(`#FFD02F`)每页不超过2处使用
2. 排版层次清晰，标题与正文对比明确
3. 保持品牌调性一致，避免混用风格
