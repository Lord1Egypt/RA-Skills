# OpenClaw 维护脚本合集

用于保障 OpenClaw 稳定运行的本地维护脚本（监控、重启、日志清理、网络代理健康检查）。

## 功能特性

- **Gateway 看护** - 自动检测 Gateway 健康状态，异常时重启
- **代理健康监控** - 监控消息队列积压，自动切换 VPN/代理节点
- **安全重启** - 优雅重启 Gateway，避免误判
- **日志清理** - 自动清理过期日志，防止磁盘占用
- **跨平台支持** - macOS (LaunchAgent) / Linux (systemd/cron) / NAS

## 脚本清单

| 脚本 | 作用 | 运行方式 |
|------|------|----------|
| `gateway-watchdog.sh` | Gateway 健康监控 | 每分钟/常驻 |
| `proxy-health.sh` | 代理网络监控 | 每分钟 |
| `openclaw-safe-restart.sh` | 安全重启 | 手动 |
| `cleanup-logs.sh` | 日志清理 | 每天 |
| `log-cleanup-launchd.sh` | macOS 定时清理 | LaunchAgent |

## 安装步骤

```bash
# 1. 复制环境变量示例
cp .env.example .env

# 2. 配置环境变量（至少设置 OPENCLAW_NOTIFY_TARGET）
vim .env

# 3. 运行安装脚本
bash install.sh

# 4. 运行自检
bash check.sh
```

## 配置说明

### 环境变量

```bash
# 通知目标（Telegram 用户 ID）
OPENCLAW_NOTIFY_TARGET=123456789

# Clash API（可选，用于代理切换）
CLASH_API=http://127.0.0.1:9090
CLASH_SECRET=your-secret

# 积压阈值（消息数）
QUEUE_THRESHOLD=100
```

### 系统要求

- `openclaw` CLI
- `curl`
- `jq`
- (可选) Clash / Mihomo

## 部署方式

### macOS (推荐)
使用 LaunchAgent 定时/常驻运行：
```bash
launchctl load ~/Library/LaunchAgents/ai.openclaw.watchdog.plist
```

### Linux
使用 systemd 或 cron：
```bash
sudo systemctl enable --now openclaw-watchdog
```

### NAS
使用任务计划程序定时执行。

## 使用场景

- 保障 Gateway 24/7 稳定运行
- 自动处理网络波动导致的消息积压
- 定期清理日志防止磁盘占用
- 多设备统一运维部署

## 注意事项

- 首次部署需配置通知目标
- Clash API 为可选配置
- 多设备需分别设置通知 ID
- 建议配合监控告警使用

## 版本

0.1.0 - 初始发布
