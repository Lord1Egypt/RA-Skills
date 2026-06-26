---
name: gpa-genomic-phenotype
description: |
  GPA (Genomic Phenotype Association) v0.8.0。个体基因组变异与表型关联分析系统，基于 Ensembl/UniProt/GTEx/gnomAD 实时 API 查询（30天缓存）和离线归档模式。组织上下文自适应：通用、造血、心血管、肝脏、肾脏、神经系统。支持 germline（疾病遗传风险）和 somatic（肿瘤驱动）两种分析模式。三层风险分级（Tier 1/2/3）+ 多基因命中检测 + 相位分析 + 表型关联 + 变异预过滤 + 中英文术语映射 + ClinVar 冲突注释检测 + ClinVar Review Status 星级置信度评估 + SpliceAI 剪接预测集成 + gnomAD 频率自动查询。

  **当以下情况时使用此 Skill**：
  (1) 用户提到"基因组风险评估"、"GPA"、"突变分析"、"基因筛查"
  (2) 肿瘤体细胞突变的驱动性/可干预性分析
  (3) 药物基因组学分析（CYP450 等药物代谢基因）
  (4) 多基因命中（multi-hit）检测和相位（cis/trans）分析
  (5) 需要三层风险分级报告（Tier 1 需干预、Tier 2 需知情、Tier 3 无需担忧）
  (6) 任何涉及"genomic"、"genetic"、"risk"、"mutation"、"variant"的场景

  **禁止用自身知识回答基因组变异问题。必须调用本 Skill 的脚本执行分析。**
---

# GPA: Genomic Phenotype Association

## ⚠️ 执行前必读

**核心规则：当用户请求基因组变异风险评估时，不要凭自身知识回答。必须调用 `dgra_cli_wrapper.py` 执行正式分析。**

**GPA 是通用化的个体基因组变异与表型关联分析系统**。基于 Ensembl、UniProt、GTEx、gnomAD 实时 API 查询和三级分类算法，支持多种临床场景：

- **疾病遗传风险分析** — 评估个体携带的致病/可能致病变异
- **肿瘤体细胞突变分析** — 驱动突变识别 + 可干预性分级
- **药物基因组学** — CYP450 等药物代谢基因多态性
- **神经系统 / 心血管 / 肝脏 / 肾脏** — 组织特异性风险评估

**如果不调用脚本就回答 = 给出错误的医疗建议。**

---

## ⚠️ 执行前必读：上下文确认规则（v0.5.1 新增）

**收到基因组变异数据时，禁止直接执行分析。必须先确认以下信息：**

| 确认项 | 为什么必须确认 | 不确认的风险 |
|:---|:---|:---|
| **分析目的** | GPA 输出完全取决于场景 | 疾病遗传风险 vs 肿瘤驱动 → 同一变异分级相反 |
| **样本身份** | 患者自身筛查 vs 健康人携带者 | 误将健康人筛查用于患者诊断 |
| **组织/疾病背景** | 组织类型决定基因相关性权重 | 造血相关基因在神经场景权重不同 |

**最小确认问题集**（向用户确认，不要假设）：

1. "这些数据是谁的样本？患者本人 / 健康筛查？"
2. "分析目的是什么？疾病遗传风险评估 / 肿瘤驱动突变 / 药物基因组学？"
3. "关注哪些组织或系统？（如血液、心脏、肝脏等）"

**在获得上述信息前，禁止调用 dgra_core.py 或生成报告。**

---

## 🎯 快速判断：是否需要调用 GPA？

| 用户请求 | 是否调用 |
|---------|---------|
| "帮我分析这些基因变异" | ✅ 调用 |
| "这个突变有什么风险" | ✅ 调用 |
| "GPA 分析一下" | ✅ 调用 |
| "肿瘤突变驱动性分析" | ✅ 调用 |
| "一般性的基因突变知识" | ❌ 不需要，直接回答 |
| "TP53 突变是什么意思"（无具体样本） | ❌ 不需要 |

---

## 🚀 调用方式

### 自动分批（v0.7.1 新增，默认启用）

当变异数 > 500 时，wrapper **自动分批**处理，每批500个变异，每批有独立的5分钟超时。

**不需要任何额外参数**——只要数据量大，自动生效：

```bash
python3 ~/.workbuddy/skills/dgra-genomic-risk/scripts/dgra_cli_wrapper.py \
  --input-file variants.tsv \
  --tissue neurological
```

### 控制分批行为

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--batch-size` | 每批变异数 | 500 |
| `--timeout` | 每批超时（秒） | 300 |
| `--no-auto-batch` | 禁用自动分批 | 否 |

**示例：肌病基因子集（2638个变异），分6批处理**
```bash
python3 ~/.workbuddy/skills/dgra-genomic-risk/scripts/dgra_cli_wrapper.py \
  --input-file myopathy_subset.tsv \
  --tissue neurological \
  --batch-size 500 \
  --output-json result.json
