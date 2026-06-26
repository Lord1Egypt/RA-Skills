---
name: mail_invoice_archiver
description: Read supported mailbox providers such as 126, 163, and Gmail, identify invoice attachments or invoice download links, archive invoices by month, deduplicate by invoice number and amount, and prepare monthly reports plus delivery bundles. Use when OpenClaw needs to sync invoice mail, investigate failed downloads, package a month's archive, or summarize totals and high-value invoices.
metadata: {"openclaw":{"name":"mail_invoice_archiver","displayName":"Mail Invoice Archiver","requires":["python3"],"requiresNetwork":true}}
---

# Mail Invoice Archiver

## Quick Start

- In the first session after installation, ask the user which credential storage mode they want before doing anything else.
- Run `python3 {baseDir}/scripts/cli.py providers --json` when you need to show the currently supported mailbox providers and their setup notes.
- Run `python3 {baseDir}/scripts/cli.py doctor --json` first. If it returns `setup_required: true`, guide the user through setup and wait for confirmation.
- Use `python3 {baseDir}/scripts/cli.py setup` for an interactive setup wizard, or pass `--mail-provider 126|163|gmail|custom` plus `--provider system|env|config|prompt` for scripted setup.
- Use `python3 {baseDir}/scripts/cli.py sync --month YYYY-MM --json` to pull a month into the local archive.
- Use `python3 {baseDir}/scripts/cli.py report --month YYYY-MM --json` to inspect totals, duplicates, conflicts, and failures.
- Use `python3 {baseDir}/scripts/cli.py deliver --month YYYY-MM --json` to prepare a zip plus summary for the current chat.

## Workflow

1. Run `doctor`.
2. If `doctor` reports `setup_required`, ask the user which mailbox provider they want first:
   `126`, `163`, `gmail`, or `custom`.
3. Ask the user which auth mode they want:
   system credential store, environment variables, config file, or prompt-each-session.
4. Run `setup` with the chosen mailbox provider and auth mode, then wait for the user to confirm they completed any external steps, such as exporting environment variables.
4. Run `doctor` again to confirm the setup works.
5. Run `list --month YYYY-MM --limit 20 --json` when you need a quick mailbox preview without downloading files.
6. Run `sync --month YYYY-MM --json` to archive candidate invoices into `~/Documents/invoice-archive/YYYY-MM/`.
7. Run `report --month YYYY-MM --json` after sync and summarize:
   total amount, canonical invoice count, high-value invoices, duplicates, conflicts, and failures.
8. Run `deliver --month YYYY-MM --json`, then attach the returned zip file in the current chat and paste the summary.

## Windows Env Setup

- If the user chooses `env` on Windows, offer one of these exact snippets and wait for confirmation before rerunning `doctor`.

```powershell
$env:MAIL_INVOICE_ARCHIVER_EMAIL = "your-mail@example.com"
$env:MAIL_INVOICE_ARCHIVER_AUTH_CODE = "your-provider-secret"
python "{baseDir}/scripts/cli.py" doctor --json
```

```cmd
set MAIL_INVOICE_ARCHIVER_EMAIL=your-mail@example.com
set MAIL_INVOICE_ARCHIVER_AUTH_CODE=your-provider-secret
python "{baseDir}\scripts\cli.py" doctor --json
```

- For Gmail, `MAIL_INVOICE_ARCHIVER_AUTH_CODE` must be a Gmail app password, not the normal Google account password.

## Rules

- Prefer `system` auth on macOS and Windows, `env` on Linux, CI, or headless sessions, and `prompt` only when the user does not want to persist the secret anywhere.
- `system` currently means macOS Keychain on macOS and Windows Credential Manager on Windows.
- First-phase built-in providers are `126`, `163`, and `gmail`.
- Treat `appleimap.126.com` as the preferred 126 IMAP host.
- Send the provider-configured IMAP client `ID` only when that provider needs it. Today that means 126 and 163; Gmail does not need it.
- Gmail is implemented today through IMAP app passwords for personal Gmail accounts. Some Google Workspace tenants may still require admin-side IMAP changes or OAuth, which is a future enhancement and not part of the current runtime.
- Deduplicate in two layers:
  storage duplicates by message UID / part / SHA256;
  business duplicates by `invoice number + amount`.
- If invoice number matches but amount differs, keep the file and report it as a conflict instead of auto-merging.
- Keep invoice amount and OCR results in SQLite metadata, not in file names.
- If a link download fails and the message still looks like an invoice, report that failure back to the user.
- When the same invoice appears in multiple attachment formats in one mail, prefer user-friendly formats for the canonical saved file. Default priority should be: **image (png/jpg/jpeg) or PDF first**, then XML, then OFD, and ZIP last. Do not prefer OFD or ZIP when a readable PDF or image version of the same invoice is available.
- Treat OFD as a fallback archival format, not the default user-facing format, unless it is the only available canonical representation.
- For PDF invoice amount extraction, do not blindly take the first `¥` amount. PDF text extraction may reorder the invoice area and expose tax base amount, tax amount, and total amount in the wrong sequence.
- For PDF invoices, prefer a dedicated total-amount extractor over generic regex fallback. Use the invoice total area first, then fall back only when that area is missing.
- Buyer and seller names in PDF invoices may collapse into repeated `名称： 名称：` layouts after text extraction. Prefer layout-aware extraction over a single regex when distinguishing buyer and seller.
- Month summaries must be stable even when a current-month row is marked as `duplicate` against an older canonical row outside the month window. Summaries should aggregate by current-month business keys, not only by `status='saved'` rows inside the month.
- If the user specifies a business rule for a specific invoice family, such as using `价税合计` for totals, record and honor that rule consistently in later extraction and reporting.

## Resources

- Runtime: [scripts/cli.py](scripts/cli.py)
- Detailed findings and pitfalls: [references/compatibility-notes.md](references/compatibility-notes.md)
- Feishu local config example: [config/feishu/config.example.yaml](config/feishu/config.example.yaml)

## Local Secret Config Convention

When this skill needs Feishu app credentials for local delivery helpers or follow-up integrations, do not store real secrets inside the published skill directory.

Use this split instead:

- committed example inside the skill: `config/feishu/config.example.yaml`
- local real config outside the skill: `~/.config/openclaw/mail_invoice_archiver/feishu.config.yaml`

Why this rule exists:

- `.gitignore` reduces Git commit risk, but should not be treated as the security boundary for skill publishing.
- Publishing flows may not behave exactly like Git, so real secrets must live outside the skill folder.
- The skill should only ship examples, docs, and secret-loading logic, never the real credential file.

Recommended loading order for Feishu credentials:

1. explicit environment variables
2. local private config at `~/.config/openclaw/mail_invoice_archiver/feishu.config.yaml`
3. prompt the user

Environment variable names:

- `MAIL_INVOICE_ARCHIVER_FEISHU_APP_ID`
- `MAIL_INVOICE_ARCHIVER_FEISHU_APP_SECRET`
- `MAIL_INVOICE_ARCHIVER_FEISHU_RECEIVE_ID_TYPE`
- optional override path: `MAIL_INVOICE_ARCHIVER_FEISHU_CONFIG`

Never publish or share the real local config file.

If `config/feishu/config.yaml` appears inside the skill directory, treat it as an unsafe misconfiguration. The runtime should fail fast and require moving that file out of the skill.
