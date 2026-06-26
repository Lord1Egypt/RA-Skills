# Kids 积分日报 Cron 配置

## 定时任务

### 1. 生成日报（每天 07:00 UTC = 北京时间 15:00）

```bash
# 系统 Cron
0 23 * * * cd /home/wang/.openclaw/agents/kids-study/workspace/skills/kids-points && node scripts/daily-report.js >> /tmp/kids-points-cron.log 2>&1
```

### 2. 发送日报（每天 07:05 UTC = 北京时间 15:05）

使用 OpenClaw Agent 发送：

```bash
# 添加到 OpenClaw Cron
openclaw cron add \
  --name "kids-points-send" \
  --cron "5 23 * * *" \
  --message "请发送 Kids 积分日报到群聊 oc_7d968e918766825eb21d51ce45d7e043" \
  --agent kids-study \
  --session kids-study
```

## 手动执行

```bash
# 生成日报
node scripts/daily-report.js

# 发送日报（Agent 执行）
# 读取 /tmp/kids-points-daily-message.json 并发送
```

## 文件说明

| 文件 | 说明 |
|------|------|
| `daily-report.js` | 生成日报，保存到文件和 `/tmp/kids-points-daily-message.json` |
| `send-to-feishu.js` | 读取消息文件并准备发送 |
| `cron-send-report.sh` | Cron 调用的包装脚本 |

## 消息流程

```
1. daily-report.js 生成日报
   ↓
2. 保存到 daily-reports/YYYY-MM-DD.md
   ↓
3. 同时保存到 /tmp/kids-points-daily-message.json
   ↓
4. OpenClaw Cron 触发 kids-study Agent
   ↓
5. Agent 读取消息文件并使用 message 工具发送
   ↓
6. 飞书群聊收到消息
```
