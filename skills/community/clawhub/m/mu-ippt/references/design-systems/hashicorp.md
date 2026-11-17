---
name: "Hashicorp"
category: "Backend & Data"
description: "Infrastructure automation. Enterprise-clean, black and white."
colors:
  primary: "#15181e"
  secondary: "#6B7280"
  accent: "#000000"
  background: "#efeff1"
  surface: "#F8F9FA"
  muted: "#6B7280"
  border: "#E5E7EB"
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
HashiCorp's website is enterprise infrastructure made tangible — a design system that must communicate the complexity of cloud infrastructure management whil...

## Colors
primary(`#15181e`)标题 | accent(`#000000`)强调 | bg(`#efeff1`)底色 | surface(`#F8F9FA`)卡片

## Typography
Display: HashiCorp Sans | Body: HashiCorp Sans | Mono: Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 82px | 600 | 1.17 | normal | 首页主标题 |
| 章节标题 | 52px | 600 | 1.19 | normal | 分章标题 |
| 卡片标题 | 26px | 700 | 1.19 | normal | 内容卡标题 |
| 正文 | 20px | 400 | 1.50 | normal | 主要阅读 |
| 辅助文字 | 13px | 400 | 1.23 | normal | 标注/脚注 |
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
- 标题: `#15181e` | 正文: `#6B7280` | 强调: `#000000`
- 底色: `#efeff1` | 卡片: `#F8F9FA` | 边框: `#E5E7EB`

### SVG 组件示例
- "封面：`#efeff1`底，标题48px system-ui, sans-serif weight 600，色`#15181e`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#F8F9FA`底+`#E5E7EB`边框+16px圆角。标题24px weight 500 色`#15181e`。正文18px weight 400 色`#6B7280`。"

### 品牌铁律
1. Always start with the mode decision: light (white) for informational, dark (#15181e) for hero/product
2. HashiCorp Sans for headings only (17px+), system-ui for everything else
3. Shadows are at whisper level (0.05 opacity) — if visible, reduce
