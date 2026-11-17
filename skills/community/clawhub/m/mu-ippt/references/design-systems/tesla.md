---
name: "Tesla"
category: "Automotive"
description: "Electric automotive. Radical subtraction, full-viewport photography, near-zero UI."
colors:
  primary: "#171A20"
  secondary: "#F4F4F4"
  accent: "#3E6AE1"
  background: "#FFFFFF"
  surface: "#EEEEEE"
  muted: "#F4F4F4"
  border: "#E5E7EB"
typography:
  display:
    fontFamily: Universal Sans Display
    fontSize: 3rem
    fontWeight: 700
    letterSpacing: -0.02em
  body:
    fontFamily: Universal Sans Text
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
  sm: 6px
  md: 12px
  lg: 24px
ppt:
  scenes: ["产品发布", "科技主题演讲"]
  posture: "平衡"
  accentBudget: 2
---

## Overview
Tesla's website is an exercise in radical subtraction — a digital showroom where the product is everything and the interface is almost nothing.

## Colors
primary(`#171A20`)标题 | accent(`#3E6AE1`)强调 | bg(`#FFFFFF`)底色 | surface(`#EEEEEE`)卡片

## Typography
Display: Universal Sans Display | Body: Universal Sans Display | Mono: Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 48px | 600 | 1.0 | -1.0px | 首页主标题 |
| 章节标题 | 32px | 500 | 1.1 | -0.5px | 分章标题 |
| 卡片标题 | 24px | 500 | 1.2 | -0.2px | 内容卡标题 |
| 正文 | 18px | 400 | 1.5 | normal | 主要阅读 |
| 辅助文字 | 14px | 500 | 16.8 | normal | 标注/脚注 |
| 数据标签 | 12px | 500 | 1.3 | normal | 图表标签 |

## Layout & Shapes
间距风格平衡，圆角全圆角/胶囊。 全圆角胶囊形按钮与标签，卡片使用大圆角。

## Elevation
扁平，不使用阴影。

## Components
标题卡(accent左边框) | 数据卡(surface底+数字突出) | 引用块(muted底+斜体)

## Do's and Don'ts
✅ accent≤2处/页，大面积留白 | ❌ 禁混用3+强调色，禁过度装饰

## Agent Prompt Guide

### 快速色板
- 标题: `#171A20` | 正文: `#F4F4F4` | 强调: `#3E6AE1`
- 底色: `#FFFFFF` | 卡片: `#EEEEEE` | 边框: `#E5E7EB`

### SVG 组件示例
- "封面：`#FFFFFF`底，标题48px Universal Sans Display weight 700，色`#171A20`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#EEEEEE`底+`#E5E7EB`边框+16px圆角。标题24px weight 500 色`#171A20`。正文18px weight 400 色`#F4F4F4`。"

### 品牌铁律
1. Focus on ONE component at a time — Tesla's system is so minimal that each element must be pixel-perfect
2. Reference specific color names and hex codes from this document — there are only 6-7 colors in the entire system
3. Use natural language descriptions, not CSS values — "barely rounded corners" not "border-radius: 4px"
