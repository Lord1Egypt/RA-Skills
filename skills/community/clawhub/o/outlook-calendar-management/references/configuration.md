# Connecting to Your Calendar for the First Time

This toolkit operates your calendar through the Microsoft Graph API (Microsoft's official interface). You need to sign in and authorize once before first use (a one-time step; the login renews automatically afterwards).
Prerequisites: Python 3.10+; the dependencies requests/msal/tzdata are installed automatically on first run.

## Connection steps (about 2 minutes)

Run from the project root; missing dependencies are installed automatically.

```bash
python scripts/outlook_setup.py   # no arguments = built-in default app
```

1. The script prints a **verification code**
2. Open `https://www.microsoft.com/link` in a browser and enter the code
3. Sign in with your Outlook account (Microsoft account) and authorize. Three permissions are requested, each with its own purpose:

| Permission | Official description | Use in this toolkit |
|------------|----------------------|---------------------|
| `Calendars.ReadWrite` | Have full access to user calendars | All event operations: view, add, modify, move, delete (via `/me/events`, `/me/calendar*`) |
| `MailboxSettings.Read` | Read user mailbox settings | Reads the mailbox's preferred timezone (`/me/mailboxSettings`); all-day events are written in it, so they never span two days even when the machine timezone differs |
| `User.Read` | Sign in and read user profile | Base permission of the device-code sign-in: returns the signed-in user's identity (name, email); `status` shows the current account |

> The three are independent and non-interchangeable: `User.Read` reads "who the user is" (identity profile, required for sign-in); `MailboxSettings.Read` reads "what the mailbox is configured with" (timezone, language preferences - this is what the toolkit uses for the timezone); `Calendars.ReadWrite` reads/writes "the event content".
4. Done - the login renews automatically while the stored authorization remains valid; reconnect if it expires or is revoked

> When upgrading from an older version, re-run `python scripts/outlook_setup.py` once to add the `MailboxSettings.Read` permission (a new consent item will appear).

**To confirm success**: `python scripts/outlook_cal.py status` shows "✅ Connected to Outlook calendar".

> Your phone, computer, and web show the same calendar - all operations sync in real time after connecting.

## Switching accounts / reconnecting

Re-run `python scripts/outlook_setup.py` to authorize with another account (overwrites the current connection).
Do the same when the login expires (reports invalid_grant / 401).

## Want to use your own Azure app?

The built-in default app works out of the box; usually nothing to do. If you want to register your own app (e.g. for security isolation), see `azure-app-setup.md`.
After registration you only need to copy one parameter - the **Client ID**: `python scripts/outlook_setup.py <your Client ID>`.

## Separate test login

Set `OCAL_TOKEN_PATH` to a separate credential file before running both setup and calendar commands. The parent directory must exist. The same setting must remain present for the integration runner, whose subprocesses inherit it. Without this setting the tool uses `~/.outlook_cal_token.json`.

PowerShell example from the project root:

```powershell
New-Item -ItemType Directory -Force .local-calendar-test | Out-Null
$env:OCAL_TOKEN_PATH = Join-Path (Get-Location) '.local-calendar-test/outlook-token.json'
python scripts/outlook_setup.py
python scripts/outlook_cal.py status --json
```

This directory is ignored by Git. A separate credential file preserves the usual login, but it does not create a separate calendar: sign in with the intended test account and verify its email before test writes.
