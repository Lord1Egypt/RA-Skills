# 🛡️ OpenClaw Gateway Guardian - 网关守护神

**自动监控、保护和重启 OpenClaw 网关服务**
**防止网关意外停止、崩溃或消失**

## 🎯 核心功能

| 功能 | 说明 |
|------|------|
| **🔍 实时监控** | 每 30 秒检查网关状态（端口 + 进程） |
| **🔄 自动重启** | 网关异常时自动重启，最多 10 次 |
| **📱 多渠道通知** | 飞书/Telegram/企业微信告警 |
| **📊 健康日志** | 记录所有健康检查数据 |
| **🛡️ 进程保护** | 防止多实例运行 |
| **⚙️ 灵活配置** | 可自定义检查间隔、重启策略 |

## 📋 工作原理

```
┌─────────────────────────────────────────────────────────┐
│                   Gateway Guardian                       │
│                                                          │
│  ┌────────────┐    ┌────────────┐    ┌────────────┐    │
│  │  健康检查  │───>│  异常检测  │───>│  自动重启  │    │
│  │  (30 秒)    │    │  (端口 + 进程) │    │  (最多 10 次) │    │
│  └────────────┘    └────────────┘    └────────────┘    │
│         │                  │                  │          │
│         ▼                  ▼                  ▼          │
│  ┌────────────┐    ┌────────────┐    ┌────────────┐    │
│  │  健康日志  │    │  告警通知  │    │  重启统计  │    │
│  │  (JSON)    │    │ (飞书/ TG)  │    │  (计数重置) │    │
│  └────────────┘    └────────────┘    └────────────┘    │
└─────────────────────────────────────────────────────────┘
                    │
                    ▼
           ┌──────────────┐
           │ OpenClaw     │
           │ Gateway      │
           │ (被保护对象)  │
           └──────────────┘
```

## 🚀 快速开始

### 1. 安装依赖

```bash
cd openclaw-gateway-guardian
pip install -r requirements.txt
```

### 2. 初始化配置

```bash
python scripts/gateway_guardian.py init
```

按照向导输入：
- 网关端口（默认 18789）
- 检查间隔（默认 30 秒）
- 最大重启次数（默认 10 次）
- 通知渠道配置

### 3. 启动守护进程

```bash
python scripts/gateway_guardian.py start
```

### 4. 查看状态

```bash
python scripts/gateway_guardian.py status
```

## 📱 通知渠道配置

### 飞书配置（推荐）

1. 在飞书开放平台创建机器人
2. 获取 `bot_token` 和 `user_id`
3. 配置到初始化向导

### Telegram 配置

1. 在 BotFather 创建机器人
2. 获取 `bot_token` 和 `chat_id`
3. 配置到初始化向导

### 企业微信配置

1. 在企业微信管理后台创建机器人
2. 获取 `webhook` 地址
3. 配置到初始化向导

## 🔧 配置文件

配置文件位于 `~/.openclaw_guardian/config.json`

```json
{
  "gateway": {
    "port": 18789,
    "check_interval_seconds": 30,
    "max_restart_attempts": 10,
    "restart_delay_seconds": 5,
    "health_check_url": "ws://127.0.0.1:18789"
  },
  "notifications": {
    "enabled": true,
    "feishu_bot_token": "",
    "feishu_user_id": "",
    "telegram_bot_token": "",
    "telegram_chat_id": "",
    "wechat_webhook": ""
  },
  "logging": {
    "level": "INFO",
    "max_log_size_mb": 10,
    "backup_count": 5
  },
  "auto_start": {
    "enabled": true,
    "delay_seconds": 10
  }
}
```

## 📊 命令行用法

```bash
# 初始化配置
python scripts/gateway_guardian.py init

# 启动守护进程
python scripts/gateway_guardian.py start

# 停止守护进程
python scripts/gateway_guardian.py stop

# 查看运行状态
python scripts/gateway_guardian.py status

# 查看日志（最后 50 行）
python scripts/gateway_guardian.py logs

# 查看健康报告
python scripts/gateway_guardian.py health

# 显示帮助
python scripts/gateway_guardian.py help
```

