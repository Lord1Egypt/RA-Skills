# OpenClaw Local Memory System

基于 Ollama 的 OpenClaw 本地化记忆管理系统，为 AI 助手提供稳定、高效、零成本的长期记忆能力。

## 🎯 特性

- **本地化部署** — 无需第三方服务，完全自主控制
- **零成本运行** — 无需 API Key，无订阅费用
- **高性能检索** — 语义搜索响应 ~40ms
- **四层记忆架构** — 感官/工作/情景/语义分层管理

## 🏗️ 架构

```
接入层: 飞书 / WebChat / OpenClaw Gateway
    ↓
服务层: cognitive-brain + Ollama (nomic-embed-text)
    ↓
存储层: PostgreSQL + Redis + 本地文件
```

## 📦 四层记忆模型

| 层级 | 名称 | 存储 | TTL |
|------|------|------|-----|
| L1 | 感官记忆 | Redis | 30秒 |
| L2 | 工作记忆 | Redis | 60分钟 |
| L3 | 情景记忆 | PostgreSQL | 永久 |
| L4 | 语义记忆 | PostgreSQL | 永久 |

## 🚀 快速开始

### 环境要求

- OpenClaw 已安装
- Ollama 已安装，`nomic-embed-text` 模型已拉取
- PostgreSQL + Redis 运行中
- cognitive-brain 技能已安装

### 部署步骤

1. 配置 Ollama 环境变量
2. 配置 cognitive-brain (provider: ollama)
3. 配置 OpenClaw memorySearch
4. 重启 Gateway

详见 [部署指南](references/deployment.md)

## 🔗 引用与致谢

### 直接引用的技能和代码

| 引用来源 | 引用内容 | 来源链接 |
|---------|---------|---------|
| **cognitive-brain** | brain.encode() / brain.recall() 接口、episodes/concepts 表结构、Redis 缓存逻辑 | https://clawhub.ai/skills/cognitive-brain |
| **Ollama** | nomic-embed-text 模型、/api/embeddings 接口 | https://ollama.ai/ |
| **pgvector** | 向量存储、ivfflat 索引、vector_cosine_ops | https://github.com/pgvector/pgvector |

### 架构图绘制

| 贡献者 | 工具 | 说明 |
|-------|------|------|
| **小明 (xiaoming)** | lark-whiteboard | 绘制系统架构图、数据流图、四层记忆模型 |

### 工具链

| 工具 | 用途 |
|------|------|
| **Ollama** | 本地 LLM 和 Embedding 运行服务 |
| **PostgreSQL** | 关系数据库 + 向量存储 |
| **Redis** | 热缓存、L1/L2 记忆存储 |
| **ClawHub** | 技能发布和管理平台 |
| **OpenClaw** | AI 助手框架 |

## 📚 文档结构

```
openclaw-memory-ollama/
├── SKILL.md                    # 技能主文件
├── README.md                   # 项目说明
├── references/
│   ├── architecture.md         # 架构参考
│   ├── deployment.md           # 部署实施指南
│   └── config-reference.md     # 配置参考
└── assets/
    ├── arch-diagram-pro.png   # 架构图（小明绘制）
    ├── flowchart-pro.png      # 流程图（小明绘制）
    └── layers-pro.png         # 四层记忆图（小明绘制）
```

## 📄 开源协议

MIT License

## 🙏 致谢

- [cognitive-brain](https://clawhub.ai/skills/cognitive-brain) — 核心记忆服务架构
- [Ollama](https://ollama.ai/) — 本地 LLM 和 Embedding 服务
- [pgvector](https://github.com/pgvector/pgvector) — PostgreSQL 向量扩展
- [lark-whiteboard](https://clawhub.ai/skills/lark-whiteboard) — 架构图绘制工具
- **小明** — 使用 lark-whiteboard 绘制三张架构图
