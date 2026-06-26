---
name: ms-ppt-style
description: Morgan Stanley classic PPT style generator for OpenClaw/WorkBuddy/QClaw. Use when user needs to create professional financial report style presentations with bilingual content, gradient covers, and charts. Supports pie charts, radar charts, stacked bars, waterfall charts, and metric cards.
---

# MS-PPT-Style Skill

## Overview

摩根士丹利经典款PPT风格生成器 - 一键生成专业金融报告风格PPT。

Morgan Stanley classic PPT style generator - one-click professional financial report style presentation.

## Features

- **经典配色**: 摩根士丹利蓝(#003087) + 金色(#C9A227)
- **渐变封面**: 极简深色渐变背景，居中双语标题
- **全双语内容**: 所有页面中英对照
- **专业图表**: 瀑布图、玫瑰图、雷达图、散点矩阵、堆叠图
- **金融级排版**: 干净利落的投行报告风格

## Installation

```bash
# 安装依赖
npm install pptxgenjs

# 使用此Skill生成PPT
```

## Usage

### 基础用法

```javascript
const pptxgen = require("pptxgenjs");
let pres = new pptxgen();

// 定义摩根士丹利色彩
const MS_BLUE = "003087";
const MS_GOLD = "C9A227";
const MS_DARK = "1A1A2E";
const MS_WHITE = "FFFFFF";
const MS_GRAY = "6B7280";
const MS_LIGHT_GRAY = "F3F4F6";

// ===== 封面 =====
let slide1 = pres.addSlide();

// 渐变背景
slide1.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 5.625,
  fill: { color: "0A1628" }
});
slide1.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 5.625,
  fill: { color: "1A2744", transparency: 60 }
});

// 金色顶线
slide1.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 0.04,
  fill: { color: MS_GOLD }
});

// 居中双语标题
slide1.addText("Title Here", {
  x: 0.5, y: 1.8, w: 9, h: 0.8,
  fontSize: 46, fontFace: "Arial", color: MS_WHITE,
  bold: true, align: "center"
});
slide1.addText("中文标题", {
  x: 0.5, y: 2.7, w: 9, h: 0.5,
  fontSize: 26, fontFace: "Arial", color: MS_GOLD,
  align: "center"
});

// 金色装饰线
slide1.addShape(pres.shapes.RECTANGLE, {
  x: 4.25, y: 3.4, w: 1.5, h: 0.02,
  fill: { color: MS_GOLD }
});

// 底部信息
slide1.addText("Research Report | 研究报告", {
  x: 0.5, y: 4.8, w: 9, h: 0.25,
  fontSize: 10, fontFace: "Arial", color: "9CA3AF",
  align: "center"
});

// ===== 内容页模板 =====
let slide2 = pres.addSlide();
slide2.background = { color: MS_WHITE };

// 蓝色标题栏
slide2.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 0.8,
  fill: { color: MS_BLUE }
});

slide2.addText("ENGLISH TITLE  中文标题", {
  x: 0.5, y: 0.18, w: 8, h: 0.45,
  fontSize: 22, fontFace: "Arial", color: MS_WHITE,
  bold: true
});

// 内容区域...

// 保存
pres.writeFile({ fileName: "output.pptx" });
```

### 图表模板

#### 瀑布图
```javascript
const items = [
  { name: "Item1", value: 100, color: "003087" },
  { name: "Item2", value: 200, color: "1E5AA8" }
];
// 使用矩形堆叠模拟瀑布效果
```

#### 玫瑰图 (Pie Chart)
```javascript
slide.addChart(pres.charts.PIE, [{
  name: "Category",
  labels: ["A", "B"],
  values: [40, 60]
}], {
  chartColors: ["003087", "C9A227"],
  showPercent: true,
  showLegend: true,
  legendPos: "r"
});
```

#### 雷达图
```javascript
slide.addChart(pres.charts.RADAR, [
  {
    name: "Series1",
    labels: ["Dim1", "Dim2", "Dim3"],
    values: [80, 90, 70]
  }
], {
  chartColors: ["003087"],
  lineSize: 2,
  radarStyle: "filled"
});
```

#### 散点矩阵 (手动绘制)
```javascript
// 绘制坐标轴
slide.addShape(pres.shapes.RECTANGLE, {
  x: 1.0, y: 1.3, w: 0.02, h: 4.0,
  fill: { color: "374151" }
});
// 绘制气泡...
```

## Color Reference

| 名称 | 色值 | 用途 |
|------|------|------|
| MS_BLUE | #003087 | 标题栏、强调 |
| MS_LIGHT_BLUE | #1E5AA8 | 次要强调 |
| MS_GOLD | #C9A227 | 装饰线、点缀 |
| MS_DARK | #1A1A2E | 深色背景 |
| MS_WHITE | #FFFFFF | 正文背景 |
| MS_GRAY | #6B7280 | 次要文字 |
| MS_LIGHT_GRAY | #F3F4F6 | 卡片背景 |

## Chart Colors

```javascript
const MS_CHART_COLORS = [
  "003087", "1E5AA8", "3B82F6", "60A5FA",
  "93C5FD", "C9A227", "D4AF37", "E5E7EB"
];
```

## Typography

| 用途 | 字体 | 字号 |
|------|------|------|
| 封面标题 | Arial | 46pt |
| 封面副标题 | Arial | 26pt |
| 页面标题 | Arial | 22pt |
| 正文英文 | Arial | 12pt |
| 正文中文 | Arial | 10pt |
| 注释 | Arial | 9pt |

## Dependencies

- `pptxgenjs` >= 3.0.0

## License

MIT

## Author

QClaw (小龙虾)
