# Enhanced MemCore

> 基于原版 MemCore 的完整增强版本，新增 8 大功能模块

---

## 架构图

```
┌────────────────────────────────────────────────┐
│         MemCoreEnhanced (Central Router)          │
├────────────────────────────────────────────────┤
│                                                    │
│  📕 原版五层记忆                                    │
│  ┌─────────────────────────────────────┐         │
│  │ Context Memory  (秒-分钟级)    │         │
│  │ Task Memory     (任务状态)      │         │
│  │ User Memory     (用户偏好)     │         │
│  │ Knowledge Memory(知识库)       │         │
│  │ Experience Memory(经验学习)   │         │
│  └─────────────────────────────────────┘         │
│                                                    │
│  🆕 新增四层记忆                                    │
│  ┌─────────────────────────────────────┐         │
│  │ Episodic Memory  (情景/事件)   │         │
│  │ Semantic Compress(语义压缩)   │         │
│  │ Memory Triggers  (触发器)      │         │
│  │ Forgetting Curve (遗忘曲线)    │         │
│  └─────────────────────────────────────┘         │
│                                                    │
│  🔧 增强功能模块                                    │
│  ┌─────────────────────────────────────┐         │
│  │ 💾 Persistent Storage (SQLite)   │         │
│  │ 🔢 Vector Knowledge(向量检索)  │         │
│  │ ⚖️ Conflict Resolver(冲突解决)│         │
│  │ 📊 Confidence Tracker(置信度)  │         │
│  └─────────────────────────────────────┘         │
│                                                    │
└────────────────────────────────────────────────┘
```

---

## 文件结构

```
memcore-enhanced/
├── enhanced_memcore.py       # 基础类定义
├── persistent_backend.py    # SQLite 持久化
├── vector_knowledge.py      # 向量检索
├── conflict_resolver.py     # 冲突解决
├── confidence_tracker.py    # 置信度跟踪
├── memcore_enhanced.py      # 整合主模块
├── SKILL.md                 # 使用文档
└── README.md                # 本文件
```

---

## 功能详解

### 1. Episodic Memory (情景记忆)

记录具体事件和结论：

```python
mc = MemCoreEnhanced()

# 记录情景
episode_id = mc.record_episode(
    context_summary="用户询问 MemCore 优化",
    conclusion="建议添加四个新模块",
    related_topics=["MemCore", "AI记忆"],
    priority=MemoryPriority.HIGH
)

# 自然语言输出
print(mc.episodic_memory[episode_id].to_natural_language())
# [2026-01-13 10:00] discussion: 关于 '用户询问 MemCore 优化' 的讨论，结论是：建议添加四个新模块

# 按主题回忆
episodes = mc.recall_episodes(topic="MemCore")
```

### 2. Semantic Compression (语义压缩)

自动压缩冗余信息：

```python
# 添加大量上下文
for msg in conversation:
    mc.context_memory.append(msg)

# 超过阈值时自动触发压缩
mc.compress_memories("context")
# 压缩后: [最近2条消息, {摘要}]
```

### 3. Memory Triggers (记忆触发器)

关键词自动触发记忆加载：

```python
# 创建触发器
mc.create_trigger(
    keywords=["项目X", "Project X"],
    target_memory_ids=["ep_abc123"]
)

# 用户输入触发
result = mc.process_input("我想继续搞项盯x")
# result['loaded_memories'] 自动包含相关记忆
```

### 4. Forgetting Curve (遗忘曲线)

模拟艾宾浩斯遗忘曲线：

```python
# 运行遗忘周期
result = mc.run_forgetting_cycle()
# 自动删除低优先级且长时间未访问的记忆

# 遗忘分数计算（基于）：
# - 记忆年龄
# - 访问频率
# - 优先级
# - 压缩次数
```

### 5. Persistent Storage (持久化存储)

SQLite 数据库持久化：

