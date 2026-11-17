# PptxGenJS 演示文稿创建指南

## 概述

本指南旨在帮助设计师和开发者使用 PptxGenJS 创建专业级演示文稿。涵盖从基础设置到高级技巧的完整工作流程。

**核心原则**：
- 分析用户提示词的结构、意图和关键要素
- 将指令转化为干净、结构化的视觉隐喻（蓝图、展示图、原理图）
- 使用特定的、克制的调色板和字体系列，以获得最大的清晰度和专业影响力
- 所有视觉输出必须严格保持 16:9 的长宽比
- 以三联画（triptych）或基于网格的布局呈现信息，保持文本和视觉的平衡

---

## 第一部分：基础概念

### PptxGenJS 简介

PptxGenJS 是一个用于程序化生成 PowerPoint 文件的 JavaScript 库。

```javascript
const pptxgen = require("pptxgenjs");

let pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';  // 或 'LAYOUT_16x10', 'LAYOUT_4x3', 'LAYOUT_WIDE'
pres.author = 'Your Name';
pres.title = 'Presentation Title';

let slide = pres.addSlide();
slide.addText("Hello World!", { x: 0.5, y: 0.5, fontSize: 36, color: "363636" });

pres.writeFile({ fileName: "Presentation.pptx" });
```

### 布局尺寸

幻灯片尺寸（坐标单位为英寸）：
- `LAYOUT_16x9`: 10" × 5.625"（默认）
- `LAYOUT_16x10`: 10" × 6.25"
- `LAYOUT_4x3`: 10" × 7.5"
- `LAYOUT_WIDE`: 13.3" × 7.5"

---

## 第二部分：文本与格式

### 基础文本

```javascript
slide.addText("Simple Text", {
  x: 1, y: 1, w: 8, h: 2, fontSize: 24, fontFace: "Arial",
  color: "363636", bold: true, align: "center", valign: "middle"
});
```

### 字符间距

使用 `charSpacing`，而非 `letterSpacing`（后者会被静默忽略）。

```javascript
slide.addText("SPACED TEXT", { x: 1, y: 1, w: 8, h: 1, charSpacing: 6 });
```

### 富文本数组

```javascript
slide.addText([
  { text: "Bold ", options: { bold: true } },
  { text: "Italic ", options: { italic: true } }
], { x: 1, y: 3, w: 8, h: 1 });
```

### 多行文本

需要在数组项之间使用 `breakLine: true`。

```javascript
slide.addText([
  { text: "Line 1", options: { breakLine: true } },
  { text: "Line 2", options: { breakLine: true } },
  { text: "Line 3" }  // 最后一项不需要 breakLine
], { x: 0.5, y: 0.5, w: 8, h: 2 });
```

### 文本框内边距

文本框默认有内部边距。当需要与 shapes、线条或图标精确对齐时，设置 `margin: 0`。

```javascript
slide.addText("Title", {
  x: 0.5, y: 0.3, w: 9, h: 0.6,
  margin: 0
});
```

---

## 第三部分：列表与项目符号

### 正确使用项目符号

✅ **正确做法**：使用 `bullet: true`

```javascript
slide.addText([
  { text: "First item", options: { bullet: true, breakLine: true } },
  { text: "Second item", options: { bullet: true, breakLine: true } },
  { text: "Third item", options: { bullet: true } }
], { x: 0.5, y: 0.5, w: 8, h: 3 });
```

❌ **错误做法**：绝不要使用 Unicode 符号如 "•"

```javascript
slide.addText("• First item", { ... });  // 会产生双项目符号
```

### 子项和编号列表

```javascript
{ text: "Sub-item", options: { bullet: true, indentLevel: 1 } }
{ text: "First", options: { bullet: { type: "number" }, breakLine: true } }
```

---

## 第四部分：形状

### 基础形状

```javascript
slide.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 0.8, w: 1.5, h: 3.0,
  fill: { color: "FF0000" }, line: { color: "000000", width: 2 }
});

slide.addShape(pres.shapes.OVAL, { x: 4, y: 1, w: 2, h: 2, fill: { color: "0000FF" } });

slide.addShape(pres.shapes.LINE, {
  x: 1, y: 3, w: 5, h: 0, line: { color: "FF0000", width: 3, dashType: "dash" }
});
```

### 带透明度的形状

```javascript
slide.addShape(pres.shapes.RECTANGLE, {
  x: 1, y: 1, w: 3, h: 2,
  fill: { color: "0088CC", transparency: 50 }
});
```

### 圆角矩形

⚠️ `rectRadius` 仅对 `ROUNDED_RECTANGLE` 有效，不要与矩形 accent overlays 配对使用（无法覆盖圆角）。

```javascript
slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 1, y: 1, w: 3, h: 2,
  fill: { color: "FFFFFF" }, rectRadius: 0.1
});
```

### 带阴影的形状

