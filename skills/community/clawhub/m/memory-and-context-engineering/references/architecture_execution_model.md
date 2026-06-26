# 全局架构总览 - 补充说明

> 本文档补充架构总览中缺失的关键信息：运行方式、执行模型和使用场景

## 零、系统运行模式

### 核心定位

**Agent Memory System 是一个 Skill，而非独立应用程序。**

这意味着：
- ❌ 它不是独立运行的 Web 服务
- ❌ 它不需要启动服务器或监听端口
- ❌ 它没有独立的用户界面

✅ 它是一个能力扩展包，由智能体动态加载和执行
✅ 它在智能体的会话上下文中运行
✅ 所有交互通过智能体与用户的对话完成

### 执行模型

```
┌─────────────────────────────────────────────────────────────┐
│                     智能体运行环境                           │
│                                                             │
│  用户请求 ──▶ 智能体 ──▶ 加载 Skill ──▶ 执行 Skill 指令     │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │            Agent Memory System (Skill)                │ │
│  │                                                       │ │
│  │  • SKILL.md：指导智能体如何使用记忆能力              │ │
│  │  • scripts/：提供可调用的工具函数                    │ │
│  │  • references/：提供详细的参考文档                   │ │
│  │                                                       │ │
│  │  智能体按需调用：                                    │ │
│  │  - 存储记忆 → scripts.store_memory()                │ │
│  │  - 准备上下文 → scripts.prepare_context()           │ │
│  │  - 追踪状态 → scripts.track_state()                 │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 元技能常驻运行

**定义**：元技能（Meta Skill）是智能体的底层能力，在智能体启动时加载，并在整个生命周期内保持可用。

**工作流程**：
1. 智能体启动时，自动加载 Agent Memory System
2. 初始化核心模块（ContextOrchestrator、GlobalStateCapture等）
3. 在智能体执行任务过程中，持续提供记忆能力支持
4. 会话结束时，自动保存状态和统计信息

**与普通 Skill 的区别**：

| 维度 | 普通 Skill | 元 Skill（Memory System） |
|------|-----------|--------------------------|
| 加载时机 | 用户明确请求时 | 智能体启动时自动加载 |
| 生命周期 | 单次会话或任务 | 跨会话持久存在 |
| 调用频率 | 按需调用 | 持续可用 |
| 作用范围 | 特定任务域 | 全局基础设施 |

---

## 一、触发场景与使用时机

### 自动触发场景

智能体在以下场景会**自动使用**记忆能力：

| 场景 | 触发条件 | 智能体行为 |
|------|----------|-----------|
| **新会话启动** | 用户开始新对话 | 加载用户画像和历史偏好 |
| **多轮对话** | 用户继续对话 | 使用 `prepare_context()` 获取历史上下文 |
| **任务执行** | 执行复杂任务 | 使用 `track_state()` 追踪进度 |
| **决策制定** | 需要做出选择 | 使用 `get_related_memories()` 获取相关经验 |
| **错误恢复** | 任务失败 | 使用 `get_past_solutions()` 查找类似问题的解决方案 |

### 用户明确请求场景

用户也可以**直接请求**使用记忆能力：

| 用户表达 | 智能体行为 |
|---------|-----------|
| "记住我喜欢简洁的解释" | 调用 `store_memory()` 存储偏好 |
| "我上次说过什么？" | 调用 `retrieve_memories()` 检索历史 |
| "帮我总结一下我们的对话" | 调用 `generate_summary()` 生成总结 |

### 使用示例

**场景 1：多轮对话**

```
用户：我想实现一个登录功能
智能体：
  [内部调用] orchestrator.store_memory(
    content="用户想实现登录功能",
    bucket_type=USER_INTENT,
    topic_label="用户登录"
  )
  [响应] 好的，我来帮你实现登录功能...

（几轮对话后）

用户：还是用邮箱登录吧
智能体：
  [内部调用] orchestrator.prepare_context() 
  // 自动获取之前的"用户登录"相关记忆
  [响应] 根据你之前的想法，我们来实现邮箱登录功能...
