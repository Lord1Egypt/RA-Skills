---
name: "Posthog"
category: "Backend & Data"
description: "Product analytics. Playful hedgehog branding, developer-friendly dark UI."
colors:
  primary: "#4d4f46"
  secondary: "#65675e"
  accent: "#F54E00"
  background: "#f4f4f4"
  surface: "#F8F9FA"
  muted: "#65675e"
  border: "#b17816"
typography:
  display:
    fontFamily: IBM Plex Sans Variable
    fontSize: 3rem
    fontWeight: 600
    letterSpacing: -0.02em
  body:
    fontFamily: IBM Plex Sans Variable
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
PostHog's website feels like a startup's internal wiki that escaped into the wild — warm, irreverent, and deliberately anti-corporate.

## Colors
primary(`#4d4f46`)标题 | accent(`#F54E00`)强调 | bg(`#f4f4f4`)底色 | surface(`#F8F9FA`)卡片

## Typography
Display: IBM Plex Sans Variable | Body: IBM Plex Sans Variable | Mono: Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 30px | 800 | 1.20 | -0.75px | 首页主标题 |
| 章节标题 | 36px | 700 | 1.50 | 0px | 分章标题 |
| 卡片标题 | 20px | 700 | 1.40 | -0.5px | 内容卡标题 |
| 正文 | 16px | 400 | 1.50 | 0px | 主要阅读 |
| 辅助文字 | 14px | 400 | 1.43 | 0px | 标注/脚注 |
| 数据标签 | 12px | 400 | 1.33 | 0px | 图表标签 |

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
- 标题: `#4d4f46` | 正文: `#65675e` | 强调: `#F54E00`
- 底色: `#f4f4f4` | 卡片: `#F8F9FA` | 边框: `#b17816`

### SVG 组件示例
- "封面：`#f4f4f4`底，标题48px IBM Plex Sans Variable weight 600，色`#4d4f46`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#F8F9FA`底+`#b17816`边框+16px圆角。标题24px weight 500 色`#4d4f46`。正文18px weight 400 色`#65675e`。"

### 品牌铁律
1. Verify the background is warm parchment (#fdfdf8) not pure white — the sage-cream warmth is essential
2. Check that all text uses the olive family (#4d4f46, #23251d) not pure black or neutral gray
3. Ensure hover states flash PostHog Orange (#F54E00) — if hovering feels bland, you're missing this