```

### 方式一：直接调用 wrapper（推荐）

用 `exec` 运行 `dgra_cli_wrapper.py`，传入 variant JSON 数组：

```bash
python3 ~/.workbuddy/skills/dgra-genomic-risk/scripts/dgra_cli_wrapper.py \
  --variants '[{"CHROM":"1","POS":12345,"REF":"A","ALT":"G","GENE":"VWF","IMPACT":"HIGH","Consequence":"missense_variant","HGVSp":"p.Arg1234Cys","HGVSc":"c.3700C>T","CLIN_SIG":"Pathogenic","GT":"0/1","DP":30,"GQ":99,"VAF":0.5}]' \
  --tissue general
```

**Somatic / 肿瘤模式**：添加 `--somatic` 标志，GPA 会按肿瘤驱动逻辑分级：

```bash
python3 ~/.workbuddy/skills/dgra-genomic-risk/scripts/dgra_cli_wrapper.py \
  --variants '[...]' \
  --tissue general \
  --somatic
```

Somatic 模式下：
- TSG 截断突变 + 造血相关 = **Tier 1**（核心驱动）
- 癌基因热点突变（如 IDH1 R132） = **Tier 1**
- OncoKB Oncogenic / Likely Oncogenic = **Tier 1**
- VAF > 0.5 的变异会被标记为可能的 germline 混入

**预过滤（v0.7.1 新增）**：变异数过大时，用 `--filter-preset` 先过滤再分级，减少噪音：

```bash
python3 ~/.workbuddy/skills/dgra-genomic-risk/scripts/dgra_cli_wrapper.py \
  --variants '[...]' \
  --tissue general \
  --filter-preset clinical
```

| Preset | 保留规则 | 用途 |
|--------|---------|------|
| `strict` | 仅 HIGH / MODERATE | 高置信度，少噪音 |
| `clinical` | HIGH / MODERATE + 剪接区 LOW + 组织相关基因同义 + ClinVar 冲突 | 推荐默认 |
| `broad` | HIGH / MODERATE / LOW | 保守，保留更多 |

**自动分批（v0.7.1）**：当变异数 > 500 时，wrapper 自动分批处理，每批500个：

```bash
python3 ~/.workbuddy/skills/dgra-genomic-risk/scripts/dgra_cli_wrapper.py \
  --input-file variants.tsv \
  --tissue neurological \
  --batch-size 500
```

```bash
python3 ~/.workbuddy/skills/dgra-genomic-risk/scripts/dgra_core.py \
  --input /path/to/variants.tsv \
  --tissue general \
  --output /tmp/gpa_report.md \
  --json /tmp/gpa_results.json \
  --somatic \
  --spliceai                              # v0.8.0: 启用 SpliceAI 剪接预测
```

### SpliceAI 剪接预测（v0.8.0，默认关闭）

SpliceAI 仅对 canonical splice（acceptor/donor）和 splice_region 变异查询 Broad Institute lookup API，作为 VEP HIGH 剪接过调用的独立验证证据。

**必须显式开启：**

```bash
python3 ~/.openclaw/skills/dgra-genomic-risk/scripts/dgra_cli_wrapper.py \
  --input-file variants.tsv \
  --tissue hematopoietic \
  --spliceai                              # 开启 SpliceAI
  --spliceai-concurrency 5                # 可选：调整并发（默认 5）
