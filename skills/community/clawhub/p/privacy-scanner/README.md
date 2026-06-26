# Privacy Scanner - 发布前隐私扫描

在发布 skill 到 ClawHub 或公开仓库前，扫描代码中是否包含敏感信息。支持 **20 项扫描**。

## 快速使用

```bash
# 扫描当前目录
bash ~/.openclaw/skills/privacy-scanner/scripts/privacy-scan.sh

# 扫描指定目录
bash ~/.openclaw/skills/privacy-scanner/scripts/privacy-scan.sh ~/.openclaw/skills/my-skill

# 严格模式
bash ~/.openclaw/skills/privacy-scanner/scripts/privacy-scan.sh --strict ~/.openclaw/skills/my-skill
```

## 扫描项（20 项）

| # | 类别 | 检测模式 | 严重程度 |
|---|------|----------|----------|
| 1 | Webhook URL | `hook/[a-f0-9]{20,}` | ❌ 失败 |
| 2 | 飞书 ID | `ou_/oc_/om_` + 20位字符 | ❌ 失败 |
| 3 | 用户名路径 | `/Users/xxx`, `/home/xxx` | ❌ 失败 |
| 4 | API Key | `sk-`, `ghp_`, `xoxb-`, AWS AKIA | ❌ 失败 |
| 5 | Bearer Token | `Bearer xxx` (20+字符) | ❌ 失败 |
| 6 | 内网 IP | `192.168.x.x`, `10.x.x.x` | ⚠️ 警告 |
| 7 | 邮箱地址 | `user@domain.com` | ⚠️ 警告 |
| 8 | 手机号 | 中国大陆 11 位 | ❌ 失败 |
| 9 | 敏感文件 | `.env`, `credentials.json`, 私钥 | ❌ 失败 |
| 10 | 密码/Secret | `password="xxx"`, `secret="xxx"` | ❌ 失败 |
| 11 | Discord Webhook | `discord.com/api/webhooks/` | ❌ 失败 |
| 12 | Slack Webhook | `hooks.slack.com/services/` | ❌ 失败 |
| 13 | Telegram Bot Token | `123456789:ABC...` | ❌ 失败 |
| 14 | Discord/Telegram 数字 ID | 17-19位数字, `-100xxx` | ⚠️ 警告 |
| 15 | JWT Token | `eyJxxx.eyJxxx` | ❌ 失败 |
| 16 | SSH 私钥 | `-----BEGIN PRIVATE KEY-----` | ❌ 失败 |
| 17 | 数据库连接 | `mongodb://`, `postgresql://` | ❌ 失败 |
| 18 | 第三方 API Key | `sk-proj-`, `sk-ant-`, `sk_live_`, `AIza`, `ghs_` | ❌ 失败 |
| 19 | 主机名/机器名 | 当前 hostname | ⚠️ 警告 |
| 20 | 公网 IP | 非内网的 IPv4 地址 | ⚠️ 警告 |

## 退出码

- `0` — 扫描通过（可能有警告）
- `1` — 扫描失败（发现严重问题）

## 占位符白名单

以下模式被视为安全占位符，不会触发告警：
- `YOUR_HOOK_ID`, `YOUR_TOKEN`, `PLACEHOLDER`
- `example.com`, `your_` 前缀
- `$HOME`, `__USER_HOME__`, `~`
- `openclaw@local`（git 默认邮箱）
- `/Users/xxx`, `/Users/john`, `/home/user`（示例路径）
- `user@domain`, `test@`, `admin@localhost`（示例邮箱）
- `127.0.0.1`, `localhost`, `1.1.1.1`, `8.8.8.8`（常见地址）

## 发布到 ClawHub 公约

参考 AGENTS.md，**必须严格遵守**：

```
1. 扫描    → bash ~/.openclaw/skills/privacy-scanner/scripts/privacy-scan.sh <目录>
2. 通过    → 全部 ✅ 或只有 ⚠️（需人工确认）
3. Review  → git diff 查看改动内容
4. 发布    → clawhub publish <目录> --version x.x.x --changelog "..."
```

**退出码必须为 0 才能发布。**
