---
name: outlook
emoji: f4e7
description: Microsoft Outlook/Live.com email and calendar client via Microsoft Graph API. List, search, read, send emails. View and create calendar events. Supports device code auth for servers.
license: MIT
compatibility: [openclaw, openclaw-cli, openclaw-web, claude-desktop, claude-api, claude-cli]
allowed-tools: [Bash, Read, Write, Python]
network_access: true
metadata:
  {
    "openclaw":
      {
        "emoji": "📧",
        "requires": { "bins": ["python3"], "python_packages": ["requests"] },
        "install":
          [
            {
              "id": "manual",
              "kind": "manual",
              "label": "Requires Azure AD app registration",
            },
          ],
      },
    "execution":
      {
        "type": "python-script",
        "interpreter": "python3",
        "main": "./outlook",
        "description": "All operations execute through Python script that calls Microsoft Graph API",
      },
    "security":
      {
        "network": "Performs HTTPS API calls to Microsoft Graph API (graph.microsoft.com) for email and calendar operations",
        "authentication": "Requires OAuth 2.0 device code flow authentication",
        "data_storage": "Stores OAuth tokens locally in ~/.config/outlook-cli/token.json",
      },
  }
---
# Outlook CLI

Command-line email and calendar client for Microsoft Outlook/Live/Hotmail using Microsoft Graph API.

**Version**: 2.0

**Features**:
- 📧 Email management (list, search, read, send, reply)
- 📅 Calendar management (view, create events)
- 🔐 Device code authentication (for servers/headless environments)
- ⚡ Auto token refresh

## System Requirements & Permissions

**Required Tools**:
- `Bash`: Execute Python CLI script
- `Read`: Read token and configuration files
- `Write`: Store OAuth tokens and settings

**Network Access**:
- ✅ This skill makes HTTPS API calls to **Microsoft Graph API** (`graph.microsoft.com`)
- ✅ Requires internet connection for all operations
- ✅ Uses Python `requests` library for HTTP communications

**Data Storage**:
- OAuth tokens stored at: `~/.config/outlook-cli/token.json` (requires file permission 600)
- No email content is stored locally (all operations via API)

**Python Dependencies**:
- Python 3.6+
- `requests` library

## Setup

