---
name: privacy-scanner
description: 发布前隐私扫描。在发布 skill 到 ClawHub 或公开仓库前，扫描代码中是否包含敏感信息（webhook、token、用户名路径、飞书 ID、内网 IP、Discord/Slack/Telegram、JWT、SSH 私钥、数据库连接、第三方 API Key 等）。当用户提到发布、publish、隐私检查、隐私扫描、敏感信息检查时使用此技能。支持 20 项扫描。
---

# Privacy Scanner - 发布前隐私扫描

扫描代码/技能目录中是否包含敏感信息，防止隐私数据泄露到 ClawHub 或公开仓库。

## 快速使用

```bash
# 扫描当前目录
bash ~/.openclaw/skills/privacy-scanner/scripts/privacy-scan.sh

# 扫描指定目录
bash ~/.openclaw/skills/privacy-scanner/scripts/privacy-scan.sh ~/.openclaw/skills/my-skill

# 严格模式（发现任何问题即退出码非零）
bash ~/.openclaw/skills/privacy-scanner/scripts/privacy-scan.sh --strict /path/to/skill
```

## 扫描项（20 项）

| # | 类别 | 检测内容 | 严重程度 |
|---|------|----------|----------|
| 1 | Webhook URL | 飞书等 webhook | ❌ |
| 2 | 飞书 ID | ou_/oc_/om_ + 20位 | ❌ |
| 3 | 用户名路径 | /Users/xxx, /home/xxx | ❌ |
| 4 | API Key | sk-, ghp_, xoxb-, AKIA | ❌ |
| 5 | Bearer Token | Bearer xxx (20+字符) | ❌ |
| 6 | 内网 IP | 192.168.x.x, 10.x.x.x | ⚠️ |
| 7 | 邮箱 | user@domain.com | ⚠️ |
| 8 | 手机号 | 中国大陆 11 位 | ❌ |
| 9 | 敏感文件 | .env, credentials.json, 私钥 | ❌ |
| 10 | 密码/Secret | password="xxx", secret="xxx" | ❌ |
| 11 | Discord Webhook | discord.com/api/webhooks/ | ❌ |
| 12 | Slack Webhook | hooks.slack.com/services/ | ❌ |
| 13 | Telegram Bot Token | 123456:ABCdef... | ❌ |
| 14 | 数字 ID | Discord/Telegram 17-19位 | ⚠️ |
| 15 | JWT Token | eyJxxx.eyJxxx.xxx | ❌ |
| 16 | SSH 私钥 | -----BEGIN PRIVATE KEY----- | ❌ |
| 17 | 数据库连接 | mongodb://, postgresql:// | ❌ |
| 18 | 第三方 API Key | OpenAI, Anthropic, Stripe, Google | ❌ |
| 19 | 主机名/机器名 | 当前 hostname | ⚠️ |
| 20 | 公网 IP | 非内网的 IPv4 | ⚠️ |

## 跳过规则

以下文件/目录自动跳过：
- `node_modules/`, `.git/`, `backups/`
- `logs/`, `*.log`, `*.tmp`
- `agents/`, `extensions/`
- 二进制文件（图片、压缩包等）

## 输出

- `✅` 通过 — 未发现隐私泄露
- `⚠️` 警告 — 可能是占位符，需人工确认
- `❌` 失败 — 确认是真实敏感数据

## 在公约中使用

参考 AGENTS.md 中的「发布到 ClawHub 公约」，发布前必须通过此扫描。
