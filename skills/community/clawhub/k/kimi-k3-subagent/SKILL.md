---
name: kimi-k3-subagent
description: "Kimi K3子Agent架构 - 两阶段批量调度、生命周期管理、限流策略。借鉴MoonshotAI/kimi-code源码，提供Python实现"
metadata:
  version: 1.0.0
  source: "github.com/MoonshotAI/kimi-code (MIT)"
  author: "曙光"
  date: "2026-07-29"
  tags:
    - subagent
    - swarm
    - batch-scheduling
    - rate-limit
    - lifecycle
    - agent-architecture
---

# Kimi K3 Subagent 架构

Kimi K3 (MoonshotAI) 的子Agent调度架构，蒸馏为Python实现。

## 架构

```
SubagentHost (生命周期管理)
  ├── spawn()    — 创建新子Agent
  ├── resume()   — 恢复已有子Agent(保留上下文)
  ├── retry()    — 重试失败子Agent
  └── runQueued()— 批量执行

SubagentBatch (两阶段调度引擎)
  ├── 正常阶段: 5个立即启动, 之后每700ms启动1个
  └── 限流阶段: 指数退避(3s/6s/12s/24s) + 容量收缩/恢复(3分钟)

SwarmEventEmitter (生命周期事件)
  ├── spawned / started / completed / failed / suspended / batch_done
  └── on() / off() / emit() 监听机制

SummaryCheck (结果质量控制)
  └── 子Agent结果 ≥ 200字符, 不足自动补全
```

## 内置子Agent类型

| 类型 | 用途 | 工具 |
|------|------|------|
| coder | 通用编码执行 | read/write/edit/bash/grep/glob |
| explore | 探索调研 | read/grep/glob/web_search/web_fetch |
| plan | 规划设计 | read/write/web_search |
| btw | 侧通道问答 | 无工具(纯文本) |

## 使用方法

### 1. 批量并行任务

```python
from scripts.lib.agent import SubagentHost, SubagentBatch, QueuedSubagentTask

host = SubagentHost(session, "main_agent")

tasks = [
    QueuedSubagentTask(
        data={"code": "600519"},
        prompt="分析贵州茅台资金流向",
        profile_name="explore",
    ),
    QueuedSubagentTask(
        data={"code": "000858"},
        prompt="分析五粮液资金流向",
        profile_name="explore",
    ),
]
results = await host.run_queued(tasks)
```

### 2. 生命周期管理

```python
# 创建子Agent
handle = await host.spawn("coder", "扫描板块资金流")

# 恢复已有子Agent
handle = await host.resume(agent_id, "继续之前的分析")

# 重试失败
handle = await host.retry(agent_id, "重试板块扫描")
```

### 3. 事件监听

```python
from scripts.swarm import SwarmEventType

scheduler = SwarmScheduler(executor)

def on_completed(event_type, data):
    print(f"Task {data['task_id']} completed in {data['result_len']} chars")

scheduler.on(SwarmEventType.COMPLETED, on_completed)
results = await scheduler.run(tasks)
```

### 4. 结果摘要检查

子Agent结果自动确保≥200字符, 不足时自动补全:

```python
from scripts.swarm import _ensure_min_summary

result = _ensure_min_summary(short_result)
# 不足200字符自动追加说明
```

## 限流策略

```
正常阶段 → 遇到RateLimit → 限流阶段
  ├── 容量收缩: 每次限流-1, 最小1
  ├── 重试间隔: 3s/6s/12s/24s... 指数退避
  └── 容量恢复: 3分钟无新限流则+1
```

## 文件清单

| 文件 | 说明 |
|------|------|
| scripts/lib/agent/subagent_types.py | 类型定义 |
| scripts/lib/agent/subagent_host.py | 生命周期管理 |
| scripts/lib/agent/subagent_batch.py | 批量调度引擎 |
| scripts/swarm/__init__.py | 统一调度器(含事件+摘要检查) |
| learnings/kimi-k3-subagent-architecture.md | 完整学习笔记 |
