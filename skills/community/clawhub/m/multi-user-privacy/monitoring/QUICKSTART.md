# 🚀 监控告警系统 - 快速上手

## 一分钟启动

```bash
cd ~/.openclaw/workspace/monitoring
./start.sh start
```

## 常用命令

| 命令 | 说明 |
|-----|------|
| `./start.sh start` | 启动监控服务 |
| `./start.sh stop` | 停止监控服务 |
| `./start.sh restart` | 重启监控服务 |
| `./start.sh status` | 查看服务状态 |
| `./start.sh log` | 查看实时日志 |
| `node monitor.js check` | 手动执行一次检查 |

## 查看监控状态

```bash
./start.sh status
```

输出示例：
```
✅ 监控服务运行中 (PID: 672371)

📊 OpenClaw 监控状态
══════════════════════════════════════════════════
最后检查：2026/3/12 11:47:57
子代理状态：ok (6 个活跃)
配额检查：ok (2 个用户)
Gateway 状态：✅ 正常
当前告警：0 项
══════════════════════════════════════════════════
```

## 配置告警阈值

编辑 `alert-config.json`：

```bash
nano alert-config.json
```

关键配置：
- `checkIntervalSeconds`: 检查间隔（默认 60 秒）
- `thresholds.subagents.maxConcurrent`: 最大并发子代理数（默认 10）
- `thresholds.quota.tokenUsagePercent`: Token 预警阈值（默认 80%）

## 查看日志

```bash
# 实时监控日志
./start.sh log

# 查看告警日志
tail -f ../logs/alert.log
```

## 接收飞书告警

当触发告警时，会自动发送飞书消息到配置的接收人。

告警类型：
- ⏰ 子代理运行超时
- 🔒 子代理卡住
- 🚦 并发数超限
- ⚠️ 配额即将用尽
- ❌ 配额已用尽
- 💥 Gateway 宕机

## 停止监控

```bash
./start.sh stop
```

## 开机自启（可选）

使用 systemd：
```bash
sudo systemctl enable openclaw-monitor@$(whoami).service
sudo systemctl start openclaw-monitor@$(whoami).service
```

使用 cron（每分钟检查）：
```bash
(crontab -l 2>/dev/null; echo "* * * * * cd ~/.openclaw/workspace/monitoring && node monitor.js check") | crontab -
```

## 问题排查

**服务未运行？**
```bash
./start.sh status
ps aux | grep monitor.js
```

**告警未发送？**
1. 检查 `alert-config.json` 中 `notification.enabled` 是否为 `true`
2. 检查 `openclaw.json` 中飞书配置是否正确
3. 查看日志：`./start.sh log`

**配额数据未更新？**
配额由 `multi-user-privacy` 技能管理，确保该技能已正确配置。

---

📖 完整文档：`README.md`  
📊 监控总结：`../docs/monitoring-system-summary.md`
