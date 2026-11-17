---
name: "Cursor"
category: "Developer Tools"
description: "AI-first code editor. Sleek dark interface, gradient accents."
colors:
  primary: "#26251e"
  secondary: "#6B7280"
  accent: "#000000"
  background: "#ffffff"
  surface: "#f7f7f4"
  muted: "#6B7280"
  border: "#26251e"
typography:
  display:
    fontFamily: CursorGothic
    fontSize: 3rem
    fontWeight: 600
    letterSpacing: -0.02em
  body:
    fontFamily: jjannon
    fontSize: 1rem
    fontWeight: 400
  mono:
    fontFamily: berkeleyMono
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
Cursor's website is a study in warm minimalism meets code-editor elegance.

## Colors
primary(`#26251e`)标题 | accent(`#000000`)强调 | bg(`#ffffff`)底色 | surface(`#f7f7f4`)卡片

## Typography
Display: CursorGothic | Body: CursorGothic | Mono: Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 72px | 400 | 1.10 | -2.16px | 首页主标题 |
| 章节标题 | 36px | 400 | 1.20 | -0.72px | 分章标题 |
| 卡片标题 | 26px | 400 | 1.25 | -0.325px | 内容卡标题 |
| 正文 | 18px | 400 | 1.5 | normal | 主要阅读 |
| 辅助文字 | 11px | 400 | 1.50 | normal | 标注/脚注 |
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
- 标题: `#26251e` | 正文: `#6B7280` | 强调: `#000000`
- 底色: `#ffffff` | 卡片: `#f7f7f4` | 边框: `#26251e`

### SVG 组件示例
- "封面：`#ffffff`底，标题48px CursorGothic weight 600，色`#26251e`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#f7f7f4`底+`#26251e`边框+16px圆角。标题24px weight 500 色`#26251e`。正文18px weight 400 色`#6B7280`。"

### 品牌铁律
1. Always use warm tones -- `#f2f1ed` background, `#26251e` text, never pure white/black for primary surfaces
2. Letter-spacing scales with font size for CursorGothic: -2.16px at 72px, -0.72px at 36px, -0.325px at 26px, normal at 16px
3. Use `rgba(38, 37, 30, alpha)` as a CSS-compatible fallback for oklab borders
