# OpenClaw 自救套件 - 完整指南

## 脚本详细说明

### 1. gateway-start.sh - 网关启动包装

启动前自动清理端口占用、锁文件和过期 PID 文件，防止 LaunchAgent 重启失败。

```bash
# 直接测试（会实际启动网关）
bash ~/.openclaw/scripts/gateway-start.sh

# 传递自定义参数
bash ~/.openclaw/scripts/gateway-start.sh openclaw gateway start --port 18789
```

工作流程：
1. 执行 `openclaw gateway stop` 优雅关闭（2 秒等待）
2. 检测端口占用（支持 lsof/netstat/ss 三种方式）
3. 先发 SIGTERM 等待优雅退出（3 秒）
4. 未退出的发 SIGKILL 强制清理
5. 清理过期锁文件
6. 清理过期 PID 文件
7. 启动网关（exec 替换当前进程）

环境变量：
- `OPENCLAW_GATEWAY_PORT` — 网关端口（默认 18789）
- `OPENCLAW_HOME` — OpenClaw 主目录（默认 ~/.openclaw）

LaunchAgent 配置（安装脚本自动配置）：
```xml
<key>ProgramArguments</key>
<array>
    <string>/bin/bash</string>
    <string>-c</string>
    <string>sleep 5; exec bash ~/.openclaw/scripts/gateway-start.sh</string>
</array>
```

### 2. core.sh - 核心诊断

检查网关进程和端口状态、验证配置文件、检测僵尸状态、检测重复服务冲突。

```bash
bash ~/.openclaw/scripts/core.sh
```

诊断逻辑：
- 网关状态 = `openclaw gateway status` OR 端口监听（任一通过即正常）
- 僵尸检测 = 检查最新 session 文件修改时间（默认阈值 6 小时）
- 配置验证 = `openclaw` 命令验证 OR jq JSON 格式验证

### 3. gateway-watchdog.sh - 网关看门狗

自动检测网关状态，异常时自动重启。支持单次运行和守护进程模式。

```bash
# 单次检查
bash ~/.openclaw/scripts/gateway-watchdog.sh

# 守护进程模式
bash ~/.openclaw/scripts/gateway-watchdog.sh --daemon
```

配置项：
- `MAX_RETRIES=3` — 最大重启次数
- `RETRY_COOLDOWN=60` — 重启冷却期（秒）
- `CHECK_INTERVAL=60` — 守护模式检查间隔（秒）

工作流程：
1. 检查网关状态
2. 正常 → 退出
3. 异常 → 清理端口占用（防止端口冲突）
4. 验证配置
5. 配置错误 → 尝试自动修复
6. 修复失败 → 触发配置回滚
7. 修复成功 → 重启网关（启动前再次清理端口）
8. 重启失败 → 计数+1，发送告警
9. 达到上限 → 发送紧急告警，停止尝试

### 4. health-check.sh - 健康检查

Gateway HTTP 健康检查、Provider 进程存活、消息活动检测、资源配置检查。

```bash
bash ~/.openclaw/scripts/health-check.sh
```

检查项：
- Gateway /health 端点响应
- Provider 进程存活（超过 6 小时无重启则警告）
- 消息活动（超过 6 小时无消息则告警）
- 配置有效性
- 磁盘使用率（阈值 90%）
- 内存使用率（阈值 85%）

### 5. git-tag.sh - 配置快照与回滚

使用 Git tag 管理配置版本，比文件拷贝更可靠。

```bash
# 查看所有快照
bash ~/.openclaw/scripts/git-tag.sh list

# 快速回滚到上一个安全版本
bash ~/.openclaw/scripts/git-tag.sh quick-rollback

# 回滚到指定标签
bash ~/.openclaw/scripts/git-tag.sh rollback <tag-name>
```

### 6. security-hardening.sh - 安全加固

检查公网暴露、访问令牌、重复服务、防火墙状态。

```bash
# 运行安全扫描
bash ~/.openclaw/scripts/security-hardening.sh

# 保存当前配置为安全配置
bash ~/.openclaw/scripts/security-hardening.sh --save-safe
```

检查项：
- 公网暴露（端口监听地址）
- 访问令牌配置
- 重复服务冲突
- 防火墙状态

### 7. notify.sh - 告警通知

支持飞书、Telegram、企业微信、钉钉 4 种通知渠道。

```bash
# 发送 INFO 级别告警
bash ~/.openclaw/scripts/notify.sh "测试消息"

# 发送 ERROR 级别告警
bash ~/.openclaw/scripts/notify.sh -l ERROR "网关崩溃了！"

# 从管道读取
echo "磁盘空间不足" | bash ~/.openclaw/scripts/notify.sh -l WARNING
```

### 8. log-cleaner.sh - 智能日志清理

清理过期日志、Session 文件瘦身、每日 memory 归档。

```bash
bash ~/.openclaw/scripts/log-cleaner.sh
bash ~/.openclaw/scripts/log-cleaner.sh --dry-run  # 试运行
bash ~/.openclaw/scripts/log-cleaner.sh --keep-days 14
```

Session 清理策略：
- < 1MB：不处理
- 1-2MB：保留最近 200 条
- 2-5MB：保留 100 条，移除详细工具输出
- 5-10MB：保留 50 条，精简
- > 10MB：保留 30 条，激进精简

### 9. git-tag.sh - Git 配置版本管理

使用 Git 标记管理配置版本，支持回滚和 Diff。

