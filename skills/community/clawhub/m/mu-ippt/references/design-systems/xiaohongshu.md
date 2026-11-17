---
name: "Xiaohongshu"
category: "Media & Consumer"
description: "Lifestyle UGC social platform. Singular brand red, generous radius, content-first."
colors:
  primary: "#133667"
  secondary: "#6B7280"
  accent: "#FF2442"
  background: "#F5F5F5"
  surface: "#FFFFFF"
  muted: "#6B7280"
  border: "#EAEAEA"
typography:
  display:
    fontFamily: 14-16/400
    fontSize: 3rem
    fontWeight: 600
    letterSpacing: -0.02em
  body:
    fontFamily: 14-16/400
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
  scenes: ["内容营销", "消费品推广", "科技主题演讲"]
  posture: "紧凑"
  accentBudget: 2
---

## Overview
Xiaohongshu (小红书 / RED) is the visual opposite of a SaaS console.

## Colors
primary(`#133667`)标题 | accent(`#FF2442`)强调 | bg(`#F5F5F5`)底色 | surface(`#FFFFFF`)卡片

## Typography
Display: PingFang SC | Body: PingFang SC | Mono: Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 48px | 600 | 1.0 | -1.0px | 首页主标题 |
| 章节标题 | 32px | 500 | 1.1 | -0.5px | 分章标题 |
| 卡片标题 | 24px | 500 | 1.2 | -0.2px | 内容卡标题 |
| 正文 | 18px | 400 | 1.5 | normal | 主要阅读 |
| 辅助文字 | 14px | 400 | 1.4 | normal | 标注/脚注 |
| 数据标签 | 12px | 500 | 1.3 | normal | 图表标签 |

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
- 标题: `#133667` | 正文: `#6B7280` | 强调: `#FF2442`
- 底色: `#F5F5F5` | 卡片: `#FFFFFF` | 边框: `#EAEAEA`

### SVG 组件示例
- "封面：`#F5F5F5`底，标题48px 14-16/400 weight 600，色`#133667`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#FFFFFF`底+`#EAEAEA`边框+16px圆角。标题24px weight 500 色`#133667`。正文18px weight 400 色`#6B7280`。"

### 品牌铁律
1. **Start from the picture, not the chrome.** Drop a generous photographic hero or pin grid first; build UI around it as quietly as possible.
2. **One accent.** If you have used `#FF2442` once on a screen, you have used it enough.
3. **Translucent neutrals.** Reach for `rgba(48,48,52, .10)` before reaching for a fresh grey hex.
