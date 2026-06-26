---
name: ncbi-search
description: "Search NCBI databases using E-Utilities API (official, free). Supports 10+ databases: PubMed (literature), Gene, Protein, Nucleotide, dbSNP, ClinVar, Taxonomy, BioSample, Assembly, SRA. Automatically detects search intent and routes to appropriate database. Returns formatted results with key information. Use for biomedical literature, gene information, protein sequences, genetic variants, and more."
allowed-tools: [Bash]
trigger-keywords: [ncbi, pubmed, gene, protein, snp, clinvar, literature, paper, article, review, variant, genome, sequence, taxonomy, dna, rna]
---

# NCBI Search — AI Agent 工具文档

> **一句话描述**: NCBI 多数据库智能检索工具，使用官方 E-Utilities API，免费、可靠、零外部依赖。

---

## 目录

1. [快速决策树](#1-快速决策树)
2. [数据库总览](#2-数据库总览)
3. [使用方式](#3-使用方式)
4. [参数详解](#4-参数详解)
5. [完整示例集](#5-完整示例集)
6. [高级查询技巧](#6-高级查询技巧)
7. [结果解析说明](#7-结果解析说明)
8. [错误处理指南](#8-错误处理指南)
9. [批量处理能力](#9-批量处理能力)
10. [缓存机制](#10-缓存机制)
11. [API Key 配置](#11-api-key-配置)
12. [文件结构](#12-文件结构)

---

## 1. 快速决策树

AI Agent 请按以下优先级判断使用哪个数据库：

```
用户查询
│
├─ 包含 rs\d+ 模式（如 rs429358）? → dbSNP
│
├─ 包含 VCV\d+ 模式（如 VCV000242862）? → ClinVar
│
├─ 包含已知基因符号（APOE, BRCA1 等）或 4-8 位潜在基因正则（如 SHANK3）?
│   ├─ 同时包含文献关键字（paper/review/trial/文献/论文/临床等）? → PubMed
│   └─ 否则 → Gene
│
├─ 包含数据库关键词?
│   ├─ paper/article/review/journal/trial/文献/论文/临床/综述 → PubMed
│   ├─ protein/peptide/amino acid/蛋白/多肽/氨基酸/sequence → Protein
│   ├─ nucleotide/DNA/RNA/genome/cDNA/核酸/序列/基因组 → Nucleotide
│   ├─ SNP/variant/polymorphism/allele/变异/多态性/突变 → dbSNP
│   ├─ clinvar/clinical variant/pathogenic/致病/临床变异 → ClinVar
│   ├─ species/taxonomy/organism/classification/物种/分类 → Taxonomy
│   ├─ biosample/sample/样本 → BioSample
│   ├─ assembly/genome assembly/基因组组装 → Assembly
│   └─ SRA/sequencing/reads/测序数据 → SRA
│
└─ 以上都不匹配 → PubMed（默认）
```

### 触发规则优先级

| 优先级 | 匹配条件 | 路由目标 |
|--------|---------|---------|
| 🔴 最高 | `rs\d+` 正则匹配 | dbSNP |
| 🔴 最高 | `VCV\d+` 正则匹配 | ClinVar |
| 🟠 高 | 已知基因符号或 4-8 位大写混合字母（非普通英文短词） | Gene |
| 🟡 中 | 数据库关键词高特异性打分匹配 | 对应数据库 |
| 🟢 默认 | 无明确匹配 | PubMed |

### Do / Don't

| ✅ Do | ❌ Don't |
|-------|---------|
| 用户提到"基因"时用 `--db gene` | 不要对纯数字查询（如"348"）自动路由到 Gene |
| 用户提到"文献/论文"时用 `--db pubmed` | 不要对含基因符号的查询直接路由到 Gene（先检查是否要查文献） |
| 用户给 rsID 时用 `--db snp` | 不要用 `--db snp` 查非 SNP 内容 |
| 不确定时默认用 PubMed | 不要同时查多个数据库（需分步执行） |

---

## 2. 数据库总览

### 2.1 完整数据库列表

| 数据库 | 命令行名称 | 用途 | 触发关键词 | ID 格式 | 链接模板 |
|--------|-----------|------|-----------|---------|---------|
| **PubMed** | `pubmed` | 生物医学文献检索 | paper, article, review, publication, journal, study, 论文, 文献, 研究, 发表, 文章, 综述 | PMID（数字） | `https://pubmed.ncbi.nlm.nih.gov/{PMID}/` |
| **Gene** | `gene` | 基因信息查询 | gene, symbol, 编码, 基因, mRNA, expression, 转录 | Gene ID（数字） | `https://www.ncbi.nlm.nih.gov/gene/{ID}` |
| **Protein** | `protein` | 蛋白质序列 | protein, peptide, amino, 蛋白, 多肽, 氨基酸, sequence | Accession（字母+数字） | `https://www.ncbi.nlm.nih.gov/protein/{ACC}` |
| **Nucleotide** | `nucleotide` | 核酸序列 | nucleotide, DNA, RNA, sequence, genome, cDNA, 核酸, 序列, 基因组 | Accession（字母+数字） | `https://www.ncbi.nlm.nih.gov/nuccore/{ACC}` |
| **dbSNP** | `snp` | SNP 变异查询 | SNP, variant, polymorphism, allele, rs, 变异, 多态性, 突变 | rsID（rs+数字） | `https://www.ncbi.nlm.nih.gov/snp/{rsID}` |
| **ClinVar** | `clinvar` | 临床变异 | clinvar, clinical variant, pathogenic, 致病, 临床变异 | Variation ID（数字） | `https://www.ncbi.nlm.nih.gov/clinvar/variation/{ID}` |
| **Taxonomy** | `taxonomy` | 物种分类 | species, taxonomy, organism, classification, 物种, 分类, 物种分类 | TaxID（数字） | `https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id={ID}` |
| **BioSample** | `biosample` | 生物样本信息 | biosample, sample, 样本 | Sample ID | `https://www.ncbi.nlm.nih.gov/biosample/{ID}` |
| **Assembly** | `assembly` | 基因组组装 | assembly, genome assembly, 基因组组装 | Assembly ID | `https://www.ncbi.nlm.nih.gov/assembly/{ID}` |
| **SRA** | `sra` | 测序数据归档 | SRA, sequencing, reads, 测序数据 | SRA ID（SRR/ERR/DRR） | `https://www.ncbi.nlm.nih.gov/sra/{ID}` |

### 2.2 数据库选择建议

| 用户意图 | 推荐数据库 | 说明 |
|---------|-----------|------|
| 查某疾病的文献 | `pubmed` | 最全面的生物医学文献库 |
| 查某个基因的功能 | `gene` | 包含基因位置、功能、别名等 |
| 查蛋白质序列 | `protein` | 包含 FASTA 序列 |
| 查 DNA/RNA 序列 | `nucleotide` | 包含 GenBank 序列 |
| 查某个 SNP 位点 | `snp` | 包含等位基因频率、临床意义 |
| 查变异与疾病关系 | `clinvar` | 临床级别的变异注释 |
| 查物种分类信息 | `taxonomy` | 完整的物种分类树 |
| 查测序数据 | `sra` | 高通量测序原始数据 |

---

## 3. 使用方式

### 3.1 脚本说明

项目包含 4 个脚本，各有侧重：

| 脚本 | 功能 | 适用场景 |
|------|------|---------|
| `ncbi_search.py` | **主脚本**：多数据库智能搜索，自动意图识别 | 大多数情况，推荐使用 |
| `pubmed_search.py` | **PubMed 专用**：自然语言转检索式，MeSH 词识别 | 仅 PubMed 检索，需要智能解析 |
| `pubmed_fetch.py` | **批量获取**：通过 PMID 列表批量获取文献详情 | 已有 PMID 列表，需要批量获取 |
| `ncbi_utils.py` | **工具函数**：共享工具函数 | 被其他脚本调用，不直接使用 |

### 3.2 自动模式（推荐）

```bash
# 自动判断搜索意图
python scripts/ncbi_search.py "APOE gene"
python scripts/ncbi_search.py "Alzheimer disease review"
python scripts/ncbi_search.py "insulin protein"
python scripts/ncbi_search.py "rs429358"
```

### 3.3 指定数据库

```bash
python scripts/ncbi_search.py "APOE" --db gene
python scripts/ncbi_search.py "diabetes" --db pubmed
python scripts/ncbi_search.py "rs429358" --db snp
```

### 3.4 PubMed 专用脚本（自然语言检索）

```bash
# 自动将自然语言转换为 PubMed 检索式
python scripts/pubmed_search.py "Alzheimer disease cerebrovascular mechanisms"
python scripts/pubmed_search.py "APOE gene and Alzheimer disease" --years 5
python scripts/pubmed_search.py "Smith J author Alzheimer" --max 20
```

---

## 4. 参数详解

### 4.1 ncbi_search.py 参数

| 参数 | 类型 | 默认值 | 适用数据库 | 说明 |
|------|------|--------|-----------|------|
| `query` | 必填 | - | 全部 | 搜索查询（自然语言或标准检索式） |
| `--db` | 可选 | auto-detect | 全部 | 指定数据库，不指定则自动识别 |
| `--max` | int | 10 | 全部 | 最大返回结果数（1-100） |
| `--years` | int | - | **仅 pubmed** | 限制最近 N 年 |
| `--type` | str | - | **仅 pubmed** | 文章类型过滤 |
| `--organism` | str | - | **仅 gene** | 物种过滤 |
| `--format` | str | summary | 全部 | 输出格式：summary 或 json |
| `--output` / `-o` | str | - | 全部 | 保存结果到文件 |
| `--api-key` | str | env var | 全部 | NCBI API Key |
| `--verbose` / `-v` | bool | false | 全部 | 显示详细信息 |

### 4.2 pubmed_search.py 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `query` | 必填 | - | 自然语言检索词或 PubMed 检索式 |
| `--max` | int | 10 | 最大返回结果数 |
| `--years` | int | - | 限制最近 N 年 |
| `--type` | str | - | 文章类型：review, clinical_trial, randomized, meta_analysis |
| `--mesh` | str | - | MeSH 主题词筛选 |
| `--format` | str | summary | 输出格式：summary 或 json |
| `--output` / `-o` | str | - | 保存结果到文件 |
| `--api-key` | str | env var | NCBI API Key |
| `--verbose` / `-v` | bool | false | 显示详细信息 |

### 4.3 --type 参数可选值

| 值 | 含义 | PubMed 标签 |
|----|------|-------------|
| `review` | 综述 | `Review[pt]` |
| `clinical_trial` | 临床试验 | `Clinical Trial[pt]` |
| `randomized` | 随机对照试验 | `Randomized Controlled Trial[pt]` |
| `meta_analysis` | Meta 分析 | `Meta-Analysis[pt]` |

### 4.4 参数组合规则

| 组合 | 是否合法 | 说明 |
|------|---------|------|
| `--db pubmed --years 5` | ✅ 合法 | PubMed 限定年份 |
| `--db pubmed --type review` | ✅ 合法 | PubMed 限定文章类型 |
| `--db gene --organism human` | ✅ 合法 | Gene 限定物种 |
| `--db snp --years 5` | ❌ 无效 | `--years` 仅适用于 PubMed |
| `--db protein --organism human` | ❌ 无效 | `--organism` 仅适用于 Gene |
| `--db pubmed --organism human` | ❌ 无效 | `--organism` 仅适用于 Gene |

---

## 5. 完整示例集

### 5.1 基础示例

```bash
# 自动模式
python scripts/ncbi_search.py "APOE gene"                    # → Gene
python scripts/ncbi_search.py "Alzheimer disease review"     # → PubMed
python scripts/ncbi_search.py "rs429358"                     # → dbSNP
python scripts/ncbi_search.py "insulin protein"              # → Protein
python scripts/ncbi_search.py "Escherichia coli taxonomy"    # → Taxonomy

# 指定数据库
python scripts/ncbi_search.py "APOE" --db gene --organism human
python scripts/ncbi_search.py "insulin" --db protein
python scripts/ncbi_search.py "BRCA1" --db nucleotide
```

### 5.2 组合参数示例

```bash
# PubMed 高级过滤
python scripts/ncbi_search.py "diabetes treatment" --years 5 --type review --max 20
python scripts/ncbi_search.py "Alzheimer amyloid beta" --years 3 --max 5
python scripts/ncbi_search.py "COVID-19 vaccine" --type clinical_trial --max 50

# Gene 高级过滤
python scripts/ncbi_search.py "APOE" --db gene --organism human
python scripts/ncbi_search.py "TP53" --db gene --organism mouse

# JSON 格式输出
python scripts/ncbi_search.py "BRCA1" --db gene --format json

# 保存到文件
python scripts/ncbi_search.py "Alzheimer disease" --years 5 --max 100 -o results.txt
```

### 5.3 PubMed 自然语言检索示例

```bash
# 使用 pubmed_search.py 进行智能解析
python scripts/pubmed_search.py "Alzheimer disease cerebrovascular mechanisms"
python scripts/pubmed_search.py "APOE gene and Alzheimer disease" --years 5
python scripts/pubmed_search.py "Smith J author Alzheimer" --max 20
python scripts/pubmed_search.py "diabetes treatment review" --type review
python scripts/pubmed_search.py "cancer immunotherapy" --mesh "Neoplasms" --years 3
```

### 5.4 边界情况示例

```bash
# 无结果查询
python scripts/ncbi_search.py "xyzabc123nonexistent" --db gene

# 大量结果（仅返回前 N 条）
python scripts/ncbi_search.py "cancer" --db pubmed --max 5

# 特殊字符查询
python scripts/ncbi_search.py "IL-6 gene" --db gene
python scripts/ncbi_search.py "p53 protein" --db protein

# 中文查询
python scripts/ncbi_search.py "阿尔茨海默病 综述" --db pubmed
python scripts/ncbi_search.py "APOE 基因" --db gene
```

---

## 6. 高级查询技巧

### 6.1 PubMed 检索式构建

`pubmed_search.py` 会自动将自然语言转换为标准 PubMed 检索式。转换逻辑如下：

| 自然语言 | 转换后 | 说明 |
|---------|--------|------|
| `Alzheimer disease` | `"Alzheimer Disease"[MeSH]` | 识别为 MeSH 词 |
| `APOE gene` | `APOE[Title/Abstract]` | 识别为基因符号 |
| `Smith J` | `Smith J[Author]` | 识别为作者 |
| `last 5 years` | `2020/01/01:2025/01/01[PDat]` | 日期范围 |
| `review` | `Review[pt]` | 文章类型 |

### 6.2 手动构建检索式

如果自动转换不满足需求，可以直接传入标准 PubMed 检索式：

```bash
# 复杂布尔检索
python scripts/ncbi_search.py "(Alzheimer[Title/Abstract]) AND (APOE[Title/Abstract]) AND (Review[pt])"

# 多字段组合
python scripts/ncbi_search.py "(diabetes[MeSH]) AND (insulin[Title/Abstract]) AND (2020[PDat]:2025[PDat])"

# 排除检索
python scripts/ncbi_search.py "(Alzheimer[Title/Abstract]) NOT (mouse[Title/Abstract])"
```

### 6.3 常用 PubMed 字段标签

| 标签 | 含义 | 示例 |
|------|------|------|
| `[Title/Abstract]` | 标题/摘要 | `Alzheimer[Title/Abstract]` |
| `[MeSH]` | MeSH 主题词 | `"Alzheimer Disease"[MeSH]` |
| `[Author]` | 作者 | `Smith J[Author]` |
| `[Journal]` | 期刊名 | `Nature[Journal]` |
| `[PDat]` | 出版日期 | `2020/01/01:2025/01/01[PDat]` |
| `[pt]` | 文章类型 | `Review[pt]` |
| `[Organism]` | 物种 | `human[Organism]` |
| `[Gene]` | 基因名 | `APOE[Gene]` |

### 6.4 布尔运算符

| 运算符 | 含义 | 示例 |
|--------|------|------|
| `AND` | 与（必须同时包含） | `Alzheimer AND APOE` |
| `OR` | 或（包含任一即可） | `Alzheimer OR dementia` |
| `NOT` | 非（排除） | `Alzheimer NOT mouse` |

---

## 7. 结果解析说明

### 7.1 PubMed 结果字段

| 字段 | 说明 | 提取建议 |
|------|------|---------|
| `PMID` | PubMed 唯一标识符 | 用于生成链接和引用 |
| `Title` | 文章标题 | 判断相关性 |
| `Authors` | 作者列表（前 5 位） | 提取第一作者和通讯作者 |
| `Journal` | 期刊名称 | 判断期刊影响力 |
| `Year` | 出版年份 | 判断时效性 |
| `DOI` | 数字对象标识符 | 用于查找全文 |
| `Abstract` | 摘要（前 200 字符预览） | 快速了解研究内容 |
| `MeSH` | MeSH 主题词 | 了解文章主题分类 |
| `URL` | PubMed 链接 | 直接访问 |

### 7.2 Gene 结果字段

| 字段 | 说明 | 提取建议 |
|------|------|---------|
| `Gene ID` | 基因唯一标识符 | 用于生成链接 |
| `Symbol` | 基因符号 | 标准命名 |
| `Description` | 基因描述 | 了解基因功能 |
| `Chromosome` | 染色体位置 | 基因组定位 |
| `Organism` | 物种信息 | 判断物种 |

### 7.3 dbSNP 结果字段

| 字段 | 说明 | 提取建议 |
|------|------|---------|
| `rsID` | SNP 标识符 | 标准命名 |
| `Genes` | 关联基因 | 了解变异所在基因 |
| `Alleles` | 等位基因 | 判断变异类型 |
| `Clinical` | 临床意义 | 判断致病性 |
| `Frequency` | 人群频率 | 判断稀有程度 |

### 7.4 结果排序规则

- **默认排序**: 按相关性（relevance）降序
- **PubMed 特殊排序**: 相关性与时间综合排序
- **无 API Key 限制**: 最多返回 20 条（NCBI 限制）
- **有 API Key 限制**: 最多返回 100 条

---

## 8. 错误处理指南

### 8.1 常见错误码

| 错误 | 原因 | 处理方式 |
|------|------|---------|
| `HTTP 429` | 请求过于频繁 | 等待 1 秒后重试（自动处理） |
| `HTTP 500` | NCBI 服务器错误 | 等待后重试（自动重试 3 次） |
| `HTTP 502/503/504` | 网关超时 | 等待后重试（自动重试 3 次） |
| `ConnectionError` | 网络连接失败 | 检查网络连接后重试 |
| `Timeout` | 请求超时 | 增加超时时间或减少结果数 |
| `0 results` | 无匹配结果 | 尝试更宽泛的查询词 |

### 8.2 速率限制

| 情况 | 限制 | 说明 |
|------|------|------|
| 无 API Key | 3 次/秒 | 脚本自动限流，无需手动处理 |
| 有 API Key | 10 次/秒 | 建议配置 API Key 提高效率 |

### 8.3 降级策略

当 API Key 缺失或请求失败时：

```bash
# 1. 无 API Key 时自动降速（脚本自动处理）
# 2. 减少请求量
python scripts/ncbi_search.py "query" --max 5

# 3. 使用更精确的查询减少结果数
python scripts/ncbi_search.py "Alzheimer APOE" --db pubmed --max 10

# 4. 检查 API Key 是否配置
echo $env:NCBI_API_KEY  # Windows PowerShell
```

### 8.4 无结果时的应对策略

| 情况 | 建议操作 |
|------|---------|
| 查询太具体 | 使用更宽泛的术语 |
| 拼写错误 | 检查拼写，尝试同义词 |
| 数据库不对 | 尝试其他数据库 |
| 过滤太严格 | 减少过滤条件（去掉 --years, --type 等） |

---

## 9. 批量处理能力

### 9.1 批量获取文献详情

使用 `pubmed_fetch.py` 通过 PMID 列表批量获取：

```bash
# 通过 PMID 列表获取
python scripts/pubmed_fetch.py 33597265 34239348 35022842

# 从文件读取 PMID 列表
python scripts/pubmed_fetch.py -f pmids.txt

# 指定输出格式
python scripts/pubmed_fetch.py 33597265 34239348 --format json

# 保存到文件
python scripts/pubmed_fetch.py 33597265 34239348 -o articles.json
```

### 9.2 多次查询结果合并

```bash
# 分步查询不同数据库
python scripts/ncbi_search.py "APOE" --db gene --format json -o gene_result.json
python scripts/ncbi_search.py "APOE" --db pubmed --max 5 --format json -o pubmed_result.json

# 使用 pubmed_search.py 获取详细信息
python scripts/pubmed_search.py "APOE gene Alzheimer" --max 10 -o detailed_results.txt
```

### 9.3 数据导出格式

| 格式 | 适用场景 | 命令 |
|------|---------|------|
| **summary**（默认） | 人类阅读 | `--format summary` |
| **JSON** | 程序处理 | `--format json` |
| **保存到文件** | 持久化 | `-o filename.txt` |

---

## 10. 缓存机制

### 10.1 缓存说明

脚本内置了**零依赖的 SQLite 本地持久化缓存**，可自动优化检索速度并防止触发 NCBI 速率限制：

1. **自动缓存机制**: ESearch、ESummary 和 EFetch 的所有 HTTP 响应都会被自动持久化存储在工作区下的 `.ncbi_cache/cache.db`。
2. **零网络延迟**: 重复进行相同的查询时，数据会瞬间从本地数据库返回（耗时由数百毫秒缩短至数毫秒），完全无网络请求。
3. **缓存有效期**: 缓存默认有效期为 **24 小时**。可以通过 `NCBI_CACHE_EXPIRE_HOURS` 环境变量调整过期时长。

### 10.2 缓存控制与配置

```bash
# 1. 调整缓存有效期（例如设为 48 小时）
# Windows PowerShell
$env:NCBI_CACHE_EXPIRE_HOURS = "48"

# 2. 临时禁用缓存（绕过缓存，强制向网络发起实时请求）
# Windows PowerShell
$env:NCBI_NO_CACHE = "1"
python scripts/ncbi_search.py "APOE gene"
```

### 10.3 速率限制（内置）

即使在缓存未命中（Cache Miss）时，脚本也会自动处理 NCBI 的速率限制：

- **无 API Key**: 每次请求间隔 ≥ 0.34 秒（≤ 3 次/秒）
- **有 API Key**: 每次请求间隔 ≥ 0.11 秒（≤ 10 次/秒）
- **自动重试**: 遇到 429/500/502/503/504 错误时自动重试 3 次

---

## 11. API Key 配置

### 11.1 获取 API Key

1. 注册 [NCBI 账号](https://www.ncbi.nlm.nih.gov/account/)
2. 进入 Settings → API Key Management → Create API Key
3. 复制生成的 API Key

### 11.2 配置方式

```powershell
# Windows PowerShell（当前会话）
$env:NCBI_API_KEY = "your-api-key-here"

# Windows PowerShell（永久）
[Environment]::SetEnvironmentVariable("NCBI_API_KEY", "your-api-key", "User")

# 命令行指定
python scripts/ncbi_search.py "query" --api-key "your-api-key"
```

### 11.3 速率对比

| 方式 | 速率 | 建议 |
|------|------|------|
| 无 API Key | 3 次/秒 | 临时使用 |
| 有 API Key | 10 次/秒 | ✅ 推荐，效率提升 3 倍+ |

---

## 12. 文件结构

```
ncbi-search/
├── SKILL.md                    # 本文档（AI Agent 技能说明）
├── README.md                   # 用户文档
├── LICENSE                     # MIT License
├── scripts/
│   ├── ncbi_search.py          # 主脚本：多数据库智能搜索
│   ├── pubmed_search.py        # PubMed 专用：自然语言转检索式
│   ├── pubmed_fetch.py         # 批量获取：通过 PMID 获取文献详情
│   └── ncbi_utils.py           # 工具函数
└── references/
    └── query_syntax.md         # PubMed 检索语法指南
```

---

## 参考链接

- [NCBI E-Utilities 官方文档](https://www.ncbi.nlm.nih.gov/books/NBK25501/)
- [NCBI 数据库列表](https://www.ncbi.nlm.nih.gov/books/NBK25500/table/chapter.T5/)
- [PubMed 检索语法](https://pubmed.ncbi.nlm.nih.gov/help/)

---

**技能状态**: 就绪
**API 要求**: NCBI API Key（免费，推荐配置）
**费用**: 完全免费
**依赖**: 仅需 Python 3.7+ 和 `requests` 库