---
name: "Lamborghini"
category: "Automotive"
description: "Supercar brand. True black surfaces, gold accents, dramatic uppercase typography."
colors:
  primary: "#917300"
  secondary: "#7D7D7D"
  accent: "#1EAEDB"
  background: "#FFFFFF"
  surface: "#000000"
  muted: "#7D7D7D"
  border: "#E5E7EB"
typography:
  display:
    fontFamily: LamboType
    fontSize: 3rem
    fontWeight: 600
    letterSpacing: -0.02em
  body:
    fontFamily: LamboType
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
  scenes: ["产品发布", "科技主题演讲"]
  posture: "宽松"
  accentBudget: 2
---

## Overview
Lamborghini's website is a cathedral of darkness — a digital stage where jet-black surfaces stretch infinitely and every element emerges from the void like a...

## Colors
primary(`#917300`)标题 | accent(`#1EAEDB`)强调 | bg(`#FFFFFF`)底色 | surface(`#000000`)卡片

## Typography
Display: LamboType | Body: LamboType | Mono: Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 120px | 400 | 0.92 | normal | 首页主标题 |
| 章节标题 | 32px | 500 | 1.1 | -0.5px | 分章标题 |
| 卡片标题 | 24px | 400 | 1.5 | normal | 内容卡标题 |
| 正文 | 18px | 400 | 1.56 | normal | 主要阅读 |
| 辅助文字 | 14px | 600 | 1.14 | -0.42px | 标注/脚注 |
| 数据标签 | 10px | 400 | 1.00 | 0.225px | 图表标签 |

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
- 标题: `#917300` | 正文: `#7D7D7D` | 强调: `#1EAEDB`
- 底色: `#FFFFFF` | 卡片: `#000000` | 边框: `#E5E7EB`

### SVG 组件示例
- "封面：`#FFFFFF`底，标题48px LamboType weight 600，色`#917300`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#000000`底+`#E5E7EB`边框+16px圆角。标题24px weight 500 色`#917300`。正文18px weight 400 色`#7D7D7D`。"

### 品牌铁律
1. Focus on ONE component at a time — Lamborghini's system is extreme and every element must feel aggressive
2. Reference specific color names and hex codes from this document — the palette has only about 5 active colors
3. Use natural language descriptions, not CSS values — "sharp-cut golden rectangle" not "border-radius: 0px; background: #FFC000"
