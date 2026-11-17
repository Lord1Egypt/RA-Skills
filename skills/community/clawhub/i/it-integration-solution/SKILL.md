---
name: it-integration-solution
zh_name: 信息化解决方案
description: |
  信息化解决方案 — 用于生成 IT 集成公司面向企业客户的 Word（.docx）格式解决方案文档。当用户要求编写、生成或创建「信息化解决方案」「IT集成解决方案」「IT解决方案」「技术方案」「系统集成方案」「项目实施方桇」「投标技术方案」等面向企业客户的专业文档时使用。覆盖封面、目录、项目概述、需求分析、技术方案设计、系统架构、实施方案、项目管理、培训方案、售后服务、验收方案完整章节。基于国央企Word文档规范，适配企业级方案的专业排版需求。
  This skill should be used when the user wants to create IT integration solution proposals for enterprise clients in .docx format.
agent_created: true
---

# 信息化解决方案

本技能用于创建 IT 集成公司面向企业客户的 Word（.docx）格式解决方案文档，基于国央企文档规范，适配企业级方案的专业排版需求。

## 文档结构

标准 IT 集成解决方案包含以下章节模块（按实际需求选择和排列）：

| 序号 | 章节 | 说明 | 必须 |
|------|------|------|------|
| 1 | 封面 | 项目名称、公司名称、日期、版本号 | 是 |
| 2 | 目录 | 自动生成的章节目录 | 是 |
| 3 | 项目概述 | 项目背景、建设目标、建设范围 | 是 |
| 4 | 需求分析 | 现状分析、痛点梳理、需求总结 | 是 |
| 5 | 技术方案设计 | 总体设计思路、关键技术选型 | 是 |
| 6 | 系统架构 | 网络拓扑、部署架构、安全架构 | 推荐 |
| 7 | 实施方案 | 实施阶段、进度计划、团队配置 | 是 |
| 8 | 项目管理 | 管理方法论、质量保证、风险管理 | 推荐 |
| 9 | 培训方案 | 培训对象、内容、方式、计划 | 推荐 |
| 10 | 售后服务与技术支持 | 服务级别、响应时间、维保内容 | 是 |
| 11 | 验收方案 | 验收标准、验收流程、交付物清单 | 是 |

## 页面设置

| 属性 | 值 |
|------|-----|
| 纸张 | A4（210mm × 297mm） |
| 上边距 | 3.7 厘米（封面）/ 2.54 厘米（正文） |
| 下边距 | 3.5 厘米（封面）/ 2.54 厘米（正文） |
| 左边距 | 2.8 厘米（封面）/ 3.17 厘米（正文） |
| 右边距 | 2.6 厘米（封面）/ 3.17 厘米（正文） |
| 页码 | 正文页居中显示"第N页 / 共N页"（SECTIONPAGES 域），宋体五号，封面和目录不编页码，正文起编第1页 |

## 字体规范

### 封面字体

| 元素 | 中文字体 | 西文字体 | 字号 | 对齐 |
|------|----------|----------|------|------|
| 公司名称 | 方正小标宋简体 | Times New Roman | 小一号（24pt） | 居中 |
| 项目名称 | 方正小标宋简体 | Times New Roman | 小初号（36pt） | 居中 |
| 公司信息 | 方正仿宋简体 | Times New Roman | 小三号（15pt） | 居中 |
| 日期版本 | 方正仿宋简体 | Times New Roman | 小三号（15pt） | 居中 |

### 正文字体

| 样式 | 中文字体 | 西文字体 | 字号 |
|------|----------|----------|------|
| 正文 | 方正仿宋简体 | Times New Roman | 小三号（15pt） |
| 一级标题（章标题） | 黑体 | Times New Roman | 小三号（15pt） |
| 二级标题（节标题） | 楷体 | Times New Roman | 小三号（15pt） |
| 三级标题（条标题） | 方正仿宋简体 | Times New Roman | 小三号（15pt）加粗 |
| 四级标题 | 方正仿宋简体 | Times New Roman | 小三号（15pt） |
| 表格内容 | 方正仿宋简体 | Times New Roman | 小五号（9pt） |
| 表格表头 | 黑体 | Times New Roman | 小五号（9pt）加粗 |
| 页码 | 宋体 | - | 五号（10.5pt） |
| 题注 | 宋体 | Times New Roman | 五号（10.5pt） |
| 封面公司名称 | 方正小标宋简体 | Times New Roman | 小一号（24pt） |
| 封面项目名称 | 方正小标宋简体 | Times New Roman | 小初号（36pt） |
| 封面文档类型 | 黑体 | Times New Roman | 小二号（18pt） |
| 封面信息 | 方正仿宋简体 | Times New Roman | 小三号（15pt） |

## 行间距

| 样式 | 行间距 |
|------|--------|
| 封面元素 | 固定 36 磅 |
| 正文 | 固定 28 磅 |
| 一级标题 | 固定 28 磅 |
| 二级标题 | 固定 28 磅 |
| 三级标题 | 固定 28 磅 |
| 四级标题 | 固定 28 磅 |
| 题注 | 单倍行距 |
| 图片 | 单倍行距 |
| 表格 | 单倍行距 |

