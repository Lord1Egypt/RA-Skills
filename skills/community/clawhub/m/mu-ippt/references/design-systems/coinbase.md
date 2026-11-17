---
name: "Coinbase"
category: "Fintech & Crypto"
description: "Crypto exchange. Clean blue identity, trust-focused, institutional feel."
colors:
  primary: "#0667d0"
  secondary: "#5b616e"
  accent: "#0052FF"
  background: "#ffffff"
  surface: "#eef0f3"
  muted: "#5b616e"
  border: "#E5E7EB"
typography:
  display:
    fontFamily: CoinbaseDisplay
    fontSize: 3rem
    fontWeight: 600
    letterSpacing: -0.02em
  body:
    fontFamily: CoinbaseText
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
  scenes: ["金融科技报告", "金融科技报告", "科技主题演讲"]
  posture: "平衡"
  accentBudget: 2
---

## Overview
Coinbase's website is a clean, trustworthy crypto platform that communicates financial reliability through a blue-and-white binary palette.

## Colors
primary(`#0667d0`)标题 | accent(`#0052FF`)强调 | bg(`#ffffff`)底色 | surface(`#eef0f3`)卡片

## Typography
Display: CoinbaseDisplay | Body: CoinbaseText | Mono: Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 80px | 400 | 1.00 | 1.00px | 首页主标题 |
| 章节标题 | 36px | 400 | 1.11 | 1.11px | 分章标题 |
| 卡片标题 | 32px | 400 | 1.13 | 1.13px | 内容卡标题 |
| 正文 | 18px | 400 | 1.56 | 1.56px | 主要阅读 |
| 辅助文字 | 13px | 600 | 1.23 | 1.23px | 标注/脚注 |
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
- 标题: `#0667d0` | 正文: `#5b616e` | 强调: `#0052FF`
- 底色: `#ffffff` | 卡片: `#eef0f3` | 边框: `#E5E7EB`

### SVG 组件示例
- "封面：`#ffffff`底，标题48px CoinbaseDisplay weight 600，色`#0667d0`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#eef0f3`底+`#E5E7EB`边框+16px圆角。标题24px weight 500 色`#0667d0`。正文18px weight 400 色`#5b616e`。"

### 品牌铁律
1. 强调色(`#0052FF`)每页不超过2处使用
2. 排版层次清晰，标题与正文对比明确
3. 保持品牌调性一致，避免混用风格
