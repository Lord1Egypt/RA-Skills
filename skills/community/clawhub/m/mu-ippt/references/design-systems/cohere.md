---
name: "Cohere"
category: "AI & LLM"
description: "Enterprise AI platform. Vibrant gradients, data-rich dashboard aesthetic."
colors:
  primary: "#17171c"
  secondary: "#93939f"
  accent: "#39594D"
  background: "#ffffff"
  surface: "#F8F9FA"
  muted: "#93939f"
  border: "#d9d9dd"
typography:
  display:
    fontFamily: CohereText
    fontSize: 3rem
    fontWeight: 600
    letterSpacing: -0.02em
  body:
    fontFamily: CohereText
    fontSize: 1rem
    fontWeight: 400
  mono:
    fontFamily: CohereMono
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
Cohere's interface is a polished enterprise command deck — confident, clean, and designed to make AI feel like serious infrastructure rather than a consumer ...

## Colors
primary(`#17171c`)标题 | accent(`#39594D`)强调 | bg(`#ffffff`)底色 | surface(`#F8F9FA`)卡片

## Typography
Display: CohereText | Body: CohereText | Mono: CohereMono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 60px | 400 | 1.00 | -1.2px | 首页主标题 |
| 章节标题 | 48px | 400 | 1.20 | -0.48px | 分章标题 |
| 卡片标题 | 32px | 400 | 1.20 | -0.32px | 内容卡标题 |
| 正文 | 18px | 400 | 1.40 | normal | 主要阅读 |
| 辅助文字 | 12px | 400 | 1.40 | normal | 标注/脚注 |
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
- 标题: `#17171c` | 正文: `#93939f` | 强调: `#39594D`
- 底色: `#ffffff` | 卡片: `#F8F9FA` | 边框: `#d9d9dd`

### SVG 组件示例
- "封面：`#ffffff`底，标题48px CohereText weight 600，色`#17171c`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#F8F9FA`底+`#d9d9dd`边框+16px圆角。标题24px weight 500 色`#17171c`。正文18px weight 400 色`#93939f`。"

### 品牌铁律
1. Focus on ONE component at a time
2. Always use 22px radius for primary cards — "the Cohere card roundness"
3. Specify the typeface — CohereText for headlines, Unica77 for body, CohereMono for labels
