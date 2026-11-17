---
name: "Lovable"
category: "Developer Tools"
description: "AI full-stack builder. Playful gradients, friendly dev aesthetic."
colors:
  primary: "#1A1A1A"
  secondary: "#5f5f5d"
  accent: "#3B82F6"
  background: "#fcfbf8"
  surface: "#f7f4ed"
  muted: "#5f5f5d"
  border: "#E5E7EB"
typography:
  display:
    fontFamily: Camera Plain Variable
    fontSize: 3rem
    fontWeight: 600
    letterSpacing: -0.02em
  body:
    fontFamily: Camera Plain Variable
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
  scenes: ["技术演讲", "科技主题演讲"]
  posture: "宽松"
  accentBudget: 2
---

## Overview
Lovable's website radiates warmth through restraint.

## Colors
primary(`#1A1A1A`)标题 | accent(`#3B82F6`)强调 | bg(`#fcfbf8`)底色 | surface(`#f7f4ed`)卡片

## Typography
Display: Camera Plain Variable | Body: Camera Plain Variable | Mono: Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 60px | 600 | 1.00 | -1.5px | 首页主标题 |
| 章节标题 | 48px | 600 | 1.00 | -1.2px | 分章标题 |
| 卡片标题 | 20px | 400 | 1.25 | normal | 内容卡标题 |
| 正文 | 18px | 400 | 1.38 | normal | 主要阅读 |
| 辅助文字 | 14px | 400 | 1.50 | normal | 标注/脚注 |
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
- 标题: `#1A1A1A` | 正文: `#5f5f5d` | 强调: `#3B82F6`
- 底色: `#fcfbf8` | 卡片: `#f7f4ed` | 边框: `#E5E7EB`

### SVG 组件示例
- "封面：`#fcfbf8`底，标题48px Camera Plain Variable weight 600，色`#1A1A1A`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#f7f4ed`底+`#E5E7EB`边框+16px圆角。标题24px weight 500 色`#1A1A1A`。正文18px weight 400 色`#5f5f5d`。"

### 品牌铁律
1. Always use cream (`#f7f4ed`) as the base — never pure white
2. Derive grays from `#1c1c1c` at opacity levels rather than using distinct hex values
3. Use `#eceae4` borders for containment, not shadows
