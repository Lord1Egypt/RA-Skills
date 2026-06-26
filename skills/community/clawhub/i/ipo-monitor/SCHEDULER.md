# IPO监控 V2 - 定时任务配置

本项目支持两种定时任务运行方式：

## 方式1：使用 OpenClaw Cron（推荐）

使用 OpenClaw 内置的定时任务功能，支持飞书消息推送：

```bash
# 添加定时任务：每小时运行一次
openclaw cron add \
  --name "IPO监控" \
  --schedule "0 * * * *" \
  --session isolated \
  --deliver \
  --post-to-main none \
  --message "请使用 message 工具发送：📈 IPO数据已更新，请查看最新进展！" \
  --channel feishu
```

## 方式2：使用项目内置守护进程模式

```bash
# 在项目目录下运行
cd /Users/eurus/.openclaw/workspace/ipo-monitor-v2

# 方式A: 使用 --daemon 参数（每1小时运行一次）
python main.py --daemon

# 方式B: 指定运行间隔（每2小时运行一次）
python main.py --daemon --interval 2
```

## 方式3：使用 macOS/Linux crontab

```bash
# 编辑 crontab
crontab -e

# 添加定时任务（每天9点和15点运行）
0 9,15 * * * /usr/bin/python3 /Users/eurus/.openclaw/workspace/ipo-monitor-v2/main.py >> /tmp/ipo_monitor.log 2>&1
```

## 配置说明

在 `config.yaml` 中可以配置定时任务相关参数：

```yaml
scheduler:
  # 启用定时任务
  enabled: true
  # 调度间隔（小时）
  interval_hours: 1
  # 每日定时运行时间（可选，格式: "HH:MM"）
  # daily_time: "09:00"
```

## 告警配置

当某个交易所连续失败达到阈值时，会触发告警：

```yaml
alert:
  # 连续失败多少次触发告警
  failure_threshold: 3
  # 告警冷却时间（秒）
  cooldown_seconds: 3600
  # 是否启用告警
  enabled: true

feishu:
  # 单独的告警webhook
  alert_webhook: "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_ALERT_WEBHOOK_HERE"
```

## 启动命令汇总

```bash
# 单次运行（测试模式，不推送）
python main.py --test

# 单次运行（生产模式）
python main.py

# 守护进程模式
python main.py --daemon

# 指定配置文件
python main.py --config /path/to/config.yaml
```
