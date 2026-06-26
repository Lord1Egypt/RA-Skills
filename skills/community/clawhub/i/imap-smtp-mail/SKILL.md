---
name: imap-smtp-mail
version: 1.0.4
description: Read and send email via IMAP/SMTP using local Node scripts. Use when the agent needs to check inboxes, fetch email content, search messages, download attachments, or send emails with optional attachments from configured mailboxes. Includes optional inbox watcher that can forward alerts via OpenClaw CLI.
metadata:
  openclaw:
    emoji: "EM"
    requires:
      bins:
        - node
        - npm
      env:
        - IMAP_HOST
        - IMAP_USER
        - IMAP_PASS
        - SMTP_HOST
        - SMTP_USER
        - SMTP_PASS
---

# IMAP/SMTP Email Tool

Use local Node scripts for inbox access and outbound mail:
- `node scripts/imap.js ...`
- `node scripts/smtp.js ...`

> **Published as `imap-smtp-mail` on ClawHub.**

## Configuration

Create `~/.openclaw/credentials/imap-smtp-mail.env` with:

```bash
# IMAP
IMAP_HOST=imap.example.com
IMAP_PORT=993
IMAP_USER=you@example.com
IMAP_PASS=your_password
IMAP_TLS=true
IMAP_REJECT_UNAUTHORIZED=true
IMAP_MAILBOX=INBOX
IMAP_SAVE_SENT=true
# Optional override if your provider does not expose the Sent folder cleanly
# IMAP_SENT_MAILBOX=Sent

# SMTP
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_SECURE=false
SMTP_USER=you@example.com
SMTP_PASS=your_password
SMTP_FROM=you@example.com
SMTP_FROM_NAME=Your Name
SMTP_REPLY_TO=you@example.com
SMTP_CLIENT_NAME=example.com
SMTP_REJECT_UNAUTHORIZED=true

# File access controls
ALLOWED_READ_DIRS=~/.openclaw/workspace,~/.openclaw/workspace/exports,~/.openclaw/workspace/out,~/.openclaw/workspace/tmp
ALLOWED_WRITE_DIRS=~/.openclaw/workspace/exports,~/.openclaw/workspace/tmp
```

This skill loads `~/.openclaw/credentials/imap-smtp-mail.env` at runtime with `dotenv`. The credential file path can be overridden with the `EMAIL_ENV_FILE` environment variable. The IMAP/SMTP variables do not need to be exported globally in the OpenClaw service environment.

SMTP notes:
- `SMTP_FROM_NAME` sets a display name.
- `SMTP_REPLY_TO` is optional.
- `SMTP_CLIENT_NAME` controls the hostname used in `EHLO/HELO`. If omitted, the script derives it from the sender domain.
- When only plain text is provided, the tool also generates a simple HTML alternative part.
- For emails containing structured data, prefer well-formed HTML content over plain-text pseudo-layouts when readability matters.

IMAP Sent-copy notes:
- If IMAP is configured and `IMAP_SAVE_SENT` is not `false`, the tool appends a copy of each sent email to the IMAP Sent mailbox after successful SMTP delivery.
- The script tries to detect the Sent mailbox automatically using IMAP mailbox attributes and common folder names.
- If needed, set `IMAP_SENT_MAILBOX` explicitly (for example `Sent`, `Sent Items`, or `INBOX.Sent`).

Default contact file:
`contacts/email-contacts.json`

Contact shape:

```json
{
  "version": 1,
  "contacts": [
    {
      "id": "client-a",
      "name": "Client A",
      "email": "client@example.com",
      "phone": "+000000000000",
      "aliases": ["client a", "achat client a"],
      "tags": ["client"],
      "notes": "Optional note"
    }
  ]
}
```

## Install

Run once in the skill folder:

```bash
cd skills/imap-smtp-mail
npm install
```

## Common commands

### Check inbox

```bash
cd skills/imap-smtp-mail
node scripts/imap.js check --limit 10
```

### Search email

```bash
cd skills/imap-smtp-mail
node scripts/imap.js search --subject "invoice" --recent 7d --limit 20
```

### Fetch one message

```bash
cd skills/imap-smtp-mail
node scripts/imap.js fetch 123
```

Fetch output includes parsed recipient fields (`from`, `to`, `cc`, `replyTo`) and threading headers (`messageId`, `inReplyTo`, `references`).

### Fetch message and read attachment content inline

```bash
cd skills/imap-smtp-mail
node scripts/imap.js fetch 123 --extract-attachments
```

Parses `.xlsx`, `.csv`, and `.pdf` attachments directly and returns their content in the JSON output. Each attachment entry includes a `status` field:

- `parsed` — content extracted. Excel/CSV: `sheets[]` with `headers` and `rows`. PDF: `text` and `pages`.
- `skipped_large` — over limit: raw file > 500 KB, or Excel > 200 rows / 10 000 cells, or PDF > 25 000 extracted chars. Includes a `reason` field.
- `skipped_inline_image` — image with inline disposition (logo, signature). Silently ignored.
- `unsupported` — file type not supported for extraction (e.g. attached JPEG, DOCX, ZIP).
- `failed` — parsing error. Includes a `reason` field.

Additional fields on `parsed` PDF results:
- `warning: 'scanned_pdf_likely'` — extracted text is under 20 chars despite the file having pages; the PDF is probably a scan and text extraction yielded nothing useful.

For multi-sheet workbooks, each sheet carries its own `status`. The attachment-level status is `parsed` if at least one sheet was successfully read; `skipped_large` if all sheets exceeded the limit.

Use `fetch --extract-attachments` when the email is known or suspected to contain a useful business document (price list, invoice, order). Use the standard `download` command instead when the file is too large or needs to be saved to disk.

