# 微触发管理器 Payload

你是 {{AGENT_NAME}}，正在执行 Living Agent 的微触发管理器任务。

## 第一步：检查用户最后消息时间

1. 调用 `sessions_history(sessionKey="agent:main:main", limit=30)` 获取最近消息
2. 找出最后一条来自用户的消息时间
3. 计算 `minutesSinceLastUser = 当前时间 - 那个时间戳`（分钟）

## 第二步：读取当前状态

读取 `~/.openclaw/workspace/thinking-state.json` 获取：
- microHeartbeatEnabled
- microHeartbeatCronId（微触发思考的 cron ID）

## 第三步：逻辑判断

**如果用户超过 30 分钟没消息 且 microHeartbeatEnabled = false**：
- 用 `cron update` 启用微触发思考 cron：
  - `cron(action="update", jobId=microHeartbeatCronId, patch={"enabled": true, "schedule": {"kind": "every", "everyMs": <5-15分钟随机>}})`
- 更新 thinking-state.json：
  - microHeartbeatEnabled = true

**如果用户最近 30 分钟内有消息 且 microHeartbeatEnabled = true**：
- 用 `cron update` 禁用微触发思考 cron：
  - `cron(action="update", jobId=microHeartbeatCronId, patch={"enabled": false})`
- 更新 thinking-state.json：
  - microHeartbeatEnabled = false

## 第四步：动态调整自己的间隔

根据用户最后消息时间，调整下次检查间隔：

```
如果 minutesSinceLastUser < 5:
    nextInterval = 10 分钟（600000 ms）
如果 5 <= minutesSinceLastUser < 30:
    nextInterval = 5 分钟（300000 ms）# 开始警觉
如果 minutesSinceLastUser >= 30:
    nextInterval = 10 分钟（微触发模式已启动，不需要太频繁检查）
```

用 `cron update` 更新自己的 `schedule.everyMs`。

完成后回复 "✅ 微触发管理器检查完成"。
