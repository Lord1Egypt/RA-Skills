---
name: Mysteel_PriceSearch
description: 大宗商品价格数据查询技能。用于查询大宗商品期现货价格、宏观经济指标、产业链供需数据、进出口库存数据、金融市场数据等。当用户询问：(1) 期货/现货价格查询，如"螺纹钢价格"、"铜期货收盘价"； (2) 历史行情或趋势分析；(3) 区域或企业价格对比；(4) 宏观经济指标，如GDP、CPI；(5) 产业链上下游数据；(6) 多市场金融数据（期权、股票、债券、外汇）；(7) 结算确认单生成时触发此技能。
dependency:
  python:
    - 内置模块 (urllib, json, os, sys, re, argparse, datetime, pathlib)
---

# Mysteel Price Search

大宗商品与宏观经济数据综合查询技能，基于Mysteel数据平台提供专业、全面的价格数据服务。

## Quick Start

使用 `scripts/search.py` 脚本查询价格数据：

```bash
python scripts/search.py "<查询文本>"
```

## CSV 输出模式（推荐）

将查询结果保存为 CSV 文件，**强烈建议使用过滤参数减少数据量**：

### 基本用法
```bash
python scripts/search.py "螺纹钢最新价格" --csv
```

### 数据过滤参数（重要！）

为避免 LLM 读取过多数据，**请根据需要使用以下参数**：

| 参数 | 说明 | 示例 |
|------|------|------|
| `--limit N` | 限制每个文件最多 N 行数据 | `--limit 10` |
| `--days N` | 仅查询最近 N 天的数据 | `--days 30` |
| `--start-date` | 起始日期（含） | `--start-date 2024-01-01` |
| `--end-date` | 结束日期（含） | `--end-date 2024-01-31` |

### 推荐使用示例

```bash
# 查询最新10条价格（最常用）
python scripts/search.py "螺纹钢最新价格" --csv --limit 10

# 查询最近30天价格
python scripts/search.py "铜期货价格" --csv --days 30

# 查询特定日期范围
python scripts/search.py "热卷价格" --csv --start-date 2024-01-01 --end-date 2024-03-31
```

## 读取已有 CSV 文件

**不要使用 Read 工具读取整个 CSV 文件！** 使用 Bash 工具按需读取：

```bash
# 查看文件元数据（了解数据概况）
head -10 output/螺纹钢.csv

# 仅读取前N行数据
head -20 output/螺纹钢.csv | tail -n +10

# 按日期过滤（使用 grep）
grep -E "^2024-01" output/螺纹钢.csv

# 查看文件统计信息
wc -l output/螺纹钢.csv
```

## CSV 文件格式

CSV 文件包含元数据头注释，格式如下：

```
# index_name: 螺纹钢_上海_HRB400E
# unit: 元/吨
# total_rows: 365
# date_range: 2023-01-15 ~ 2024-01-15
# generated: 2024-01-15 10:30:00
#
date,price,unit,change,change_pct
2024-01-15,3800,元/吨,+20.00,+0.53%
2024-01-14,3780,元/吨,-10.00,-0.26%
```

## 输出示例

```
Generated 2 CSV file(s) in output:
  - 螺纹钢_上海_HRB400E.csv (10 rows, 2024-01-05 ~ 2024-01-15)
  - 热卷_上海_Q235B.csv (10 rows, 2024-01-05 ~ 2024-01-15)
```

## 完整参数列表

- `--csv`: 保存结果为 CSV 文件到 output 目录
- `--output-dir`: 指定 CSV 输出目录（默认：技能目录/output）
- `--limit N`: 限制每个文件最多 N 行数据
- `--days N`: 仅查询最近 N 天的数据
- `--start-date YYYY-MM-DD`: 起始日期过滤
- `--end-date YYYY-MM-DD`: 结束日期过滤
- `--max-files N`: 限制 output 目录最多保留 N 个 CSV 文件（默认：100），超过时删除最旧的文件

## Query Capabilities

### 1. 价格数据查询
- **期货价格**：最新收盘价、结算价、涨跌幅
- **现货价格**：实时报价、区域价格、企业报价
- **历史数据**：趋势分析、周期对比

### 2. 宏观经济数据
- 全球宏观经济主要指标
- 分国别/地区数据查询
- GDP、CPI、PMI等指标

### 3. 产业链数据
- 上游原材料价格
- 下游产品价格
- 供需平衡数据
- 进出口数据
- 库存数据

### 4. 金融市场数据
- 期权价格与隐含波动率
- 股票行情
- 债券收益率
- 外汇汇率

### 5. 智能分析
- 类目识别与指标识别
- 多维度数据对比
- 口径标准化
- 差值计算

### 6. 结算凭证
- 支持贸易双方成交数量输入

## API Reference

详细API文档参见 [api_reference.md](references/api_reference.md)。

## Response Handling

API返回JSON格式数据，主要包含：

1. **价格数据**：数值、单位、涨跌幅、时间戳
2. **图表数据**：支持历史趋势图表
3. **对比数据**：多维度价格对比

## Best Practices

1. **查询表达**：使用自然语言描述查询需求，API支持智能语义解析
2. **数据对比**：可同时查询多个品种或区域进行对比分析
3. **历史溯源**：支持基于时间范围的查询，获取历史趋势

## 回复格式
需要详细标明数据所引用的指标（indexName）