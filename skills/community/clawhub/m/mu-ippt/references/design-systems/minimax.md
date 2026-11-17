---
name: "Minimax"
category: "AI & LLM"
description: "AI model provider. Bold dark interface with neon accents."
colors:
  primary: "#ea5ec1"
  secondary: "#6B7280"
  accent: "#1456f0"
  background: "#ffffff"
  surface: "#F8F9FA"
  muted: "#6B7280"
  border: "#f2f3f5"
typography:
  display:
    fontFamily: Outfit
    fontSize: 3rem
    fontWeight: 700
    letterSpacing: -0.02em
  body:
    fontFamily: Outfit
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
  sm: 4px
  md: 8px
  lg: 16px
ppt:
  scenes: ["技术演讲", "科技主题演讲"]
  posture: "紧凑"
  accentBudget: 2
---

## Overview
MiniMax's website is a clean, product-showcase platform for a Chinese AI technology company that bridges consumer-friendly appeal with technical credibility.

## Colors
primary(`#ea5ec1`)标题 | accent(`#1456f0`)强调 | bg(`#ffffff`)底色 | surface(`#F8F9FA`)卡片

## Typography
Display: DM Sans | Body: DM Sans | Mono: Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 80px | 500 | 1.10 | 1.10px | 首页主标题 |
| 章节标题 | 31px | 600 | 1.50 | 1.50px | 分章标题 |
| 卡片标题 | 28px | 500 | 1.71 | 1.71px | 内容卡标题 |
| 正文 | 20px | 500 | 1.50 | 1.50px | 主要阅读 |
| 辅助文字 | 13px | 400 | 1.70 | 1.70px | 标注/脚注 |
| 数据标签 | 10px | 400 | 1.50 | 1.50px | 图表标签 |

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
- 标题: `#ea5ec1` | 正文: `#6B7280` | 强调: `#1456f0`
- 底色: `#ffffff` | 卡片: `#F8F9FA` | 边框: `#f2f3f5`

### SVG 组件示例
- "封面：`#ffffff`底，标题48px Outfit weight 700，色`#ea5ec1`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#F8F9FA`底+`#f2f3f5`边框+16px圆角。标题24px weight 500 色`#ea5ec1`。正文18px weight 400 色`#6B7280`。"

### 品牌铁律
1. Start with white — color comes from product cards and illustrations only
2. Pill buttons (9999px) for nav/tabs, standard radius (8px) for CTA buttons
3. Purple-tinted shadows for featured cards, neutral shadows for everything else
