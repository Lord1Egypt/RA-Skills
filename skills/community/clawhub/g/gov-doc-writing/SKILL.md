---
name: gov-doc-writing
display_name_zh: 国央企Word文档
display_name_en: Government & SOE Word Document
description: "此技能用于创建符合中国政府及央企规范的Word文档(.docx)。当用户要求创建公文、国央企文档、规范文书、正式报告等需要特定中国公文格式的文档时使用此技能。"
description_en: "Create Word documents (.docx) that comply with the formatting standards of Chinese government agencies and state-owned enterprises (SOEs). Use this skill when the user needs to produce official documents, SOE documents, formal standardized documents, or official reports that require specific Chinese official-document layout and typography."
author: 刘洪亮
version: "1.8.0"
agent_created: true
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
| 图片 | 单倍行距 |
| 表格 | 单倍行距 |

### 段落格式

| 样式 | 序号格式 | 首行缩进 | 大纲级别 |
|------|----------|----------|----------|
| 正文有缩进 | 无 | 2字符 | - |
| 一级的标题 | 一、二、三、 | 2字符 | 1级 |
| 二级的标题 | （一）、（二）、（三）、 | 2字符 | 2级 |
| 三级的标题 | 1.、2.、3.、 | 2字符 | 3级 |

## 样式名称

创建文档时，必须使用以下样式名称：

- `首页大标题` - 首页大标题
- `正文有缩进` - 正文段落
- `一级的标题` - 一级标题
- `二级的标题` - 二级标题
- `三级的标题` - 三级标题
- `图片样式` - 图片
- `表格样式` - 表格
- `页码样式` - 页脚页码

## 使用方法

### 方式一：使用JavaScript脚本创建文档

> **注意**：Node.js 的 `require` **不会**展开 `~`，必须传入脚本的绝对路径。本技能的脚本位于其安装目录下的 `scripts/create_gov_doc.js`。调用前，先用 `Glob` 或 `ls` 定位本技能的实际安装目录（即包含本 `SKILL.md` 的文件夹，例如 `~/.workbuddy/skills/gov-doc-writing/` 或带市场后缀的目录），将该绝对路径填入 `require`。
> 依赖 `docx` 需已安装，且运行时应设置 `NODE_PATH` 指向包含 `node_modules/docx` 的目录。

```javascript
// 将 <绝对路径> 替换为实际路径，例如：
// require('/Users/<用户名>/.workbuddy/skills/gov-doc-writing/scripts/create_gov_doc.js')
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
} = require('/Users/<用户名>/.workbuddy/skills/gov-doc-writing/scripts/create_gov_doc.js');

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
    createLevel2Heading('第一节', 0),  // 输出: （一）、第一节
    createLevel2Heading('第二节', 1),  // 输出: （二）、第二节
    // 注意：序号由第二个参数决定，且不会按章自动重置，需在每进入新的一级章节时把计数器归零

    // 三级标题
    createLevel3Heading('第一点', 0),  // 输出: 1、第一点
    createLevel3Heading('第二点', 1),  // 输出: 2、第二点

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

- 表格总宽度 = 内容宽度（A4宽度 - 左右边距）
- 列宽用最后一列吸收余量，确保精确等于内容宽度
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

## 图片规范

- 行间距：单倍行距
- 对齐：居中
- 样式名称：`图片样式`

## 文档属性

- 文档作者需为空（`dc:creator` 与 `lastModifiedBy` 均为空串）
- `createDocument` 内部已把 `creator` 与 `lastModifiedBy` 同时设为传入的 `author`（默认空串）。**不要**只设置 `creator`：`docx` 库在未显式指定 `lastModifiedBy` 时会写入 `Un-named`，导致文档属性中出现非预期作者。

## 完整示例

```javascript
const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Footer, BorderStyle, WidthType, ShadingType, VerticalAlign,
  PageNumber, ImageRun, AlignmentType, HeadingLevel, LevelFormat,
  createTitleParagraph, createBodyParagraph, createLevel1Heading,
  createLevel2Heading, createLevel3Heading, createTable,
  createImageParagraph, createDocument, CHINESE_FONTS, FONT_SIZES,
  CONTENT_WIDTH, PAGE_MARGINS, LINE_SPACING_EXACT_28
} = require('/Users/<用户名>/.workbuddy/skills/gov-doc-writing/scripts/create_gov_doc.js');

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
6. **文档作者**：`createDocument` 的 `author` 留空即可，勿单独设置 `creator`

## 生成策略与交付前校验

**推荐做法：把正文内容全部组织成 `sections` 数组，用 node 脚本一次性生成完整文档。**
长文档（数十页以上）迭代时也应按"改脚本 → 整篇重建"的方式更新，而不是在已生成的 docx 上做增量插入。原因见下。

**不要在长文档上用编辑器类工具（`doc_insert_paragraph*` 等）批量写入正文**：实测出现过把连续多个段落合并为一个巨型段落（单段长度约 1500 字符、内含十余个 `&#13;` 软回车并整段重复）的情况，而文档大纲接口仍显示结构正常——即内存态与落盘 XML 不一致，检查手段会被误导。若必须用编辑器路径，写入后务必按下面的方法直接校验 XML。

**交付前必须校验**（建议用 python `zipfile` 读取 `word/document.xml` 后统计；`doc_to_image` 转图校验依赖云端凭证接口，可能返回"服务繁忙"，不能作为唯一手段）：

```python
import zipfile, re
xml = zipfile.ZipFile(path).read('word/document.xml').decode('utf-8')
paras = re.findall(r'<w:p\b.*?</w:p>', xml, re.S)          # 段落切分
texts = [''.join(re.findall(r'<w:t(?:\s[^>]*)?>(.*?)</w:t>', p, re.S)) for p in paras]
assert sum(t.count('\x13') + t.count('&#13;') for t in texts) == 0   # 不应有软回车
print(len(paras), sum(len(t) for t in texts))                        # 段落数 / 总字符数
```

校验要点：①段落数、字符数与预期一致；②不存在含软回车的异常段落；③关键词计数符合修改预期（如某厂商名应为 0）；④`word/core.xml` 中 `dc:creator`、`lastModifiedBy` 为空。

## 相关文件

- `scripts/create_gov_doc.js` - 核心创建函数库
