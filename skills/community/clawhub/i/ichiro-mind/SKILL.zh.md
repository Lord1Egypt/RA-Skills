---
name: ichiro-mind
version: 1.0.0
description: "Ichiro-Mind: 终极统一记忆系统。4层架构（热层→温层→冷层→归档层），神经网络图、向量搜索、经验学习、自动清理。为持久智能记忆而生。"
author: "兵步一郎 & OpenClaw 社区"
keywords: [记忆, AI代理, 长期记忆, 神经图, 向量搜索, 经验学习, 一郎, 统一记忆, 持久上下文, 智能召回]
metadata:
  openclaw:
    emoji: "🧠"
    requires:
      env:
        - OPENAI_API_KEY
      plugins:
        - memory-lancedb
---

# 🧠 Ichiro-Mind（一郎之脑）

> *"一郎的思维 — 将所有记忆层统一为一个智能系统。"*

**Ichiro-Mind** 是 AI 代理的终极统一记忆系统，将 5 种成熟的记忆方案融合为一个内聚架构。以其创造者对持久、智能记忆的愿景命名。

## 🏗️ 架构概览

```
┌─────────────────────────────────────────────────────────────────┐
│                    🧠 ICHIRO-MIND                               │
│                   "永不遗忘的大脑"                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ⚡ 热层（工作内存）               🔥 温层（神经网络）           │
│  ┌─────────────────────┐          ┌─────────────────────┐       │
│  │ SESSION-STATE.md    │◄────────►│ 关联记忆网络        │       │
│  │ • 实时状态          │  同步    │ • 传播激活检索      │       │
│  │ • WAL协议           │          │ • 因果链追踪        │       │
│  │ •  survived compact │          │ • 矛盾自动检测      │       │
│  └─────────────────────┘          └─────────────────────┘       │
│           │                                │                    │
│           ▼                                ▼                    │
│  💾 冷层（向量存储）               📚 归档层（长期存储）         │
│  ┌─────────────────────┐          ┌─────────────────────┐       │
│  │ LanceDB 存储        │          │ MEMORY.md + 日志    │       │
│  │ • 语义搜索          │          │ • Git-Notes 图      │       │
│  │ • 自动提取          │          │ • 云端备份          │       │
│  │ • 重要性评分        │          │ • 人类可读          │       │
│  └─────────────────────┘          └─────────────────────┘       │
│                                                                 │
│  🧹 卫生引擎                      🎓 学习引擎                   │
│  • 自动清理                       • 决策追踪                     │
│  • 去重合并                       • 错误学习                     │
│  • Token优化                      • 实体演化                     │
└─────────────────────────────────────────────────────────────────┘
```

## ✨ 核心特性

### 1. 智能记忆路由
根据查询类型自动选择最佳检索方法：

| 查询类型 | 方法 | 速度 |
|----------|------|------|
| 近期上下文 | 热层 (SESSION-STATE) | <10ms |
| 事实与偏好 | 冷层 (向量搜索) | ~50ms |
| 因果关系 | 温层 (神经图) | ~100ms |
| 长期决策 | 归档层 (Git-Notes) | ~200ms |

### 2. 自动记忆生命周期
```
捕获 → 提取 → 处理 → 存储 → 召回 → 清理
  │      │       │      │      │      │
输入   Mem0/    重要性  4层    智能   定期
捕获   自动提取   评分   存储   路由   清理
```

### 3. 神经图与传播激活
- **不是关键词搜索** — 通过图遍历找到概念相关记忆
- **20种突触类型** — 时间、因果、语义、情感连接
- **Hebbian学习** — 记忆随使用增强
- **矛盾检测** — 自动检测冲突信息

### 4. 经验学习
```
决策 → 行动 → 结果 → 教训
  │      │      │      │
存储   追踪   记录   学习
```
- 追踪决策及其结果
- 从错误中学习
- 基于过去模式提供建议

### 5. 智能卫生
- 自动清理垃圾记忆
- 去重相似条目
- 优化Token使用
- 月度维护模式

## 🚀 快速开始

### 安装
```bash
clawhub install ichiro-mind
```

### 配置
```bash
# 初始化 Ichiro-Mind
ichiro-mind init

# 配置 MCP
ichiro-mind setup-mcp
```

### 基础用法
```python
from ichiro_mind import IchiroMind

# 初始化
mind = IchiroMind()

# 存储记忆（自动路由到适当层）
mind.remember(
    content="用户偏好深色模式",
    category="preference",
    importance=0.9
)

# 智能路由召回
result = mind.recall("用户偏好什么模式？")

# 经验学习
mind.learn(
    decision="开发环境使用 SQLite",
    outcome="大数据量时变慢",
    lesson="数据集 >1GB 时使用 PostgreSQL"
)
```