```javascript
slide.addShape(pres.shapes.RECTANGLE, {
  x: 1, y: 1, w: 3, h: 2,
  fill: { color: "FFFFFF" },
  shadow: { type: "outer", color: "000000", blur: 6, offset: 2, angle: 135, opacity: 0.15 }
});
```

### 阴影选项详解

| 属性 | 类型 | 范围 | 说明 |
|------|------|------|------|
| `type` | string | `"outer"`, `"inner"` | |
| `color` | string | 6位十六进制 (如 `"000000"`) | 不要加 `#` 前缀，不要使用8位十六进制 |
| `blur` | number | 0-100 pt | |
| `offset` | number | 0-200 pt | **必须为非负值** — 负值会导致文件损坏 |
| `angle` | number | 0-359 degrees | 阴影落下的方向 (135 = 右下，270 = 上) |
| `opacity` | number | 0.0-1.0 | 使用此属性表示透明度，不要编码在颜色字符串中 |

向上投射阴影（如在 footer bar 上）：使用 `angle: 270` 和正值 offset — **不要使用负 offset**。

### 渐变填充

> **⚠️ 注意**：PptxGenJS 的 `addShape().fill` 和 `addText().color` 不支持渐变填充。如需渐变效果，需自行用图片实现。

---

## 第五部分：图片

### 图片来源

```javascript
// 从文件路径
slide.addImage({ path: "images/chart.png", x: 1, y: 1, w: 5, h: 3 });

// 从 URL
slide.addImage({ path: "https://example.com/image.jpg", x: 1, y: 1, w: 5, h: 3 });

// 从 base64（更快，无文件I/O）
slide.addImage({ data: "image/png;base64,iVBORw0KGgo...", x: 1, y: 1, w: 5, h: 3 });
```

### 图片选项

```javascript
slide.addImage({
  path: "image.png",
  x: 1, y: 1, w: 5, h: 3,
  rotate: 45,              // 0-359 degrees
  rounding: true,          // 圆形裁剪
  transparency: 50,        // 0-100
  flipH: true,             // 水平翻转
  flipV: false,            // 垂直翻转
  altText: "Description",  // 无障碍访问
  hyperlink: { url: "https://example.com" }
});
```

### 图片尺寸模式

```javascript
// Contain - 适应内部，保持比例
{ sizing: { type: 'contain', w: 4, h: 3 } }

// Cover - 填充区域，保持比例（可能裁剪）
{ sizing: { type: 'cover', w: 4, h: 3 } }

// Crop - 裁剪特定部分
{ sizing: { type: 'crop', x: 0.5, y: 0.5, w: 2, h: 2 } }
```

### 计算尺寸（保持宽高比）

```javascript
const origWidth = 1978, origHeight = 923, maxHeight = 3.0;
const calcWidth = maxHeight * (origWidth / origHeight);
const centerX = (10 - calcWidth) / 2;

slide.addImage({ path: "image.png", x: centerX, y: 1.2, w: calcWidth, h: maxHeight });
```

### 支持的格式

- **标准**: PNG, JPG, GIF（动画 GIF 在 Microsoft 365 中有效）
- **SVG**: 在现代 PowerPoint/Microsoft 365 中有效

---

## 第六部分：图标

使用 react-icons 生成 SVG 图标，然后栅格化为 PNG 以获得通用兼容性。

### 设置

```javascript
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const { FaCheckCircle, FaChartLine } = require("react-icons/fa");

function renderIconSvg(IconComponent, color = "#000000", size = 256) {
  return ReactDOMServer.renderToStaticMarkup(
    React.createElement(IconComponent, { color, size: String(size) })
  );
}

async function iconToBase64Png(IconComponent, color, size = 256) {
  const svg = renderIconSvg(IconComponent, color, size);
  const pngBuffer = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + pngBuffer.toString("base64");
}
```

### 添加图标到幻灯片

```javascript
const iconData = await iconToBase64Png(FaCheckCircle, "#4472C4", 256);

slide.addImage({
  data: iconData,
  x: 1, y: 1, w: 0.5, h: 0.5  // 尺寸单位为英寸
});
```

**注意**: 使用 256 或更大的尺寸以获得清晰的图标。size 参数控制栅格化分辨率，而不是幻灯片上的显示尺寸（由 `w` 和 `h` 英寸设置）。

### 图标库

安装：`npm install -g react-icons react react-dom sharp`

react-icons 中的流行图标集：
- `react-icons/fa` - Font Awesome
- `react-icons/md` - Material Design
- `react-icons/hi` - Heroicons
- `react-icons/bi` - Bootstrap Icons

---

## 第七部分：幻灯片背景

```javascript
// 纯色
slide.background = { color: "F1F1F1" };

// 带透明度
slide.background = { color: "FF3399", transparency: 50 };

// 来自 URL 的图片
slide.background = { path: "https://example.com/bg.jpg" };

// 来自 base64
slide.background = { data: "image/png;base64,iVBORw0KGgo..." };
```

