# PPTX 可编辑管线技术规则

> 此文件是 `ppt-pro` skill 的 reference，按需加载。包含 HTML→PPTX 提取管线的不可违反的技术约束。

## data-pptx-role 分层架构

HTML 生成阶段通过 `data-pptx-role` 属性标注每个元素的语义角色，提取阶段严格以 role 为唯一分层依据。

| 角色 | 含义 | 截图行为 | PPTX 输出 |
|------|------|---------|----------|
| `content` | 用户可编辑的文字/数据 | 隐藏文字 | 原生文本框 + 形状 |
| `content-icon` | 用户可移动的 SVG 图标/图表 | 隐藏整个元素 | 嵌入 SVG/PNG 图片 |
| `decoration` | 纯视觉装饰（CSS 渐变、光晕、与内容无关的装饰线条等） | 保留在背景 | 不提取 |
| `watermark` | 大字水印 | 保留在背景 | 不提取 |

分类原则：
- SVG（WAI-ARIA）：隐藏后丢失信息 → `content-icon`；仅丢失视觉风格 → `decoration`
- 箭头/连接符（→、⇢、▼等）：表示步骤顺序/数据流向 → `content`；纯装饰性 → `decoration`
- 代码侧 `ARROW_CHARS`（U+2190–21FF 全区间及补充箭头区块）仅作为 **fallback 安全网**：当 LLM 误将箭头标为 decoration 时，`isDecorativeElement` 会将其救回前景文本提取。主路径是 prompt 规则 8 引导 LLM 直接将箭头标为 `content`

## 颜色处理

- CSS Color Level 4：Chrome getComputedStyle 返回 `color(srgb r g b / alpha)` 格式，必须与 `rgba()` 都支持
- SVG rgba 保真：fill/stroke/stop-color 的 alpha 分离为 fill-opacity/stroke-opacity/stop-opacity

## 形状提取

- 单边 border 拆分：PPTX 不支持 per-side border → 拆分为填充矩形 + 窄色带矩形
- 双 border 元素：≥2 边有 border 时即使 transparent 背景也提取为 shape
- 圆角阈值：borderRadius >= 4 → roundedRect
- z-order：插入顺序 shapes → icons → text boxes

## 图标/图片处理

- icon PNG 透明度：Puppeteer screenshot 产生不透明矩形，有 SVG 的 icon 用 cairosvg 生成透明 PNG
- Icon bbox 精确性：SVG 容器远大于内部 SVG 时，使用 SVG 自身 bbox
- DOM 漂移防护：icon 坐标使用 DOM 修改前的原始坐标

## CSS 图形

- conic-gradient → 解析为 doughnut 原生图表（CategoryChartData + 逐 point 着色 + XML holeSize）
- radial-gradient → 装饰性背景，不提取为 icon

## 原生图表

- 使用标准 python-pptx API：has_legend=False, has_title=False, has_data_labels=False
- 禁止手动注入 dLbls/spPr XML（破坏 MS PPT/WPS 兼容性）
- chartSpace spPr 位置：c:spPr 在 c:chart 之后（用 addnext()）

## 原生表格

- HTML `<table>` → python-pptx add_table()，提取必须在 hideTextElement 之前
- 表格样式清除：No Style, No Grid（`{2D5ABB26-…}`）
- 半透明单元格：低 alpha 需与底色 alpha-blend 为不透明色
- 单元格边框：_set_cell_border XML helper（a:lnT/a:lnB/a:lnL/a:lnR）
- cell margin：cell.margin_left 而非 text_frame.margin_*

## 尺寸转换

- CSS 1px = 0.75pt（96dpi vs 72dpi）
- 控件尺寸以 HTML bbox 为准，字号服从控件

## DOM 分析架构

模块注入顺序：constants.js → color-utils.js → svg-utils.js → table-extractor.js → text-utils.js → dom-analyzer.js

通过 `window.__pptLib` 命名空间共享（IIFE 模式）。

## 文本提取

- collectLeafBlocks 跳过 content-icon 角色元素（decoration 中的箭头字符通过 containsArrowChar 豁免）
- collectDecoShapes 中 decoration/watermark 角色元素不参与形状提取，样式保留在背景截图中
- flex 子元素独立性检测：有独立背景色的 inline 子元素识别为块级
- 表格区域文本去重：textRegion 中心在 tableRegion 内时跳过
