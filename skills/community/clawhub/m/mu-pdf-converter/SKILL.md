---
name: mu-pdf-converter
description: "PDF格式转换与处理工具。触发词：PDF转PPT、PDF转Word、PDF转Excel、PDF转图片、PDF格式转换、把PDF转成PPT、PDF去水印、移除水印、PDF表单填写、填写PDF表格、批量提取PDF表格、外文PDF翻译。即使用户没说'转换'，只要提到'PDF里的表提取到Excel''这个报告能不能编辑''去掉这个水印''把这个英文PDF翻成中文'也应触发。不适用：非PDF输入、PDF内容分析/摘要（用pdf skill）、扫描件OCR识别。"
version: 1.7
tags: PDF,格式转换,PDF转PPT,PDF转Word,PDF转Excel,PDF转图片,去水印,表单填写,批量处理,办公自动化,python,文档处理,翻译
visibility: public
---


**IRON LAW：①转换前必须确认源文件为有效PDF（非扫描件），不支持的格式必须明确拒绝并告知替代方案；②转换后必须验证输出文件可正常打开且内容完整，不可直接交付未验证的产物；③pdf_to_xlsx.py使用三引擎优先级（E1 XY-Cut→E2 MarkItDown→E3 pdfplumber），表格提取失败时必须降级而非报错退出；④批量模式单次处理不超过100个PDF文件、翻译不超过5000个文本块。无例外。**

# mu-pdf-converter — PDF 格式转换工具

## 概述

将 PDF 文件高保真转换为多种可编辑格式。核心能力：

| 目标格式 | 特点 |
|---------|------|
| **PPT** (.pptx) | 文本框可编辑 + SVG矢量图 + 位图原格式 + 表格原生可编辑（四层叠加）；外文PDF自动生成中文版 |
| **Word** (.docx) | 文本段落 + 标题识别 + 表格插入，保留字体/加粗/斜体 |
| **Excel** (.xlsx) | 仅提取表格内容，每个表格一个 Sheet；支持批量目录扫描 |
| **图片** (.png/.jpg) | 每页高质量渲染，支持自定义 DPI |

> **不适用场景**：非 PDF 输入、PDF 内容分析/摘要（请用 `pdf` skill）、扫描件的 OCR 识别（需外部 OCR 工具预处理）。

---

## 安装依赖

```bash
# 核心依赖（必装）
pip install pymupdf pdfplumber python-pptx python-docx openpyxl lxml pypdf

# 可选依赖（增强功能）
pip install pypdfium2 markitdown translators requests
```

依赖说明：
- `pymupdf`（`fitz`）：PDF 解析、文本/图片/矢量路径提取、页面渲染
- `pdfplumber`：表格识别（基于 pdfminer.six）
- `python-pptx` + `lxml`：生成 PowerPoint 文件（SVG插入需lxml）
- `python-docx`：生成 Word 文件
- `openpyxl`：生成 Excel 文件
- `pypdf`：PDF 表单填写、水印移除的 XObject 操作
- `pypdfium2`（可选）：XY-Cut 无边框表格识别引擎 E1
- `markitdown`（可选）：AI辅助表格识别引擎 E2
- `translators` + `requests`（可选）：外文PDF自动翻译

---

## 快速开始

```bash
SKILL_DIR=~/.openclaw/skills/mu-pdf-converter/scripts

# 1. PDF → PPT（默认跟PDF页面尺寸一致，外文自动翻译）
python3 $SKILL_DIR/pdf_to_pptx.py report.pdf --outfile report.pptx
python3 $SKILL_DIR/pdf_to_pptx.py report.pdf --slide-size 16:9          # 指定尺寸
python3 $SKILL_DIR/pdf_to_pptx.py report.pdf --no-translate             # 禁用翻译

# 2. PDF → Word
python3 $SKILL_DIR/pdf_to_docx.py report.pdf --outfile report.docx

# 3. PDF → Excel（仅表格）
python3 $SKILL_DIR/pdf_to_xlsx.py report.pdf --outfile tables.xlsx

# 4. PDF → Excel（批量，扫描目录内所有 PDF）
python3 $SKILL_DIR/pdf_to_xlsx.py --batch ./invoices/ --outfile batch_result.xlsx

# 5. PDF → 图片（每页一张 PNG，150 DPI）
python3 $SKILL_DIR/pdf_to_images.py report.pdf --dpi 150 --outdir ./images

# 6. PDF 表单填写（可填字段）
python3 $SKILL_DIR/pdf_fill_form.py form.pdf --detect                           # 检测字段
python3 $SKILL_DIR/pdf_fill_form.py form.pdf --fill-json values.json --outfile filled.pdf  # 填写

# 7. PDF 表单填写（非可填字段，坐标注释）
python3 $SKILL_DIR/pdf_fill_form.py form.pdf --analyze --outdir ./form_images   # 转图分析
python3 $SKILL_DIR/pdf_fill_form.py form.pdf --annotate-json ann.json --outfile filled.pdf # 注释填写

# 8. PDF 去水印（通用版）
python3 $SKILL_DIR/pdf_remove_watermark.py watermarked.pdf --outfile clean.pdf
python3 $SKILL_DIR/pdf_remove_watermark.py watermarked.pdf --detect-only          # 预览模式（不修改）
python3 $SKILL_DIR/pdf_remove_watermark.py watermarked.pdf --method text --outfile clean.pdf  # 仅文字水印
python3 $SKILL_DIR/pdf_remove_watermark.py watermarked.pdf --aggressive --outfile clean.pdf   # 激进模式
```

