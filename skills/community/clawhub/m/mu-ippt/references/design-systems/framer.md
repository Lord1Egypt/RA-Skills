---
name: "Framer"
category: "Design & Creative"
description: "Website builder. Bold black and blue, motion-first, design-forward."
colors:
  primary: "#0000ee"
  secondary: "#a6a6a6"
  accent: "#0055FF"
  background: "#ffffff"
  surface: "#F8F9FA"
  muted: "#a6a6a6"
  border: "#E5E7EB"
typography:
  display:
    fontFamily: Inter Variable
    fontSize: 3rem
    fontWeight: 700
    letterSpacing: -0.02em
  body:
    fontFamily: Inter Variable
    fontSize: 1rem
    fontWeight: 400
  mono:
    fontFamily: Azeret Mono
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
  scenes: ["设计提案", "科技主题演讲"]
  posture: "宽松"
  accentBudget: 2
---

## Overview
Framer's website is a cinematic, tool-obsessed dark canvas that radiates the confidence of a design tool built by designers who worship craft.

## Colors
primary(`#0000ee`)标题 | accent(`#0055FF`)强调 | bg(`#ffffff`)底色 | surface(`#F8F9FA`)卡片

## Typography
Display: GT Walsheim Framer Medium | Body: GT Walsheim Framer Medium | Mono: Azeret Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 110px | 500 | 0.85 | -5.5px | 首页主标题 |
| 章节标题 | 62px | 500 | 1.00 | -3.1px | 分章标题 |
| 卡片标题 | 24px | 400 | 1.30 | -0.01px | 内容卡标题 |
| 正文 | 18px | 400 | 1.30 | -0.01px | 主要阅读 |
| 辅助文字 | 14px | 400 | 1.40 | normal | 标注/脚注 |
| 数据标签 | 4px | 400 | 1.60 | normal | 图表标签 |

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
- 标题: `#0000ee` | 正文: `#a6a6a6` | 强调: `#0055FF`
- 底色: `#ffffff` | 卡片: `#F8F9FA` | 边框: `#E5E7EB`

### SVG 组件示例
- "封面：`#ffffff`底，标题48px Inter Variable weight 700，色`#0000ee`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#F8F9FA`底+`#E5E7EB`边框+16px圆角。标题24px weight 500 色`#0000ee`。正文18px weight 400 色`#a6a6a6`。"

### 品牌铁律
1. Focus on ONE component at a time — the dark canvas makes each element precious
2. Always verify letter-spacing on GT Walsheim headings — the extreme negative tracking is non-negotiable
3. Check that Framer Blue appears ONLY on interactive elements — never as decorative background or text color for non-links
