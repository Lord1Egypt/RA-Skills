---
name: minimax-token-plan-monitor
description: MiniMax Token Plan 用量监控 — 专为云部署龙虾（OpenClaw）设计，自动查询本周/5小时窗口用量、套餐余量、剩余调用次数及重置时间。支持 QQ/Discord/Telegram 多通道通知，可配置告警阈值。触发词：minimax额度查询、token plan用量、本周用量、剩余次数、订阅状态、minimax coding plan、minimax配额。
---

# MiniMax Token Plan 用量监控 📊

监控 MiniMax Token Plan 订阅套餐的实时用量，支持多通道通知和告警阈值配置。

## 功能特性

- 🔄 **自动查询**：5小时窗口 + 本周用量同时监控
- 🔔 **多通道通知**：支持 QQ / Discord / Telegram 推送
- ⚙️ **告警阈值**：可配置用量百分比告警
- ⏰ **定时巡检**：通过 cronjob 实现每日定时检查
- 🇨🇳 **国内适配**：针对国内版 MiniMax 平台优化

---

## 环境配置

在 `~/.env` 中配置以下变量：

```bash
# MiniMax 账号（账号 + 密码）
MINIMAX_PHONE=your_account_here
MINIMAX_PASSWORD=your_password_here

# 通知配置（可选，留空则只输出日志）
QQBOT_PORT=37701
# QQ/Discord/Telegram 通知通过 OpenClaw 消息通道发送
```

---

## 快速使用

### 手动查询

```bash
cd ~/.openclaw/workspace/skills/minimax-token-plan/scripts
node get_token_plan_usage.js
```

> 依赖 `~/.env` 中的账号信息运行

### 输出示例

```
📊 MiniMax Token Plan 用量报告

⏰ 2026/4/4 22:00:21

🏷️ 套餐: Starter

📌 5小时窗口: 4 / 600 (1%)

📌 本周: 1398 / 6000 (23%)

🔄 25 小时 59 分钟后重置
```

### JSON 原始输出

```json
{
  "success": true,
  "data": {
    "url": "https://platform.minimaxi.com/user-center/payment/token-plan",
    "plan": "Starter",
    "fiveHour": { "used": 4, "limit": 600, "usedPercent": 1 },
    "week": { "used": 1398, "limit": 6000, "usedPercent": 23 },
    "resetTime": "25 小时 59 分钟后重置"
  }
}
```

---

## 定时任务配置（cron）

推荐监控时间点：每天 10/12/14/16/18/20/22 点

```bash
# 在 OpenClaw 配置中设置 cron
0 10,12,14,16,18,20,22 * * * /usr/bin/node /root/.openclaw/workspace/skills/minimax-token-plan/scripts/get_token_plan_usage.js >> /root/.openclaw/workspace/skills/minimax-token-plan/cron.log 2>&1
```

---

## 告警阈值配置

在 `scripts/config.json` 中修改：

```json
{
  "alertThreshold": {
    "fiveHourPercent": 80,
    "weekPercent": 80
  }
}
```

当用量超过阈值时，会在通知中突出显示 ⚠️ 警告。

---

## 限速说明

| 窗口 | 套餐 | 说明 |
|------|------|------|
| 5小时 | 600次 | Starter 套餐限制 |
| 本周 | 6000次 | 自然周统计，重置时间见输出 |

> 1次 API 调用 ≈ 1次模型请求

---

## 依赖

- Node.js + Playwright
- Chromium 浏览器（自动安装）
- `.env` 配置文件（账号凭证）

---

## 故障排查

| 问题 | 解决方案 |
|------|---------|
| 登录失败 | 检查手机号 + 密码是否正确 |
| 页面解析失败 | MiniMax 可能更新了页面结构，需更新正则 |
| 滑动验证码 | 当前版本暂不支持，可尝试增加运行间隔 |
| 通知发送失败 | 检查 QQBot 端口配置（默认 37701） |

---

> 💡 需要在 OpenClaw 中配置 MiniMax 账号的 cookie/token 才能实现免登录，具体咨询 MiniMax 官方文档。
