# OpenClaw 自救套件

一套完整的 Shell 脚本，用于保障 OpenClaw AI 助手 7x24 小时稳定运行。

## 功能

- 🔌 网关启动包装（端口冲突防护 + 自动清理）
- 🛡️ 网关看门狗（配置验证 + 自动回滚 + 重启）
- 🏥 健康检查（资源、消息活动）
- 🔄 配置回滚（多级备份）
- 🔒 安全加固扫描
- 📢 告警通知（飞书/Telegram/企微/钉钉）
- 🧹 智能日志清理
- 📦 Git 配置版本管理

## 安装

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

## 安装后配置

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

## 获取飞书 Webhook

1. 在飞书群聊中，点击右上角「设置」→「群机器人」→「添加机器人」→「自定义机器人」
2. 输入机器人名称（如：OpenClaw 告警）
3. 复制生成的 Webhook URL
4. 填入 `~/.openclaw/notify.conf`：
   ```bash
   FEISHU_WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_WEBHOOK_ID"
   ```

## 定时任务

### macOS LaunchAgent

```bash
# plist 已生成到 ~/.openclaw/launchagents-ready/
cp ~/.openclaw/launchagents-ready/*.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/ai.openclaw.*.plist
```

### Linux crontab

```bash
# 每分钟看门狗
* * * * * /bin/bash $HOME/.openclaw/scripts/gateway-watchdog.sh >> $HOME/.openclaw/logs/cron.log 2>&1

# 每小时健康检查
0 * * * * /bin/bash $HOME/.openclaw/scripts/health-check.sh >> $HOME/.openclaw/logs/cron.log 2>&1

# 每天凌晨3点日志清理
0 3 * * * /bin/bash $HOME/.openclaw/scripts/log-cleaner.sh >> $HOME/.openclaw/logs/cron.log 2>&1

# 每天凌晨2:30 Git 基线版本
30 2 * * * /bin/bash $HOME/.openclaw/scripts/git-tag.sh save-baseline >> $HOME/.openclaw/logs/cron.log 2>&1
```

## 脚本清单

| 脚本 | 功能 | 运行方式 |
|------|------|----------|
| `core.sh` | 核心诊断（网关状态、配置验证） | 被其他脚本调用 |
| `gateway-start.sh` | 网关启动包装（端口冲突防护） | 被 LaunchAgent 调用 |
| `gateway-watchdog.sh` | 网关看门狗（配置验证+自动回滚+重启） | 定时任务 |
| `health-check.sh` | 健康检查（资源、消息活动） | 定时任务 |
| `security-hardening.sh` | 安全加固扫描 | 手动 |
| `notify.sh` | 告警通知（飞书/Telegram/企微/钉钉） | 被其他脚本调用 |
| `log-cleaner.sh` | 智能日志清理 | 定时任务 |
| `git-tag.sh` | Git 配置版本管理 | 手动/定时任务 |
| `safe-config-modify.sh` | 安全配置修改（原子写入+自动回滚） | 手动/被其他脚本调用 |

## 配置修改公约

修改 `openclaw.json` 前必须按以下流程操作：

```bash
1. 备份    → bash ~/.openclaw/scripts/git-tag.sh save-working
2. 检查    → bash ~/.openclaw/scripts/core.sh
3. 修改    → 编辑配置文件
4. 验证    → openclaw gateway status
5. 成功    → bash ~/.openclaw/scripts/git-tag.sh save-safe
6. 失败    → bash ~/.openclaw/scripts/git-tag.sh quick-rollback
```

## 关键经验

- **端口冲突导致重启失败** → gateway-start.sh 启动前自动清理端口
- 网关挂了 AI 诊断不了自己 → 使用独立脚本 + 端口检测
- Webhook 通知不依赖网关 → 网关挂了也能发告警
- macOS 上 LaunchAgent 比 crontab 更可靠
- KeepAlive 只管重启，不管配置验证 → 看门狗脚本仍有价值
- 必须有锁文件机制 → 防止看门狗重复执行
- 必须有重启冷却期 → 避免频繁重启（默认 60 秒）
- 必须有重启次数限制 → 防止无限循环（默认 3 次）

## 故障排查

```bash
# 网关反复重启
tail -f ~/.openclaw/logs/watchdog.log
bash ~/.openclaw/scripts/core.sh

# 告警不生效
bash ~/.openclaw/scripts/notify.sh "测试消息"
cat ~/.openclaw/logs/unsent_alerts.log

# 配置回滚失败
ls -la ~/.openclaw/backups/
bash ~/.openclaw/scripts/git-tag.sh list
```

## 许可证

MIT
