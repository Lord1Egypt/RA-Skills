---
name: elite-longterm-memory
description: "终极AI智能体记忆系统。WAL协议 + 向量搜索 + git-notes + 云备份。6层记忆架构：热RAM(SESSION-STATE)、温存储(LanceDB向量)、冷存储(Git-Notes知识图)、精选档案(MEMORY.md)、云备份(SuperMemory)、自动提取(Mem0)。"
version: 1.0.0
author: skillforge-JOJO
keywords: [memory, long-term, elite, vector-search, lancedb, git-notes, wal, persistent, context]
---

# Elite Longterm Memory — 精英长期记忆

**一句话描述**: 终极AI智能体记忆系统，6层记忆架构永不忘上下文。

---

## 功能概述

结合6种成熟方法的终极记忆系统。永不丢失上下文、永不忘记决策、永不重复错误。

## 架构概览

```
┌─────────────────────────────────────────────────────────────────┐
│                    ELITE LONGTERM MEMORY                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   HOT RAM   │  │  WARM STORE │  │  COLD STORE │             │
│  │             │  │             │  │             │             │
│  │ SESSION-    │  │  LanceDB    │  │  Git-Notes  │             │
│  │ STATE.md    │  │  Vectors    │  │  Knowledge  │             │
│  │             │  │             │  │  Graph      │             │
│  │ (survives   │  │ (semantic   │  │ (permanent  │             │
│  │  compaction)│  │  search)    │  │  decisions) │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│         │                │                │                     │
│         └────────────────┼────────────────┘                     │
│                          ▼                                      │
│                  ┌─────────────┐                                │
│                  │  MEMORY.md  │  ← Curated long-term           │
│                  │  + daily/   │    (human-readable)            │
│                  └─────────────┘                                │
│                          │                                      │
│                          ▼                                      │
│                  ┌─────────────┐                                │
│                  │ SuperMemory │  ← Cloud backup (optional)     │
│                  │    API      │                                │
│                  └─────────────┘                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5层记忆架构

### 第1层: HOT RAM (SESSION-STATE.md)
**来源**: bulletproof-memory

活跃工作记忆，在压缩后仍然保留。写前日志协议。

```markdown
# SESSION-STATE.md — 活跃工作记忆

## 当前任务
[我们现在正在做什么]

## 关键上下文
- 用户偏好: ...
- 已做决策: ...
- 阻塞项: ...

## 待处理动作
- [ ] ...
```

**规则**: 响应前写入。由用户输入触发，非智能体记忆。

### 第2层: WARM STORE (LanceDB向量)
**来源**: lancedb-memory

跨所有记忆的语义搜索。自动回忆注入相关上下文。

```bash
# 自动回忆（自动发生）
memory_recall query="项目状态" limit=5

# 手动存储
memory_store text="用户偏好暗色模式" category="preference" importance=0.9
```

### 第3层: COLD STORE (Git-Notes知识图)
**来源**: git-notes-memory

结构化决策、学习和上下文。分支感知。

```bash
# 存储决策（静默 — 永不宣布）
python3 memory.py -p $DIR remember '{"type":"decision","content":"前端使用React"}' -t tech -i h

# 检索上下文
python3 memory.py -p $DIR get "frontend"
```

### 第4层: 精选档案 (MEMORY.md + daily/)
**来源**: OpenClaw原生

人类可读的长期记忆。每日日志 + 提炼智慧。

```
workspace/
├── MEMORY.md              # 精选长期（精华）
└── memory/
    ├── 2026-01-30.md      # 每日日志
    ├── 2026-01-29.md
    └── topics/            # 主题特定文件
```

### 第5层: 云备份 (SuperMemory) — 可选
**来源**: supermemory

跨设备同步。与你的知识库聊天。

```bash
export SUPERMEMORY_API_KEY="your-key"
supermemory add "重要上下文"
supermemory search "我们决定了什么关于..."
```

### 第6层: 自动提取 (Mem0) — 推荐
**新: 自动事实提取**

Mem0自动从对话中提取事实。80% token减少。

```bash
npm install mem0ai
export MEM0_API_KEY="your-key"
```

---

## WAL协议（关键）

**写前日志**: 响应前写入状态，非之后。

| 触发器 | 动作 |
|--------|------|
| 用户陈述偏好 | 写入SESSION-STATE.md → 然后响应 |
| 用户做出决策 | 写入SESSION-STATE.md → 然后响应 |
| 用户给出截止日期 | 写入SESSION-STATE.md → 然后响应 |
| 用户纠正你 | 写入SESSION-STATE.md → 然后响应 |

**为什么？** 如果你先响应然后在保存前崩溃/压缩，上下文丢失。WAL确保持久性。

---

## 核心参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| autoRecall | bool | true | 自动回忆 |
| autoCapture | bool | false | 自动捕获 |
| minImportance | float | 0.7 | 最小重要性阈值 |
| maxResults | int | 10 | 最大结果数 |
| minScore | float | 0.3 | 最小相似度分数 |

---

## 使用示例

### 示例工作流

```
用户: "这个项目我们用Tailwind，不用vanilla CSS"

智能体（内部）:
1. 写入SESSION-STATE.md: "决策：用Tailwind，不用vanilla CSS"
2. 存储到Git-Notes: 关于CSS框架的决策
3. memory_store: "用户偏好Tailwind胜过vanilla CSS" importance=0.9
4. 然后响应: "好的 — 用Tailwind..."
```

---

## 维护命令

```bash
# 审计向量记忆
memory_recall query="*" limit=50

# 清除所有向量（核选项）
rm -rf ~/.openclaw/memory/lancedb/
openclaw gateway restart

# 导出Git-Notes
python3 memory.py -p . export --format json > memories.json

# 检查记忆健康
du -sh ~/.openclaw/memory/
wc -l MEMORY.md
ls -la memory/
```

---

## 版本历史

| 版本 | 日期 | 变化 |
|------|------|------|
| v1.0.0 | 2026-04-12 | ClawHub发布版 |

---

*🎩 马斯克出品 | 打造地表最强智能体*
