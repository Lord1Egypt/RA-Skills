---
name: "Nvidia"
category: "Media & Consumer"
description: "GPU computing. Green-black energy, technical power aesthetic."
colors:
  primary: "#ffffff"
  secondary: "#a7a7a7"
  accent: "#76B900"
  background: "#ffffff"
  surface: "#000000"
  muted: "#a7a7a7"
  border: "#5e5e5e"
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
  sm: 4px
  md: 8px
  lg: 16px
ppt:
  scenes: ["内容营销", "消费品推广", "科技主题演讲"]
  posture: "紧凑"
  accentBudget: 2
---

## Overview
NVIDIA's website is a high-contrast, technology-forward experience that communicates raw computational power through design restraint.

## Colors
primary(`#ffffff`)标题 | accent(`#76B900`)强调 | bg(`#ffffff`)底色 | surface(`#000000`)卡片

## Typography
Display: NVIDIA-EMEA | Body: NVIDIA-EMEA | Mono: Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 36px | 700 | 1.25 | normal | 首页主标题 |
| 章节标题 | 24px | 700 | 1.25 | normal | 分章标题 |
| 卡片标题 | 20px | 700 | 1.25 | normal | 内容卡标题 |
| 正文 | 18px | 700 | 1.67 | normal | 主要阅读 |
| 辅助文字 | 14px | 600 | 1.50 | normal | 标注/脚注 |
| 数据标签 | 10px | 700 | 1.50 | normal | 图表标签 |

## Layout & Shapes
间距风格紧凑，圆角直角/极小圆角。 小圆角矩形，保持克制的几何感。

## Elevation
扁平，不使用阴影。

## Components
标题卡(accent左边框) | 数据卡(surface底+数字突出) | 引用块(muted底+斜体)

## Do's and Don'ts
✅ accent≤2处/页，大面积留白 | ❌ 禁混用3+强调色，禁过度装饰

## Agent Prompt Guide

### 快速色板
- 标题: `#ffffff` | 正文: `#a7a7a7` | 强调: `#76B900`
- 底色: `#ffffff` | 卡片: `#000000` | 边框: `#5e5e5e`

### SVG 组件示例
- "封面：`#ffffff`底，标题48px system-ui, sans-serif weight 600，色`#ffffff`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#000000`底+`#5e5e5e`边框+8px圆角。标题24px weight 500 色`#ffffff`。正文18px weight 400 色`#a7a7a7`。"

### 品牌铁律
1. Always use `#76b900` as accent, never as a background fill -- it's a signal color for borders, underlines, and highlights
2. Buttons are transparent with green borders by default -- filled backgrounds appear only on hover/active states
3. Weight 700 is the dominant voice for all interactive and heading elements; 400 is only for body paragraphs
