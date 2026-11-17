---
name: "Voltagent"
category: "AI & LLM"
description: "AI agent framework. Void-black canvas, emerald accent, terminal-native."
colors:
  primary: "#ffffff"
  secondary: "#4f5d75"
  accent: "#306cce"
  background: "#f2f2f2"
  surface: "#818cf8"
  muted: "#4f5d75"
  border: "#3d3a39"
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
  scenes: ["技术演讲", "科技主题演讲"]
  posture: "宽松"
  accentBudget: 2
---

## Overview
VoltAgent's interface is a deep-space command terminal for the AI age — a developer-facing darkness built on near-pure-black surfaces (`#050507`) where the o...

## Colors
primary(`#ffffff`)标题 | accent(`#306cce`)强调 | bg(`#f2f2f2`)底色 | surface(`#818cf8`)卡片

## Typography
Display: Inter | Body: Inter | Mono: Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 48px | 600 | 1.0 | -1.0px | 首页主标题 |
| 章节标题 | 36px | 400 | 1.11 | -0.9px | 分章标题 |
| 卡片标题 | 24px | 700 | 1.33 | -0.6px | 内容卡标题 |
| 正文 | 18px | 400 | 1.5 | normal | 主要阅读 |
| 辅助文字 | 45px | 500 | 1.65 | normal | 标注/脚注 |
| 数据标签 | 12px | 400 | 1.33 | normal | 图表标签 |

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
- 标题: `#ffffff` | 正文: `#4f5d75` | 强调: `#306cce`
- 底色: `#f2f2f2` | 卡片: `#818cf8` | 边框: `#3d3a39`

### SVG 组件示例
- "封面：`#f2f2f2`底，标题48px Inter weight 600，色`#ffffff`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#818cf8`底+`#3d3a39`边框+16px圆角。标题24px weight 500 色`#ffffff`。正文18px weight 400 色`#4f5d75`。"

### 品牌铁律
1. Focus on ONE component at a time
2. Reference specific color names and hex codes — "use Warm Parchment (#b8b3b0)" not "make it lighter"
3. Use border treatment to communicate elevation: "change the border to 2px solid Emerald Signal Green (#00d992)" for emphasis
