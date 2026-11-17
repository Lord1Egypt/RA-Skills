---
name: "Vercel"
category: "Developer Tools"
description: "Frontend deployment. Black and white precision, Geist font."
colors:
  primary: "#de1d8d"
  secondary: "#171717"
  accent: "#000000"
  background: "#ffffff"
  surface: "#F8F9FA"
  muted: "#171717"
  border: "#E5E7EB"
typography:
  display:
    fontFamily: Geist
    fontSize: 3rem
    fontWeight: 600
    letterSpacing: -0.02em
  body:
    fontFamily: Geist Mono
    fontSize: 1rem
    fontWeight: 400
  mono:
    fontFamily: Geist Mono
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
Vercel's website is the visual thesis of developer infrastructure made invisible — a design system so restrained it borders on philosophical.

## Colors
primary(`#de1d8d`)标题 | accent(`#000000`)强调 | bg(`#ffffff`)底色 | surface(`#F8F9FA`)卡片

## Typography
Display: Geist | Body: Geist | Mono: Geist Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 48px | 600 | 1.00 | -2.4px | 首页主标题 |
| 章节标题 | 40px | 600 | 1.20 | -2.4px | 分章标题 |
| 卡片标题 | 24px | 600 | 1.33 | -0.96px | 内容卡标题 |
| 正文 | 20px | 400 | 1.80 | normal | 主要阅读 |
| 辅助文字 | 12px | 400 | 1.33 | normal | 标注/脚注 |
| 数据标签 | 7px | 700 | 1.00 | normal | 图表标签 |

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
- 标题: `#de1d8d` | 正文: `#171717` | 强调: `#000000`
- 底色: `#ffffff` | 卡片: `#F8F9FA` | 边框: `#E5E7EB`

### SVG 组件示例
- "封面：`#ffffff`底，标题48px Geist weight 600，色`#de1d8d`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#F8F9FA`底+`#E5E7EB`边框+16px圆角。标题24px weight 500 色`#de1d8d`。正文18px weight 400 色`#171717`。"

### 品牌铁律
1. Always use shadow-as-border instead of CSS border — `0px 0px 0px 1px rgba(0,0,0,0.08)` is the foundation
2. Letter-spacing scales with font size: -2.4px at 48px, -1.28px at 32px, -0.96px at 24px, normal at 14px
3. Three weights only: 400 (read), 500 (interact), 600 (announce)
