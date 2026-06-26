---
name: openclaw-watchdog
description: OpenClaw 跨平台配置备份与网关监控。自动备份 openclaw.json，每分钟检查 gateway 状态，宕机时自动恢复。支持 Linux/macOS/Windows。触发：配置备份、gateway 监控、自动恢复、看门狗、watchdog。
---

# OpenClaw Watchdog

跨平台配置自动备份与网关健康监控。

> **⚠️ 首次使用请运行安装脚本：**
> ```bash
> node /usr/lib/node_modules/openclaw/skills/openclaw-watchdog/scripts/install.js
> ```
> 安装后将自动配置持久化运行并启动服务。

## 安装

### 从 ClawHub 安装

```bash
clawhub install openclaw-watchdog-pro
```

### 手动安装（本地）

```bash
# 运行安装脚本（推荐）
node /usr/lib/node_modules/openclaw/skills/openclaw-watchdog/scripts/install.cjs

# 安装后自动：
# - 检测系统类型（systemd/launchd/cron/Windows）
# - 配置持久化运行
# - 添加 oc 快捷命令
# - 启动看门狗服务
```

### 手动启动

```bash
# 启动看门狗（后台运行）
node /usr/lib/node_modules/openclaw/skills/openclaw-watchdog/scripts/watchdog.cjs monitor &

# 或使用包装命令（自动备份）
oc config edit
oc gateway restart
```

## 核心功能

### 1. 自动备份

使用 `oc` 命令（包装脚本），修改配置前自动备份：

```bash
# Linux/macOS - 添加到 ~/.bashrc
alias oc='node /usr/lib/node_modules/openclaw/skills/openclaw-watchdog/scripts/watchdog.cjs wrap'

# Windows (PowerShell) - 添加到 $PROFILE
function oc { node C:\path\to\watchdog.cjs wrap $args }
```

备份位置：`~/.openclaw/backups/`
保留策略：最近 5 个备份（可配置）

### 2. 网关监控

- **WebSocket 探针**检测 gateway 状态（直接连接 ws://127.0.0.1:18789）
- 每分钟检查一次，连续两次无响应时触发恢复
- 自动恢复最新备份并验证 gateway 启动
- **连续 3 次恢复失败后自动调用 `openclaw doctor --fix` 进行深度修复**

### 3. 错误模式检测

从 gateway 日志中检测异常错误模式：

| 类别 | 模式 |
|------|------|
| 限流 | HTTP 429, rate.limit, too many requests |
| 服务端错误 | HTTP 5xx |
| 认证/权限 | HTTP 401/403, unauthorized, forbidden, token expired |
| 网络错误 | ETIMEDOUT, ECONNREFUSED, ECONNRESET, ENOTFOUND |
| 消息投递失败 | sendMessage failed, deliver failed, fetch failed |
| 自定义 | 可配置正则模式 |

**智能分析：**
- 错误率 (errors/min)
- 突增检测 (3x vs 上次检查)
- 错误集中度 (单一类型 ≥80%)

### 4. 命令参考

```bash
# 启动监控（前台）
node .../watchdog.cjs monitor

# 手动备份
node .../watchdog.cjs backup

# 检查 gateway 状态
node .../watchdog.cjs check

# 检查错误模式
node .../watchdog.cjs check-errors

# 检查状态
node .../watchdog.cjs check

# 恢复并重启
node .../watchdog.cjs recover

# 查看运行状态
node .../watchdog.cjs status

# 配置管理
node .../watchdog.cjs config edit    # 查看当前配置
node .../watchdog.cjs config reset   # 重置为默认
```

## 配置

编辑 `~/.openclaw/watchdog.config.json`：

```json
{
  "checkIntervalMs": 60000,      // 检查间隔（毫秒）
  "retryDelayMs": 5000,          // 重试延迟（毫秒）
  "maxBackups": 5,               // 最大备份数
  "gatewayStartTimeoutMs": 30000, // gateway 启动超时（毫秒）
  "logLevel": "info",            // 日志级别：debug, info, warn, error
  
  "errorThreshold": 30,          // 错误数阈值，超过则告警
  "errorWindowMs": 1800000,      // 监控窗口（毫秒，30分钟）
  "spikeRatio": 3,               // 突增倍数
  "errorLogPath": null,          // 日志路径（自动检测）
  "extraPatterns": ""            // 自定义正则模式
}
```

## 持久化运行

**推荐：** 运行安装脚本自动配置

```bash
node /usr/lib/node_modules/openclaw/skills/openclaw-watchdog/scripts/install.js
```

### 手动配置

#### Linux (systemd)

```bash
systemctl status openclaw-watchdog
systemctl restart openclaw-watchdog   # 重启服务
journalctl -u openclaw-watchdog -f    # 查看日志
```

#### macOS (launchd)

```bash
launchctl list | grep openclaw
launchctl unload ~/Library/LaunchAgents/com.openclaw.watchdog.plist
launchctl load ~/Library/LaunchAgents/com.openclaw.watchdog.plist
```

#### Windows

```powershell
# 查看任务
schtasks /query /tn "OpenClaw Watchdog"

# 删除并重新创建
schtasks /delete /tn "OpenClaw Watchdog" /f
```

#### cron (备用方案)

```bash
# 每分钟检查
* * * * * node .../watchdog.cjs check || node .../watchdog.cjs recover
```

## 文件结构

```
~/.openclaw/
├── watchdog.cjs              # 主脚本
├── watchdog.config.json      # 用户配置
├── watchdog.state.json       # 运行状态
├── watchdog.pid              # 进程 ID
├── watchdog.log              # 日志文件
└── backups/
    ├── openclaw.2026-03-24T08-00-00.json
    └── ...
```

## 故障排查

```bash
# 查看服务状态
systemctl status openclaw-watchdog

# 查看日志
tail -f ~/.openclaw/watchdog.log

# 查看运行状态
node .../watchdog.cjs status

# 手动测试
node .../watchdog.cjs check

# 重启服务
systemctl restart openclaw-watchdog

# 调试模式
node .../watchdog.cjs config reset
LOG_LEVEL=debug node .../watchdog.cjs monitor
```

## API 参考

### 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `OPENCLAW_CONFIG_DIR` | 配置目录 | `~/.openclaw` |

### 退出码

| 码 | 说明 |
|----|------|
| 0 | 成功 |
| 1 | 失败（gateway 无响应/命令执行失败） |

## 更新日志

- **v2.2** - 新增错误模式检测：从 gateway 日志分析 429/限流、5xx、认证/权限、网络错误、投递失败等，智能分析错误率、突增、集中度
- **v2.1** - WebSocket 探针检测 gateway（替代 CLI 调用），连续恢复失败自动调用 doctor --fix 修复，增强状态监控
- **v2.0** - 重构为 Node.js，跨平台支持，添加状态跟踪、配置管理、优雅关闭
- **v1.0** - 初始 Bash 版本
