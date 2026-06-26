---
name: BIPPI-imp-trm-accstmt
description: |
  银行对账单转换为各系统标准银行账户流水导入模板的技能。当用户需要将银行对账单文件（MT940格式的SWIFT银行对账单、国内各银行的Excel格式对账单、或PDF格式对账单）转换为BIPV5、金蝶云星瀚(EAS_YXH)、保融ATS(FINGARD)、九恒星司库(NSTC)、用友NCC(YYNCC)等系统的标准导入模板时，**必须使用此技能**。

  **核心功能**：解析MT940/Excel/PDF格式银行对账单 → 智能字段映射 → 生成对应系统标准Excel/xls导入模板

  **支持的目标系统**：
  - **BIPV5**（默认）：银行流水处理 Excel 模板
  - **EAS_YXH**（金蝶云星瀚）：离线明细导入 .xlsx 模板
  - **FINGARD**（保融ATS）：离线信息 .xls 模板
  - **NSTC**（九恒星司库）：批量导入银行明细格式 .xls 模板
  - **YYNCC**（用友NCC）：数据页签 .xls 模板

  **必须触发场景**：
  - "银行对账单转换"、"MT940解析"、"银行流水导入模板"
  - "境外银行对账单"、"SWIFT对账单处理"、"生成BIP导入文件"
  - "PDF对账单转换"、"PDF银行流水"、"银行PDF导入"
  - "转换为金蝶云星瀚模板"、"EAS_YXH导入"、"金蝶流水导入"
  - "转换为保融ATS"、"FINGARD对账单"、"保融流水导入"
  - "转换为九恒星"、"NSTC导入"、"九恒星司库流水"
  - "转换为用友NCC"、"Yonyou NCC导入"、"NC流水"
  - "bank statement import"、"MT940 to BIP"、"PDF to BIP"
  - 处理MT940格式（TXT/STA文件）的银行对账单
  - 国内银行Excel格式对账单转换（如招商银行、中信银行、兴业银行等）
  - 国内银行PDF格式对账单转换（如农商行、平安银行、恒丰银行、浙商银行、郑州银行等）
  - 批量转换多银行对账单生成导入模板（合并为单个文件）
  - 将银行流水数据导入到BIPV5、金蝶云星瀚、保融ATS、九恒星司库、用友NCC等系统
  - 处理对账单中账号与交易明细分离的情况
  - 当用户提到银行对账单、MT940、SWIFT、银行流水、账户流水、PDF对账单、金蝶/保融/九恒星/用友等关键词时

  **输出位置**：默认情况下，输出文件将保存在与输入文件相同的目录中，保持数据同位置管理。

  **特性说明**：
  - 支持MT940格式解析（SWIFT标准银行对账单）
  - 支持国内各银行Excel格式对账单（招商、中信、兴业、浦发、民生、徽商、广西北部湾、渤海、国开、中原等）
  - **支持国内各银行PDF格式对账单**（文本型PDF + 可选OCR支持图片型PDF）
  - 内置余弦相似度算法智能匹配字段（自动处理列名差异）
  - 支持对方账号/对方名称的多种别名匹配（对方账号、对手账号、收款账号等）
  - 可配置的JSON映射文件支持灵活扩展新的银行格式和目标系统
  - 支持借贷标识自动分离、日期格式转换、币种处理
  - 支持从表头区域自动提取本方账号信息
  - 自动清理账号中的币种标识（如"账号（人民币）"自动处理）
  - PDF解析支持多种列头折行格式（如"交易时"+"间" → "交易时间"）
  - PDF解析使用PyMuPDF的X/Y位置信息按列重组表格（不依赖固定列数）
  - 5 个目标系统的输出严格遵循各自模板格式（EAS_YXH 保留单元格批注和下拉项；FINGARD/NSTC/YYNCC 保留说明 sheet 和对照表）

  **注意**：本技能通过可配置的映射文件支持灵活扩展新的银行格式和目标系统，无需修改代码即可适应新的对账单格式。

  **模板文件加载策略（兼容 clawhub 等不支持上传二进制模板的市场）**：
  - 5 个目标系统的导入模板位于 `assets/template/` 目录下：
    - `YYBIPV5_banktransaction.xlsx` — BIPV5
    - `eas_yxh_banktransaction.xlsx` — 金蝶云星瀚
    - `fingard_banktransaction.xls` — 保融ATS
    - `nstc_banktransaction.xls` — 九恒星司库
    - `yyncc_banktransaction.xls` — 用友NCC
  - 当用户基于 clawhub 之类的市场安装本 skill，且 `assets/template/` 目录下缺失对应模板文件时，会自动从预配置的互联网地址下载到本地使用。
  - 模板加载统一入口：`scripts/core/template_manager.py::resolve_template(target_system)`。
