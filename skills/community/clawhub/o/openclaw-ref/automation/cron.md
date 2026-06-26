# 定时任务 (Cron) 参考

## 核心概念
- 运行在 Gateway 内部，持久化存储在 `~/.openclaw/cron/jobs.json`
- 两种执行方式:
  - **主会话** (`sessionTarget: "main"`) + `payload.kind: "systemEvent"` → 注入系统事件到主会话
  - **隔离式** (`sessionTarget: "isolated"`) + `payload.kind: "agentTurn"` → 独立会话运行
- 唤醒模式: `wakeMode: "now"` (立即) 或 `"next-heartbeat"` (默认)

## 调度类型
| 类型 | 字段 | 说明 |
|------|------|------|
| `at` | `schedule.at` (ISO 8601) | 一次性，成功后默认删除 |
| `every` | `schedule.everyMs` (毫秒) | 固定间隔 |
| `cron` | `schedule.expr` + `schedule.tz` | 5字段cron表达式 |

⚠️ ISO时间戳省略时区按UTC处理。cron省略tz用网关主机本地时区。

## 投递 (隔离任务)
```json5
delivery: {
  mode: "announce",           // announce|none|webhook
  channel: "telegram",        // 渠道名
  to: "-1001234567890",       // 目标(聊天ID/用户等)
  bestEffort: true            // 投递失败不影响任务状态
}
```
- 隔离任务默认 announce
- Telegram主题: `"-1001234567890:topic:123"`
- 省略channel/to时回退到主会话最后路由

## 工具调用 JSON

### 一次性提醒 (主会话)
```json
{
  "name": "Reminder",
  "schedule": { "kind": "at", "at": "2026-02-01T16:00:00Z" },
  "sessionTarget": "main",
  "wakeMode": "now",
  "payload": { "kind": "systemEvent", "text": "提醒内容" }
}
```

### 周期性隔离任务
```json
{
  "name": "每日摘要",
  "schedule": { "kind": "cron", "expr": "0 7 * * *", "tz": "Asia/Shanghai" },
  "sessionTarget": "isolated",
  "payload": { "kind": "agentTurn", "message": "总结今日更新", "model": "opus", "thinking": "high" },
  "delivery": { "mode": "announce", "channel": "telegram", "to": "123456789" }
}
```

### 更新任务
```json
{ "jobId": "xxx", "patch": { "enabled": false, "schedule": { "kind": "every", "everyMs": 3600000 } } }
```

## CLI 命令
```bash
# 列出/状态
openclaw cron list [--all] [--json]
openclaw cron status [--json]

# 添加
openclaw cron add --name "任务" --cron "0 9 * * *" --tz "Asia/Shanghai" \
  --session isolated --message "执行..." --announce --channel telegram --to "123"

# 一次性提醒
openclaw cron add --name "提醒" --at "20m" --session main \
  --system-event "提醒内容" --wake now --delete-after-run

# 带模型覆盖
openclaw cron add --name "深度分析" --cron "0 6 * * 1" \
  --session isolated --message "分析..." --model opus --thinking high

# 编辑/删除
openclaw cron edit <jobId> --message "新提示" --model opus
openclaw cron rm <jobId>
openclaw cron enable|disable <jobId>

# 手动运行/历史
openclaw cron run <jobId> [--force]
openclaw cron runs --id <jobId> [--limit 50]

# 直接发送系统事件(不创建任务)
openclaw system event --mode now --text "检查日历"
```

## 配置
```json5
cron: {
  enabled: true,
  store: "~/.openclaw/cron/jobs.json",
  maxConcurrentRuns: 1
}
```
禁用: `cron.enabled: false` 或 `OPENCLAW_SKIP_CRON=1`

## 存储
- 任务: `~/.openclaw/cron/jobs.json`
- 运行历史: `~/.openclaw/cron/runs/<jobId>.jsonl`
