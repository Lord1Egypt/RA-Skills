---
name: gi-excel-pdf-process
description: Process Excel and PDF files - extract data, parse tables, generate reports. Use when working with .xlsx, .xls, .csv, .pdf files, or when the user mentions spreadsheet, PDF extraction, or report generation.
tags: ["excel", "pdf", "spreadsheet", "data-extraction", "report", "python"]
---

# Excel / PDF 处理

处理 Excel 与 PDF 文件：提取数据、解析表格、生成报告。适用于数据导入导出、报表生成、文档解析等场景。

## 何时使用

- 用户提供或请求处理 `.xlsx`、`.xls`、`.csv`、`.pdf` 文件
- 用户提到「表格」「Excel」「报表」「PDF 提取」「表单」
- 需要从文件读取数据或生成可下载文件

**可执行脚本**：`scripts/excel_extract.py`（Excel→CSV）、`scripts/pdf_extract.py`（PDF 文本/表格提取），依赖见 `scripts/requirements.txt`。

## Excel 处理

### 读取 Excel

```python
import pandas as pd

# 读取整个文件
df = pd.read_excel("file.xlsx", sheet_name=0)  # 第一个 sheet

# 指定 sheet
df = pd.read_excel("file.xlsx", sheet_name="Sheet1")

# 读取 CSV
df = pd.read_csv("file.csv", encoding="utf-8")
```

### 写入 Excel

```python
# 单 sheet
df.to_excel("output.xlsx", index=False)

# 多 sheet
with pd.ExcelWriter("output.xlsx") as writer:
    df1.to_excel(writer, sheet_name="汇总", index=False)
    df2.to_excel(writer, sheet_name="明细", index=False)
```

### 常用操作

- 筛选：`df[df['列名'] > 0]`
- 去重：`df.drop_duplicates(subset=['列名'])`
- 合并：`pd.concat([df1, df2])` 或 `pd.merge(df1, df2, on='key')`
- 透视：`df.pivot_table(values='val', index='row', columns='col', aggfunc='sum')`

### 依赖

```bash
pip install pandas openpyxl  # xlsx 需要 openpyxl
```

## PDF 处理

### 提取文本

```python
import pdfplumber

with pdfplumber.open("file.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            print(text)
```

### 提取表格

```python
with pdfplumber.open("file.pdf") as pdf:
    page = pdf.pages[0]
    tables = page.extract_tables()
    for table in tables:
        # table 为二维列表
        for row in table:
            print(row)
```

### 依赖

```bash
pip install pdfplumber
```

若需 OCR（扫描版 PDF）：`pip install pdf2image pytesseract`，并安装 Tesseract。

## 报告生成流程

1. **数据准备**：从 API/DB 或 Excel 获取数据，用 pandas 清洗
2. **计算/聚合**：按业务逻辑生成汇总表
3. **输出**：
   - Excel：`df.to_excel()`
   - PDF：可用 `reportlab` 或先生成 Excel 再转 PDF

## 注意事项

- 大文件：分块读取或限制行数，避免内存溢出
- 编码：CSV 常见 `utf-8`、`gbk`，先尝试 `utf-8`
- 空值：`df.fillna(0)` 或 `df.dropna()` 按需处理
- 日期：`pd.to_datetime(df['date_col'])` 统一格式
