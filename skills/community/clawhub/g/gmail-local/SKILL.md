---
name: gmail-local
description: Local Gmail IMAP/SMTP access using a Google App Password. Use when the user wants to search, read, or send Gmail without routing mail through Maton or any third-party proxy. Requires GMAIL_ADDRESS and GMAIL_APP_PASSWORD_FILE. All writes/sends require explicit user approval and --confirm-send.
version: 1.0.0
metadata:
  openclaw:
    emoji: 📬
    requires:
      env:
        - GMAIL_ADDRESS
        - GMAIL_APP_PASSWORD_FILE
      bins:
        - python3
    primaryEnv: GMAIL_APP_PASSWORD_FILE
    envVars:
      - name: GMAIL_ADDRESS
        required: true
        description: Full Gmail address used for IMAP and SMTP login.
      - name: GMAIL_APP_PASSWORD_FILE
        required: true
        description: Local 0600 file containing the Google App Password.
---

# Gmail Local

Use direct Gmail IMAP/SMTP with a Google App Password. This skill does not use
Maton or any third-party proxy.

## Trust Boundary

- Mail goes directly between this host and Google Gmail servers:
  - IMAP: `imap.gmail.com:993`
  - SMTP: `smtp.gmail.com:465`
  These endpoints are fixed in the helper and are not configurable by
  environment variable.
- Credentials stay local and must be provided through:
  - `GMAIL_ADDRESS`
  - `GMAIL_APP_PASSWORD_FILE`
- Never print, log, commit, or echo the app password. Do not pass it directly
  as an environment variable.
- App Passwords require Google 2-Step Verification and may be unavailable for
  some accounts, Workspace policies, or Advanced Protection accounts.
- IMAP must be enabled in Gmail settings.

## Commands

The local helper is under this skill folder:

```bash
scripts/gmail_local.py
```

List recent Inbox messages:

```bash
python3 scripts/gmail_local.py list --limit 10
```

Search with an IMAP query:

```bash
python3 scripts/gmail_local.py search --query 'UNSEEN'
python3 scripts/gmail_local.py search --query 'FROM "person@example.com"'
```

Read a message by UID:

```bash
python3 scripts/gmail_local.py read --uid 12345
```

Send mail only after explicit approval:

```bash
python3 scripts/gmail_local.py send \
  --to person@example.com \
  --subject "Subject" \
  --body "Message body" \
  --confirm-send
```

## Safety Rules

- Before `send`, show `to`, `cc`, `bcc`, `subject`, and a body preview, then get
  explicit user approval.
- The helper refuses to send unless `--confirm-send` is provided after that
  approval.
- Do not use this skill to mass-mail, spam, scrape contacts, or send sensitive
  data without confirmation.
- Prefer read-only commands (`list`, `search`, `read`) unless the user clearly
  asks to send.
- If an authentication error occurs, do not retry repeatedly; ask the user to
  check IMAP settings and rotate the App Password if needed.

## Setup

Create a Google App Password at:

```text
https://myaccount.google.com/apppasswords
```

Store it in a local `0600` file:

```bash
install -m 600 /dev/null ~/.openclaw/gmail-app-password
nano ~/.openclaw/gmail-app-password
```

Then set local environment for the gateway service. Example:

```bash
openclaw config set env.vars.GMAIL_ADDRESS you@gmail.com
openclaw config set env.vars.GMAIL_APP_PASSWORD_FILE ~/.openclaw/gmail-app-password
openclaw gateway restart
```
