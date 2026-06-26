# 国央企Word文档技能更新日志

## [1.7.1] - 2026-05-26

### 修复

- **Bug 7：Word 样式窗格中「正文」（Normal）样式的行距不是28磅固定**
  - 问题：`docDefaults` 中仅设置了 `<w:rPrDefault>`（字体默认值），`<w:pPrDefault/>` 为空，导致 Normal（正文）样式缺少段落的行距定义，Word 样式窗格中显示为默认单倍行距而非固定28磅。
  - 修复：在 `createDocument` 的 `styles.default.document` 中增加 `paragraph` 键，设置 `spacing: { before: 0, after: 0, line: 560, lineRule: "exact" }`。这会填充 `<w:pPrDefault>`，使 Normal 样式自动继承28磅固定行距。
  - 影响函数：`createDocument`

## [1.7.0] - 2026-05-26

### 修复

- **Bug 6：正文及标题中西文字体不稳定，西文未显示 Times New Roman**
  - 问题根因一：`createTextRunsFromSegments` 中 `useDirectFormatting = false` 时，所有 `TextRun` 只写 `text` 字段，不包含任何 `<w:rPr>`，依赖段落样式 `run` 字段的字体继承。Word 对无 rPr 的 TextRun 在中西文混排时字体应用不稳定，导致西文片段（NETCONF、BIN 等）实际使用方正仿宋而非 Times New Roman。
  - 问题根因二：`createDocument` 的 `styles.default.document.run.font` 传入了字符串（`FZFangSong-Z02S`），导致 `docDefaults` 中 `w:ascii` 和 `w:hAnsi` 也被设置为方正仿宋，而非 Times New Roman，进一步加剧了西文字体错误。
  - 修复一：`createTextRunsFromSegments` 改为**始终为每个 TextRun 明确写入字体**：西文片段写 `ascii/hAnsi/cs = Times New Roman`，中文片段写 `eastAsia = 对应中文字体` + `ascii/hAnsi/cs = Times New Roman`。行距、缩进等段落属性仍由段落样式控制。
  - 修复二：`createDocument` 的 `styles.default.document.run.font` 改为对象格式：`{ eastAsia: FZFangSong, ascii: Times New Roman, hAnsi: Times New Roman, cs: Times New Roman }`，修正 `docDefaults` 中西文字体。
  - 废弃 `useDirectFormatting` 参数（保留签名兼容性，不再区分两种模式）。
  - 影响函数：`createTextRunsFromSegments`、`createDocument`

## [1.6.0] - 2026-04-25

### 变更
- **二级标题序号格式调整**：去掉序号后的顿号
  - 旧格式：`（一）、标题内容`
  - 新格式：`（一）标题内容`
  - 涉及函数：`createLevel2Heading`、`createLevel2HeadingSafe`

- **三级标题序号格式调整**：序号后改用点号，去掉顿号
  - 旧格式：`1、标题内容`
  - 新格式：`1.标题内容`
  - 涉及函数：`createLevel3Heading`

- **表格宽度改为自动适应**：改为百分比宽度，自动适应窗口和内容
  - 旧方式：固定 DXA 宽度（按页面内容区域计算）
  - 新方式：`WidthType.PERCENTAGE` 100%（自动铺满可用宽度）
  - 涉及函数：`createTable`

- **双引号自动规范化为中文引号**：所有文本内容中的 ASCII 双引号 `"` 自动替换为配对的中文双引号 `""`
  - 规则：按出现顺序奇偶配对，奇数位→左引号 `"`，偶数位→右引号 `"`
  - 已有的正确中文引号对保持不变，全角引号 `"` `"` 也统一为 `\u201c` `\u201d`
  - 奇数个引号时自动容错闭合为右引号
  - 涉及函数：`normalizeQuotes`（新增）、`createTextRunsFromSegments`、`createTitleParagraph`、`createTable`、`createTableHeaderRow`
  - 覆盖范围：正文、标题（全部层级）、表格单元格、表头行