---

> 📖 各格式详细参数、技术细节、降级策略、已知限制见 [references/usage-guide.md](references/usage-guide.md)

## 脚本路径

```
~/.openclaw/skills/mu-pdf-converter/
├── SKILL.md          # 本文件
├── _meta.json        # 元数据（.skillignore 排除，不随发布）
└── scripts/
    ├── utils.py                 # 公共工具（坐标转换/字体映射/XY-Cut v2/扫描件检测）
    ├── translate_utils.py       # 翻译工具（语言检测/批量翻译/专有名词保护）
    ├── mcp_server.py            # MCP Server（JSON-RPC stdin/stdout，零依赖）
    ├── pdf_to_pptx.py           # PDF → PPT（核心，四层叠加+自动翻译）
    ├── pdf_to_docx.py           # PDF → Word
    ├── pdf_to_xlsx.py           # PDF → Excel（三引擎；支持 --batch 批量模式）
    ├── pdf_to_images.py         # PDF → 图片
    ├── pdf_fill_form.py         # PDF 表单填写（双路径：可填字段 / 坐标注释）
    └── pdf_remove_watermark.py  # PDF 去水印（通用版，4 种策略）
```


## Claude 使用指南

当用户请求 PDF 转换时，按以下流程执行：

```bash
SKILL_DIR="~/.openclaw/skills/mu-pdf-converter/scripts"

# 1. 确认输入文件存在
# 2. 根据目标格式选择脚本
# 3. 运行对应脚本
# 4. 验证输出文件存在且大小合理
# 5. 返回输出文件路径给用户

# 示例（PDF转PPT）：
python3 $SKILL_DIR/pdf_to_pptx.py 'input.pdf' --outfile 'output.pptx'

# 示例（PDF转PPT，禁用翻译）：
python3 $SKILL_DIR/pdf_to_pptx.py 'input.pdf' --outfile 'output.pptx' --no-translate
```

**pdf_to_pptx.py 额外参数**：
- `--slide-size pdf|16:9|4:3|A4|A4v`：幻灯片尺寸（默认pdf=跟原文件一致）
- `--no-translate`：禁用外文自动翻译
- `--verbose-translate`：打印逐条翻译日志

**处理扫描件时**：提示用户可先用 OCR 工具（如 `ocrmypdf`）添加文本层：
```bash
pip install ocrmypdf
ocrmypdf input_scan.pdf input_ocr.pdf
python3 $SKILL_DIR/pdf_to_pptx.py input_ocr.pdf
```

---

## MCP Server（可选）

本 Skill 提供 MCP（Model Context Protocol）Server，可被 Claude 等 AI 助手直接调用：

```bash
# 启动 MCP Server
python3 ~/.openclaw/skills/mu-pdf-converter/scripts/mcp_server.py
```

协议：JSON-RPC 2.0 over stdin/stdout，零外部依赖。暴露 6 个工具：`pdf_to_pptx`、`pdf_to_docx`、`pdf_to_xlsx`、`pdf_to_images`、`pdf_fill_form`、`pdf_remove_watermark`。

---

## references/ 索引

| 文件 | 说明 |
|------|------|
| [references/usage-guide.md](references/usage-guide.md) | 各格式详细参数、PPT技术细节、降级策略、已知限制、表单填写/批量模式完整说明 |
