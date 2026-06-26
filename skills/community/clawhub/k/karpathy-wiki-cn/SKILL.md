---
name: karpathy-wiki
description: 基于 Karpathy LLM Wiki 模式，为科研工作建立和维护持久化知识库。
  当用户提到建立知识库、LLM Wiki、Karpathy 方法、Obsidian 知识管理、论文管理、
  研究笔记、摄入论文、维护 Wiki 时使用。
---

# Karpathy LLM Wiki — 科研知识库

## 触发条件
- 建立 LLM 知识库 / Karpathy Wiki
- 管理论文、研究笔记
- 摄入（Ingest）新的论文或资料
- 对知识库提问（Query）
- 维护知识库健康（Lint）

## 核心思想

和传统 RAG 不同——RAG 每次提问都从零开始检索、重新拼凑答案——Karpathy 模式让 LLM **持续构建和维护一个持久化的 wiki**。新资料进来后，LLM 不是简单索引它，而是提取关键信息、整合到现有 wiki 中、更新实体页、修订主题摘要、标记新旧资料之间的矛盾。知识被编译一次，然后持续保持最新，而不是每次查询都重新推导。

**Wiki 是一个持久化、不断复利的产物。** 交叉引用已经在那里了，矛盾已经被标记，综合摘要已经反映了你读过的所有内容。

你从不自己写 wiki 页面——LLM 写和维护所有内容。你负责提供资料、提问、引导方向。LLM 负责摘要、交叉引用、归档和簿记。

## 系统架构

### 三层结构

- **Raw sources（原始资料）**：你收集的论文、文章、数据文件。不可变——LLM 只读不改，这是真相来源。
- **The wiki（知识库）**：LLM 生成的 markdown 文件集合。LLM 全权负责这个层，你只读不写。
- **The schema（配置）**：你正在读的 CLAUDE.md/SKILL.md。它告诉 LLM wiki 的结构、约定和工作流。这个文件不是一成不变的——你和 LLM 随着使用共同演化它。

### 目录结构

```
research-wiki/
├── CLAUDE.md          # Schema：告诉 LLM 如何维护 Wiki
├── raw/               # 原始资料（不可变，只进不改）
│   ├── papers/        # PDF 论文
│   ├── articles/      # Markdown/Web 文章
│   ├── images/        # 图片资源
│   └── data/          # 数据文件
├── wiki/              # LLM 维护的 Wiki（LLM 全权负责）
│   ├── index.md       # 内容目录（每个页面 + 一行摘要）
│   ├── log.md         # 操作日志（只追加）
│   ├── overview.md    # 研究主题概述
│   ├── entities/      # 研究实体页
│   ├── concepts/      # 核心概念页
│   ├── papers/        # 论文摘要页
│   └── synthesis/     # 综合分析（Query 产物存回）
└── assets/            # 图片附件
```

> 页面格式和目录结构只是起点，不是铁律。根据你的研究领域和偏好，和 LLM 一起调整。

## 核心操作

### 1. Ingest（摄入新资料）
当用户提供论文、文章或其他资料时：

1. 将资料保存到 `raw/` 对应子目录
2. 读取资料内容，与用户讨论关键要点
3. 在 `wiki/papers/` 创建论文摘要页
4. 在 `wiki/concepts/` 更新或创建相关概念页
5. 在 `wiki/entities/` 更新或创建相关实体页（学者、机构、方法名等）
6. 更新 `wiki/index.md` 添加新页面索引
7. 追加 `wiki/log.md` 记录本次摄入（格式：`## [YYYY-MM-DD] ingest | 论文标题`）。文件引用使用 Markdown 标准链接 `[文件名](路径)`，确保 VSCode Markdown Preview 中可点击
8. 向用户汇报：触及了多少个 Wiki 页面

一篇资料可能触及 10-15 个 wiki 页面。建议逐篇摄入、保持参与——阅读摘要、检查更新、引导 LLM 强调重点。当然也可以批量摄入，取决于你的工作风格。

### 2. Query（对知识库提问）
当用户提出问题：

1. 先读 `wiki/index.md` 找到相关页面
2. 深入阅读相关 Wiki 页面
3. 综合回答，引用具体来源
4. **如果回答有持续价值（对比分析、主题梳理、新发现），存回 `wiki/synthesis/` 作为新页面**——你的探索也在为知识库积累知识，不应消失在聊天记录里
5. 追加 `wiki/log.md` 记录本次查询

Query 产物可以是多种格式：markdown 页面、对比表、演示文稿（Marp）、图表（matplotlib）。好的分析应该像 ingested sources 一样复利增长。

### 3. Lint（健康检查）
当用户要求维护或定期检查：

