---
name: gws
description: Google Workspace admin and investigation tool via service account + domain-wide delegation. Covers Vault (eDiscovery email search), Gmail (read any inbox), Directory (users/groups/OUs), Reports (audit logs, logins, Drive activity), Drive (file search), Calendar (events), Sheets (read data), Docs (read content), and People (contacts/directory). Use when querying any user's email, searching org-wide email content, checking login activity, listing users/groups, reading Drive files, viewing calendars, or pulling spreadsheet/doc data across a Google Workspace domain.
metadata:
  openclaw:
    homepage: https://github.com/jmac122/gws-skill
    requires:
      env:
        - GWS_SERVICE_ACCOUNT_PATH
        - GWS_ADMIN_EMAIL
        - GWS_DOMAIN
      bins:
        - python3
      pip:
        - google-auth
        - google-auth-httplib2
        - google-api-python-client
    credentials:
      primary: GWS_SERVICE_ACCOUNT_PATH
      description: "GCP service account JSON key with domain-wide delegation. Grants read-only access to Gmail, Vault, Drive, Calendar, Sheets, Docs, Directory, Reports, and People APIs for any user in the Google Workspace domain."
---

# GWS Skill

Unified Google Workspace admin and investigation tool. All scripts in `scripts/` relative to this file.

## Security

- **Never log, echo, or output credentials** — service account key and tokens stay in memory only
- **Never send raw email body content to chat unprompted** — always summarize unless explicitly asked for full content
- **Impersonation is logged** — every DWD call specifies which account is being impersonated
- **Read-only access** — no write scopes are granted; cannot send email, create events, or modify files
- **Credential storage** — service account key at `~/.config/gws/service-account.json` (chmod 600, outside any repo)
- **No secrets in code** — key path loaded from env var `GWS_SERVICE_ACCOUNT_PATH` or default path

## Auth

All scripts use `scripts/auth.py` — loads service account key and impersonates users via domain-wide delegation.

- Default admin: configured via `GWS_ADMIN_EMAIL` env var
- Domain: configured via `GWS_DOMAIN` env var
- Impersonate another user: pass their email to `--user` flag

## Scripts

### vault.py — Email Investigation (org-wide content search)

Search anyone's email content. Creates temporary matter → runs query → returns results → auto-deletes matter.

```bash
python3 scripts/vault.py --accounts user@domain.com --terms "from:vendor@acme.com" --start "2026-03-01T00:00:00Z" --end "2026-03-26T23:59:59Z"
python3 scripts/vault.py --org-unit <orgUnitId> --terms "subject:confidential"
python3 scripts/vault.py --accounts user@domain.com --terms "from:vendor@acme.com" --export
```

Search terms use Gmail operators: `from:`, `to:`, `subject:`, `has:attachment`, `filename:`, `newer_than:`, `older_than:`, etc.

### gmail.py — Read Any User's Inbox

```bash
# Metadata summary
python3 scripts/gmail.py --user user@domain.com --query "from:acme.com newer_than:7d" --max 10 --mode summary
# Full email body
python3 scripts/gmail.py --user user@domain.com --query "from:acme.com" --max 5 --mode full
# Single message by ID
python3 scripts/gmail.py --user user@domain.com --query "" --mode read --message-id <id>
```

**Investigation workflow:** Vault count → Gmail summary → Gmail full content.

### directory.py — Users, Groups, OUs

```bash
python3 scripts/directory.py users [--query "name:Jared"] [--max 100]
python3 scripts/directory.py user user@domain.com
python3 scripts/directory.py groups
python3 scripts/directory.py members group@domain.com
python3 scripts/directory.py orgunits
```

### reports.py — Audit Logs & Activity

```bash
python3 scripts/reports.py login [--user user@domain.com] [--event login_failure] [--start ISO] [--end ISO]
python3 scripts/reports.py admin [--max 25]
python3 scripts/reports.py drive [--user user@domain.com]
python3 scripts/reports.py token [--user user@domain.com]
python3 scripts/reports.py gmail [--user user@domain.com]
```

### drive.py — Search & Read Files

```bash
python3 scripts/drive.py search --user user@domain.com --query "name contains 'invoice'"
python3 scripts/drive.py recent --user user@domain.com
python3 scripts/drive.py file --user user@domain.com --id <fileId>
python3 scripts/drive.py shared --user user@domain.com
python3 scripts/drive.py type --user user@domain.com --type sheet
```

### gcalendar.py — Read Calendars

```bash
python3 scripts/gcalendar.py today --user user@domain.com
python3 scripts/gcalendar.py tomorrow --user user@domain.com
python3 scripts/gcalendar.py events --user user@domain.com --start ISO --end ISO [--query "meeting"]
python3 scripts/gcalendar.py calendars --user user@domain.com
```

### sheets.py — Read Spreadsheets

```bash
python3 scripts/sheets.py metadata --user user@domain.com --id <spreadsheetId>
python3 scripts/sheets.py get --user user@domain.com --id <spreadsheetId> --range "Sheet1!A1:D10"
python3 scripts/sheets.py batch --user user@domain.com --id <spreadsheetId> --ranges "Sheet1!A1:B5" "Sheet2!A1:C3"
```

### docs.py — Read Documents

```bash
python3 scripts/docs.py get --user user@domain.com --id <documentId>
python3 scripts/docs.py text --user user@domain.com --id <documentId>
```

### people.py — Contacts & Org Directory

```bash
python3 scripts/people.py contacts --user user@domain.com
python3 scripts/people.py search --user user@domain.com --query "John"
python3 scripts/people.py directory --user user@domain.com --query "manager"
```

## Setup

See `references/setup-checklist.md` for one-time GCP + Google Admin configuration steps.
