---
name: openclaw-memory-ollama
description: OpenClaw 本地化记忆管理系统 — 构建稳定、高效、零成本的 AI 长期记忆解决方案。基于 Ollama（本地 Embedding）+ cognitive-brain（结构化存储）+ Memory Files（日常记忆）的三档存储架构。触发场景：(1) 用户需要为 AI 助手添加记忆功能 (2) 想要本地化部署向量数据库 (3) 需要基于 PostgreSQL + Redis 的记忆存储方案 (4) 需要完整的记忆系统部署指南 (5) 遇到 cognitive-brain 记忆功能异常需要排查。本技能引用 cognitive-brain 技能的代码和架构。
---

# OpenClaw Memory System

本地化 AI 记忆管理系统，为 OpenClaw AI 助手提供稳定、高效、零成本的长期记忆能力。

## 核心架构

**三层存储 + 四层记忆模型：**

| 层级 | 组件 | 说明 |
|------|------|------|
| 接入层 | 飞书 / WebChat / Gateway | 多渠道接入 |
| 服务层 | cognitive-brain + Ollama | Memory Service + Embedding |
| 存储层 | PostgreSQL + Redis + 文件 | 向量 + 缓存 + 文件 |

**四层记忆：**
- L1 感官记忆 — Redis，TTL 30秒
- L2 工作记忆 — Redis，TTL 60分钟
- L3 情景记忆 — PostgreSQL，永久
- L4 语义记忆 — PostgreSQL，永久

## 快速开始

### 1. 环境要求

- OpenClaw 已安装运行
- Ollama 已安装，`nomic-embed-text` 模型已拉取
- PostgreSQL + Redis 服务运行中
- cognitive-brain 技能已安装

### 2. 配置步骤

```bash
# Step 1: 配置 Ollama 环境变量
export OLLAMA_API_KEY=ollama-local
export OLLAMA_HOST=localhost:11434

# Step 2: 配置 cognitive-brain (见 references/config-reference.md)
# 修改 config.json 中的 provider 设置

# Step 3: 重启 OpenClaw Gateway
openclaw gateway restart
```

### 3. 验证

```bash
# 验证 Embedding 服务
python3 scripts/embed.py --warmup

# 验证记忆检索
memory_search 测试查询
```

## 核心脚本

- `scripts/embed.py --warmup` — 预热 Embedding 服务
- `scripts/embed.py <文本>` — 生成文本向量

## 🔗 引用与致谢

### 直接引用的技能和代码

| 引用来源 | 引用内容 | 说明 |
|---------|---------|------|
| **cognitive-brain** | brain.encode() / brain.recall() 接口、episodes/concepts 表结构、Redis 缓存逻辑 | 核心记忆服务架构 |
| **Ollama** | nomic-embed-text 模型、/api/embeddings 接口 | 本地 Embedding 服务 |
| **pgvector** | 向量存储、ivfflat 索引、vector_cosine_ops | PostgreSQL 向量扩展 |

### 架构参考

| 参考来源 | 引用内容 |
|---------|---------|
| **lark-whiteboard** | 系统架构图、数据流图、四层记忆模型（小明使用此技能绘制）| PNG 图片 |
| **ppt-generator** | HTML 演示稿模板、乔布斯风设计规范 | 输出样式参考 |

### 工具链

| 工具 | 用途 |
|------|------|
| **Ollama** | 本地 LLM 和 Embedding 运行服务 |
| **PostgreSQL** | 关系数据库 + 向量存储 |
| **Redis** | 热缓存、L1/L2 记忆存储 |
| **ClawHub** | 技能发布和管理平台 |
| **OpenClaw** | AI 助手框架 |

### 开发者贡献

- **小明 (xiaoming)** — 使用 lark-whiteboard 技能绘制三张架构图

## 参考文档

- [架构图参考](references/architecture.md) — 系统架构、数据流图、四层记忆模型
- [部署实施指南](references/deployment.md) — 完整部署步骤
- [配置参考](references/config-reference.md) — 配置文件详解