## 📋 通知模板

### 网关异常告警
```
🛡️ 网关守护神

⚠️ 网关异常告警

网关状态异常

端口状态：❌
进程状态：❌
连续失败：3

正在尝试重启...
```

### 网关已恢复
```
🛡️ 网关守护神

✅ 网关已恢复

网关已成功重启
重启时间：2026-03-12 16:30:45
```

### 守护神已启动
```
🛡️ 网关守护神

🚀 守护神已启动

OpenClaw 网关守护进程已启动
监控端口：18789
检查间隔：30 秒
```

## 📊 健康报告

运行 `python scripts/gateway_guardian.py health` 查看：

```
📊 健康报告 (共 288 条记录)

总检查次数：288
健康次数：285 (99.0%)
异常次数：3 (1.0%)

📋 最近 10 条记录:
   ✅ 2026-03-12T16:30:00 - healthy
   ✅ 2026-03-12T16:29:30 - healthy
   ✅ 2026-03-12T16:29:00 - healthy
   ❌ 2026-03-12T16:28:30 - port_closed
   ✅ 2026-03-12T16:28:00 - healthy (重启后)
   ...
```

## 🔧 高级配置

### 修改检查间隔

编辑 `~/.openclaw_guardian/config.json`：

```json
{
  "gateway": {
    "check_interval_seconds": 60  // 改为 60 秒
  }
}
```

### 禁用通知

```json
{
  "notifications": {
    "enabled": false
  }
}
```

### 增加最大重启次数

```json
{
  "gateway": {
    "max_restart_attempts": 20  // 改为 20 次
  }
}
```

## 📁 文件结构

```
openclaw-gateway-guardian/
├── README.md                     # 本文档
├── SKILL.md                      # OpenClaw Skill 定义
├── requirements.txt              # Python 依赖
├── scripts/
│   └── gateway_guardian.py       # 主程序
└── ~/.openclaw_guardian/         # 运行时目录（自动创建）
    ├── config.json               # 配置文件
    ├── guardian.log              # 日志文件
    ├── guardian.pid              # PID 文件
    └── health_log.json           # 健康日志
```

## 🔍 故障排除

### Q: 守护进程启动失败？
A: 
1. 检查是否已有实例运行：`python gateway_guardian.py status`
2. 删除 PID 文件：`~/.openclaw_guardian/guardian.pid`
3. 查看日志：`python gateway_guardian.py logs`

### Q: 通知不发送？
A:
1. 检查通知配置是否正确
2. 运行 `python gateway_guardian.py status` 确认配置
3. 检查网络连接

### Q: 网关频繁重启？
A:
1. 查看健康日志：`python gateway_guardian.py health`
2. 检查网关日志：`Get-Content "$env:TEMP\openclaw\*.log" -Tail 50`
3. 可能是网关配置问题，需要修复网关

### Q: 如何开机自启？
A: 
Windows: 将 `pythonw.exe scripts/gateway_guardian.py start` 添加到启动项
Linux: 添加 systemd 服务或 cron @reboot

## 📊 性能指标

| 指标 | 数值 |
|------|------|
| CPU 占用 | < 1% |
| 内存占用 | < 50MB |
| 检查延迟 | < 1 秒 |
| 重启延迟 | 5-10 秒 |
| 日志大小 | < 10MB |

## ⚠️ 注意事项

1. **不要同时运行多个实例** - 会导致冲突
2. **定期清理日志** - 避免日志文件过大
3. **配置通知渠道** - 否则无法收到告警
4. **检查网关配置** - 守护神只能重启，不能修复配置错误

## 📄 许可证

MIT License

## 👥 作者

davidme6

## 🆘 支持

如有问题，请提交 Issue 或联系作者。

---

**让网关永远在线，不再担心意外停止！🛡️**
