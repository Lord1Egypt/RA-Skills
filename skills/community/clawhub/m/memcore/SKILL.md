# MemCore Enhanced - 增强版五层记忆系统

> 基于原版 MemCore，新增四大核心功能：情景记忆、语义压缩、记忆触发器、遗忘曲线

## 架构概览

```
┌─────────────────────────────────────────────────────┐
│  Context Memory    - 当前对话 (秒-分钟级)    │ 原有
│  (滑动窗口 + Token限制)                 │
├─────────────────────────────────────────────────────┤
│  Task Memory       - 任务状态 (分钟-小时级)   │ 原有
│  (状态机管理)                           │
├─────────────────────────────────────────────────────┤
│  User Memory       - 用户偏好 (持久化)    │ 原有
│  (版本控制)                             │
├─────────────────────────────────────────────────────┤
│  Knowledge Memory  - 外部知识 (持久化)    │ 原有
│  (向量检索)                             │
├─────────────────────────────────────────────────────┤
│  Experience Memory - 执行历史 (长期)      │ 原有
│  (强化学习)                             │
├─────────────────────────────────────────────────────┤
│  ✨ 新增四大功能                            │ 增强
├─────────────────────────────────────────────────────┤
│  Episodic Memory   - 情景记忆 (事件/结论)  │ ✓ 新增
│  (上次讨论X时，结论是Y)               │
├─────────────────────────────────────────────────────┤
│  Semantic          - 语义压缩              │ ✓ 新增
│  Compression       (10条→1条摘要)          │
├─────────────────────────────────────────────────────┤
│  Memory Triggers   - 记忆触发器            │ ✓ 新增
│  (关键词→自动加载相关记忆)                │
├─────────────────────────────────────────────────────┤
│  Forgetting Curve  - 遗忘曲线              │ ✓ 新增
│  (艾宾浩斯遗忘模型)                     │
└─────────────────────────────────────────────────────┘
│  🔧 额外增强功能                           │
├─────────────────────────────────────────────────────┤
│  Persistent Storage - SQLite持久化          │ ✓ 新增
│  Vector Knowledge   - 向量语义检索        │ ✓ 新增
│  Conflict Resolver  - 智能冲突解决        │ ✓ 新增
│  Confidence Tracker - 记忆置信度跟踪      │ ✓ 新增
└─────────────────────────────────────────────────────┘
```

## 快速开始

### 安装依赖

```bash
pip install numpy
```

### 基本使用

```python
from memcore_enhanced import MemCoreEnhanced, MemoryPriority, MemorySource

# 初始化（启用持久化）
mc = MemCoreEnhanced(db_path="~/.memcore/memory.db")

# 记录情景记忆
episode_id = mc.record_episode(
    episode_type="discussion",
    context_summary="用户询问优化建议",
    conclusion="建议添加四个新功能",
    related_topics=["MemCore", "AI记忆"],
    priority=MemoryPriority.HIGH,
    confidence=1.0,
    source=MemorySource.EXPLICIT
)

# 查询时触发相关记忆
result = mc.process_input("我想继续弄MemCore")
print(result['suggested_context'])
```

## 核心功能详解

### 1. Episodic Memory (情景记忆)

记录具体事件和结论，支持自然语言回忆。

```python
# 记录情景
mc.record_episode(
    episode_type="discussion",  # discussion | decision | event
    context_summary="用户询问优化建议",
    conclusion="建议添加四个模块",
    related_topics=["MemCore", "AI记忆"],
    participants=["user", "assistant"],
    priority=MemoryPriority.HIGH
)

# 回忆相关情景
episodes = mc.recall_episodes(topic="MemCore", limit=5)
for ep in episodes:
    print(ep.to_natural_language())
    # 输出: [2025-01-13 14:30] discussion: 关于 '用户询问优化建议' 的讨论，结论是：建议添加四个模块
```

### 2. Semantic Compression (语义压缩)

自动压缩冗余信息，保持上下文窗口精简。

```python
# 添加大量对话上下文
for msg in conversation:
    mc.add_to_context(msg)

# 超过20条消息时自动触发压缩
mc.compress_memories("context")
# 压缩后保留: [最近2条, {摘要}]
```

### 3. Memory Triggers (记忆触发器)

关键词触发，自动加载相关背景。

```python
# 创建触发器（也会自动根据情景记忆创建）
mc.create_trigger(
    keywords=["项目X", "Project X"],
    target_memory_ids=["ep_abc123", "user_pref_456"]
)

# 处理用户输入
result = mc.process_input("我想继续搞项盯x")
# 返回: {
#   "triggered": True,
#   "loaded_memories": [...],
#   "suggested_context": "...",
#   "related_knowledge": [...]
# }
```

### 4. Forgetting Curve (遗忘曲线)

模拟艾宾浩斯遗忘曲线，智能清理低价值记忆。

```python
# 运行遗忘周期（通常每天运行一次）
result = mc.run_forgetting_cycle()
# 返回: {
#   "checked": 100,      # 检查的记忆数
#   "deleted": 5,        # 删除的记忆数
#   "deleted_ids": [...]
# }

# 查看记忆健康报告
health = mc.get_health_report()
```

**Forgetting Score 计算:**
```
9057忘分数 = 1 - R(t)
R(t) = e^(-t/S) + 最近访问奖励 - 压缩惩罚

S = 优先级 × (1 + 访问次数 × 0.1)  # 记忆强度
```

