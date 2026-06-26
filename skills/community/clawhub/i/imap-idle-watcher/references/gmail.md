# Gmail Setup

## Prerequisites
- Google account with 2-Step Verification enabled

## Create App Password

1. Go to: https://myaccount.google.com/apppasswords
2. Sign in if prompted
3. Under "App name", type any label (e.g. "IMAP Watcher")
4. Click **Create**
5. Copy the 16-character password (spaces don't matter)

## If App Passwords page is missing
- 2FA is not enabled → enable at https://myaccount.google.com/signinoptions/two-step-verification
- Using a Workspace account → admin may have disabled app passwords

## Enable IMAP (usually already on)
1. Gmail → Settings → See all settings → Forwarding and POP/IMAP
2. IMAP access: **Enabled**

## Connection details
| Setting | Value |
|---------|-------|
| Host | `imap.gmail.com` |
| Port | `993` |
| SSL | Yes (required) |
