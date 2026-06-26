---
name: multi-source-data-cleaner
description: |
  EN: Production-grade data cleaning across heterogeneous sources (CSV/Excel/JSON/Parquet/SQL dumps/log files). Profiles schemas, detects encoding/delimiter, normalizes types, handles missing values, deduplicates fuzzy records, reconciles schema across sources, and outputs a clean unified dataset plus a full data-quality report. Use when user provides one or more dirty datasets and asks "清洗数据 / 合并数据 / 去重 / 缺失值处理 / data cleaning / dedup / schema reconcile".
  中文：跨异构来源（CSV/Excel/JSON/Parquet/SQL 导出/日志文件）的工业级数据清洗。剖析 schema、自动识别编码与分隔符、归一化类型、处理缺失值、模糊去重、跨源字段对齐，输出统一的干净数据集与完整数据质量报告。当用户提供脏数据并要求"清洗/合并/去重/缺失值处理"时触发。
version: 1.0.0
metadata:
  openclaw:
    emoji: "🧹"
    homepage: https://github.com/openclaw-skills/multi-source-data-cleaner
    requires:
      bins:
        - python3
    envVars:
      - name: CLEANER_DEFAULT_ENCODING
        required: false
        description: Fallback encoding when auto-detection fails. Defaults to utf-8.
      - name: CLEANER_PII_POLICY
        required: false
        description: PII handling policy, one of `keep|mask|drop`. Defaults to `mask`.
---

# Multi-Source Data Cleaner · 多源数据清洗

> Drop a folder of CSVs, Excels, and JSONs from 5 different teams; get back a single clean table, a deduplication report, and a data-quality scorecard. No manual schema mapping required.
>
> 把 5 个部门各种格式的 CSV/Excel/JSON 一起扔进来，自动给你一张干净统一表、去重报告、数据质量评分。无需手工配字段映射。

---

## 🎯 When to Use · 何时使用

**Trigger keywords (中文):** 清洗数据、数据清洗、合并数据、去重、缺失值、字段对齐、schema 合并、数据质量、数据预处理、ETL

**Trigger keywords (EN):** clean data, data cleaning, deduplicate, missing values, schema reconcile, ETL, data quality, profile dataset

**Supported sources:**

| 格式 / Format | 说明 |
|---|---|
| CSV / TSV | Auto-detect encoding (UTF-8/GBK/BIG5), delimiter, quote char, header row |
| Excel (.xlsx/.xls/.xlsm) | Multi-sheet, merged cells, formula values |
| JSON / JSONL / NDJSON | Nested structures auto-flattened |
| Parquet / Feather | Native columnar reading |
| SQL dumps (.sql) | MySQL / PostgreSQL INSERT extraction |
| Log files | Pattern-detected structured lines |

**Do NOT use when:**
- Input is unstructured free text (use NLP extraction skills first)
- Input is binary/proprietary format with no parser (Adobe Indesign, custom CAD, etc.)
- User wants real-time streaming cleaning (this is batch-oriented)

---

## 📋 Cleaning Pipeline · 清洗流程

### Step 1: Source profiling · 源剖析

```bash
python3 scripts/profile.py --input <file-or-dir> --out profile.json
```

For each source produces:
- File format, encoding, line endings
- Schema (columns, inferred types, null rates, cardinality)
- Sample rows
- Quality flags: encoding mismatches, type inconsistencies, suspicious patterns

### Step 2: Type inference & normalization · 类型推断与归一

`scripts/normalize_types.py` standardizes:
- Numbers: thousands separators, scientific notation, currency symbols → numeric
- Dates: 50+ formats (`2024-03-15`, `2024/3/15`, `15 Mar 2024`, `民国113年3月15日`, Excel serial) → ISO 8601
- Booleans: `Y/N/是/否/0/1/true/false/T/F/✓/✗` → boolean
- Phone numbers: normalize to E.164
- Chinese names: full-width / half-width normalization
- IDs: zero-padding, prefix detection

### Step 3: Missing value handling · 缺失值处理

Per-column strategy (configurable in `templates/missing_strategy.json`):
- `drop_row` — drop rows where this column is null
- `mean|median|mode` — statistical imputation (with imputation flag column)
- `constant:<value>` — fill with literal
- `forward_fill` — for time-series
- `interpolate` — linear/spline for numeric series
- `keep_null` — preserve as null (default for unknown)

**Critical rule:** every imputed value gets a sidecar `<col>_imputed` boolean column so downstream analysis can distinguish original vs. imputed data.

### Step 4: Schema reconciliation · Schema 合并

`scripts/reconcile_schema.py` aligns columns across sources using:
- Exact name match
- Fuzzy match (Levenshtein + Chinese pinyin)
- Type compatibility check
- User-supplied mapping override (`--mapping mapping.yaml`)

