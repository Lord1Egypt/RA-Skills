---
name: "Uber"
category: "Media & Consumer"
description: "Mobility platform. Bold black and white, tight type, urban energy."
colors:
  primary: "#0000ee"
  secondary: "#4b4b4b"
  accent: "#000000"
  background: "#ffffff"
  surface: "#F8F9FA"
  muted: "#4b4b4b"
  border: "#000000"
typography:
  display:
    fontFamily: UberMove
    fontSize: 3rem
    fontWeight: 700
    letterSpacing: -0.02em
  body:
    fontFamily: UberMoveText
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
  scenes: ["内容营销", "消费品推广", "科技主题演讲"]
  posture: "宽松"
  accentBudget: 2
---

## Overview
Uber's design language is a masterclass in confident minimalism -- a black-and-white universe where every pixel serves a purpose and nothing decorates withou...

## Colors
primary(`#0000ee`)标题 | accent(`#000000`)强调 | bg(`#ffffff`)底色 | surface(`#F8F9FA`)卡片

## Typography
Display: UberMove | Body: UberMove | Mono: Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 48px | 600 | 1.0 | -1.0px | 首页主标题 |
| 章节标题 | 36px | 700 | 1.22 | 1.22px | 分章标题 |
| 卡片标题 | 32px | 700 | 1.25 | 1.25px | 内容卡标题 |
| 正文 | 18px | 400 | 1.5 | normal | 主要阅读 |
| 辅助文字 | 14px | 400 | 1.14 | 1.14px | 标注/脚注 |
| 数据标签 | 12px | 400 | 1.67 | 1.67px | 图表标签 |

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
- 标题: `#0000ee` | 正文: `#4b4b4b` | 强调: `#000000`
- 底色: `#ffffff` | 卡片: `#F8F9FA` | 边框: `#000000`

### SVG 组件示例
- "封面：`#ffffff`底，标题48px UberMove weight 700，色`#0000ee`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#F8F9FA`底+`#000000`边框+16px圆角。标题24px weight 500 色`#0000ee`。正文18px weight 400 色`#4b4b4b`。"

### 品牌铁律
1. Focus on ONE component at a time
2. Reference the strict black/white palette -- "use Uber Black (#000000)" not "make it dark"
3. Always specify 999px radius for buttons and pills -- this is non-negotiable for the Uber identity
