---
name: "Default"
category: "Starter"
description: "A clean, product-oriented default. Use when the brief doesn't call for a"
colors:
  primary: "#111111"
  secondary: "#6B6B6B"
  accent: "#2F6FEB"
  background: "#FAFAFA"
  surface: "#FFFFFF"
  muted: "#6B6B6B"
  border: "#E5E5E5"
typography:
  display:
    fontFamily: system-ui, sans-serif
    fontSize: 3rem
    fontWeight: 600
    letterSpacing: -0.02em
  body:
    fontFamily: system-ui, sans-serif
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
  scenes: ["品牌演示"]
  posture: "平衡"
  accentBudget: 2
---

## Overview
简洁产品风格默认方案，适用于无特定品牌要求的通用场景。

## Colors
primary(`#111111`)标题 | accent(`#2F6FEB`)强调 | bg(`#FAFAFA`)底色 | surface(`#FFFFFF`)卡片

## Typography
Display: Inter | Body: Inter | Mono: Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 48px | 600 | 1.0 | -1.0px | 首页主标题 |
| 章节标题 | 32px | 500 | 1.1 | -0.5px | 分章标题 |
| 卡片标题 | 24px | 500 | 1.2 | -0.2px | 内容卡标题 |
| 正文 | 18px | 400 | 1.5 | normal | 主要阅读 |
| 辅助文字 | 14px | 400 | 1.4 | normal | 标注/脚注 |
| 数据标签 | 12px | 500 | 1.3 | normal | 图表标签 |

## Layout & Shapes
间距风格平衡，圆角小圆角（4-8px）。 小圆角矩形，保持克制的几何感。

## Elevation
扁平，不使用阴影。

## Components
标题卡(accent左边框) | 数据卡(surface底+数字突出) | 引用块(muted底+斜体)

## Do's and Don'ts
✅ accent≤2处/页，大面积留白 | ❌ 禁混用3+强调色，禁过度装饰

## Agent Prompt Guide

### 快速色板
- 标题: `#111111` | 正文: `#6B6B6B` | 强调: `#2F6FEB`
- 底色: `#FAFAFA` | 卡片: `#FFFFFF` | 边框: `#E5E5E5`

### SVG 组件示例
- "封面：`#FAFAFA`底，标题48px system-ui, sans-serif weight 600，色`#111111`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#FFFFFF`底+`#E5E5E5`边框+8px圆角。标题24px weight 500 色`#111111`。正文18px weight 400 色`#6B6B6B`。"

### 品牌铁律
1. 强调色(`#2F6FEB`)每页不超过2处使用
2. 排版层次清晰，标题与正文对比明确
3. 保持品牌调性一致，避免混用风格
