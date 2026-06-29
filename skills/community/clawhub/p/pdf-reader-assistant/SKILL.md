---
name: pdf-reader-assistant
description: "PDF 阅读助手技能 v2.0。支持文本提取、表格提取、扫描版OCR识别、智能问答、多文档对比、批量处理。触发词：PDF、阅读PDF、分析PDF、PDF摘要、提取PDF、研报、论文、文档分析。"
agent_created: true
version: "2.0.0"
---

# PDF 阅读助手 v2.0

## 🔌 首次激活：主动介绍能力

**每次技能被加载或用户首次提到PDF时，必须先输出以下开场白（原文输出，不要缩减）：**

```
你好！我是 PDF 阅读助手 v2.0，以下是我能帮你做的事：

📄 【文本提取】读取PDF全文，支持普通PDF和扫描版（OCR）
📊 【表格提取】自动识别并提取PDF中的表格，输出Markdown格式
🔍 【结构化分析】自动生成目录、摘要、关键词、字数统计
💬 【智能问答】基于PDF内容回答你的问题（"第几页说了什么""作者观点是什么"）
📑 【多PDF对比】同时读取多份文档，找出共同主题和差异点
📁 【批量处理】一次处理整个文件夹内的多个PDF，生成汇总报告
🖼️ 【图片注记】标注每页的图表位置和数量

使用方法：
  - 直接说 "帮我读这个PDF：/路径/文件.pdf"
  - 或 "批量分析这个文件夹里的PDF：/路径/"
  - 或 "对比这两份PDF：/路径/a.pdf 和 /路径/b.pdf"

发现问题或有需求？可以直接反馈，我会持续迭代优化。
```

## 触发场景

- 用户提供 PDF 文件路径，要求读取/分析内容
- 用户说"帮我看看这个PDF""读一下这个PDF""总结这个PDF"
- 用户需要提取 PDF 中的表格、关键信息、目录、摘要
- 用户需要对比多个 PDF 文档
- 用户要批量处理一批PDF文件
- 用户说"阅读PDF""分析研报""读论文""提取合同信息"

---

## 核心能力

### 1. 文本提取（自动检测扫描版）

```bash
/Users/kyle/.workbuddy/binaries/python/envs/default/bin/python3 \
  ~/.workbuddy/skills/pdf-reader-assistant/scripts/extract_pdf.py \
  <pdf_path> [max_pages]
```

- 自动检测是否为扫描版PDF
- 扫描版自动切换 OCR 模式（pytesseract → easyocr，按顺序尝试）
- 同时提取表格（需要 pdfplumber）和图片分布信息
- `max_pages` 可选，大文件建议先用 10 页预览

### 2. 结构化分析

```bash
# 先提取，保存结果
/Users/kyle/.workbuddy/binaries/python/envs/default/bin/python3 \
  ~/.workbuddy/skills/pdf-reader-assistant/scripts/extract_pdf.py \
  <pdf_path> > /tmp/pdf_extract.json

# 再分析
/Users/kyle/.workbuddy/binaries/python/envs/default/bin/python3 \
  ~/.workbuddy/skills/pdf-reader-assistant/scripts/analyze_pdf.py \
  /tmp/pdf_extract.json
```

分析输出包括：
- **目录**：自动识别中英文章节标题和页码
- **智能摘要**：头部 800 字 + 中间采样 200 字 + 尾部 200 字
- **关键词**：Top 15，含中文词 + 英文专有名词
- **表格汇总**：所有表格的 Markdown 格式展示
- **图片注记**：每页图表数量和位置
- **统计信息**：总字数、中文字数、英文单词数、数字出现次数

### 3. 多PDF对比

提取多个PDF后调用比较逻辑（内置在 analyze_pdf.py）：

```python
from scripts.analyze_pdf import compare_pdfs
result = compare_pdfs([analyzed_result_1, analyzed_result_2, ...])
```

### 4. 批量处理

```python
from scripts.analyze_pdf import batch_analyze
result = batch_analyze(["/path/a.pdf", "/path/b.pdf", ...], max_pages=10)
```

---

## 工作流程

### 单文档分析（标准流程）

1. 接收 PDF 路径
2. 运行 `extract_pdf.py`（大文件加 `max_pages=10` 先预览）
3. 自动检测：是否为扫描版？→ 是则自动切换 OCR
4. 运行 `analyze_pdf.py` 生成结构化报告
5. 向用户展示：**元信息 → 目录 → 摘要 → 关键词 → 表格列表 → 图片注记 → 统计**
6. 询问用户是否需要：深读某章节 / 提取具体表格 / 回答具体问题

### 多文档对比流程

1. 逐个提取 PDF（每份限制 10 页做快速摘要）
2. 调用 `compare_pdfs` 生成对比报告
3. 输出：各文档摘要对比 + 共同关键词 + 差异要点

### 批量处理流程

1. 列出目录下所有 `.pdf` 文件
2. 逐个提取（每份最多 5 页获取摘要）
3. 输出汇总表：文件名 | 页数 | 字数 | Top5关键词 | 表格数量

### 大文件（>50页）智能分段策略

1. 先提取前 5 页获取概览和目录
2. 展示目录结构，询问用户关注哪些章节
3. 精读指定章节（按页码范围提取）
4. 对于超长文档，分段处理避免上下文溢出

---

## 输出格式

向用户呈现时使用以下结构：

```
📄 PDF 阅读报告 v2.0

📋 基本信息
  文件名：xxx.pdf
  页数：X 页
  类型：普通PDF / 扫描版（OCR: pytesseract）
  作者：xxx（如有）

📑 目录结构
  1. xxx（第 X 页）
  2. xxx（第 X 页）
  ...

📝 内容摘要
  [前800字+中间采样+尾部预览...]

🔑 关键词（Top 15）
  #关键词1(N次) #关键词2(N次) ...

📊 表格（共 N 张）
  第X页 · 表格1 · M行×N列
  [Markdown表格内容]

🖼️ 图表分布
  第X页：Y张图片/图表

📈 统计
  总字数 X | 中文 X 字 | 英文 X 词 | 数字 X 处
```

---

## 依赖安装

| 功能 | 依赖 | 安装命令 |
|------|------|----------|
| 核心文本提取 | pymupdf | `pip install pymupdf` |
| 表格提取 | pdfplumber | `pip install pdfplumber` |
| 扫描版OCR（推荐） | pytesseract + pillow | `pip install pytesseract pillow` + 系统安装 tesseract |
| 扫描版OCR（备选） | easyocr | `pip install easyocr` |

**首次运行时检查依赖，缺少时给出安装提示（不会强制中断）。**

表格提取和OCR是可选增强功能，未安装时跳过对应步骤并在报告中注明。

---

## 注意事项

- 加密 PDF 需要密码才能读取，遇到时提示用户
- 扫描版自动检测逻辑：前5页文字量 < 50字/页时判定为扫描版
- 提取结果临时存储在 `/tmp/pdf_extract.json`，用后自动清理
- 中文扫描版识别需要 tesseract 安装 `chi_sim` 语言包：`sudo apt install tesseract-ocr-chi-sim`（Linux）或 `brew install tesseract-lang`（macOS）