---

## 第八部分：表格

```javascript
slide.addTable([
  ["Header 1", "Header 2"],
  ["Cell 1", "Cell 2"]
], {
  x: 1, y: 1, w: 8, h: 2,
  border: { pt: 1, color: "999999" }, fill: { color: "F1F1F1" }
});

// 高级用法：合并单元格
let tableData = [
  [{ text: "Header", options: { fill: { color: "6699CC" }, color: "FFFFFF", bold: true } }, "Cell"],
  [{ text: "Merged", options: { colspan: 2 } }]
];
slide.addTable(tableData, { x: 1, y: 3.5, w: 8, colW: [4, 4] });
```

---

## 第九部分：图表

### 基础图表

```javascript
// 柱状图
slide.addChart(pres.charts.BAR, [{
  name: "Sales", labels: ["Q1", "Q2", "Q3", "Q4"], values: [4500, 5500, 6200, 7100]
}], {
  x: 0.5, y: 0.6, w: 6, h: 3, barDir: 'col',
  showTitle: true, title: 'Quarterly Sales'
});

// 折线图
slide.addChart(pres.charts.LINE, [{
  name: "Temp", labels: ["Jan", "Feb", "Mar"], values: [32, 35, 42]
}], { x: 0.5, y: 4, w: 6, h: 3, lineSize: 3, lineSmooth: true });

// 饼图
slide.addChart(pres.charts.PIE, [{
  name: "Share", labels: ["A", "B", "Other"], values: [35, 45, 20]
}], { x: 7, y: 1, w: 5, h: 4, showPercent: true });
```

### 美化图表

默认图表看起来过时。应用以下选项以获得现代、干净的外观：

```javascript
slide.addChart(pres.charts.BAR, chartData, {
  x: 0.5, y: 1, w: 9, h: 4, barDir: "col",

  // 自定义颜色（匹配演示文稿配色）
  chartColors: ["0D9488", "14B8A6", "5EEAD4"],

  // 干净的背景
  chartArea: { fill: { color: "FFFFFF" }, roundedCorners: true },

  // 柔和的坐标轴标签
  catAxisLabelColor: "64748B",
  valAxisLabelColor: "64748B",

  // 细网格（仅值坐标轴）
  valGridLine: { color: "E2E8F0", size: 0.5 },
  catGridLine: { style: "none" },

  // 数据标签
  showValue: true,
  dataLabelPosition: "outEnd",
  dataLabelColor: "1E293B",

  // 隐藏单系列图例
  showLegend: false,
});
```

### 关键样式选项

- `chartColors: [...]` - 系列/段落的十六进制颜色
- `chartArea: { fill, border, roundedCorners }` - 图表背景
- `catGridLine/valGridLine: { color, style, size }` - 网格线（`style: "none"` 隐藏）
- `lineSmooth: true` - 曲线（折线图）
- `legendPos: "r"` - 图例位置: "b", "t", "l", "r", "tr"

### 图表类型

PptxGenJS 支持的图表类型：
- `pptx.ChartType.area`
- `pptx.ChartType.bar`, `pptx.ChartType.bar3d`
- `pptx.ChartType.bubble`, `pptx.ChartType.bubble3d`
- `pptx.ChartType.doughnut`
- `pptx.ChartType.line`
- `pptx.ChartType.pie`
- `pptx.ChartType.radar`
- `pptx.ChartType.scatter`

### 组合图表

组合图表的函数签名与标准图表不同。有两个参数：`chartTypes` 和 `options`。`chartTypes` 可以是任何 `pptx.ChartType`，尽管 `area`、`bar` 和 `line` 会给出最佳结果。

---

## 第十部分：幻灯片母版

```javascript
pres.defineSlideMaster({
  title: 'TITLE_SLIDE', background: { color: '283A5E' },
  objects: [{
    placeholder: { options: { name: 'title', type: 'title', x: 1, y: 2, w: 8, h: 2 } }
  }]
});

let titleSlide = pres.addSlide({ masterName: "TITLE_SLIDE" });
titleSlide.addText("My Title", { placeholder: "title" });
```

---

## 第十一部分：设计风格指南

你是一位世界级的演示文稿设计师和故事讲述者。你创作的幻灯片在视觉上令人震撼、极其精美，并能有效地传达复杂的信息。你的特点是：既精通设计，又极具讲故事的天赋。

你制作的幻灯片能根据源素材和目标受众进行调整。凡事皆有故事，而你要找到最佳的讲述方式。你结合了顶尖设计师的创造力与专业知识。

本幻灯片主要设计用于**阅读和分享**。其结构应当不言自明，即便没有演讲者也能轻松理解。叙事逻辑和所有有用的数据都应包含在幻灯片的文本和视觉元素中。幻灯片应包含足够的语境，以便任何视觉图像都能被独立理解。如果有助于叙事，你可以添加某些包含更密集信息（从源素材中提取）的幻灯片。