### Download attachments

```bash
cd skills/imap-smtp-mail
node scripts/imap.js download 123 --dir ~/.openclaw/workspace/tmp
```

### Mark messages as read

```bash
cd skills/imap-smtp-mail
node scripts/imap.js mark-read 123 456
```

### Mark messages as unread

```bash
cd skills/imap-smtp-mail
node scripts/imap.js mark-unread 123
```

### List mailboxes

```bash
cd skills/imap-smtp-mail
node scripts/imap.js list-mailboxes
```

### Test SMTP

> **Note:** This command sends a real test email to your own address (`SMTP_USER`). It is not a passive connectivity check.

```bash
cd skills/imap-smtp-mail
node scripts/smtp.js test
```

Verbose SMTP debug:

```bash
cd skills/imap-smtp-mail
node scripts/smtp.js test --debug
```

### List contacts

```bash
cd skills/imap-smtp-mail
node scripts/smtp.js contacts
node scripts/smtp.js contacts --query compta
```

### Resolve one contact

```bash
cd skills/imap-smtp-mail
node scripts/smtp.js resolve-contact --contact "Client A"
```

### Send email

```bash
cd skills/imap-smtp-mail
node scripts/smtp.js send --to client@example.com --subject "Subject" --body "Message"
```

By default, `send` creates a draft preview only. Actual sending requires `--approve`.

```bash
cd skills/imap-smtp-mail
node scripts/smtp.js send --to client@example.com --subject "Subject" --body "Message" --approve
```

### Reply to an existing email

Preview a threaded reply to the sender (or `Reply-To` when present):

```bash
cd skills/imap-smtp-mail
node scripts/smtp.js send --reply-uid 123 --body "Hello,\n\nReceived, thanks.\n\nBest regards"
```

Reply-all while keeping the original `To` and `Cc` recipients (except own mailbox and duplicates):

```bash
cd skills/imap-smtp-mail
node scripts/smtp.js send --reply-uid 123 --reply-all --body "Hello,\n\nReceived, thanks.\n\nBest regards" --approve
```

With `--reply-uid`, the tool auto-fills the reply target, adds `Re:` to the subject when needed, and sets `In-Reply-To` / `References` for proper threading.
Use `--reply-all` by default for normal business thread replies unless the user explicitly wants a sender-only reply.

### Send email by contact name

```bash
cd skills/imap-smtp-mail
node scripts/smtp.js send --contact "Client A" --subject "Subject" --body "Message" --approve
```

Verbose send debug:

```bash
cd skills/imap-smtp-mail
node scripts/smtp.js send --contact "Client A" --subject "Subject" --body "Message" --approve --debug
```

When IMAP Sent-copy is active, the send result also includes:
- `savedToSent`
- `sentMailbox`
- `sentCopyError` if the SMTP send succeeded but the IMAP append failed

### Draft email with attachment

```bash
cd skills/imap-smtp-mail
node scripts/smtp.js send --to client@example.com --subject "Report" --body "Please find attached the report." --attach ~/.openclaw/workspace/exports/pdfs/report.pdf
```

Actual sending with attachment:

```bash
cd skills/imap-smtp-mail
node scripts/smtp.js send --to client@example.com --subject "Report" --body "Please find attached the report." --attach ~/.openclaw/workspace/exports/pdfs/report.pdf --approve
```

### Send styled HTML email

```bash
cd skills/imap-smtp-mail
node scripts/smtp.js send --to client@example.com --subject "Stock status" --html "<p>Hello,</p><p>Here is the stock status.</p><table border=\"1\" cellpadding=\"6\" cellspacing=\"0\"><tr><th>Reference</th><th>Stock</th></tr><tr><td>REF-001</td><td>12</td></tr></table><p>Best regards</p>" --approve
```

## Operational rules

- Use this skill for email only.
- Keep outbound email approval-based: never auto-send without user validation.
- Use attachments only from allowed workspace directories.
- Use contact aliases from `contacts/email-contacts.json` when the user refers to recipients by name.
- The contact list is for outbound convenience and recipient resolution; incoming email can come from any sender.
- The agent may summarize incoming email and prepare a draft reply, but must never auto-reply without user validation.
- For replies to an inbound email, prefer `node scripts/smtp.js send --reply-uid <uid> --reply-all ...`; omit `--reply-all` only when the user explicitly wants sender-only.
- `node scripts/imap.js fetch <uid>` exposes `Cc`, `Reply-To`, `messageId`, `In-Reply-To`, and `References` so reply behavior can be inspected before sending.
- Do not expose credentials in responses.
- Use `--debug` when delivery behavior needs investigation; it prints SMTP transport logs to stderr and returns envelope/accepted/rejected details in JSON.

## Lightweight email watch (optional)

> **Note:** This feature is optional and higher-trust than basic IMAP/SMTP usage. When enabled, `email-watch-lite.js` invokes the local `openclaw` CLI to analyze pending emails and may forward summarized email content to another OpenClaw channel (e.g. WhatsApp). Do not enable it unless you understand and accept this behavior.

For low-cost inbox polling, use the detector script instead of a recurring model cron:

```bash
cd skills/imap-smtp-mail
node scripts/email-watch-lite.js detect --state ../../memory/email-watch-state.json
```

To poll and trigger the agent only when `pendingUids` exist:

```bash
cd skills/imap-smtp-mail
node scripts/email-watch-lite.js detect-and-trigger --state ../../memory/email-watch-state.json --channel whatsapp --to +000000000000 --openclaw-bin ~/.npm-global/bin/openclaw --timeout 180 --thinking low
```

Customize the analysis prompt with `--message "your custom instructions"`.

The email watcher requires the `openclaw` CLI binary. It is not needed for core IMAP/SMTP operations.
