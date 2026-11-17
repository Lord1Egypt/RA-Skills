---
name: "Stripe"
category: "Fintech & Crypto"
description: "Payment infrastructure. Signature purple gradients, weight-300 elegance."
colors:
  primary: "#061b31"
  secondary: "#64748d"
  accent: "#533afd"
  background: "#ffffff"
  surface: "#d6d9fc"
  muted: "#64748d"
  border: "#e5edf5"
typography:
  display:
    fontFamily: SF Pro Display
    fontSize: 3rem
    fontWeight: 300
    letterSpacing: -0.02em
  body:
    fontFamily: SF Pro Display
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
  scenes: ["金融科技报告", "金融科技报告", "编辑风格汇报"]
  posture: "紧凑"
  accentBudget: 2
---

## Overview
Stripe's website is the gold standard of fintech design -- a system that manages to feel simultaneously technical and luxurious, precise and warm.

## Colors
primary(`#061b31`)标题 | accent(`#533afd`)强调 | bg(`#ffffff`)底色 | surface(`#d6d9fc`)卡片

## Typography
Display: sohne-var | Body: sohne-var | Mono: SourceCodePro

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 48px | 300 | 1.15 | -0.96px | 首页主标题 |
| 章节标题 | 32px | 300 | 1.10 | -0.64px | 分章标题 |
| 卡片标题 | 22px | 300 | 1.10 | -0.22px | 内容卡标题 |
| 正文 | 18px | 300 | 1.40 | normal | 主要阅读 |
| 辅助文字 | 13px | 400 | 1.5 | normal | 标注/脚注 |
| 数据标签 | 10px | 300 | 1.15 | 0.1px | 图表标签 |

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
- 标题: `#061b31` | 正文: `#64748d` | 强调: `#533afd`
- 底色: `#ffffff` | 卡片: `#d6d9fc` | 边框: `#e5edf5`

### SVG 组件示例
- "封面：`#ffffff`底，标题48px SF Pro Display weight 300，色`#061b31`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#d6d9fc`底+`#e5edf5`边框+16px圆角。标题24px weight 500 色`#061b31`。正文18px weight 400 色`#64748d`。"

### 品牌铁律
1. Always enable `font-feature-settings: "ss01"` on sohne-var text -- this is the brand's typographic DNA
2. Weight 300 is the default; use 400 only for buttons/links/navigation
3. Shadow formula: `rgba(50,50,93,0.25) 0px Y1 B1 -S1, rgba(0,0,0,0.1) 0px Y2 B2 -S2` where Y1/B1 are larger (far shadow) and Y2/B2 are smaller (near shadow)