你现在需要为下面所描述的幻灯片编写一份**大纲**。我们将把这份大纲提供给一位专家级设计师，由其制作最终的实际演示文稿。幻灯片的具体内容应使用{Chinese}。占位符内容应保留为{Chinese}。

本幻灯片内容应专注于：`{Custom Prompt, 描述你想要创建的幻灯片，默认为：添加高层级大纲，或引导受众、风格和重点："为初学者创建一个风格大胆且俏皮的演示文稿，重点在于分步说明。"}`


**请记住：除非用户明确要求，否则不要创建幻灯片。**

### 视觉元素设计原则

**每张幻灯片都需要视觉元素** — 纯文字幻灯片容易被遗忘。

### 布局选项

- 双栏（文字左，图片右）
- 图标+文字行（彩色圆圈中的图标，标题粗体，说明文字在下方）
- 2x2 或 2x3 网格
- 半出血图片（占满左或右半侧）

### 数据展示

- 大数字强调（60-72pt 大数字配小标签）
- 对比栏（前后对比、优劣势对比）
- 时间轴或流程图

### 视觉细节

- 章节标题旁的小图标（放在彩色圆圈中）
- 关键数据用斜体强调

### 风格指南

设计美学和配色方案应根据具体项目需求灵活选择，不预设特定的配色主题或渐变效果。

---

### 主题与视觉

- 默认情况下，使用浅色主题并创建带有适当支持性视觉效果的精美幻灯片
- 嵌入式图片是幻灯片的关键部分，应经常使用以阐明概念。**仅当**有文本覆盖时才添加淡入淡出效果

### 图片使用注意

- 使用 `addImage` 时，由于存在错误，请避免使用 `sizing` 参数。相反，您必须在 `output.mjs` 中使用以下之一：
  - 裁剪：对于大多数图片，默认使用 `imageSizingCrop`（放大并居中裁剪以适应）
  - 包含：对于需要保持完全不裁剪的图片（如带有重要文本或图表的图片），使用 `imageSizingContain`
  - 拉伸：对于纹理或背景，直接使用 `addImage`
- 不要重复使用同一张图片，尤其是标题幻灯片的图片，除非绝对必要；请搜索或生成新图片使用

### 图标使用

- 非常谨慎地使用图标，例如每张幻灯片最多1-2个
- **切勿**在前两张幻灯片中使用图标
- **不要**将图标用作独立的图片

### 项目符号使用

- 对于 PptxGenJS 中的项目符号：您**必须**像这样使用项目符号缩进和段后间距：
  ```javascript
  slide.addText([{text:"placeholder.",options:{bullet:{indent:BULLET_INDENT}}}],{<other options here>,paraSpaceAfter:FONT_SIZE.TEXT*0.3})
  ```
- **不要**直接使用 `•`，**不要使用 UNICODE 项目符号**，而应使用上面提到的 PptxGenJS 项目符号

### 内容与布局

- 内容要非常全面，并不断迭代直到作品精良。您必须确保所有文本都不会被其他元素遮挡
- 所有内容必须完全位于幻灯片内——**绝不能**溢出幻灯片边界。**这一点至关重要**。如果 `pptx_to_img.py` 显示内容溢出警告，您**必须**解决该问题。常见问题是元素溢出（尝试通过 `x`、`y`、`w` 和 `h` 重新定位或调整元素大小）或文本溢出（重新定位、调整大小或减小字体大小）
- 请记住在您的 `output.mjs` 代码中用实际内容替换所有占位符图片或块。**不要**在最终的演示文稿中使用占位符图片

### 图表要求

- 当您使用 PptxGenJS 图表时，请确保始终使用这些图表选项包含坐标轴标题和图表标题：
  - `catAxisTitle: "x轴标题"`
  - `valAxisTitle: "y轴标题"`
  - `showValAxisTitle: true`
  - `showCatAxisTitle: true`
  - `title: "图表标题"`
  - `showTitle: true`
- 默认使用模板的 `16x9`（10 x 5.625 英寸）布局制作幻灯片

### 图片生成限制

- 只用PptxGenJS 的API来绘制图表
  - Chart type of PptxGenJS can be any one of pptx.ChartType: pptx.ChartType.area, pptx.ChartType.bar, pptx.ChartType.bar3d, pptx.ChartType.bubble, pptx.ChartType.bubble3d, pptx.ChartType.doughnut, pptx.ChartType.line, pptx.ChartType.pie, pptx.ChartType.radar, pptx.ChartType.scatter.
  - Combo charts have a different function signature than standard. There are two parameters: chartTypes and options. ChartTypes can be any one of pptx.ChartType, although pptx.ChartType.area, pptx.ChartType.bar, and pptx.ChartType.line will give the best results.
