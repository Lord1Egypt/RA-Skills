# NCBI Search

<div align="center">

[![NCBI](https://img.shields.io/badge/NCBI-E--Utilities-blue)](https://www.ncbi.nlm.nih.gov/books/NBK25501/)
[![Python](https://img.shields.io/badge/Python-3.7+-green)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![Free](https://img.shields.io/badge/API-Free-success)](https://www.ncbi.nlm.nih.gov/account/)
[![Release](https://img.shields.io/github/v/release/Side-Peng/ncbi-search)](https://github.com/Side-Peng/ncbi-search/releases)

**智能多数据库检索工具 | 直接调用NCBI官方API | 无需第三方服务**

[English](#english) | [中文](#中文)

</div>

---

## 中文

### ✨ 功能特性

- 🎯 **智能意图识别** - 自动判断搜索目标数据库（文献/基因/变异等），支持通用基因正则匹配
- 📚 **多数据库支持** - PubMed, Gene, Protein, dbSNP, ClinVar 等 10+ 数据库
- 🔄 **自然语言转换** - 自动将自然语言转换为标准检索式
- ⚡ **零外部依赖** - 直接调用 NCBI 官方 E-Utilities API
- 💾 **SQLite 本地缓存** - 自动缓存查询结果，二次查询毫秒级响应，避免触发 API 限速
- 💰 **完全免费** - 使用自己的 NCBI API Key，无任何费用
- 🚀 **速率优化** - 自动重试、智能限流、支持高并发
- 🧪 **单元测试覆盖** - 内置自动化测试套件，保障路由与缓存逻辑的正确性

### 📦 安装

```bash
# 克隆仓库
git clone https://github.com/Side-Peng/ncbi-search.git
cd ncbi-search

# 安装依赖
pip install requests
```

### 🔑 配置 API Key

1. 注册 [NCBI 账号](https://www.ncbi.nlm.nih.gov/account/)
2. 进入 Settings → API Key Management → Create API Key
3. 配置环境变量：

```bash
# Linux/macOS
export NCBI_API_KEY="your-api-key-here"

# Windows PowerShell (永久)
[Environment]::SetEnvironmentVariable("NCBI_API_KEY", "your-api-key", "User")

# 或在命令行指定
python scripts/ncbi_search.py "query" --api-key "your-api-key"
```

**速率限制**：无 API Key 3次/秒，有 API Key 10次/秒

### 🚀 快速开始

```bash
# 自动识别搜索意图
python scripts/ncbi_search.py "APOE gene"                    # → Gene 数据库
python scripts/ncbi_search.py "Alzheimer disease review"     # → PubMed
python scripts/ncbi_search.py "rs429358"                     # → dbSNP
python scripts/ncbi_search.py "VCV000242862"                 # → ClinVar（v1.1 新增）
python scripts/ncbi_search.py "SHANK3 function"              # → Gene（通用基因正则匹配）

# 指定数据库
python scripts/ncbi_search.py "APOE" --db gene --organism human
python scripts/ncbi_search.py "insulin" --db protein

# PubMed 高级过滤
python scripts/ncbi_search.py "diabetes treatment" --years 5 --type review --max 20
```

### 📖 使用示例

#### PubMed 文献检索

```bash
# 近5年阿尔茨海默病Aβ研究
python scripts/ncbi_search.py "Alzheimer amyloid beta" --years 5 --max 10

# 指定作者和期刊
python scripts/ncbi_search.py "Smith J[Author] AND Nature[Journal]"

# 临床试验
python scripts/ncbi_search.py "diabetes" --type clinical_trial
```

输出示例：
```
======================================================================
PubMed Search Results
======================================================================
Query: (Alzheimer amyloid beta) AND 2021/03/12:2026/03/11[PDat]
Total: 21355 articles | Returned: 10 articles
======================================================================

[1] PMID: 34239348
Title: Interaction between Aβ and Tau in the Pathogenesis...
Authors: Zhang H, Wei W, Zhao M et al.
Journal: International journal of biological sciences (2021)
URL: https://pubmed.ncbi.nlm.nih.gov/34239348/
----------------------------------------------------------------------
```

#### Gene 基因检索

```bash
# 搜索基因
python scripts/ncbi_search.py "APOE gene" --organism human

# 输出
======================================================================
Gene Search Results
======================================================================
Query: (APOE gene) AND human[Organism]
Total: 1 gene
======================================================================

[1] Gene ID: 348
Symbol: APOE
Description: apolipoprotein E
Chromosome: 19
URL: https://www.ncbi.nlm.nih.gov/gene/348
----------------------------------------------------------------------
```

#### dbSNP 变异检索

```bash
# 搜索 SNP
python scripts/ncbi_search.py "rs429358"

# 输出
======================================================================
dbSNP Search Results
======================================================================
Query: rs429358
Total: 1 variant
======================================================================

[1] rsID: rs429358
Genes: APOE
URL: https://www.ncbi.nlm.nih.gov/snp/rs429358
----------------------------------------------------------------------
```

### 💾 本地缓存机制（v1.1 新增）

工具内置了零外部依赖的 SQLite 本地自动缓存，所有 NCBI API 响应结果会自动持久化存储在 `.ncbi_cache/cache.db` 中。

| 特性 | 说明 |
|------|------|
| **自动缓存** | ESearch、ESummary、EFetch 响应全部自动存储 |
| **缓存有效期** | 默认 24 小时，支持自定义 |
| **二次查询** | 命中缓存时 1-5ms 响应，零网络请求 |
| **禁用方式** | 设置 `NCBI_NO_CACHE=1` 环境变量 |

```bash
# 调整缓存有效期（例如 48 小时）
$env:NCBI_CACHE_EXPIRE_HOURS = "48"

# 临时禁用缓存
$env:NCBI_NO_CACHE = "1"
python scripts/ncbi_search.py "APOE gene"

# 使用 verbose 模式查看缓存命中情况
python scripts/ncbi_search.py "APOE gene" -v
```

### 🗄️ 支持的数据库

| 数据库 | 用途 | 触发关键词 |
|--------|------|-----------|
| **pubmed** | 文献检索 | paper, article, review, 论文, 文献 |
| **gene** | 基因信息 | gene, 基因, symbol, 或自动识别基因符号 |
| **protein** | 蛋白质序列 | protein, 蛋白, sequence |
| **nucleotide** | 核酸序列 | DNA, RNA, 序列, genome |
| **snp** | SNP变异 | SNP, rs, 变异, variant |
| **clinvar** | 临床变异 | clinvar, pathogenic, 致病, 或 VCV 编号 |
| **taxonomy** | 物种分类 | species, 物种, taxonomy |
| **biosample** | 生物样本 | biosample, 样本 |
| **assembly** | 基因组组装 | genome assembly, 组装 |
| **sra** | 测序数据 | SRA, sequencing |

### 🎯 智能路由优先级

```
用户查询
│
├─ 包含 rs\d+ 模式（如 rs429358）? → dbSNP
├─ 包含 VCV\d+ 模式（如 VCV000242862）? → ClinVar
├─ 包含已知/通用基因符号?
│   ├─ 同时含文献关键字? → PubMed
│   └─ 否则 → Gene
├─ 包含特定数据库关键词? → 对应数据库
└─ 以上都不匹配 → PubMed（默认）
```

### 📝 命令行参数

```
python scripts/ncbi_search.py <query> [options]

必需参数:
  query                 搜索查询（自然语言或标准检索式）

可选参数:
  --db DATABASE         指定数据库（不指定则自动识别）
  --max N               最大返回结果数（默认: 10）
  --years N             限制最近 N 年（仅 PubMed）
  --type TYPE           文章类型: review, clinical_trial 等（仅 PubMed）
  --organism ORGANISM   限制物种（仅 Gene）
  --format FORMAT       输出格式: summary, json（默认: summary）
  --output FILE         保存到文件
  --api-key KEY         NCBI API Key
  --verbose             显示详细信息（含缓存命中状态）
```

### 📁 项目结构

```
ncbi-search/
├── README.md                   # 本文档
├── SKILL.md                    # AI Agent 技能说明文档
├── LICENSE                     # MIT License
├── .ncbi_cache/                # 本地 SQLite 缓存目录（自动生成）
│   └── cache.db                # 缓存数据库
├── scripts/
│   ├── ncbi_search.py          # 主脚本（多数据库智能搜索）
│   ├── pubmed_search.py        # PubMed 专用脚本（自然语言转检索式）
│   ├── pubmed_fetch.py         # PMID 批量获取
│   ├── ncbi_utils.py           # 共享工具函数（Session、限流、缓存）
│   └── test_ncbi.py            # 单元测试套件
└── references/
    └── query_syntax.md         # PubMed 检索语法指南
```

### 🧪 运行测试

```bash
python scripts/test_ncbi.py
```

测试覆盖：意图路由准确性、SQLite 缓存读写、缓存禁用环境变量、速率限制机制。

### 🔧 作为 Agent Skill 使用

本项目设计为 AI Agent（如 Claude、Gemini 等）的技能插件：

```bash
# 安装到 Agent skills 目录
cp -r ncbi-search ~/.agents/skills/
```

在 SKILL.md 中定义了详细的触发规则和使用说明。

### 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

### 🙏 致谢

- [NCBI E-Utilities](https://www.ncbi.nlm.nih.gov/books/NBK25501/) - 官方 API

---

## English

### ✨ Features

- 🎯 **Smart Intent Detection** - Automatically routes queries to appropriate databases, with universal gene symbol regex matching
- 📚 **Multi-Database Support** - PubMed, Gene, Protein, dbSNP, ClinVar, and 10+ more
- 🔄 **Natural Language Processing** - Converts plain language to structured queries
- ⚡ **No External Dependencies** - Direct NCBI E-Utilities API calls
- 💾 **SQLite Local Cache** - Automatic query caching with millisecond-level repeat lookups
- 💰 **Completely Free** - Uses your own NCBI API key
- 🚀 **Rate Optimized** - Auto-retry, smart throttling, high concurrency support
- 🧪 **Unit Tested** - Built-in test suite for routing and caching logic

### 📦 Installation

```bash
git clone https://github.com/Side-Peng/ncbi-search.git
cd ncbi-search
pip install requests
```

### 🔑 API Key Setup

1. Register at [NCBI](https://www.ncbi.nlm.nih.gov/account/)
2. Go to Settings → API Key Management → Create API Key
3. Configure:

```bash
# Linux/macOS
export NCBI_API_KEY="your-api-key"

# Windows PowerShell
[Environment]::SetEnvironmentVariable("NCBI_API_KEY", "your-api-key", "User")
```

### 🚀 Quick Start

```bash
# Auto-detect database
python scripts/ncbi_search.py "APOE gene"                # → Gene database
python scripts/ncbi_search.py "Alzheimer disease review" # → PubMed
python scripts/ncbi_search.py "rs429358"                 # → dbSNP
python scripts/ncbi_search.py "VCV000242862"             # → ClinVar (v1.1)

# Specify database
python scripts/ncbi_search.py "APOE" --db gene --organism human

# PubMed filters
python scripts/ncbi_search.py "diabetes" --years 5 --type review --max 20
```

### 💾 Local Cache (v1.1)

All NCBI API responses are automatically cached in a local SQLite database (`.ncbi_cache/cache.db`). Repeat queries return instantly (1-5ms) with zero network requests. Cache expires after 24 hours by default.

```bash
# Customize cache TTL (hours)
export NCBI_CACHE_EXPIRE_HOURS=48

# Disable cache
export NCBI_NO_CACHE=1
```

### 🧪 Run Tests

```bash
python scripts/test_ncbi.py
```

### 📄 License

MIT License - see [LICENSE](LICENSE)

---

<div align="center">

**Made with ❤️ for researchers**

[⬆ Back to Top](#ncbi-search)

</div>