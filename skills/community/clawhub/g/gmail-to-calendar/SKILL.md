---
name: gmail-to-calendar
description: |
  Promote schedule details from Gmail into Google Calendar via Maton. Reads Gmail messages, extracts structured or free-text event information, and creates Google Calendar events. Also includes Gmail API reference and helper workflows for listing and reading messages. Use when users want to turn email scheduling details into calendar events, import meeting details from Gmail, or work with Gmail message data before creating Google Calendar entries.
compatibility: Requires network access and valid Maton API key
metadata:
  author: orulink
  version: "1.0"
  openclaw:
    requires:
      env:
        - MATON_API_KEY
---

# Gmail To Calendar

> **Skill 初始化规则：** 使用此 skill 前，需检查 skill 目录下是否存在 `.env` 文件保存 `MATON_API_KEY`。如果不存在，提示用户提供 API key 并创建 `.env` 文件后，再执行后续操作。

Access the Gmail API with managed OAuth authentication. Read, send, and manage emails, threads, labels, and drafts.

This skill also includes a bundled helper script, `gmail_to_calendar.py`, for a tested Gmail -> Google Calendar workflow. Use it when an email contains schedule details and you want to create a calendar event through the same Maton account.

## .env 文件说明

API Key 保存在 skill 目录的 `.env` 文件中（**不要提交到 Git**）。首次使用前需要创建：

```bash
# 在 skill 目录下创建 .env 文件
echo "MATON_API_KEY=你的API密钥" > ~/.openclaw/workspace/skills/gmail-to-calendar/.env
```

所有 exec 调用会自动从该文件加载环境变量（通过 `set -a; source ~/.openclaw/workspace/skills/gmail-to-calendar/.env; set +a`）。

## Quick Start

```bash
# 自动从 .env 加载环境变量后，列出邮件
set -a; source ~/.openclaw/workspace/skills/gmail-to-calendar/.env; set +a
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/google-mail/gmail/v1/users/me/messages?maxResults=10')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Base URL

```
https://gateway.maton.ai/google-mail/{native-api-path}
```

Replace `{native-api-path}` with the actual Gmail API endpoint path. The gateway proxies requests to `gmail.googleapis.com` and automatically injects your OAuth token.

## Authentication

All requests require the Maton API key in the Authorization header:

```
Authorization: Bearer $MATON_API_KEY
```

**Environment Variable:** API key 已保存在 skill 目录的 `.env` 文件中（见上方说明）。在 exec 调用中，通过以下方式加载：

```bash
set -a; source ~/.openclaw/workspace/skills/gmail-to-calendar/.env; set +a
```

### Getting Your API Key

1. Sign in or create an account at [maton.ai](https://maton.ai)
2. Go to [maton.ai/settings](https://maton.ai/settings)
3. Copy your API key
4. 将 API key 写入 `~/.openclaw/workspace/skills/gmail-to-calendar/.env` 文件（格式：`MATON_API_KEY=你的密钥`）

## Connection Management

Manage your Google OAuth connections at `https://ctrl.maton.ai`.

### List Connections

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=google-mail&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Create Connection

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'google-mail'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Get Connection

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**Response:**
```json
{
  "connection": {
    "connection_id": "21fd90f9-5935-43cd-b6c8-bde9d915ca80",
    "status": "ACTIVE",
    "creation_time": "2025-12-08T07:20:53.488460Z",
    "last_updated_time": "2026-01-31T20:03:32.593153Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "google-mail",
    "metadata": {}
  }
}
```

Open the returned `url` in a browser to complete OAuth authorization.

### Delete Connection

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Specifying Connection

If you have multiple Gmail connections, specify which one to use with the `Maton-Connection` header:

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/google-mail/gmail/v1/users/me/messages')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

If omitted, the gateway uses the default (oldest) active connection.

## Gmail -> Google Calendar

This workflow requires both of the following Maton connections to be ACTIVE:

- `google-mail`
- `google-calendar`

Use the bundled helper script when the email body includes either structured event fields or recognizable free-text schedule details. The script:

1. Reads a Gmail message by `--message-id` or Gmail search `--query`
2. Extracts event details from explicit fields first, then falls back to free-text parsing
3. Creates an event in Google Calendar

Supported field labels in the email body:

- Summary: `Title`, `Summary`, `标题`, `主题`
- Date: `Date`, `日期`
- Start time: `Start`, `Start Time`, `开始`, `开始时间`
- End time: `End`, `End Time`, `结束`, `结束时间`
- Time zone: `Time Zone`, `Timezone`, `时区`
- Location: `Location`, `地点`
- Description: `Description`, `Details`, `描述`, `详情`

Recommended email format:

```text
Title: Product Sync
Date: 2026-04-21
Start: 15:00
End: 15:30
Time Zone: Asia/Shanghai
Location: Zoom
Description: Weekly review with the product team.
```

Supported free-text patterns include:

- Absolute dates: `2026-04-25 15:00-16:00`, `2026年4月25日下午3点到4点`
- Relative dates: `tomorrow 3pm-4pm`, `明天下午 3 点到 4 点`
- Weekdays: `next Tuesday 2pm`, `下周三上午10点`
- Meeting locations: `on Google Meet`, `在 Zoom`, or a meeting URL such as `https://meet.google.com/...`

Example free-text email body:

```text
我们约在2026年4月25日下午3点到4点，在 Zoom 讨论项目里程碑。
```

Another example:

```text
Let's meet tomorrow 3pm-3:45pm on Google Meet to discuss the role.
```

The script loads `MATON_API_KEY` from the local `.env` file automatically.

Dry run without writing to Google Calendar:

```bash
python ~/.openclaw/workspace/skills/gmail-to-calendar/gmail_to_calendar.py \
  --query 'subject:"面试安排" newer_than:7d' \
  --dry-run
```

