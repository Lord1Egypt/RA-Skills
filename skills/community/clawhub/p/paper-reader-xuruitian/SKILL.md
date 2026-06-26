---
name: paper-reader
description: >
  精读学术文献的专家级 Skill。当用户上传 PDF、Word、Excel、PPT 或 TXT
  格式的学术论文，并希望进行深度学术分析时使用本 Skill。支持中英双语文献，
  可自动识别文件类型、提取全文内容，并按六大维度（研究目标、新方法、实验验证、
  未来方向、批判分析、实用建议）输出结构化分析报告。触发词包括：
  精读、论文分析、文献解读、读论文、paper analysis、academic reading、
  帮我看看这篇论文、论文讲了什么。
---

# Paper Reader Skill

**学术论文精读专家** — 深度解读学术论文，输出结构化分析报告，并自动生成 Word 文档保存在桌面。

---

## 什么时候使用本 Skill

当用户上传学术论文（PDF、Word、Excel、PPT、TXT 等格式）并希望：
- 深入理解论文的研究目标、方法和贡献
- 获取论文的批判性分析
- 了解该方向的前沿进展和学习建议
- 将论文转化为可用的创新想法

**典型触发句式**：
- "精读这篇论文"
- "帮我分析这篇文献"
- "这篇论文讲了什么"
- "论文解读"
- "学术论文分析"

---

## 执行流程

### 第一步：识别文件并提取内容

根据用户上传的文件扩展名，使用 `scripts/extract_text.py` 提取全文：

```bash
python <skill_path>/scripts/extract_text.py <file_path> [-o <输出文件路径>]
```

**支持的格式一览**：

| 格式 | 扩展名 | 主要工具 |
|------|--------|---------|
| PDF | `.pdf` | PyMuPDF (fitz) + pdfplumber |
| Word | `.docx` | python-docx |
| Word | `.doc` | textutil (macOS) / antiword (Windows) |
| Excel | `.xlsx` | openpyxl |
| Excel | `.xls` | xlrd + pandas |
| PPT | `.pptx` | python-pptx |
| 文本 | `.txt` / `.md` / `.csv` | Python 内置编码自动检测（UTF-8/GBK/GB2312） |

> **注意**：Word `.doc` 格式在 macOS 上使用 textutil，Windows 上需要预装 `antiword`；如不可用请提示用户将文件另存为 `.docx` 格式。

### 第二步：判断学科领域与背景

根据论文的摘要、关键词和章节标题，判断：
- 论文所属学科领域（机器学习、供应链管理、金融、医学等）
- 是否涉及多学科交叉
- 是否需要补充领域最新研究动态

### 第三步：加载分析参考模板

读取 `references/academic_prompt.md` 获取完整的六维度分析框架，在分析过程中**严格遵循**该模板的格式要求。

### 第四步：执行深度分析（六大维度）

按以下顺序逐一分析，**直接引用原文细节**：

1. **研究目标与实际问题** — 研究目的、解决的问题、产业意义
2. **新思路、方法与模型** — 创新点、相比已有方法的优势（引用原文细节）
3. **实验设计与验证** — 实验设计、数据、结果（引用关键数据）
4. **未来研究方向与机会** — 值得探索的问题、新技术/投资机会
5. **批判性分析** — 不足、缺失、需进一步验证的内容
6. **实用价值与学习建议** — 可借鉴的创新想法、学习重点、需补充的背景知识

### 第五步：输出 Markdown 报告

以 **Markdown 格式**输出，**严格遵循**以下格式规范：

- 使用 `### 三级标题` 对应六大问题
- 引用原文使用 `>` blockquote
- 关键术语**首次出现时加粗**
- 中文书写，学术名词附英文
- 适当使用列表、加粗、表格
- 适当插入图表说明（可用文字描述关键图表内容）

### 第六步：生成 Word 文档并保存至桌面 ⭐

将分析报告自动转换为 Word 文档（.docx），保存到用户桌面：

**推荐方式：JSON 数据文件模式**

1. 先将分析内容写入 JSON 文件（保存到 `<skill_path>/data/latest_analysis.json`）：
```json
{
  "title": "论文主标题",
  "subtitle": "副标题（如：—— 精读报告）",
  "author": "作者名",
  "school": "学校/机构",
  "date": "2026年x月x日",
  "overview": "整体概述段落内容...",
  "dimensions": [
    { "heading": "维度一：研究目标与实际问题", "content": "多行内容..." },
    { "heading": "维度二：新思路、方法与模型", "content": "多行内容..." },
    { "heading": "维度三：实验设计与验证", "content": "多行内容..." },
    { "heading": "维度四：未来研究方向与挑战", "content": "多行内容..." },
    { "heading": "维度五：批判性分析", "content": "多行内容..." },
    { "heading": "维度六：实用价值与学习建议", "content": "多行内容..." }
  ],
  "summary": "总结段落",
  "filename": "论文简称_精读报告"
}
```

2. 运行生成脚本：
```bash
node <skill_path>/scripts/generate_report.js --data <skill_path>/data/latest_analysis.json
```

**命令行参数模式（备选）**：
```bash
node <skill_path>/scripts/generate_report.js \
  --title "<论文标题>" \
  --output "<输出完整路径>"
```

**生成后告知用户**：
> ✅ Word 文档已生成并保存至桌面：`<filepath>`

---

## 文件结构

```
paper-reader/
├── SKILL.md                          ← Skill 主入口（本文件）
├── scripts/
│   ├── extract_text.py               ← 文档文本提取脚本（支持7种格式）
│   └── generate_report.js            ← Word 报告生成脚本
├── references/
│   └── academic_prompt.md            ← 六维度分析 Prompt 模板
└── data/
    └── .gitkeep                       ← 保持目录结构，忽略临时数据
```

---

## 注意事项

1. **引用原文**：分析时大量引用论文原文中的关键句子、数据和图表说明，体现分析的深度和依据
2. **通俗解释**：对于新颖或专业的术语，在引用后给出通俗易懂的解释
3. **批判视角**：不回避论文的不足，以建设性批评帮助用户全面理解论文
4. **实用建议**：重点帮助用户提炼"拿来即用"的创新想法，而非泛泛而谈
5. **格式严格遵循**：按 academic_prompt.md 中的格式规范输出，不遗漏任何部分
6. **Word 输出**：分析完成后必须执行第六步，将报告保存为 Word 文档到桌面，文件名格式为：`<论文简称>_精读报告.docx`
