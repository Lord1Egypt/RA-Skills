# 邮件回复（路由 A · 个人邮箱）

在「查看原邮件」之后回复该信。策略：

1. **优先**：网页邮箱（`webmail_url`）— 打开原信后在邮箱网页点「回复」
2. **备选**：SMTP 系统内发送 — 与 IMAP **同账号密码**，另配 **`smtp_host`** / **`smtp_port`**

---

## 配置

与 IMAP 共用：

```json
{
  "email": "user@example.com",
  "email_password": "app-password",
  "imap_host": "imap.gmail.com",
  "smtp_host": "smtp.gmail.com",
  "smtp_port": 465
}
```

| 字段 | 说明 |
|------|------|
| `smtp_host` | SMTP 服务器；可省略，按 `imap_host` 自动推断 |
| `smtp_port` | 默认 `465`（SSL）或 Outlook `587`（STARTTLS） |
| `smtp_use_ssl` | 可选；`465` 默认 true |

常见对照：

| IMAP | SMTP | 端口 |
|------|------|------|
| imap.gmail.com | smtp.gmail.com | 465 |
| imap.qq.com | smtp.qq.com | 465 |
| imap.163.com | smtp.163.com | 465 |
| imap-mail.outlook.com | smtp-mail.outlook.com | 587 |

---

## 用户入口

### 预览页

`GET /mail/preview/{token}` 顶部：

- **在网页邮箱中回复** → `webmail_url`（须浏览器已登录邮箱）
- **或用 SMTP 回复** → `GET /mail/reply/{token}` 表单页

### 检索结果字段

`search` / `query-by-port` 除 `preview_url`、`webmail_url` 外，另有 **`reply_url`**：

```json
{
  "preview_url": "http://host:8765/mail/preview/abc...",
  "reply_url": "http://host:8765/mail/reply/abc...",
  "webmail_url": "https://mail.google.com/..."
}
```

---

## HTTP API

| 路径 | 说明 |
|------|------|
| `GET /mail/reply/{token}` | SMTP 回复表单页 |
| `GET /api/mail/reply-draft/{token}` | 回复草稿 JSON（to、subject、In-Reply-To） |
| `POST /api/mail/send-reply` | 发送（form 或 JSON） |

**POST 示例**（JSON）：

```json
{
  "preview_token": "32位hex",
  "body": "Thanks, please advise laycan.",
  "subject": "",
  "include_quote": true
}
```

成功响应含 `message_id`（新发件 Message-ID）。

---

## CLI

```bash
# 查看回复草稿（含 webmail 链接、SMTP 是否可用）
python scripts/mail_reply.py --token <preview_token> --draft-json

# SMTP 发送
python scripts/mail_reply.py --token <preview_token> --body "回复正文"

# 网页邮箱定位（不发送，只打开搜索页）
python scripts/webmail_locate.py --message-id "<id>" --from-addr "..." --open
```

---

## Agent 规则

1. 用户要「回复这封邮件」时：若有 **`webmail_url`**，先建议 **在网页邮箱中打开并回复**。
2. 用户要在智能体/租船页内直接发信，或网页邮箱不可用 → 检查 **`smtp_host`** 配置后走 **`reply_url`** 或 `mail_reply.py`。
3. SMTP 回复自动带 **`In-Reply-To`** / **`References`** / **`Re:` 主题**，尽量保持邮件会话。
4. 对用户说 **「回复邮件」**，不要说 SMTP/IMAP 术语（见 **`USER_WORDING.md`**）。

---

## 限制

- 无法在服务端替用户登录网页邮箱；网页回复依赖用户浏览器会话。
- 附件回复、HTML 富文本：当前 SMTP 路径为**纯文本**。
- 部分企业邮需应用专用密码；发信失败时检查 SMTP 端口与 SSL 设置。
