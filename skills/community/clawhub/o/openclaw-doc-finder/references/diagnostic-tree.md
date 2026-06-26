# OpenClaw 问题诊断决策树

> 基于官方文档构建的"症状 → 排查路径"速查

---

## 决策树

```
用户报告问题
    │
    ├─ 说"任务卡住" / "没有反应"
    │       │
    │       ├─ 先问：是什么类型的任务？
    │       │   ├─ cron 任务 → gateway/heartbeat.md + automation/cron-jobs.md
    │       │   ├─ heartbeat → gateway/heartbeat.md
    │       │   ├─ 子代理任务 → tools/subagents.md + concepts/queue.md
    │       │   └─ 手动触发 → concepts/agent-loop.md
    │       │
    │       └─ 排查命令：
    │           openclaw logs --follow
    │           openclaw sessions list
    │           → 找 "queued for …ms" 确认队列是否在 drain
    │
    ├─ 消息队列相关
    │       │
    │       ├─ 配置项：messages.queue（见下方配置片段）
    │       ├─ 文档：concepts/queue.md
    │       └─ 常见问题：
    │           Q: 消息堆积 → 检查 debounceMs / cap
    │           Q: 响应延迟 → 检查 main lane 并发是否耗尽
    │           Q: 消息丢失 → 检查 drop 策略（默认 summarize）
    │
    ├─ 配置问题
    │       │
    │       ├─ openclaw config get messages.queue
    │       ├─ openclaw config get agents.defaults.maxConcurrent
    │       └─ 文档：gateway/configuration.md
    │
    ├─ 报错类
    │       │
    │       ├─ 429 / rate limit → providers/<name>.md
    │       ├─ 401/403 凭证 → gateway/secrets.md
    │       ├─ 连接失败 → channels/troubleshooting.md
    │       └─ 执行阻塞 → concepts/agent-loop.md + concepts/queue.md
    │
    └─ 性能/并发问题
            │
            ├─ openclaw config get agents.defaults.maxConcurrent
            ├─ 默认值：main=4, subagent=8, 其他=1
            └─ 文档：concepts/queue.md
```

---

## 消息队列配置片段

```json
{
  "messages": {
    "queue": {
      "mode": "collect",
      "debounceMs": 1000,
      "cap": 20,
      "drop": "summarize",
      "byChannel": {
        "discord": "collect"
      }
    }
  }
}
```

**关键参数说明：**
- `debounceMs`: 等待静默时间，防止"continue, continue"
- `cap`: 每 session 最大排队数（默认 20）
- `drop`: 溢出策略（old/new/summarize）
- `mode`: collect/steer/followup/steer-backlog

---

## 排查命令速查

```bash
# 队列状态
openclaw logs --follow 2>&1 | grep "queued for"

# Session 列表
openclaw sessions list

# 并发配置
openclaw config get agents.defaults.maxConcurrent

# 队列配置
openclaw config get messages.queue

# Gateway 状态
openclaw gateway status
openclaw doctor
```
