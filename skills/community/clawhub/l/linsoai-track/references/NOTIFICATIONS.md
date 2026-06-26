# 通知渠道配置指南

## 概览

linsoai-track 支持三类通知方式：

| 类型 | 方式 | 推荐度 |
|------|------|--------|
| IM 通知 | `openclaw message send` | 推荐 — 开箱即用 |
| 邮件通知 | send-email skill | 需要 SMTP 配置 |
| Webhook | curl 调用 | 适合系统集成 |

---

## IM 通知（推荐）

OpenClaw 原生支持 18 个即时通讯渠道，无需额外配置。

### 配置渠道

```bash
# Telegram
openclaw channels add telegram --token <BotToken> --chat <ChatID>

# 飞书
openclaw channels add feishu
# 按提示完成配置

# Discord
openclaw channels add discord --webhook <WebhookURL>

# Slack
openclaw channels add slack --webhook <WebhookURL>
```

### 支持的渠道列表

Telegram、飞书、Discord、Slack、WhatsApp、Signal、企业微信、Mattermost、Matrix、Google Chat、LINE、Zulip、Rocket.Chat、Gotify、Ntfy、Pushover、Pushbullet、IFTTT

### 在任务中使用

在 `--message` 中指示 Agent 使用通知：

```
"...如果{条件}，用 openclaw message send --channel telegram --message '{通知内容}' 通知我。"
```

### 多渠道同时通知

```
"...如果{条件}，分别用以下方式通知我：
1. openclaw message send --channel telegram --message '{内容}'
2. openclaw message send --channel feishu --message '{内容}'"
```

### 测试通知

```bash
openclaw message send --channel telegram --message "测试通知 from linsoai-track"
```

---

## 邮件通知

邮件通知依赖 `send-email` skill，需要先安装并配置 SMTP。

### 安装 send-email skill

```bash
openclaw skills install send-email
```

### 配置 SMTP

设置环境变量：

```bash
# Resend（推荐，免费 100 封/天）
export SMTP_HOST=smtp.resend.com
export SMTP_PORT=587
export SMTP_USER=resend
export SMTP_PASS=re_xxxxxxxxxx  # 你的 Resend API Key
export MAIL_FROM="Task Notify <notify@yourdomain.com>"
```

其他 SMTP 服务：

| 服务 | SMTP Host | 端口 | 免费额度 |
|------|-----------|------|----------|
| Resend | smtp.resend.com | 587 | 100 封/天 |
| Mailgun | smtp.mailgun.org | 587 | 100 封/天 |
| SendGrid | smtp.sendgrid.net | 587 | 100 封/天 |
| Gmail | smtp.gmail.com | 587 | 500 封/天 |

### 在任务中使用

```
"...如果{条件}，用 send-email skill 发送邮件到 me@example.com，主题为 '{主题}'，内容为 '{正文}'。"
```

---

## Webhook 通知

适合与外部系统（企业内部平台、自建服务、自动化流程）集成。

### 在任务中使用

```
"...如果{条件}，用 curl 发送 POST 请求：
curl -X POST https://your-server.com/webhook \
  -H 'Content-Type: application/json' \
  -d '{\"event\": \"task_alert\", \"message\": \"{摘要}\"}'"
```

### 带认证的 Webhook

```
"...用 curl 发送通知：
curl -X POST https://your-server.com/webhook \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -d '{\"event\": \"monitor_alert\", \"data\": {\"summary\": \"{结果摘要}\"}}'"
```

---

## 选择建议

- **个人日常使用** → Telegram 或飞书，配置简单，消息即时
- **团队协作** → Slack 或 Discord，可发到指定频道
- **需要邮件存档** → 邮件通知，适合正式报告类任务
- **系统集成** → Webhook，对接内部平台或自动化流程
- **重要告警** → 多渠道同时通知，确保不遗漏
