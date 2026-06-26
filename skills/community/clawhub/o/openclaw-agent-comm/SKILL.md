---
name: agent-communication
description: 标准化跨 Agent 通信协议。当需要向另一个 Agent 询问、协作或委托任务时，使用本技能。
version: 1.0.0
---

# Agent 间通信协议

## 核心原则

1. **先查 sessionKey**：用 `sessions_list` 获取实时 sessionKey，禁止使用记忆中的硬编码值
2. **按需选择模式**：阻塞 / 非阻塞 / 即发即走，根据任务性质选择
3. **减少目标开销**：请求中带上必要信息，让目标快速理解
4. **统一回复归属**：主 Agent 统一处理引用回复，下游 Agent 只返回结果

---

## 通信工具

| 工具 | 用途 | 等待方式 |
|------|------|----------|
| `sessions_send` | 点对点通信 | 可配置超时 |
| `sessions_spawn` | 后台任务委托 | 非阻塞，结果自动推送 |
| `sessions_list` | 获取实时 sessionKey | — |

---

## 通信模式

### 模式 A：阻塞等待（查询、学习）
```
sessions_send({ sessionKey, message, timeoutSeconds: 120 })
→ 等待目标回复（最多 5 轮 ping-pong）
→ 返回结果
```

### 模式 B：即发即走（通知、传达）
```
sessions_send({ sessionKey, message, timeoutSeconds: 0 })
→ 立即返回，不等待结果
```

### 模式 C：后台委托（任务执行）
```
sessions_spawn({ task, label?, agentId?, runTimeoutSeconds?, cleanup? })
→ 立即返回 { status: "accepted", runId, childSessionKey }
→ 任务完成后自动推送结果到请求方
```

---

## 请求消息模板

所有 `sessions_send` 请求统一使用以下格式：

```
【Agent 间通信】
发件方: <我的名字> (<我的agentId>)
收件方: <目标agent>
source sessionKey: <当前session的key>
通信目的: <场景类型>
期望响应: <阻塞等待/即发即走/非阻塞>
timeout: <秒数>

---
用户需求: <用户原话>

<具体请求内容>

---
上下文摘要: <补充说明>
```

---

## 场景类型

### 场景 1：知识获取（阻塞）
**意图**：问、学、查询、确认
**工具**：`sessions_send`，timeoutSeconds: 120
```
sessions_send({ sessionKey, message, timeoutSeconds: 120 })
```

### 场景 2：任务委托（非阻塞）
**意图**：让做、研究、处理、分析
**工具**：`sessions_spawn`
```
sessions_spawn({ task: "...", label?: "...", agentId?: "...", runTimeoutSeconds?: 0 })
```

### 场景 3：单向通知（即发即走）
**意图**：通知、传达、转发（不关心结果）
**工具**：`sessions_send`，timeoutSeconds: 0
```
sessions_send({ sessionKey, message, timeoutSeconds: 0 })
```

### 场景 4：顺序协作
多个 `sessions_spawn` 串联，前一个完成后再启动下一个：
```
用户: "先让A分析，再让B基于结果写报告"
→ sessions_spawn A
→ 等待 A 完成（通告回我）
→ sessions_spawn B，附上 A 的结果
→ 汇总后汇报用户
```

### 场景 5：多 Agent 并行汇总
```
用户: "收集多个 Agent 的状态并汇总"
→ 并行 sessions_spawn 多个目标
→ 等待所有完成（收集所有通告）
→ 汇总结果 → 汇报用户
```

---

## 结果交付方式

**推荐**：下游 Agent 只返回结果，由主 Agent统一回复用户。

- `sessions_spawn` 的结果自动推送到发起方的绑定渠道
- 如果需要结果直接发给用户，在 task 中说明即可，不需要用 `message` 工具发

---

## 超时配置

| 模式 | timeoutSeconds | 说明 |
|------|----------------|------|
| 阻塞等待 | **120** | 等待目标处理和回复 |
| 即发即走 | **0** | 发完即返回 |
| 后台委托 | **0**（默认无超时） | 结果自动推送 |

---

## 控制指令

在消息正文中精确包含以下内容可控制流程：

| 指令 | 效果 |
|------|------|
| `REPLY_SKIP` | 停止 ping-pong 回复循环 |
| `ANNOUNCE_SKIP` | 不发布任何结果通告 |

---

## 错误处理

### 目标 Agent 不存在
```
❌ 目标 Agent "<name>" 不存在或不可用

可用 Agent（从 sessions_list 获取）:
- <list>

请确认目标名称，或选择其他 Agent。
```

### 通信超时
```
⚠️ 与目标 Agent 通信超时（120秒未响应）

可能原因：
1. 目标正在处理其他任务
2. 任务较复杂需要更长时间

建议：
1. 稍后重试
2. 改用 sessions_spawn 后台执行
```

### 未知错误
```
⚠️ 与目标 Agent 通信失败

错误: <error message>

建议：
1. 检查 sessionKey 是否正确
2. 尝试 sessions_spawn 后台执行
```

---

## 快速参考

| 需求 | 工具 | timeout |
|------|------|---------|
| 问/学/查询 | `sessions_send` | 120s（阻塞） |
| 让做/研究/处理 | `sessions_spawn` | 非阻塞 |
| 通知/传达 | `sessions_send` | 0（即发即走） |
| 顺序协作 | `sessions_spawn` × n | 非阻塞 |
| 多 Agent 汇总 | 并行 `sessions_spawn` | 非阻塞 |
