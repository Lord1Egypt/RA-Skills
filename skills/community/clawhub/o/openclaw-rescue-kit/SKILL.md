---
name: openclaw-rescue-kit
description: OpenClaw 自救套件 - 网关启动包装（端口冲突防护）、看门狗监控、自动重启、配置回滚、安全加固、日志清理、Git版本管理。当用户提到 OpenClaw 网关崩溃、需要看门狗、配置回滚、安全扫描、日志清理、端口冲突、或部署自救脚本时使用此技能。包含 10 个独立脚本和完整部署指南。
---

# OpenClaw 自救套件

一套完整的 Shell 脚本，用于保障 OpenClaw AI 助手 7x24 小时稳定运行。

## 快速安装

### 从 clawhub 安装（推荐）

```bash
clawhub install openclaw-rescue-kit
bash ~/.openclaw/skills/openclaw-rescue-kit/scripts/install-rescue-kit.sh
```

### 从 .skill 文件安装

```bash
clawhub install ./openclaw-rescue-kit.skill
bash ~/.openclaw/skills/openclaw-rescue-kit/scripts/install-rescue-kit.sh
```

### 手动安装

```bash
mkdir -p ~/.openclaw/scripts ~/.openclaw/logs ~/.openclaw/backups
cp ~/.openclaw/skills/openclaw-rescue-kit/scripts/*.sh ~/.openclaw/scripts/
chmod +x ~/.openclaw/scripts/*.sh
bash ~/.openclaw/scripts/install-rescue-kit.sh
```

安装完成后：

```bash
# 1. 编辑告警配置（填入飞书/Telegram Webhook）
vim ~/.openclaw/notify.conf

# 2. 保存安全配置
bash ~/.openclaw/scripts/security-hardening.sh --save-safe

# 3. 保存 Git 安全版本
bash ~/.openclaw/scripts/git-tag.sh save-safe

# 4. 测试告警
bash ~/.openclaw/scripts/notify.sh -l INFO "自救套件部署完成"
```

## 脚本清单

| 脚本 | 功能 | 运行方式 |
|------|------|----------|
| `core.sh` | 核心诊断（网关状态、配置验证） | 被其他脚本调用 |
| `gateway-start.sh` | 网关启动包装（端口冲突防护 + 自动清理） | 被 LaunchAgent 调用 |
| `gateway-watchdog.sh` | 网关看门狗（配置验证+自动回滚+重启） | 定时任务 |
| `health-check.sh` | 健康检查（资源、消息活动） | 定时任务 |
| `git-tag.sh` | 配置快照与回滚（Git tag） | 手动/看门狗触发 |
| `security-hardening.sh` | 安全加固扫描 | 手动 |
| `notify.sh` | 告警通知（飞书/Telegram/企微/钉钉） | 被其他脚本调用 |
| `log-cleaner.sh` | 智能日志清理 | 定时任务 |

| `safe-config-modify.sh` | 安全配置修改（原子写入+自动回滚） | 手动/被其他脚本调用 |

### git-tag.sh 使用（配置回滚）

```bash
# 查看所有配置快照
bash ~/.openclaw/scripts/git-tag.sh list

# 快速回滚到上一个安全版本
bash ~/.openclaw/scripts/git-tag.sh quick-rollback

# 回滚到指定版本
bash ~/.openclaw/scripts/git-tag.sh rollback <tag-name>
```

## 定时任务配置

### macOS LaunchAgent（推荐）

macOS 上 crontab 受 SIP 限制，推荐使用 LaunchAgent。

安装脚本会自动生成 plist 到 `~/.openclaw/launchagents-ready/`（路径已正确替换）。

如果安装脚本因沙箱权限无法自动复制，请手动执行：

```bash
# 复制已准备好的 plist（路径已替换，无需手动修改）
cp ~/.openclaw/launchagents-ready/*.plist ~/Library/LaunchAgents/

# 加载所有服务
launchctl load ~/Library/LaunchAgents/ai.openclaw.watchdog.plist
launchctl load ~/Library/LaunchAgents/ai.openclaw.healthcheck.plist
launchctl load ~/Library/LaunchAgents/ai.openclaw.logcleaner.plist
launchctl load ~/Library/LaunchAgents/ai.openclaw.gittag.plist

# 验证
launchctl list | grep openclaw
```

**服务说明：**

| 服务 | 频率 | 功能 |
|------|------|------|
| `ai.openclaw.gateway` | 持续 (KeepAlive) | 网关进程守护（OpenClaw 自带） |
| `ai.openclaw.watchdog` | 每分钟 | 配置验证 + 自动回滚 + 重启 |
| `ai.openclaw.healthcheck` | 每小时 | 健康检查 + 告警 |
| `ai.openclaw.logcleaner` | 每天 | 日志清理 + Session 瘦身 |
| `ai.openclaw.gittag` | 每天 | Git 配置基线版本 |

