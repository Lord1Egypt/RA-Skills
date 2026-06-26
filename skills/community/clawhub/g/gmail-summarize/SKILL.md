---
name: gmail-summarize
description: Fetch recent unread Gmail (yesterday + today) and send a digest to the user.
metadata: {
  "skill": {
    "emoji": "📬",
    "requires": {
      "runtime": "python3",
      "env_vars": {
        "required": ["IMAP_USERNAME", "IMAP_PASSWORD"],
        "optional": ["IMAP_HOST", "IMAP_PORT", "IMAP_MAX_BODY_CHARS", "EMAIL_CONFIG_PATH"]
      },
      "credentials": [
        "IMAP_USERNAME (env, required) — IMAP login username",
        "IMAP_PASSWORD (env, required) — IMAP login password / app-password",
        "IMAP_HOST    (env, optional, default: imap.gmail.com)",
        "IMAP_PORT    (env, optional, default: 993)"
      ],
      "config": "$EMAIL_CONFIG_PATH or ~/.config/gmail-summarize/config.json (used only when IMAP_USERNAME/IMAP_PASSWORD env vars are absent)",
      "config_fields": ["email.imapHost", "email.imapPort", "email.imapUsername", "email.imapPassword"],
      "external_connections": ["IMAP server specified in IMAP_HOST or email.imapHost"]
    }
  }
}
---

# Gmail Recent Digest

## Requirements
- **Python 3** must be available in the container environment (`python` command).
- IMAP credentials must be supplied via **one** of the following methods (env vars take precedence):

### Option A — Environment variables (recommended)

| Variable | Description | Default |
|---|---|---|
| `IMAP_HOST` | IMAP server hostname | `imap.gmail.com` |
| `IMAP_PORT` | IMAP server port | `993` |
| `IMAP_USERNAME` | IMAP login username | *(required)* |
| `IMAP_PASSWORD` | IMAP login password / app-password | *(required)* |
| `IMAP_MAX_BODY_CHARS` | Max body characters per email | `2000` |

### Option B — Config file

Set `EMAIL_CONFIG_PATH` to point to a JSON file, or place the file at `~/.config/gmail-summarize/config.json`.
The file must contain **only** the fields below (no other sensitive data should be stored in this file):

```json
{
  "email": {
    "imapHost": "imap.gmail.com",
    "imapPort": 993,
    "imapUsername": "your@gmail.com",
    "imapPassword": "your-app-password",
    "maxBodyChars": 2000
  }
}
```

## Security notes
- **Preferred**: supply credentials via environment variables (`IMAP_HOST`, `IMAP_PORT`, `IMAP_USERNAME`, `IMAP_PASSWORD`) so no file on disk is read at all.
- When a config file is used, it should contain **only** the `email` fields listed above. The script reads only those four fields and nothing else from the file.
- The only external connection made is to the IMAP server declared in `IMAP_HOST` / `email.imapHost`. No other endpoints are contacted.
- Credentials are used solely to authenticate the IMAP session and are not logged or stored elsewhere by this skill.

## When to use
- User asks "check my Gmail", "summarize my emails", "邮件摘要"
- Cron trigger message contains "gmail_digest"

## Workflow
1. Run the fetch script via exec tool:
   `python {workspace}/skills/gmail-summarize/scripts/fetch_unseen.py`
   (replace {workspace} with your actual workspace root)
2. Parse the JSON array. Each item has: sender, subject, date, body
3. For each email compose one line:
   `[date] sender | subject — one-sentence body summary`
4. Send the full digest via MessageTool in this format:

   📬 **邮件摘要** (N封，覆盖 MM/DD–MM/DD)

   • [日期] 发件人 | 主题 — 一句话摘要
   • [日期] 发件人 | 主题 — 一句话摘要
   ...

5. If result is empty, send: 📭 近两日暂无未读邮件

## Output Rules
- Send the digest message ONLY. Do NOT add any extra comments, greetings, explanations, or follow-up questions before or after the digest.
- Do NOT say things like "主人，以下是您的邮件摘要" or "如需了解详情请告知" etc.
- The digest message itself is the complete and final response.
- The one-sentence body summary MUST be translated into Chinese. Sender names and subjects should keep their original text as-is.
