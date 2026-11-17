---
name: pdf-invoice-stat
description: PDF 增值税发票提取 skill v2.4.3（稳定版）。支持增值税电子普票、铁路电子客票、通行费、餐饮、过路费等 PDF 格式，本地运行无外部 API 依赖，输出 15 列 Excel 报表。
---

# PDF 增值税发票提取 Skill v2.4.3（稳定版）

> **当前版本**: v2.4.3  
> **发布状态**: 稳定版（Stable）  
> **发布日期**: 2026-10-18  
> **测试覆盖**: 48 张真实发票（idunique 10 张 + youge 海口 38 张）

## 版本号（单一真相源）

```python
from version import __version__  # "2.4.3"
```

## 核心能力

| 能力 | 状态 |
|------|------|
| 增值税电子普通发票 | ✅ |
| 铁路电子客票（火车票）| ✅ |
| 通行费发票 | ✅ |
| 餐饮发票 | ✅ |
| 过路费发票 | ✅ |
| 合并 PDF 多张发票 | ✅ |
| 跨行发票号/日期识别 | ✅ |
| 多税率发票税率留空（设计规范）| ✅ |
| 项目名杂质清理 | ✅ |
| 多项目分行 | ✅ |

## 已知不支持（本目录范围外）

| 不支持 | 原因 |
|--------|------|
| XML（数电票/全电发票）| 另一 SKU 路径 |
| OFD（国标版式发票）| 另一 SKU 路径 |

## 目录边界

**本目录**：`v2.4.3 PDF 单格式版`，仅处理 PDF 格式增值税发票。

## 使用方式

### 方式一：作为 Python 模块

```python
import sys
sys.path.insert(0, '/path/to/pdf-invoice-stat')
from invoice_extractor import extract_all_invoices, create_excel

# 识别发票
invoices = extract_all_invoices('invoices.pdf')

# 输出 Excel
create_excel(invoices, duplicate_rows=[], output_path='output.xlsx')
```

### 方式二：命令行（待加 argparse）

```bash
# 未来 v2.4.4 计划
python3 invoice_extractor.py invoices.pdf
```

## 输出 Excel 字段（15 列）

| # | 字段 | 来源 |
|---|------|------|
| 1 | 序号 | 自动 |
| 2 | 发票号码 | 页面提取 |
| 3 | 开票日期 | 页面提取 |
| 4 | 购买方信息-名称 | 页面提取 |
| 5 | 购买方信息-统一社会信用代码 | 页面提取 |
| 6 | 销售方信息-名称 | 页面提取 |
| 7 | 销售方信息-统一社会信用代码 | 页面提取 |
| 8 | 项目名称 | 页面提取 |
| 9 | 金额 | 页面提取 |
| 10 | 税率/征收率 | 页面提取 |
| 11 | 税额 | 页面提取 |
| 12 | 价税合计 | 页面提取 |
| 13 | 备注 | 页面提取 |
| 14 | 报销人 | 手动填 |
| 15 | 报销日期 | 手动填 |

## 运行测试

```bash
bash run_tests.sh
```

或单跑：
```bash
python3 tests/test_extract_v243.py
python3 tests/perf_test.py
```

## 配置（可选）

`config.py` 集中管理可调参数。删除它，主代码会走 fallback 默认值。

## 依赖

```text
pdfplumber>=3.0.0
openpyxl>=3.0.0
```

## License

MIT
