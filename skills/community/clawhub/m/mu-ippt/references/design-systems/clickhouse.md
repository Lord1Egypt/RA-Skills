---
name: "Clickhouse"
category: "Backend & Data"
description: "Fast analytics database. Yellow-accented, technical documentation style."
colors:
  primary: "#14572f"
  secondary: "#6B7280"
  accent: "#3B82F6"
  background: "#ffffff"
  surface: "#F8F9FA"
  muted: "#6B7280"
  border: "#4f5100"
typography:
  display:
    fontFamily: Basier
    fontSize: 3rem
    fontWeight: 600
    letterSpacing: -0.02em
  body:
    fontFamily: Basier
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
  scenes: ["品牌演示", "科技主题演讲"]
  posture: "紧凑"
  accentBudget: 2
---

## Overview
ClickHouse's interface is a high-performance cockpit rendered in acid yellow-green on obsidian black — a design that screams "speed" before you read a single...

## Colors
primary(`#14572f`)标题 | accent(`#3B82F6`)强调 | bg(`#ffffff`)底色 | surface(`#F8F9FA`)卡片

## Typography
Display: Inter | Body: Inter | Mono: Inconsolata

### PPT 字号层级

| 角色 | 字号 | 字重 | 行高 | 字距 | 用途 |
|------|------|------|------|------|------|
| 封面标题 | 48px | 600 | 1.0 | -1.0px | 首页主标题 |
| 章节标题 | 32px | 500 | 1.1 | -0.5px | 分章标题 |
| 卡片标题 | 24px | 600 | 1.17 | normal | 内容卡标题 |
| 正文 | 18px | 400 | 1.56 | normal | 主要阅读 |
| 辅助文字 | 12px | 500 | 1.33 | normal | 标注/脚注 |
| 数据标签 | 2px | 500 | 1.79 | normal | 图表标签 |

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
- 标题: `#14572f` | 正文: `#6B7280` | 强调: `#3B82F6`
- 底色: `#ffffff` | 卡片: `#F8F9FA` | 边框: `#4f5100`

### SVG 组件示例
- "封面：`#ffffff`底，标题48px Basier weight 600，色`#14572f`，字距-0.02em。accent装饰≤2处。"
- "内容页：卡片`#F8F9FA`底+`#4f5100`边框+16px圆角。标题24px weight 500 色`#14572f`。正文18px weight 400 色`#6B7280`。"

### 品牌铁律
1. Keep everything on pure black — no dark gray alternatives
2. Neon Volt (#faff69) is for accents and CTAs only — never large backgrounds
3. Weight 900 for hero, 700 for headings, 600 for labels, 400-500 for body
