---
name: kinema-concept-research
displayName: "Kinema's Concept Re-Search"
version: 1.0.4
description: |
  Research whether a concept has been implemented and its current state. Use multi-language keywords, multi-engine cross-validation, and multi-dimensional search.
  When user proposes an idea or concept, systematically research its existing solutions through a structured search process.
  Trigger: User asks "has anyone done this", "check the status of xxx", "research xxx", etc.
---

# Concept Research - Concept Status Research | 概念现状调研

- **Author**: [LeeShunEE](https://github.com/LeeShunEE)
- **Organization**: [KinemaClawWorkspace](https://github.com/KinemaClawWorkspace)
- **GitHub**: https://github.com/KinemaClawWorkspace/kinema-concept-research

Research whether a concept has been implemented and what it looks like. Search thoroughly and output a summary list.

调查一个概念是否已被实现、做成什么样子。彻底搜索，输出摘要清单。

## Workflow | 工作流

### Phase 1: Concept Clarification (Dialogue) | 阶段 1: 概念澄清（对话）

Through multi-turn dialogue clarify: | 通过多轮对话明确：
- What user wants to do | 用户想做什么
- Core functionality | 核心功能是什么
- Target users | 目标用户是谁
- Differentiation expectations | 差异化期望是什么

**Output**: One-sentence concept definition | **产出**: 一句话概念定义

### Phase 2: Keyword Breakdown | 阶段 2: 关键词拆解

Based on concept definition, break down into multiple keyword groups: | 基于概念定义，拆解为多组关键词：

1. Core word variants - synonyms, near-synonyms, different expressions | 核心词变体 - 同义词、近义词、不同表述
2. Tech stack words - involved technologies, frameworks, protocols | 技术栈词 - 涉及的技术、框架、协议
3. Scenario words - use cases, problems to solve | 场景词 - 使用场景、解决的问题
4. Combined words - core word + tech/scenario | 组合词 - 核心词 + 技术/场景

Generate Chinese and English versions for each group. | 每组生成中英文版本。

### Phase 3: Broad Search | 阶段 3: 广度搜索

Search using searxng-search batch by batch: | 使用 searxng-search 逐批搜索：

1. Search 1-2 pages for each keyword group | 每组关键词搜索 1-2 页结果
2. Record all relevant links | 记录所有相关链接
3. Preliminary relevance marking based on title/abstract | 根据标题/摘要初步标记相关性

Time filter (if search engine supports): | 时间过滤（如搜索引擎支持）:
- Five years ago, two years ago, one year ago, three months ago, recent three months | 五年之前、两年之前、一年之前、三个月之前、最近三个月

### Phase 4: Deep Exploration | 阶段 4: 深度探索

From high-relevance results, select 3-5 for deep exploration: | 从高相关性结果中挑选 3-5 个进行深度探索：

1. Web pages: Use web_fetch to grab content | Web 页面: 使用 web_fetch 抓取内容
2. GitHub Repo: Clone locally, read README | GitHub Repo: 克隆到本地，阅读 README
3. PDF/Papers: Download and read | PDF/论文: 下载阅读

Record exploration content: | 探索内容记录：
- Core functionality | 核心功能
- Technical implementation | 技术实现
- Pros and cons | 优缺点
- Similarities/differences with user concept | 与用户概念的异同

### Phase 5: Output Report | 阶段 5: 输出报告

Generate summary list: | 生成摘要清单：

| Field | Description | 说明 |
|-------|-------------|------|
| Link | Original URL | 链接 |
| Overview | What it is, what it does | 概述 |
| Basic Approach | Core technical solution | 基本思路 |
| Similarities | Common points with user concept | 相同点 |
| Differences | Differences from user concept | 不同点 |
| Analysis | Opportunities, improvement space | 分析 |

## Project Directory | 项目目录

All files saved in: `projects/research-{uuid}/` | 所有文件保存在：`projects/research-{uuid}/`

```
projects/research-{uuid}/
├── concepts/
│   └── definition.md
├── keywords/
│   └── keywords.md
├── search/
│   ├── broad/
│   └── deep/
├── repos/
├── papers/
└── report.md
```

## Search Tools | 搜索工具

Priority: searxng-search. If SearXNG not deployed, can use ddg-search. | 优先使用 searxng-search。如 SearXNG 未部署，可使用 ddg-search。

---

## Related Documentation | 相关文档

- searxng-search skill
- skill-creator skill