- 创建幻灯片时：**不要**使用 imagegen 生成图表、表格、数据可视化或任何内部包含文本的图片（对于这些情况，应搜索现有图片）；除非用户明确要求，否则仅将 imagegen 用于装饰性或抽象图片
- **不要**使用 imagegen 描绘任何现实世界的实体或具体概念（例如徽标、地标、地理参考）

### 幻灯片内容规则（至关重要）

**页数限制**：
- **生成的幻灯片切勿超过 30 页**

**标题格式**：
- 避免使用"标题：副标题"的格式作为标题；这种格式显得非常有 AI 感
- 应通过**叙事性的主题句**将整个演示文稿串联起来

**语言风格**：
- 明确避免陈词滥调的"AI 废话（AI slop）"模式。切勿使用诸如"不仅仅是 [X]，而是 [Y]"之类的短语
- 使用直接、自信、主动的人类语言

**禁止内容**：
- 切勿包含任何供作者插入姓名、日期等的占位符幻灯片
- 切勿要求包含知名人物的逼真照片
- **切勿以通用的"有任何问题吗？"或"谢谢"幻灯片结尾**。相反，封底应为经过设计的结束语、有意义的引用或强有力的视觉总结，以此锚定整个叙事

### 大纲编写规则

请记住以下大纲编写规则：

- 专注于演示文稿的大纲以及每张幻灯片应涵盖的内容
- 每张幻灯片的描述必须全面且结构严谨
- **第 1 页必须是封面页，最后一页必须是封底页。** 请注意，这两张幻灯片的视觉风格和布局应与内部内容页截然不同（例如，使用"海报式"布局、醒目的排版或满版出血图像），以设定基调并提供强有力的结尾
- 对于每一张幻灯片，必须严格按照以下 4 个部分输出内容：

  **NARRATIVE GOAL (叙事目标)**
  解释这张幻灯片在整个故事弧光中的具体叙事目的

  **KEY CONTENT (关键内容)**
  列出标题、副标题和正文/要点。每一个具体数据点都必须能追溯到源材料。

  **VISUAL (视觉画面)**
  描述支持该观点所需的图像、图表、图形或抽象视觉元素。

  **LAYOUT (布局结构)**
  描述构图、层级、空间安排或焦点。

- 保留源素材中的关键要素
- 每一个具体的数据点都必须能直接追溯到源素材
- 所有细节都需要提及，因为设计师之后将无法访问源内容
- 永远假设听众比想象的更专业、更感兴趣、更聪明

---

## 第十二部分：工作流程

### ⚠️ 重要原则：图片规划与PPT代码编写可并行执行

> **🛑 反直觉警告（必读，下文有完整反思教训）**
>
> 设计师的本能是先写代码、再补图。**这是错的。** 形状、几何块、单字圆形图标（如"AI"/"经"塞进小圆圈）等都不是"视觉元素"的合格替代品。19 页演示文稿**至少**要为封面 + 2 个核心模型页 + 1 个收官页生图，目标张数 4–6 张起步。
>
> 任务开始前**先**扫一眼可用 skill：huny-img... 等。任何一个能生图的 skill 都行——**不是"有没有完美的图"，而是"有没有图"**。

1. **Task 0（图片规划）**：先完成所有图片的规划（placeholder_id、prompt、尺寸、位置）。**这不是"如需要"的任务，是必做项。**
2. **Task 3（PPT代码）**：先写PPT代码，在代码中预留图片占位符（灰色矩形，标注placeholder_id）
3. **并行执行**：启动subagent(s)调用文生图skill生成图片，同时主进程可以继续完善PPT代码
4. **图片替换**：图片生成完成后，下载到output目录，替换PPT代码中的占位符矩形
5. **最终执行**：运行更新后的PPT代码，生成最终文件

### Task 0: 图片规划清单（必须在 Task 1 之前完成 — 必做、不可跳过）

为每张需要图片的幻灯片准备以下信息：

```
每张图片需要包含：
- placeholder_id: 唯一标识，如 "Page-1-Image-1"
- page_number: 幻灯片页码
- image_prompt: 文生图prompt（英文，中文内容用拼音或描述）
- aspect_ratio: [1:1, 3:4, 4:3, 9:16, 16:9] 之一
- pixel_size: 根据aspect ratio换算的像素尺寸
- x, y: 在幻灯片中的绝对位置（英寸）
- w, h: 在幻灯片中的宽高（英寸）
- text_zone: 图片与文字的位置关系（left/right/top/bottom/overlay）
- color_guide: 配色要求（如品牌色值）
```

**调用文生图skill生成图片**：
1. 根据需要选择可用的文生图skill（如 `huny-img` 等）
2. 根据aspect ratio确定pixel_size
3. 设计符合风格指南的prompt，**必须包含**：具体颜色值、尺寸比例、文件格式、所在页码、内容描述
4. 执行图片生成脚本
5. 下载图片到 `{OUTPUT_DIR}/{placeholder_id}.png`
6. 验证图片尺寸与预期一致

