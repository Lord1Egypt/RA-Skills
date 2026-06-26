# Memory Architecture - 四层存储架构详解

## 概览

Omni-Memory采用四层存储架构，结合认知心理学模型与工程最佳实践，实现从即时响应到永久保存的完整记忆链路。

```
┌────────────────────────────────────────────────────────────────┐
│                     OMNI-MEMORY SYSTEM                          │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │  INSTANT │  │   HOT    │  │   WARM   │  │   COLD   │      │
│  │  CACHE   │  │   RAM    │  │  STORE   │  │  STORE   │      │
│  │          │  │          │  │          │  │          │      │
│  │ 10 turns │  │ SESSION  │  │ ChromaDB │  │ Git-Notes│      │
│  │ instant  │  │ STATE.md │  │ + Fluid  │  │ Knowledge│      │
│  │          │  │ + WAL    │  │  Decay   │  │  Graph   │      │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘      │
│       L0            L1            L2            L3            │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

## Layer 0: Instant Cache

### 定义
即时缓存层，存在于模型上下文窗口中。

### 特性
- **容量**: 最近10轮对话
- **TTL**: 即时，超出轮次自动丢弃
- **响应速度**: 最快，无I/O开销
- **用途**: 即时上下文连贯、重复问题检测

### 实现方式
```python
# 模型上下文自动维护
# 无需显式存储
instant_cache = conversation_history[-10:]  # 最近10轮
```

### 使用场景
- 用户追问同一话题
- 上下文指代消解
- 快速响应已回答问题

---

## Layer 1: Hot RAM (SESSION-STATE.md)

### 定义
活跃工作内存，通过WAL协议保护，在压缩、重启后依然存活。

### 特性
- **容量**: 无限制（建议<5KB）
- **TTL**: 永久（手动清理）
- **响应速度**: 极快（文件读取）
- **用途**: 当前任务上下文、关键决策、待办事项

### 存储内容
```markdown
# SESSION-STATE.md

## Current Task
正在进行的任务描述

## Key Context
- User preference: 用户明确表达的偏好
- Decision made: 最近的重要决策
- Blocker: 当前障碍

## Pending Actions
- [ ] 待办事项列表

## Recent Decisions
- 决策1: 原因
- 决策2: 原因
```

### WAL协议（核心）

**Write-Ahead Log原则：先写后响应**

| 触发条件 | 动作 |
|----------|------|
| 用户表达偏好 | 1. 写入SESSION-STATE.md → 2. 存入向量 → 3. 再回复 |
| 用户做决策 | 1. 写入SESSION-STATE.md → 2. 存入向量 → 3. 再回复 |
| 用户纠正 | 1. 写入SESSION-STATE.md → 2. 存入feedback → 3. 再回复 |
| 用户给期限 | 1. 写入SESSION-STATE.md → 2. 再回复 |

**为何重要**：
- 防止崩溃导致上下文丢失
- 防止压缩导致关键信息被清除
- 确保重要信息持久化

---

## Layer 2: Warm Store (ChromaDB + Fluid Decay)

### 定义
中期记忆层，通过向量语义搜索召回，受流体衰减算法管理。

### 特性
- **容量**: 无限制
- **TTL**: 7-30天（流体衰减）
- **响应速度**: 快（向量检索）
- **用途**: 语义召回、知识检索、上下文补充

### 核心技术

#### 1. 向量存储 (ChromaDB)
```python
# 存储记忆
collection.add(
    documents=[content],
    metadatas=[{
        "type": "user|feedback|project|reference",
        "importance": 0.0-1.0,
        "created_at": timestamp,
        "access_count": 0,
        "status": "active"
    }],
    ids=[memory_id]
)
```

#### 2. 流体衰减算法
```python
def calculate_score(similarity, created_at, access_count):
    """
    艾宾浩斯遗忘曲线 + 访问强化
    """
    LAMBDA_DECAY = 0.05  # 遗忘速度
    ALPHA_BOOST = 0.2    # 强化力度
    
    days_passed = (now - created_at) / 86400
    decay = exp(-LAMBDA_DECAY * days_passed)  # 艾宾浩斯衰减
    boost = ALPHA_BOOST * log(1 + access_count)  # 访问强化
    
    return (similarity * decay) + boost
```

**参数含义**：
- `LAMBDA_DECAY = 0.05`: 每~14天记忆强度降到37%
- `ALPHA_BOOST = 0.2`: 每次访问增加~0.2分
- 阈值<0.05被过滤（自然遗忘）

#### 3. 访问强化
每次检索强化top3记忆：
```python
# 检索后更新访问次数
new_count = memory.access_count + 1
update_metadata(memory_id, access_count=new_count)
```

#### 4. 去重机制
```python
# 存储前检查相似度
if similarity > 0.95:
    return "duplicate"  # 拒绝重复存储
```

### Daily Logs
每日对话日志存储在 `memory/YYYY-MM-DD.md`：
```markdown
# 2026-04-06 Daily Log

## Session Log

### 14:30 - 用户偏好设置
**User said**: 我喜欢简洁的回复风格
**Action**: 存储到user类型记忆
**Remember**: 用户偏好简洁回复

