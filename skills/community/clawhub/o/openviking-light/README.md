# OpenViking Light

> A lightweight RAG knowledge base for AI agents — BM25 full-text search + MiniMax LLM.

[English](#english) | [中文](#中文)

---

## English

### Overview

OpenViking Light is a lightweight RAG (Retrieval-Augmented Generation) knowledge base built for AI agents. It uses **BM25** (a proven full-text search algorithm from Elasticsearch) for retrieval and **MiniMax M2.7** for answer generation. No external embedding API required — everything runs locally.

### Features

- **BM25 Retrieval** — Pure Python implementation with jieba Chinese word segmentation
- **MiniMax LLM** — OpenAI-compatible API for intelligent answer synthesis
- **Zero External Dependencies for Retrieval** — Search runs 100% locally
- **Simple JSON Storage** — No database, no vectors, just a JSON file
- **OpenClaw Skill** — Ready to use as a drop-in skill for OpenClaw agents

### Architecture

```
User Query → BM25 Retrieval (local) → Top-K Chunks → MiniMax LLM → Answer
```

### Setup

**Requirements:**
- Python 3.9+
- `jieba` (auto-installed if missing)
- `MiniMax API Key` (set in environment)

**Environment Variables:**
```bash
export MINIMAX_API_KEY="your-api-key"
export MINIMAX_API_HOST="https://api.minimaxi.com"  # or your region endpoint
```

**Quick Install:**
```bash
# Install as OpenClaw skill (via ClawHub)
clawhub install openviking-light
```

### Usage

```bash
# Add knowledge to the database
python3 scripts/store.py --content "Your knowledge content" --title "Title"

# Search (retrieval only, no LLM)
python3 scripts/search.py --query "your question"

# RAG Q&A (retrieve + generate)
python3 scripts/ask.py --query "your question" --limit 5
```

### Scripts

| Script | Description |
|--------|-------------|
| `store.py` | Add content to knowledge base |
| `search.py` | BM25 full-text search |
| `ask.py` | RAG Q&A (search + MiniMax LLM) |
| `bm25.py` | All-in-one CLI (add/search/ask/stats) |

### Example

```bash
# Add investment knowledge
python3 scripts/store.py \
  --content "PEG = P/E ÷ earnings growth rate. PEG < 1 means growth is undervalued." \
  --title "Peter Lynch PEG Ratio"

# Ask a question
python3 scripts/ask.py --query "What is PEG ratio and how to use it?"
```

### Knowledge Base Content (Pre-loaded)

9 classic investment frameworks are pre-loaded:

| # | Book/Framework | Core Metrics |
|---|----------------|-------------|
| 1 | Graham — *The Intelligent Investor* | Graham Number, P/E, P/B |
| 2 | Klarman — *Margin of Safety* | NCAV, margin of safety discount |
| 3 | Buffett — *Letters to Shareholders* | ROE, moat (5 sources) |
| 4 | Peter Lynch — *Beating the Street* | PEG, P/S |
| 5 | Fisher — *Super Stock* | P/S, Fisher Four M |
| 6 | O'Neil — CAN SLIM | C/A/N/S/L/I/M |
| 7 | Sperandeo — 2B / 123法则 | 2B法则, trend confirmation |
| 8 | Kelly Criterion | Optimal position sizing |
| 9 | *The Snowball* | Compound interest phases |

---

## 中文

### 概述

OpenViking Light 是为 AI Agent 打造的轻量级 RAG（检索增强生成）知识库。采用 **BM25** 全文检索算法（Elasticsearch 内核）进行检索，**MiniMax M2.7** 进行回答生成。不依赖任何外部 embedding 服务，纯本地运行。

### 特点

- **BM25 检索** — 纯 Python 实现，jieba 中文分词
- **MiniMax LLM** — OpenAI-compatible API，智能回答生成
- **检索零外部依赖** — 100% 本地运行
- **JSON 存储** — 无数据库、无向量，纯文件存储
- **OpenClaw Skill** — 可直接作为 OpenClaw Agent 技能安装

### 工作原理

```
用户查询 → BM25 本地检索 → Top-K 相关内容 → MiniMax LLM → 生成回答
```

### 安装

**环境要求：**
- Python 3.9+
- `jieba`（自动安装）
- `MiniMax API Key`（环境变量配置）

**环境变量：**
```bash
export MINIMAX_API_KEY="your-api-key"
export MINIMAX_API_HOST="https://api.minimaxi.com"
```

**快速安装：**
```bash
# 通过 ClawHub 安装为 OpenClaw Skill
clawhub install openviking-light
```

### 使用方法

```bash
# 添加知识
python3 scripts/store.py --content "知识内容" --title "标题"

# 搜索（纯检索，不用 LLM）
python3 scripts/search.py --query "关键词"

# RAG 问答（检索 + 生成）
python3 scripts/ask.py --query "问题" --limit 5
```

### 脚本说明

| 脚本 | 功能 |
|------|------|
| `store.py` | 添加内容到知识库 |
| `search.py` | BM25 全文搜索 |
| `ask.py` | RAG 问答（检索+LLM生成） |
| `bm25.py` | 综合 CLI（add/search/ask/stats） |

### 预置知识库内容

已内置 9 个经典投资框架：

| # | 书名/框架 | 核心指标 |
|---|----------|---------|
| 1 | 格雷厄姆《聪明的投资者》 | 格雷厄姆数、P/E、P/B |
| 2 | 卡拉曼《安全边际》 | NCAV、安全边际折扣 |
| 3 | 巴菲特《给股东的信》 | ROE、护城河5来源 |
| 4 | 彼得·林奇《成功投资》 | PEG、P/S |
| 5 | 费雪《超级强势股》 | P/S、Fisher Four M |
| 6 | 欧奈尔 CAN SLIM | C/A/N/S/L/I/M |
| 7 | 斯波朗迪 2B/123法则 | 底部2B、趋势确认 |
| 8 | 凯利公式与仓位管理 | 最优仓位、2%止损 |
| 9 | 《滚雪球》巴菲特传记 | 复利三阶段 |

---

## License

MIT

## Publish / 发布

```bash
clawhub publish ./openviking-light \
  --slug openviking-light \
  --name "OpenViking Light" \
  --version 1.0.0 \
  --changelog "Initial release: BM25 + MiniMax LLM RAG knowledge base"
```
