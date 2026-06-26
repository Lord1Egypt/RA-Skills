# Agent Loops 集成指南

> 本文档说明如何将 Agent Memory System 与 Agent Loop 集成，包含完整的端到端示例、故障排查和最佳实践。

## 目录

1. [概述](#概述)
2. [集成方式](#集成方式)
3. [完整端到端示例](#完整端到端示例)
4. [故障排查指南](#故障排查指南)
5. [性能优化配置](#性能优化配置)
6. [实际应用场景](#实际应用场景)
7. [依赖和环境要求](#依赖和环境要求)
8. [配置参数详解](#配置参数详解)
9. [最佳实践](#最佳实践)

---

## 概述

Agent Loop 是智能体的核心执行模式，通过"感知-决策-行动-观察"循环完成任务。Agent Memory System 为 Agent Loop 提供记忆能力，实现跨会话的上下文保持和智能决策。

---

## 集成方式

### 方式 1：状态同步集成

```python
from scripts.state_capture import GlobalStateCapture

# 创建状态捕捉器
capture = GlobalStateCapture(
    user_id="user_123",
    storage_path="./state_storage",
)

# 在 Agent Loop 的每个节点同步状态
checkpoint_id = capture.sync_from_langgraph(
    state={"phase": "planning", "current_task": "task_1"},
    node_name="planner",
)
```

### 方式 2：事件订阅集成

```python
# 订阅关键事件
subscription_id = capture.subscribe(
    event_types=[
        StateEventType.PHASE_CHANGE,
        StateEventType.TASK_SWITCH,
        StateEventType.ERROR_OCCURRED,
    ],
    callback=on_state_change,
)

def on_state_change(event):
    # 处理状态变化
    print(f"状态变化: {event.event_type}")
```

### 方式 3：完整循环集成

```python
from scripts.context_orchestrator import create_context_orchestrator

# 创建编排器
orchestrator = create_context_orchestrator(
    user_id="user_123",
    session_id="session_456",
    max_context_tokens=32000,
)

# 在 Agent Loop 的每个步骤使用
for step in agent_loop:
    # 准备上下文（包含历史记忆）
    context = orchestrator.prepare_context(
        user_input=step.input,
        system_instruction=step.instruction,
    )

    # 执行决策
    action = decide(context)

    # 存储结果到记忆
    orchestrator.store_memory(
        content=action.description,
        bucket_type=SemanticBucketType.TASK_RESULT,
    )
```

---

## 完整端到端示例

### 基础 Agent Loop 集成

```python
from scripts import (
    create_context_orchestrator,
    GlobalStateCapture,
    SemanticBucketType,
    StateEventType,
)

class AgentLoopWithMemory:
    """集成 Agent Memory System 的 Agent Loop"""
    
    def __init__(self, user_id: str, session_id: str):
        # 初始化记忆系统
        self.orchestrator = create_context_orchestrator(
            user_id=user_id,
            session_id=session_id,
            max_context_tokens=32000,
        )
        
        # 初始化状态捕捉
        self.state_capture = GlobalStateCapture(
            user_id=user_id,
            storage_path="./state_storage",
        )
        
        # 订阅关键事件
        self.subscription_id = self.state_capture.subscribe(
            event_types=[
                StateEventType.PHASE_CHANGE,
                StateEventType.TASK_SWITCH,
                StateEventType.ERROR_OCCURRED,
            ],
            callback=self._on_state_change,
        )
        
        self.max_iterations = 10
    
    def run(self, user_input: str, tools: list) -> str:
        """执行 Agent Loop"""
        try:
            # 存储用户意图
            self.orchestrator.store_memory(
                content=user_input,
                bucket_type=SemanticBucketType.USER_INTENT,
            )
            
            # 主循环
            for iteration in range(self.max_iterations):
                # 准备上下文（包含历史记忆）
                context = self.orchestrator.prepare_context(
                    user_input=user_input,
                    system_instruction="你是一个智能助手",
                )
                
                # 执行决策和行动
                action = self._decide(context, tools)
                result = self._execute_action(action)
                
                # 存储结果到记忆
                self.orchestrator.store_memory(
                    content=result,
                    bucket_type=SemanticBucketType.TASK_RESULT,
                )
                
                # 同步状态
                self.state_capture.sync_from_langgraph(
                    state={"phase": "executing", "iteration": iteration},
                    node_name="executor",
                )
                
                if self._is_task_complete(result):
                    break
            
            return self._generate_final_answer()
            
        except Exception as e:
            print(f"Agent Loop 执行失败: {e}")
            return self._fallback_response(user_input)
        
        finally:
            # 清理资源
            stats = self.orchestrator.end_session()
            self.state_capture.unsubscribe(self.subscription_id)
    
    def _on_state_change(self, event):
        """状态变化回调"""
        print(f"[状态变化] {event.event_type}: {event.details}")

# 使用示例
agent = AgentLoopWithMemory("user_123", "session_456")
result = agent.run("帮我分析数据", [analyze_tool])
```

### LangGraph 深度集成

```python
from langgraph.graph import StateGraph, END
from scripts import create_context_orchestrator, SemanticBucketType

def build_agent_graph(user_id: str, session_id: str):
    """构建集成记忆系统的 LangGraph"""
    
    orchestrator = create_context_orchestrator(
        user_id=user_id,
        session_id=session_id,
    )
    
    def planner_node(state):
        context = orchestrator.prepare_context(
            user_input=state["user_input"],
            system_instruction="你是规划专家",
        )
        plan = generate_plan(context)
        orchestrator.store_memory(str(plan), SemanticBucketType.PLAN)
        return {"plan": plan}
    
    def executor_node(state):
        context = orchestrator.prepare_context(state["plan"])
        result = execute_plan(context, state["plan"])
        orchestrator.store_memory(result, SemanticBucketType.TASK_RESULT)
        return {"result": result}
    
    # 构建图
    graph = StateGraph(AgentState)
    graph.add_node("planner", planner_node)
    graph.add_node("executor", executor_node)
    graph.set_entry_point("planner")
    graph.add_edge("planner", "executor")
    graph.add_edge("executor", END)
    
    return graph.compile(), orchestrator
```

---

## 故障排查指南

### 常见问题

#### 问题 1: 导入错误

```python
ImportError: cannot import name 'GlobalStateCapture'
```

**解决方案**: 检查导入路径
```python
from scripts import GlobalStateCapture  # ✓ 正确
from scripts.state_capture import GlobalStateCapture  # ✗ 错误
```

#### 问题 2: Token 预算不足

```python
ValueError: Context exceeds token budget: 35000 > 32000
```

**解决方案**:
```python
# 方案 1: 增加预算
orchestrator = create_context_orchestrator(max_context_tokens=48000)

# 方案 2: 启用压缩
context = orchestrator.prepare_context(enable_compression=True)

# 方案 3: 限制历史
context = orchestrator.prepare_context(max_history_turns=5)
```

#### 问题 3: Redis 连接失败

```python
ConnectionError: Could not connect to Redis
```

**解决方案**:
```python
# 使用文件存储降级
orchestrator = create_context_orchestrator(
    storage_backend="file",  # 降级到文件存储
)
```

### 调试技巧

```python
import logging

# 启用详细日志
logging.basicConfig(level=logging.DEBUG)

# 获取统计信息
stats = orchestrator.get_stats()
print(f"Token 使用: {stats['token_usage']}")
print(f"记忆数量: {stats['memory_count']}")
print(f"缓存命中率: {stats['cache_hit_rate']:.1%}")

# 检查状态同步
state_snapshot = state_capture.get_current_state()
print(f"当前阶段: {state_snapshot.phase}")
```

---

## 性能优化配置

### Token 预算管理

```python
# 根据任务复杂度调整预算
orchestrator = create_context_orchestrator(
    max_context_tokens=48000,  # 复杂任务增加预算
)

# 动态压缩
context = orchestrator.prepare_context(
    enable_compression=True,  # 启用自动压缩
    compression_threshold=0.8,  # 压缩阈值
)
```

### 缓存策略

```python
# 配置缓存
orchestrator = create_context_orchestrator(
    cache_config={
        "enable_l1_cache": True,  # 内存缓存
        "l1_max_size": 1000,      # 最大条目数
    }
)

# 预热缓存
orchestrator.warmup_cache(hot_memories=["user_profile"])
```

---

## 实际应用场景

### 场景 1: 代码助手

```python
class CodeAssistant:
    """带记忆的代码助手"""
    
    def __init__(self, user_id: str):
        self.orchestrator = create_context_orchestrator(
            user_id=user_id,
            max_context_tokens=48000,  # 代码需要更多上下文
        )
    
    def analyze_code(self, code: str):
        # 存储代码上下文
        self.orchestrator.store_memory(
            f"用户代码: {code[:200]}...",
            SemanticBucketType.CODE,
        )
        
        # 准备上下文（包含编程习惯）
        context = self.orchestrator.prepare_context(
            user_input=code,
            system_instruction="你是代码分析专家",
        )
        
        return analyze(context, code)
```

### 场景 2: 多轮对话

```python
class ChatAgent:
    """带记忆的对话代理"""
    
    def __init__(self, user_id: str):
        self.orchestrator = create_context_orchestrator(user_id=user_id)
    
    def chat(self, message: str):
        # 准备上下文（包含对话历史）
        context = self.orchestrator.prepare_context(
            user_input=message,
            system_instruction="记住用户偏好和历史对话",
        )
        
        response = generate_response(context, message)
        
        # 存储对话
        self.orchestrator.store_memory(
            response,
            SemanticBucketType.CONVERSATION,
        )
        
        return response
```

---

## 依赖和环境要求

### 版本要求

```txt
pydantic>=2.0.0          # 数据模型验证
typing-extensions>=4.0.0 # 类型扩展
langgraph>=0.0.20        # LangGraph 框架（可选）
tiktoken>=0.5.0          # Token 计数
redis>=4.5.0             # Redis 存储（可选）
mmh3>=3.0.0              # 布隆过滤器（可选）
cryptography>=41.0.0     # 数据加密（可选）
```

### 环境配置

```python
from dataclasses import dataclass

@dataclass
class MemoryConfig:
    """记忆系统配置"""
    storage_base_path: str = "./memory_data"
    max_context_tokens: int = 32000
    redis_host: str = "localhost"  # 可选
```

---

## 配置参数详解

### ContextOrchestrator 参数

| 参数 | 类型 | 默认值 | 说明 | 推荐值 |
|------|------|--------|------|--------|
| `user_id` | str | 必填 | 用户唯一标识 | - |
| `session_id` | str | 必填 | 会话唯一标识 | - |
| `max_context_tokens` | int | 32000 | 最大上下文 Token 数 | 简单任务: 16000<br>复杂任务: 48000 |
| `enable_compression` | bool | True | 启用自动压缩 | 建议启用 |
| `max_history_turns` | int | 10 | 最大历史轮次 | 对话: 20<br>任务: 5 |

### GlobalStateCapture 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `user_id` | str | 必填 | 用户唯一标识 |
| `storage_path` | str | "./state_storage" | 状态存储路径 |
| `max_checkpoints` | int | 100 | 最大检查点数 |

---

## 最佳实践

### 1. 使用元技能常驻

Agent Memory System 是元技能，应在 Agent Loop 启动时初始化，在整个循环周期内复用：

```python
# ✓ 正确：在启动时初始化
orchestrator = create_context_orchestrator(user_id, session_id)

for step in agent_loop:
    # 复用同一个实例
    context = orchestrator.prepare_context(step.input)

# ✗ 错误：每次循环都创建新实例
for step in agent_loop:
    orchestrator = create_context_orchestrator(user_id, session_id)
```

### 2. 合理配置 Token 预算

根据任务复杂度调整 `max_context_tokens`：

```python
# 简单任务（对话、查询）
max_context_tokens=16000

# 中等任务（分析、总结）
max_context_tokens=32000

# 复杂任务（代码分析、多步推理）
max_context_tokens=48000
```

### 3. 事件驱动更新

仅在关键事件时更新记忆，避免频繁的状态同步：

```python
# ✓ 正确：关键事件时更新
if task_complete or error_occurred:
    orchestrator.store_memory(result, bucket_type)

# ✗ 错误：每次循环都更新
for step in agent_loop:
    orchestrator.store_memory(result, bucket_type)
```

### 4. 错误处理和降级

捕获并处理状态同步错误，使用降级策略确保可用性：

```python
try:
    context = orchestrator.prepare_context(user_input)
except Exception as e:
    # 降级策略：使用简化上下文
    context = simplified_context(user_input)
    logger.warning(f"Context preparation failed, using fallback: {e}")
```

---

## 关键集成点

### 1. 初始化阶段
- 创建 `GlobalStateCapture` 实例
- 创建 `ContextOrchestrator` 实例
- 订阅关键事件

### 2. 执行阶段
- 每个状态变化时调用 `sync_from_langgraph`
- 使用 `prepare_context` 获取历史上下文
- 使用 `store_memory` 存储执行结果

### 3. 清理阶段
- 调用 `end_session` 保存会话统计
- 取消事件订阅

---

## 参考文档

- [架构总览](architecture_overview.md)
- [Agent Loops 进阶指导](agent_loops_advanced.md)
- [状态管理类 API](api_class_reference.md#三状态管理类)
- [上下文编排类 API](api_class_reference.md#七上下文编排类)
- [使用指南](usage_guide.md)

---

> **文档版本**：2.0  
> **更新日期**：2024年  
> **适用场景**：Agent Memory System 集成、状态同步、事件订阅、性能优化
