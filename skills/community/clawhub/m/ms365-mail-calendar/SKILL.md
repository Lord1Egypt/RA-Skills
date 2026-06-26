---
name: ms365
description: Microsoft 365 Email & Calendar CLI via Microsoft Graph API. Supports multiple accounts.
metadata: {"openclaw":{"emoji":"🟦","requires":{"bins":["node"],"env":["MICROSOFT_CLIENT_ID"]}}}
---

# ms365

Microsoft 365 CLI for Email & Calendar via Graph API. Multi-account support.

## Setup (once per account)
1. Register app in Azure Portal → App registrations → New → Public client (mobile & desktop)
2. Enable "Allow public client flows" (Device Code Flow)
3. API permissions: `Mail.Read`, `Mail.Send`, `Calendars.ReadWrite`, `User.Read`
4. Set env: `MICROSOFT_CLIENT_ID=<your-app-id>` and optionally `MICROSOFT_TENANT_ID`
5. Run: `node skills/ms365/index.js --account work login`

## Commands
- Login: `node index.js --account work login`
- Who am I: `node index.js --account work whoami`
- Inbox: `node index.js --account work mail inbox --top 10`
- Unread: `node index.js --account work mail unread`
- Read: `node index.js --account work mail read <id>`
- Send: `node index.js --account work mail send --to a@b.com --subject "Hi" --body "Hello"`
- Search: `node index.js --account work mail search "invoice"`
- Calendar: `node index.js --account work calendar --from 2026-04-14T00:00:00Z --to 2026-04-14T23:59:59Z`
- Create event: `node index.js --account work calendar-create --subject "Meeting" --start 2026-04-15T10:00 --end 2026-04-15T11:00`

## Multi-account
Use `--account <name>` to switch. Each account has separate tokens stored in `~/.openclaw/credentials/`.

## Notes
- Device Code Flow — authenticate in browser, no secrets stored
- Tokens auto-refresh
- Confirm before sending emails
