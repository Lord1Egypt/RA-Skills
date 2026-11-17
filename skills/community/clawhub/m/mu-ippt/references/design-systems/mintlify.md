---
name: "Mintlify"
category: "Productivity & SaaS"
description: "Documentation platform. Clean, green-accented, reading-optimized."
colors:
  primary: "#0d0d0d"
  secondary: "#0d0d0d"
  accent: "#18E299"
  background: "#ffffff"
  surface: "#3772cf"
  muted: "#0d0d0d"
  border: "#E5E7EB"
typography:
  display:
    fontFamily: Inter
    fontSize: 3rem
    fontWeight: 600
    letterSpacing: -0.02em
  body:
    fontFamily: Inter Fallback, system-ui, -apple-system, sans-ser
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
  sm: 8px
  md: 16px
  lg: 32px
ppt:
  scenes: ["产品介绍", "效率工具演示", "科技主题演讲"]
  posture: "宽松"
  accentBudget: 2
---

## Overview
Mintlify's website is a study in documentation-as-product design — a white, airy, information-rich surface that treats clarity as its highest aesthetic value.

## Colors
primary(`#0d0d0d`)标题 | accent(`#18E299`)强调 | bg(`#ffffff`)底色 | surface(`#3772cf`)卡片

## Typography
Display: Inter | Body: Inter | Mono: Geist Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 64px | 600 | 1.15 | -1.28px | 首页主标题 |
| 章节标题 | 40px | 600 | 1.10 | -0.8px | 分章标题 |
| 卡片标题 | 20px | 600 | 1.30 | -0.2px | 内容卡标题 |
| 正文 | 18px | 400 | 1.50 | normal | 主要阅读 |
| 辅助文字 | 13px | 400 | 1.50 | -0.26px | 标注/脚注 |
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
- 标题: `#0d0d0d` | 正文: `#0d0d0d` | 强调: `#18E299`
- 底色: `#ffffff` | 卡片: `#3772cf` | 边框: `#E5E7EB`

### SVG 组件示例
- "封面：`#ffffff`底，标题48px Inter weight 600，色`#0d0d0d`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#3772cf`底+`#E5E7EB`边框+16px圆角。标题24px weight 500 色`#0d0d0d`。正文18px weight 400 色`#0d0d0d`。"

### 品牌铁律
1. Always use full-pill radius (9999px) for buttons and inputs — this is Mintlify's signature shape
2. Keep borders at 5% opacity (`rgba(0,0,0,0.05)`) — stronger borders break the airy feeling
3. Letter-spacing scales with font size: -1.28px at 64px, -0.8px at 40px, -0.24px at 24px, normal at 16px
