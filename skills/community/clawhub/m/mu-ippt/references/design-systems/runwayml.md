---
name: "Runwayml"
category: "AI & LLM"
description: "AI video generation. Cinematic dark UI, media-rich layout."
colors:
  primary: "#1a1a1a"
  secondary: "#a7a7a7"
  accent: "#3B82F6"
  background: "#ffffff"
  surface: "#1a1a1a"
  muted: "#a7a7a7"
  border: "#27272a"
typography:
  display:
    fontFamily: system-ui, sans-serif
    fontSize: 3rem
    fontWeight: 600
    letterSpacing: -0.02em
  body:
    fontFamily: system-ui, sans-serif
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
Runway's interface is a cinematic reel brought to life as a website — a dark, editorial, film-production-grade design where full-bleed photography and video ...

## Colors
primary(`#1a1a1a`)标题 | accent(`#3B82F6`)强调 | bg(`#ffffff`)底色 | surface(`#1a1a1a`)卡片

## Typography
Display: abcNormal | Body: abcNormal | Mono: Mono

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 48px | 600 | 1.0 | -1.0px | 首页主标题 |
| 章节标题 | 40px | 400 | 1.00 | -1px | 分章标题 |
| 卡片标题 | 24px | 400 | 1.00 | normal | 内容卡标题 |
| 正文 | 18px | 400 | 1.5 | normal | 主要阅读 |
| 辅助文字 | 13px | 400 | 1.30 | -0.16px | 标注/脚注 |
| 数据标签 | 11px | 450 | 1.30 | normal | 图表标签 |

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
- 标题: `#1a1a1a` | 正文: `#a7a7a7` | 强调: `#3B82F6`
- 底色: `#ffffff` | 卡片: `#1a1a1a` | 边框: `#27272a`

### SVG 组件示例
- "封面：`#ffffff`底，标题48px system-ui, sans-serif weight 600，色`#1a1a1a`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#1a1a1a`底+`#27272a`边框+16px圆角。标题24px weight 500 色`#1a1a1a`。正文18px weight 400 色`#a7a7a7`。"

### 品牌铁律
1. Visual content first — always include cinematic photography
2. Use abcNormal for everything — specify size and weight, never change the font
3. Keep the interface invisible — no heavy borders, no shadows, no bright colors