Outputs a `crosswalk.json` documenting every column mapping for audit.

### Step 5: Fuzzy deduplication · 模糊去重

`scripts/dedup.py` uses configurable blocking + record linkage:
- Blocking keys to narrow candidates (e.g. first 3 chars of name + phone last 4)
- Similarity scoring: Jaro-Winkler for names, token-set for addresses, exact for IDs
- Threshold-based merge with conflict resolution rules (newest wins / longest non-null / authoritative source priority)

Reports merge groups for human review before commit.

### Step 6: PII handling · 隐私字段处理

Per `CLEANER_PII_POLICY`:
- `keep` — leave as-is (use only with explicit user authorization)
- `mask` — partial mask (`王*三`, `138****5678`, `4400****1234`)
- `drop` — remove column entirely

Auto-detection of common PII: 姓名、身份证号、手机号、邮箱、地址、银行卡号、IP、车牌号。

### Step 7: Data quality report · 数据质量报告

```bash
python3 scripts/quality_report.py --input cleaned.parquet --out dq_report.md
```

Six dimensions (per DAMA-DMBOK):
- Completeness (完整性)
- Accuracy (准确性, sample validation)
- Consistency (一致性, cross-column rules)
- Timeliness (时效性)
- Uniqueness (唯一性, dedup outcome)
- Validity (有效性, regex/range checks)

Each scored 0-100 with drill-down detail.

---

## 📤 Output Format · 输出格式

```
output/
├── cleaned.parquet              # main clean dataset (or .csv if requested)
├── crosswalk.json               # source → target schema mapping
├── dedup_groups.json            # merged record groups for review
├── dq_report.md                 # human-readable data quality report
├── dq_report.json               # machine-readable DQ metrics
├── audit/
│   ├── per_source_profile.json
│   ├── imputation_log.csv
│   └── pii_actions.log
└── provenance.csv               # row-level lineage: which source each row came from
```

---

## ⚠️ Safety & Compliance · 安全合规

1. **No silent data loss** — every drop/merge/impute action logged in `audit/`.
2. **Imputation flags mandatory** — imputed values marked so they cannot masquerade as originals.
3. **PII default mask** — unless user explicitly authorizes `keep`, PII is masked.
4. **Reversibility** — original sources never modified; cleaning is non-destructive.
5. **Dedup human-in-the-loop** — fuzzy merges above threshold but below 0.95 confidence flagged for review, not auto-committed.
6. **No external network calls** — all processing local; no data leaves the workspace.

> 不静默丢数据，所有删除/合并/填充均记录到 audit/；填充值带标志列防止假冒原值；隐私字段默认脱敏；原始文件不修改；模糊去重低置信度合并强制人工复核；不向外部上传任何数据。

---

## 🚀 Usage Examples · 使用示例

### Example 1: Clean a single messy CSV

```bash
python3 scripts/run_pipeline.py \
  --input sales_q1.csv \
  --output-dir ./cleaned_q1/ \
  --pii-policy mask
```

### Example 2: Merge 3 source CSVs into unified customer table

```bash
python3 scripts/run_pipeline.py \
  --input ./customer_sources/ \
  --output-dir ./unified_customers/ \
  --dedup-keys name,phone \
  --priority-source crm_export.csv
```

### Example 3: Schema reconcile with manual mapping override

```bash
python3 scripts/run_pipeline.py \
  --input ./multi_team_data/ \
  --mapping mapping.yaml \
  --output-dir ./unified/
```

`mapping.yaml`:
```yaml
target_schema:
  customer_id: { aliases: [客户ID, cust_id, ClientID, 编号] }
  phone:        { aliases: [手机, 联系电话, Mobile, tel] }
  signup_date:  { aliases: [注册日期, 开户日期, CreatedAt], type: date }
```

### Example 4: Quality scan only (read-only audit)

```bash
python3 scripts/profile.py --input ./suspicious_dataset/ --out dq_audit.md --read-only
```

---

## 🧪 Testing · 测试

```bash
cd tests && python3 -m pytest -v
```

Fixtures include:
- Encoding test set (UTF-8 BOM, GBK, BIG5, Latin1)
- 12 date format variants
- Schema-drift simulation across 5 source files
- Synthetic dedup dataset (10k records with controlled duplication)
- PII regression suite

---

## 📚 References · 参考资料

- DAMA-DMBOK Data Quality dimensions
- Fellegi-Sunter probabilistic record linkage
- Jaro-Winkler distance for fuzzy match
- `pandas`, `pyarrow`, `recordlinkage` library docs

## 🏷️ Tags · 标签

`data` `ETL` `data-cleaning` `dedup` `schema-reconcile` `data-quality` `数据清洗` `多源整合` `去重` `数据质量`
