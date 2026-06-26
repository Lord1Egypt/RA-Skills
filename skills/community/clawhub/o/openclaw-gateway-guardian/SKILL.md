---
name: openclaw-gateway-guardian
description: OpenClaw Gateway Guardian - Automatic monitoring, protection, and restart of OpenClaw Gateway service. Prevents gateway from stopping, crashing, or disappearing. Features real-time health checks (port + process), auto-restart (up to 10 attempts), multi-channel notifications (Feishu/Telegram/WeChat), health logging, and process protection against multiple instances.
version: 1.0.0
license: MIT
author: davidme6
homepage: https://github.com/davidme6/openclaw-gateway-guardian
---

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

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 初始化配置

```bash
python scripts/gateway_guardian.py init
```

### 3. 启动守护进程

```bash
python scripts/gateway_guardian.py start
```

### 4. 查看状态

```bash
python scripts/gateway_guardian.py status
```

## 📋 通知渠道

| 渠道 | 配置难度 | 推荐度 |
|------|---------|--------|
| **飞书** | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Telegram** | ⭐⭐ | ⭐⭐⭐⭐ |
| **企业微信** | ⭐⭐ | ⭐⭐⭐⭐ |

## 🔧 配置示例

```json
{
  "gateway": {
    "port": 18789,
    "check_interval_seconds": 30,
    "max_restart_attempts": 10,
    "restart_delay_seconds": 5
  },
  "notifications": {
    "enabled": true,
    "feishu_bot_token": "xxx",
    "feishu_user_id": "ou_xxx"
  }
}
```

## 📱 通知模板

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

## 📊 命令行用法

```bash
# 初始化
python scripts/gateway_guardian.py init

# 启动
python scripts/gateway_guardian.py start

# 停止
python scripts/gateway_guardian.py stop

# 状态
python scripts/gateway_guardian.py status

# 日志
python scripts/gateway_guardian.py logs

# 健康报告
python scripts/gateway_guardian.py health
```

## 📁 文件结构

```
openclaw-gateway-guardian/
├── README.md
├── SKILL.md
├── requirements.txt
├── scripts/
│   └── gateway_guardian.py
└── ~/.openclaw_guardian/
    ├── config.json
    ├── guardian.log
    ├── guardian.pid
    └── health_log.json
```

## 🔍 工作原理

```
健康检查 (30 秒) → 异常检测 (端口 + 进程) → 自动重启 (最多 10 次)
      ↓                   ↓                      ↓
  健康日志            告警通知              重启统计
```

## ⚠️ 注意事项

1. **不要同时运行多个实例** - 会导致冲突
2. **定期清理日志** - 避免日志文件过大
3. **配置通知渠道** - 否则无法收到告警
4. **检查网关配置** - 守护神只能重启，不能修复配置错误

## 🔧 故障排除

**Q: 守护进程启动失败？**

A: 
1. 检查是否已有实例：`python gateway_guardian.py status`
2. 删除 PID 文件：`~/.openclaw_guardian/guardian.pid`
3. 查看日志：`python gateway_guardian.py logs`

**Q: 通知不发送？**

A:
1. 检查通知配置
2. 检查网络连接
3. 测试通知渠道

**Q: 网关频繁重启？**

A:
1. 查看健康日志：`python gateway_guardian.py health`
2. 检查网关日志
3. 修复网关配置问题

## 📊 性能指标

| 指标 | 数值 |
|------|------|
| CPU 占用 | < 1% |
| 内存占用 | < 50MB |
| 检查延迟 | < 1 秒 |
| 重启延迟 | 5-10 秒 |

---

**版本:** 1.0.0
**作者:** davidme6
**许可:** MIT
**发布日期:** 2026-03-12

**让网关永远在线，不再担心意外停止！🛡️**
