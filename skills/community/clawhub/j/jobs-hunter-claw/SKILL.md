---
name: jobs-hunter-claw
description: Unified job hunting automation with Google Sheets — discover jobs, submit applications, and track your pipeline with activity logging. Use when: (1) searching job boards (LinkedIn, Indeed, BuiltIn), (2) tracking application status and interviews, (3) logging recruiter contacts and follow-ups, (4) querying jobs by status/company/role, (5) automating periodic job pipeline checks via cron. Requires Google Sheets + gog CLI. Recommended model: google/gemini-flash-latest.
metadata:
  openclaw:
    emoji: "🎯"
    requires:
      bins: ["gog", "bash"]
    install:
      - id: clawhub
        kind: clawhub
        slug: jobs-hunter-claw
        label: "Install via ClawHub"
---

# Jobs Hunter Claw 🎯

Unified skill for job hunting automation: **Discover → Apply → Track**.

**ClawHub:** https://clawhub.ai/QuantDeveloperUSA/jobs-hunter-claw  
**GitHub:** https://github.com/ABFS-Inc/jobs-hunter-claw

## Installation

### Option 1: ClawHub (Recommended)

```bash
# Install the skill
clawhub install jobs-hunter-claw

# Verify installation
clawhub list

# Fix executable permission (required after install)
chmod +x /path/to/skills/jobs-hunter-claw/scripts/job-tracker.sh
```

### Option 2: Git Clone

```bash
# Clone to your skills directory
git clone https://github.com/ABFS-Inc/jobs-hunter-claw.git /path/to/skills/jobs-hunter-claw
```

## Prerequisites

### 1. gog CLI (Google Workspace)

The skill uses `gog` for Google Sheets access:

```bash
# Install gog
brew install steipete/tap/gogcli

# Authenticate with Google
gog auth credentials /path/to/client_secret.json
gog auth add your@gmail.com --services sheets
```

### 2. Google Sheet Setup

Create a Google Sheet with these tabs:

| Tab | Purpose |
|-----|---------|
| **Jobs** | Main tracker (columns A-P) |
| **Activity Log** | Timestamped event history |
| **Add or Edit Job** | Form interface (optional) |

See [references/google-sheet-setup.md](references/google-sheet-setup.md) for detailed setup.

### 3. Configure Spreadsheet ID (Required)

Set the environment variable with your Google Sheet ID:

```bash
export JOB_TRACKER_SPREADSHEET_ID="your-google-sheet-id"
```

The ID is found in your Google Sheet URL:
```
https://docs.google.com/spreadsheets/d/[THIS-IS-THE-ID]/edit
```

**For persistent configuration**, add to your shell profile (`~/.bashrc`, `~/.zshrc`):

```bash
echo 'export JOB_TRACKER_SPREADSHEET_ID="your-google-sheet-id"' >> ~/.bashrc
```

**For OpenClaw agents**, set in the agent's environment or TOOLS.md.

## Quick Start

```bash
# Set your spreadsheet ID first
export JOB_TRACKER_SPREADSHEET_ID="your-google-sheet-id"

# View all commands
./scripts/job-tracker.sh help

# Add a discovered job
./scripts/job-tracker.sh add --company "Morgan Stanley" --role "AI Architect" --source LinkedIn

# List active interviews
./scripts/job-tracker.sh list --status interview

# Log an event
./scripts/job-tracker.sh log JOB002 --event interview_scheduled --details "3rd round Monday 10am"

# Search jobs
./scripts/job-tracker.sh search "citi" --columns company,role
```

## Agent Setup

Create a dedicated agent to run job hunting automation.

### Model Requirement

**This skill requires `google/gemini-flash-latest`** for optimal performance and cost efficiency.

Gemini Flash provides:
- Fast response times for frequent job board scanning
- Cost-effective for high-volume cron jobs (hourly scans, daily reviews)
- Sufficient capability for structured data operations (CRUD, search, logging)
- Good tool-use performance for shell command execution

**Do not use** Opus, Sonnet, or other premium models — they're overkill for this skill and will incur unnecessary costs.

### 1. Create the Agent

```bash
openclaw agents create job-hunter \
  --model google/gemini-flash-latest \
  --workspace /path/to/workspace-job-hunter
```

### 2. Configure Agent Identity

Create `IDENTITY.md` in the agent workspace:

```markdown
# IDENTITY.md

- **Name:** [First Name] [Last Name]
- **Creature:** Career automation assistant
- **Vibe:** Proactive, organized, candidate-focused
- **Emoji:** 🎯
```