## 章节编号规范

| 级别 | 编号格式 | 示例 | 首行缩进 | 大纲级别 |
|------|----------|------|----------|----------|
| 一级标题（章） | 第一章、第二章... | 第一章 项目概述 | 2 字符 | 1 级 |
| 二级标题（节） | 1.1、1.2... | 1.1 项目背景 | 2 字符 | 2 级 |
| 三级标题（条） | 1.1.1、1.1.2... | 1.1.1 建设背景 | 2 字符 | 3 级 |
| 四级标题 | （1）（2）... | （1）网络现状 | 2 字符 | 4 级 |

## 样式名称定义

创建文档时必须使用以下样式名称：

- `封面公司名称` — 封面页公司全称
- `封面项目名称` — 封面页项目名称
- `封面文档类型` — 封面页文档类型（如"技术解决方案"）
- `封面信息` — 封面页公司信息 / 日期
- `正文` — 正文段落（方正仿宋、小三号、首行缩进2字符、固定28磅）
- `一级标题` — 章节标题（黑体、小三号、大纲1级）
- `二级标题` — 节标题（楷体、小三号、大纲2级）
- `三级标题` — 条标题（方正仿宋加粗、小三号、大纲3级）
- `四级标题` — 款标题（方正仿宋、小三号、大纲4级）
- `图片` — 图片段落（居中、单倍行距）
- `表格正文` — 表格内容（方正仿宋、小五号）
- `表格表头` — 表头内容（黑体、小五号、加粗）
- `题注` — 表格/图片题注（宋体、五号、居中）
- `落款` — 落款信息（方正仿宋、小三号、右对齐；传入 `signature` 选项自动生成，或手动调用 `createSignatureBlock`）

## 封面规范

封面为独立一页，不显示页码。包含以下元素（从上到下居中排列）：

```
[公司 LOGO]（如有，居中放置）

[公司全称]（方正小标宋简体、小一号）
[项目名称]（方正小标宋简体、小初号）

（中间以空行填充，将底部信息推至页面底部）

[编制单位]：XXX 公司
[编制日期]：2026年X月
[文档版本]：V1.0
```

使用 `createCoverPage()` 函数一键生成封面。

## 目录规范

- 目录位于封面之后，独立一页（通过分节符 `SectionType.NEXT_PAGE` 实现）
- 目录页预置"目  录"标题（"目录标题"样式），用户在 Word 中使用「引用 → 目录 → 自动目录」手动插入
- 文档已预定义 TOC1 / TOC2 / TOC3 样式，自动目录会使用这些预定义格式而非 Word 默认模板：
  - TOC1（章标题）：黑体小三号、固定28磅、首行不缩进、右对齐点引导符 + 页码
  - TOC2（节标题）：方正仿宋小三号、固定28磅、2字符缩进、右对齐点引导符 + 页码
  - TOC3（子节标题）：方正仿宋小三号、固定28磅、2字符缩进、右对齐点引导符 + 页码
- 目录页不编页码
- 使用 `createTableOfContents()` 函数生成

## 表格规范

- 表格上方不添加空行，直接紧跟前文内容
- 表格宽度自动适应窗口（百分比 100%）
- 列宽比例通过 `columnWidths` 参数控制（DXA 相对值）
- 表头：灰色底（#D9D9D9）、黑体加粗、居中
- 内容：白色底、方正仿宋、居中、小五号（9pt）
- 边框：单线黑色
- 表格下方可添加题注（如"表1 XXX"），序号全文档独立递增，使用"题注"样式（宋体五号居中）
- 使用 `createSolutionTable()` 函数创建

## 图片规范

- 行间距：单倍行距
- 对齐：居中
- 支持在图片下方添加图注（如"图1 XXX"），序号全文档独立递增
- 图注使用"题注"样式（宋体五号、居中）

## 落款规范

- 落款默认由技能自动生成：在 `createSolutionDocument` / `createItSolution` 中传入 `signature: { company, date }` 即可，落款会自动追加到正文末尾（与上方正文间隔两行）。也可手动调用 `createSignatureBlock(company, date)`。
- 落款（公司名称 + 日期）放置文档最后，与上方正文间隔两行
- 右对齐，无首行缩进
- 使用方正仿宋小三号

## 文档属性

- 设置文档标题为项目名称
- 删除文档作者信息（`dc:creator` 和 `lastModifiedBy` 留空）
- 设置文档分类为"技术方案"

## 使用方法

### 方式一：使用 JavaScript API 创建文档

