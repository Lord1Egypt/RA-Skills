---
name: "Kraken"
category: "Fintech & Crypto"
description: "Crypto trading. Purple-accented dark UI, data-dense dashboards."
colors:
  primary: "#5741d8"
  secondary: "#6B7280"
  accent: "#3B82F6"
  background: "#ffffff"
  surface: "#F8F9FA"
  muted: "#6B7280"
  border: "#dedee5"
typography:
  display:
    fontFamily: Kraken-Brand
    fontSize: 3rem
    fontWeight: 600
    letterSpacing: -0.02em
  body:
    fontFamily: Kraken-Product
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
  scenes: ["金融科技报告", "金融科技报告", "科技主题演讲"]
  posture: "紧凑"
  accentBudget: 2
---

## Overview
Kraken's website is a clean, trustworthy crypto exchange that uses purple as its commanding brand color.

## Colors
primary(`#5741d8`)标题 | accent(`#3B82F6`)强调 | bg(`#ffffff`)底色 | surface(`#F8F9FA`)卡片

## Typography
Display: Kraken-Brand | Body: Kraken-Product | Mono: Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 48px | 700 | 1.17 | -1px | 首页主标题 |
| 章节标题 | 36px | 700 | 1.22 | -0.5px | 分章标题 |
| 卡片标题 | 28px | 700 | 1.29 | -0.5px | 内容卡标题 |
| 正文 | 16px | 400 | 1.38 | normal | 主要阅读 |
| 辅助文字 | 12px | 400 | 1.33 | normal | 标注/脚注 |
| 数据标签 | 7px | 500 | 1.00 | normal | 图表标签 |

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
- 标题: `#5741d8` | 正文: `#6B7280` | 强调: `#3B82F6`
- 底色: `#ffffff` | 卡片: `#F8F9FA` | 边框: `#dedee5`

### SVG 组件示例
- "封面：`#ffffff`底，标题48px Kraken-Brand weight 600，色`#5741d8`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#F8F9FA`底+`#dedee5`边框+16px圆角。标题24px weight 500 色`#5741d8`。正文18px weight 400 色`#6B7280`。"

### 品牌铁律
1. 强调色(`#3B82F6`)每页不超过2处使用
2. 排版层次清晰，标题与正文对比明确
3. 保持品牌调性一致，避免混用风格
