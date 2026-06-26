# OpenClaw 监控运维指南

## 目录
- [日志配置](#日志配置)
- [性能指标](#性能指标)
- [健康检查](#健康检查)
- [告警配置](#告警配置)
- [备份恢复](#备份恢复)

---

## 日志配置

### 开发环境

```json
{
  "logging": {
    "level": "DEBUG",
    "handlers": {
      "console": {
        "class": "logging.StreamHandler",
        "formatter": "standard"
      },
      "file": {
        "class": "logging.handlers.RotatingFileHandler",
        "filename": "~/.openclaw/logs/openclaw.log",
        "maxBytes": 104857600,
        "backupCount": 5
      }
    }
  }
}
```

### 生产环境

```json
{
  "logging": {
    "level": "INFO",
    "format": "json",
    "handlers": {
      "syslog": {
        "class": "logging.handlers.SysLogHandler",
        "address": "/dev/log"
      },
      "json_file": {
        "class": "logging.handlers.TimedRotatingFileHandler",
        "when": "midnight",
        "backupCount": 90
      }
    }
  }
}
```

### 日志分析

```bash
# 查看最近 100 行
tail -100 ~/.openclaw/logs/openclaw.log

# 搜索错误
grep -i error ~/.openclaw/logs/openclaw.log

# 统计错误类型
grep -i error ~/.openclaw/logs/openclaw.log | cut -d: -f4 | sort | uniq -c

# 实时监控
tail -f ~/.openclaw/logs/openclaw.log | grep -i error
```

---

## 性能指标

### 关键指标

| 指标 | 说明 | 阈值 |
|------|------|------|
| CPU 使用率 | 系统 CPU 占用 | > 90% 告警 |
| 内存使用率 | 系统内存占用 | > 85% 告警 |
| 请求延迟 P95 | 95% 请求耗时 | > 500ms 告警 |
| 错误率 | 失败请求占比 | > 1% 告警 |
| 队列深度 | 待处理请求数 | > 100 告警 |

### Prometheus 配置

```yaml
scrape_configs:
  - job_name: 'openclaw'
    scrape_interval: 15s
    static_configs:
      - targets: ['localhost:9090']
```

### Grafana 仪表盘

```json
{
  "dashboard": {
    "title": "OpenClaw 监控",
    "panels": [
      {
        "title": "系统资源",
        "type": "graph",
        "targets": [
          {"expr": "cpu_usage", "legendFormat": "CPU"},
          {"expr": "memory_usage", "legendFormat": "Memory"}
        ]
      },
      {
        "title": "请求延迟",
        "type": "graph",
        "targets": [
          {"expr": "request_duration_p95"},
          {"expr": "request_duration_p99"}
        ]
      }
    ]
  }
}
```

---

## 健康检查

### 基础检查

```json
{
  "health_check": {
    "enabled": true,
    "endpoint": "/health",
    "interval": 30,
    "checks": [
      {"name": "process", "type": "process"},
      {"name": "disk", "type": "disk", "threshold": 90}
    ]
  }
}
```

### 全面检查

```json
{
  "health_check": {
    "enabled": true,
    "endpoint": "/health",
    "checks": [
      {"name": "gateway", "type": "http", "url": "http://localhost:18789/health"},
      {"name": "database", "type": "database"},
      {"name": "memory", "type": "memory", "threshold": 80},
      {"name": "disk", "type": "disk", "threshold": 85},
      {"name": "network", "type": "network", "ports": [18789]}
    ]
  }
}
```

### 健康检查 API

```bash
# 检查健康状态
curl http://localhost:18789/health

# 详细健康信息
curl http://localhost:18789/health?verbose=true
```

---

## 告警配置

### 告警规则

```json
{
  "alerts": {
    "rules": [
      {
        "name": "high_cpu",
        "condition": "cpu_usage > 90",
        "duration": "5m",
        "severity": "critical",
        "channels": ["email", "slack"],
        "message": "CPU 使用率超过 90%"
      },
      {
        "name": "high_memory",
        "condition": "memory_usage > 85",
        "duration": "5m",
        "severity": "critical",
        "channels": ["email", "slack"]
      },
      {
        "name": "slow_response",
        "condition": "request_duration_p99 > 5000",
        "duration": "5m",
        "severity": "warning",
        "channels": ["slack"]
      }
    ],
    "channels": {
      "email": {
        "enabled": true,
        "smtp_host": "smtp.example.com",
        "to": ["admin@example.com"]
      },
      "slack": {
        "enabled": true,
        "webhook_url": "https://hooks.slack.com/services/xxx"
      }
    }
  }
}
```

### 告警渠道配置

#### Email

```json
{
  "channel": "email",
  "config": {
    "smtp_host": "smtp.example.com",
    "smtp_port": 587,
    "from": "openclaw-alert@example.com",
    "to": ["admin@example.com"],
    "use_tls": true
  }
}
```

#### Slack

```json
{
  "channel": "slack",
  "config": {
    "webhook_url": "https://hooks.slack.com/services/xxx",
    "channel": "#alerts",
    "username": "OpenClaw Alert"
  }
}
```

---

## 备份恢复

### 备份配置

```json
{
  "backup": {
    "enabled": true,
    "schedule": "0 2 * * *",
    "retention": {
      "daily": 7,
      "weekly": 4,
      "monthly": 12
    },
    "targets": [
      {
        "name": "config",
        "path": "~/.openclaw/config",
        "compression": "gzip"
      },
      {
        "name": "memory",
        "path": "~/.openclaw/chroma",
        "compression": "gzip"
      },
      {
        "name": "plugins",
        "path": "~/.openclaw/plugins"
      }
    ],
    "destination": {
      "type": "local",
      "path": "~/.openclaw/backups"
    }
  }
}
```

### 云端备份

```json
{
  "destination": {
    "type": "s3",
    "bucket": "openclaw-backups",
    "prefix": "openclaw/",
    "region": "us-east-1",
    "encryption": true
  }
}
```

### 手动备份

```bash
# 创建备份
openclaw backup create

# 列出备份
openclaw backup list

# 恢复备份
openclaw backup restore --id <backup_id>

# 清理旧备份
openclaw backup cleanup --keep 3
```

---

## 运维命令

```bash
# 查看状态
openclaw status

# 查看日志
openclaw logs

# 重启服务
openclaw restart

# 清理缓存
openclaw cache clear

# 更新版本
openclaw update

# 卸载
openclaw uninstall
```

---

## 故障排查清单

| 问题 | 检查项 |
|------|--------|
| 服务无法启动 | 日志、端口、权限 |
| 响应慢 | CPU、内存、网络 |
| 存储满 | 清理日志、备份 |
| 无法连接 | 防火墙、网络 |
| 数据丢失 | 备份、历史 |