**Task 0 的硬性产出指标**（满足任意一条才算"完成"）：
- ✅ `output.mjson` 中每张幻灯片的 elements 数组**至少含一个 `type: "image_placeholder"` 条目**，且对应 prompt 已写入
- ✅ 生图脚本已经在执行中或图片已下载到 `OUTPUT_DIR`
- ✅ `output.cjs/.mjs` 中存在至少一处 `addImage({ path: ... })`（或对应的占位符矩形 + TODO 注释）

**如果三项都不满足，** Task 0 没做完。**立刻停下补图，不要继续写代码。**

### Task 1: 提炼Story Line

1. 根据用户的输入和附件，先进行归纳，提炼出整体结构Story Line
   - 如果是大会演讲：采用"开头交待背景、抛出问题和冲突，然后展开3个大点，每个大点下3个小点，最后总结展望"的结构
   - 如果是产品服务提案：采用"问题、洞察分析、解决方案和对策、路线图和具体计划"的结构
   - 如果是工作汇报：采用"原计划、进度进展成果、问题和阻碍、需要领导支持的地方、下一步行动计划"的结构
   - 如果都不符合：由AI建议合适结构

### Task 2: 设计每一页内容

1. 幻灯片封面的id设定为0，正文页面的id编号与页码相同都从1开始
2. 要区分主次轻重，区分哪些内容需要用图片、图标、图表、charts、table等来支持
3. 每页内容都要至少包含整页的layout设计，以及幻灯片标题、正文、图标建议、图表内容（如有）、**图片占位符（来自Task 0）**。**图片必须先设计布局再生成，不能先生成图片再随意放置**。每页幻灯片上图片数量通常为0~2张。图片的aspect ratio只能是[1:1, 3:4, 4:3, 9:16, 16:9]之一
4. 进行事实核查，幻灯片所引用的内容，必须符合用户输入的原意，最好是原文，给出引用出处
5. **输出规范文档**：将设计规范输出到 `output.mjson`，包含每页的完整布局、元素坐标、内容结构。JSON规范是代码审查和修改的依据，必须在写PPT代码前完成。

### Task 3: 生成PPT代码

1. 根据上一步的json，按照幻灯片制作备注，基于PptxGenJS 语法（Version 3.0+），修改到 `output.mjs` 文件（支持ES Module），用于后续一键生成幻灯片。默认输出目录为当前工作目录。
2. 根据要求，生成整体的视觉风格
3. 补充适合于本页内容的视觉元素（图片、智能图形、图标、图表），体现美观大方专业。**先预留占位符**（灰色矩形填充，标注`placeholder_id`），**不要直接放入图片**
4. 基于16宫格网格对每一页内容layout排版，比如左右二分、左右三分、上下分割、四宫格、六宫格等常见布局。平衡文字和图形的比重
5. 检查每页的主要内容在布局排版上不能重叠
6. 每一页的各种内容和"文生图prompt"，放入每页的"演讲者注释"里
7. 如果有生成口播稿脚本，放入每页的"演讲者注释"里
8. 构建每一页的幻灯片代码，最前面都用`console.log('building slide...')`函数输出进度，便于后续调试
9. 构建完所有幻灯片，加一句日志输出每一页幻灯片的元素数量，便于后续调试
9.5. **🛑 写代码前自检：本次任务已经按 Task 0 完成图片生成了吗？** 如果 `output.mjson` 里没有 `image_placeholder` 条目，请**回去补 Task 0**，不要硬着头皮写形状版。
10. **图片占位符代码示例**：
    ```javascript
    // 占位符矩形（灰色填充，标注placeholder_id）
    slide.addShape(pres.ShapeType.rect, {
      x: 0.5, y: 1.5, w: 4.0, h: 2.5,
      fill: { color: "CCCCCC" }
    });
    // 注释：在图片生成完成后，替换为：
    // slide.addImage({
    //   path: OUT_DIR + "/Page-1-Image-1.png",
    //   x: 0.5, y: 1.5, w: 4.0, h: 2.5
    // });
    ```
11. **并行执行图片生成**：启动subagent(s)调用文生图skill生成Task 0中规划的所有图片
12. **图片替换**：图片生成完成后，下载到output目录，用`slide.addImage({path: ...})`替换占位符矩形
13. **最终执行**：运行更新后的PPT代码，生成最终文件
14. 所有生成的文件都应只保存在工作目录下的新目录 `pptx-gen-{TIMESTAMP}`

### Task 4: 复查与验证