## [1.5.0] - 2026-04-08

### 修复
- **Bug 5：正文首行缩进只有1字符而非2字符**
  - 问题：所有样式定义（`正文有缩进`、`一级的标题`、`二级的标题`、`三级的标题`）中的首行缩进计算公式错误
  - 错误公式：`Math.round(2 * FONT_SIZES['小三号'] / 2 * 10)` = 300 Twips（仅1字符）
  - 错误原因：`FONT_SIZES['小三号'] = 30`（半磅值 = 15pt），正确换算应为 `15pt × 20twips/pt = 300twips = 1字符`，2字符需要 `600 twips`；而原公式 `/2 * 10 = * 5` 实际只得到1字符
  - 修复公式：`2 * FONT_SIZES['小三号'] * 10` = 600 Twips（正确2字符）
  - 同时修复 `createDocument` 中 `charWidth` 变量的计算，从约150改为正确的300 Twips
  - 影响样式：`正文有缩进`、`一级的标题`、`二级的标题`、`三级的标题`

## [1.4.0] - 2026-04-07

### 新增
- 添加 `createGovDocument(content, outputPath)` 便捷函数，简化文档生成流程
  - 支持通过简单的内容对象定义文档结构
  - 支持类型：title、body、heading1、heading2、heading3、table
  - 自动处理标题序号计数和添加

### 修复
- **Bug 4：Word中显示"由多种样式组成"**
  - 问题：段落中的 `TextRun` 元素包含 `rPr`（直接格式化属性），导致 Word 认为段落同时应用了样式和直接格式化
  - 修复：移除所有 `TextRun` 中的 `rPr` 元素，只保留 `pPr` 中的 `pStyle` 样式引用
  - 影响函数：createTitleParagraph、createBodyParagraph、createLevel1Heading、createLevel2Heading、createLevel3Heading、createTable、createTableHeaderRow

## [1.3.0] - 2026-04-07

### 修复
- **Bug 3：Word中新增内容字体不生效**
  - 问题：样式定义中只使用 `run.font` 设置单一字体，Word 样式系统对于中西文混排需要分别指定中文字体和西文字体
  - 修复：在所有样式定义中将 `run.font` 从字符串改为对象格式
    - `eastAsia`: 对应中文字体（方正仿宋/黑体/楷体/方正小标宋）
    - `ascii`: Times New Roman（西文字体）
    - `hAnsi`: Times New Roman
    - `cs`: Times New Roman

## [1.2.0] - 2026-04-07

### 修复
- **Bug 2：表格中西文字体未正确应用**
  - 问题：表格单元格和表头行中的文本直接使用 `new TextRun` 创建，只指定了中文字体，没有分别处理中西文字符
  - 修复：
    - 修改 `createTable` 函数，使用 `createTextRunsFromSegments` 处理单元格文本
    - 修改 `createTableHeaderRow` 函数，使用 `createTextRunsFromSegments` 处理表头文本

## [1.1.0] - 2026-04-07

### 修复
- **Bug 1：标题序号重复**
  - 问题：一级、二级、三级标题函数在传入序号参数时会自动添加序号前缀，如果调用者已经在text中写了序号，会导致重复（如"一、一、会议议程"）
  - 修复：在 `createLevel1Heading`、`createLevel2Heading`、`createLevel3Heading` 函数中添加序号前缀检测逻辑
    - 检测text是否已包含对应格式的序号前缀
    - 如果已包含正确序号，则不再添加
    - 如果包含其他序号，则替换为正确序号
    - 如果没有序号，则添加序号前缀

## [1.0.0] - 初始版本

### 功能
- 创建符合中国政府及央企规范的Word文档(.docx)
- 支持页面设置（A4纸张、标准边距）
- 支持标准字体规范（方正小标宋、方正仿宋、黑体、楷体）
- 支持标题层级（一级、二级、三级标题）
- 支持表格创建（自动计算列宽、表头样式）
- 支持图片插入
- 支持页码设置
- 提供完整的JavaScript API