```

**场景 2：跨会话记忆**

```
（新会话）

用户：帮我设计一个API
智能体：
  [内部调用] orchestrator.prepare_context()
  // 自动加载用户偏好："喜欢简洁的技术解释"
  [响应] 根据你偏好简洁的风格，我建议采用RESTful API设计...
```

---

## 二、调用接口与执行流程

### 智能体可调用的核心接口

```python
# 1. 存储记忆
from scripts import create_context_orchestrator, SemanticBucketType

orchestrator = create_context_orchestrator(
    user_id="user_123",
    session_id="session_456",
)

# 存储用户意图
orchestrator.store_memory(
    content="用户想要实现登录功能",
    bucket_type=SemanticBucketType.USER_INTENT,
    topic_label="用户登录",
)

# 2. 准备上下文（包含历史记忆）
context = orchestrator.prepare_context(
    user_input="用邮箱登录吧",
    system_instruction="你是登录功能开发专家",
)

# 3. 追踪状态
from scripts import GlobalStateCapture, StateEventType

capture = GlobalStateCapture(user_id="user_123")

# 同步状态
capture.sync_from_langgraph(
    state={"phase": "implementing", "task": "login_feature"},
    node_name="executor",
)

# 4. 结束会话
stats = orchestrator.end_session()
```

### 完整执行流程

```
┌─────────────────────────────────────────────────────────────┐
│                   智能体执行流程                             │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
           ┌──────────────────────────┐
           │  用户发起请求             │
           └───────────┬──────────────┘
                       │
                       ▼
           ┌──────────────────────────┐
           │  智能体加载 Memory Skill │
           └───────────┬──────────────┘
                       │
                       ▼
           ┌──────────────────────────┐
           │  初始化 Orchestrator     │
           │  创建 GlobalStateCapture │
           └───────────┬──────────────┘
                       │
                       ▼
           ┌──────────────────────────┐
           │  准备上下文              │
           │  prepare_context()       │
           │  • 加载用户画像          │
           │  • 检索相关记忆          │
           │  • 构建上下文包          │
           └───────────┬──────────────┘
                       │
                       ▼
           ┌──────────────────────────┐
           │  执行任务                │
           │  （智能体的核心逻辑）    │
           └───────────┬──────────────┘
                       │
                       ▼
           ┌──────────────────────────┐
           │  存储执行结果            │
           │  store_memory()          │
           │  • 用户意图              │
           │  • 决策上下文            │
           │  • 任务结果              │
           └───────────┬──────────────┘
                       │
                       ▼
           ┌──────────────────────────┐
           │  追踪状态变化            │
           │  sync_from_langgraph()   │
           └───────────┬──────────────┘
                       │
                       ▼
           ┌──────────────────────────┐
           │  任务完成或用户离开      │
           └───────────┬──────────────┘
                       │
                       ▼
           ┌──────────────────────────┐
           │  结束会话                │
           │  end_session()           │
           │  • 保存统计信息          │
           │  • 清理资源              │
           └──────────────────────────┘
```

---

## 三、关键术语解释

### 元技能（Meta Skill）

**定义**：元技能是智能体的底层能力基础设施，与普通技能相比，具有常驻性和全局性。

**特征**：
- **常驻性**：在智能体启动时加载，不会主动卸载
- **全局性**：为所有其他技能提供基础能力支持
- **透明性**：用户通常不直接感知，而是通过智能体的行为间接体验

**类比**：如果把智能体比作操作系统，元技能就是文件系统、内存管理等核心服务。

### P0/P1 连接

**定义**：表示模块间连接的优先级和依赖关系。

| 优先级 | 含义 | 示例 |
|--------|------|------|
| **P0** | 核心连接，必须实现 | 上下文重构器 ↔ 长期记忆 |
| **P1** | 增强连接，可选实现 | 状态捕捉器 ↔ 洞察模块 |

**在代码中的体现**：
```python
# P0 连接：核心流程必需
reconstructor.bind_state_capture(capture)  # 必须调用