### 3. Configure Agent Tools

Create `TOOLS.md` in the agent workspace with the spreadsheet ID:

```markdown
# TOOLS.md

## Environment Variables

Set before running job-tracker commands:
- `JOB_TRACKER_SPREADSHEET_ID` — Your Google Sheet ID

## Jobs Hunter Claw Skill

**Installed at:** `/openclaw/skills/jobs-hunter-claw`

### Usage

```bash
# Set spreadsheet ID
export JOB_TRACKER_SPREADSHEET_ID="your-sheet-id"

# Run commands
/openclaw/skills/jobs-hunter-claw/scripts/job-tracker.sh list
/openclaw/skills/jobs-hunter-claw/scripts/job-tracker.sh add --company "X" --role "Y"
```

## Google Sheet

- **URL:** https://docs.google.com/spreadsheets/d/your-sheet-id
- **Tabs:** Jobs, Activity Log, Add or Edit Job
```

### 4. Configure Heartbeat (Optional)

Create `HEARTBEAT.md` for periodic checks:

```markdown
# HEARTBEAT.md

## Periodic Checks
- [ ] Scan email for recruiter messages
- [ ] Check calendar for upcoming interviews
- [ ] Review jobs with status "Interview" for follow-ups
- [ ] Look for new job postings matching profile
```

## Cron Job Setup

Automate job hunting tasks with OpenClaw cron jobs.

**Important:** Cron jobs need the spreadsheet ID in the task prompt or agent environment.

### Job 1: Email Scan (Hourly, Business Hours)

```bash
openclaw cron add \
  --id job-email-scan \
  --schedule "0 14-23 * * 1-5" \
  --agent job-hunter \
  --channel "channel:YOUR_DISCORD_CHANNEL_ID" \
  --task "Set JOB_TRACKER_SPREADSHEET_ID from TOOLS.md, then scan email for job-related messages. Use /openclaw/skills/jobs-hunter-claw/scripts/job-tracker.sh for updates."
```

Schedule: Every hour from 9 AM - 6 PM EST (14-23 UTC), Monday-Friday.

### Job 2: Weekly Pipeline Review (Monday Morning)

```bash
openclaw cron add \
  --id job-weekly-review \
  --schedule "0 14 * * 1" \
  --agent job-hunter \
  --channel "channel:YOUR_DISCORD_CHANNEL_ID" \
  --task "Weekly pipeline review. Set JOB_TRACKER_SPREADSHEET_ID, then:
1. job-tracker.sh list --status Interview
2. job-tracker.sh list --status Applied
3. job-tracker.sh list --status Discovered
Report summary and recommended actions."
```

Schedule: Monday 9 AM EST (14:00 UTC).

### Managing Cron Jobs

```bash
# List all cron jobs
openclaw cron list

# Pause/resume a job
openclaw cron pause job-email-scan
openclaw cron resume job-email-scan

# Delete a job
openclaw cron delete job-email-scan
```

## CLI Reference

### Commands

| Command | Description |
|---------|-------------|
| `add` | Add new job with auto-generated ID |
| `update` | Modify existing job fields |
| `delete` | Delete a job (clears row, preserves logs) |
| `log` | Add timestamped activity entry |
| `show` | Display detailed job view |
| `list` | List jobs with optional filters |
| `search` | Search with regex or fuzzy matching |
| `logs` | View activity history |
| `next-id` | Get next available job ID |
| `schema` | Show valid statuses and event types |
| `help` | Show command help |

### Adding a Job

```bash
./scripts/job-tracker.sh add \
  --company "Goldman Sachs" \
  --role "VP, AI Engineering" \
  --location "NYC" \
  --salary "$200k-$275k" \
  --source "LinkedIn" \
  --url "https://linkedin.com/jobs/view/123456" \
  --status Discovered
```

Required: `--company`, `--role`

### Updating a Job

```bash
./scripts/job-tracker.sh update JOB015 \
  --status Applied \
  --resume "AI-Architect-Resume-v3" \
  --applied-date "2026-03-19"
```

### Logging Activity

```bash
./scripts/job-tracker.sh log JOB015 \
  --event interview_scheduled \
  --details "3rd round with VP Engineering, Monday 10am"
```

### Deleting a Job

```bash
# Delete with confirmation prompt
./scripts/job-tracker.sh delete JOB015

# Delete without confirmation (for scripts/automation)
./scripts/job-tracker.sh delete JOB015 --force
```