1. 扫描所有 Wiki 页面，查找：
   - 页面间的矛盾或不一致
   - 过时声明（被新论文/来源推翻的旧观点）
   - 孤立页面（没有入站链接）
   - 文中提到但未建立页面的重要概念
   - 缺失的交叉引用
   - 可以填补的数据缺口
2. 自动修复能发现的问题
3. 报告需要人工判断的问题
4. 建议值得追问的新问题和值得补充的新来源
5. 追加 `wiki/log.md` 记录维护结果

## 页面格式规范

以下格式是建议起点，可根据领域调整。

### 论文摘要页（wiki/papers/）
```markdown
---
title: "论文完整标题"
authors: ["作者1", "作者2"]
year: 2024
venue: "会议/期刊名"
tags: [标签1, 标签2]
ingested: 2026-04-21
---

## 核心问题
本文要解决什么问题？

## 方法
核心方法是什么？

## 关键发现
- 主要结果1
- 主要结果2

## 与Wiki的关系
[[相关概念页]]
[[其他相关论文]]

## 笔记
任何额外的观察和笔记
```

### 概念页（wiki/concepts/）
```markdown
---
topic: 概念名称
tags: [类别标签]
created: 2026-04-21
---

## 定义
这个概念是什么？

## 关键要点
- 要点1
- 要点2

## 相关论文
[[论文1]]
[[论文2]]

## 相关概念
[[相关概念]]

## 笔记
补充信息
```

## index.md 和 log.md

**index.md** 是内容导向的目录——列出 wiki 中每个页面的链接和一行摘要，按类别（论文、概念、实体、综合分析）组织。LLM 在每次 ingest 时更新它。查询时 LLM 先读 index 找相关页面，再深入阅读。在中等规模（~100 篇论文，几百个页面）效果很好，不需要 embedding-based RAG 基础设施。

**log.md** 是时间线日志——追加记录发生了什么（ingest、query、lint）。每条以一致前缀开头（如 `## [YYYY-MM-DD] ingest | 标题`），可以用简单 unix 工具查询：`grep "^## \[" log.md | tail -5` 得到最近 5 条记录。log.md 在 wiki/ 目录下，文件链接使用相对于 wiki/ 的路径：`[文件名](concepts/xxx.md)`、`[文件名](papers/xxx.md)`、`[文件名](../raw/papers/xxx.pdf)`。

## Bundled Scripts

### `scripts/search-agent-papers.sh`
搜索 arXiv 最新的智能体方向论文并下载 PDF 到 `raw/papers/`。
用法：`bash scripts/search-agent-papers.sh [output_dir] [max_papers]`
- 自动查询 arXiv API，按提交日期排序
- 默认取 5 篇，输出到 `raw/papers/`
- 去重 + 跳过 2025-04-01 之前的论文
- 下载后可直接触发 Ingest 流程

## 可选工具生态

随着 wiki 增长，你可能需要这些配套工具：

- **[qmd](https://github.com/tobi/qmd)** — 本地 markdown 搜索引擎（BM25 + 向量混合 + LLM 重排序）。wiki 页面多时比 index.md 更高效。有 CLI（LLM 可 shell 调用）和 MCP server。
- **[Marp](https://marp.app/)** — markdown 转演示文稿。可以直接从 wiki 内容生成幻灯片。
- **Dataview** — Obsidian 插件，对页面 frontmatter 跑查询，生成动态表格和列表。
- **本地图片管理** — 下载文章图片到 `assets/`，让 LLM 能直接查看和引用图片，而不是依赖可能失效的 URL。
- Wiki 本质上是 git repo，免费获得版本历史、分支和协作能力。

## 为什么有效

维护知识库最烦的部分不是阅读和思考——而是簿记。更新交叉引用、保持摘要最新、标记新旧矛盾、维持几十页的一致性。人类放弃 wiki 是因为维护负担增长比价值还快。LLM 不会厌倦、不会忘记更新交叉引用、一次可以改 15 个文件。wiki 能保持维护是因为维护成本接近零。

人的工作是筛选资料、引导分析、提出好问题、思考这一切意味着什么。LLM 的工作是剩下的所有事。

> 本文档基于 Andrej Karpathy 的 LLM Wiki 方法论改编，原始 gist：https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
> 该文档发布于 2026 年 4 月，获得 88,000+ 收藏。本 skill 将其适配为中文科研场景。

这个理念可以追溯到 Vannevar Bush 1945 年的 Memex 构想——一个私人的、主动策展的知识库，文档之间的关联路径和文档本身一样有价值。他没能解决的问题是：谁来做维护？LLM 回答了这个问题。
