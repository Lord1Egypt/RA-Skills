---
name: "Sanity"
category: "Backend & Data"
description: "Headless CMS. Red accent, content-first editorial layout."
colors:
  primary: "#212121"
  secondary: "#6B7280"
  accent: "#19d600"
  background: "#ffffff"
  surface: "#F8F9FA"
  muted: "#6B7280"
  border: "#0b0b0b"
typography:
  display:
    fontFamily: waldenburgNormal
    fontSize: 3rem
    fontWeight: 600
    letterSpacing: -0.02em
  body:
    fontFamily: waldenburgNormal
    fontSize: 1rem
    fontWeight: 400
  mono:
    fontFamily: IBM Plex Mono
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
Sanity's website is a developer-content platform rendered as a nocturnal command center -- dark, precise, and deeply structured.

## Colors
primary(`#212121`)标题 | accent(`#19d600`)强调 | bg(`#ffffff`)底色 | surface(`#F8F9FA`)卡片

## Typography
Display: waldenburgNormal | Body: waldenburgNormal | Mono: Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 48px | 600 | 1.0 | -1.0px | 首页主标题 |
| 章节标题 | 48px | 400 | 1.08 | -1.68px | 分章标题 |
| 卡片标题 | 24px | 500 | 1.2 | -0.2px | 内容卡标题 |
| 正文 | 18px | 400 | 1.50 | -0.18px | 主要阅读 |
| 辅助文字 | 13px | 400 | 1.30 | -0.13px | 标注/脚注 |
| 数据标签 | 11px | 500 | 1.00 | normal | 图表标签 |

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
- 标题: `#212121` | 正文: `#6B7280` | 强调: `#19d600`
- 底色: `#ffffff` | 卡片: `#F8F9FA` | 边框: `#0b0b0b`

### SVG 组件示例
- "封面：`#ffffff`底，标题48px waldenburgNormal weight 600，色`#212121`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#F8F9FA`底+`#0b0b0b`边框+16px圆角。标题24px weight 500 色`#212121`。正文18px weight 400 色`#6B7280`。"

### 品牌铁律
1. **Start dark**: Begin with `#0b0b0b` background, `#ffffff` primary text, `#b9b9b9` secondary text
2. **Add structure**: Use `#212121` surfaces and `#353535` borders for containment -- no shadows
3. **Apply typography**: Inter (or Space Grotesk) with tight letter-spacing on headings, 1.50 line-height on body
