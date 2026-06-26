# 多源数据清洗器 · Multi-Source Data Cleanser

> 上传乱数据，输出干净数据。

[![版本](https://img.shields.io/badge/version-1.0.0-blue)](#)
[![语言](https://img.shields.io/badge/language-Python-green)](#)
[![平台](https://img.shields.io/badge/平台-飞书%20妙搭-cyan)](#)

---

## 🎯 产品定位

电商、财务、运营、客服等岗位每天都在和"脏数据"打交道——Excel 格式不统一、CRM 导出的数据缺胳膊少腿、跨平台客户信息重复又分散。

**多源数据清洗器**让用户把原始数据一股脑丢进去，AI 自动识别格式、清洗、归类、合并，输出可直接使用的干净数据集。

---

## ✨ 核心功能

| 编号 | 功能 | 说明 |
|------|------|------|
| F1 | 多格式识别与解析 | Excel / CSV / TSV / JSON / 剪贴板粘贴 |
| F2 | 智能字段识别 | AI 自动识别姓名/电话/邮箱/金额/日期等字段 |
| F3 | 数据清洗 | 智能去重 + 缺失值填补 + 格式统一 |
| F4 | 数据分类/打标签 | 内置规则 + AI 自动打标签（专业版） |
| F5 | 多源数据关联合并 | 跨文件关联 + Fuzzy Join（专业版） |
| F6 | 飞书原生输出 | Excel/CSV + 多维表格 + 数据质量报告文档 |

---

## 📋 版本与定价

| 版本 | 价格 | 月额度 | 数据源 | 主要功能 |
|------|------|--------|--------|---------|
| 免费版 | ¥0 | 50 条 | 1 个 | 基础去重、CSV/XLSX |
| 基础版 | ¥9.9/月 | 500 条 | 3 个 | 多格式解析、基础去重 |
| 标准版 | ¥29/月 | 3000 条 | 不限 | 智能补全、格式统一、模糊去重 |
| 专业版 | ¥69/月 | 不限 | 不限 | 多源合并、AI分类、质量报告、飞书多维表格 |

---

## 🚀 快速开始

### 方式一：飞书对话触发

```
数据清洗
数据去重
表格整理
CRM数据整理
Excel清洗
```

### 方式二：CLI 快速使用

```bash
# 安装依赖
pip install pandas openpyxl xlrd fuzzywuzzy python-Levenshtein

# 清洗 Excel 文件
python scripts/main.py clean -i data.xlsx -o cleaned.xlsx

# 粘贴文本数据
python scripts/main.py clean -t "姓名,电话\n张三,13800138000" -f csv -o cleaned.csv

# 多源合并
python scripts/main.py merge --sources customers.xlsx orders.csv --on 手机号 -o merged.xlsx
```

### 方式三：Python 代码调用

```python
from main import run_clean_pipeline

result = run_clean_pipeline(
    sources=["订单.xlsx"],
    output_format="xlsx",
    output_path="/tmp/cleaned.xlsx",
    dedup_strategy="auto",
    fill_strategy="auto",
    classify=True,
    ai_model="deepseek",
    generate_report=True,
)

print(f"清洗完成！输出文件：{result['file_path']}")
print(f"清洗后行数：{result['cleaned_rows']}")
print(f"数据质量评分：{result['report_dict']['overall_score']}")
```

---

## 📊 数据质量报告示例

清洗完成后自动生成 Markdown 格式的质量报告，包含：

- **综合质量评分**（0-100）
- **数据规模变化**（清洗前后行/列数对比）
- **重复率 / 缺失率变化**
- **清洗详情**（去重数、补全数、格式化单元格数）
- **字段质量详情表**（每列缺失率、唯一值数、示例值）
- **优化建议**（AI 自动生成）

报告可直接创建为飞书云文档，一键分享给团队。

---

## 🗂️ 目录结构

```
multi-source-data-cleaner/
├── SKILL.md                    # Skill 定义（触发词、参数、说明）
├── README.md                   # 本文件
├── scripts/
│   ├── __init__.py
│   ├── main.py                 # 入口脚本（run_clean_pipeline / run_merge_pipeline）
│   ├── parser.py               # F1：多格式解析
│   ├── field_identifier.py     # F2：AI 字段识别
│   ├── cleaner.py              # F3：清洗引擎（去重/补全/格式化）
│   ├── classifier.py          # F4：数据分类/打标签
│   ├── merger.py               # F5：多源关联合并
│   ├── reporter.py            # F6：数据质量报告生成
│   ├── output.py               # F6：输出（Excel/CSV/Bitable/飞书文档）
│   └── tier_limits.py         # 版本权限控制
└── tests/
    ├── test_parser.py
    ├── test_cleaner.py
    └── test_field_identifier.py
```

---

## 🔧 配置说明

### 环境变量

| 变量 | 必填 | 说明 |
|------|------|------|
| `DATA_CLEANER_API_KEY` | AI 功能需填写 | MiniMax 或 DeepSeek API Key |
| `DATA_CLEANER_TIER` | 推荐填写 | 订阅版本（free/basic/std/pro） |

### AI API Key 申请

**MiniMax：** https://platform.minimax.chat/
**DeepSeek：** https://platform.deepseek.com/

将 Key 配置到环境变量后，AI 字段识别和智能分类功能即可使用。

---

## 🧪 测试

```bash
cd tests
pytest test_parser.py -v
pytest test_cleaner.py -v
```

---

## ⚠️ 注意事项

1. **数据安全**：所有数据处理在本地/Python 进程内完成，不会上传到第三方服务器
2. **编码**：CSV 文件优先使用 UTF-8，GBK 编码自动兼容
3. **日期格式**：支持 `YYYY-MM-DD`、`YYYY/MM/DD`、`YYYY年MM月DD日`、`YYYYMMDD`、Unix 时间戳
4. **手机号**：自动识别 11 位中国手机号并格式化为 `1xx-xxxx-xxxx`
5. **月度额度**：用量记录在 `/tmp/data_cleaner_state.json`，支持手动清理

---

## 🔄 更新日志

### v1.0.0（2026-04-19）
- 初始版本发布
- 支持 F1-F6 全部核心功能
- 4 档订阅版本完整实现

---

## 📞 反馈与支持

如遇问题或功能建议，请联系技能开发者。
