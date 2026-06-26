name: pdf-field-extractor
description: "PDF关键信息提取 — AI驱动的PDF结构化数据提取工具。把PDF里的关键字段抽成Excel/JSON。支持的文档类型：发票、合同、收据、银行对账单、营业执照、身份证、快递单、通用文档。触发词：PDF提取、PDF字段提取、PDF转Excel、PDF转JSON、发票提取、合同提取、文档识别、批量PDF、PDF批量处理、字段提取"
override-tools: []
---

# PDF Field Extractor · PDF关键信息提取

AI驱动的PDF结构化数据提取工具——把PDF里的关键字段抽成Excel/JSON。

## 一键端到端流程

用户上传PDF → 文档类型识别 → AI字段提取 → 结构化输出（Excel/JSON）

```python
# 核心调用示例
from scripts.pdf_extractor import extract_pdf_text
from scripts.field_extractor import extract_fields
from scripts.output_generator import generate_excel, generate_json

# Step 1: 提取PDF文本（PyMuPDF + pdfplumber）
text, tables, images = extract_pdf_text("invoice.pdf")

# Step 2: AI字段提取（用户配置API Key，OpenAI兼容格式）
fields = extract_fields(
    text=text,
    doc_type="invoice",
    api_key="sk-xxx",           # 用户自己的API Key
    api_base="https://api.openai.com/v1",  # 可配置
    model="gpt-4o",
)

# Step 3: 输出Excel或JSON
generate_excel(fields, "output.xlsx")
generate_json(fields, "output.json")
```

## 核心模块

### 1. PDF文本提取 (`scripts/pdf_extractor.py`)

- **PyMuPDF**：高速文本提取，支持加密PDF
- **pdfplumber**：表格精确提取，保留表格结构
- **自动判断**：文本型PDF vs 扫描件（无文本层→触发OCR）

```python
# 返回：(full_text, tables_list, has_text_layer)
text, tables, is_scanned = extract_pdf_text("document.pdf")
```

### 2. OCR处理 (`scripts/ocr_processor.py`)

- **pytesseract**：本地OCR引擎，多语言支持
- **图片预处理**：去噪、增强对比度，提升识别率
- **支持语言**：中文、英文、日文、韩文等

```python
# 返回：OCR识别后的文本
ocr_text = process_ocr(image_path, lang="chi_sim+eng")
```

### 3. AI字段提取 (`scripts/field_extractor.py`)

- **模型无关**：OpenAI兼容格式，适配任意大模型
- **用户自配API Key**：安全可控，不存储密钥
- **支持模型**：GPT-4o/MiniMax/DeepSeek/豆包等

```python
fields = extract_fields(
    text="发票号：12345678\\n日期：2024-01-01\\n金额：1000.00",
    doc_type="invoice",
    custom_fields=["发票号", "日期", "金额", "买方", "卖方"],
    api_key="sk-xxx",
    model="gpt-4o",
)
```

### 4. 文档类型识别 (`scripts/doc_type_identifier.py`)

- **自动识别**：发票/合同/营业执照/身份证/收据/银行对账单/快递单/通用
- **基于关键词+AI辅助判断**

```python
doc_type = identify_doc_type(text)
# 返回: "invoice" | "contract" | "license" | "id_card" | "receipt" | "bank_statement" | "express" | "generic"
```

### 5. 输出生成 (`scripts/output_generator.py`)

- **Excel**：结构化数据，一行一条记录，支持多sheet
- **JSON**：嵌套结构，保留完整字段信息
- **飞书消息**：结果摘要推送飞书

```python
from scripts.output_generator import generate_excel, generate_json, build_feishu_message

generate_excel(results, "extracted_data.xlsx", sheet_name="Sheet1")
generate_json(results, "extracted_data.json")

# 飞书消息卡片
msg = build_feishu_message(results, doc_type="invoice")
# feishu_im_user_message action=send ...
```

### 6. 批量处理 (`scripts/batch_processor.py`)

```python
results = process_batch(
    pdf_files=["doc1.pdf", "doc2.pdf", "doc3.pdf"],
    doc_type="invoice",
    api_key="sk-xxx",
    max_workers=4,
)
generate_excel(results, "batch_output.xlsx")
```

## 定价套餐（Token前缀：PDF-FREE / PDF-BSC / PDF-STD / PDF-PRO / PDF-ENT）

| 套餐 | 价格 | 功能 |
|------|------|------|
| Free | $0 | 10页/月，发票类型，文本输出 |
| Basic | ¥9.9/月 | 200页/月，4种文档类型，Excel输出 |
| Standard | ¥29/月 | 1000页/月，批量处理，通用文档类型 |
| Professional | ¥69/月 | 不限页数，JSON输出，API优先 |
| Enterprise | ¥149/月 | 不限一切，多语言OCR，定制字段模板 |

## 套餐限制配置 (`scripts/tier_config.py`)

```python
from scripts.tier_config import TierConfig, TIER_LIMITS

# 检查套餐限制
config = TierConfig(tier="PDF-BSC")
config.check_limits(pages=150, doc_types=5)  # 超出Basic限制会抛出异常
```

## 使用示例

### 示例1：发票字段提取
```
用户：帮我提取这张发票的关键信息
[上传PDF: invoice.pdf]
```
→ 识别为"发票"类型 → 提取：发票号、日期、金额、买方、卖方、商品明细
→ 输出Excel或JSON

### 示例2：合同关键条款提取
```
用户：从这份合同里提取签订日期、金额、甲乙双方和违约条款
[上传PDF: contract.pdf]
```
→ 识别为"合同"类型 → AI按字段提取 → 结构化输出

### 示例3：批量处理
```
用户：批量处理这10份PDF，输出到Excel
[上传多个PDF文件]
```
→ 逐个提取 → 合并结果 → 生成Excel

### 示例4：通用文档（用户自定义字段）
```
用户：从这份文档里提取：姓名、职位、入职日期、部门
[上传PDF]
```
→ 识别为"通用"类型 → AI按用户指定字段提取

## 常见问题

| 问题 | 解答 |
|------|------|
| 如何处理扫描件？ | 自动检测无文本层PDF，触发pytesseract OCR，支持多语言 |
| API Key如何配置？ | 用户在Agent中配置，Skill调用时不存储 |
| 支持哪些输出格式？ | Excel(.xlsx)和JSON，批量时优先Excel |
| 能处理多少页的PDF？ | Free版10页/月，付费版按套餐 |
| 如何提升OCR识别率？ | 确保图片清晰、分辨率足够（建议300dpi），可预处理去噪 |

## 参考资料

- 文档类型识别规则：[references/doc_types.md](references/doc_types.md)
- AI字段提取Prompt模板：[references/prompts.md](references/prompts.md)
- 套餐配置与限制：[scripts/tier_config.py](scripts/tier_config.py)
