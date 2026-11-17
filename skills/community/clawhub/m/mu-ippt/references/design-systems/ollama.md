---
name: "Ollama"
category: "AI & LLM"
description: "Run LLMs locally. Terminal-first, monochrome simplicity."
colors:
  primary: "#090909"
  secondary: "#6B7280"
  accent: "#3B82F6"
  background: "#ffffff"
  surface: "#090909"
  muted: "#6B7280"
  border: "#d4d4d4"
typography:
  display:
    fontFamily: SF Pro Rounded
    fontSize: 3rem
    fontWeight: 600
    letterSpacing: -0.02em
  body:
    fontFamily: ui-sans-serif
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
  scenes: ["技术演讲"]
  posture: "平衡"
  accentBudget: 2
---

## Overview
Ollama's interface is radical minimalism taken to its logical conclusion — a pure-white void where content floats without decoration, shadow, or color.

## Colors
primary(`#090909`)标题 | accent(`#3B82F6`)强调 | bg(`#ffffff`)底色 | surface(`#090909`)卡片

## Typography
Display: SF Pro Rounded | Body: SF Pro Rounded | Mono: Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 48px | 600 | 1.0 | -1.0px | 首页主标题 |
| 章节标题 | 36px | 500 | 1.11 | normal | 分章标题 |
| 卡片标题 | 24px | 400 | 1.33 | normal | 内容卡标题 |
| 正文 | 18px | 400 | 1.56 | normal | 主要阅读 |
| 辅助文字 | 12px | 400 | 1.33 | normal | 标注/脚注 |
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
- 标题: `#090909` | 正文: `#6B7280` | 强调: `#3B82F6`
- 底色: `#ffffff` | 卡片: `#090909` | 边框: `#d4d4d4`

### SVG 组件示例
- "封面：`#ffffff`底，标题48px SF Pro Rounded weight 600，色`#090909`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#090909`底+`#d4d4d4`边框+16px圆角。标题24px weight 500 色`#090909`。正文18px weight 400 色`#6B7280`。"

### 品牌铁律
1. Focus on ONE component at a time
2. Keep all values grayscale — "Stone (#737373)" not "use a light color"
3. Always specify pill (9999px) or container (12px) radius — nothing in between
