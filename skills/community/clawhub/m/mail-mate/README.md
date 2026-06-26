# 📬 imap-mail-pipeline

**纯标准库实现的 IMAP 邮件处理流水线 · 零浏览器依赖 · 为 LLM Agent 而生**

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](./CHANGELOG)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen.svg)](./requirements.txt)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-orange.svg)](#)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)

---

## 🌟 项目简介

`imap-mail-pipeline` 是一个面向 Linux 服务器与 AI Agent 场景的 **IMAP 邮件处理流水线**，采用 OpenClaw Skill 标准封装。

与市面上依赖 Selenium / Playwright 等浏览器方案的"邮件抓取器"不同，本项目**只使用 Python 3 标准库**（`imaplib` / `email` / `re` / `urllib`），没有一行第三方依赖。这带来了三个直接好处：

- 🪶 **极低资源消耗**：无 Chromium、无 headless 运行时，适合常驻服务器、容器、边缘设备。
- 🛡️ **风控友好**：走底层 IMAP 协议 + 客户端授权码，不触发网页端滑块 / 短信验证。
- 🚀 **即装即用**：`git clone` 后即可运行，不需要任何 `pip install`。

它同时是一个**为 LLM Agent 设计的结构化工具**——输出不只是邮件原文，而是经过"**归一化匹配 → 精确时间窗 → 正则结构化提取**"三重处理后、可被大模型直接消费的 JSON。

---

## ✨ 特性速览（Features）

| | |
|---|---|
| 🧹 **极端字符串归一化** | 抗全角/半角空格、换行、制表、零宽字符（ZWSP/BOM）、双向控制符干扰。`【SEO順位チェック_夜間バッチ処理】` 的匹配，无视后续任何空白字符全部稳命中。 |
| ⏱️ **毫秒级精准时间窗** | `start_datetime` / `end_datetime` 下沉到代码层做 aware datetime 严格比对，完美处理跨日、跨时区、跨夏令时场景。 |
| 🧭 **20+ 主流邮箱路由** | 内置阿里云、QQ、腾讯企业邮、163/126、Gmail、Outlook/Office365、Yahoo、iCloud、Fastmail、Zoho 等。一个 `provider: "gmail"` 参数自动补全 host/port。 |
| 🔍 **复合关键字检索** | 主题 + 正文双维度，组内支持 `AND` / `OR` 逻辑，组间固定 `AND`。多关键字用逗号分隔。 |
| 🧬 **正则结构化提取** | `extract_patterns` 传入 `{字段名: 正则}` 字典，自动从正文抽取结构化字段到 `extracted_data`，让 Agent 无需二次解析自然语言。 |
| 📤 **内置三平台推送** | 钉钉、飞书、Telegram Bot，支持钉钉/飞书加签校验，全部基于 `urllib` 标准库实现。 |
| ⏰ **一键 Cron 部署** | `setup_cron.sh` 幂等注册 Linux crontab，自动固化 `SKILL_*` 环境变量到 `.env`（权限 600）。 |
| 📦 **零依赖** | Python 3 标准库足矣，`requirements.txt` 为空。 |

---

## 📁 项目结构

```
imap-mail-pipeline/
├── _meta.json        # OpenClaw Skill 元数据
├── main.py           # 调度主入口
├── reader.py         # IMAP 读取 / 路由 / 时间窗 / 归一化匹配 / 正则提取
├── pusher.py         # 钉钉 / 飞书 / Telegram 推送
├── setup_cron.sh     # Linux crontab 一键注册脚本
├── README.md         # 本文档
└── skill.md          # 详细技术文档（参数表、返回字段、迁移指南等）
```

---

## 🚀 快速上手（Quick Start）

### 前置准备

1. 进入目标邮箱的 Web 后台，开启 IMAP 协议。
2. 生成 **客户端授权码**（不是登录密码）。
3. Python 3.10+，无需 `pip install`。

### 最简运行

```bash
git clone https://github.com/<your-org>/imap-mail-pipeline.git
cd imap-mail-pipeline

export SKILL_EMAIL_ACCOUNT="you@example.com"
export SKILL_AUTH_PASSWORD="your-auth-code"
export SKILL_PROVIDER="qq"                          # 或 gmail / outlook / aliyun / ...
export SKILL_SUBJECT_KEYWORDS="跑批,日报"            # 选填，默认不过滤
export SKILL_MATCH_LOGIC="OR"                        # 选填，默认 AND

python3 main.py
```

不设置任何时间窗参数时，默认抓取**过去 24 小时**内的邮件——最适合定时任务的"滑动窗口"语义。

### 也支持 stdin JSON 传参

```bash
echo '{
  "email_account": "you@example.com",
  "auth_password": "your-auth-code",
  "provider":      "gmail",
  "subject_keywords": "alert,error",
  "match_logic":   "OR"
}' | python3 main.py
```

---

## 🧠 高级用法（Advanced）

### 1. 精确时间窗：跨日抓取特定区间

需求：抓取 **前天 23:00 到今天 10:00** 的邮件（跨日不漏件）。

```bash
echo '{
  "email_account":  "you@example.com",
  "auth_password":  "your-auth-code",
  "provider":       "outlook",
  "start_datetime": "2026-04-20 23:00:00",
  "end_datetime":   "2026-04-21 10:00:00"
}' | python3 main.py
```

- 输入格式接受 `YYYY-MM-DD HH:MM:SS`、`YYYY-MM-DD`、ISO 8601（带时区）。
- **不带时区时按服务器本地时区解析**，并在返回 JSON 的 `window.tz` 字段中回显。
- 代码层执行 `start_datetime <= mail.Date <= end_datetime` 的严格比对，既不漏件也不越界。

### 2. 正则结构化提取：让 Agent 直接消费字段

需求：从跑批通知邮件中提取并行号、机器号、状态。

```bash
echo '{
  "email_account":   "you@example.com",
  "auth_password":   "your-auth-code",
  "provider":        "qq",
  "subject_keywords":"【SEO順位チェック_夜間バッチ処理】",
  "extract_patterns": {
    "parallel_id": "【並行(\\d+)番目】",
    "machine":     "(本番\\d+号機)",
    "status":      "(成功|失敗|完了|エラー)"
  }
}' | python3 main.py
```

返回的每封邮件将包含一个结构化字段：

```json
{
  "subject": "【SEO順位チェック_夜間バッチ処理】【並行2番目】　完了",
  "extracted_data": {
    "parallel_id": "2",
    "machine":     "本番1号機",
    "status":      "完了"
  }
}
```

> **匹配规则**：`re.search` + `IGNORECASE | MULTILINE`，有捕获组取第 1 组，无捕获组取整段匹配，未命中为 `null`。非法正则会优雅降级为 `null`，不抛异常。

### 3. 复合检索：主题 × 正文双维度

```json
{
  "subject_keywords": "监控,告警",
  "body_keywords":    "error,timeout,失败",
  "match_logic":      "OR"
}
```

含义：**主题** 含 `监控`/`告警` 之一 **且** **正文** 含 `error`/`timeout`/`失败` 之一。

- **组内**逻辑由 `match_logic` 控制（`AND` 全部命中 / `OR` 任一命中）。
- **组间**（主题 vs 正文）固定为 `AND`。
- 空组视为恒真，不参与过滤。

### 4. 推送到钉钉 / 飞书 / Telegram

```json
{
  "push_platform": "dingtalk",
  "webhook_url":   "https://oapi.dingtalk.com/robot/send?access_token=xxx",
  "push_secret":   "SECxxxxxxxxxxxxxxx"
}
```

| 平台 | `push_platform` | `webhook_url` | `push_secret` |
|---|---|---|---|
| 钉钉 | `dingtalk` | 群机器人 Webhook | 加签密钥（`SEC...`，可选） |
| 飞书 | `feishu` | 群机器人 Webhook | 签名密钥（可选） |
| Telegram | `tg` | `https://api.telegram.org/bot<TOKEN>/sendMessage` | 目标 `chat_id` |

推送消息自动渲染为 Markdown / 交互式卡片，并携带 `extracted_data` 字段。

---

## ⏰ 定时跑批部署

内置 `setup_cron.sh` 将本 Skill 一键注册为 Linux 系统级 Cron 任务。

### 使用方式

```bash
chmod +x setup_cron.sh

# 1. 导出所有需要的 SKILL_* 环境变量（支持继承外部的 Webhook 配置）
export SKILL_EMAIL_ACCOUNT="you@example.com"
export SKILL_AUTH_PASSWORD="your-auth-code"
export SKILL_PROVIDER="qq"
export SKILL_SUBJECT_KEYWORDS="【SEO順位チェック_夜間バッチ処理】"
export SKILL_EXTRACT_PATTERNS='{"status":"(成功|失敗|完了)"}'

# —— 推送配置直接从外部继承 ——
export SKILL_PUSH_PLATFORM="dingtalk"
export SKILL_WEBHOOK_URL="$DINGTALK_WEBHOOK"
export SKILL_PUSH_SECRET="$DINGTALK_SECRET"

# 2. 一条命令注册（每天 09:00 跑，日志追加到 /var/log/mail-pipeline.log）
./setup_cron.sh "0 9 * * *" /var/log/mail-pipeline.log
```

### 脚本行为

- 将当前所有 `SKILL_*` 环境变量固化到脚本同目录的 `.env`（权限 `600`，保护敏感信息）。
- 追加带标签 `# imap-mail-pipeline` 的 crontab 条目；**重复执行会幂等替换**旧条目，不会产生重复任务。
- cron 触发时自动 `source .env`，再执行 `python3 main.py`，stdout/stderr 追加到指定日志文件。

### 常用 Cron 表达式

| 表达式 | 含义 |
|---|---|
| `0 9 * * *` | 每天 09:00 |
| `*/30 * * * *` | 每 30 分钟 |
| `0 9,18 * * 1-5` | 工作日早 9 晚 6 |
| `0 */2 * * *` | 每 2 小时整点 |

### 💡 定时任务的时间窗语义

**强烈建议在定时场景下不要设置 `start_datetime` / `end_datetime`**，让其默认为"过去 24 小时"。

这样每次触发都是一个**滚动窗口**：
- 今天 9:00 跑 → 覆盖昨天 9:00 至今天 9:00
- 明天 9:00 跑 → 覆盖今天 9:00 至明天 9:00

如果固定写死绝对时间，反而会让每次任务都查同一段历史——这几乎肯定不是你想要的。

### 查看与移除

```bash
crontab -l                                            # 查看所有任务
crontab -l | grep -v imap-mail-pipeline | crontab -   # 移除本 Skill 的任务
```

---

## 📖 更多文档

完整的参数表、返回字段定义、版本迁移指南、**机器号 × 并行号复合状态汇总**的高级 Prompt 示例，请看 [skill.md](./skill.md)。

---

## 🤝 贡献

欢迎提交 Issue 与 PR！以下方向尤其欢迎：

- 新增更多邮箱服务商的路由（在 `reader.py` 的 `PROVIDER_ROUTES` 字典中添加）。
- 新增更多推送平台（在 `pusher.py` 中按 `push_dingtalk` 模式添加）。
- 更多归一化字符覆盖（在 `_NORMALIZE_PATTERN` 中扩展）。

提交前请确保：
- 无第三方依赖（保持 `requirements.txt` 为空）。
- 通过 `python -m py_compile` 语法检查。

---

## 📜 License

MIT License — 欢迎商用与二次分发。