### 15:45 - 项目决策
**User said**: 我们用React吧，不要Vue
**Decision**: 采用React作为前端框架
**Reason**: 用户熟悉React生态
```

---

## Layer 3: Cold Store (MEMORY.md + Git-Notes)

### 定义
长期永久存储层，经过Dream整合后晋升至此。

### 特性
- **容量**: 无限制
- **TTL**: 永久
- **响应速度**: 中等（文件读取）
- **用途**: 永久知识、重要决策、用户画像

### MEMORY.md 索引结构

MEMORY.md是**索引而非内容**，指向分类文件：

```markdown
# MEMORY.md — 长期记忆索引

## User Memory
- [profile](memory/user/profile.md) — 用户角色和核心偏好

## Feedback Memory
- [no-tables](memory/feedback/no-tables.md) — 偏好列表而非表格
- [concise-style](memory/feedback/concise.md) — 偏好简洁回复

## Project Memory
- [react-decision](memory/project/react-decision.md) — 为何选择React

## Reference
- [project-docs](memory/reference/docs-path.md) — 项目文档位置
```

### 分类记忆文件格式

每条长期记忆存储为独立文件：

```markdown
---
name: react-decision
description: 项目选择React作为前端框架
type: project
created: 2026-04-06
---

## 内容
项目采用React作为前端框架，不使用Vue。

## 原因
用户熟悉React生态系统，团队有React开发经验，组件库丰富。

## 应用方式
当讨论前端架构、组件设计、状态管理时，默认使用React方案。
```

### Git-Notes知识图谱（可选）

将决策存储在Git Notes中：
```bash
# 存储决策
git notes add -m "decision: use React for frontend" HEAD

# 检索决策
git notes show HEAD
```

---

## Dream整合流程

每日定时执行的自动整合流程：

```
┌─────────────────────────────────────────────────────────────┐
│                     DREAM DAEMON                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Phase 1: ORIENT                                            │
│  ├── 扫描MEMORY.md索引                                      │
│  ├── 检查各类型目录                                         │
│  └── 列出daily logs                                         │
│                                                             │
│  Phase 2: GATHER                                            │
│  ├── 读取working memory (daily logs)                       │
│  ├── 提取信号（偏好、决策、纠正）                           │
│  └── 计算重要性分数                                         │
│                                                             │
│  Phase 3: CONSOLIDATE                                       │
│  ├── 晋升到long-term (importance >= 0.7)                   │
│  ├── 分类写入对应目录                                       │
│  └── 更新MEMORY.md索引                                      │
│                                                             │
│  Phase 4: PRUNE                                             │
│  ├── 归档过期daily logs (>7天)                             │
│  ├── 清理MEMORY.md中的失效引用                              │
│  └── 保持索引<5KB                                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 执行时机
建议每日12:30执行（用户午休时）：
```bash
# crontab配置
30 12 * * * python scripts/dream_daemon.py consolidate
```

---

## 检索优先级

当需要召回记忆时，按以下优先级检索：

```
1. Instant Cache (10 turns)    → ⚡ 即时返回
2. SESSION-STATE.md            → 🔥 当前任务上下文
3. ChromaDB向量搜索            → 🌡️ 语义相关记忆
4. MEMORY.md索引               → ❄️ 永久知识
5. Daily Logs (working memory) → 📅 近期活动
```

### 检索策略

```python
def recall(query):
    # 1. 检查SESSION-STATE
    if query_in_session_state(query):
        return session_state.get(query)
    
    # 2. 向量搜索
    vector_results = chroma_search(query, limit=5)
    
    # 3. 计算流体分数
    scored_results = [
        (r, calculate_fluid_score(r))
        for r in vector_results
    ]
    
    # 4. 过滤低分记忆
    filtered = [r for r in scored_results if r.score > 0.05]
    
    # 5. 强化top3
    boost_memories(filtered[:3])
    
    return filtered
```

---

## 目录结构总览

```
workspace/
├── SESSION-STATE.md           # L1: Hot RAM
├── MEMORY.md                  # L3: 长期记忆索引
├── memory/
│   ├── user/                  # 用户画像
│   │   ├── profile.md
│   │   └── preferences.md
│   ├── feedback/              # 纠正与确认
│   │   ├── no-tables.md
│   │   └── concise-style.md
│   ├── project/               # 项目决策
│   │   ├── react-decision.md
│   │   └── api-design.md
│   ├── reference/             # 外部资源
│   │   └── docs-path.md
│   ├── vectors/               # L2: ChromaDB向量
│   ├── archive/               # 归档的daily logs
│   └── YYYY-MM-DD.md          # Working memory daily logs
```

---

## 关键设计决策

| 决策 | 原因 |
|------|------|
| 四层架构 | 匹配认知心理学模型，优化检索效率 |
| WAL协议 | 防止崩溃/压缩导致数据丢失 |
| 流体衰减 | 模拟人类遗忘曲线，自动管理记忆生命周期 |
| 4类型分类 | 结构化存储，精准检索 |
| Dream整合 | 自动化长期记忆管理，减轻认知负担 |
| 向量去重 | 避免冗余存储，节省空间 |

---

*Architecture Version: 1.0*
*Based on: OpenClaw Memory Skills Analysis*
