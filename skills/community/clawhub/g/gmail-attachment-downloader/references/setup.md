# Gmail Setup

This skill uses Gmail IMAP with an app password. It does not require Google
Cloud or OAuth client setup.

## Prerequisites

- Gmail IMAP enabled in Gmail settings
- Google account with 2-Step Verification enabled
- A Gmail app password

## Setup Steps

1. Open Gmail settings and enable IMAP:
   `https://mail.google.com/mail/#settings/fwdandpop`
2. Generate an app password:
   `https://myaccount.google.com/apppasswords`
3. Export credentials before running:

```bash
export GMAIL_USER="your_email@gmail.com"
export GMAIL_PASS="abcd efgh ijkl mnop"
```

## Notes

- The app password is not the same as the normal Gmail login password.
- This skill only reads mail and downloads attachments.
- The script writes files locally and does not modify mailbox contents.
