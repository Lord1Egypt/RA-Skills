# Multi-Source Data Cleaner · 多源数据清洗

[English](#english) | [中文](#chinese)

---

## English

Production-grade data cleaning across heterogeneous sources (CSV/Excel/JSON/Parquet/SQL/logs) with profiling, schema reconciliation, fuzzy dedup and DAMA-DMBOK data quality reporting.

### Quick Start

```bash
python3 scripts/run_pipeline.py \
  --input ./mixed_sources/ --output-dir ./cleaned/ \
  --dedup-keys name,phone --pii-policy mask
```

### Features

- 🧹 Auto-detect encoding (UTF-8/GBK/BIG5), delimiter, header
- 🔄 Type normalization: 50+ date formats, numbers, booleans, phones
- 🎯 Fuzzy dedup with blocking + record linkage
- 🔗 Schema reconcile across sources (fuzzy + pinyin)
- 🔒 PII auto-detect and mask by default
- 📊 DAMA-DMBOK 6-dimension quality scorecard
- 📝 Full audit trail (impute log, dedup groups, provenance)

### License

MIT-0

---

## Chinese

跨异构源（CSV/Excel/JSON/Parquet/SQL/日志）的工业级数据清洗：剖析、schema 对齐、模糊去重、DAMA-DMBOK 数据质量评分。

### 快速开始

```bash
python3 scripts/run_pipeline.py \
  --input ./多源数据/ --output-dir ./清洗后/ \
  --dedup-keys 姓名,手机 --pii-policy mask
```

### 功能

- 🧹 自动识别编码（UTF-8/GBK/BIG5）、分隔符、表头
- 🔄 类型归一：50+ 日期格式、数字、布尔、手机号
- 🎯 模糊去重：blocking + 记录关联
- 🔗 跨源 schema 对齐（模糊 + 拼音）
- 🔒 PII 自动识别并默认脱敏
- 📊 DAMA-DMBOK 六维度数据质量评分
- 📝 完整审计轨迹（填充日志、去重组、行级溯源）

### 协议

MIT-0
