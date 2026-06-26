---
name: "国央企word文档"
description: "此技能用于创建符合中国政府及央企规范的Word文档(.docx)。当用户要求创建公文、国央企文档、规范文书、正式报告等需要特定中国公文格式的文档时使用此技能。"
author: "刘洪亮"
version: "1.10"
---

# 国央企Work文档创建技能

本技能用于创建符合中国政府及央企规范的Word文档(.docx)，使用Microsoft Word最新格式。

## 文档格式规范

### 页面设置

| 属性 | 值 |
|------|-----|
| 纸张 | A4 |
| 上边距 | 3.7厘米 |
| 下边距 | 3.5厘米 |
| 左边距 | 2.8厘米 |
| 右边距 | 2.6厘米 |
| 页码 | 居中显示，宋体四号 |

### 字体规范

| 样式 | 中文字体 | 西文字体 | 字号 |
|------|----------|----------|------|
| 首页大标题 | 方正小标宋简体 (FZXiaoBiaoSong-B05S) | Times New Roman | 小二号 (18pt) |
| 正文 | 方正仿宋简体 (FZFangSong-Z02S) | Times New Roman | 小三号 (15pt) |
| 一级标题 | 黑体 | Times New Roman | 小三号 (15pt) |
| 二级标题 | 楷体 | Times New Roman | 小三号 (15pt) |
| 三级标题 | 方正仿宋简体 (FZFangSong-Z02S) | Times New Roman | 小三号 (15pt) 加粗 |
| 落款-部门 | 方正仿宋简体 (FZFangSong-Z02S) | Times New Roman | 小三号 (15pt) |
| 落款-日期 | 方正仿宋简体 (FZFangSong-Z02S) | Times New Roman | 小三号 (15pt) |
| 页码 | 宋体 | - | 四号 (14pt) |
| 表格 | 方正仿宋简体 (FZFangSong-Z02S) | Times New Roman | 小五号 (9pt) |

### 行间距

| 样式 | 行间距 |
|------|--------|
| 首页大标题 | 固定28磅 |
| 正文 | 固定28磅 |
| 一级标题 | 固定28磅 |
| 二级标题 | 固定28磅 |
| 三级标题 | 固定28磅 |
| 落款-部门 | 固定28磅 |
| 落款-日期 | 固定28磅 |
| 图片 | 单倍行距 |
| 表格 | 单倍行距 |

### 段落格式

| 样式 | 序号格式 | 首行缩进 | 大纲级别 |
|------|----------|----------|----------|
| 正文有缩进 | 无 | 2字符 | - |
| 一级的标题 | 一、二、三、 | 2字符 | 1级 |
| 二级的标题 | （一）（二）（三） | 2字符 | 2级 |
| 三级的标题 | 1.2.3. | 2字符 | 3级 |
| 落款-部门 | 无 | 无 | - |
| 落款-日期 | 无 | 无 | - |

## 样式名称

创建文档时，必须使用以下样式名称：

- `首页大标题` - 首页大标题
- `正文有缩进` - 正文段落
- `一级的标题` - 一级标题
- `二级的标题` - 二级标题
- `三级的标题` - 三级标题
- `图片样式` - 图片
- `表格样式` - 表格
- `落款-部门` - 部门落款（右下对齐）
- `落款-日期` - 日期落款（右下对齐，自动与部门左对齐）
- `页码样式` - 页脚页码

## 使用方法

### 方式一：使用JavaScript脚本创建文档

```javascript
const {
  createDocument,
  createTitleParagraph,
  createBodyParagraph,
  createLevel1Heading,
  createLevel2Heading,
  createLevel3Heading,
  createTable,
  createImageParagraph,
  CHINESE_FONTS,
  FONT_SIZES,
  CONTENT_WIDTH,
  Packer,
  BorderStyle,
  WidthType,
  ShadingType,
  VerticalAlign,
  Paragraph,
  TextRun,
  Table,
  TableRow,
  TableCell,
  Footer,
  ImageRun,
} = require('~/.openclaw/skills/gov-doc-writing/scripts/create_gov_doc.js');

// 创建文档
const doc = createDocument({
  title: '文档标题',
  sections: [
    // 首页大标题
    createTitleParagraph('这是文档标题'),

    // 一级标题
    createLevel1Heading('第一章', 0),  // 输出: 一、第一章
    createLevel1Heading('第二章', 1),  // 输出: 二、第二章

    // 二级标题
    createLevel2Heading('第一节', 0),  // 输出: （一）第一节
    createLevel2Heading('第二节', 1),  // 输出: （二）第二节

    // 三级标题
    createLevel3Heading('第一点', 0),  // 输出: 1.第一点
    createLevel3Heading('第二点', 1),  // 输出: 2.第二点

    // 正文
    createBodyParagraph('这是正文内容，首行自动缩进2字符。'),

    // 表格
    createTable(
      [
        { children: ['表头1', '表头2', '表头3'] },
        { children: ['内容1', '内容2', '内容3'] },
      ],
      { columnWidths: [2000, 2000, 2000] }
    ),
  ]
});

// 生成文件
Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync('output.docx', buffer);
});
```

### 方式二：使用CLI命令

```bash
node scripts/create_gov_doc.js output.docx '{
  "title": "文档标题",
  "body": [
    {"type": "heading1", "text": "第一章", "number": 0},
    {"type": "paragraph", "text": "正文内容"},
    {"type": "table", "rows": [...], "columnWidths": [2000, 2000, 2000]}
  ]
}'
```

## 表格规范

