---
name: one-calendar
description: 每日单向历图片发送工具。自动获取当天日期，构造图片 URL，并通过飞书发送单向历图片。支持配置向导和定时任务。
metadata:
  author: chempeng
  version: "1.1.0"
  created: "2026-03-05"
  updated: "2026-03-05"
  repository: https://github.com/chempeng/one-calendar
---

# One Calendar - 单向历

> 📅 一天，一张图，一份日历的温度。

## 快速开始

### 1. 配置

```bash
cd ~/.openclaw/workspace/skills/one-calendar
node scripts/setup.js
```

向导会引导你输入飞书用户 ID 并保存配置。

### 2. 使用

**手动发送**：
```bash
node scripts/send.js
```

**对话触发**：
```
单向历
今日单向历
发单向历
```

**定时任务**（每天早上 8 点）：
```bash
openclaw cron add \
  --name "每日单向历" \
  --at "0 8 * * *" \
  --session isolated \
  --message "node ~/.openclaw/workspace/skills/one-calendar/scripts/send.js" \
  --workdir ~/.openclaw/workspace
```

## 配置说明

配置文件：`config.json`（由 `setup.js` 生成）

```json
{
  "feishu": {
    "userId": "ou_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  },
  "settings": {
    "timezone": "Asia/Shanghai",
    "baseUrl": "https://img.owspace.com/Public/uploads/Download"
  }
}
```

**获取飞书用户 ID**：运行 `openclaw logs --follow`，然后在飞书中给机器人发消息，日志中 `ou_` 开头的字符串即为你的 ID。

## 文件结构

```
one-calendar/
├── config.example.json   # 配置模板
├── config.json           # 用户配置（setup.js 生成）
├── SKILL.md              # 技能定义
├── README.md             # 详细文档
└── scripts/
    ├── send.js           # 发送脚本
    └── setup.js          # 配置向导
```

## 注意事项

- 首次使用请先运行 `node scripts/setup.js`
- 飞书用户 ID 必须以 `ou_` 开头
- 图片源为单向历官方服务器，格式：`{YEAR}/{MMDD}.jpg`