compatibility:
  python: "3.8+"
  dependencies:
    - openpyxl
    - pandas
    - scikit-learn
    - pymupdf
    - pillow
    - xlrd
    - xlwt
---

# BIPPI-imp-trm-accstmt - 银行对账单转换技能

将银行对账单文件（MT940格式、国内银行Excel格式或PDF格式）转换为目标系统的标准银行账户流水导入模板。

## 核心特性

1. **多格式解析支持**：通过插件化的解析器系统支持扩展（MT940/Excel/PDF）
2. **多系统输出支持**：通过插件化的映射器系统支持扩展：
   - **BIPV5**：银行流水处理 Excel 模板
   - **EAS_YXH**（金蝶云星瀚）：离线明细导入 .xlsx 模板
   - **FINGARD**（保融ATS）：离线信息 .xls 模板
   - **NSTC**（九恒星司库）：批量导入银行明细格式 .xls 模板
   - **YYNCC**（用友NCC）：数据页签 .xls 模板
3. **智能字段匹配**：使用余弦相似度算法匹配可能存在细微差异的列名
4. **可配置映射**：通过JSON配置文件管理字段映射关系
5. **批量合并**：支持将多个银行对账单合并为单个文件
6. **PDF支持**：基于PyMuPDF的X/Y位置信息按列重组表格，兼容多种列头折行格式

## 支持的银行格式

### 国际格式
- MT940 (SWIFT标准银行对账单)

### 国内银行Excel格式

### 国内银行PDF格式

## 使用方法

### 基本转换

**单文件转换**：
```
请将 平安银行.pdf 银行对账单转换为 目标 系统的导入模板
```

**批量合并转换**（将目录下所有对账单合并为单个文件）：
```
将当前目录下所有银行对账单（MT940、Excel和PDF格式）合并转换为一个目标系统的导入模板
```

### 完整参数指定

```
将以下银行对账单转换为 BIPV5 系统导入模板：
- 输入文件：/path/to/平安银行.pdf
- 输出文件：/path/to/output/BIPV5_平安银行.xlsx
- 目标系统：BIPV5
- 账户组织编码：ORG001
- 银行名称：平安银行
```

### 输出位置说明

| 转换模式 | 默认输出位置 |
|----------|--------------|
| 单文件转换 | 与输入文件相同目录 |
| 批量合并转换 | 与输入目录相同位置 |
| 指定输出路径 | 用户指定路径 |

输出文件名格式：
- 单文件：`{原文件名}_BIPV5.xlsx`
- 合并文件：`merged_BIPV5.xlsx`

## 工作流程

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  输入文件       │───▶│  格式解析器     │───▶│  数据映射器     │───▶│  输出生成器     │
│  (MT940/Excel/  │    │  (Parser)       │    │  (Mapper)       │    │  (Excel)        │
│   PDF)          │    │                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
                              │                      │                      │
                              ▼                      ▼                      ▼
                       parsers/              mappings/               输出文件
                       mt940_parser.py       mt940_to_bipv5.json     BIPV5_银行流水.xlsx
                       excel_parser.py
                       pdf_parser.py