- 表格宽度自动适应窗口（百分比100%），无需手动计算列宽
- 列宽比例通过 `columnWidths` 参数控制（DXA 相对值，实际宽度自动缩放）
- 表头：灰色底 (#D9D9D9)、加粗、居中
- 内容：白色底、居中、小五号 (9pt) 字体
- 边框：单线黑色

```javascript
// 表格示例
const border = { style: BorderStyle.SINGLE, size: 1, color: "000000" };
const borders = { top: border, bottom: border, left: border, right: border };

// 表头行
new TableRow({
  tableHeader: true,
  children: [
    new TableCell({
      borders,
      shading: { fill: "D9D9D9", type: ShadingType.CLEAR },
      children: [new Paragraph({ children: [new TextRun({ text: "表头", bold: true })] })]
    })
  ]
});
```

## 落款规范

- 落款（部门名称 + 日期）放文档右下角，与上方正文间隔一行
- 两行均右顶格对齐，不加缩进；日期自然向左延伸
- 部门名称使用 `落款-部门` 样式，日期使用 `落款-日期` 样式，均为方正仿宋小三号
- 使用 `createSignatureBlock()` 一键生成

```javascript
const { createSignatureBlock } = require('...');

// 一键创建落款块（含间隔空行 + 部门名称 + 日期）
sections.push(...createSignatureBlock('科技创新部', '2026年6月'));
```

## 图片规范

- 行间距：单倍行距
- 对齐：居中
- 样式名称：`图片样式`

## 文档属性

- 删除文档作者（`dc:creator` 和 `lastModifiedBy` 留空或不写入）
- 在创建文档时不要设置 `creator` 属性，或设置为空字符串

## 完整示例

```javascript
const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Footer, BorderStyle, WidthType, ShadingType, VerticalAlign,
  PageNumber, ImageRun, AlignmentType, HeadingLevel, LevelFormat,
  createTitleParagraph, createBodyParagraph, createLevel1Heading,
  createLevel2Heading, createLevel3Heading, createTable,
  createImageParagraph, createSignatureBlock, createDocument, CHINESE_FONTS, FONT_SIZES,
  CONTENT_WIDTH, PAGE_MARGINS, LINE_SPACING_EXACT_28
} = require('~/.openclaw/skills/gov-doc-writing/scripts/create_gov_doc.js');

// 内容构建
const sections = [
  createTitleParagraph('关于XXX工作的报告'),

  createLevel1Heading('一、基本情况', 0),
  createBodyParagraph('这里是正文内容，详细描述基本情况。'),
  createBodyParagraph('继续描述相关内容和细节。'),

  createLevel1Heading('二、主要做法', 1),
  createLevel2Heading('（一）加强组织领导', 0),
  createBodyParagraph('具体做法描述...'),
  createLevel2Heading('（二）完善制度建设', 1),
  createBodyParagraph('制度建设内容...'),

  createLevel1Heading('三、存在问题', 2),
  createBodyParagraph('当前存在以下问题：'),
  createLevel3Heading('问题一', 0),
  createBodyParagraph('问题一的具体描述。'),
  createLevel3Heading('问题二', 1),
  createBodyParagraph('问题二的具体描述。'),

  createLevel1Heading('四、下一步计划', 3),
  createBodyParagraph('针对以上问题，计划采取以下措施...'),

  // 落款（右下对齐，与正文间隔一行）
  ...createSignatureBlock('科技创新部', '2026年6月'),
];

// 创建文档（不设置作者）
const doc = createDocument({
  title: '关于XXX工作的报告',
  sections
});

// 生成并保存
Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync('report.docx', buffer);
  console.log('文档已生成: report.docx');
});
```

## 注意事项

1. **字号转换**：Word中的"号"转换为半磅值（如小三号=30，小二号=36，四号=28，小五号=18）
2. **行间距固定28磅**：line值设置为560（28 × 20），lineRule设置为"exact"
3. **首行缩进**：使用 `indent: { firstLine: charWidth * 2 }`，字符宽度约等于字号的一半
4. **页码**：仅在页脚居中显示，使用宋体四号
5. **不要封面**：文档从首页大标题开始，不创建封面页
6. **文档作者**：不设置或留空
7. **双引号自动规范化**：所有文本内容中的 ASCII 双引号 `"` 会自动替换为配对的中文双引号 `""`（`\u201c`/`\u201d`），无需手动转换
8. **中西文字体分段写入**：`createTextRunsFromSegments` 对每个 TextRun 均明确写入字体（西文：Times New Roman；中文：对应中文字体 + Times New Roman）。**不要**使用 `useDirectFormatting: false` 模式（已废弃），始终明确写字体以保证 Word 渲染稳定。
9. **docDefaults 字体**：`createDocument` 的 `styles.default.document.run.font` 必须使用对象格式（`{ eastAsia, ascii, hAnsi, cs }`），不能传字符串，否则 `docDefaults` 中 ascii/hAnsi 会被设为中文字体导致西文渲染错误。
10. **pPrDefault 行距**：`createDocument` 的 `styles.default.document.paragraph` 必须设置 `spacing: { before: 0, after: 0, line: 560, lineRule: "exact" }`，确保 `pPrDefault` 不为空。这使 Normal（正文）样式在 Word 样式窗格中显示正确的28磅固定行距。无需额外定义 Normal 样式，各自定义样式通过 `basedOn: "Normal"` 继承后自行覆盖 spacing。

## 相关文件

- `scripts/create_gov_doc.js` - 核心创建函数库