Keep the old strict behavior and disable free-text fallback:

```bash
python ~/.openclaw/workspace/skills/gmail-to-calendar/gmail_to_calendar.py \
  --query 'subject:"面试安排" newer_than:7d' \
  --structured-only
```

Create an event from a specific Gmail message:

```bash
python ~/.openclaw/workspace/skills/gmail-to-calendar/gmail_to_calendar.py \
  --message-id 19da9b349a1016c8
```

Pin specific Maton connections if multiple Gmail or Google Calendar accounts are active:

```bash
python ~/.openclaw/workspace/skills/gmail-to-calendar/gmail_to_calendar.py \
  --query 'subject:"[TEST] Maton Gmail->Calendar"' \
  --mail-connection e7eb1207-4f81-43f8-8aaf-2a483b3b48b7 \
  --calendar-connection a40e0d20-4f6d-4461-8db0-877ed581627e
```

The underlying calendar write uses the Google Calendar Maton gateway:

```bash
POST /google-calendar/calendar/v3/calendars/primary/events
```

## API Reference

### List Messages

```bash
GET /google-mail/gmail/v1/users/me/messages?maxResults=10
```

With query filter:

```bash
GET /google-mail/gmail/v1/users/me/messages?q=is:unread&maxResults=10
```

### Get Message

```bash
GET /google-mail/gmail/v1/users/me/messages/{messageId}
```

With metadata only:

```bash
GET /google-mail/gmail/v1/users/me/messages/{messageId}?format=metadata&metadataHeaders=From&metadataHeaders=Subject&metadataHeaders=Date
```

### Send Message

```bash
POST /google-mail/gmail/v1/users/me/messages/send
Content-Type: application/json

{
  "raw": "BASE64_ENCODED_EMAIL"
}
```

### List Labels

```bash
GET /google-mail/gmail/v1/users/me/labels
```

### List Threads

```bash
GET /google-mail/gmail/v1/users/me/threads?maxResults=10
```

### Get Thread

```bash
GET /google-mail/gmail/v1/users/me/threads/{threadId}
```

### Modify Message Labels

```bash
POST /google-mail/gmail/v1/users/me/messages/{messageId}/modify
Content-Type: application/json

{
  "addLabelIds": ["STARRED"],
  "removeLabelIds": ["UNREAD"]
}
```

### Trash Message

```bash
POST /google-mail/gmail/v1/users/me/messages/{messageId}/trash
```

### Create Draft

```bash
POST /google-mail/gmail/v1/users/me/drafts
Content-Type: application/json

{
  "message": {
    "raw": "BASE64URL_ENCODED_EMAIL"
  }
}
```

### Send Draft

```bash
POST /google-mail/gmail/v1/users/me/drafts/send
Content-Type: application/json

{
  "id": "{draftId}"
}
```

### Get Profile

```bash
GET /google-mail/gmail/v1/users/me/profile
```

## Query Operators

Use in the `q` parameter:
- `is:unread` - Unread messages
- `is:starred` - Starred messages
- `from:email@example.com` - From specific sender
- `to:email@example.com` - To specific recipient
- `subject:keyword` - Subject contains keyword
- `after:2024/01/01` - After date
- `before:2024/12/31` - Before date
- `has:attachment` - Has attachments

## Code Examples

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/google-mail/gmail/v1/users/me/messages?maxResults=10',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
```

### Python

```python
import os
import requests

response = requests.get(
    'https://gateway.maton.ai/google-mail/gmail/v1/users/me/messages',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'maxResults': 10, 'q': 'is:unread'}
)
```

## Notes

- Use `me` as userId for the authenticated user
- Message body is base64url encoded in the `raw` field
- Common labels: `INBOX`, `SENT`, `DRAFT`, `STARRED`, `UNREAD`, `TRASH`
- IMPORTANT: When using curl commands, use `curl -g` when URLs contain brackets (`fields[]`, `sort[]`, `records[]`) to disable glob parsing
- IMPORTANT: When piping curl output to `jq` or other commands, environment variables like `$MATON_API_KEY` may not expand correctly in some shell environments. You may get "Invalid API key" errors when piping.

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Missing Gmail connection |
| 401 | Invalid or missing Maton API key |
| 429 | Rate limited (10 req/sec per account) |
| 4xx/5xx | Passthrough error from Gmail API |

### Troubleshooting: API Key Issues

1. 检查 `.env` 文件是否存在且包含有效密钥：

```bash
cat ~/.openclaw/workspace/skills/gmail-to-calendar/.env
```

2. Verify the API key is valid by listing connections:

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Troubleshooting: Invalid App Name

1. Ensure your URL path starts with `google-mail`. For example:

- Correct: `https://gateway.maton.ai/google-mail/gmail/v1/users/me/messages`
- Incorrect: `https://gateway.maton.ai/gmail/v1/users/me/messages`

## Resources

- [Gmail API Overview](https://developers.google.com/gmail/api/reference/rest)
- [List Messages](https://developers.google.com/gmail/api/reference/rest/v1/users.messages/list)
- [Get Message](https://developers.google.com/gmail/api/reference/rest/v1/users.messages/get)
- [Send Message](https://developers.google.com/gmail/api/reference/rest/v1/users.messages/send)
- [List Threads](https://developers.google.com/gmail/api/reference/rest/v1/users.threads/list)
- [List Labels](https://developers.google.com/gmail/api/reference/rest/v1/users.labels/list)
- [Create Draft](https://developers.google.com/gmail/api/reference/rest/v1/users.drafts/create)
- [Maton Community](https://discord.com/invite/dBfFAcefs2)
- [Maton Support](mailto:support@maton.ai)
