# lu-nas-monitor

NAS 服务监控技能 - 帮助你监控 NAS 上的 Docker 容器和系统状态。

## 描述

这个技能提供 NAS 服务监控功能，包括：
- 查看 Docker 容器状态
- 系统资源监控（CPU/内存/磁盘）
- 服务健康检查
- 告警通知

## 触发条件

当用户提到以下关键词时激活：
- "NAS 状态"
- "服务监控"
- "容器状态"
- "CPU 使用率"
- "内存使用"
- "磁盘空间"
- "服务健康"

## 用法

### 查看 NAS 状态
```
NAS 状态
服务监控
系统状态
```

### 查看容器状态
```
容器状态
Docker 状态
mopidy 运行正常吗
```

### 系统资源
```
CPU 使用率
内存使用
磁盘空间
```

### 服务健康检查
```
服务健康检查
检查所有服务
mopidy 健康状态
```

## 示例对话

**用户**: NAS 状态怎么样？
**助手**: NAS 运行正常！Docker 容器：3 个运行中。CPU: 15%, 内存：2.3GB/8GB, 磁盘：450GB/1TB 可用。

**用户**: 容器状态
**助手**: 
```
✅ mopidy - 运行中 (3 小时)
✅ nginx-proxy-manager - 运行中 (3 小时)
✅ uptime-kuma - 运行中 (1 小时)
```

**用户**: 磁盘空间
**助手**: 磁盘使用情况：
- 系统盘：50GB/100GB (50%)
- 数据盘：450GB/1TB (45%)
- 剩余空间充足 ✅

## Docker 命令

```bash
# 查看所有容器
docker ps -a

# 查看系统资源
docker stats --no-stream

# 查看磁盘使用
docker system df

# 查看日志
docker logs <容器名> --tail 50

# 重启服务
docker-compose restart
```

## 监控脚本

```bash
#!/bin/bash

echo "=== NAS 服务监控 ==="
echo ""

# Docker 容器状态
echo "📦 Docker 容器:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo ""

# CPU 和内存
echo "💻 系统资源:"
top -bn1 | grep "Cpu(s)" | awk '{print "CPU: "$2"%" }'
free -h | grep Mem | awk '{print "内存："$3"/"$2" ("int($3/$2*100)"%)"}'
echo ""

# 磁盘空间
echo "💾 磁盘空间:"
df -h | grep -E "^/dev/sd|/vol" | awk '{print $1": "$3"/"$2" ("$5")"}'
echo ""

# 运行中的容器数量
RUNNING=$(docker ps -q | wc -l)
echo "✅ 运行中容器：$RUNNING 个"
```

## 告警配置（可选）

### Telegram 告警
```bash
TELEGRAM_BOT_TOKEN="你的 Bot Token"
TELEGRAM_CHAT_ID="你的 Chat ID"

# 发送告警
curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  -d "chat_id=${TELEGRAM_CHAT_ID}&text=⚠️ NAS 告警：容器异常"
```

## 作者

- **作者**: jesson1222-ship-it
- **版本**: 1.0.0
- **创建时间**: 2026-03-08
- **许可证**: MIT

## 更新日志

### v1.0.0 (2026-03-08)
- 初始版本
- 支持容器状态查看
- 支持系统资源监控
- 支持磁盘空间检查
