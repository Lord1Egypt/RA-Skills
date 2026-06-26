---
name: mao-selected-works
description: |
  触发：当用户要检索《毛泽东选集》全文、按卷或文章定位原文、按标题/关键词找内容时使用。此 skill 适用于 OpenClaw，本地默认使用结构化检索与关键词检索；只有在配置文件显式开启后，才使用向量召回和重排组成的混合检索。
---

# 毛选检索

## Overview

这个 skill 为 OpenClaw 提供《毛泽东选集》的本地知识库能力，包含 2 个部分：

- `scripts/build_index.py`：从 Markdown 建立 SQLite FTS 索引，并按配置决定是否生成向量索引
- `scripts/search.py`：按卷、篇、标题、关键词或混合检索查询文章与段落

默认模式不依赖外部 API，只使用本地结构化检索与全文检索。只有 `config/search.json` 中显式开启 `rag.enabled` 时，才会使用 embedding；只有 `rag.rerank.enabled` 也打开时，才会继续重排。

默认模型与平台约定：

- 嵌入模型：`BAAI/bge-m3`
- 重排模型：`BAAI/bge-reranker-v2-m3`
- 嵌入分批默认按 `64` 条请求，避免常见平台的单批上限
- 如果用户没有单独为 embedding / rerank 配置 `base_url` 和 `api_key_env`，则默认继承 `rag.api.base_url` 与 `rag.api.api_key_env`

## 何时使用

在这些场景调用本 skill：

- 用户要找《毛选》第几卷、某篇文章或某个主题出现在哪里
- 用户给出标题、别名或关键词，希望返回对应文章或相关段落
- 用户要求开启混合检索，并提供可用的 embedding / rerank API 配置

以下情况不要直接调用本 skill：

- 用户只是在讨论观点，不需要定位《毛选》原文
- 当前工作已经有准确文件路径和文本片段，不需要再次建索引或检索

## 工作流

### 1. 建立索引

直接运行：

```bash
python scripts/build_index.py
```

默认会建立：

- 文档级索引：按卷、篇、标题、别名、全文找文章
- 段落级索引：按关键词找命中片段

索引工具默认直接扫描 `data/` 目录下的 Markdown 文件。

如果 `config/search.json` 里开启了 `rag.enabled` 并配置好 embedding，则会同时生成向量索引。

### 2. 配置

API key 建议通过环境变量 `MAO_SKILL_API_KEY` 配置。

使用配置管理脚本：

```bash
# 查看当前配置
python scripts/config.py show

# 修改配置
python scripts/config.py set rag.api.base_url "https://api.siliconflow.cn/v1"
python scripts/config.py set rag.api.api_key_env "MAO_SKILL_API_KEY"
python scripts/config.py set rag.enabled true
python scripts/config.py set chunk_size 1024
python scripts/config.py set chunk_overlap 100
```

其他模型参数（如 `embedding.model`、`embedding.batch_size`、`rerank.model`）直接编辑 `config/search.json`。

### 3. 查询

常用查询方式：

按卷列文章：

```bash
python scripts/search.py catalog --volume 第一卷
```

按卷和篇直接定位文章：

```bash
python scripts/search.py show --volume 1 --chapter 3
```

按标题找文章：

```bash
python scripts/search.py show --title 实践论
```

按关键词搜段落：

```bash
python scripts/search.py search "调查研究"
```

显式开启混合检索：

```bash
python scripts/search.py search "统一战线" --mode hybrid
```

测试模型连通性：

```bash
python scripts/search.py test-model --target embedding
python scripts/search.py test-model --target rerank
```

如果没有配置 `rag.api.base_url`，或没有设置环境变量 `MAO_SKILL_API_KEY`，命令会直接提示用户先设置。

卷、篇、标题、关键词混合过滤：

```bash
python scripts/search.py search "调查研究" --volume 1 --chapter 7 --title 本本主义
```

## 输出要求

调用本 skill 时，返回结果必须优先给出可核对来源：

- 卷次
- 篇次
- 文章标题
- 日期（如果有）
- 命中的段落摘要
- 源文件路径或文档 ID
- 检索方式：`catalog`、`lexical`、`lexical-like`、`hybrid`、`hybrid-rerank`

如果没有命中，不要臆造答案。应明确说明：

- 没有在当前语料中检到
- 是标题未命中，还是关键词未命中
- 如果用户允许，可以建议补充别名、整理 metadata 或开启混合检索

## 参考资料

- 数据格式：`references/corpus-format.md`
- 检索规则：`references/retrieval-rules.md`
- 输出结构：`references/output-schema.md`
