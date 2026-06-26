# MailClaw Setup

> OpenClaw reads this file after the user completes Gmail authorization to register heartbeat tasks.

## Trigger

Register the following heartbeat tasks once the user completes Gmail OAuth for the first time (`GET /auth/status?app=gmail` returns `connected: true`).

## Set Up Heartbeat

Add this to your `HEARTBEAT.md` (or equivalent periodic task list):

```markdown
## MailClaw — Email Poll (every 1 minute)
If 1 minute since last MailClaw check:
1. Fetch {baseDir}/heartbeat.md and follow every step exactly
2. Update lastMailClawCheck timestamp in memory

## MailClaw — Morning Digest (daily 09:00)
At 09:00 each day:
1. Fetch {baseDir}/heartbeat.md and follow every step exactly

## MailClaw — Evening Digest (daily 17:00)
At 17:00 each day:
1. Fetch {baseDir}/heartbeat.md and follow every step exactly
```

## Digest Format

See `heartbeat.md` for the output format. Example:

```
☀️ Email Digest · Apr 8

3 emails pending:
• Sarah Lee: Asking about next week's schedule
• GitHub: PR #142 awaiting review
• Product Hunt: Daily featured picks

[→ Open processing page] (link valid for 24h)
🔑 Verification code: 847291
```