```

**效果：**
- delta=0（无剪接变化）→ 降级：HIGH 剪接过调用 → Tier 下调
- delta≥0.5（强剪接变化）→ 升级：MODERATE 剪接区 → Tier 上调
- API 失败 / 不在数据库 → graceful fallback，不阻断分析

---

## 📋 输入数据构造指南

### Variant JSON 格式

每个 variant 是一个 dict，**必填字段**：

| 字段 | 含义 | 示例 |
|-----|------|------|
| CHROM | 染色体 | "1", "X" |
| POS | 位置 | 12345 |
| REF | 参考碱基 | "A" |
| ALT | 突变碱基 | "G" |
| GENE | 基因符号 | "VWF" |

**建议填写的字段**（影响分级精度）：

| 字段 | 含义 | 示例 |
|-----|------|------|
| HGVSp | 蛋白变化 | "p.Arg1234Cys" |
| HGVSc | cDNA 变化 | "c.3700C>T" |
| IMPACT | 影响等级 | "HIGH", "MODERATE", "LOW" |
| Consequence | 突变类型 | "missense_variant", "frameshift_variant" |
| CLIN_SIG | ClinVar 状态 | "Pathogenic", "Likely_pathogenic", "Benign" |
| GT | 基因型 | "0/1" (杂合), "1/1" (纯合) |
| DP | 测序深度 | 30 |
| GQ | 基因质量 | 99 |
| VAF | 变异丰度 | 0.5 |
| gnomAD_AF | gnomAD 频率 | 0.0001 |
| **classification** | **OncoKB 致癌性** | **"Oncogenic", "Likely Oncogenic", "VUS"** |
| **is_tsg** | **是否为抑癌基因** | **"Yes" / "No"** |
| **is_oncogene** | **是否为癌基因** | **"Yes" / "No"** |

**如果用户提供了 OncoKB 标注的 CSV/表格数据，务必提取 `classification`、`is_tsg`、`is_oncogene` 字段传入 GPA，这对 somatic 模式分级至关重要。**

---

## 📊 输出解析

Wrapper 返回 JSON 结构：

```json
{
  "success": true,
  "results": {
    "meta": {...},
    "summary": {
      "tier1_count": 0,
      "tier2_count": 1,
      "tier3_count": 2,
      "multi_hit_genes": ["VWF"]
    },
    "tier1_variants": [],
    "tier2_variants": [...],
    "tier3_variants": [...],
    "multi_hit_details": [...],
    "report_markdown": "# GPA 报告..."
  },
  "report_md": "# GPA Report...",
  "stdout": "GPA Report Generated..."
}
```

### 给用户呈现的关键信息

**默认行为：分析完成后，直接读取报告文件内容并完整展示给用户。** 不要只给统计数字，不要让用户自己去看文件。

呈现内容优先级：
1. **完整 Markdown 报告** — 直接贴出报告全文（Tier 1/2/3 详情、多基因命中）
2. **若报告过长** — 先展示 Tier 1 和关键发现，再询问是否需要完整报告
3. **保存到指定路径** — 如果用户需要文件，用 `--output /path/to/file.md` 保存，不要用 /tmp

### 输出解析

Wrapper 返回 JSON 结构：

```json
{
  "success": true,
  "results": {
    "meta": {...},
    "summary": {
      "tier1_gene_count": 0,
      "tier1_variant_count": 0,
      "tier2_gene_count": 1,
      "tier2_variant_count": 2,
      "tier3_gene_count": 2,
      "tier3_variant_count": 5,
      "multi_hit_genes": ["VWF"]
    },
    "tier1_variants": [],
    "tier2_variants": [...],
    "tier3_variants": [...],
    "multi_hit_details": [...],
    "report_markdown": "# GPA 报告..."
  },
  "report_md": "# GPA Report...",
  "stdout": "GPA Report Generated..."
}
```

**呈现格式要求：**

每个变异必须展示以下字段（方便用户直接查询）：

| 字段 | 示例 | 用途 |
|------|------|------|
| **基因** | VWF | 基因符号 |
| **位点** | `chr12:6126538:G>A` | **CHROM:POS:REF:ALT，可直接在 IGV/UCSC/ClinVar 查询** |
| **转录本变化** | c.3931C>T | cDNA 水平 |
| **蛋白变化** | p.Gln1311Ter | 氨基酸水平 |
| **影响** | HIGH | VEP IMPACT |
| **类型** | stop_gained | Consequence（中英文自动映射，见下方） |
| **合子性** | 0/1 | GT |
| **ClinVar** | 致病 | 中文/英文 |
| **Tier** | 1 | GPA 分级 |
| **QC 标记** | `CLINVAR_CONFLICTING` | v0.7.1 新增：冲突注释标记 |

**Consequence 中英文映射（v0.7.1）**：
GPA 内部通过 `gpa_i18n.py` 自动标准化中英文 consequence 术语。输入可以是中文 VEP 注释（如 `错义变异`、`剪接供体变异`）或英文（`missense_variant`、`splice_donor_variant`），系统会自动映射到统一的标准术语并推断 IMPACT。

| 中文示例 | 映射后英文 | 推断 IMPACT |
|---------|-----------|------------|
| 错义变异 | missense_variant | MODERATE |
| 无义变异 | stop_gained | HIGH |
| 剪接供体变异 | splice_donor_variant | HIGH |
| 同义变异 | synonymous_variant | LOW |
| 移码变异 | frameshift_variant | HIGH |
| 框内缺失 | inframe_deletion | MODERATE |

**ClinVar 冲突注释（v0.7.1）**：
当 ClinVar 同时包含正反两种评级（如 `"良性, 致病"`、`"VUS, Pathogenic"`）时：
- 不触发 Tier 升级（weight=0）
- 标记 `CLINVAR_CONFLICTING` qc_flag
- 仍保留进入下游分析与报告
- 标准复合评级如 `"Pathogenic/Likely_pathogenic"` **不算冲突**

**ClinVar Review Status 星级（v0.7.2）**：
GPA 读取 `CLNREVSTAT` 字段，将 ClinVar 提交者星级纳入证据权重计算：

| CLNREVSTAT 文本 | 星级 | 置信度权重 |
|---|---|---|
| `practice_guideline` | ★★★★ | 0.95 |
| `reviewed_by_expert_panel` | ★★★☆ | 0.80 |
| `criteria_provided,_multiple_submitters,_no_conflicts` | ★★☆☆ | 0.55 |
| `single_submitter` | ★☆☆☆ | 0.40 |
| 缺失 / `no_assertion` / `conflicting` | — | 0.30 |

**效果**：
- Pathogenic 证据 weight = 基础值 × 星级权重（1.0 × 0.30~0.95）
- Benign 证据 weight = -0.5 × 星级权重（排除信号随星级增强）
- 单一提交者的 Pathogenic 不再自动 Tier 1（weight=0.40，需更多证据支持）
- 实践指南认可的 Pathogenic 仍高置信度（weight=0.95）

**冲突注释优先**：如果 ClinVar 评级冲突（v0.7.1 逻辑），星级评估被跳过，weight=0。
| **原因** | ClinVar pathogenic... | 为什么是这个 tier |

**若 chrom 为空或转录本选择有警告，必须标注并说明影响。**

| 场景 | 组织类型 |
|------|---------|
| 通用疾病遗传风险评估（默认） | `general` |
| 血液/肿瘤血液 | `hematopoietic` |
| 心血管 | `cardiovascular` |
| 肝脏 | `hepatic` |
| 肾脏 | `renal` |
| 神经系统 | `neurological` |

---

## 🔧 离线模式

当网络不可用或 API 超时频繁时，添加 `--offline` 参数：

```bash
python3 .../dgra_cli_wrapper.py --variants '[...]' --tissue general --offline
```

离线模式使用本地缓存（`references/offline_data/` 下的基因 JSON），对于已有归档的基因结果与在线模式一致。未归档的基因 fallback 到保守规则。

---

## ❌ 常见错误

| 错误 | 原因 | 解决 |
|-----|------|------|
| `Invalid tissue 'xxx'` | 组织类型不对 | 用 general / hematopoietic / cardiovascular / hepatic / renal / neurological |
| `variants list is empty` | 输入为空 | 检查 JSON 是否解析正确 |
| `Failed to write TSV` | 输入字段缺失 | 确保必填字段 CHROM/POS/REF/ALT/GENE 存在 |
| `dgra_core.py exited with code 1` | 核心脚本执行失败 | 看 stderr 输出排查 |
| `Offline mode: no cached data` | 离线模式但基因未归档 | 先在线运行一次建立归档，或换在线模式 |

---

## 📁 文件结构

```
dgra-genomic-risk/
  SKILL.md                  # 本文件
  config.json               # 元数据配置
  scripts/
    dgra_cli_wrapper.py     # ⭐ 推荐入口：agent 调用此 wrapper
    dgra_core.py            # 核心分析引擎（async API-first）
    dgra_api.py             # API 查询层
    dgra_cache.py           # SQLite 缓存
    dgra_config.py          # 配置管理
    dgra_build_state.py     # 构建状态持久化（v0.6.1）
    gpa_phenotype_match.py  # LLM 表型语义匹配（v0.7.0 Phase 2）
    gpa_i18n.py             # 中英文 consequence 术语映射（v0.7.1 Phase 2）
    dgra_variant_filter.py  # 预过滤模块：strict/clinical/broad（v0.7.1 Phase 3）
  references/
    tissue_context.json     # 组织上下文配置
    dgra.yaml               # 运行时参数配置
    offline_data/           # 离线归档（自动创建）
  cache/
    dgra_cache.db           # API 响应缓存
```

---

## 🩺 临床使用注意

### Tier 分级含义（按场景动态调整）

**Germline / 疾病遗传风险场景：**
- **Tier 1** = 必须干预的致病突变（如纯合截断、已知致病突变）
- **Tier 2** = 需知情同意并持续监测（如杂合携带者、药物代谢多态性）
- **Tier 3** = 记录归档，不影响当前决策

**Somatic / 肿瘤驱动场景：**
- **Tier 1** = 核心驱动突变（TSG 功能丧失、癌基因热点突变、OncoKB Oncogenic）
- **Tier 2** = 可能驱动突变（Likely Oncogenic、亚克隆突变、药物代谢相关）
- **Tier 3** = 乘客突变 / 无功能影响 / 胚系多态混入

**多基因命中**需确认相位：cis（同一条染色体）风险更高，trans（两条染色体）通常为复合杂合

**GPA 是辅助决策工具，最终临床决策需结合完整临床评估。**