1. 复查以上所有步骤都已经完成。特别要检查，必须为需要图片的页面设计prompt并生成图片
2. **布局验收checklist（每张有图片的幻灯片都必须验证）**：
   - [ ] 占位符矩形在布局中有精确定位（x, y, w, h）
   - [ ] 图片aspect ratio与占位符一致
   - [ ] 图片与文字区域不重叠（如果文字在左，图片在右，反之亦然）
   - [ ] 图片使用`path`参数正确嵌入，不是`url`
   - [ ] `pptx_to_img.py`无溢出警告
   - [ ] 所有占位符矩形已被替换为实际图片（无残留灰色占位符）
3. **🛑 图片覆盖率验收（不可妥协）**：
   - [ ] 整本 PPT 至少包含 4 张实际图片（封面 + 至少 3 张内容页）
   - [ ] 如果总页数 ≥ 6 但 `addImage` 调用次数 < 4，**视为 Task 0 未完成**，回去补图
   - [ ] 不允许用形状、字符、几何块"假装"成图片
4. **如果图片数量不达标，必须主动询问用户：**
   - 「当前已完成 [N] 页形状版，封面和核心页（如 ADKAR、CLARC）建议补 [M] 张主题插画，要现在补吗？」
   - 而不是悄悄交付一个无图版本。

---

### 反思教训 — 为什么必须先生成图片

> 📌 **本节来自一次真实的失败。** 写下来是为了下次不再犯。

#### 失败回放

一次 19 页的「引领团队，迎战变革」培训 PPT 制作过程中，我犯的错：

| 错误 | 具体表现 | 真实代价 |
|------|---------|---------|
| ❌ 把图片生成写成 "如需要" | todo 列表里写「生成图片（如需要）」 | 给自己留了"不需要"的退路，结果真就没做 |
| ❌ 跳过 Task 0 | 没有任何 `output.mjson` 里 `image_placeholder` 条目 | 后面想补也无从下手 |
| ❌ 用形状假装是图片 | 把"AI/经/贸/环/市/效"单字塞进 0.6" 小圆圈 | 看起来业余，明显是"权宜之计" |
| ❌ 排查 `react-icons`/`sharp` 失败就放弃 | 改用单字字符 | 完全忽略 `wanx-img`、`huny-img`、`minimax` 等可用 AI 生图 skill |
| ❌ 自欺式判断"已经够丰富了" | 通篇 19 页都是 形状+文字+金句 | 封面、ADKAR、CLARC、收官页都本应有图 |

最终产物 489 个元素、19 张幻灯片全部在边界内、结构 OK，但**没有一张配图**。用户原话："good, 但是反思你为什么没生成任何图片？"

#### 五个常见借口（每个都是陷阱）

| 借口 | 为什么是陷阱 | 正确做法 |
|------|------------|---------|
| "形状+图标已经够丰富了" | 形状永远不是图片；通篇几何感会让演示看起来像流程图而非商务演示 | **默认要为封面 + 核心模型页 + 收官页配图** |
| "react-icons / sharp 不可用" | 那是 npm 库问题；**AI 生图 skill 是另一条路** | 扫一眼 `huny-img`、`wanx-img` 、`minimax`等可用的图生 skill |
| "生图耗时太长" | 调用 AI 生图 + 下载 ≈ 1–2 分钟/张；**不生图的代价是用户重做** | 早花 5 分钟生图 vs 晚花 20 分钟返工 |
| "环境没装 LibreOffice/soffice" | 这影响的是 PDF 转图片做 QA，**不影响 PPT 内嵌图片** | 区分开"QA 工具" vs "PPT 内容"两件事 |
| "用户没明确要图" | 用户说"做个 PPT"等价于"做份好看的 PPT"，好看就需要图 | 默认 4–6 张起步；少图要明确说"极简版" |

#### Task 0 红线（绝对不可让步）

> **🛑 如果 PPT 总页数 ≥ 6 张，必须在 Task 0 阶段启动图片生成。**
> 阈值是 6 张，不是 30 张。即便只做 6 页，也至少要有封面图 + 1 张内容图。

**Task 0 必做三件事**（缺一即视为流程违规）：
1. 在 `output.mjson` 至少标注 N 个 `image_placeholder`（N = 总页数 × 0.3，向上取整）
2. 调用至少一个图生 skill（`huny-img` /`wanx-img` ）生成图片
3. 把生成的图片路径写入 `output.cjs/.mjs`（用占位符矩形 + 注释，或直接 `addImage`）

#### 默认配图清单（按页面重要性）

| 页面类型 | 建议配图 | 数量 |
|---------|---------|------|
| 封面 | 主题意象图 / 人物剪影 / 抽象几何 | 1（必备）|
| 核心模型页（ADKAR/CLARC/流程图等）| 概念插画 / 示意性图像 | 1–2 |
| 故事/场景页 | 真实场景感插画 | 0–1 |
| 收官页 | 强视觉总结图 / 引言类图像 | 1（推荐）|
| 内容密集页 | 留白，不加图 | 0 |

#### 可用的图生 skill（不完全清单）

