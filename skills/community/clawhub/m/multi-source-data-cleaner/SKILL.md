# SKILL.md — 多源数据清洗器

## Metadata

| 字段 | 值 |
|------|-----|
| name | multi-source-data-cleaner |
| label | 多源数据清洗器 |
| version | 1.0.0 |
| language | Python |
| runtime | subprocess (scripts/main.py) |
| trigger_words | 数据清洗、数据去重、表格整理、数据合并、格式统一、CRM数据整理、Excel清洗 |

---

## Description

上传乱数据，输出干净数据。支持多格式解析、智能字段识别、AI去重/补全/格式化、多源关联合并，飞书原生输出（多维表格+云文档质量报告）。

**适用场景：** 电商订单整理、CRM客户数据清洗、银行流水整理、花名册整理、多系统数据合并。

---

## Capabilities

### F1 · 多格式识别与解析
- Excel (.xlsx / .xls)
- CSV / TSV
- JSON（半结构化）
- 剪贴板粘贴文本

### F2 · 智能字段识别
- AI 自动识别：姓名、手机号、邮箱、地址、金额、日期、SKU、订单号、身份证、性别等
- 支持用户自定义字段映射覆盖

### F3 · 数据清洗
- **去重**：精确去重 + 智能模糊去重（FuzzyWuzzy，阈值 88%）
- **补全**：均值/众数/语义推断/留空
- **格式统一**：
  - 手机号 → `1xx-xxxx-xxxx`
  - 日期 → `YYYY-MM-DD`
  - 金额 → 两位小数
  - 地址 → 省市区街道标准化

### F4 · 数据分类/打标签（专业版）
- 内置 8 种业务规则（高价值客户、沉睡用户、VIP客户、企业客户等）
- 支持自定义 JSON 规则
- AI 自动打标签（需要专业版 + AI API Key）

### F5 · 多源关联合并（专业版）
- 按手机号/姓名/订单号等跨文件关联
- Fuzzy Join（模糊匹配阈值可调）
- 支持 2+ 文件迭代合并

### F6 · 飞书原生输出
- 导出干净 Excel / CSV
- **飞书多维表格**（标准版/专业版）：直接写入 Bitable
- **数据质量报告 → 飞书云文档**：重复率/缺失率/清洗前后对比

---

## Pricing / Tier Features

| 功能 | 免费版 | 基础版 | 标准版 | 专业版 |
|------|--------|--------|--------|--------|
| 月额度 | 50条 | 500条 | 3000条 | 不限 |
| 数据源数 | 1 | 3 | 不限 | 不限 |
| 最大列数 | 10 | 50 | 200 | 不限 |
| 多格式解析 | ❌ | ✅ | ✅ | ✅ |
| 基础去重 | ✅ | ✅ | ✅ | ✅ |
| 智能模糊去重 | ❌ | ❌ | ✅ | ✅ |
| 格式统一 | ❌ | ❌ | ✅ | ✅ |
| 智能补全 | ❌ | ❌ | ✅ | ✅ |
| 多源合并 | ❌ | ❌ | ❌ | ✅ |
| AI分类/打标签 | ❌ | ❌ | ❌ | ✅ |
| 数据质量报告 | ❌ | ❌ | ❌ | ✅ |
| 飞书多维表格 | ❌ | ❌ | ❌ | ✅ |

**权限隔离实现：** `scripts/tier_limits.py` — 所有操作入口均调用 `check_tier()` / `check_feature()` 验证。

---

## Invocation

### Agent 直接调用

```
from main import run_clean_pipeline, run_merge_pipeline

# 基本清洗
result = run_clean_pipeline(
    sources=["订单数据.xlsx"],
    texts=None,
    output_format="xlsx",
    output_path="/tmp/cleaned.xlsx",
    dedup_strategy="auto",
    fill_strategy="auto",
    classify=True,
    ai_model="deepseek",
    generate_report=True,
)

# 多源合并
merge_result = run_merge_pipeline(
    sources=["客户表.xlsx", "订单表.csv"],
    on=["手机号"],
    fuzzy_on=["姓名"],
    fuzzy_threshold=85,
    output_format="xlsx",
)
```

