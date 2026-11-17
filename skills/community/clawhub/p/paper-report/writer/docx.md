# 输出格式：Word (.docx)

原生 Word 文档（图片以二进制 PNG 内嵌于 OOXML 容器），适合在 Word / WPS / Pages 中阅读与二次编辑，便于走 OA 流转或公司内审。

---

## 1. 适用场景

- 用户明确要求"生成 Word 报告""docx""给我 Word 版"。
- 报告需要在 Microsoft Word / WPS / Pages 中**线下编辑**，或走公司 OA / 邮件附件 / 评审流转。
- 用户希望保留章节大纲（H1/H2/H3）以便后续在 Word 中使用导航窗格 / 自动目录。
- 与 HTML 报告对比：单文件、无 JS 依赖、无 base64 二次膨胀；与 Markdown 报告对比：单文件自包含、不另带 images 目录。

> Word 输出**不作为默认格式**——HTML 仍为默认，本格式仅在用户显式指定时启用。

## 2. 图片处理

调用模板库里的 `figure(filename, caption, opts?)`，传入 `{workspace}/figures/` 下的相对文件名即可：

```js
figure('fig1_architecture.png', '图 1：方法总体架构（原文 Figure 1）。')
```

库内部会：

- 读取 PNG 文件头 IHDR 段（前 24 字节）拿到原始 `width × height`，按 `opts.widthPx`（默认 560 px）等比缩放，避免拉伸。
- 用 `ImageRun` 把 PNG **原始字节**直接嵌入 docx，**不要**做 base64 二次编码（OOXML 容器本身就是 ZIP，PNG 进去即被压缩）。
- 在图片下方追加一个居中、斜体、灰色的 caption 段。

> 单张图片体积过大（>2 MB）时，建议在 `figures/` 目录里预先缩放（macOS 上 `sips`、跨平台可用 PIL / ImageMagick），避免 docx 体积失控。

## 3. 数学公式

`docx-js` 没有原生 LaTeX 渲染器，OOXML 的公式标记是 OMML，工程成本不值得为阅读报告引入。按复杂度分两条路：

- **简单符号**（行内变量、希腊字母、上下标）：在 `p([...])` 中用 Unicode 直接写，例如 `α`、`β`、`x₁`、`σ²`、`≥`、`→`。这样在任何 Word/WPS 中都是普通文本，不需要额外渲染。
- **复杂多行公式**：从 HTML 版本报告中借助 MathJax 截图（或用 poppler 的 `pdftoppm` 渲染单行公式），保存为 PNG 后用 `figure()` 嵌入。

模板库**不提供** `math()` 助手，避免 agent 在 Word 中堆砌只有部分渲染器支持的 OMML。

## 4. 表格处理

调用 `table({ caption, cols, rows, headerFill? })`，列宽必须以 DXA（1440 DXA = 1 英寸）声明：

```js
table({
  caption: '表 1：主要超参数对照（原文 Table 1）。',
  cols: [3000, 3000, 3360],          // 三列；Σ === 9360
  rows: [
    ['超参', '取值', '说明'],
    ['学习率', '5e-4', '余弦退火'],
    ['批大小', b('1024'), '梯度累积 4 步'],
  ],
})
```

约定：

- 表宽固定为 **9360 DXA**（US Letter 12240 − 两侧各 1440 DXA 边距）。模板库会断言 `Σcols === 9360`，写错立即抛错。
- 首行自动作为表头（加粗 + 浅灰底）。
- 单元格内容可以是字符串，也可以是 `b('文本')` 等内联标记原语；最佳值用 `b(...)` 加粗，沿用 HTML / Markdown 的惯例。
- 不要使用 `WidthType.PERCENTAGE`，Google Docs 打开会崩。

## 5. 模板路径

[docx-template.js](docx-template.js)

该文件同时承担两个角色：

- **库**：导出 `buildDocx`、`h2`、`h3`、`p`、`b`、`i`、`code`、`bullet`、`numbered`、`highlight`、`figure`、`table` 等原语。
- **自检示例**：`if (require.main === module)` 块内含一段通用占位论文的最小可运行示例，直接 `node docx-template.js` 会在当前目录生成 `report_Example.docx`，可作为 API 演示和回归测试。

agent 写真实报告时：**复制** `docx-template.js` 旁起一个 `gen_<简短标题>.js`，删掉文件底部的示例块，保留 `require('./docx-template.js')` 和顶层 `buildDocx({...})` 调用，按真实论文内容填写 `meta + sections`。

## 6. 输出文件命名

保存到 `{workspace}/outputs/`：

- `report_{简短标题}.docx` —— 单一自包含文件

简短标题从论文标题中提取核心关键词（去除特殊字符，空格替换为 `-` 或 `_`）。**不需要**配套的 images 目录，所有 PNG 已嵌入 docx。

## 7. 写作风格细节

