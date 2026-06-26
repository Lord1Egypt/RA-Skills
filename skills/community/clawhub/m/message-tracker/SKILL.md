# Message Tracker Skill

**版本**: v2.0
**更新日期**: 2026-05-01
**状态**: 正常运行

---

## 简介

message-tracker 是一个基于 Python 的消息追踪系统，支持飞书频道消息采集、存储、检索和统计分析。

## 目录结构

```
message-tracker/
├── SKILL.md                          # 本文件
├── track.py                          # v1版本追踪器
├── track_v2.py                       # v2版本追踪器（推荐）
└── .daemon.pid                       # 守护进程PID文件
```

## 核心功能

### 1. 消息采集
- 飞书频道消息实时采集
- 定时轮询采集模式
- 支持指定时间范围

### 2. 消息存储
- SQLite本地存储
- JSON格式导出
- 自动归档

### 3. 消息检索
- 按关键词搜索
- 按时间范围过滤
- 按发送人筛选

### 4. 统计分析
- 消息数量统计
- 活跃度分析
- 趋势图表

## 使用方式

### 启动守护进程
```bash
# 启动v2版本（推荐）
python3 message-tracker/track_v2.py start

# 启动v1版本
python3 message-tracker/track.py start
```

### 命令行操作
```bash
# 查看状态
python3 message-tracker/track_v2.py status

# 停止守护进程
python3 message-tracker/track_v2.py stop

# 重启守护进程
python3 message-tracker/track_v2.py restart

# 手动触发采集
python3 message-tracker/track_v2.py collect

# 搜索消息
python3 message-tracker/track_v2.py search "关键词"

# 导出消息
python3 message-tracker/track_v2.py export --days 7 --output messages.json

# 统计报告
python3 message-tracker/track_v2.py stats --days 30
```

### 守护进程管理
```bash
# 检查进程
cat message-tracker/.daemon.pid

# 查看日志
tail -f /root/.openclaw/logs/message-tracker.log

# 手动杀死进程
kill $(cat message-tracker/.daemon.pid)
```

## 配置说明

### 数据存储
- 数据库：`/root/.openclaw/workspace/memory/tracker/messages.db`
- 日志：`/root/.openclaw/logs/message-tracker.log`
- 导出：`/root/.openclaw/workspace/memory/tracker/exports/`

### 采集间隔
- 默认：60秒
- 可通过配置调整

### 日志级别
- INFO: 正常日志
- WARNING: 警告
- ERROR: 错误

## 状态文件

| 文件 | 路径 | 说明 |
|------|------|------|
| PID文件 | message-tracker/.daemon.pid | 守护进程PID |
| 数据库 | memory/tracker/messages.db | 消息存储 |
| 日志 | logs/message-tracker.log | 运行日志 |

## 常见问题

### Q: 守护进程意外退出？
**A**: 检查日志文件 `/root/.openclaw/logs/message-tracker.log` 排查原因，手动重启。

### Q: 消息采集不到？
**A**: 
1. 检查飞书机器人Token是否有效
2. 检查网络连接
3. 查看错误日志

### Q: 数据库太大？
**A**: 使用 `track_v2.py export` 导出后清理旧数据

## 版本说明

| 版本 | 文件 | 说明 |
|------|------|------|
| v1 | track.py | 早期版本 |
| v2 | track_v2.py | 当前主力版本，功能更完善 |