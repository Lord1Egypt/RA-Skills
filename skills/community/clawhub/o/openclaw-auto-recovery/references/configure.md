# 配置参考

## 配置文件路径

默认：`~/.config/infra-heartbeat/config.env`

可通过 `heartbeat-daemon.sh --config /path/to/config.env` 覆盖。

## 必填参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `FEISHU_APP_ID` | 飞书应用 App ID | `cli_xxxxxxxxxxxxxxxxxxxxxxxxxxxx` |
| `FEISHU_APP_SECRET` | 飞书应用 App Secret | `Uu4RlQz...` |
| `GATEWAY_TOKEN` | OpenClaw Gateway 访问令牌 | 在 openclaw.json 中查找 |
| `TARGET_OPEN_ID` | 飞书通知目标的 open_id | `ou_xxx` |

## 可选参数（带默认值）

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `GATEWAY_PORT` | `18789` | Gateway WebSocket 端口 |
| `OPENCLAW_JSON` | `~/.openclaw/openclaw.json` | openclaw 配置文件路径 |
| `CHECK_INTERVAL` | `180`（秒） | 心跳检测间隔 |
| `MAX_RESTART_FAILS` | `3` | 连续失败次数阈值（达到后停止自动重启） |
| `DISK_THRESHOLD` | `80`（%） | 磁盘使用率告警阈值 |
| `MEM_THRESHOLD` | `85`（%） | 内存使用率告警阈值 |
| `CPU_THRESHOLD` | `60`（%） | CPU 使用率告警阈值 |
| `WS_MODULE` | 自动检测 | WebSocket 模块路径，通常不需要改 |

## 获取配置值

### Gateway Token

```bash
cat ~/.openclaw/openclaw.json | jq -r '.gateway.auth.secret'
```

### 飞书 App ID / Secret

在飞书开放平台 → 应用凭证 中查看。

### Target Open ID

飞书用户的 open_id，可通过以下方式获取：
- 飞书开发者工具
- 搜索用户 API

## 日志文件

| 文件 | 路径 |
|------|------|
| 主日志 | `~/.openclaw/workspace-infra/heartbeat.log` |
| 告警日志 | `~/.openclaw/workspace-infra/alerts.log` |
| 失败计数 | `~/.openclaw/workspace-infra/restart-fail-count` |
| 自动备份 | `~/.openclaw/openclaw.json.auto.*` |

## 阈值设计建议

| 环境 | CPU | 内存 | 磁盘 |
|------|-----|------|------|
| 个人工作站 | 60-70% | 80-85% | 80% |
| VPS/服务器 | 70-80% | 85-90% | 85% |
| 高可用环境 | 50% | 75% | 70% |

## 与 cron 任务的区别

| | Heartbeat Daemon | Cron 健康检查 |
|---|---|---|
| 实时性 | 3 分钟间隔 | 通常每天一次 |
| 自动恢复 | ✅ 自动重启 Gateway | ❌ 仅告警 |
| 进程保活 | ✅ systemd 托管 | ❌ 依赖 cron |
| 适用场景 | 生产环境需要自动恢复 | 日常巡检/统计 |
