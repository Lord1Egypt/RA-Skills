---
name: Hermes 协议 - 多智能体高并发调度
description: 突触式多智能体通信调度，像人类神经突触一样，毫秒级分发，精准对齐，把 100 个 Agent 同时协同的通信成本降到最低
author: OpenClaw
version: 1.0.3
tags: [hermes, multi-agent, scheduling, high-concurrency]
---

# Hermes 协议 - 多智能体高并发调度

> **核心设计：** 当 100 个 Agent 同时协同工作，通信成本如何降到最低？
> Hermes 模仿人类神经突触：**只有已建立连接（订阅）才传递消息，不做全量广播**

## 前置要求

- **sessions_spawn 集成**：`HermesSessionsIntegration` 依赖外部 `sessions_spawn` API 存在。
  仅使用 `HermesRouter` / `HermesAgent` 手动订阅发布时**无需** sessions_spawn。
- **数据存储**：本 skill 不创建任何数据库文件。如需持久化记忆或技能进化，
  由上层业务自行实现，本 skill 只负责消息调度。

## 特性

- ⚡ **毫秒级分发**：平均单消息投递 < 0.1ms
- 💰 **通信成本最低**：稀疏订阅，只投递感兴趣的 Agent，节省 50%-90% 通信量
- 🎯 **精准对齐**：每个 Agent 只收到自己该处理的任务，不被打扰
- 🔌 **完美集成 sessions_spawn**：spawn 后自动注册订阅，退出自动清理
- 🛡️ **安全可控**：参数可调，不会疯狂消耗资源
- 📦 **零依赖**：纯 Python，只用标准库

## 快速开始

### 导入

```python
from skills.hermes_multiagent_skill import (
    hermes,               # 全局路由器
    HermesRouter,         # 可创建独立路由器
    hermes_sessions,      # 与 sessions_spawn 集成
    HermesSessionsIntegration,
    HermesMessage,        # 消息结构
    HermesAgent,          # Agent 基类
)
```

### 基本用法：手动订阅发布

```python
from skills.hermes_multiagent_skill import hermes, HermesMessage

def my_handler(msg: HermesMessage):
    print(f"收到: {msg.topic}, payload={msg.payload}")

# Agent 订阅自己关心的主题
hermes.subscribe(agent_id="my-agent-id", topic="task:code-review", handler=my_handler)

# 发布消息，自动分发给所有订阅者
hermes.publish(topic="task:code-review", from_agent="publisher-id",
               session_id="session-id", payload={"pr": "..."})
```

### 与 sessions_spawn 集成（推荐日常使用）

```python
from skills.hermes_multiagent_skill import hermes_sessions

# 1. spawn 子智能体后调用
session_key = ...  # sessions_spawn 返回的 session key
hermes_sessions.on_agent_spawn(
    session_key=session_key,
    agent_id="code-review-agent",
    hermes_topics=["task:code-review", "done:web-search"],
    message_handler=lambda topic, payload: print(f"{topic}: {payload}")
)
# → 自动完成所有订阅，消息通过 message_handler 回调

# 2. 提交任务，自动分发
task_id = hermes_sessions.submit_task_to_agents(
    task_type="code-review",
    creator="user",
    session_id="main",
    payload={"pr": "https://github.com/..."}
)
# → Hermes 自动分给所有订阅了 code-review 的 Agent

# 3. Agent 退出自动清理
hermes_sessions.on_agent_exit(session_key)
# → 自动取消所有订阅，注销 Agent
```

### Agent 基类

```python
from skills.hermes_multiagent_skill import HermesAgent, HermesRouter, HermesMessage

router = HermesRouter(max_workers=16)
agent = HermesAgent(agent_id="my-agent", router=router)

def handler(msg: HermesMessage):
    print(msg.payload)

agent.subscribe("task:code-review", handler)
agent.publish("task:done", session_id="s1", payload={"result": "ok"})
agent.unsubscribe("task:code-review")
```

## 性能对比（20 Agent，8 任务）

| 指标 | Hermes 协议 | 传统全量广播 |
|-----|------------|---------------|
| 总投递次数 | **40** | 160 |
| 总耗时 | **11.2 ms** | 23.3 ms |
| 节省通信量 | 75% | - |
| 速度提升 | 2.1x | - |

Agent 越多，节省越明显：100 Agent 能节省 ~90% 通信量。

## API

### HermesRouter

```python
router = HermesRouter(max_workers=None, pool_max=1000)
router.subscribe(agent_id, topic, handler)           # 订阅
router.unsubscribe(topic, agent_id)                  # 取消订阅
router.publish(topic, from_agent, session_id, payload, trace_id="") -> int  # 发布
router.get_stats() -> dict                            # 统计
router.shutdown()                                     # 关闭线程池
```

### HermesAgent

```python
agent = HermesAgent(agent_id, router)
agent.subscribe(topic, handler)        # 订阅主题
agent.unsubscribe(topic)               # 取消订阅
agent.publish(topic, session_id, payload, trace_id="") -> int  # 发布
agent.stats() -> dict                  # 当前 Agent 统计
```

### HermesSessionsIntegration（集成 sessions_spawn）

```python
hermes_sessions.on_agent_spawn(
    session_key, agent_id, hermes_topics,
    message_handler=None   # Callable[[str, Any], None]，默认静默丢弃
) -> HermesSubAgent

hermes_sessions.on_agent_exit(session_key)

hermes_sessions.submit_task_to_agents(
    task_type, creator, session_id, payload
) -> task_id: str

hermes_sessions.publish_done(task_type, task_id, result, session_id, agent_id)
hermes_sessions.publish_system(event_type, payload, session_id, agent_id)
hermes_sessions.list_agents() -> List[HermesSubAgent]
hermes_sessions.stats() -> dict
```

## 安全说明

- **幂等取消**：`unsubscribe` 对同一 agent 多次调用安全，不会导致计数变负
- **对象池上限**：默认最多缓存 1000 条消息，防止极端情况内存膨胀
- **pending 任务清理**：超过 `pending_task_ttl`（默认 1 小时）的任务自动清除
- **输入校验**：空 `agent_id`、空 `topic` 等参数会抛出 `ValueError`
- **线程安全**：所有内部状态通过 `threading.RLock` 保护，50 并发压测零错误

## 依赖

- Python 3.8+
- 零第三方依赖（不使用 SQLite，不创建任何数据库文件）

## License

MIT
