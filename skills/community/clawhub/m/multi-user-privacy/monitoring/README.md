# OpenClaw 监控告警系统使用文档

## 📋 概述

OpenClaw 监控告警系统提供对子代理运行状态、配额使用情况和 Gateway 健康状态的实时监控，并通过飞书消息发送告警通知。

## 🎯 功能特性

### 1. 子代理运行状态监控
- ✅ 监控活跃子代理数量
- ✅ 检测运行时间超限（默认 2 小时）
- ✅ 检测卡住的子代理（已完成但未清理）
- ✅ 并发数超限告警（默认 10 个）

### 2. 配额使用情况监控
- ✅ Token 配额使用率监控
- ✅ 消息配额使用率监控
- ✅ 磁盘配额使用率监控
- ✅ 配额预警（80% 阈值）
- ✅ 配额超限告警（100%）

### 3. Gateway 健康监控
- ✅ Gateway 运行状态检查
- ✅ 连续失败检测
- ✅ 宕机告警

### 4. 飞书消息告警
- ✅ 实时告警通知
- ✅ 格式化告警消息
- ✅ 告警分类汇总
- ✅ 可配置告警接收人

## 📁 文件结构

```
~/.openclaw/workspace/monitoring/
├── monitor.js              # 主监控脚本
├── alert-config.json       # 告警配置文件
├── monitor-state.json      # 监控状态文件（运行时生成）
├── openclaw-monitor.service # systemd 服务文件
└── README.md               # 本文档
```

## ⚙️ 配置说明

### 告警配置文件 (alert-config.json)

```json
{
  "enabled": true,                    // 是否启用监控
  "checkIntervalSeconds": 60,         // 检查间隔（秒）
  "notification": {
    "channel": "feishu",              // 通知渠道
    "recipientUserId": "ou_xxx",      // 告警接收人 ID
    "enabled": true                   // 是否启用通知
  },
  "thresholds": {
    "subagents": {
      "maxConcurrent": 10,            // 最大并发子代理数
      "maxRunningTimeHours": 2,       // 最大运行时间（小时）
      "alertOnStuck": true,           // 卡住时告警
      "stuckThresholdMinutes": 30     // 卡住判定阈值（分钟）
    },
    "quota": {
      "tokenUsagePercent": 80,        // Token 预警阈值（%）
      "messageUsagePercent": 80,      // 消息预警阈值（%）
      "diskUsagePercent": 80,         // 磁盘预警阈值（%）
      "alertOnApproaching": true,     // 接近阈值时告警
      "alertOnExceeded": true         // 超限时告警
    },
    "gateway": {
      "checkHealth": true,            // 是否检查 Gateway 健康
      "alertOnFailure": true,         // 失败时告警
      "consecutiveFailures": 3        // 连续失败次数阈值
    }
  },
  "quietHours": {
    "enabled": false,                 // 是否启用免打扰时段
    "start": "23:00",                 // 开始时间
    "end": "08:00",                   // 结束时间
    "timezone": "Asia/Shanghai"       // 时区
  }
}
```

## 🚀 使用方法

### 手动执行检查

```bash
cd ~/.openclaw/workspace/monitoring
node monitor.js check
```

### 查看监控状态

```bash
node monitor.js status
```

### 启动持续监控服务

```bash
# 前台运行
node monitor.js start

# 后台运行（使用 nohup）
nohup node monitor.js start > monitor.log 2>&1 &

# 或使用 systemd（推荐）
sudo systemctl enable openclaw-monitor@$(whoami).service
sudo systemctl start openclaw-monitor@$(whoami).service
```

### 查看监控日志

```bash
# 查看告警日志
tail -f ~/.openclaw/workspace/logs/alert.log

# 查看 systemd 日志（如果使用 systemd）
journalctl -u openclaw-monitor@$(whoami).service -f
```

## 📊 监控状态文件 (monitor-state.json)

运行时会自动生成状态文件，包含：

```json
{
  "lastCheck": "2026-03-12T11:44:00.000Z",
  "subagents": {
    "active": 3,
    "status": "ok"
  },
  "quotas": {
    "usersChecked": 2,
    "status": "ok"
  },
  "gateway": {
    "status": "ok",
    "healthy": true,
    "alerts": []
  },
  "alertsCount": 0,
  "lastAlerts": []
}
```

## 🚨 告警类型

### 子代理告警

| 告警类型 | 说明 | 触发条件 |
|---------|------|---------|
| `subagent_timeout` | 子代理运行超时 | 运行时间 > 2 小时 |
| `subagent_stuck` | 子代理卡住 | 已完成但未清理 |
| `subagent_concurrent_exceeded` | 并发数超限 | 活跃数 > 最大并发数 |

### 配额告警

| 告警类型 | 说明 | 触发条件 |
|---------|------|---------|
| `quota_warning` | 配额预警 | 使用率 ≥ 80% |
| `quota_exceeded` | 配额用尽 | 使用率 ≥ 100% |

### Gateway 告警

| 告警类型 | 说明 | 触发条件 |
|---------|------|---------|
| `gateway_down` | Gateway 宕机 | 连续失败 ≥ 3 次 |
| `gateway_error` | 健康检查异常 | 检查过程出错 |

## 📱 飞书告警示例

```
🚨 监控告警 (3 项)

⏰ 子代理运行超时
- P1-监控告警：2.5h

⚠️ 配额即将用尽
- ou_b96f5424... token: 85%

💥 Gateway 宕机：Gateway 已宕机 (连续失败 3 次)

时间：2026-03-12 11:44:00
```

## 🔧 故障排查

### 监控服务未运行

```bash
# 检查进程
ps aux | grep monitor.js

# 检查 systemd 状态
systemctl status openclaw-monitor@$(whoami).service
```

### 飞书告警未发送

1. 检查飞书配置是否正确
2. 检查 `openclaw.json` 中的 `appId` 和 `appSecret`
3. 查看告警日志：`~/.openclaw/workspace/logs/alert.log`
4. 检查网络连接

### 配额数据未更新

配额数据由 `multi-user-privacy` 技能管理，确保该技能已正确安装和配置。

## 📝 最佳实践

### 1. 合理设置阈值
- 根据实际使用情况调整配额阈值
- 生产环境建议设置更保守的阈值

### 2. 定期检查日志
- 每天查看告警日志
- 关注重复出现的告警

### 3. 配置免打扰时段
- 避免夜间告警打扰
- 紧急告警可绕过免打扰

### 4. 备份配置
- 定期备份 `alert-config.json`
- 记录配置变更历史

## 🔗 相关文件

- 配额数据库：`~/.openclaw/skills/multi-user-privacy/.quota-db.json`
- 子代理运行记录：`~/.openclaw/subagents/runs.json`
- Gateway 状态：`~/.openclaw/workspace/watchdog-state.json`

## 📞 支持

如有问题，请查看日志文件或联系系统管理员。

---

**版本**: 1.0  
**创建时间**: 2026-03-12  
**最后更新**: 2026-03-12