## 📝 记忆层详解

### 热层 — SESSION-STATE.md
使用预写日志协议的实时工作内存。

```markdown
# SESSION-STATE.md — Ichiro-Mind 热层

## 当前任务
构建统一记忆系统

## 活动上下文
- 用户: 兵步一郎
- 项目: Ichiro-Mind
- 技术栈: Python + LanceDB + 神经图

## 关键决策
- [x] 使用4层架构
- [ ] 实现 MCP 接口

## 待处理项
- [ ] 编写 SKILL.md
- [ ] 创建 Python 核心
```

**WAL协议**: 先写再回复，而非先回复再写。

### 温层 — 神经图
具有传播激活的关联记忆。

```python
# 存储带关系的记忆
mind.remember(
    content="生产环境使用 PostgreSQL",
    type="decision",
    tags=["数据库", "基础设施"],
    relations=[
        {"type": "CAUSED_BY", "target": "性能问题"},
        {"type": "LEADS_TO", "target": "更好的扩展性"}
    ]
)

# 深度召回
memories = mind.recall_deep(
    query="数据库决策",
    depth=2  # 追踪因果链
)
```

### 冷层 — 向量存储
使用 LanceDB 的语义搜索。

```python
# 从对话自动捕获
mind.auto_capture(text="用户喜欢极简界面")

# 语义搜索
results = mind.search("用户界面偏好")
```

### 归档层 — 持久存储
人类可读的长期记忆。

```
workspace/
├── MEMORY.md              # 精选长期记忆
└── memory/
    ├── 2026-03-07.md      # 每日日志
    ├── decisions/         # 结构化决策
    ├── entities/          # 人、项目、概念
    └── lessons/           # 学到的经验
```

## 🛠️ 高级特性

### 记忆卫生
```bash
# 审计记忆
ichiro-mind audit

# 清理垃圾
ichiro-mind cleanup --dry-run
ichiro-mind cleanup --confirm

# 优化 Token
ichiro-mind optimize
```

### 经验回放
```python
# 在做类似决策前
similar = mind.get_lessons(context="数据库选择")
# 返回过去的决策和结果
```

### 实体追踪
```python
# 追踪演化中的实体
mind.track_entity(
    name="兵步一郎",
    type="person",
    attributes={
        "role": "创造者",
        "interests": ["AI", "自动化"],
        "preferences": {"ui": "极简", "docs": "双语"}
    }
)

# 更新实体
mind.update_entity("兵步一郎", {"last_contact": "2026-03-07"})
```

## 🔌 MCP 集成

添加到 `~/.openclaw/mcp.json`:

```json
{
  "mcpServers": {
    "ichiro-mind": {
      "command": "python3",
      "args": ["-m", "ichiro_mind.mcp"],
      "env": {
        "ICHIRO_MIND_BRAIN": "default"
      }
    }
  }
}
```

## 📊 性能

| 操作 | 延迟 | 吞吐量 |
|------|------|--------|
| 热层召回 | <10ms | 10K ops/s |
| 温层召回 | ~100ms | 1K ops/s |
| 冷层搜索 | ~50ms | 500 ops/s |
| 归档读取 | ~200ms | 100 ops/s |
| 存储记忆 | ~20ms | 5K ops/s |

## 🎯 使用场景

1. **长期项目** — 跨会话永不丢失上下文
2. **复杂决策** — 追踪决策树和结果
3. **用户关系** — 记住偏好、历史、特点
4. **错误预防** — 从错误中学习，建议替代方案
5. **知识积累** — 随时间建立领域专业知识

## 🧠 理念

> *"记忆不是存储 — 而是智能。"*

Ichiro-Mind 将记忆视为一等公民：
- 记忆有关系
- 记忆随时间演化
- 记忆竞争注意力
- 记忆不用则衰
- 矛盾被解决

## 📚 相关技能

- **elite-longterm-memory** — 基础层架构
- **neural-memory** — 关联图引擎
- **memory-hygiene** — 清理和优化
- **memory-setup** — 配置和结构

## 🙏 致谢

由 **兵步一郎** (Ichiro) 出于对持久、智能 AI 记忆的热爱而构建。

受 OpenClaw 生态系统中最佳记忆系统的启发。

## License

MIT

---

📖 [English Documentation](SKILL.md)