```bash
bash ~/.openclaw/scripts/git-tag.sh save-safe      # 保存安全版本
bash ~/.openclaw/scripts/git-tag.sh save-working   # 保存工作版本
bash ~/.openclaw/scripts/git-tag.sh save-baseline  # 保存基线版本
bash ~/.openclaw/scripts/git-tag.sh list           # 列出所有标记
bash ~/.openclaw/scripts/git-tag.sh quick-rollback # 快速回滚
bash ~/.openclaw/scripts/git-tag.sh diff <tag>     # 查看差异
```

标记类型：
- `config-safe-*` — 确认稳定的配置
- `config-working-*` — 当前可用的配置
- `config-baseline-*` — 每日基线快照

## 定时任务说明

### macOS LaunchAgent vs KeepAlive

macOS 上的 OpenClaw 网关通常已配置 `KeepAlive=true`，launchd 会自动重启崩溃的进程。但 KeepAlive 只管"挂了重启"，**不管配置验证**。

看门狗脚本的价值：
1. 检测配置是否有效
2. 配置坏了先尝试修复
3. 修复失败触发回滚
4. 回滚后再启动

这个逻辑 KeepAlive 做不到，所以看门狗仍然需要。

### macOS LaunchAgent 管理

```bash
# 查看所有 OpenClaw 服务
launchctl list | grep openclaw

# 停止服务
launchctl unload ~/Library/LaunchAgents/ai.openclaw.watchdog.plist

# 重启服务
launchctl unload ~/Library/LaunchAgents/ai.openclaw.watchdog.plist
launchctl load ~/Library/LaunchAgents/ai.openclaw.watchdog.plist

# 查看日志
tail -f ~/.openclaw/logs/watchdog.log
tail -f ~/.openclaw/logs/health-check.log
```

### Linux crontab 管理

```bash
# 查看定时任务
crontab -l

# 编辑定时任务
crontab -e

# 查看执行日志
tail -f ~/.openclaw/logs/cron.log
```

## 实战经验

### 端口冲突导致 LaunchAgent 重启失败

**问题现象：**
```
Gateway failed to start: gateway already running (pid 8239); lock timeout after 5000ms
Port 18789 is already in use.
```

**根本原因：**
旧网关进程占着端口，LaunchAgent 的 KeepAlive 机制会尝试启动新进程，但新进程无法绑定已被占用的端口，导致无限重试失败。

**解决方案：**
gateway-start.sh 在启动前自动清理端口占用：
```bash
# 发送 SIGTERM，等待 3 秒优雅退出
kill $pid
sleep 3

# 未退出的发 SIGKILL
kill -9 $pid
sleep 1

# 确认端口已释放
lsof -ti:18789 || echo "端口已清理"
```

**watchdog 双重保障：**
gateway-watchdog.sh 重启时也会先调用 cleanup_gateway_port()，确保无残留进程。

### 网关挂了，AI 诊断不了自己

OpenClaw 的诊断功能依赖网关运行。使用独立脚本 + 端口检测：

```bash
# 端口检测比进程检测更可靠
lsof -i :18789 -sTCP:LISTEN  # 端口在监听 = 网关大概率正常
pgrep -f "openclaw.*gateway"  # 进程检测可能因权限失败
```

### Webhook 通知不依赖网关

飞书/Telegram 的 Webhook 通过 curl 直接发送，不经过 OpenClaw 网关。即使网关完全挂掉，告警通知依然能送达。

### macOS 上 LaunchAgent 比 crontab 更可靠

- crontab 在 macOS 上权限受限（SIP 保护）
- crontab 环境变量不完整（PATH 缺失）
- LaunchAgent 是 macOS 原生机制，更稳定

### 锁文件机制防止重复执行

```bash
LOCK_FILE="$LOG_DIR/watchdog.lock"
if [ -f "$LOCK_FILE" ]; then
    lock_pid=$(cat "$LOCK_FILE")
    if kill -0 "$lock_pid" 2>/dev/null; then
        exit 0  # 另一个实例正在运行
    fi
fi
echo $$ > "$LOCK_FILE"
trap "rm -f $LOCK_FILE" EXIT
```

### 重启冷却期防止频繁重启

```bash
RETRY_COOLDOWN=60  # 60秒冷却期
if [ $time_since_last_restart -lt $RETRY_COOLDOWN ]; then
    exit 0  # 冷却期内，跳过重启
fi
```

### 重启次数限制防止无限循环

```bash
MAX_RETRIES=3  # 最多重试3次
if [ $restart_count -ge $MAX_RETRIES ]; then
    send_alert "ERROR" "网关连续重启失败，需要人工干预！"
    exit 1
fi
```

## 环境变量

```bash
export OPENCLAW_HOME="$HOME/.openclaw"        # OpenClaw 主目录
export OPENCLAW_LOG_DIR="$OPENCLAW_HOME/logs" # 日志目录
export OPENCLAW_GATEWAY_PORT=18789            # 网关端口
export CLEANER_KEEP_DAYS=14                   # 日志保留天数
```

## 日志文件

- `~/.openclaw/logs/core.log` — 核心诊断日志
- `~/.openclaw/logs/watchdog.log` — 看门狗运行日志
- `~/.openclaw/logs/health-check.log` — 健康检查日志
- `~/.openclaw/logs/security-hardening.log` — 安全加固日志
- `~/.openclaw/logs/cleaner.log` — 日志清理日志
- `~/.openclaw/logs/alerts.log` — 告警记录
- `~/.openclaw/logs/unsent_alerts.log` — 未发送的告警
- `~/.openclaw/logs/cron.log` — crontab 执行日志（Linux）
