---
name: "Intercom"
category: "Productivity & SaaS"
description: "Customer messaging. Friendly blue palette, conversational UI patterns."
colors:
  primary: "#ff2067"
  secondary: "#9c9fa5"
  accent: "#3B82F6"
  background: "#ffffff"
  surface: "#F8F9FA"
  muted: "#9c9fa5"
  border: "#dedbd6"
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
    fontFamily: SaansMono
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
  scenes: ["产品介绍", "效率工具演示", "编辑风格汇报"]
  posture: "平衡"
  accentBudget: 2
---

## Overview
Intercom's website is a warm, confident customer service platform that communicates "AI-first helpdesk" through a clean, editorial design language.

## Colors
primary(`#ff2067`)标题 | accent(`#3B82F6`)强调 | bg(`#ffffff`)底色 | surface(`#F8F9FA`)卡片

## Typography
Display: Saans | Body: MediumLL | Mono: SaansMono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 80px | 400 | 1.00 | -2.4px | 首页主标题 |
| 章节标题 | 54px | 400 | 1.00 | -1.6px | 分章标题 |
| 卡片标题 | 32px | 400 | 1.00 | -0.96px | 内容卡标题 |
| 正文 | 16px | 400 | 1.50 | normal | 主要阅读 |
| 辅助文字 | 18px | 400 | 1.00 | normal | 标注/脚注 |
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
- 标题: `#ff2067` | 正文: `#9c9fa5` | 强调: `#3B82F6`
- 底色: `#ffffff` | 卡片: `#F8F9FA` | 边框: `#dedbd6`

### SVG 组件示例
- "封面：`#ffffff`底，标题48px system-ui, sans-serif weight 600，色`#ff2067`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#F8F9FA`底+`#dedbd6`边框+8px圆角。标题24px weight 500 色`#ff2067`。正文18px weight 400 色`#9c9fa5`。"

### 品牌铁律
1. 强调色(`#3B82F6`)每页不超过2处使用
2. 排版层次清晰，标题与正文对比明确
3. 保持品牌调性一致，避免混用风格