```python
mc = MemCoreEnhanced(db_path="~/.memcore/memory.db")

# 所有操作自动持久化
mc.record_episode(...)  # 自动写入数据库
mc.update_user_preference(...)  # 自动保存

# 重启后自动恢复
mc2 = MemCoreEnhanced(db_path="~/.memcore/memory.db")
# 所有记忆已加载
```

支持的表：
- `episodic_memory` - 情景记忆
- `user_memory` - 用户偏好
- `memory_triggers` - 触发器
- `task_memory` - 任务状态
- `knowledge_memory` - 知识库

### 6. Vector Knowledge (向量检索)

语义相似度检索：

```python
# 添加知识
mc.add_knowledge(
    content="MemCore 使用五层记忆架构",
    metadata={"topics": ["architecture"]},
    source="docs"
)

# 语义查询（不需精确关键词匹配）
results = mc.query_knowledge("记忆系统是怎么设计的？")
# 返回高相似度结果
```

支持外部 Embedding 模型（如 OpenAI）：

```python
from vector_knowledge import OpenAIEmbeddingWrapper

mc = MemCoreEnhanced(
    embedding_fn=OpenAIEmbeddingWrapper(api_key="sk-...")
)
```

### 7. Conflict Resolution (冲突解决)

自动检测并解决记忆冲突：

```python
# 自动检测冲突
mc.record_episode(
    context_summary="用户偏好",
    conclusion="用户喜欢 Python"
)

mc.record_episode(
    context_summary="用户偏好",
    conclusion="用户讨厌 Python"  # 检测到矛盾！
)

# 解决策略：
# - TIME_PRIORITY: 新的覆盖旧的
# - CONFIDENCE_PRIORITY: 高置信度优先
# - MERGE: 尝试合并
# - KEEP_BOTH: 保留两者
```

### 8. Confidence Tracking (置信度跟踪)

每条记忆都有置信度和来源溯源：

```python
# 注册记忆时指定来源和置信度
mc.record_episode(
    context_summary="用户告知姓名",
    conclusion="用户名字是露丝",
    confidence=1.0,  # 用户明确说的
    source=MemorySource.EXPLICIT
)

# 用户验证增加置信度
mc.confidence_tracker.verify("ep_xxx", verifier="user")

# 用户否认降低置信度
mc.confidence_tracker.contradict("ep_xxx", reason="姓名错误")

# 查看置信度报告
report = mc.confidence_tracker.get_confidence_report("ep_xxx")
# {
#   "effective_confidence": 0.95,
#   "verification_count": 2,
#   "trust_level": "💚 高度可信"
# }
```

---

## 安装

```bash
pip install numpy  # 向量计算需要
# 可送: pip install openai  # 如果使用 OpenAI Embedding
```

---

## 快速开始

```python
from memcore_enhanced import MemCoreEnhanced, MemoryPriority, MemorySource

# 初始化
mc = MemCoreEnhanced(db_path="~/.memcore/my_memory.db")

# 记录情景
mc.record_episode(
    context_summary="用户给我起名字",
    conclusion="用户喜欢叫我'露丝'",
    related_topics=["用户信息", "名字"],
    priority=MemoryPriority.CRITICAL,
    source=MemorySource.EXPLICIT
)

# 添加知识
mc.add_knowledge(
    content="MemCore 是五层记忆架构的 AI 记忆系统",
    source="github"
)

# 处理输入（触发记忆）
result = mc.process_input("你好，我是露丝")
print(result['suggested_context'])

# 健康报告
print(mc.get_health_report())
```

---

## 性能指标

| 指标 | 数值 |
|------|------|
| 情景记忆查询 | O(n) |
| 向量检索 | O(n) |
| 触发器检查 | O(m*k) m=触发器数, k=关键词数 |
| 数据库查询 | O(log n) 有索引 |
| 遗忘分数计算 | O(1) |

---

## 贡献

- 原版 MemCore: [@laojun509](https://clawhub.ai/laojun509/memcore)
- 增强功能设计: 社区反馈 + Hermes Agent (露丝)

## 许可证

MIT-0 - 完全开源，无需声明
