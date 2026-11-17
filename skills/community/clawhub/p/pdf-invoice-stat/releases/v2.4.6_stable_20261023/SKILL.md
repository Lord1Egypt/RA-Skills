---
name: pdf-invoice-stat
description: 多格式增值税发票提取 skill v2.4.6（稳定版）。支持 PDF / XML / OFD / ZIP / RAR 五种格式，涵盖增值税电子普票、铁路电子客票、通行费、餐饮、过路费等类型，本地运行无外部 API 依赖，输出 v2.4.0 原版 15 列 Excel 报表。
---

# 多格式发票提取 Skill v2.4.6（稳定版）

> **当前版本**: v2.4.6  
> **发布状态**: 稳定版（Stable）  
> **发布日期**: 2026-10-23  
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

## 格式支持（v2.4.5 新增 XML/OFD/ZIP/RAR）

| 格式 | 说明 | 状态 |
|------|------|------|
| PDF | 增值税电子发票 | ✅ 主路径（零改动）|
| XML | 数电票 / 全电发票 | ✅ v2.4.5 |
| OFD | 国标 GB/T 33190 | ✅ v2.4.5 |
| ZIP | 压缩包（内含三种格式）| ✅ v2.4.5 |
| RAR | 压缩包（无密码）| ✅ v2.4.5（brew install unar）|

## 目录边界

**本目录**：`v2.4.4 PDF 单格式版`，仅处理 PDF 格式增值税发票。

## 使用方式

### 方式一：统一入口（推荐，格式自动识别）

```python
import sys
sys.path.insert(0, '/path/to/pdf-invoice-stat')
from format_router import extract_invoices, create_excel_any

invoices = extract_invoices('invoice.pdf')   # PDF/XML/OFD/ZIP/RAR 自动识别
create_excel_any(invoices, 'output.xlsx')    # v2.4.0 原版 15 列样式
```

### 方式二：只用 PDF（v2.4.4 原版接口）

```python
from invoice_extractor import extract_all_invoices, create_excel
invoices = extract_all_invoices('invoices.pdf')
create_excel(invoices, duplicate_rows=[], output_path='output.xlsx')
```

### 方式三：命令行

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
