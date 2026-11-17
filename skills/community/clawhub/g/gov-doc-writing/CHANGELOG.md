# 国央企Word文档技能更新日志

## [1.8.0] - 2026-10-27

### 变更（为 WorkBuddy 收录做准备）
- **前置元数据合规化**：`name` 由中文名改为 hyphen-case 的 `gov-doc-writing`，新增 `display_name_zh`/`display_name_en`、`description_en`、`agent_created: true`，使技能满足 WorkBuddy 技能规范与收录校验。
- **脚本路径动态化**：将 SKILL.md 中硬编码的 `gov-doc-writing__skillhub/scripts/` 路径改为「本技能安装目录/scripts/create_gov_doc.js」的动态说明，避免技能被 WorkBuddy 收录（目录不再带 `__skillhub` 后缀）后路径失效。
- **清理市场专属元数据**：导出用于收录的包中移除 `_skillhub_meta.json`、`_meta.json`、`package.json`、`package-lock.json`、`skill-card.md` 等第三方市场文件。

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