**管理命令：**

```bash
# 停止服务
launchctl unload ~/Library/LaunchAgents/ai.openclaw.watchdog.plist

# 重启服务
launchctl unload ~/Library/LaunchAgents/ai.openclaw.watchdog.plist
launchctl load ~/Library/LaunchAgents/ai.openclaw.watchdog.plist

# 查看日志
tail -f ~/.openclaw/logs/watchdog.log
```

### Linux crontab

Linux 上可以使用 crontab：

```bash
crontab -e
```

添加以下内容：

```bash
# OpenClaw 自救套件定时任务
SHELL=/bin/bash
PATH=/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin

# 每分钟检查网关（看门狗）
* * * * * /bin/bash $HOME/.openclaw/scripts/gateway-watchdog.sh >> $HOME/.openclaw/logs/cron.log 2>&1

# 每小时健康检查
0 * * * * /bin/bash $HOME/.openclaw/scripts/health-check.sh >> $HOME/.openclaw/logs/cron.log 2>&1

# 每天凌晨3点日志清理
0 3 * * * /bin/bash $HOME/.openclaw/scripts/log-cleaner.sh >> $HOME/.openclaw/logs/cron.log 2>&1

# 每天凌晨2:30 Git 基线版本
30 2 * * * /bin/bash $HOME/.openclaw/scripts/git-tag.sh save-baseline >> $HOME/.openclaw/logs/cron.log 2>&1
```

## 安全配置修改

使用 `safe-config-modify.sh` 进行配置修改，自动处理通知、备份、验证、回滚：

```bash
# 安全修改配置
bash ~/.openclaw/scripts/safe-config-modify.sh modify "操作名" "描述" '修改命令'

# 查看当前操作状态
bash ~/.openclaw/scripts/safe-config-modify.sh state

# 重启后恢复检查（watchdog 自动调用）
bash ~/.openclaw/scripts/safe-config-modify.sh recovery
```

**安全流程：**
1. 先发送通知给用户
2. Git 快照备份
3. 记录操作状态（用于重启后恢复）
4. 原子写入配置（先写临时文件，验证 JSON 后替换）
5. 验证配置合法性
6. 重启网关
7. 验证网关运行
8. 失败则自动回滚

## 配置修改公约（必须遵守）

修改 `openclaw.json` 前必须按以下流程操作：

```
1. 备份    → bash ~/.openclaw/scripts/git-tag.sh save-working
2. 检查    → bash ~/.openclaw/scripts/core.sh（确认网关正常）
3. 修改    → 编辑配置文件
4. 验证    → openclaw gateway status
5. 成功    → bash ~/.openclaw/scripts/git-tag.sh save-safe
6. 失败    → bash ~/.openclaw/scripts/git-tag.sh quick-rollback
```

## 获取飞书 Webhook

1. 在飞书群聊中，点击右上角「设置」→「群机器人」→「添加机器人」→「自定义机器人」
2. 输入机器人名称（如：OpenClaw 告警）
3. 复制生成的 Webhook URL
4. 填入 `~/.openclaw/notify.conf`

## 告警通知配置

编辑 `~/.openclaw/notify.conf`，填入至少一个 Webhook：

```bash
# 飞书机器人 Webhook
FEISHU_WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_HOOK_ID"

# Telegram（可选）
# TELEGRAM_BOT_TOKEN="your_bot_token"
# TELEGRAM_CHAT_ID="your_chat_id"

# 企业微信（可选）
# WECHAT_WEBHOOK_URL="your_webhook_url"

# 钉钉（可选）
# DINGTALK_WEBHOOK_URL="your_webhook_url"
```

## 关键经验

- **端口冲突导致重启失败** → gateway-start.sh 启动前自动清理端口占用和锁文件
- **网关挂了 AI 诊断不了自己** → 使用独立脚本 + 端口检测
- **Webhook 通知不依赖网关** → 网关挂了也能发告警
- **macOS 上 LaunchAgent 比 crontab 更可靠**
- **KeepAlive 只管重启，不管配置验证** → 看门狗脚本仍有价值
- **必须有锁文件机制** → 防止看门狗重复执行
- **必须有重启冷却期** → 避免频繁重启（默认 60 秒）
- **必须有重启次数限制** → 防止无限循环（默认 3 次）

## 故障排查

```bash
# 网关反复重启
tail -f ~/.openclaw/logs/watchdog.log
bash ~/.openclaw/scripts/core.sh
bash ~/.openclaw/scripts/git-tag.sh list

# 告警不生效
bash ~/.openclaw/scripts/notify.sh "测试消息"
cat ~/.openclaw/logs/unsent_alerts.log

# 配置回滚失败
ls -la ~/.openclaw/backups/
bash ~/.openclaw/scripts/git-tag.sh list
```

## 详细文档

完整使用说明和踩坑记录见 [references/guide.md](references/guide.md)
