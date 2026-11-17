---
name: lit-review
version: 1.1.0
description: "Conduct structured literature reviews with systematic search and synthesis"
tags: [documentation, general, api-integration, template-based, file-based]
---

# 文献智能检索与综述生成 v1.1

## 功能描述

根据用户提供的研究主题（关键词或问题），自动在多个公共学术数据库（Semantic Scholar、arXiv、CrossRef）中检索相关文献，经相关性筛选、去重、主题聚类分析后，生成结构化综述文档（含摘要、分主题讨论、趋势分析、参考文献列表）�?
## 什么时候使�?
- 用户要求检索学术文�?- 用户要求写文献综�?- 用户要求了解某领域研究热�?- 用户要求追踪某方向最新进�?- 用户提到"文献综述"�?检索文�?�?写一篇综�?�?研究热点"�?论文检�?

**使用示例**�?- "帮我检索近3年关�?联邦学习在工业视觉中的应�?的文献，写一篇综�?
- "追踪'大模型微调技�?的最新进展，给我一份热点概�?
- "我想了解'柔性机器人'领域的研究趋势，输出综述报告"

## 执行流程

该技能按以下阶段顺序执行，每个阶段失败时会自动重试或给出明确错误提示�?
### 1. 请求解析
- 从用户输入中提取：核心关键词、时间范围、最大文献数、输出格式等
- 若用户未提供，使用配置文件中的默认值（默认5年�?0篇）
- 自动生成英文同义词和字段变体

### 2. 文献检�?- 并发调用以下API（优先使用Semantic Scholar，返回结果快且丰富）�?  - **Semantic Scholar API**：`https://api.semanticscholar.org/graph/v1/paper/search`
  - **arXiv API**：`http://export.arxiv.org/api/query`
  - **CrossRef API**：`https://api.crossref.org/works`
- 检索参数：关键词、出版年份范围、按相关性排序、每页最�?00�?- 合并去重（基于DOI或标题相似度�?
### 3. 相关性筛选（本地�?- 对摘要和标题进行关键词匹配或TF-IDF向量化，计算与用户关键词的余弦相似度
- 按相似度降序排序，结合引用数加权，保留前 `max_papers` �?- �?`human_review_papers = true`，则生成候选列表并询问用户是否采纳或手动剔�?
### 4. 主题聚类分析（可选，本地�?- 如果安装�?`sentence-transformers` �?`bertopic`，自动对摘要进行BERTopic聚类
- 否则使用基于关键词的简单分�?- 输出：每个聚类的主题词、代表性论文、论文数�?- 同时统计每年发文量，生成趋势文本描述

### 5. 综述草稿生成

支持两种模式�?
**模式A（纯本地，零API费用�?*�?- 根据聚类结果按大纲自动生成结构化综述，包含：
  - 摘要（基于检索到的论文数量和主要聚类方向�?  - 主要研究方向（按主题分类，附带代表性论文关键信息）
  - 研究趋势与挑战（年度发文趋势、热门期刊、潜在研究机会）
  - 参考文献列表（含DOI和链接）

**模式B（大模型润色，可选）**�?- 将本地生成的草稿和论文摘要输入大模型，生成更流畅的综述文�?
## 运行方式

```bash
cd skills/lit-review
python main.py --topic "embodied intelligence for industrial manufacturing" --years 5 --max_papers 30
```

### 参数说明

| 参数 | 说明 | 默认�?|
|------|------|--------|
| --topic | 研究主题（必填） | - |
| --years | 检索年�?| 5 |
| --max_papers | 最大保留文献数 | 50 |
| --output | 输出文件路径（不含后缀�?| literature_review |
| --config | JSON配置字符�?| {} |

### 配置选项（通过 --config 传入�?
| 选项 | 类型 | 默认�?| 说明 |
|------|------|--------|------|
| use_llm_for_writing | bool | false | 是否使用大模型润色综�?|
| llm_model | str | deepseek-chat | 大模型名�?|
| llm_api_base | str | https://api.deepseek.com/v1 | 大模型API端点 |
| llm_api_key | str | - | 大模型API密钥（需配置�?|
| output_format | str | markdown | 输出格式（markdown/docx/txt�?|
| human_review_papers | bool | false | 是否请求用户确认文献列表 |

## 错误处理与降级策�?
### API 故障
| 场景 | 处理方式 |
|------|---------|
| Semantic Scholar API 超时 | 等待 10s 超时 �?跳过，使�?arXiv + CrossRef 结果 |
| Semantic Scholar 返回 429 | 限流 �?等待 5s 重试 �?仍失败则跳过 |
| arXiv API 无响�?| 跳过 arXiv，使用其他源 |
| CrossRef API 返回错误 | 跳过 CrossRef，使用其他源 |
| 所�?API 均失�?| 输出"所有学术数据源暂不可用，请检查网络连�? |
| 检索结果为 0 �?| 提示"未找到相关文献，建议更换关键词或扩大时间范围" |

### 计算异常
| 场景 | 处理方式 |
|------|---------|
| TF-IDF 向量化失�?| 降级到关键词匹配模式 |
| 聚类失败（依赖缺失） | 使用简单关键词分组替代 BERTopic |
| 大模型调用失�?| 降级到本地模板生成（模式A�?|
| 输出文件写入失败 | 提示检查磁盘空间和路径权限 |

### 数据质量
| 场景 | 处理方式 |
|------|---------|
| 论文无摘�?| 仅使用标题进行相关性计�?|
| 论文�?DOI | 使用标题+年份作为去重�?|
| 作者信息缺�?| 标注"未知作�? |

## 文件结构

```
lit-review/
├── SKILL.md           # 技能文�?├── main.py            # 核心实现（主入口�?├── lit_review.py      # 核心实现（备用入口）
├── config.json        # 配置文件
├── requirements.txt   # Python依赖
├── README.md          # 使用说明
└── test.py            # 测试脚本
```

## 依赖

### 核心依赖
```bash
pip install requests scikit-learn numpy
```

### 可选依�?```bash
pip install sentence-transformers bertopic  # 高级主题聚类
pip install python-docx                      # DOCX格式输出
```

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.1.0 | 2026-06-29 | 修复乱码、完善frontmatter、增加错误处理和降级策略、依赖声�?|
| 1.0.0 | 2026-06-15 | 初始版本 |
