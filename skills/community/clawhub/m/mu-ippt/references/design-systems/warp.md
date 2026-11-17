---
name: "Warp"
category: "Developer Tools"
description: "Modern terminal. Dark IDE-like interface, block-based command UI."
colors:
  primary: "#454545"
  secondary: "#afaeac"
  accent: "#3B82F6"
  background: "#faf9f6"
  surface: "#F8F9FA"
  muted: "#afaeac"
  border: "#E5E7EB"
typography:
  display:
    fontFamily: Matter Regular
    fontSize: 3rem
    fontWeight: 600
    letterSpacing: -0.02em
  body:
    fontFamily: Matter Regular
    fontSize: 1rem
    fontWeight: 400
  mono:
    fontFamily: Matter Mono Regular Placeholder
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
Warp's website feels like sitting at a campfire in a deep forest — warm, dark, and alive with quiet confidence.

## Colors
primary(`#454545`)标题 | accent(`#3B82F6`)强调 | bg(`#faf9f6`)底色 | surface(`#F8F9FA`)卡片

## Typography
Display: Matter Regular | Body: Matter Regular | Mono: Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 80px | 400 | 1.00 | -2.4px | 首页主标题 |
| 章节标题 | 48px | 400 | 1.20 | -0.48px | 分章标题 |
| 卡片标题 | 22px | 500 | 1.14 | 0px | 内容卡标题 |
| 正文 | 20px | 400 | 1.40 | -0.2px | 主要阅读 |
| 辅助文字 | 14px | 400 | 1.00 | 1.4px | 标注/脚注 |
| 数据标签 | 11px | 400 | 1.20 | 0px | 图表标签 |

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
- 标题: `#454545` | 正文: `#afaeac` | 强调: `#3B82F6`
- 底色: `#faf9f6` | 卡片: `#F8F9FA` | 边框: `#E5E7EB`

### SVG 组件示例
- "封面：`#faf9f6`底，标题48px Matter Regular weight 600，色`#454545`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#F8F9FA`底+`#E5E7EB`边框+16px圆角。标题24px weight 500 色`#454545`。正文18px weight 400 色`#afaeac`。"

### 品牌铁律
1. Verify text color is warm parchment (#faf9f6) not pure white — the warmth is subtle but essential
2. Ensure all buttons use the restrained dark palette (#353534) — no bright or colorful CTAs
3. Check that Matter Regular (400) is the default weight — Medium (500) only for emphasis
