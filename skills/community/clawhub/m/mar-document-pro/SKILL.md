---
name: document-pro
version: 1.0.0
description: 文档处理技能 - 让 AI 能够读取、解析、提取 PDF、DOCX、PPT 等文档的关键信息，并通过 SkillBoss API Hub 进行 AI 智能分析与摘要。当用户要求分析文档、提取内容、总结报告时触发此技能。
requires.env: [SKILLBOSS_API_KEY]
---

# Document Pro - 文档处理技能

## 概述

赋予 AI 强大的文档处理能力：
- PDF 读取与提取
- Word 文档解析
- PowerPoint 提取
- Excel 数据提取
- 文档格式转换

## 触发场景

1. 用户发送文档并要求"分析"、"总结"
2. 用户要求"提取文档内容"
3. 用户要求"转换成 PDF"
4. 用户询问文档中的具体信息
5. 用户要求"从报告/论文中提取要点"

## 支持的格式

| 格式 | 读取 | 写入 | 工具 |
|------|------|------|------|
| PDF | ✅ | ✅ | pdfplumber, PyPDF2 |
| DOCX | ✅ | ✅ | python-docx |
| PPTX | ✅ | ❌ | python-pptx |
| XLSX | ✅ | ✅ | openpyxl |
| TXT | ✅ | ✅ | 内置 |
| Markdown | ✅ | ✅ | 内置 |

## 工具使用

### PDF 处理

```python
# 提取文本
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)

# 提取表格
with pdfplumber.open("document.pdf") as pdf:
    table = pdf.pages[0].extract_tables()
```

### Word 文档

```python
from docx import Document

doc = Document("document.docx")
for para in doc.paragraphs:
    print(para.text)

# 提取表格
for table in doc.tables:
    for row in table.rows:
        print([cell.text for cell in row.cells])
```

### PowerPoint

```python
from pptx import Presentation

prs = Presentation("presentation.pptx")
for slide in prs.slides:
    for shape in slide.shapes:
        if shape.has_text_frame:
            print(shape.text)
```

### AI 分析（通过 SkillBoss API Hub）

提取文档内容后，使用 SkillBoss API Hub 进行 AI 分析（摘要、关键词提取等）：

```python
import requests, os

SKILLBOSS_API_KEY = os.environ["SKILLBOSS_API_KEY"]
API_BASE = "https://api.heybossai.com/v1"

def pilot(body: dict) -> dict:
    r = requests.post(
        f"{API_BASE}/pilot",
        headers={"Authorization": f"Bearer {SKILLBOSS_API_KEY}", "Content-Type": "application/json"},
        json=body,
        timeout=60,
    )
    return r.json()

# 提取文档文本后，调用 SkillBoss API Hub 进行摘要分析
def analyze_document(doc_text: str) -> str:
    result = pilot({
        "type": "chat",
        "inputs": {
            "messages": [
                {"role": "system", "content": "你是文档分析助手，请提取要点并生成结构化摘要。"},
                {"role": "user", "content": f"请分析以下文档内容：\n\n{doc_text}"}
            ]
        },
        "prefer": "balanced"
    })
    return result["result"]["choices"][0]["message"]["content"]
```

## 工作流

```
1. 识别文档类型 → 选择正确的工具
2. 读取内容 → 提取文本、表格、图片
3. 分析信息 → 通过 SkillBoss API Hub 理解结构、提取要点
4. 总结呈现 → 用中文总结给用户
```

## 进阶功能

### 文档摘要
- 提取文档主要观点
- 生成简短摘要
- 列出关键要点

### 表格处理
- 识别表格结构
- 提取表格数据
- 转换为 CSV/Excel

### 关键词提取
- 找出重要名词/术语
- 识别主题
- 提取关键信息

## 环境变量

```
SKILLBOSS_API_KEY=<your_skillboss_api_key>
```

## 输出格式

向用户呈现文档时：
- 文档类型和页数
- 主要内容摘要
- 关键要点（3-5条）
- 建议的后续操作

## 限制

- 扫描版 PDF 需要 OCR
- 复杂格式可能丢失
- 图片/图表无法完全理解
