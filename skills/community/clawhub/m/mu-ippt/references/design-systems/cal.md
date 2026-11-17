---
name: "Cal"
category: "Productivity & SaaS"
description: "Open-source scheduling. Clean neutral UI, developer-oriented simplicity."
colors:
  primary: "#0099ff"
  secondary: "#6B7280"
  accent: "#3B82F6"
  background: "#ffffff"
  surface: "#F8F9FA"
  muted: "#6B7280"
  border: "#E5E7EB"
typography:
  display:
    fontFamily: Cal Sans
    fontSize: 3rem
    fontWeight: 600
    letterSpacing: -0.02em
  body:
    fontFamily: Inter Placeholder
    fontSize: 1rem
    fontWeight: 400
  mono:
    fontFamily: Roboto Mono
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
  scenes: ["产品介绍", "效率工具演示", "科技主题演讲"]
  posture: "宽松"
  accentBudget: 2
---

## Overview
Cal.com's website is a masterclass in monochromatic restraint — a grayscale world where boldness comes not from color but from the sheer confidence of black ...

## Colors
primary(`#0099ff`)标题 | accent(`#3B82F6`)强调 | bg(`#ffffff`)底色 | surface(`#F8F9FA`)卡片

## Typography
Display: Cal Sans | Body: Inter | Mono: Roboto Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 64px | 600 | 1.10 | 0px | 首页主标题 |
| 章节标题 | 48px | 600 | 1.10 | 0px | 分章标题 |
| 卡片标题 | 16px | 600 | 1.10 | 0px | 内容卡标题 |
| 正文 | 18px | 400 | 1.5 | normal | 主要阅读 |
| 辅助文字 | 14px | 300 | 1.40 | -0.28px | 标注/脚注 |
| 数据标签 | 12px | 500 | 1.00 | 0px | 图表标签 |

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
- 标题: `#0099ff` | 正文: `#6B7280` | 强调: `#3B82F6`
- 底色: `#ffffff` | 卡片: `#F8F9FA` | 边框: `#E5E7EB`

### SVG 组件示例
- "封面：`#ffffff`底，标题48px Cal Sans weight 600，色`#0099ff`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#F8F9FA`底+`#E5E7EB`边框+16px圆角。标题24px weight 500 色`#0099ff`。正文18px weight 400 色`#6B7280`。"

### 品牌铁律
1. Verify headings use Cal Sans at weight 600, body uses Inter — never mix them
2. Check that the palette is purely grayscale — if you see brand colors, remove them
3. Ensure card elevation uses the multi-layered shadow stack, not CSS borders
