# pdf-invoice-stat

**多格式发票提取 Skill · v2.4.6（稳定版）**

## 这是什么

从 PDF / XML / OFD / ZIP / RAR 格式的增值税电子发票中自动提取关键字段（发票号、日期、购销方、金额、税额、价税合计），输出 15 列 Excel 报表。

## 版本

```python
from version import __version__  # "2.4.6"
```

- **当前状态**: 稳定版（推荐生产使用）
- **发布日期**: 2026-10-22
- **测试覆盖**: 48 张真实发票（100% 字段完整度）

## 快速使用

**方式 A：统一入口（推荐，格式自动识别）**

```python
import sys
sys.path.insert(0, '/path/to/pdf-invoice-stat')
from format_router import extract_invoices, create_excel_any

# 1. 识别发票（自动识别 PDF/XML/OFD/ZIP/RAR）
invoices = extract_invoices('invoice.pdf')

# 2. 输出 Excel（v2.4.0 原版 15 列表头 + 样式）
create_excel_any(invoices, 'output.xlsx')
```

**方式 B：只用 PDF（v2.4.4 原版接口，零改动）**

```python
from invoice_extractor import extract_all_invoices, create_excel
invoices = extract_all_invoices('invoices.pdf')
create_excel(invoices, duplicate_rows=[], output_path='output.xlsx')
```

**命令行**

```bash
python3 format_router.py <文件或目录> [输出.xlsx]
```

## 支持的发票类型

| 发票类型 | 支持 |
|---------|------|
| 增值税电子普通发票 | ✅ |
| 增值税电子专用发票 | ✅ |
| 铁路电子客票（火车票）| ✅ |
| 通行费发票 | ✅ |
| 餐饮发票 | ✅ |
| 过路费发票 | ✅ |
| 合并 PDF（多张发票）| ✅ |
| 跨行发票号/日期 | ✅ |

## 格式支持

| 格式 | 说明 | 状态 |
|------|------|------|
| **PDF** | 增值税电子发票 | ✅ 主路径（v2.4.4 起零改动）|
| **XML** | 数电票 / 全电发票 | ✅ v2.4.5 新增 |
| **OFD** | 国标 GB/T 33190 版式 | ✅ v2.4.5 新增 |
| **ZIP** | 压缩包（内含 PDF/XML/OFD）| ✅ v2.4.5 新增 |
| **RAR** | 压缩包（无密码）| ✅ v2.4.5 新增（需 unar）|

> RAR 需要系统工具：`brew install unar`

## 目录结构

```
pdf-invoice-stat/
├── README.md                  # 本文件
├── requirements.txt           # 依赖清单
├── LICENSE                    # MIT 许可
├── version.py                 # 版本定义（单一真相源）
├── invoice_extractor.py      # 主代码（v2.4.3 稳定版）
├── invoice_extractor_v240_compat.py  # v2.4.0 兼容版
├── config.py                 # 配置（可选，删除时走 fallback）
├── _meta.json                # 元数据
├── CHANGELOG.md              # 变更日志
├── SKILL.md                  # 使用文档
├── RELEASE_NOTES.md          # 发布说明
├── run_tests.sh              # 本地测试运行器
├── tests/
│   ├── test_extract_v243.py # 单元测试
│   ├── perf_test.py         # 性能基准
│   └── test_integration.py  # 集成测试
├── .github/workflows/test.yml
├── .pre-commit-config.yaml
├── releases/
│   └── v2.4.3_stable_20261018/
└── _backups_history/         # 历史备份
```

## 运行测试

```bash
bash run_tests.sh
```

或单跑：
```bash
python3 tests/test_extract_v243.py
python3 tests/perf_test.py
```

## 性能

- 单文件 38 张：1.59s（24 张/秒）
- 单文件 10 张：0.21s（48 张/秒）

## 依赖

```
pdfplumber>=3.0.0
openpyxl>=3.0.0
```

安装：`pip install -r requirements.txt`

## License

MIT
