# Gmail IMAP Reference

## Credentials

Set these env vars (never print the password):
```
GMAIL_IMAP_USER=user@gmail.com
GMAIL_IMAP_PASSWORD=<app-password>
```

Generate an app password at: https://myaccount.google.com/apppasswords
(Requires 2FA enabled on the Google account.)

## Connection Details

| Setting | Value |
|---------|-------|
| IMAP server | imap.gmail.com |
| IMAP port | 993 (SSL) |
| SMTP server | smtp.gmail.com |
| SMTP port | 587 (STARTTLS) |

## Gmail Folder Names

Gmail uses labels, exposed as IMAP folders. Standard names:

| Purpose | IMAP Folder Name |
|---------|-----------------|
| Inbox | `INBOX` |
| Sent | `[Gmail]/Sent Mail` |
| Drafts | `[Gmail]/Drafts` |
| Spam | `[Gmail]/Spam` |
| **Trash** | `[Gmail]/Trash` |
| All Mail | `[Gmail]/All Mail` |
| Starred | `[Gmail]/Starred` |

Custom labels appear as top-level folder names.

## Deletion Rules (Critical)

Standard IMAP `\Deleted` + EXPUNGE **does not delete** in Gmail — it only removes the Inbox
label and archives to All Mail.

**Correct deletion procedure:**
1. Use `MOVE` (RFC 6851) or `COPY` to `[Gmail]/Trash`
2. If `MOVE` unsupported: `COPY` to Trash + `STORE \Deleted` + `EXPUNGE`
3. Gmail auto-purges Trash after 30 days

The `gmail_imap.py` script handles this automatically in `cmd_trash()`.

## IMAP Search Criteria (Common)

```
ALL                         # all messages
UNSEEN                      # unread
SEEN                        # read
FROM "someone@example.com"  # from address
SUBJECT "keyword"           # subject contains
SINCE 01-Mar-2026           # after date (DD-Mon-YYYY)
BEFORE 10-Mar-2026          # before date
BODY "text"                 # body contains
```

Combine with parentheses: `(FROM "boss" UNSEEN)`

## Direct IMAP via Python (without the helper script)

```python
import imaplib, os

mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
mail.login(os.environ["GMAIL_IMAP_USER"], os.environ["GMAIL_IMAP_PASSWORD"])
mail.select("INBOX", readonly=True)

# Search
_, data = mail.search(None, "UNSEEN")
uids = data[0].split()

# Fetch headers
_, msg_data = mail.fetch(uids[-1], "(BODY.PEEK[HEADER.FIELDS (FROM DATE SUBJECT)])")

# Move to trash (correct deletion)
mail.uid("MOVE", uid, "[Gmail]/Trash")

mail.logout()
```
