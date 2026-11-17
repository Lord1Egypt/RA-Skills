---
name: "Replicate"
category: "AI & LLM"
description: "Run ML models via API. Clean white canvas, code-forward."
colors:
  primary: "#202020"
  secondary: "#6B7280"
  accent: "#3B82F6"
  background: "#ffffff"
  surface: "#F8F9FA"
  muted: "#6B7280"
  border: "#E5E7EB"
typography:
  display:
    fontFamily: rb-freigeist-neue
    fontSize: 3rem
    fontWeight: 600
    letterSpacing: -0.02em
  body:
    fontFamily: basier-square
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
Replicate's interface is a developer playground crackling with creative energy — a bold, high-contrast design that feels more like a music festival poster th...

## Colors
primary(`#202020`)标题 | accent(`#3B82F6`)强调 | bg(`#ffffff`)底色 | surface(`#F8F9FA`)卡片

## Typography
Display: rb-freigeist-neue | Body: rb-freigeist-neue | Mono: jetbrains-mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 48px | 600 | 1.0 | -1.0px | 首页主标题 |
| 章节标题 | 48px | 400 | 1.00 | normal | 分章标题 |
| 卡片标题 | 30px | 600 | 1.20 | normal | 内容卡标题 |
| 正文 | 20px | 400 | 1.40 | normal | 主要阅读 |
| 辅助文字 | 14px | 400 | 1.43 | -0.35px | 标注/脚注 |
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
- 标题: `#202020` | 正文: `#6B7280` | 强调: `#3B82F6`
- 底色: `#ffffff` | 卡片: `#F8F9FA` | 边框: `#E5E7EB`

### SVG 组件示例
- "封面：`#ffffff`底，标题48px rb-freigeist-neue weight 600，色`#202020`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#F8F9FA`底+`#E5E7EB`边框+16px圆角。标题24px weight 500 色`#202020`。正文18px weight 400 色`#6B7280`。"

### 品牌铁律
1. Everything is pill-shaped — never specify any other border-radius
2. Display text is HEAVY — weight 700, sizes 48px+
3. Links use dotted underline (#bbbbbb) — never solid
