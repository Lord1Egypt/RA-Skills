# MS-PPT-Style: Morgan Stanley PPT Generator

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
npm install pptxgenjs
```

## Quick Start

```javascript
const pptxgen = require("pptxgenjs");
let pres = new pptxgen();

// 定义摩根士丹利色彩
const MS_BLUE = "003087";
const MS_GOLD = "C9A227";
const MS_DARK = "1A1A2E";
const MS_WHITE = "FFFFFF";

// 封面
let slide1 = pres.addSlide();
slide1.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 5.625,
  fill: { color: "0A1628" }
});
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

pres.writeFile({ fileName: "output.pptx" });
```

## Color Reference

| 名称 | 色值 | 用途 |
|------|------|------|
| MS_BLUE | #003087 | 标题栏、强调 |
| MS_GOLD | #C9A227 | 装饰线、点缀 |
| MS_DARK | #1A1A2E | 深色背景 |
| MS_WHITE | #FFFFFF | 正文背景 |

## License

MIT

## Author

QClaw (小龙虾)
