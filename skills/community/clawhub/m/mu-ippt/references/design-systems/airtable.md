---
name: "Airtable"
category: "Design & Creative"
description: "Spreadsheet-database hybrid. Colorful, friendly, structured data aesthetic."
colors:
  primary: "#181d26"
  secondary: "#6B7280"
  accent: "#3B82F6"
  background: "#ffffff"
  surface: "#f8fafc"
  muted: "#6B7280"
  border: "#e0e2e6"
typography:
  display:
    fontFamily: Haas Groot Disp
    fontSize: 3rem
    fontWeight: 600
    letterSpacing: -0.02em
  body:
    fontFamily: Haas Groot Disp
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
  sm: 6px
  md: 12px
  lg: 24px
ppt:
  scenes: ["设计提案"]
  posture: "平衡"
  accentBudget: 2
---

## Overview
Airtable's website is a clean, enterprise-friendly platform that communicates "sophisticated simplicity" through a white canvas with deep navy text (`#181d26...

## Colors
primary(`#181d26`)标题 | accent(`#3B82F6`)强调 | bg(`#ffffff`)底色 | surface(`#f8fafc`)卡片

## Typography
Display: Haas | Body: Haas | Mono: Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 48px | 400 | 1.15 | normal | 首页主标题 |
| 章节标题 | 40px | 400 | 1.25 | normal | 分章标题 |
| 卡片标题 | 24px | 400 | 1.20 | 0.12px | 内容卡标题 |
| 正文 | 18px | 400 | 1.35 | 0.18px | 主要阅读 |
| 辅助文字 | 14px | 400 | 1.25 | 0.28px | 标注/脚注 |
| 数据标签 | 12px | 500 | 1.3 | normal | 图表标签 |

## Layout & Shapes
间距风格平衡，圆角直角/极小圆角。 小圆角矩形，保持克制的几何感。

## Elevation
扁平，不使用阴影。

## Components
标题卡(accent左边框) | 数据卡(surface底+数字突出) | 引用块(muted底+斜体)

## Do's and Don'ts
✅ accent≤2处/页，大面积留白 | ❌ 禁混用3+强调色，禁过度装饰

## Agent Prompt Guide

### 快速色板
- 标题: `#181d26` | 正文: `#6B7280` | 强调: `#3B82F6`
- 底色: `#ffffff` | 卡片: `#f8fafc` | 边框: `#e0e2e6`

### SVG 组件示例
- "封面：`#ffffff`底，标题48px Haas Groot Disp weight 600，色`#181d26`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#f8fafc`底+`#e0e2e6`边框+8px圆角。标题24px weight 500 色`#181d26`。正文18px weight 400 色`#6B7280`。"

### 品牌铁律
1. 强调色(`#3B82F6`)每页不超过2处使用
2. 排版层次清晰，标题与正文对比明确
3. 保持品牌调性一致，避免混用风格
