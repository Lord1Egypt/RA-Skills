---
name: Hermes Agent
description: 突触式多智能体调度 + 主动记忆洞察 + GEPA 技能自进化
author: OpenClaw
version: 1.0.3
tags: [hermes, multi-agent, scheduling, memory, evolution]
---

# Hermes Agent Skill

> Hermes 协议：极致的"执行效率"与"自我进化"

## 功能特性

- 🧠 **突触式多智能体调度**：100个Agent同时协同，通信成本降到最低，毫秒级分发
- 🧩 **主动记忆与自我建模**：自动提取用户偏好习惯，SQLite FTS5 全文检索快速翻旧账
- 🧬 **GEPA 技能自进化**：多次执行后自动提炼技能卡，越用越聪明
- ⚡ **极致轻量**：纯Python，零依赖，启动快内存占用低
- 🔧 **工程化友好**：完美集成 `sessions_spawn`，开箱即用
- 🔒 **隐私优先**：持久化默认关闭，数据存储完全可控

## 安装

在 OpenClaw 中：
```
/install-skill https://github.com/你的仓库/hermes-agent-skill
```

或者手动放到 `~/.openclaw/workspace/skills/` 即可。

## 快速开始

### 1. 导入

```python
from hermes_agent import (
    hermes,                 # 核心路由器
    hermes_workflow,        # 工作流调度
    hermes_sessions,        # sessions_spawn 集成
    hermes_insight,         # 记忆洞察数据库
    insight_extractor,      # 洞察提取器
    hermes_gepa,            # GEPA 技能进化
    hermes_skill_executor,  # 带自进化的执行器
    hermes_config           # 全局配置（控制持久化开关）
)
```

### 2. 多智能体任务分发

```python
# spawn 子智能体之后，自动注册 Hermes 订阅
hermes_sessions.on_agent_spawn(
    session_key="session-code-agent",
    agent_id="code-review-agent",
    hermes_topics=["task:code-review"]
)

# 提交任务，自动分发给所有订阅了该类型的 Agent
task_id = hermes_sessions.submit_task_to_agents(
    task_type="code-review",
    creator="user",
    session_id="main",
    payload={"pr": "https://github.com/openclaw/openclaw/pull/123"}
)
```

### 3. 主动记忆用户洞察

```python
# 从对话提取洞察
insights = insight_extractor.extract_from_conversation(
    "我喜欢用 Python 写脚本，更快，不喜欢重型框架",
    context="对话上下文"
)

# 存储
for ins in insights:
    hermes_insight.add_insight(ins)

# 全文检索
results = hermes_insight.search_memory("Python")
```

### 4. GEPA 技能自进化

```python
# 开始任务，自动记录
exec_id = hermes_skill_executor.start_task(
    "video-clip",
    {"input": "input.mp4", "start": 10, "end": 20}
)

# 一步一步执行，自动记录
hermes_skill_executor.step("load-video", load_video, path)
hermes_skill_executor.step("cut-segment", cut, start, end)
result = hermes_skill_executor.step("export-video", export, output)

# 完成，自动触发提炼
hermes_skill_executor.finish_task(True, result)

# 几次之后自动生成技能卡
skill = hermes_gepa.get_skill_card("video-clip")
print(f"推荐步骤: {skill.steps}")
print(f"成功率: {skill.success_rate:.1%}")
```

## 架构

```
hermes.py                     # 核心路由器（突触式通信）
├─ hermes_config.py           # 全局配置（持久化开关、隐私控制）
├─ hermes_openclaw.py         # 工作流调度（任务/进度/完成）
├─ hermes_sessions_integration.py  # sessions_spawn 自动集成
├─ hermes_agent_insight.py    # 主动记忆 + FTS5 全文检索
└─ hermes_skill_evolution.py  # GEPA 技能自进化
```

## 控制参数（避免 token 浪费）

GEPA 默认参数：
- `min_success_samples = 2`  - 最少 2 次成功才提炼
- `min_new_executions = 3`   - 已有技能后新增 3 次才重新提炼
- `max_refines_per_task = 10` - 单个任务最多提炼 10 次
- `min_improvement = 0.05`   - 成功率变化 < 5% 不提炼

自定义：
```python
from hermes_skill_evolution import GEPASkillEvolution
my_gepa = GEPASkillEvolution(
    min_success_samples=5,
    max_refines_per_task=5
)
```

## 数据存储

**默认关闭，需显式开启。**

```
# 方式一：环境变量
export HERMES_PERSISTENCE_ENABLED=true

# 方式二：运行时代码控制
from hermes_agent import hermes_config
hermes_config.set_persistence(True)
```

开启后数据存储位置：
- `~/.hermes/insights.db` - 洞察和记忆（SQLite FTS5）
- `~/.hermes/skills.db` - 技能卡和执行记录

首次运行自动创建，不需要手动初始化。

### 隐私控制参数

| 环境变量 | 默认值 | 说明 |
|----------|--------|------|
| `HERMES_PERSISTENCE_ENABLED` | `false` | 是否启用持久化（默认关闭）|
| `HERMES_INSIGHT_EXTRACTION_ENABLED` | `true` | 是否提取对话洞察 |
| `HERMES_SENSITIVE_FILTER_ENABLED` | `true` | 是否自动过滤敏感信息 |
| `HERMES_SESSION_LOG_LEVEL` | `summary` | fallback 日志级别：`off`/`summary`/`full` |
| `HERMES_INSIGHTS_DB` | `~/.hermes/insights.db` | 洞察 DB 路径 |
| `HERMES_SKILLS_DB` | `~/.hermes/skills.db` | 技能 DB 路径 |

**敏感信息过滤**：自动过滤 API Key、密码、Token、私钥、证书、邮箱等。

## 依赖

- Python 3.8+
- 不需要第三方包，SQLite 内置

## 性能

测试数据（100 Agent，1000 条发布，49500 次投递）：
- 平均单消息处理：**14 微秒** → 真·毫秒级分发

## License

MIT
