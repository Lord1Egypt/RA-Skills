# First setup

## A. Capabilities (this skill)

1. **Mailbox** open tonnage / cargo (route A) — needs **email**.  
2. **Pre-arrival** at a port (route C) — needs **API Key**; contacts on demand per **`CONTACT_API.md`**.

**Liner schedules** (bulk / Ro-Ro / container): install **`hifleet-schedule`**.

## B. Config checklist

| Item | For |
|------|-----|
| `hifleet_api_key` | Route C; route A enrich |
| `hifleet_liner_api_base` | Route C ports/suggest + contact fetch (`CONTACT_API.md`) |
| Email IMAP | Route A only |
| `mail_preview_server.py` | Route A「查看原邮件」按钮（见 **`MAIL_PREVIEW.md`**） |

## C. API Key

See **`CONFIG.example.md`**. Get key at mytonnages.hifleet.com.

## D. How to ask

| Question | Skill |
|----------|--------|
| My **mail** / sender / inbox tonnage | **A** (this skill) |
| **Pre-arrival** / ETA at port | **C** (this skill) |
| **Liner / line** schedule | **hifleet-schedule** |
| **Public** open tonnage/cargo on HiFleet | **hifleet-opentonnages** |

## E. Language

Set agent locale via `HIFLEET_USER_LOCALE` or `OPENCLAW_USER_LOCALE`; see **`LOCALIZATION.md`**.