- **`huny-img`** — 混元图片（默认）
- **`wanx-img`** — 通义万相


> 调起方式：在主流程中通过 `Skill` 工具调用，或在 subagent 中指定。
> Prompt 设计要点：必须包含**颜色值、尺寸比例、文件格式、所在页码、内容描述**五要素。

#### 反思的动作

每次 PPT 任务结束前，自问：
1. 这一版里**真的有图**吗？（数一下 `addImage` 的调用次数）
2. 封面/封底/核心模型这三类页有图吗？
3. 如果用户说"good 但是..."，这个 "但是" 有没有可能就是因为没图？

如果任何一个答案是 "没有/可能"，**主动问用户是否需要补图**，不要等用户来问。

---

### 常见错误清单

⚠️ 以下问题会导致文件损坏、视觉 bug 或输出异常。避免之。

1. **绝不使用 "#" 前缀的十六进制颜色** — 导致文件损坏
   ```javascript
   color: "FF0000"      // ✅ 正确
   color: "#FF0000"     // ❌ 错误
   ```

2. **绝不在十六进制颜色字符串中编码透明度** — 8字符颜色（如 `"00000020"`）会损坏文件。使用 `opacity` 属性。
   ```javascript
   shadow: { type: "outer", blur: 6, offset: 2, color: "00000020" }          // ❌ 损坏文件
   shadow: { type: "outer", blur: 6, offset: 2, color: "000000", opacity: 0.12 }  // ✅ 正确
   ```

3. **使用 `bullet: true`** — 绝不使用 unicode 符号如 "•"（会造成双项目符号）
   ```javascript
   // ✅ 正确
   { text: "First item", options: { bullet: true, breakLine: true } },
   { text: "Second item", options: { bullet: true, breakLine: true } },

   // ❌ 错误 — 不要用 unicode bullets
   "• First item"
   ```

4. **数组项之间使用 `breakLine: true`** — 否则文字会连在一起

5. **避免 `lineSpacing` 与 bullets 搭配** — 会导致过大间隙；使用 `paraSpaceAfter` 代替

6. **每次创建新实例** — 不要复用 `pptxgen()` 对象

7. **绝不要重用 option 对象** — PptxGenJS 会 in-place 修改对象（如将 shadow 值转换为 EMU）。共享一个对象会导致第二个 shape 损坏。
   ```javascript
   const makeShadow = () => ({ type: "outer", blur: 6, offset: 2, color: "000000", opacity: 0.15 });
   slide.addShape(pres.shapes.RECTANGLE, { shadow: makeShadow(), ... });  // ✅ 每次新建
   slide.addShape(pres.shapes.RECTANGLE, { shadow: makeShadow(), ... });
   ```

8. **不要对 accent borders 使用 `ROUNDED_RECTANGLE`** — 矩形叠加条无法覆盖圆角。使用 `RECTANGLE`。

9. **图表始终包含坐标轴标题和图表标题**：
   ```javascript
   slide.addChart(pres.charts.BAR, chartData, {
     catAxisTitle: "x轴标题",
     valAxisTitle: "y轴标题",
     showValAxisTitle: true,
     showCatAxisTitle: true,
     title: "图表标题",
     showTitle: true,
     // ... 其他样式
   });
   ```

10. **让图表更美观的选项**：
    ```javascript
    {
      chartColors: ["0D9488", "14B8A6", "5EEAD4"],
      chartArea: { fill: { color: "FFFFFF" }, roundedCorners: true },
      catAxisLabelColor: "64748B",
      valAxisLabelColor: "64748B",
      valGridLine: { color: "E2E8F0", size: 0.5 },
      catGridLine: { style: "none" },
      lineSmooth: true,
      legendPos: "r"
    }
    ```

11. **布局名称必须正确** — 使用 `LAYOUT_16x9` 而不是 `'16x9'`
    ```javascript
    pres.layout = 'LAYOUT_16x9';              // ✅ 正确
    pres.layout = { name: '16x9', width: 10, height: 5.625 };  // ✅ 正确
    pres.layout = '16x9';                     // ❌ 错误：UNKNOWN-LAYOUT
    ```

12. **所有元素必须位于幻灯片边界内** — 装饰元素也要遵守边界规则
    - 幻灯片尺寸：10" x 5.625" (16:9)
    - 所有元素 x ≥ 0, y ≥ 0, x+w ≤ 10, y+h ≤ 5.625
    - 延伸到边界外（如 x: -1）的装饰元素可能引发渲染问题
    ```javascript
    // ❌ 错误：装饰元素出界
    slide.addShape(pres.ShapeType.ellipse, { x: -1, y: -1, w: 4, h: 4, ... });

    // ✅ 正确：将装饰元素控制在边界内，或使用clip裁剪
    slide.addShape(pres.ShapeType.ellipse, { x: 0, y: 0, w: 4, h: 4, ... });
    ```


