---
name: nex-crm
description: Chat-native Customer Relationship Management system designed for one-person agencies, freelancers, and small Belgian businesses managing multiple client relationships and complex sales pipelines. Track all prospects and leads through the complete sales funnel with stage progression (lead, contacted, demo scheduled, demo completed, proposal sent, negotiation, won, lost, churned) along with activity logging, follow-up reminders, and comprehensive interaction history. Automatically remember conversation context and activity details from natural language input, store lead source information with categorization (web scraping, referrals, inbound inquiries, outreach, events, website submissions), and assign priority levels (hot, warm, cold) to prospects. Monitor your sales pipeline with visual ASCII bar charts showing deal counts and revenue potential per stage, track win rates and average deal sizes, identify revenue forecasts, and discover stale prospects who haven't been contacted in over two weeks. Log all activities (calls, emails, meetings, demos, proposals) with timestamps and detailed summaries, set follow-up reminders with configurable dates or day counts, manage interaction channels (Telegram, email, phone), export prospect data for external reporting. Perfect for Belgian SMEs, web agencies, and service providers who need lightweight CRM without expensive subscriptions.
version: 1.0.0
metadata:
  clawdbot:
    emoji: "\U0001F4BC"
    requires:
      bins:
        - python3
      env: []
    primaryEnv: ""
    homepage: https://nex-ai.be
    files:
      - "nex-crm.py"
      - "lib/*"
      - "setup.sh"
---

# Nex CRM

Chat-native CRM for one-person agencies and freelancers. Prospect tracking, pipeline management, conversation memory, and conversational activity logging. All prospect data stays local on your machine.

## When to Use

Use this skill when the user asks about:

- Adding new prospects, leads, or customers
- Viewing prospect details, contact information, or sales history
- Listing prospects with filters (by stage, priority, source)
- Updating prospect stage (lead, contacted, demo scheduled, proposal sent, won, lost)
- Logging activities (calls, emails, meetings, demos, proposals)
- Managing follow-ups and reminders
- Searching for prospects by company name, location, contact, or notes
- Pipeline overview and statistics (win rate, deal size, revenue)
- Tracking deals through the sales funnel
- Exporting prospect data for reporting
- Creating interaction records from conversations
- Setting reminders and follow-up dates
- Monitoring stale prospects (no contact > 14 days)
- Managing customer relationships and dealing with Belgian SMEs

Trigger phrases: "add prospect", "add lead", "new customer", "add klant", "show prospect", "list prospects", "pipeline", "follow-up", "demo scheduled", "proposal sent", "deal won", "deal lost", "log call", "log email", "log activity", "search prospect", "contact Jan", "when did I last contact", "stage update", "deal status", "sales pipeline", "how many prospects", "export prospects", "CRM", "klanten", "prospects", "offerte", "demo"

## Quick Setup

If the database does not exist yet, run the setup script:

```bash
bash setup.sh
```

This creates the data directory, installs dependencies in a virtual environment, initializes the database, and sets up the CLI tool.

## Available Commands

The CLI tool is `nex-crm`. All commands output plain text or JSON as specified.

### Add Prospect

Create a new prospect from natural language or structured data:

```bash
# Natural language
nex-crm add "nieuwe lead Bakkerij Peeters, Gent, website nodig"
nex-crm add "ECHO Management, Jan contact, jan@echo.be, +32 471 123456, warm, 799"

# Structured format
nex-crm add --company "ECHO Management" --contact "Jan" --email "jan@echo.be" --phone "+32 471 123456" --source scrape --priority warm --value 799
```

### Show Prospect

Display prospect details with full timeline:

```bash
nex-crm show "ECHO Management"
nex-crm show 42
nex-crm show "ECHO Management" --output json
```

Output shows: company info, contact details, current stage, priority, value, last contact, next follow-up, and recent activities.

### List Prospects

List prospects with optional filtering:

```bash
nex-crm list
nex-crm list --stage proposal_sent
nex-crm list --priority hot
nex-crm list --stale
nex-crm list --source scrape
nex-crm list --output json
```

### Update Stage

Move a prospect through the pipeline:

```bash
nex-crm stage "ECHO Management" demo_scheduled
nex-crm stage "Bakkerij Peeters" won --reason "Starter pakket 299/maand"
nex-crm stage "TechnoFix" lost --reason "Te duur"
```

### Log Activity

Log a call, email, meeting, or note for a prospect:

```bash
# Natural language
nex-crm log "had a call with Jan from ECHO Management, interested in premium package"

# Structured
nex-crm log --prospect "ECHO Management" --type call --summary "Discussed premium package, wants demo next week"
nex-crm log --prospect "Bakkerij Peeters" --type email --summary "Sent intro email with portfolio"
```

### Manage Follow-ups

Schedule and view follow-ups:

```bash
nex-crm follow-up
nex-crm follow-up "ECHO Management" --date 2026-04-10
nex-crm follow-up "ECHO Management" --in 3
```

### Search Prospects

Search by text across company name, contact, email, or notes:

