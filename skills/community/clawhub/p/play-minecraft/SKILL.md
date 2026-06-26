---
name: openclaw-mindcraft-controller
description: 通过 Mindcraft HTTP API 控制 Minecraft Bot（无内置 LLM）。当用户提到 OpenClaw、外部 agent、REST 接口控制、读取状态、执行动作、批量任务编排时使用。
---

# OpenClaw Mindcraft Controller

## 适用场景

- 用户要用 OpenClaw 或任意外部系统控制 `mindcraft` Bot。
- 用户要求“不要内置 LLM，只走接口调用”。
- 用户需要：读取状态、查询动作 schema、执行动作、排错与恢复。

## 快速流程

1. 确认服务已启动：`node main.js`
2. 确认配置为外控模式：`settings.js` 中 `external_controller_only: true`
3. 用 `GET /api/v1/agents` 找到 agent 名（如 `andy`）
4. 用 `GET /api/v1/agents/:agentName/actions/schema` 获取动作参数定义
5. 用 `POST /api/v1/agents/:agentName/actions/execute` 执行动作
6. 用 `GET /api/v1/agents/:agentName/state` 校验动作结果

## 控制规则

- 动作前先查 schema，不要硬编码参数类型和数量。
- 长动作执行后必须二次读 state，避免“命令发送成功但未达成目标”。
- 异常时先执行 `!stop`，再做恢复动作。
- 多动作编排推荐“小步执行 + 每步校验”，不要一次提交过长链路。

## API 基础信息

- Base URL: `http://localhost:8080`
- Content-Type: `application/json`
- 关键接口：
  - `GET /api/v1/agents`
  - `GET /api/v1/agents/:agentName/state`
  - `GET /api/v1/agents/:agentName/actions/schema`
  - `POST /api/v1/agents/:agentName/actions/execute`

详细字段和示例见 [reference.md](reference.md) 与 [examples.md](examples.md)。

## 推荐执行模板

1. **发现 Agent**
   - 调用 `/agents`
   - 选择 `in_game=true` 的 agent
2. **加载能力**
   - 调用 `/actions/schema`
   - 缓存 command + params 描述
3. **执行动作**
   - 调用 `/actions/execute`，传 `command` + `args`
4. **结果验证**
   - 读 `/state`，核对位置、背包、健康、当前动作
5. **失败恢复**
   - 执行 `!stop`
   - 重新规划下一步动作

## 常见故障处理

- `Agent 'xxx' not found`
  - 先调 `/agents`，确认 agent 名称。
- `Agent 'xxx' is not connected in game`
  - Bot 未进服；检查 Minecraft 是否开放 LAN 端口，或进程是否重启失败。
- 参数不匹配（args count/type）
  - 以 `/actions/schema` 为准重建入参。
- 命令存在但效果不符合预期
  - 读 `/state` 二次确认，再做补偿动作（例如 `!stop`、`!goToCoordinates` 重试）。

## 输出要求（给 OpenClaw 的调用层）

- 每次动作调用都记录：
  - request payload
  - response payload
  - state 前后快照（至少位置/背包/健康）
- 失败返回要保留原始 `error` 字段，便于排查。
