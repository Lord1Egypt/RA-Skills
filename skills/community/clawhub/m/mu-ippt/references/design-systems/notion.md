---
name: "Notion"
category: "Productivity & SaaS"
description: "All-in-one workspace. Warm minimalism, serif headings, soft surfaces."
colors:
  primary: "#213183"
  secondary: "#615d59"
  accent: "#2383E2"
  background: "#ffffff"
  surface: "#F8F9FA"
  muted: "#615d59"
  border: "#E5E7EB"
typography:
  display:
    fontFamily: Inter, -apple-system, system-ui, Segoe UI, Helveti
    fontSize: 3rem
    fontWeight: 600
    letterSpacing: -0.02em
  body:
    fontFamily: Inter, -apple-system, system-ui, Segoe UI, Helveti
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
  sm: 4px
  md: 8px
  lg: 16px
ppt:
  scenes: ["产品介绍", "效率工具演示", "科技主题演讲"]
  posture: "紧凑"
  accentBudget: 2
---

## Overview
Notion's website embodies the philosophy of the tool itself: a blank canvas that gets out of your way.

## Colors
primary(`#213183`)标题 | accent(`#2383E2`)强调 | bg(`#ffffff`)底色 | surface(`#F8F9FA`)卡片

## Typography
Display: NotionInter | Body: NotionInter | Mono: Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 64px | 700 | 1.00 | -2.125px | 首页主标题 |
| 章节标题 | 48px | 700 | 1.00 | -1.5px | 分章标题 |
| 卡片标题 | 22px | 700 | 1.27 | -0.25px | 内容卡标题 |
| 正文 | 20px | 600 | 1.40 | -0.125px | 主要阅读 |
| 辅助文字 | 14px | 500 | 1.43 | normal | 标注/脚注 |
| 数据标签 | 12px | 400 | 1.33 | 0.125px | 图表标签 |

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
- 标题: `#213183` | 正文: `#615d59` | 强调: `#2383E2`
- 底色: `#ffffff` | 卡片: `#F8F9FA` | 边框: `#E5E7EB`

### SVG 组件示例
- "封面：`#ffffff`底，标题48px Inter, -apple-system, system-ui, Segoe UI, Helveti weight 600，色`#213183`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#F8F9FA`底+`#E5E7EB`边框+16px圆角。标题24px weight 500 色`#213183`。正文18px weight 400 色`#615d59`。"

### 品牌铁律
1. Always use warm neutrals -- Notion's grays have yellow-brown undertones (#f6f5f4, #31302e, #615d59, #a39e98), never blue-gray
2. Letter-spacing scales with font size: -2.125px at 64px, -1.875px at 54px, -0.625px at 26px, normal at 16px
3. Four weights: 400 (read), 500 (interact), 600 (emphasize), 700 (announce)