- **章节层级**：`h2()` / `h3()` 对应 Word 大纲的 Heading 2 / 3；顶部封面标题由 `meta.titleCn` 自动以 H1 居中渲染。
- **字体**：默认 `Arial` + 后备 `PingFang SC` / `Microsoft YaHei`，由模板库的默认样式表声明，正文 11 pt（22 半磅）。
- **颜色基调**：H1 / H2 用主色 `#1A365D`，H3 用副色 `#2B6CB0`，与 HTML 报告视觉一致。
- **正文段落**：使用 `p(...)` 包裹，两端对齐，行距 1.5。
- **重点结论卡片**：使用 `highlight([...])` —— 实现为单格表格，左侧 24 磅蓝边、底色 `#F7FAFC`，对应 HTML 报告的 `.highlight` 卡片。
- **列表**：项目符号用 `bullet(...)`，编号用 `numbered(...)`；**绝不**在 `p()` 中直接写 `•`、`·`、`*` 之类字面字符（详见 §9）。
- **图表引用**：正文中用"如图 1 所示"、"表 1 汇总了……"，与 HTML / Markdown 风格保持一致。

## 8. 校验清单

`.docx` 是 ZIP 容器，用 `unzip -l` 看清单即可完成结构校验，不依赖第三方验证器。

**通用检查**：

- 各章节标题完整、层级清晰
- 每个章节有实质内容，不存在空段落或 `{{...}}` 占位符残留
- 不包含"报告生成日期"或"AI 辅助生成"相关文字

**Word 专项检查**：

- 依赖预检（先于生成）：

  ```bash
  NODE_PATH="$(npm root -g)" node -e "require('docx')" \
    || npm install -g docx
  ```

- 结构完整性（生成后）：

  ```bash
  unzip -l {workspace}/outputs/report_{简短标题}.docx \
    | grep -E '\[Content_Types\]\.xml|word/document\.xml|word/styles\.xml|word/numbering\.xml'
  # 上述四项必须齐全
  ```

- 图片清点（数量应等于 `figure()` 调用次数）：

  ```bash
  unzip -l {workspace}/outputs/report_{简短标题}.docx \
    | grep -c 'word/media/'
  ```

- 视觉终审：由使用者在 Microsoft Word / WPS / Pages 中打开抽查首屏、目录/标题层级、图表位置与表格边界。docx 的目标渲染器就是这几个，任何自动化渲染差异都不作为 bug 判据。

## 9. 已知陷阱

- **不要字面项目符号字符**：`new TextRun('• item')` 会得到一个孤立的圆点字符，Word 不会识别为列表。必须用 `bullet(...)`，库内部走 `LevelFormat.BULLET` + numbering 定义。
- **表格列宽必须 DXA**：`WidthType.PERCENTAGE` 在 Google Docs 中会崩；`columnWidths` 数组之和必须等于表宽 9360 DXA。`table()` 已内置断言，写错立即抛错。
- **`ImageRun` 必须传 `type` 字段**：`'png' / 'jpg' / 'jpeg' / 'gif' / 'bmp' / 'svg'` 之一；`figure()` 根据扩展名自动推断，但若手动调底层 API 需自己指定。
- **PNG 尺寸**：直接给 docx-js 写固定 `width/height` 会按那个尺寸拉伸图片；`figure()` 解析 PNG IHDR 自动取原始宽高再等比缩放，**不要**绕过去自己写。
- **全局安装的 docx-js 在脚本中 require 失败**：Node 只在 `NODE_PATH` 或本地 `node_modules` 里找包，`npm install -g` 装的全局包默认不在解析路径上。`docx-template.js` 已内置候选路径 fallback（优先 `npm root -g` 结果、其次直接 `require('docx')`），因此复制到 `gen_<简短标题>.js` 后一般无需再关心；实在不行两种解法：
  1. 运行时 `NODE_PATH="$(npm root -g)" node script.js`；
  2. 在项目内 `npm install docx` 走本地依赖，`require('docx')` 直接命中。
- **`PageBreak` 必须在 `Paragraph` 内**：`children: [new PageBreak()]`，不能裸放在 section.children 里。
- **避免 Unicode 等宽空格 / 全角空格**：复制自 PDF/HTML 的内容里偶尔混入 `U+00A0` / `U+3000`，会在 Word 中显示为可见方块。`p()` 内部不会清洗，agent 自行清洗或避免来源含这种字符。
- **中文渲染必须走 `eastAsia` 字体槽**：OOXML 的字体属性有四槽 ascii / hAnsi / cs / eastAsia，只写 `font: 'Arial'` 字符串会把四槽全填 Arial——由于 Arial 本身无 CJK 字形，中文字符是否可见完全依赖渲染器"字体缺失自动回退"这个隐式行为，不同 Word 版本、字体包、企业策略、Word Online 等场景下都可能翻车，属于**结果不确定**的写法。模板 `FONT` 常量已固定使用 `{ ascii, hAnsi, cs: 'Arial', eastAsia: 'PingFang SC', hint: 'eastAsia' }` 对象形式，把 CJK 字体作为契约显式写入 OOXML；扩展库时任何新增 `TextRun` 必须复用 `FONT` 常量，**禁止**回退为裸字符串。缺 PingFang SC 的环境会由 Word/WPS 按 fontTable 顺序替换为 Microsoft YaHei / SimSun 等，均可接受。
- **`skills/docx` 自带的 `validate.py` 不可用**：该脚本要求 Python 3.10+ 的 `match` 语法 + `lxml` 模块，两项都缺时无法运行。退一步用 `unzip -l` 的结构完整性检查 + 使用者在 Word / WPS 中肉眼终审即可，无需强行满足其依赖。
