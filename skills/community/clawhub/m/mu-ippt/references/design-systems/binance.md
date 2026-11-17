---
name: "Binance"
category: "Fintech & Crypto"
description: "Crypto exchange. Bold yellow accent on monochrome, trading-floor urgency."
colors:
  primary: "#222126"
  secondary: "#32313A"
  accent: "#F0B90B"
  background: "#FFFFFF"
  surface: "#2B2F36"
  muted: "#32313A"
  border: "#E6E8EA"
typography:
  display:
    fontFamily: system-ui, sans-serif
    fontSize: 3rem
    fontWeight: 700
    letterSpacing: -0.02em
  body:
    fontFamily: system-ui, sans-serif
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
Binance.US radiates the polished urgency of a digital trading floor — a space where money moves and decisions happen in seconds.

## Colors
primary(`#222126`)标题 | accent(`#F0B90B`)强调 | bg(`#FFFFFF`)底色 | surface(`#2B2F36`)卡片

## Typography
Display: BinancePlex | Body: BinancePlex | Mono: Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 60px | 700 | 1.08 | normal | 首页主标题 |
| 章节标题 | 28px | 500 | 1.00 | normal | 分章标题 |
| 卡片标题 | 24px | 700 | 1.00 | normal | 内容卡标题 |
| 正文 | 20px | 500 | 1.50 | normal | 主要阅读 |
| 辅助文字 | 12px | 600 | 1.00 | normal | 标注/脚注 |
| 数据标签 | 11px | 500 | 1.00 | normal | 图表标签 |

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
- 标题: `#222126` | 正文: `#32313A` | 强调: `#F0B90B`
- 底色: `#FFFFFF` | 卡片: `#2B2F36` | 边框: `#E6E8EA`

### SVG 组件示例
- "封面：`#FFFFFF`底，标题48px system-ui, sans-serif weight 700，色`#222126`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#2B2F36`底+`#E6E8EA`边框+16px圆角。标题24px weight 500 色`#222126`。正文18px weight 400 色`#32313A`。"

### 品牌铁律
1. Focus on ONE component at a time
2. Reference specific color names and hex codes from this document
3. Remember: Binance Yellow (#F0B90B) is the ONLY accent color — everything else is grey/dark/white
