# CLAUDE.md

**项目：huo15-knowledge-base** — LLM 驱动的结构化知识库

## 背景

基于 Andrej Karpathy 的 LLM Knowledge Bases 方案：
- 用 LLM 作为"研究图书馆员"，主动编译和维护 Markdown 知识库
- 绕过传统 RAG 的向量数据库，用人类可读的 Wiki 代替黑盒 embedding
- 核心创新：** Compilation Step** — LLM 读取 raw/ 原始文档，生成结构化 wiki

## 架构

```
raw/   → 原始文档入库（按日期分目录）
wiki/  → LLM 编译后的百科全书（Markdown）
cache/ → 临时缓存
```

## 核心脚本

| 脚本 | 作用 |
|------|------|
| `init.sh` | 初始化目录结构 |
| `ingest.sh` | 文档入库（支持 URL/文件/文本）|
| `compile.sh` | 全量/增量编译 raw → wiki |
| `lint.sh` | wiki 自愈体检 |
| `search.sh` | 搜索 wiki 内容 |
| `index.sh` | 生成 wiki 索引 |

## 开发规范

- 所有数据存 Markdown，纯文本友好
- LLM 调用通过 OpenClaw API，不硬编码模型
- 配置通过 `config.json`，敏感信息不上传
- 与 memory-evolution 通过 `memory/reference/` 类型桥接