```javascript
const {
  createSolutionDocument,
  createCoverPage,
  createTableOfContents,
  createChapterHeading,
  createSectionHeading,
  createSubsectionHeading,
  createBodyParagraph,
  createSolutionTable,
  createSignatureBlock,
  createImageWithCaption,
  createBulletList,
  Packer,
  CHINESE_FONTS,
  FONT_SIZES,
} = require('~/.workbuddy/skills/it-integration-solution/scripts/create_it_solution.js');

// 构建文档内容
const sections = [
  // 封面
  ...createCoverPage({
    companyName: 'XX科技有限公司',
    projectName: 'XX企业数字化转型IT基础设施集成项目',
    date: '2026年7月',
    version: 'V1.0',
  }),

  // 目录（自动生成，不可选章节参数）
  createTableOfContents(),

  // 第一章 项目概述
  createChapterHeading('项目概述', 0),
  
  createSectionHeading('项目背景', 0, 0),
  createBodyParagraph('随着企业业务的快速发展，现有IT基础设施已无法满足...'),

  createSectionHeading('建设目标', 0, 1),
  createBodyParagraph('本项目旨在构建一套高可用、可扩展的企业IT基础架构...'),

  createSectionHeading('建设范围', 0, 2),
  createBodyParagraph('本次项目建设范围涵盖以下内容：'),
  createBulletList([
    '数据中心网络升级改造',
    '服务器虚拟化平台建设',
    '存储系统扩容与灾备建设',
    '网络安全防护体系建设',
  ]),

  // 第二章 需求分析
  createChapterHeading('需求分析', 1),

  createSectionHeading('现状分析', 1, 0),
  // 使用表格展示现状
  createSolutionTable(
    [
      { children: ['系统名称', '当前配置', '存在问题', '改造需求'] },
      { children: ['核心网络', '千兆交换机', '带宽不足', '万兆升级'] },
      { children: ['服务器', 'Xeon E5 v3', '性能瓶颈', 'Xeon Scalable'] },
    ],
    { columnWidths: [1500, 2000, 2500, 2500] }
  ),

  // ... 后续章节 ...
];

// 创建文档
const doc = createSolutionDocument({
  title: 'XX企业数字化转型IT基础设施集成项目',
  sections,
  hasCover: true,
  hasTOC: true,
});

// 生成文件
Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync('解决方案.docx', buffer);
  console.log('文档已生成: 解决方案.docx');
});
```

### 方式二：使用便捷函数 createItSolution

```javascript
const { createItSolution } = require('.../scripts/create_it_solution.js');

const content = {
  cover: {
    companyName: 'XX科技有限公司',
    projectName: 'XX企业数字化转型IT基础设施集成项目',
    date: '2026年7月',
    version: 'V1.0',
  },
  chapters: [
    {
      heading: '项目概述',
      sections: [
        { heading: '项目背景', body: ['背景段落1', '背景段落2'] },
        { heading: '建设目标', body: ['目标段落'] },
        { heading: '建设范围', body: ['范围描述'], bulletList: ['范围1', '范围2'] },
      ]
    },
    {
      heading: '需求分析',
      sections: [
        { heading: '现状分析', body: ['...'], tables: [...] },
        { heading: '需求总结', body: ['...'] },
      ]
    },
    // ... 更多章节
  ],
  signature: { company: 'XX科技有限公司', date: '2026年7月' },
};

createItSolution(content, '解决方案.docx');
```

## 注意事项

1. **字号转换**：Word中的"号"转换为半磅值（小初号=72半磅=36pt，小一号=48半磅=24pt，小三号=30半磅=15pt，小五号=18半磅=9pt）
2. **行间距固定28磅**：line值设置为560（28 × 20），lineRule设置为"exact"
3. **首行缩进**：使用 `indent: { firstLine: charWidth * 2 }`，字符宽度约等于字号的一半
4. **封面和目录不编页码**：通过分节符 `SectionType.NEXT_PAGE` 分隔，正文 section 才有页脚，封面和目录 section 无页脚
5. **页码格式**：正文页脚显示"第N页 / 共N页"，使用 `PageNumber.CURRENT` 和 `PageNumber.TOTAL_PAGES`
6. **文档作者**：不设置或留空
7. **双引号自动规范化**：ASCII 双引号 `"` 自动替换为中文双引号 `""`
8. **中西文字体分段**：每个 TextRun 明确写入字体，确保 Word 渲染稳定
9. **docDefaults 字体**：必须使用对象格式 `{ eastAsia, ascii, hAnsi, cs }`，不能传字符串
10. **pPrDefault 行距**：`pPrDefault` 必须设置 `spacing: { before: 0, after: 0, line: 560, lineRule: "exact" }`
11. **目录不使用 Word 域**：采用纯文本手动目录，避免打开文档时提示"域引用了其他文件"
12. **目录 / 正文分页**：通过 `SectionType.NEXT_PAGE` 分节符实现，不在目录末尾添加 `PageBreak`
13. **表格上方不空行**：表格直接紧跟前文内容，不添加空白段落
14. **题注**：表格和图片题注使用独立的"题注"样式（宋体五号居中），不使用正文样式

## 相关文件

- `scripts/create_it_solution.js` — 核心创建函数库