```bash
nex-crm search "website"
nex-crm search "Gent"
```

### Pipeline Overview

View pipeline status with counts and values per stage:

```bash
nex-crm pipeline
```

Shows ASCII bar chart with counts and monthly recurring value per stage, total pipeline value, and win rate.

### Statistics

View CRM statistics:

```bash
nex-crm stats
nex-crm stats --since 2026-01-01
```

Shows active prospects, won deals, total revenue, average deal size, and lead source diversity.

### Export

Export all prospects:

```bash
nex-crm export csv
nex-crm export json
```

### Store Interaction

Store a conversation or message exchange:

```bash
nex-crm interact "ECHO Management" --channel telegram --message "Jan confirmed demo for Thursday 2pm" --direction inbound
```

### Set Reminder

Set a reminder for a prospect:

```bash
nex-crm remind "ECHO Management" --date 2026-04-10 --message "Send proposal after demo"
```

### Configuration

Show CRM configuration:

```bash
nex-crm config show
```

## Example Interactions

**Scenario 1: Lead from web scraping**
User: "Add a new lead from my scraping: Bakkerij Peeters in Gent, need a website"
Agent: `nex-crm add "nieuwe lead Bakkerij Peeters, Gent, website nodig"`
Agent: "Prospect added: Bakkerij Peeters (ID: 1)"

**Scenario 2: Logged a call**
User: "I just called ECHO Management and spoke with Jan about our premium package"
Agent: `nex-crm log "had a call with Jan from ECHO Management about premium package"`
Agent: "Activity logged for ECHO Management"

**Scenario 3: Stage update - demo scheduled**
User: "Jan wants to see a demo, schedule it for next Thursday"
Agent: `nex-crm stage "ECHO Management" demo_scheduled`
Agent: `nex-crm follow-up "ECHO Management" --in 7`
Agent: "ECHO Management moved to Demo Scheduled"

**Scenario 4: Win a deal**
User: "Great news! ECHO Management signed up for the 799 growth package"
Agent: `nex-crm stage "ECHO Management" won --reason "Growth pakket 799/maand"`
Agent: "ECHO Management moved to Won"

**Scenario 5: Check pipeline**
User: "How are our sales looking this month?"
Agent: `nex-crm pipeline`
Agent: Shows pipeline overview with stage breakdown and win rate

**Scenario 6: Find stale prospects**
User: "Who haven't we contacted recently?"
Agent: `nex-crm list --stale`
Agent: Lists prospects with no contact > 14 days

**Scenario 7: Search by location**
User: "Show me all the prospects in Brussels"
Agent: `nex-crm search "Brussel"`
Agent: Lists matching prospects

**Scenario 8: Log Telegram message**
User: "I got a message from Bakkerij Peeters on Telegram asking about pricing"
Agent: `nex-crm interact "Bakkerij Peeters" --channel telegram --message "asking about pricing" --direction inbound`
Agent: "Interaction logged for Bakkerij Peeters"

**Scenario 9: Set follow-up reminder**
User: "Remind me to follow up with TechnoFix in 3 days"
Agent: `nex-crm follow-up "TechnoFix" --in 3`
Agent: "Follow-up set for TechnoFix on 2026-04-08"

**Scenario 10: Export for reporting**
User: "I need to export all prospects for my quarterly report"
Agent: `nex-crm export csv`
Agent: "Exported to ~/.nex-crm/exports/prospects-20260405.csv"

## Output Parsing

All CLI output is plain text, structured for easy parsing:

- Section headers followed by `---` or `===` separators
- List items with consistent columns
- Timestamps in ISO-8601 format
- Every command output ends with `[Nex CRM by Nex AI | nex-ai.be]`

When presenting output to the user, strip the footer line and present the information naturally.

## Important Notes

- All prospect data is stored locally at `~/.nex-crm/`. No telemetry, no analytics.
- No external API calls are made. All data stays on your machine.
- The database is SQLite3, easily portable and backupable.
- Pipeline stages: lead, contacted, demo_scheduled, demo_done, proposal_sent, negotiation, won, lost, churned
- Priority levels: hot, warm, cold
- Lead sources: scrape, referral, inbound, outreach, event, website, other
- Activity types: call, email, meeting, demo, note, follow_up, proposal, invoice
- Retainer tiers matching Nex AI pricing: starter (299), growth (799), premium (1499), enterprise (2499)
- Stale prospects: no contact for 14+ days (configurable)

## Troubleshooting

- **"Database not found"**: Run `bash setup.sh` to initialize
- **"Prospect not found"**: Use exact company name or prospect ID from `nex-crm list`
- **"Invalid stage"**: Valid stages are: lead, contacted, demo_scheduled, demo_done, proposal_sent, negotiation, won, lost, churned
- **No prospects showing**: Check if they match filters (stage, priority, source)
- **Lost data**: Make sure `~/.nex-crm/` directory is accessible and has write permissions

## Credits

Built by Nex AI (https://nex-ai.be) - Digital transformation for Belgian SMEs.
Author: Kevin Blancaflor
