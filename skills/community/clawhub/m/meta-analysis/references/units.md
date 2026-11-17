# Units / 原子任务单元索引 (meta-analysis)

> Per ct-base §6 schema: each unit has 5 fields (input / output / dependency / AI autonomy / consumer units). This index enables downstream pipeline composition (e.g., systematic-review workflow chains meta → TLF).

---

## Level 1 — Entry Units (standalone, no prerequisites)

| Unit ID | Name | Input | Output | AI Autonomy | Consumers |
|---------|------|-------|--------|-------------|-----------|
| `u_pairwise` | Pairwise Meta / 两组Meta | Summary data (2×2 tables for binary, M/SD/N for continuous, pre-calculated yi+SE, HR, r) | `rma` / `metabin` object + forest/funnel SVG + results table | ⬛ Full-auto | `u_heterogeneity`, `u_pubbias`, `u_sensitivity` |
| `u_effect_size` | Effect Size Conversion / 效应量转换 | Raw stats (M/SD/N, t/F/r, OR/RR, d) | Converted effect size + SE | ⬛ Full-auto | `u_pairwise`, `u_batch` |
| `u_network` | Network Meta / 网络Meta | Arm-level data + treatment labels | `netmeta` / `gemtc` (multinma 可选) object + league table + SUCRA | ⬛ Full-auto | `u_nma_consistency` |
| `u_single_group` | Single-Group Meta / 单组率均值 | Counts or means from single-arm studies | Pooled proportion / mean / incidence / correlation | ⬛ Full-auto | — |
| `u_diagnostic` | Diagnostic Meta / 诊断准确性 | TP/FP/FN/SN tables | `mada::reitsma` bivariate model + SROC curve | ⬛ Full-auto | — |
| `u_survival` | Survival Meta / 生存Meta | HR + CI (or KM curves for pseudo-IPD) | Pooled HR + KM reconstruction | 🟨 Semi-auto (confirm HR extraction method) | — |
| `u_tsa` | Trial Sequential Analysis / 试验序贯分析 | Accumulated trial data + alpha + beta | TSA boundaries + required info size | ⬛ Full-auto | — |

---

## Level 2 — Diagnostic & Subsidiary Units (consume Level 1)

| Unit ID | Name | Input | Output | AI Autonomy | Consumers |
|---------|------|-------|--------|-------------|-----------|
| `u_heterogeneity` | Heterogeneity / 异质性 | `rma` / `metabin` object | I² / Q / τ² / H² / PI + subgroup analysis or meta-regression | ⬛ Full-auto | `u_pubbias` |
| `u_pubbias` | Publication Bias / 发表偏倚 | `rma` object | Egger / Begg / Trim-fill / selection model | ⬛ Full-auto | — |
| `u_sensitivity` | Sensitivity / 敏感性 | `rma` object | Leave-one-out / cumulative / GOSH | ⬛ Full-auto | — |
| `u_nma_consistency` | NMA Consistency / 一致性 | `netmeta` / `gemtc` object | Node-split test + inconsistency heatmap | ⬛ Full-auto | — |
| `u_power` | Power Analysis / 功效 | Effect size + sample size info | Prospective sample-size planning + power curve | ⬛ Full-auto | — |
| `u_rob` | Risk of Bias / 偏倚风险 | Study-level judgments | RoB 1.0 / 2.0 / ROBINS-I traffic-light + weighted bar | 🟨 Semi-auto (user confirms judgments) | — |
| `u_quality` | Evidence Quality / 证据质量 | PICO + RoB + results | GRADE assessment | 🟨 Semi-auto (user confirms) | — |

---

## Level 3 — Reporting & Workflow Units

| Unit ID | Name | Input | Output | AI Autonomy | Consumers |
|---------|------|-------|--------|-------------|-----------|
| `u_report` | Report Generation / 报告生成 | All analysis objects + results tables | `results_summary.md` + R Markdown + HTML | ⬛ Full-auto | — |
| `u_prisma` | PRISMA Flow / 流程图 | Screening counts (records / screened / included) | PRISMA flow diagram SVG | ⬛ Full-auto | `u_report` |
| `u_screening` | Screening / 筛选 | PDF batch + criteria | Included/excluded lists | ⬜ Assisted (user reviews) | `u_prisma` |
| `u_data_convert` | Data Conversion / 数据转换 | External files (SPSS/Stata/SAS/Excel/Parquet) | Standard CSV columns for meta | ⬛ Full-auto | `u_pairwise`, `u_network` |
| `u_batch` | Batch Effect Size / 批量效应量 | Raw study data (multiple at once) | Standardized yi + SE table | ⬛ Full-auto | `u_pairwise` |

---

## Composition Patterns / 组合模式

| Pattern | Chain | Use Case |
|---------|-------|----------|
| Standard pairwise meta | `u_data_convert` → `u_pairwise` → `u_heterogeneity` → `u_pubbias` → `u_sensitivity` → `u_report` | Most common |
| Network meta | `u_data_convert` → `u_network` → `u_nma_consistency` → `u_report` | Multiple interventions |
| Systematic review | `u_screening` → `u_prisma` → (meta units) → `u_quality` → `u_report` | Full review |
| Quick effect size check | `u_effect_size` → `u_pairwise` (preview only) | Preliminary |
