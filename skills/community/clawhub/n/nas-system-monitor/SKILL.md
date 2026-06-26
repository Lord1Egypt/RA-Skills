---
name: nas-system-monitor
version: 1.0.0
description: Monitor NAS system health, disk usage, network status, and auto-alert via Feishu/Discord.
homepage: https://github.com/openclaw/nas-system-monitor
metadata:
  openclaw:
    emoji: "🖥️"
    category: productivity
    price: 300
---

# NAS System Monitor

专为飞牛 NAS 设计的系统监控工具，实时监控健康状态并发送告警。

## Features

- **磁盘监控**: 使用率、SMART 健康、温度
- **网络监控**: 带宽使用、连接状态、DDoS 检测
- **服务监控**: Docker 容器、关键进程状态
- **智能告警**: 飞书/Discord/Telegram 多渠道通知

## Quick Start

```bash
# 安装
pip install -r requirements.txt

# 配置告警渠道
export FEISHU_WEBHOOK=your_webhook_url

# 启动监控
python3 monitor.py --interval 60
```

## Alert Rules

| 指标 | 警告阈值 | 紧急阈值 |
|------|----------|----------|
| 磁盘使用率 | 80% | 90% |
| CPU 温度 | 70°C | 85°C |
| 内存使用率 | 85% | 95% |
| 网络延迟 | 100ms | 500ms |

## Supported Platforms

- 飞牛 NAS (Debian 12)
- Synology DSM
- QNAP QTS
- Generic Linux