```

## BIPV5目标字段

| 字段代码 | 中文名称 | 必填 | 说明 |
|----------|----------|------|------|
| accentity_code | 账户使用组织编码 | 否 | 组织编码 |
| bankaccount_account | *银行账号 | 是 | 银行账号 |
| bankNumber_name | 银行名称 | 否 | 开户行名称 |
| bank_seq_no | *本方交易流水号 | 是 | 银行流水序号 |
| tran_date | *交易日期 | 是 | 交易日期YYYY-MM-DD |
| tran_time | 交易时间 | 否 | 交易时间HH:MM:SS |
| dc_flag | 借贷标识 | 否 | C=贷,D=借 |
| debitamount | 支出金额 | 否 | 借方发生额 |
| creditamount | 收入金额 | 否 | 贷方发生额 |
| currency_name | *币种 | 是 | ISO币种代码 |
| tran_amt | 金额 | 否 | 交易金额 |
| to_acct_no | 对方账号 | 否 | 交易对方账号 |
| to_acct_name | 对方户名 | 否 | 交易对方名称 |
| to_acct_bank_name | 对方银行名称 | 否 | 对方银行 |
| use_name | 用途 | 否 | 资金用途 |
| remark | 摘要 | 否 | 交易摘要 |
| remark01 | 附言 | 否 | 附加说明 |
| acct_bal | 余额 | 否 | 账户余额 |

## 解析器系统

### MT940解析器

MT940格式关键字段映射：

| MT940 Tag | 说明 | 示例 |
|-----------|------|------|
| :20: | 交易参考号 | STMT24010001 |
| :25: | 账号识别 | 1234567890 |
| :28C: | 语句编号 | 1/1 |
| :60F: | 期初余额 | D240101USD1000,00 |
| :61: | 交易记录 | 日期+借贷+金额 |
| :86: | 交易详情 | 对方名称等 |
| :62F: | 期末余额 | C240131USD1500,00 |

### Excel解析器特性

1. **智能表头识别**：自动查找包含"交易日期"或"交易时间"的行作为表头
2. **账号自动提取**：从表头区域提取本方账号、户名、币种信息
3. **币种清理**：自动清理账号中的币种标识
4. **字段智能匹配**：使用余弦相似度匹配各种列名格式

### PDF解析器特性

1. **双模式支持**：
   - **文本型PDF（默认）**：使用 PyMuPDF 的 `page.get_text()` 直接提取文字
   - **图片型PDF（可选）**：通过可插拔 OCR 接口（默认 Tesseract）识别

2. **位置信息驱动**：使用 PyMuPDF 的 X/Y 坐标信息按列重组表格，不依赖固定列数

3. **列头归一化**：智能处理多种列头折行格式：
   - 中文两行折行（如 `交易时` + `间` → `交易时间`）
   - 中英文对照（如 `贷方发` + `生额(收` + `入)` → `贷方发生额(收入)`）
   - 含括号元（如 `发生金额（元）` → `发生金额`）

4. **可插拔OCR接口**：
   ```python
   from scripts.parsers.pdf_parser import PDFParser, TesseractOCR

   parser = PDFParser()
   parser.set_ocr_backend(TesseractOCR())  # 注入 Tesseract OCR
   data = parser.parse('image_based.pdf')
   ```

5. **多页PDF自动合并**：跨页交易表自动识别（按 Y 坐标分组、按 X 坐标排序列）

### 添加新解析器

1. 在 `scripts/parsers/` 目录创建新的解析器文件
2. 继承 `BaseParser` 类
3. 实现 `parse()` 和 `detect_format()` 方法
4. 在 `scripts/core/parser_factory.py` 中注册

## 输出文件格式

### BIPV5 Excel模板结构

```
模板文件: assets/template/YYBIPV5_banktransaction.xlsx
Sheet: 银行流水处理
├── Row 1-3: 模板说明
├── Row 4: 英文字段名 (id, accentity_code, bankaccount_account, ...)
├── Row 5: 空行
├── Row 6: 中文字段名 (*银行账号, *本方交易流水号, ...)
├── Row 7-9: 空行
└── Row 10+: 数据行
```

## 目录结构

```
BIPPI-imp-trm-accstmt/
├── SKILL.md                    # 技能说明文件
├── scripts/
│   ├── main.py                 # 主入口
│   ├── core/
│   │   ├── data_structures.py  # 数据结构定义
│   │   ├── parser_factory.py   # 解析器工厂
│   │   ├── mapper_factory.py   # 映射器工厂
│   │   ├── cosine_similarity.py # 余弦相似度工具
│   │   ├── currency_map.py     # 币种代码映射
│   │   └── template_manager.py # 模板文件管理器（本地查找+自动下载）
│   ├── parsers/
│   │   ├── base_parser.py      # 解析器基类
│   │   ├── mt940_parser.py     # MT940解析器
│   │   ├── excel_parser.py     # 国内银行Excel解析器
│   │   └── pdf_parser.py       # 国内银行PDF解析器（文本+可插拔OCR）
│   ├── mappers/
│   │   ├── base_mapper.py      # 映射器基类
│   │   ├── _xls_template_helpers.py # xls模板写入辅助
│   │   ├── bipv5_mapper.py     # BIPV5映射器
│   │   ├── eas_yxh_mapper.py   # 金蝶云星瀚映射器
│   │   ├── fingard_mapper.py   # 保融ATS映射器
│   │   ├── nstc_mapper.py      # 九恒星司库映射器
│   │   └── yyncc_mapper.py     # 用友NCC映射器
│   └── mappings/
│       └── mt940_to_bipv5.json # MT940到BIPV5映射配置
├── assets/
│   └── template/               # 5 个目标系统的导入模板
│       ├── YYBIPV5_banktransaction.xlsx
│       ├── eas_yxh_banktransaction.xlsx
│       ├── fingard_banktransaction.xls
│       ├── nstc_banktransaction.xls
│       └── yyncc_banktransaction.xls
├── references/
│   ├── currency.md             # 币种代码参考
│   └── User Guide - Exporting Data in SWIFT MT940 Format[1].pdf
└── evals/
    └── evals.json              # 测试用例
