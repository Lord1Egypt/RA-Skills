# Microsoft Graph Skill — Setup Guide

This skill connects OpenClaw to your Microsoft 365 account (Outlook, Calendar) via the Microsoft Graph API.

## Prerequisites

- A Microsoft account (personal or work/school)
- Access to the [Azure Portal](https://portal.azure.com)

## Step 1: Register an Azure App

1. Go to [Azure Portal](https://portal.azure.com) → **Azure Active Directory** → **App registrations**
2. Click **New registration**
3. Name it something like `OpenClaw Assistant`
4. Under **Supported account types**, select:
   - **Personal Microsoft accounts only** (for Outlook.com, Hotmail, Live)
   - OR **Accounts in any organizational directory and personal accounts** (for work + personal)
5. Leave Redirect URI blank for now
6. Click **Register**

## Step 2: Configure the App

1. Note your **Application (client) ID** — you'll need this later
2. Go to **Authentication** → **Add a platform** → **Single-page application**
3. Add this redirect URI: `http://localhost/msgraph-skill.html`
4. Under **Implicit grant and hybrid flows**, leave everything **unchecked** (PKCE handles this)
5. Click **Save**

## Step 3: Set Required Permissions

1. Go to **API permissions** → **Add a permission** → **Microsoft Graph**
2. Select **Delegated permissions** and add:
   - `Mail.Read`
   - `Mail.ReadWrite`
   - `Calendars.Read`
   - `Calendars.ReadWrite`
   - `User.Read`
3. Click **Add permissions** (no admin consent needed for personal accounts)

## Step 4: Configure the Skill

Copy `config.example.ini` to `config.ini` and set your Client ID:

```ini
[msgraph]
CLIENT_ID = YOUR_CLIENT_ID_HERE
tenant = consumers
scopes = Mail.ReadWrite Calendars.ReadWrite offline_access User.Read
redirect_port = 8765
```

**Note:** The redirect URI uses `http://localhost:8765/` — make sure this matches the port in your config.

## Step 5: Authenticate

The first time you ask Dae to access your email or calendar, she'll walk you through the authentication flow. You'll authenticate once and the token is stored securely in your OpenClaw credentials directory.

## Folder Structure

Your Outlook folders are respected as-is. Tell Dae how you organize your inbox and she'll learn your system over time. Example:

> "Keep open loops in inbox, move travel stuff to Events/[trip name], receipts go to eReceipts"

## Troubleshooting

### Auth errors

**Error: "Not authenticated. Run: python auth.py login"**

- Run `python scripts/auth.py login`
- Browser window should open automatically
- If browser doesn't open on WSL2, copy the printed URL and paste in your browser
- Complete the login flow and return to terminal

**Error: "401 Unauthorized" on API calls**

- Token has expired or isn't being refreshed
- Run `python scripts/auth.py refresh` to force refresh
- If that fails, re-authenticate: `python scripts/auth.py login`

**Error: "Token file not found"**

- Tokens stored in `~/.openclaw/msgraph-tokens.json`
- Run `python scripts/auth.py login` to create the token file
- On Windows, this is typically: `C:\Users\<username>\.openclaw\msgraph-tokens.json`

### Permission errors

**Error: "403 Forbidden" or "Insufficient privileges"**

- Check Azure Portal → your app → **API permissions**
- Verify all scopes are added:
  - `Mail.Read`, `Mail.ReadWrite`
  - `Calendars.Read`, `Calendars.ReadWrite`
  - `User.Read`
- **For work accounts**: Admin may need to grant consent
- After adding permissions, re-authenticate: `python scripts/auth.py login`

**Error: "Invalid scopes"**

- Check `config.ini` scopes match Azure Portal permissions
- Remove extra/custom scopes — use only the 5 above

### Configuration issues

**Error: "config.ini not found"**

- Run: `cp config.example.ini config.ini`
- Edit `config.ini` and set your Client ID from Azure Portal
- Don't commit `config.ini` to git (already in `.gitignore`)

**Error: "client_id" vs "CLIENT_ID" mismatch**

- Make sure config.ini uses UPPERCASE: `CLIENT_ID = ...`
- Python script reads this as `cfg["CLIENT_ID"]`

**Wrong tenant/scope mismatch**

- For **personal Microsoft accounts** (Outlook.com, Hotmail, Live.com):
  - `tenant = consumers`
- For **work accounts** (Microsoft 365):
  - `tenant = organizations` OR `tenant = <your-tenant-id>`
  - Admin consent may be required

### Platform-specific issues

**WSL2: Browser doesn't open**

- Script tries `cmd.exe /c start URL` first
- If that fails, it prints the URL
- Manually open browser and paste the full redirect URL
- Ensure you're using Windows browser (not WSL terminal)

**macOS: "Permission denied" on token file**

- Check `~/.openclaw/` permissions:
  ```bash
  chmod 700 ~/.openclaw
  chmod 600 ~/.openclaw/msgraph-tokens.json
  ```

**Linux: "Address already in use" on redirect port**

- If port 8765 is busy, change in `config.ini`:
  ```ini
  redirect_port = 8766
  ```
- Also update Azure Portal redirect URI: `http://localhost:8766/`

### Email/Calendar operations

**Error: "404 Not Found" on message/event**

- Message or event ID may be invalid
- Double-check the ID from `inbox` or `list` command output

**Error: Message not found in folder**

- Folder name resolution is case-insensitive
- Try well-known folders: `inbox`, `drafts`, `sentitems`, `deleteditems`, `junk`, `archive`
- For custom folders, use exact display name: `python scripts/mail.py folders` to list

**Calendar event creation fails with 400**

- Check date/time format: `YYYY-MM-DDTHH:MM`
- Make sure start time is before end time
- Attendee email addresses must be valid

**HTML in email looks mangled**

- Script strips HTML automatically
- Some complex formatting may not render perfectly in plain text
- This is expected behavior

### General debugging

**Enable debug output:**

```bash
export DEBUG=1
python scripts/auth.py login
```

**Check token contents:**

```bash
python scripts/auth.py token
```

**Test API connectivity:**

```bash
python scripts/cal.py list
# Or
python scripts/mail.py inbox --count 1
```

**Check your Python version:**

```bash
python --version  # Should be 3.7+
```

## FAQ

### Q: Is my password/credentials stored locally?

**A:** No. Only OAuth tokens are stored in `~/.openclaw/msgraph-tokens.json`. Your Microsoft password is never touched by this script. You authenticate directly with Microsoft servers.

### Q: Can I use this on both personal and work accounts?

**A:** Yes, but you need separate Client IDs and apps in Azure Portal:

- Create one app with "Personal accounts only" for Outlook.com
- Create another app with "Work/School accounts" for Microsoft 365
- Use separate `config.ini` files or swap CLIENT_ID when needed

### Q: How often do tokens refresh?

**A:** Access tokens last ~1 hour. When expired, the script automatically exchanges the refresh token for a new one. The refresh token lasts ~90 days.

### Q: What happens after 90 days?

**A:** Refresh token expires. Run `python scripts/auth.py login` again to get new tokens. No data is lost.

### Q: Can I share my client ID?

**A:** Yes, the Client ID is public. Never share your access/refresh tokens. Keep `config.ini` and `~/.openclaw/` private.

### Q: Does this work offline?

**A:** No. This skill requires internet to authenticate and call the Microsoft Graph API. Consider caching email/calendar locally if you need offline support.

### Q: Can I move emails between accounts?

**A:** No. The skill only accesses the authenticated account. To access multiple accounts, you'd need multiple Client IDs and separate authentication.

### Q: Does this delete emails?

**A:** No. The skill only:

- Reads: `Mail.Read`, `Calendars.Read`
- Modifies: `Mail.ReadWrite`, `Calendars.ReadWrite` (move, create events)
- Never deletes — use Outlook UI for that

### Q: How do I revoke access if needed?

**A:**

```bash
# Remove local token
rm ~/.openclaw/msgraph-tokens.json

# (Optional) Revoke in Azure Portal:
# 1. Go to Account settings → Security & privacy → Apps & services
# 2. Find "OpenClaw" and remove
```

### Q: Can I use this without OpenClaw?

**A:** Yes! The scripts work standalone:

```bash
python scripts/auth.py login
python scripts/mail.py inbox
python scripts/cal.py list
```

You can integrate them into any Python project. See `examples/` for patterns.

### Q: What if I get "Invalid request" errors?

**A:**

- Check internet connection
- Verify Client ID is correct (copy from Azure Portal)
- Make sure no special characters in scopes
- Try deleting tokens and re-authenticating
- Check Azure Portal for any restrictions on the app

### Q: Can I test without connecting to Microsoft?

**A:** Yes, the project includes 114 tests that mock the Graph API:

```bash
pip install -r requirements-test.txt
python -m pytest tests/ -v
```

### Q: How long do these tokens last?

**A:**

- **Access token**: ~1 hour (auto-refreshes)
- **Refresh token**: ~90 days (auto-refreshes)
- **Skill remembers**: You don't need to log in again for 90 days

### Q: Will this work with Teams, OneDrive, SharePoint email?

**A:** Teams and OneDrive won't work (different APIs). SharePoint email would need different scopes. The skill focuses on personal Outlook & Calendar, which works great.

### Q: How do I report bugs?

**A:** See [CONTRIBUTING.md](../CONTRIBUTING.md) for bug report guidelines. Include:

- Python version
- OS (Windows/Mac/Linux)
- Steps to reproduce
- Full error message
- Your config.ini scopes (don't share Client ID)
