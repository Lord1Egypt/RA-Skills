<div align="center">

# 🔗 NexLink — Enterprise Connector for Nextcloud, Exchange & YouTube

**Email, calendar, tasks, file management, document understanding, transcript extraction, contacts, and analytics**

**Built by [Firma de AI](https://firmade.ai) · Supported by [Firma de IT](https://firmade.it)**

[![Version](https://img.shields.io/badge/version-0.15.2-blue.svg)](https://github.com/asistent-alex/openclaw-nexlink)
[![License: MIT-0](https://img.shields.io/badge/License-MIT--0-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-green.svg)](https://clawhub.ai/asistent-alex/nexlink)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/tests-48%2F48%20passed-brightgreen.svg)](https://github.com/asistent-alex/openclaw-nexlink/actions)
[![ClawHub](https://img.shields.io/badge/clawhub-nexlink-8A2BE2.svg)](https://clawhub.ai/asistent-alex/nexlink)
[![Hardshell](https://img.shields.io/badge/code%20style-Hardshell-ff69b4.svg)](https://github.com/asistent-alex/openclaw-hardshell)
[![GitHub](https://img.shields.io/badge/GitHub-Repo-181717.svg?logo=github)](https://github.com/asistent-alex/openclaw-nexlink)
[![Security](https://img.shields.io/badge/security-audited-brightgreen.svg)](https://github.com/asistent-alex/openclaw-nexlink/blob/main/SECURITY.md)

</div>

---

**NexLink** connects Nextcloud, Microsoft Exchange, and YouTube into one enterprise-grade workflow layer — with built-in security confirmations and least-privilege defaults.

> **Public positioning:** *Firma de AI — Nextcloud, Exchange & YouTube Assistant*  
> **CLI name:** `nexlink` · **Version:** `v0.15.2` · **License:** `MIT-0`

### 🔗 Official Links

| Resource | URL |
|----------|-----|
| 🏠 **Homepage** | [firmade.ai](https://firmade.ai) |
| 📦 **GitHub Repository** | [github.com/asistent-alex/openclaw-nexlink](https://github.com/asistent-alex/openclaw-nexlink) |
| 📋 **ClawHub Listing** | [clawhub.ai/asistent-alex/nexlink](https://clawhub.ai/asistent-alex/nexlink) |
| 📖 **Documentation** | [github.com/asistent-alex/openclaw-nexlink#readme](https://github.com/asistent-alex/openclaw-nexlink#readme) |
| 🔒 **Security Policy** | [github.com/asistent-alex/openclaw-nexlink/blob/main/SECURITY.md](https://github.com/asistent-alex/openclaw-nexlink/blob/main/SECURITY.md) |
| 📝 **Changelog** | [github.com/asistent-alex/openclaw-nexlink/blob/main/CHANGELOG.md](https://github.com/asistent-alex/openclaw-nexlink/blob/main/CHANGELOG.md) |
| 🐛 **Issues** | [github.com/asistent-alex/openclaw-nexlink/issues](https://github.com/asistent-alex/openclaw-nexlink/issues) |
| 🔄 **Releases** | [github.com/asistent-alex/openclaw-nexlink/releases](https://github.com/asistent-alex/openclaw-nexlink/releases) |

---

## What it does

This skill connects Nextcloud, Exchange, and YouTube into one practical workflow layer for:

- **Files** — list, search, upload, download, move, copy, info, sharing
- **Document understanding** — extract text, summarize, ask questions about one file
- **Workflow extraction** — extract actions from documents and create Exchange tasks
- **YouTube** — transcript extraction with language fallback, text/JSON output, save to Nextcloud
- **Email** — read, send, draft, reply, forward, attachments
- **Calendar** — today, week, list, create, update, respond
- **Tasks** — list, create, complete, trash, delegate workflows
- **Sync & Reminders** — task sync with Exchange, email reminders, calendar linking
- **Analytics** — inbox stats, response time, top senders, heatmap, reports

## Why this is useful

Use it when a team already works in **Nextcloud**, **Microsoft Exchange** and wants one assistant layer for:

- file operations and sharing
- turning documents into action items
- extracting YouTube transcripts for meetings and research
- inbox and follow-up workflows
- meeting and task coordination

Built by [Firma de AI](https://firmade.ai), supported by [Firma de IT](https://firmade.it).

## Quick start

### Current CLI name

After installation, the command remains:

```bash
nexlink
```

### Typical first checks

```bash
nexlink mail connect
nexlink files list /
nexlink mail read --limit 5
nexlink cal today
nexlink tasks list
nexlink analytics stats --days 7
nexlink sync status
```

## Main capabilities

### Exchange — Email, Calendar, Tasks, Analytics

Full Exchange on-premises (2016/2019) workflows over EWS.

| What you can do | Command |
|---|---|
| Read email | `nexlink mail read` · `nexlink mail read --unread` · `nexlink mail get --id X` |
| Send email | `nexlink mail send --to x@y.com --subject "Hello" --body "..."` |
| Reply / forward | `nexlink mail reply --id EMAIL_ID --body "..."` · `nexlink mail forward --id EMAIL_ID --to other@example.com` |
| Download attachment | `nexlink mail download-attachment --id EMAIL_ID --name file.pdf` |
| Mark unread mail as read | `nexlink mail mark-all-read` |
| Today / week calendar | `nexlink cal today` · `nexlink cal week` |
| Create meeting | `nexlink cal create --subject "Meeting" --start "2026-04-20 14:00" --duration 60` |
| Create task | `nexlink tasks create --subject "Follow-up" --due "+7d" --priority high` |
| List delegated tasks | `nexlink tasks list --mailbox coleg@firma.ro` |
| Complete / trash task | `nexlink tasks complete --id TASK_ID` · `nexlink tasks trash --id TASK_ID` |
| Create contact | `nexlink contacts create --name "Jane Doe" --email "jane@example.com"` |
| Update contact | `nexlink contacts update --id CONTACT_ID --phone "+40-722-000-000"` |
| Delete contact | `nexlink contacts delete --id CONTACT_ID` |
| Search contacts | `nexlink contacts search --query "Acme"` |
| Sync tasks | `nexlink sync sync` · `nexlink sync status` |
| Send reminders | `nexlink sync reminders --hours 24` · `nexlink sync reminders --hours 24 --to owner@example.com` |
| Link calendar event | `nexlink sync link-calendar --task-id TASK_ID` |
| Inbox analytics | `nexlink analytics stats --days 30` |
| Response time | `nexlink analytics response-time --days 7` |
| Top senders | `nexlink analytics top-senders --limit 20` |
| Activity heatmap | `nexlink analytics heatmap --days 30` |
| Folder stats | `nexlink analytics folders` |
| Full report | `nexlink analytics report --days 30` |

> Delegate workflows are supported where Exchange permissions allow them.

### Nextcloud — Files, Sharing, Document Understanding

Nextcloud workflows over WebDAV and OCS APIs.

| What you can do | Command |
|---|---|
| List files | `nexlink files list /Documents/` |
| Search files | `nexlink files search contract /Clients/` |
| Upload / download | `nexlink files upload /local/report.pdf /Documents/` · `nexlink files download /Documents/report.pdf /tmp/` |
| Create / move / copy | `nexlink files mkdir /Documents/New` · `nexlink files move /old /new` · `nexlink files copy /src /dst` |
| File info | `nexlink files info /Documents/report.pdf` |
| Shared items | `nexlink files shared` · `nexlink files share-list` |
| List contacts | `nexlink contacts list --source nextcloud` |
| Get contact | `nexlink contacts get --uid CONTACT_UID --source nextcloud` |
| Create contact | `nexlink contacts create --source nextcloud --name "Jane" --email "j@e.com"` |
| Update contact | `nexlink contacts update --uid CONTACT_UID --source nextcloud --phone "..."` |
| Delete contact | `nexlink contacts delete --uid CONTACT_UID --source nextcloud` |
| Search contacts | `nexlink contacts search --source nextcloud --query "Jane"` |
| Create public links | `nexlink files share-create /Contracts/offer.pdf` |
| Delete file / folder | `nexlink files delete /Documents/old` |
| Extract text | `nexlink files extract-text /Clients/contract.docx` |
| Summarize a file | `nexlink files summarize /Clients/contract.docx` |
| Ask a file | `nexlink files ask-file /Clients/contract.docx "When is the renewal due?"` |
| Extract actions | `nexlink files extract-actions /Clients/contract.txt` |
| Create tasks from file | `nexlink files create-tasks-from-file /Clients/contract.txt --select 1,2 --execute` |

### YouTube — Transcript Extraction

Extract video captions/subtitles with automatic language fallback:

| What you can do | Command |
|---|---|
| Get transcript (text) | `nexlink youtube transcript <url>` |
| Get transcript (JSON) | `nexlink youtube transcript <url> --format json` |
| Language fallback | `nexlink youtube transcript <url> --lang ro,en` |
| Save to Nextcloud | `nexlink youtube transcript <url> --save` |
| List available languages | `nexlink youtube languages <url>` |

Supports all YouTube URL formats (watch, youtu.be, shorts, embed) and raw video IDs.

### Combined workflows

#### Send a Nextcloud file by email

```bash
nexlink files download /Documents/offer.pdf /tmp/
nexlink mail send --to "client@example.com" --subject "Offer" --body "Please see attached." --attach /tmp/offer.pdf
```

#### Save an email attachment into Nextcloud

```bash
nexlink mail download-attachment --id EMAIL_ID --name "contract.pdf" --output /tmp/
nexlink files upload /tmp/contract.pdf /Contracts/
```

#### Turn a document into follow-up tasks

```bash
nexlink files extract-actions /Clients/contract.txt
nexlink files create-tasks-from-file /Clients/contract.txt --select 1,2 --execute
```

## Configuration

### Exchange

```bash
export EXCHANGE_SERVER="https://mail.your-domain.com/EWS/Exchange.asmx"
export EXCHANGE_USERNAME="service-account"
export EXCHANGE_PASSWORD="your-password"
export EXCHANGE_EMAIL="service-account@your-domain.com"
export OWNER_EMAIL="owner@your-domain.com"  # Optional: recipient for notifications (defaults to EXCHANGE_EMAIL)
export EXCHANGE_VERIFY_SSL="false"   # only for self-signed certificates
```

### Nextcloud

```bash
export NEXTCLOUD_URL="https://cloud.your-domain.com"
export NEXTCLOUD_USERNAME="your-username"
export NEXTCLOUD_APP_PASSWORD="your-app-password"
```

For full setup details, see [references/setup.md](references/setup.md).

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for the full version history. Latest: v0.14.1.

## Installation options

### From Git

```bash
cd ~/.openclaw/skills/
git clone https://github.com/asistent-alex/openclaw-nexlink.git
cd openclaw-nexlink
pip3 install -r requirements.txt
```

### From ClawHub

Use the published listing/slug once the public package is live on ClawHub. The public title is intended to be:

**Firma de AI — Nextcloud, Exchange & YouTube Assistant**

The CLI command remains:

```bash
nexlink
```

## Brand positioning

For public listings, release notes, and marketing copy, prefer:

- **Title:** Firma de AI — Nextcloud, Exchange & YouTube Assistant
- **Subtitle:** Email, files, tasks, transcripts, and document workflows for teams
- **Brand line:** Built by Firma de AI, supported by Firma de IT.
- **Links:** https://firmade.ai · https://firmade.it

## License

MIT — see [LICENSE](LICENSE).

This project follows the [Hardshell Coding Standards](https://github.com/asistent-alex/openclaw-hardshell).

---

<div align="center">

**Built by [Firma de AI](https://firmade.ai), supported by [Firma de IT](https://firmade.it)**  
*Nextcloud, Exchange, YouTube — one assistant.*

[Hardshell](https://github.com/asistent-alex/openclaw-hardshell) · [prompt-to-pr](https://github.com/asistent-alex/openclaw-prompt-to-pr) · [Report Bug](https://github.com/asistent-alex/openclaw-nexlink/issues) · [Request Feature](https://github.com/asistent-alex/openclaw-nexlink/issues)

</div>
