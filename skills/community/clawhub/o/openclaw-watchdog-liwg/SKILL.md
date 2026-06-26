---
name: openclaw-watchdog
description: OpenClaw Gateway 看门狗技能。监控 OpenClaw Gateway 进程存活、WebSocket 错误、飞书/企业微信/微信通道状态、网络连通性。在检测到异常时自动重启 Gateway（最多2次，10分钟窗口），并记录通道暂停状态。当 OpenClaw Gateway 无响应、通道报错、session 过期、或网络异常时触发。
---

# OpenClaw Watchdog

监控 OpenClaw Gateway 运行状态，支持多通道检测和自动恢复。

## 核心功能

- **进程检测**：使用 systemd + 端口 + 进程名三重检测，避免误报
- **通道监控**：飞书、企业微信、微信通道的 session 过期和错误检测
- **网络检测**：百度/阿里 DNS 连通性检测
- **自动重启**：最多 2 次重启，10 分钟冷却窗口
- **代理管理**：网络异常时自动禁用系统代理

## 使用方式

### 手动运行

```bash
bash /path/to/openclaw-watchdog/scripts/watchdog.sh [interval]
# interval: 检测间隔（秒），默认 300（5分钟）
```

### Systemd 服务部署

```ini
[Unit]
Description=OpenClaw Watchdog
After=network-online.target

[Service]
ExecStart=/bin/bash /path/to/openclaw-watchdog/scripts/watchdog.sh 300
Restart=always
RestartSec=10

[Install]
WantedBy=default.target
```

部署命令：
```bash
systemctl --user enable openclaw-watchdog.service
systemctl --user start openclaw-watchdog.service
```

## 配置参数（环境变量）

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `LOG_FILE` | `/tmp/openclaw_watchdog.log` | 日志文件路径 |
| `PID_FILE` | `/tmp/openclaw_gateway.pid` | Gateway PID 文件 |
| `MAX_RESTARTS` | `2` | 最大重启次数 |
| `RESTART_WINDOW` | `600` | 重启窗口（秒） |
| `OPENCLAW_PORT` | `18789` | Gateway 端口 |

## 日志文件

- 主日志：`/tmp/openclaw_watchdog.log`
- Gateway 日志：`/tmp/openclaw_gateway.log`
- 通道暂停状态文件：
  - `/tmp/openclaw_feishu_paused`
  - `/tmp/openclaw_wecom_paused`
  - `/tmp/openclaw_weixin_paused`
  - `/tmp/openclaw_proxy_disabled`

## 通道错误识别

| 通道 | 错误关键词 | 说明 |
|------|-----------|------|
| 飞书 | `feishu.*error`, `lark.*error`, `session.*expired` | session 过期需等待 |
| 企业微信 | `wecom.*error`, `wechat.*work.*error` | 服务端错误 |
| 微信 | `errcode.*-14`, `session.*expired` | 暂停 60 分钟自动恢复 |

## 注意事项

- 微信 errcode -14 是微信官方限制，看门狗只能记录状态，无法提前解除
- 飞书/企业微信 token 过期需手动刷新授权
- 频繁重启可能导致通道被微信封禁，发现后会自动停止重启
