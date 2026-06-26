---
name: literature-review-automator
description: 自动检索学术文献（Semantic Scholar/arXiv/CrossRef），进行相关性筛选、主题聚类分析，并生成综述草稿（支持本地模板或大模型润色）。适用于快速了解某个研究方向的前沿动态。
version: 1.0.0
author: 智能装备研究所
tags:
  - literature-review
  - academic-search
  - summarization
  - research-assistant
trigger:
  - keyword: 文献综述
  - keyword: 检索文献
  - keyword: 写一篇综述
  - keyword: 研究热点
  - keyword: 论文检索
requirements:
  - python3
  - pip install requests
  - (可选) pip install scikit-learn numpy
  - (可选) pip install sentence-transformers bertopic
  - 网络连接（用于调用学术API）
  - (可选) 大模型API密钥（DeepSeek/OpenAI/阿里云）
configurable:
  - name: default_years
    type: int
    default: 5
    description: 默认检索年数
  - name: max_papers
    type: int
    default: 50
    description: 最大保留文献数
  - name: use_llm_for_writing
    type: bool
    default: false
    description: 是否使用大模型润色综述
  - name: llm_model
    type: str
    default: deepseek-chat
    description: 大模型名称（需配置API密钥）
  - name: llm_api_base
    type: str
    default: https://api.deepseek.com/v1
    description: 大模型API端点
  - name: output_format
    type: str
    default: markdown
    enum: [markdown, docx, txt]
    description: 输出文档格式
  - name: human_review_papers
    type: bool
    default: false
    description: 是否在筛选后请求用户确认文献列表
entry_point: main.py
---

# 文献智能检索与综述生成器

## 功能描述

根据用户提供的研究主题（关键词或问题），自动在多个公共学术数据库（Semantic Scholar、arXiv、CrossRef）中检索相关文献，经相关性筛选、去重、主题聚类分析后，生成结构化综述文档（含摘要、分主题讨论、趋势分析、参考文献列表）。

**使用示例**：
- "帮我检索近3年关于'联邦学习在工业视觉中的应用'的文献，写一篇综述。"
- "追踪'大模型微调技术'的最新进展，给我一份热点概览。"
- "我想了解'柔性机器人'领域的研究趋势，输出综述报告。"

## 执行流程

该技能按以下阶段顺序执行，每个阶段失败时会自动重试或给出明确错误提示。

### 1. 请求解析
- 从用户输入中提取：核心关键词、时间范围、最大文献数、输出格式等。
- 若用户未提供，使用配置文件中的默认值。
- 自动生成英文同义词和字段变体。

### 2. 文献检索
- 并发调用以下API（优先使用Semantic Scholar，返回结果快且丰富）：
  - **Semantic Scholar API**：`https://api.semanticscholar.org/graph/v1/paper/search`
  - **arXiv API**：`http://export.arxiv.org/api/query`
  - **CrossRef API**：`https://api.crossref.org/works`
- 检索参数：关键词、出版年份范围、按相关性排序、每页最多100条。
- 合并去重（基于DOI或标题相似度）。

### 3. 相关性筛选（本地）
- 对摘要和标题进行关键词匹配或TF-IDF向量化，计算与用户关键词的余弦相似度。
- 按相似度降序排序，结合引用数加权，保留前 `max_papers` 篇。
- 若 `human_review_papers = true`，则生成候选列表并询问用户是否采纳或手动剔除。

### 4. 主题聚类分析（可选，本地）
- 如果安装了 `sentence-transformers` 和 `bertopic`，自动对摘要进行BERTopic聚类。
- 否则使用基于关键词的简单分组。
- 输出：每个聚类的主题词、代表性论文、论文数量。
- 同时统计每年发文量，生成趋势文本描述。

### 5. 综述草稿生成
支持两种模式：

**模式A（纯本地，零API费用）**：
- 根据聚类结果按大纲自动生成结构化综述，包含：
  - 摘要（基于检索到的论文数量和主要聚类方向）
  - 主要研究方向（按主题分类，附带代表性论文关键信息）
  - 研究趋势与挑战（年度发文趋势、热门期刊、潜在研究机会）
  - 参考文献列表（含DOI和链接）

**模式B（大模型润色，可选）**：
- 将本地生成的草稿和论文摘要输入大模型，生成更流畅的综述文本。

## 文件结构

```
lit_review/
├── skill.md           # 技能元数据定义
├── lit_review.py      # 核心实现（主入口）
├── config.json        # 配置文件
├── requirements.txt   # Python依赖
├── README.md          # 使用说明
└── test.py            # 测试脚本
```
