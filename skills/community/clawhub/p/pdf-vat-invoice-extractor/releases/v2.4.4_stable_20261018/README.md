# pdf-invoice-stat

**PDF 增值税发票提取 Skill · v2.4.3（稳定版）**

## 这是什么

从 PDF 格式的增值税电子发票中自动提取关键字段（发票号、日期、购销方、金额、税额、价税合计），输出 15 列 Excel 报表。

## 版本

```python
from version import __version__  # "2.4.3"
```

- **当前状态**: 稳定版（推荐生产使用）
- **发布日期**: 2026-10-18
- **测试覆盖**: 48 张真实发票（100% 字段完整度）

## 快速使用

```python
import sys
sys.path.insert(0, '/path/to/pdf-invoice-stat')
from invoice_extractor import extract_all_invoices, create_excel

# 1. 识别发票
invoices = extract_all_invoices('invoices.pdf')
# invoices 是字典列表，每个字典是一张发票

# 2. 输出 Excel
create_excel(invoices, duplicate_rows=[], output_path='output.xlsx')
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

## 不支持（本目录范围外）

| 不支持 | 备注 |
|--------|------|
| XML（数电票/全电发票）| 另一 SKU |
| OFD（国标版式发票）| 另一 SKU |

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