Note: Delete clears the row data but preserves the activity log history.

### Searching Jobs

```bash
# Simple text search
./scripts/job-tracker.sh search "goldman"

# Search specific columns
./scripts/job-tracker.sh search "AI.*Architect" --columns role --regex

# Fuzzy search
./scripts/job-tracker.sh search "goldmn" --fuzzy
```

### Filtering Jobs

```bash
# By status
./scripts/job-tracker.sh list --status interview

# Limit results
./scripts/job-tracker.sh list --limit 10

# JSON output
./scripts/job-tracker.sh list --json
```

## Validation Rules

### Status Values (Title Case)

| Status | Meaning |
|--------|---------|
| `Discovered` | Found but not yet applied |
| `Applied` | Application submitted |
| `Screening` | Initial review/HR screen |
| `Interview` | Active interview process |
| `Karat Test Scheduled` | Technical assessment pending |
| `Offer` | Offer received |
| `Rejected` | Not selected |
| `Withdrawn` | Candidate withdrew |
| `Accepted` | Offer accepted |
| `Closed` | Position no longer available |

The CLI auto-normalizes status to Title Case (`interview` → `Interview`).

### Event Types (lowercase)

| Event | Meaning |
|-------|---------|
| `discovered` | Initial job discovery |
| `applied` | Application submitted |
| `recruiter_contact` | Recruiter reached out |
| `user_reply` | You responded to recruiter |
| `interview_scheduled` | Interview booked |
| `interview_completed` | Interview done |
| `test_scheduled` | Assessment booked |
| `test_completed` | Assessment done |
| `offer_received` | Offer extended |
| `rejection` | Application rejected |
| `follow_up` | Follow-up action needed |
| `status_change` | Status was updated |
| `note` | General note |

### Contact Validation

Contacts must be Google Contacts links:
```
https://contacts.google.com/person/c[alphanumeric]
```

Bypass with `--no-strict-contacts` flag.

## Google Apps Script (Optional)

For manual job entry via the Google Sheet form tab, install the Apps Script:

1. Open your Google Sheet
2. Go to **Extensions → Apps Script**
3. Delete existing code in `Code.gs`
4. Paste contents of `scripts/job-tracker-appscript.js`
5. Click **Save**
6. Refresh the Google Sheet
7. Use the new **🎯 Job Tracker** menu

### Menu Functions

- **➕ Add Job** — Creates job from form fields
- **📥 Load Job to Edit** — Loads existing job into form
- **💾 Save Changes** — Saves form changes back
- **📝 Add Log Entry** — Adds activity log
- **🧹 Clear Form** — Clears form fields
- **🔄 Refresh Next ID** — Updates ID counter
- **⚙️ Setup Data Validation** — Adds dropdowns (run once)

## Files

```
jobs-hunter-claw/
├── SKILL.md                           # This file
├── README.md                          # GitHub readme
├── scripts/
│   ├── job-tracker.sh                 # CLI for CRUD operations
│   └── job-tracker-appscript.js       # Google Apps Script
└── references/
    └── google-sheet-setup.md          # Sheet setup guide
```

## Troubleshooting

### "JOB_TRACKER_SPREADSHEET_ID environment variable is required"

Set the environment variable:
```bash
export JOB_TRACKER_SPREADSHEET_ID="your-google-sheet-id"
```

### "gog: command not found"

Install gog CLI:
```bash
brew install steipete/tap/gogcli
```

### "Google API error (403)"

Authenticate gog with Sheets access:
```bash
gog auth add your@gmail.com --services sheets
```

### "Permission denied" when running job-tracker.sh

Fix executable permission:
```bash
chmod +x /path/to/skills/jobs-hunter-claw/scripts/job-tracker.sh
```

### Cron jobs not delivering to Discord

Use the full channel format: `channel:CHANNEL_ID` (not just `discord`).

## Version History

- **1.4.0** — Specified `google/gemini-flash-latest` as required model for cost efficiency
- **1.3.0** — Added `delete` command for removing jobs; uses `gog sheets clear` for proper row clearing
- **1.2.0** — Removed hardcoded spreadsheet ID, now requires `JOB_TRACKER_SPREADSHEET_ID` env var
- **1.1.0** — Added agent setup and cron job documentation
- **1.0.2** — File extensions fixed for ClawHub compatibility
- **1.0.0** — Initial release