# P1 连接：增强功能
insight_module.enable_state_analysis(capture)  # 可选调用
```

### 感知-决策-行动-观察循环

**定义**：Agent Loop 的核心执行模式。

```
感知（Perceive）
  │ 接收用户输入、环境信息
  ▼
决策（Decide）
  │ 基于感知和记忆，决定下一步行动
  ▼
行动（Act）
  │ 执行决策（调用工具、生成回复等）
  ▼
观察（Observe）
  │ 观察行动结果，存储到记忆
  ▼
  └─▶ 回到感知阶段（循环）
```

**与记忆系统的关系**：
- **感知阶段**：调用 `prepare_context()` 获取历史记忆
- **决策阶段**：基于记忆做出更明智的决策
- **行动阶段**：使用 `track_state()` 追踪执行过程
- **观察阶段**：调用 `store_memory()` 存储结果

---

## 四、快速开始

### 最小可用示例

```python
from scripts import create_context_orchestrator, SemanticBucketType

# 1. 创建编排器
orchestrator = create_context_orchestrator(
    user_id="demo_user",
    session_id="demo_session",
)

# 2. 存储用户意图
orchestrator.store_memory(
    content="用户想学习Python",
    bucket_type=SemanticBucketType.USER_INTENT,
    topic_label="Python学习",
)

# 3. 准备上下文（自动加载相关记忆）
context = orchestrator.prepare_context(
    user_input="推荐一些Python学习资源",
    system_instruction="你是学习顾问",
)

# 4. 使用上下文生成响应
# （智能体会基于context中的历史记忆生成更个性化的回复）

# 5. 结束会话
stats = orchestrator.end_session()
print(f"本次会话使用了 {stats['token_usage']} tokens")
```

### 常见使用模式

**模式 1：对话记忆**

```python
# 存储对话内容
orchestrator.store_memory(
    content="用户说：我喜欢简洁的代码风格",
    bucket_type=SemanticBucketType.USER_INTENT,
)

# 后续对话中自动应用偏好
context = orchestrator.prepare_context(user_input="写一个排序函数")
# 智能体会自动使用简洁的代码风格
```

**模式 2：任务追踪**

```python
from scripts import GlobalStateCapture

capture = GlobalStateCapture(user_id="user_123")

# 追踪任务进度
capture.sync_from_langgraph(
    state={"phase": "implementing", "progress": 0.6},
    node_name="executor",
)

# 任务完成时
capture.sync_from_langgraph(
    state={"phase": "completed", "result": "success"},
    node_name="finalizer",
)
```

---

## 五、架构决策说明

### 为什么是 Skill 而非独立应用？

**设计考量**：

1. **集成性**：记忆系统需要深度集成到智能体的执行流程中
2. **实时性**：需要在智能体决策时即时提供上下文支持
3. **轻量性**：避免额外的服务部署和运维负担
4. **一致性**：与智能体共享同一个会话上下文

**如果是独立应用会怎样？**

```
❌ 独立应用模式：
用户 ──▶ 智能体 ──▶ HTTP API ──▶ 记忆服务
         ↑                      ↓
         └────── 响应 ──────────┘

问题：
- 增加网络延迟
- 需要额外的服务部署
- 状态同步复杂
- 增加故障点

✅ Skill 模式：
用户 ──▶ 智能体 ──▶ Memory Skill (内存)
         ↑              ↓
         └─── 即时响应 ─┘

优势：
- 零网络延迟
- 无需额外部署
- 状态天然同步
- 故障隔离
```

---

## 参考文档

- [Agent Loops 集成指南](agent_loops_integration.md) - 如何在 Agent Loop 中使用
- [使用指南](usage_guide.md) - 详细的使用示例
- [API 类参考](api_class_reference.md) - 完整的 API 文档
