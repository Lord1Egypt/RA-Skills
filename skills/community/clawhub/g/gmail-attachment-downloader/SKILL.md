---
name: gmail-attachment-downloader
description: |
  Download Gmail attachments through IMAP when the user wants to pull invoices,
  statements, or other files from Gmail into a local folder. Use it when the
  task involves Gmail attachment export, sender/subject/date filtering, or
  batch downloading attachments without setting up Google Cloud APIs.
metadata:
  author: "whauff"
  version: "1.1.0"
---

# Gmail Attachment Downloader

Use this skill when the user wants files downloaded from Gmail to the local
machine.

## When To Use

Trigger this skill when the user asks to:

- Download Gmail attachments in bulk
- Export invoices, statements, or receipts from Gmail
- Filter Gmail attachments by sender, subject, date range, extension, or limit
- Save Gmail attachments into a local folder without using Google Cloud APIs

Do not use this skill for:

- Sending email
- Modifying or deleting mailbox contents
- Managing Google OAuth projects

## Inputs To Collect

Collect or infer these inputs before running the script:

- `gmail_user`: Gmail address
- `gmail_pass`: Gmail app password
- `sender`: optional sender filter
- `subject`: optional subject filter
- `since`: optional start date in `DD-Mon-YYYY`
- `before`: optional end date in `DD-Mon-YYYY`
- `extensions`: optional comma-separated extension list such as `.pdf,.ofd`
- `save_folder`: destination folder on the local machine
- `max_results`: optional safety limit for matched messages
- `dry_run`: optional preview mode when the user wants to inspect matches first

If the user did not specify `save_folder`, choose a clear folder under their home
directory and state it explicitly before running.

## Execution

Run the bundled script with explicit arguments instead of editing source files.

```bash
python3 scripts/download_gmail_attachments.py \
  --gmail-user "$GMAIL_USER" \
  --gmail-pass "$GMAIL_PASS" \
  --sender "auth@shove.xforceplus.com" \
  --subject "发票" \
  --since "01-Jan-2025" \
  --extensions ".pdf,.ofd" \
  --save-folder "~/Documents/walmart-invoices" \
  --max-results 200
```

Preview matches without writing files:

```bash
python3 scripts/download_gmail_attachments.py \
  --gmail-user "$GMAIL_USER" \
  --gmail-pass "$GMAIL_PASS" \
  --sender "auth@shove.xforceplus.com" \
  --extensions ".pdf,.ofd" \
  --save-folder "~/Documents/walmart-invoices" \
  --dry-run
```

Environment variables are also supported:

- `GMAIL_USER`
- `GMAIL_PASS`

## Workflow

1. Confirm the user has Gmail IMAP enabled and an app password.
2. Decide the destination folder and filters.
3. Run `scripts/download_gmail_attachments.py` with explicit arguments.
4. Report:
   downloaded count, skipped count, and destination folder.
   If `--summary-json` is used, prefer reading that file for the final report.
5. If authentication fails, tell the user to re-check IMAP and the app password.

## Failure Handling

- If `GMAIL_USER` or `GMAIL_PASS` is missing, stop and ask for it.
- If mailbox auto-detection cannot find Gmail All Mail, fall back to `INBOX`.
- If no messages match, suggest loosening sender/subject/date filters.
- If downloads are zero, suggest removing extension filtering.

## Resources

- Setup details: [references/setup.md](references/setup.md)
- Script entry point: [scripts/download_gmail_attachments.py](scripts/download_gmail_attachments.py)
