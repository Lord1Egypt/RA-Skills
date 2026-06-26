# huo15-knowledge-base

> 基于 Andrej Karpathy LLM Knowledge Bases 方案，让 LLM 成为你的"研究图书馆员"

## 核心理念

传统 RAG 方案：文档 → 分块 → 向量数据库 → 相似性检索 → LLM

Karpathy 方案：原始文档 → LLM 主动编译 → 结构化 Markdown Wiki → LLM 直接阅读

**区别：AI 不是在"检索"，而是在"查阅百科全书"**

## 快速开始

```bash
# 初始化
./scripts/init.sh

# 入库一篇文档
./scripts/ingest.sh --url "https://arxiv.org/abs/1706.03762"

# 编译成 wiki
./scripts/compile.sh

# 搜索
./scripts/search.sh "attention mechanism"

# 体检
./scripts/lint.sh
```

## 目录结构

```
raw/          原始资料（论文、网页、笔记）
wiki/         LLM 编译后的百科全书
cache/        临时缓存
```

## 与记忆系统的区别

| | huo15-memory-evolution | huo15-knowledge-base |
|--|---|---|
| 本质 | Agent 的"记忆" | 外部知识的"图书馆" |
| 内容 | 决策、偏好、上下文 | 论文、文档、百科 |
| 维护 | 自己维护自己 | LLM 整理维护 |
| 可审计 | 是 | 是（人类可读 Markdown）|

## License

MIT
