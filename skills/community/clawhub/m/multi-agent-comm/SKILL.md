---
name: multi-agent-comm
description: "Multi-Agent Communication Protocol — 通用多智能体通信框架。用于在 OpenClaw 中编排多个 Agent 之间的结构化通信、任务委派和协同工作。适用场景：(1) 在主 Agent 与子 Agent 之间传递消息 (2) 多个独立 Agent（如 QClaw、学术助手、学生工作助理等）之间的双向通信 (3) 将大任务分解为并行子任务并收集结果 (4) 跨 Agent 共享上下文和记忆。关键词：agent communication, ACP, multi-agent, subagent, session spawn, agent 间通信, 多智能体协同, 任务委派。"
---

# Multi-Agent Communication

通用多智能体通信框架，基于 OpenClaw 的 session 机制实现 Agent 间结构化通信。

## 通信架构概览

```
┌──────────────┐
│   Main Agent  │ (QClaw / 主 Agent)
│  (编排中心)    │
└──┬───┬───┬───┘
   │   │   │
   ▼   ▼   ▼
┌────┐┌────┐┌────┐
│Sub1││Sub2││Sub3│  (subagent / acp runtime)
└────┘└────┘└────┘
```

**三种通信模式，按复杂度递增：**

| 模式 | 方式 | 适用场景 |
|------|------|----------|
| 1. Subagent 委派 | `sessions_spawn` (runtime=subagent) | 单向任务下发，等结果 |
| 2. 持久会话通信 | `sessions_spawn` (mode=session) + `sessions_send` | 双向持续对话 |
| 3. 跨 Agent ACP | `sessions_spawn` (runtime=acp) + agent 配置 | 独立 Agent 间协议通信 |

## 模式 1：Subagent 委派（最常用）

一次性任务委派，子 agent 完成后自动销毁。

```markdown
1. 用 `sessions_spawn` 创建子 agent：
   - runtime: "subagent"
   - mode: "run"（一次性）或 "session"（持久）
   - task: 任务描述（越具体越好）
   - model/thinking: 可选覆盖
   - cwd: 可指定工作目录
   - timeoutSeconds: 超时保护

2. 子 agent 完成后自动返回结果到当前会话

3. 如需查看/管理子 agent：
   - subagents(action="list") — 列出运行中的子 agent
   - subagents(action="steer", target=id, message=...) — 向子 agent 发送消息
   - subagents(action="kill", target=id) — 终止子 agent
```

**最佳实践：**
- Task 描述必须自包含，子 agent 无继承主会话上下文（除非 lightContext=true）
- 大任务拆为多个并行 subagent 时，用 `sessions_yield` 等待结果
- 用 label 给子 agent 命名便于后续管理

## 模式 2：持久会话通信

需要双向持续对话时使用。

```markdown
1. 创建持久会话：
   sessions_spawn(mode="session", task="初始指令", label="my-assistant")

2. 后续通过 session key 通信：
   sessions_send(sessionKey="...", message="后续指令")

3. 查看会话列表和状态：
   sessions_list(kinds=["session"])
```

**适用场景：**
- 需要多轮交互的长期协作 agent
- 有状态的工作流（如项目管理、持续监控）

## 模式 3：跨 Agent ACP 通信

用于独立的、有自己 system prompt 和配置的 Agent 之间通信。

详细配置和架构参考：[references/acp-setup.md](references/acp-setup.md)

### 快速开始

```markdown
1. 在 gateway.yaml 的 agents 部分定义新 agent（见 acp-setup.md）

2. 通过 acp runtime 通信：
   sessions_spawn(
     runtime="acp",
     agentId="student-assistant",
     task="任务描述",
     mode="run"  # 或 "session"
   )

3. 恢复已有 ACP 会话：
   sessions_spawn(
     runtime="acp",
     resumeSessionId="session-uuid"
   )
```

## 并行编排模式

同时启动多个子 agent 处理不同子任务，然后汇总结果。

```markdown
1. 依次 spawn 多个 subagent（每个处理独立子任务）
2. 调用 sessions_yield() 让出当前 turn
3. 子 agent 完成后结果自动返回
4. 汇总各子 agent 结果，生成最终回复
```

**规则：**
- 各子任务必须相互独立（无数据依赖）
- 每个 subagent 的 task 必须自包含
- 子 agent 数量建议 2-5 个，避免资源耗尽
- 每个都设置合理的 timeoutSeconds

## 共享状态策略

Agent 间不自动共享内存，需要手动传递：

| 策略 | 方法 | 适用场景 |
|------|------|----------|
| 文件系统 | 读写 workspace 中的共享文件 | 大量数据、持久化 |
| 任务描述 | 在 task/message 中包含必要上下文 | 小量上下文 |
| 文件引用 | 通过 cwd 或 attachments 传递文件 | 输入文件处理 |
| 环境变量 | 子 agent 继承父进程环境变量 | 配置信息 |

## 常见模式参考

- **分治汇总**：将大任务拆分为 N 个子任务 → 并行 spawn → yield → 汇总
- **审查链**：Agent A 生成内容 → Agent B 审查/修改 → 返回结果
- **专家协商**：多个领域专家 agent 各自分析 → 汇总决策
- **监控上报**：后台 agent 持续监控 → 有事时通过 sessions_send 上报

## 跨设备复用

本 skill 无硬编码路径，可直接通过 junction/symlink 链接到任意设备的 skills 目录。Agent 定义在 gateway config 中，跟随各自实例配置。

将此 skill 放入公共 skills 库 `~/.agents/skills/` 后，所有 agent 共享：
```powershell
# junction 链接示例
cmd /c mklink /J "~\.claude\skills\multi-agent-comm" "~\.agents\skills\multi-agent-comm"
```
