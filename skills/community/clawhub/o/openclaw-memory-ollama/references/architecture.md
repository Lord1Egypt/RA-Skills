# OpenClaw 记忆管理系统架构参考

## 系统架构图

```
┌─────────────────────────────────────────────────────────┐
│                    接入层                                 │
│     飞书 (💬)    WebChat (🌐)    Gateway (:18789)        │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│                    服务层                                 │
│  Memory Files  │  cognitive-brain  │  Ollama             │
│  📁 日常记忆    │  🧠 Memory Svc   │  🤖 nomic-embed     │
│               │  🧠 Concept Svc   │  📐 768维向量        │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│                    存储层                                 │
│  🐘 PostgreSQL     🔴 Redis      📂 本地文件             │
│  (pgvector)       (热缓存)      (~/.openclaw)           │
└─────────────────────────────────────────────────────────┘
```

## 四层记忆模型

```
用户消息
  ↓
┌─────────────────┐
│ L1 感官记忆      │ ← Redis | TTL: 30秒
│ (瞬时缓存)       │
└─────────────────┘
  ↓ 沉淀
┌─────────────────┐
│ L2 工作记忆      │ ← Redis | TTL: 60分钟
│ (对话上下文)     │
└─────────────────┘
  ↓ 重要信息
┌─────────────────┐
│ L3 情景记忆      │ ← PostgreSQL | 永久
│ (事件回忆)       │
└─────────────────┘
  ↓ 知识化
┌─────────────────┐
│ L4 语义记忆      │ ← PostgreSQL | 永久
│ (概念知识)       │
└─────────────────┘
```

## 记忆写入流程

```
用户: "记住今天的会议内容"
         ↓
   触发词检测 ("记住")
         ↓
   brain.encode() 提取内容类型
         ↓
   Ollama Embedding 生成 768维向量
         ↓
   存入 PostgreSQL (episodes 表)
```

## 记忆检索流程

```
用户查询
   ↓
memory_search (文件索引)
   ↓
brain.recall() (语义向量搜索)
   ↓
Top-K 结果排序 (~40ms)
   ↓
注入 AI 上下文
```

## 核心技术选型

| 组件 | 选型 | 理由 |
|------|------|------|
| Embedding | nomic-embed-text | 本地、免费、768维 |
| 向量存储 | PostgreSQL + pgvector | 成熟、免费 |
| 缓存 | Redis | 高性能、支持TTL |
| 文件存储 | 本地文件 | 无额外成本 |

## cognitive-brain 引用

本系统基于 cognitive-brain 技能构建，引用内容：

### 服务接口

- `brain.encode()` — 记忆写入
- `brain.recall()` — 记忆检索
- `brain.episodes_*` — 情景记忆管理
- `brain.concepts_*` — 概念记忆管理

### 数据表结构

- `episodes` — 情景记忆表（content, embedding, role, timestamp）
- `concepts` — 概念知识表（name, description, embedding, metadata）

### 存储配置

- PostgreSQL: `localhost:5432`, database: `cognitive_brain`
- Redis: `localhost:6379`
