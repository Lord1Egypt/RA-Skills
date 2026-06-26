---
name: paper-to-table
description: Extract structured data from academic papers (PDF/DOCX/TXT) into literature review tables (XLSX/CSV). Use when user says "整理文献到表格", "extract papers to table", "literature review table", or provides papers with a table template. Supports batch folder processing, dynamic header mapping, duplicate detection, and format preservation. Domains: Psychology, Cognitive Neuroscience, Computer Science, Brain Science. Handles English and Chinese papers.
---

# Paper To Table

Extract structured information from academic papers and populate literature review tables.

## Quality Principles

### 1. Extraction Fidelity (质量约束)
- **NEVER hallucinate** information not present in the paper
- **NEVER infer** beyond what is explicitly stated
- **Use "N/A"** only when a field truly cannot be found after thorough search
- **Distinguish** between:
  - Explicitly stated facts → Extract directly
  - Implied but not stated → Mark as "N/A" or note as implied
  - Absent information → "N/A"
- **Confidence scoring**: Rate each extraction as High/Medium/Low confidence

### 2. Field Understanding (字段理解)
- Understand the semantic meaning of each table header
- Map paper content to headers based on meaning, not just keyword matching
- Handle synonyms and domain-specific terminology
- Recognize implicit information in context

### 3. Structured Depth (结构化深度)
- Extract at appropriate granularity
- Distinguish between study-level, experiment-level, and result-level information
- Preserve relationships between related fields
- Handle multi-experiment papers correctly

### 4. Batch Stability (批处理稳定性)
- Process papers independently (failure of one doesn't affect others)
- Log all operations for audit trail
- Support resume from interruption
- Validate outputs before writing to table

## Workflow

### Step 1: Identify Inputs
- **Papers**: Single file, multiple files, or folder path → 支持 PDF/DOCX/TXT
- **Table template**: XLSX 或 CSV，含表头定义结构
- **Language**: 自动检测或用户指定
- **Domain**: Psychology / Cognitive Neuroscience / Computer Science / Brain Science / General

### Step 2: Read Table Headers

```bash
python scripts/read_table.py <table_path>
```

输出：列名、数据类型约束、领域推断。

### Step 3: Extract Paper Content

```bash
python scripts/extract_paper.py <paper_path> --structured
```

**自动处理格式**：PDF→pdfplumber/PyMuPDF/OCR fallback；DOCX→python-docx；TXT→直接读取。

**输出结构化 JSON**：包含 `full_text` 和 `sections`（abstract/introduction/methods/results/discussion/conclusion）。

### Step 4: LLM Extraction (Critical)

**原则**：只提取论文明确陈述的信息，绝不臆造。

**输入**：表头 + 论文全文/章节

**输出格式**（每个字段）：
```json
{
  "FieldName": {
    "value": "extracted value 或 N/A",
    "confidence": "HIGH/MEDIUM/LOW",
    "source": "paper location"
  }
}
```


**CRITICAL RULES：**
1. JSON keys 必须与表头完全匹配（大小写敏感）
2. 缺失信息→`"N/A"`，不做推断
3. 多值用分号分隔
4. 保留原文语言
5. LOW confidence 字段需说明原因

**提取优先级**：Abstract→Methods→Results→Discussion→补充材料

### Step 5: Validate & Write

```bash
python scripts/write_table.py <table_path> '<json_data>' --validate
```

**验证内容**：JSON格式、键名匹配、无重复条目、数据类型合理。

**重复检测**：标题相似度>85%视为重复，跳过并警告。

### Step 6: Report

报告：处理论文数、新增行数、跳过数（重复/错误）、LOW confidence 字段、输出路径。

## Batch Processing

```bash
python scripts/batch_process.py <papers_folder> <table_path> [output_folder]
```

- 独立处理每篇论文（单篇失败不影响其他）
- 自动生成日志 `batch_log_YYYYMMDD_HHMMSS.json`
- 支持断点续传（从日志恢复进度）

详细字段定义、提取策略 → `references/extraction-patterns.md`
质量检查清单 → `references/quality-checklist.md`

## Domain Specializations

### Psychology / Cognitive Neuroscience / Computer Science / Brain Science
