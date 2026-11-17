---
name: "Expo"
category: "Developer Tools"
description: "React Native platform. Dark theme, tight letter-spacing, code-centric."
colors:
  primary: "#0d74ce"
  secondary: "#6B7280"
  accent: "#3B82F6"
  background: "#ffffff"
  surface: "#f0f0f3"
  muted: "#6B7280"
  border: "#e0e1e6"
typography:
  display:
    fontFamily: Inter
    fontSize: 3rem
    fontWeight: 600
    letterSpacing: -0.02em
  body:
    fontFamily: Inter
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
  scenes: ["技术演讲", "科技主题演讲"]
  posture: "宽松"
  accentBudget: 2
---

## Overview
Expo's interface is a luminous, confidence-radiating developer platform built on the premise that tools for building apps should feel as polished as the apps...

## Colors
primary(`#0d74ce`)标题 | accent(`#3B82F6`)强调 | bg(`#ffffff`)底色 | surface(`#f0f0f3`)卡片

## Typography
Display: Inter | Body: Inter | Mono: JetBrains Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 48px | 600 | 1.0 | -1.0px | 首页主标题 |
| 章节标题 | 48px | 600 | 1.10 | -2px | 分章标题 |
| 卡片标题 | 20px | 600 | 1.20 | -0.25px | 内容卡标题 |
| 正文 | 18px | 400 | 1.40 | normal | 主要阅读 |
| 辅助文字 | 14px | 400 | 1.4 | normal | 标注/脚注 |
| 数据标签 | 12px | 500 | 1.3 | normal | 图表标签 |

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
- 标题: `#0d74ce` | 正文: `#6B7280` | 强调: `#3B82F6`
- 底色: `#ffffff` | 卡片: `#f0f0f3` | 边框: `#e0e1e6`

### SVG 组件示例
- "封面：`#ffffff`底，标题48px Inter weight 600，色`#0d74ce`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#f0f0f3`底+`#e0e1e6`边框+16px圆角。标题24px weight 500 色`#0d74ce`。正文18px weight 400 色`#6B7280`。"

### 品牌铁律
1. Focus on ONE component at a time
2. Reference specific color names and hex codes — "use Slate Gray (#60646c)" not "make it gray"
3. Use radius values deliberately — 6px for buttons, 8px for cards, 24px for images, 9999px for pills