### 5. Persistent Storage (持久化存储)

SQLite 数据库持久化存储，支持跨会话记忆。

```python
# 初始化时指定数据库路径
mc = MemCoreEnhanced(db_path="~/.memcore/memory.db")

# 所有操作自动持久化
# - 情景记忆
# - 用户偏好
# - 触发器
# - 任务状态

# 重启后自动恢复
mc2 = MemCoreEnhanced(db_path="~/.memcore/memory.db")
# 所有记忆已加载
```

### 6. Vector Knowledge (向量知识检索)

语义相似度检索，无需精确关键词匹配。

```python
# 添加知识
mc.add_knowledge(
    content="MemCore 采用五层记忆架构",
    metadata={"topics": ["architecture", "MemCore"]},
    source="docs"
)

# 语义查询
results = mc.query_knowledge("记忆系统怎么设计的？")
# 返回高相似度结果，即使关键词不完全匹配
```

支持外部 Embedding 模型：

```python
from vector_knowledge import OpenAIEmbeddingWrapper

mc = MemCoreEnhanced(
    embedding_fn=OpenAIEmbeddingWrapper(api_key="sk-...")
)
```

### 7. Conflict Resolution (记忆冲突解决)

自动检测并解决新旧记忆矛盾。

```python
# 当记录新记忆时自动检测冲突
mc.record_episode(
    context_summary="用户偏好",
    conclusion="用户喜欢Python"
)

mc.record_episode(
    context_summary="用户偏好",
    conclusion="用户讨厌Python"  # 检测到矛盾！
)

# 解决策略:
# - TIME_PRIORITY: 新的覆盖旧的
# - CONFIDENCE_PRIORITY: 高置信度优先
# - MERGE: 尝试合并
# - KEEP_BOTH: 保留两者
```

### 8. Confidence Tracking (记忆置信度跟踪)

每条记忆都有置信度和来源溯源。

```python
# 注册时指定来源和置信度
mc.record_episode(
    context_summary="用户告知姓名",
    conclusion="用户叫露丝",
    confidence=1.0,
    source=MemorySource.EXPLICIT  # 用户明确说的
)

# 用户验证增加置信度
mc.confidence_tracker.verify("ep_xxx", verifier="user")

# 用户否认降低置信度
mc.confidence_tracker.contradict("ep_xxx", reason="姓名错误")

# 查看置信度报告
report = mc.confidence_tracker.get_confidence_report("ep_xxx")
# {
#   "effective_confidence": 0.95,
#   "trust_level": "💚 高度可信"
# }
```

## 高级使用

### 与原版 MemCore 兼容

```python
# 也可以单独使用原有层
from memcore_enhanced import ContextMemory, TaskMemory, UserMemory

context = ContextMemory(max_messages=20, max_tokens=4000)
context.add_message("user", "Hello")
messages = context.get_context()
```

### 用户偏好管理

```python
# 更新用户偏好
mc.update_user_preference(
    user_id="user_123",
    key="response_style",
    value="concise",
    confidence=1.0,
    source=MemorySource.EXPLICIT
)

# 查询用户偏好
prefs = mc.backend.load_user_memory("user_123")
```

### 健康监控

```python
# 获取系统健康报告
health = mc.get_health_report()
# {
#   "episodic_memory": {"count": 100, "by_priority": {...}},
#   "triggers": {"count": 20, "total_triggered": 150},
#   "knowledge": {...},
#   "database": {...}
# }

# 查看低置信度记忆
low_conf = mc.confidence_tracker.get_low_confidence_memories(threshold=0.5)
```

## API 参考

### MemCoreEnhanced

主要类，提供统一入口。

**Methods:**
- `record_episode(...)` - 记录情景
- `recall_episodes(...)` - 回忆情景
- `create_trigger(...)` - 创建触发器
- `process_input(text)` - 处理输入
- `add_knowledge(...)` - 添加知识
- `query_knowledge(...)` - 查询知识
- `run_forgetting_cycle()` - 运行遗忘
- `get_health_report()` - 健康报告

### 枚举类

**MemoryPriority:** `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, `EPHEMERAL`

**MemorySource:** `EXPLICIT`, `IMPLICIT`, `INFERRED`, `IMPORTED`, `DERIVED`

**ConflictStrategy:** `TIME_PRIORITY`, `CONFIDENCE_PRIORITY`, `MERGE`, `KEEP_BOTH`, `MANUAL_REVIEW`

## 性能指标

| 操作 | 复杂度 |
|------|--------|
| 记录情景 | O(1) |
| 回忆查询 | O(n) |
| 触发器检查 | O(m×k) |
| 向量检索 | O(n) |
| 数据库查询 | O(log n) |

## 版本历史

- **v0.2.0** - 增强版
  - 新增情景记忆
  - 新增语义压缩
  - 新增记忆触发器
  - 新增遗忘曲线
  - 新增SQLite持久化
  - 新增向量检索
  - 新增冲突解决
  - 新增置信度跟踪

- **v0.1.0** - 原版
  - 五层记忆架构

## 贡献者

- 原版架构: [@laojun509](https://clawhub.ai/laojun509/memcore)
- 增强版协助: Hermes Agent (露丝)

## 许可证

MIT-0 - 完全开源，可自由使用、修改和分发