### CLI 调用

```bash
# 清洗本地文件
python scripts/main.py clean -i data.xlsx -o cleaned.xlsx -f xlsx

# 粘贴文本数据
python scripts/main.py clean -t "姓名,电话
张三,13800138000
李四,13900139000" -o cleaned.csv -f csv

# 多源合并
python scripts/main.py merge --sources data1.csv data2.csv --on 手机号 -o merged.xlsx

# 生成质量报告
python scripts/main.py clean -i cleaned.xlsx --report-title "清洗报告" -o report.md
```

---

## Function Reference

### `run_clean_pipeline()`

**参数：**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `sources` | `List[str]` | `None` | 文件路径列表 |
| `texts` | `List[str]` | `None` | 粘贴文本列表 |
| `tier` | `str` | `None` | free/basic/std/pro |
| `output_format` | `str` | `"xlsx"` | xlsx 或 csv |
| `output_path` | `str` | `None` | 输出路径（自动生成临时文件） |
| `custom_field_mapping` | `Dict[str,str]` | `None` | {列名: 类型} 覆盖 |
| `dedup_strategy` | `str` | `"auto"` | exact / fuzzy / auto |
| `fill_strategy` | `str` | `"auto"` | auto / mean / mode / leave_blank |
| `classify` | `bool` | `False` | 是否启用 AI 分类 |
| `ai_model` | `str` | `None` | minimax / deepseek |
| `generate_report` | `bool` | `True` | 是否生成质量报告 |
| `bitable_output` | `bool` | `False` | 输出到飞书多维表格 |
| `feishu_folder_token` | `str` | `None` | 飞书文件夹 token |
| `report_title` | `str` | `"数据质量报告"` | 报告文档标题 |

**返回：** `Dict` 含 `file_path`, `cleaned_rows`, `clean_report`, `usage`, `report_md`, `bitable`, `doc` 等。

---

## Environment Variables

| 变量 | 必填 | 说明 |
|------|------|------|
| `DATA_CLEANER_API_KEY` | AI 功能需填写 | MiniMax 或 DeepSeek API Key |
| `DATA_CLEANER_TIER` | 推荐填写 | 订阅版本（free/basic/std/pro），默认 free |
| `DATA_CLEANER_STATE_FILE` | 可选 | 月度用量记录文件路径 |

---

## Dependencies

```
pandas>=1.5
openpyxl>=3.0
xlrd>=2.0
fuzzywuzzy>=0.18
python-Levenshtein>=0.12
```

安装：`pip install pandas openpyxl xlrd fuzzywuzzy python-Levenshtein`

---

## Error Handling

| 异常 | 说明 | 用户提示 |
|------|------|---------|
| `TierLimitExceeded` | 超出月度额度或数据源数限制 | 提示升级版本 |
| `FeatureNotAvailable` | 当前版本不支持该功能 | 提示解锁方式 |
| `MergeError` | 合并失败（键不匹配等） | 提示检查关联键 |
| `ExportError` | 导出失败（APIKey等） | 提示配置方式 |

---

## Notes

- 所有 DataFrame 操作使用 `dtype=str` + `keep_default_na=False`，避免意外类型转换
- 日期解析支持：`YYYY-MM-DD`、`YYYY/MM/DD`、`YYYY年MM月DD日`、`YYYYMMDD`、Unix时间戳
- 手机号格式统一：自动识别 11 位中国手机号并格式化为 `1xx-xxxx-xxxx`
- 模糊去重阈值默认 88%（FuzzyWuzzy ratio），可在 `run_merge_pipeline` 中通过 `fuzzy_threshold` 参数调整
- 月度用量在 `/tmp/data_cleaner_state.json` 中持久化，重启后保留
- 飞书 Bitable 输出每批最多 500 条，超出自动分批写入

---

## Skill Author

技能开发者 · YK Global
