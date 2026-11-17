---
name: pdf-invoice-stat
description: 支持 PDF（增值税电子普通发票、铁路电子客票、通行费、餐饮）、XML（数电票/全电发票）、OFD（国标 GB/T 33190 版式发票）三格式的发票自动分类与全量字段抽取，本地运行无外部 API 依赖，输出 Excel 报表，v3.0.0 重大升级。
---

# PDF/XML/OFD 三格式发票统计 Skill v3.0.0

基于 pdfplumber + PaddleOCR + PP-StructureV3（PDF）+ ElementTree（XML/OFD）的本地提取方案，支持**三种发票格式**：
- ✅ **PDF**：增值税电子发票（普通发票）、铁路电子客票、通行费、餐饮等
- 🆕 **XML**：数电票/全电发票（国标 2023+ 标准）
- 🆕 **OFD**：国标 GB/T 33190 版式文档发票

## 🆕 v3.0.0 重大升级

相比 v2.4.0 增量升级：

- ✅ **多格式支持**：从单一 PDF 扩展为 **PDF + XML + OFD** 三格式
- ✅ **自动识别格式**：根据文件扩展名自动路由到对应解析器
- ✅ **XML 解析器**（xml_parser.py）：支持数电票/全电发票原始 XML 数据
- ✅ **OFD 解析器**（ofd_parser.py）：支持国标版式发票（GB/T 33190）
- ✅ **统一数据模型**：三种格式输出统一字段（15 列 Excel）
- ✅ **来源格式列**：新增第 16 列「来源格式」（PDF/XML/OFD）便于审计追溯
- ✅ **ZIP 兼容**：自动解析 ZIP 压缩包内的 XML 发票

## 功能特性

| 特性 | 说明 |
|------|------|
| **支持格式** | PDF / XML（数电票/全电）/ OFD（国标）/ ZIP（含 XML） |
| **票据类型** | 增值税电子普票 + 数电票/全电发票 + 通行费 + 火车票 + 餐饮 + 过路费 |
| **提取字段** | 发票号码、开票日期、购买方、销售方、税号、项目名称、金额、税率、税额、价税合计 |
| **输出格式** | Excel（**16 列**） + 来源格式追溯列 |
| **运行方式** | 纯本地（PDF 走 pdfplumber + PaddleOCR；XML/OFD 走 ElementTree）|
| **多税率处理** | 多税率发票税率留空 |
| **免税/不征税** | 税额=0，税率列显示对应文字 |
| **ZIP 自动识别** | 自动检测 ZIP 内的 XML 发票 |

## 使用方式

### 方式一：直接使用脚本

```bash
# v3.0.0 统一入口（自动识别格式）
python3 invoice_extractor_v3.py <文件> [输出.xlsx]

# 支持格式示例
python3 invoice_extractor_v3.py invoices.pdf
python3 invoice_extractor_v3.py shuidian_2024.xml
python3 invoice_extractor_v3.py e_invoice.ofd
python3 invoice_extractor_v3.py zip_with_xml.zip
```

### 方式二：作为 Python 模块调用

```python
from invoice_extractor_v3 import extract_invoices, export_to_excel

# 自动检测格式并提取
invoices = extract_invoices('invoices.pdf')          # PDF
invoices = extract_invoices('shuidian.xml')          # XML 数电票
invoices = extract_invoices('e_invoice.ofd')         # OFD

# 统一导出
export_to_excel(invoices, 'output.xlsx')
```

### 运行示例

```bash
# 混合文件夹批量处理
for f in *.pdf *.xml *.ofd; do
    python3 invoice_extractor_v3.py "$f"
done
```

## 输出 Excel 字段（16 列）

| # | 字段 | 来源 |
|---|------|------|
| 1 | 序号 | 自动 |
| 2 | 发票号 | PDF/XML/OFD |
| 3 | 日期 | PDF/XML/OFD |
| 4 | 购方 | PDF/XML/OFD |
| 5 | 购方税号 | PDF/XML/OFD |
| 6 | 销售方 | PDF/XML/OFD |
| 7 | 销售方税号 | PDF/XML/OFD |
| 8 | 项目 | PDF/XML/OFD |
| 9 | 金额 | PDF/XML/OFD |
| 10 | 税率 | PDF/XML/OFD |
| 11 | 税额 | PDF/XML/OFD |
| 12 | 价税合计 | PDF/XML/OFD |
| 13 | 备注 | PDF/XML/OFD |
| 14 | 报销人 | 手动 |
| 15 | 报销日期 | 手动 |
| 16 | **来源格式**（🆕 v3.0）| 自动（PDF/XML/OFD） |

## 模块组成

```
pdf-invoice-stat/
├── SKILL.md                 # 本文档
├── CHANGELOG.md             # 变更日志
├── invoice_extractor_v3.py  # 🆕 v3.0 统一入口
├── invoice_extractor.py     # v2.4 PDF 解析（保留）
├── xml_parser.py            # 🆕 v3.0 XML 解析器
├── ofd_parser.py            # 🆕 v3.0 OFD 解析器
├── paddle_ocr.py            # OCR 兜底
├── pp_structure.py          # PP-Structure 识别
└── tests/                   # 测试
```

## 支持的发票类型

### PDF 格式（v2.4 继承）
- 增值税电子普通发票
- 增值税电子专用发票
- 铁路电子客票（火车票）
- 通行费发票
- 餐饮发票
- 过路费发票

### XML 格式（v3.0 🆕）
- **数电票/全电发票**（国标 2023+ 标准）
- 增值税电子普通发票 XML
- 增值税电子专用发票 XML
- 数电票包含完整结构化字段（发票号、日期、金额、税号等）

### OFD 格式（v3.0 🆕）
- **国标 GB/T 33190 版式文档**
- 国家税务总局推行的电子发票标准格式
- OFD 内部 = ZIP 压缩包 + XML 数据

## 依赖

```bash
# 必需
pip install pdfplumber openpyxl

# OCR 兜底（PDF 火车票等场景）
pip install paddleocr paddlepaddle
pip install pp-structure
```

## v2.4.0 → v3.0.0 兼容性

- ✅ 完全向后兼容：原 `invoice_extractor.py` 保留
- ✅ 新入口 `invoice_extractor_v3.py` 支持三种格式
- ⚠️ v2.4 输出 15 列，v3.0 输出 **16 列**（新增"来源格式"列）

## License

MIT

