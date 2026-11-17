---
name: "Revolut"
category: "Fintech & Crypto"
description: "Digital banking. Sleek dark interface, gradient cards, fintech precision."
colors:
  primary: "#191c1f"
  secondary: "#6B7280"
  accent: "#000000"
  background: "#ffffff"
  surface: "#f4f4f4"
  muted: "#6B7280"
  border: "#E5E7EB"
typography:
  display:
    fontFamily: Aeonik Pro
    fontSize: 3rem
    fontWeight: 600
    letterSpacing: -0.02em
  body:
    fontFamily: Inter
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
  scenes: ["金融科技报告", "金融科技报告", "科技主题演讲"]
  posture: "宽松"
  accentBudget: 2
---

## Overview
Revolut's website is fintech confidence distilled into pixels — a design system that communicates "your money is in capable hands" through massive typography...

## Colors
primary(`#191c1f`)标题 | accent(`#000000`)强调 | bg(`#ffffff`)底色 | surface(`#f4f4f4`)卡片

## Typography
Display: Aeonik Pro | Body: Aeonik Pro | Mono: Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 80px | 500 | 1.00 | -0.8px | 首页主标题 |
| 章节标题 | 48px | 500 | 1.21 | -0.48px | 分章标题 |
| 卡片标题 | 32px | 500 | 1.19 | -0.32px | 内容卡标题 |
| 正文 | 18px | 400 | 1.56 | -0.09px | 主要阅读 |
| 辅助文字 | 20px | 500 | 1.40 | normal | 标注/脚注 |
| 数据标签 | 12px | 500 | 1.3 | normal | 图表标签 |

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
- 标题: `#191c1f` | 正文: `#6B7280` | 强调: `#000000`
- 底色: `#ffffff` | 卡片: `#f4f4f4` | 边框: `#E5E7EB`

### SVG 组件示例
- "封面：`#ffffff`底，标题48px Aeonik Pro weight 600，色`#191c1f`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#f4f4f4`底+`#E5E7EB`边框+16px圆角。标题24px weight 500 色`#191c1f`。正文18px weight 400 色`#6B7280`。"

### 品牌铁律
1. Aeonik Pro 500 for headings — never bold
2. All buttons are pills (9999px) with generous padding
3. Zero shadows — flat is the Revolut identity