```

## 常用命令

```bash
# 单文件转换（输出到输入文件同目录）
python scripts/main.py input.xlsx
python scripts/main.py input.pdf

# 单文件转换（指定输出路径）
python scripts/main.py input.xlsx -o output/BIPV5_output.xlsx
python scripts/main.py input.pdf -o output/BIPV5_output.xlsx

# 批量转换（每个文件单独输出到输入目录）
python scripts/main.py --batch -i ./input_dir

# 批量合并（输出到输入目录）
python scripts/main.py --merge -i ./input_dir

# 批量合并（指定输出文件）
python scripts/main.py --merge -i ./input_dir -o ./output/merged.xlsx
```

## 依赖要求

- Python 3.8+
- openpyxl
- pandas
- scikit-learn (用于余弦相似度匹配)
- pymupdf (PyMuPDF，用于PDF文本提取)
- pillow (PIL，用于OCR图片处理)

安装依赖：
```bash
pip install openpyxl pandas scikit-learn pymupdf pillow
```

如需OCR支持图片型PDF（可选）：
```bash
pip install pytesseract
# 还需要安装系统级 Tesseract：Windows 从 https://github.com/UB-Mannheim/tesseract/wiki 下载并安装
# 安装中文语言包（chi_sim），然后在 PDFParser 中注入：
#   parser.set_ocr_backend(TesseractOCR())
```

## PDF处理已知限制

1. **浦发银行对账单（英文+中文混合版式）**：当前通用启发式无法准确解析，列头散布在多 Y 位置。建议先用 Adobe/PDF转Excel工具预处理。
2. **强加密PDF**：受密码保护的PDF需先解密。
3. **扫描型PDF**：默认未启用OCR，需安装Tesseract并注入OCR后端。
4. **跨页表格**：当前已支持基础的多页合并，但极端情况下表头只出现在第一页。

## 错误处理

| 错误代码 | 说明 | 处理建议 |
|----------|------|----------|
| E001 | 无法识别文件格式 | 检查文件是否为有效的MT940/Excel/PDF格式 |
| E002 | 解析失败 | 检查文件内容是否符合规范 |
| E003 | 必填字段缺失 | 检查映射配置是否完整 |
| E004 | 日期格式错误 | 检查日期字段格式配置 |
| E005 | 金额格式错误 | 检查金额字段格式配置 |
| E006 | 映射配置错误 | 检查JSON配置文件语法 |
| E007 | 输出目录不存在 | 创建输出目录 |
| E008 | PDF无可提取文字且未配置OCR | 安装Tesseract OCR并注入后端，或预转换PDF为文本型 |
| E009 | PDF页面无文字层且无图片 | 检查PDF是否有效 |

## 扩展指南

### 添加新的银行对账单格式

1. 创建新的解析器类继承 `BaseParser`
2. 实现 `parse()` 和 `detect_format()` 方法
3. 创建对应的映射配置文件
4. 在 `parser_factory.py` 中注册

### 添加新的目标系统

1. 创建新的映射器类继承 `BaseMapper`
2. 实现到新系统的字段映射
3. 在 `mapper_factory.py` 中注册
4. 创建对应的目标模板文件

### 接入新的OCR后端

1. 实现 `OCRBackend` 接口的 `image_to_text` 方法
2. 通过 `PDFParser.set_ocr_backend(your_backend)` 注入
3. 适用于：百度OCR、阿里云OCR、腾讯云OCR、PaddleOCR等
