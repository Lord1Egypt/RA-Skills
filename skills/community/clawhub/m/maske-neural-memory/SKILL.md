---
name: neural-memory
description: "神经记忆系统 — 使用传播激活的联想记忆，实现持久、智能的回忆。主动使用场景：(1)需要跨会话记住事实、决策、错误或上下文 (2)用户问"你还记得..."或引用过去对话 (3)开始新任务时注入相关上下文 (4)做出决策或遇到错误后存储供将来参考 (5)用户问"为什么X发生？"通过记忆追踪因果链。"
version: 1.0.0
author: skillforge-JOJO
keywords: [memory, neural, associative, recall, persistent, hebbian, graph, memory-system]
---

# Neural Memory — 神经记忆系统

**一句话描述**: 使用传播激活的联想记忆，实现持久、智能的回忆。

---

## 功能概述

生物启发的记忆系统，使用传播激活代替关键词/向量搜索。记忆形成神经图，神经元通过20种类型突触连接。频繁共同访问的记忆加强连接（赫布学习）。陈旧记忆自然衰减。矛盾自动检测。

**为什么不只是向量搜索？** 向量搜索找到与查询相似的文档。NeuralMemory通过图遍历找到*概念相关*的记忆 — 即使没有关键词或嵌入重叠。

---

## 核心特性

- **零LLM依赖** — 纯算法：正则、图遍历、赫布学习
- **传播激活** — 通过神经图进行联想回忆，非关键词/向量搜索
- **20种突触类型** — 时间(BEFORE/AFTER)、因果(CAUSED_BY/LEADS_TO)、语义(IS_A/HAS_PROPERTY)、情感(FELT/EVOKES)、冲突(CONTRADICTS)
- **记忆生命周期** — 短期→工作→情景→语义，带艾宾浩斯衰减
- **矛盾检测** — 自动检测冲突记忆，降低过时记忆优先级
- **赫布学习** — "一起激发的神经元连在一起" — 记忆随使用改善
- **时间推理** — 因果链遍历、事件序列、时间范围查询

---

## 深度级别

| 深度 | 名称 | 速度 | 用例 |
|------|------|------|------|
| 0 | 即时 | <10ms | 快速事实、最近上下文 |
| 1 | 上下文 | ~50ms | 标准回忆（默认） |
| 2 | 习惯 | ~200ms | 模式匹配、工作流建议 |
| 3 | 深度 | ~500ms | 跨领域关联、因果链 |

---

## 工具参考

### 核心记忆工具

| 工具 | 用途 | 何时使用 |
|------|------|---------|
| `nmem_remember` | 存储记忆 | 决策后、错误后、事实后、洞察后、用户偏好后 |
| `nmem_recall` | 查询记忆 | 任务前、用户引用过去上下文时、"你还记得..." |
| `nmem_context` | 获取最近记忆 | 会话开始时、注入新鲜上下文 |
| `nmem_todo` | 快速TODO（30天过期） | 任务跟踪 |

### 智能工具

| 工具 | 用途 | 何时使用 |
|------|------|---------|
| `nmem_auto` | 从文本自动提取记忆 | 重要对话后 — 自动捕获决策、错误、TODO |
| `nmem_recall` (depth=3) | 深度联想回忆 | 需要跨领域连接的复杂问题 |
| `nmem_habits` | 工作流模式建议 | 用户重复类似动作序列时 |

### 管理工具

| 工具 | 用途 | 何时使用 |
|------|------|---------|
| `nmem_health` | 大脑健康诊断 | 定期检查、分享大脑前 |
| `nmem_stats` | 大脑统计 | 记忆数量快速概览 |
| `nmem_version` | 大脑快照和回滚 | 风险操作前、版本检查点 |
| `nmem_transplant` | 大脑间转移记忆 | 跨项目知识共享 |

---

## 使用示例

### 记住决策
```python
nmem_remember(
  content="生产用PostgreSQL，开发用SQLite",
  type="decision",
  tags=["database", "infrastructure"],
  priority=8
)
```

### 联想回忆
```python
nmem_recall(
  query="生产环境数据库配置",
  depth=1,
  max_tokens=500
)
```
返回通过图遍历找到的记忆，非关键词匹配。相关记忆（如"部署使用Docker与pg_dump备份"）即使没有共享关键词也会浮现。

### 追踪因果链
```python
nmem_recall(
  query="上周部署为什么失败？",
  depth=2
)
```
跟随CAUSED_BY和LEADS_TO突触追踪因果关系链。

### 从对话自动捕获
```python
nmem_auto(
  action="process",
  text="我们决定从REST切换到GraphQL，因为前端需要灵活查询。迁移需要2个sprint。TODO: 更新API文档。"
)
```
自动提取：1个决策、1个事实、1个TODO。

---

## 工作流

### 会话开始时
1. 调用 `nmem_context` 将最近记忆注入意识
2. 如果用户提及特定主题，调用 `nmem_recall`

### 对话期间
3. 做出决策时：`nmem_remember` type="decision"
4. 发生错误时：`nmem_remember` type="error"
5. 用户陈述偏好时：`nmem_remember` type="preference"
6. 被问及过去事件时：`nmem_recall`

### 会话结束时
7. 调用 `nmem_auto` action="process" 处理重要对话片段
8. 自动提取事实、决策、错误和TODO

---

## 核心参数

| 参数 | 类型 | 范围 | 默认值 | 说明 |
|------|------|------|--------|------|
| depth | int | 0-3 | 1 | 回忆深度级别 |
| priority | int | 0-10 | 5 | 记忆优先级 |
| max_tokens | int | 100-10000 | 500 | 最大上下文token数 |
| contextDepth | int | 0-3 | 1 | 上下文深度 |
| autoContext | bool | true/false | true | 自动注入上下文 |
| autoCapture | bool | true/false | true | 自动捕获记忆 |

---

## 版本历史

| 版本 | 日期 | 变化 |
|------|------|------|
| v1.0.0 | 2026-04-12 | ClawHub发布版 |

---

*🎩 马斯克出品 | 打造地表最强智能体*
