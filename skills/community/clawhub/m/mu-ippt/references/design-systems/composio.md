---
name: "Composio"
category: "Backend & Data"
description: "Tool integration platform. Modern dark with colorful integration icons."
colors:
  primary: "#1A1A1A"
  secondary: "#444444"
  accent: "#3B82F6"
  background: "#ffffff"
  surface: "#F8F9FA"
  muted: "#444444"
  border: "#e0e0e0"
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
    fontFamily: JetBrains Mono
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
  scenes: ["品牌演示", "科技主题演讲"]
  posture: "宽松"
  accentBudget: 2
---

## Overview
Composio's interface is a nocturnal command center — a dense, developer-focused darkness punctuated by electric cyan and deep cobalt signals.

## Colors
primary(`#1A1A1A`)标题 | accent(`#3B82F6`)强调 | bg(`#ffffff`)底色 | surface(`#F8F9FA`)卡片

## Typography
Display: abcDiatype | Body: abcDiatype | Mono: JetBrains Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 48px | 600 | 1.0 | -1.0px | 首页主标题 |
| 章节标题 | 48px | 400 | 1.00 | normal | 分章标题 |
| 卡片标题 | 24px | 500 | 1.20 | normal | 内容卡标题 |
| 正文 | 18px | 400 | 1.20 | normal | 主要阅读 |
| 辅助文字 | 14px | 400 | 1.63 | normal | 标注/脚注 |
| 数据标签 | 12px | 400 | 1.00 | 0.3px | 图表标签 |

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
- 标题: `#1A1A1A` | 正文: `#444444` | 强调: `#3B82F6`
- 底色: `#ffffff` | 卡片: `#F8F9FA` | 边框: `#e0e0e0`

### SVG 组件示例
- "封面：`#ffffff`底，标题48px system-ui, sans-serif weight 600，色`#1A1A1A`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#F8F9FA`底+`#e0e0e0`边框+16px圆角。标题24px weight 500 色`#1A1A1A`。正文18px weight 400 色`#444444`。"

### 品牌铁律
1. Focus on ONE component at a time
2. Reference specific color names and hex codes from this document — "use Ghost White (rgba(255,255,255,0.6))" not "make it lighter"
3. Use natural language descriptions — "make the border barely visible" = Border Mist 04-06
