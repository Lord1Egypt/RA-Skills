---
name: osascript-email
description: Send emails on macOS via AppleScript (osascript) using Mail.app — no SMTP credentials, passwords, or API keys required. Use when: sending automated emails from macOS, sending standup reports or alerts via email, emailing from a cron job or agent, or when other email tools (sendmail, himalaya, SMTP) are unavailable or unconfigured. Requires Mail.app to be installed and configured with at least one account. NOT for: bulk email sends; HTML email; email with large attachments; non-macOS environments.
---

# osascript-email

Send email via Mail.app using AppleScript. No password or API key needed — Mail.app handles auth.

## Prerequisites
- macOS with Mail.app installed
- At least one email account configured in Mail.app
- Verify the sender address matches a configured Mail.app account
- **Authorization:** This skill sends email silently from Mail.app. Only use with explicit user consent. Never use to send on behalf of a user without their knowledge.

---

## Quick send (exec)

Use `exec` to run an inline osascript command. The script below is the canonical pattern — copy it exactly, then substitute values.

```bash
osascript << 'APPLESCRIPT'
tell application "Mail"
  set m to make new outgoing message with properties {subject:"YOUR SUBJECT", content:"YOUR BODY", visible:false}
  tell m
    make new to recipient with properties {address:"recipient@example.com"}
    make new to recipient with properties {address:"cc@example.com"}
  end tell
  send m
end tell
return "sent"
APPLESCRIPT
```

**Escaping rules:**
- Double quotes inside subject/content must be escaped: `\"`
- Backslashes must be doubled: `\\`
- Newlines inside content: use `\n` (AppleScript treats literal newlines in the string as content)

---

## Python helper (for agent scripts)

Use when sending email from a Python cron script or agent workflow. Copy the function from `scripts/send_email.py` — do not rewrite it.

```python
from scripts.send_email import send_email

send_email(
    subject="Daily Report — 2026-01-01",
    body="Here is the summary...",
    to="primary@example.com",
    cc="secondary@example.com",       # optional
    sender="your-mail-app-account@icloud.com"  # must match Mail.app account
)
```

See `scripts/send_email.py` for the full implementation.

---

## Multi-recipient

Add additional `make new to recipient` lines inside the `tell m` block:

```applescript
make new to recipient with properties {address:"a@example.com"}
make new to recipient with properties {address:"b@example.com"}
```

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| `osascript: Mail got an error` | Mail.app not open or account not configured | Open Mail.app, check accounts |
| Email lands in Drafts | `send m` not reached (script errored before) | Check escape characters |
| `execution error: Mail got an error: Invalid recipient` | Address typo | Verify recipient address |
| Email sends but empty body | Newline escape issue in content string | Use Python helper instead |
| `returncode != 0` with no stderr | osascript permission denied | Grant Automation permission: **macOS Ventura+**: System Settings → Privacy & Security → Automation; **older macOS**: System Preferences → Security & Privacy → Automation |

---

## Limitations
- Plain text only (no HTML, no inline images)
- Attachments possible but require additional AppleScript — see `references/attachments.md`
- Rate: Mail.app will queue and send; not suitable for bulk sends (>10 emails)
- Sender must be a configured Mail.app account — cannot spoof arbitrary addresses
