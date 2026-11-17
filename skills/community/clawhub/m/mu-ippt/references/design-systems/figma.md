---
name: "Figma"
category: "Design & Creative"
description: "Collaborative design tool. Vibrant multi-color, playful yet professional."
colors:
  primary: "#1A1A1A"
  secondary: "#6B7280"
  accent: "#A259FF"
  background: "#ffffff"
  surface: "#F8F9FA"
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
    fontFamily: figmaMono
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
  scenes: ["设计提案"]
  posture: "紧凑"
  accentBudget: 2
---

## Overview
Figma's interface is the design tool that designed itself — a masterclass in typographic sophistication where a custom variable font (figmaSans) modulates be...

## Colors
primary(`#1A1A1A`)标题 | accent(`#A259FF`)强调 | bg(`#ffffff`)底色 | surface(`#F8F9FA`)卡片

## Typography
Display: figmaSans | Body: figmaSans | Mono: Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 48px | 600 | 1.0 | -1.0px | 首页主标题 |
| 章节标题 | 64px | 400 | 1.10 | -0.96px | 分章标题 |
| 卡片标题 | 26px | 540 | 1.35 | -0.26px | 内容卡标题 |
| 正文 | 20px | 330 | 1.30 | -0.1px | 主要阅读 |
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
- 标题: `#1A1A1A` | 正文: `#6B7280` | 强调: `#A259FF`
- 底色: `#ffffff` | 卡片: `#F8F9FA` | 边框: `#E5E7EB`

### SVG 组件示例
- "封面：`#ffffff`底，标题48px system-ui, sans-serif weight 600，色`#1A1A1A`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#F8F9FA`底+`#E5E7EB`边框+16px圆角。标题24px weight 500 色`#1A1A1A`。正文18px weight 400 色`#6B7280`。"

### 品牌铁律
1. Use variable font weight stops precisely: 320, 330, 340, 450, 480, 540, 700
2. Interface is always black + white — never add colors to chrome
3. Dashed focus outlines, not solid