> ⚠️ **安全提示**:
> - 请**仅从官方 Microsoft Azure 门户** (https://portal.azure.com) 创建应用并获取凭据
> - **切勿使用**来自非官方渠道、第三方网站或他人分享的凭据
> - Client ID 和 Tenant ID 可以公开，但 **Client Secret 必须保密**
> - 定期审查和轮换凭据以提高安全性
> - 仅授予必需的最小权限（遵循最小权限原则）

1. **Create Azure AD App:** https://portal.azure.com → App registrations
   - Name: `outlook-cli`
   - Account type: "Any organizational directory and personal Microsoft accounts"
   - Redirect URI: `http://localhost:8080/callback`
   - Enable public client flows: Yes

2. **Add API permissions** (Microsoft Graph, Delegated):
   - `Mail.Read`, `Mail.ReadWrite`, `Mail.Send`
   - `Calendars.Read`, `Calendars.ReadWrite`
   - `User.Read`, `offline_access`

3. **Get credentials** from your app registration
   - ⚠️ **重要**: 确认你正在官方 Azure 门户 (portal.azure.com) 操作
   - 记录 Application (client) ID 和 Directory (tenant) ID

4. **Configure:**
   ```bash
   outlook configure
   ```

5. **Authenticate:**
   ```bash
   # For local environment with browser
   outlook auth

   # For servers/headless environments (recommended)
   outlook auth --device-code
   ```

6. **Secure token file (Critical!):**
   ```bash
   # Set restrictive permissions
   chmod 600 ~/.config/outlook-cli/token.json

   # Verify (should show: -rw-------)
   ls -l ~/.config/outlook-cli/token.json
   ```
   > ⚠️ **Important**: Never commit this file to version control or share it with others!

## Commands

### Email Commands

| Command | Description |
|---------|-------------|
| `outlook list [n]` | List recent emails |
| `outlook search "query" [n]` | Search emails |
| `outlook read <id>` | Read email by ID |
| `outlook send --to ...` | Send email |
| `outlook reply <id>` | Reply to email |
| `outlook status` | Check auth status |

### Calendar Commands 🆕

| Command | Description |
|---------|-------------|
| `outlook calendar list [--days N]` | List upcoming events |
| `outlook calendar create ...` | Create calendar event |

## Examples

### Email Operations

**List emails:**
```bash
outlook list 20
```

返回格式示例：
```
│ 序号 │           发件人           │             主题              │       日期       │  状态  │
├──────┼────────────────────────────┼───────────────────────────────┼──────────────────┼────────┤
│  1   │ user@example.com           │ 项目进展汇报                    │ 2026-03-19 10:30 │ 未读   │
│  2   │ admin@company.com          │ 周会通知                       │ 2026-03-19 09:15 │ ✓ 已读 │
│  3   │ noreply@service.com        │ 账户安全提醒                    │ 2026-03-18 18:20 │ 未读   │
```

**Search:**
```bash
outlook search "from:linkedin.com"
outlook search "subject:invoice"
outlook search "hasattachment:yes"
```

**Send:**
```bash
outlook send --to "user@example.com" --subject "Hello" --body "Message"
outlook send --to "a@x.com,b@x.com" --cc "boss@x.com" --subject "Update" --body-file ./msg.txt
```

**Reply:**
```bash
outlook reply EMAIL_ID --body "Thanks!"
outlook reply EMAIL_ID --all --body "Thanks everyone!"
```

### Calendar Operations 🆕

**View events:**
```bash
# Next 7 days (default)
outlook calendar list

# Next 14 days
outlook calendar list --days 14
```

**Create event:**
```bash
# Simple event
outlook calendar create \
  --subject "Team Meeting" \
  --date "2026-03-20" \
  --time "14:00" \
  --duration 60

# With attendees and location
outlook calendar create \
  --subject "Project Review" \
  --date "2026-03-21" \
  --time "10:00" \
  --duration 90 \
  --attendees "user1@example.com,user2@example.com" \
  --location "Conference Room A"
```

### Authentication 🆕

**Browser auth (local environment):**
```bash
outlook auth
```

**Device code auth (servers/headless):**
```bash
outlook auth --device-code
# Visit https://microsoft.com/devicelogin
# Enter the displayed code
```

## Search Operators

- `from:email@domain.com` - Sender
- `to:email@domain.com` - Recipient
- `subject:keyword` - Subject line
- `body:keyword` - Email body
- `received:YYYY-MM-DD` - Date
- `hasattachment:yes` - Has attachments

## Files

- `SKILL.md` - This documentation
- `outlook` - Main CLI script (Python)
- `README.md` - Full documentation

---

## Authentication & Token Management

**Token storage location:** `~/.config/outlook-cli/token.json`

> 🔐 **Security Warning - Token File Protection**:
> - This file contains **sensitive OAuth tokens** that grant access to your email and calendar
> - **NEVER share, commit to version control, or expose this file publicly**
> - Set restrictive file permissions immediately after first authentication:
>   ```bash
>   chmod 600 ~/.config/outlook-cli/token.json
>   ```
> - Verify permissions: `ls -l ~/.config/outlook-cli/token.json` should show `-rw-------`
> - Add to `.gitignore` if working in a git repository:
>   ```bash
>   echo ".config/outlook-cli/token.json" >> ~/.gitignore
>   ```
> - If the token file is accidentally exposed, **immediately revoke access** at:
>   https://account.microsoft.com/privacy/app-access → Remove outlook-cli app

**Token features:**
- ✅ Automatic token refresh
- ✅ No need to re-authenticate on restart
- ✅ Long-lived refresh tokens (up to 90 days)

**When re-authentication is required:**

| Scenario | Reason |
|----------|---------|
| Changed Microsoft password | Refresh token immediately invalidated |
| Token expired (>90 days) | Microsoft refresh token has limited lifetime |
| Manually revoked access | App permissions revoked in Microsoft account settings |
| Token file deleted | File loss requires re-authentication |

**Re-authentication:**
```bash
outlook auth --device-code
# Visit https://login.microsoft.com/device
# Enter the displayed code
```

---

## Common Issues

### Q: Token expired?
A: Run `outlook auth --device-code` to re-authenticate.

### Q: Token file accidentally exposed or committed to git?
A: **Immediate action required**:
1. Revoke access at https://account.microsoft.com/privacy/app-access
2. Delete the exposed token file: `rm ~/.config/outlook-cli/token.json`
3. Re-authenticate: `outlook auth --device-code`
4. Set proper permissions: `chmod 600 ~/.config/outlook-cli/token.json`
5. If committed to git, remove from history: `git filter-branch` or BFG Repo-Cleaner

### Q: How to create recurring meetings?
A: Use Microsoft Graph API's recurrence field, or create via Outlook web interface.

### Q: API rate limit?
A: Microsoft Graph API has daily limits. Wait 1-2 hours and retry.
