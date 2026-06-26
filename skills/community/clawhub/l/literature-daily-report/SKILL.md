---
name: literature-daily-report
version: 1.0.0
description: |
  每日科研文献日报生成与管理。当用户请求生成科研日报、更新文献收集脚本或分析研究趋势时激活。支持：(1) 自动抓取 PubMed/bioRxiv/arXiv 最新文献，(2) 语义筛选 AI/生信/病原/真菌等领域，(3) LLM 智能总结与编辑排版，(4) 中文格式报告输出与定时任务管理。
---

# 每日科研文献日报 v3.2

## 🎯 核心功能

自动化生成 **生命科学×AI 交叉领域** 的每日科研文献日报，包含：

1. **📊 文献采集** - 实时抓取 PubMed, bioRxiv, arXiv 当天最新发表
2. **🔍 智能筛选** - 语义检索 AI/生信/病原/真菌等关注领域
3. **🤖 LLM 总结** - 自动生成 100-250 字核心摘要（中英文混排）
4. **📰 编辑排版** - 前言 + 重点推荐 + 完整列表 + 趋势总结

---

## 🚀 快速开始

### 生成今日日报

```bash
# 方式 1：直接使用脚本
~/.openclaw/skills/literature-daily-report/scripts/literature_collector.py

# 方式 2：通过项目目录运行
cd ~/.openclaw/workspace/projects/literature-collector && ./run.sh
```

### 自定义配置

编辑配置文件 `config.yaml`：

```yaml
output_dir: ~/.openclaw/workspace/literature
search_queries:  # 搜索关键词组合
  - "metagenomics AND machine learning"
  - "fungal pathogen AND bioinformatics"
  - "single-cell AND deep learning"
high_impact_journals:
  - Nature
  - Cell
  - Science
  - Bioinformatics
```

---

## 🔧 工作流程

### Step 1: 文献采集 (`fetch_articles_with_abstracts`)

从三大数据库获取最新文献及摘要：

| 来源 | API | 查询范围 | 特点 |
|------|-----|----------|------|
| **PubMed** | EUtils | 最近 1 天 | 已发表论文，有 PMID |
| **bioRxiv** | REST API | 最近 1 天 | 预印本，DOI 格式 |
| **arXiv** | Export API | 最近 1 天 | CS/Q-Bio 类别 |

**执行逻辑：**
```python
for query in SEARCH_QUERIES:
    articles = fetch_pubmed(query)      # PubMed
    biorxiv = fetch_biorxiv()           # bioRxiv  
    arxiv = fetch_arxiv()               # arXiv
    all_articles.extend(...)
```

### Step 2: 语义筛选 (`categorize_article`)

根据关键词匹配筛选目标领域：

```python
CATEGORY_KEYWORDS = {
    "单细胞组学": ["single-cell", "scRNA-seq", "spatial transcriptomics"],
    "宏基因组学": ["metagenomics", "microbiome", "16S"],
    "病原真菌": ["fungal", "pathogen", "Candida", "Aspergillus"],
    "生信方法": ["bioinformatics", "algorithm", "pipeline", "tool"],
    "AI/ML": ["machine learning", "deep learning", "transformer"],
    "基因组学": ["genomics", "genome", "pan-genome"],
}
```

**优先级评分：**
- 高影响力期刊（Nature/Cell/Science）+10 分
- 方法开发类文章 +5 分
- 热门话题（单细胞/AI）+3 分

### Step 3: LLM 总结 (`generate_summary`)

基于摘要生成结构化中文总结：

```markdown
【研究目的】
【样本与方法】
【研究结果】
【创新性】
```

**优化要点：**
- 识别英文摘要 → 添加 `【】` 标签包裹各部分
- 长度控制在 5000 字以内
- 提取关键句子而非简单截断

### Step 4: 编辑排版 (`generate_mark_report_v2`)

生成完整的 Markdown 日报结构：

```markdown
# 📚 每日文献速递 - YYYY-MM-DD

## 📰 编辑前言
- 日期统计
- 来源分布
- 热点领域概览

## ⭐ 重点推荐 (8 篇)
- 带标签分类
- 结构化摘要
- DOI 链接

## 📖 完整文献列表
- 按来源分组
- 详细元数据

## 📝 编辑总结
- 今日趋势分析
- 编者点评
- 关注建议
```

---

## 📂 文件组织

```
literature-daily-report/
├── SKILL.md                    # 本说明文档
├── scripts/
│   └── literature_collector.py # 主收集脚本
└── references/
    ├── categories.md           # 领域分类标准
    ├── workflows.md            # 工作流指南
    └── api_docs.md             # API 参考文档

# 输出目录
~/.openclaw/workspace/literature/
├── literature-YYYY-MM-DD.md   # 当日报告
└── latest.md                   # 最新报告索引

# ClawLib 同步目录
~/.openclaw/workspace/ClawLib/科研日报/
├── literature-YYYY-MM-DD.md   # 当日报告（自动同步）
└── latest.md                   # 最新报告（自动同步）
```

---

## 🔄 自动同步

生成日报后会自动同步到 ClawLib：
- `literature-{date}.md` → `ClawLib/科研日报/`
- `latest.md` → `ClawLib/科研日报/`

---

## 📚 Zotero 集成 (v3.2)

文献收集完成后会自动录入 **BioCiaoLab Group Library**：

**功能特点：**
- PubMed 文献：通过 PMID 自动添加
- bioRxiv/arXiv 预印本：通过 DOI 自动添加
- 自动去重（已存在的文献会跳过）
- 添加标签：`literature-daily` + 日期 + 分类（如 `单细胞组学`, `宏基因组学`）
- **按文献归属类别**添加到对应的收藏夹（单细胞组学/宏基因组学/病原真菌/AI+ML/生信方法/基因组学等）

**BioCiaoLab Group Library 配置：**
```bash
export ZOTERO_API_KEY="your-api-key"
export ZOTERO_GROUP_ID="your-group-id"  # BioCiaoLab
```

获取方式：
1. **API Key**: https://www.zotero.org/settings/keys/new
2. **Group ID**: 访问 BioCiaoLab 小组页面，URL 中的数字部分即为 Group ID

---

## 🌟 高级用法

### 自定义搜索领域

在 `SEARCH_QUERIES` 中添加新主题：

```python
SEARCH_QUERIES = [
    '(epigenetics[Title/Abstract]) AND ((deep learning[Title/Abstract]))',
    '(CAR-T[Title/Abstract]) AND ((single-cell[Title/Abstract]))',
]
```

### 调整输出格式

修改 `generate_mark_report_v2()` 中的标题层级和标签风格。

### 定时任务

添加 crontab 自动发送日报：

```bash
# 每天早上 9 点生成并发送到飞书
0 1 * * * cd ~/.openclaw/workspace/projects/literature-collector && ./run.sh
```

---

## 🔄 迭代历史

- **v1.0**: 基础采集（标题 + 来源）
- **v2.0**: 增加摘要获取 + 智能总结
- **v3.0**: 中文格式优化 + 编辑结构化排版
- **v3.1**: 自动同步到 ClawLib 科研日报目录
- **v3.2**: 新增 Zotero 自动录入功能（PMID/DOI 自动添加）

---

## 📞 技术支持

遇到问题？检查：

1. API 限流 → 增加 `time.sleep()` 延时
2. 无结果 → 扩展搜索关键词范围
3. 格式异常 → 查看 `literature/abstract_cache.json` 缓存状态
