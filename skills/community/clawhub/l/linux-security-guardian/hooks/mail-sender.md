---
name: linux-security-guardian-mail-sender
description: Uses email plugin/skill to send audit report. No inline SMTP/Python/sendmail implementation.
---

# Mail Sender Hook

## Do NOT implement email sending here.

This project does NOT bundle email sending logic (no Python smtplib, no Himalaya CLI, no sendmail).

Instead, **use an available email plugin, skill, or MCP tool** to send the report.

## Pre-requisite: Load core-extra Profile

Before sending email, load config from `core-extra/config/profile.md`:
```
→ Read: core-extra/config/profile.md
→ Extract: noreply_email = profile.Email.noreply (replace [email_domain] with profile.Domain.email_domain)
→ Extract: support_email = profile.Email.support
→ Extract: owner_name = profile.Owner.name
→ Extract: company_name = profile.Company.name
```

## Execution

```
1. Determine which report(s) to send:
   Per-server report:  reports/<client>/<server>/daily/YYYY-MM-DD.md
   Per-client summary: reports/<client>/summary-YYYY-MM-DD.md
   Master report:      reports/master-YYYY-MM-DD.md

2. Call available email plugin/skill with:
   Per-server:
     to:      SERVER_PROFILE.md → Client/<client>/notification_email
     from:    <noreply_email>    (from core-extra/config/profile.md)
     subject: "[Linux Guardian] <client>/<server> — YYYY-MM-DD | Score: N/100 | CRITICAL:N HIGH:N"

   Per-client summary:
     to:      SERVER_PROFILE.md → Client/<client>/notification_email
     from:    <noreply_email>    (from core-extra/config/profile.md)
     subject: "[Linux Guardian] <client> Summary — YYYY-MM-DD | Servers: N/N | CRITICAL:N HIGH:N"

   Master:
     to:      Global notification email
     from:    <noreply_email>    (from core-extra/config/profile.md)
     subject: "[Linux Guardian] Master Audit Report — YYYY-MM-DD | Clients:N | Servers:N"

   body (all): compiled report body

3. If plugin/skill unavailable:
   → Log to AUDIT_LOG.md: "EMAIL NOT SENT — no email plugin/skill available for <client>/<server>"
   → Report is on disk. Non-fatal. Audit is complete.
```
