# Nex CRM

**Chat-native CRM for one-person agencies and freelancers.**

Prospect tracking, pipeline management, conversation memory, and conversational activity logging. All data stays local on your machine.

Built by **Nex AI** - Digital transformation for Belgian SMEs.

## What It Does

- Add prospects and manage contact information from natural language or structured data
- Track prospects through a complete sales pipeline (lead -> contacted -> demo -> proposal -> won/lost)
- Log activities (calls, emails, meetings, demos, proposals) with conversational memory
- Schedule follow-ups and set reminders for prospect outreach
- Search prospects by company name, location, contact, or notes
- Manage pipeline overview with counts, values, and win rate statistics
- Export prospect data for reporting in CSV or JSON format
- Store conversations and interactions from multiple channels
- All data stays local on your machine. No telemetry. You own your data.

## Quick Install

```bash
# Via ClawHub
clawhub install nex-crm

# Or manual
git clone <repo-url>
cd nex-crm
bash setup.sh
```

## Example Usage

Ask your AI agent to manage your CRM:

```
You: Add a new lead from my scraping: Bakkerij Peeters in Gent, need a website
Agent: Prospect added: Bakkerij Peeters (ID: 1)

You: I just called Jan from ECHO Management, very interested in the growth package
Agent: Activity logged for ECHO Management

You: Move ECHO Management to demo scheduled
Agent: ECHO Management moved to Demo Scheduled

You: Show me our sales pipeline
Agent: [Shows pipeline overview with counts and values per stage]

You: How many prospects are stale?
Agent: [Shows prospects with no contact > 14 days]

You: Export all prospects to CSV
Agent: Exported to ~/.nex-crm/exports/prospects-20260405.csv
```

## Configuration

After installation, configure your CRM settings:

```bash
nex-crm config show
```

Data directory: `~/.nex-crm/`
Database: `~/.nex-crm/crm.db`

## Quick Commands

```bash
# Add a prospect
nex-crm add "nieuwe lead Company Name, Gent, needs X"
nex-crm add --company "Company" --contact "Person" --email "email@domain.be" --priority warm

# List prospects
nex-crm list
nex-crm list --stage proposal_sent
nex-crm list --priority hot
nex-crm list --stale

# Update a prospect
nex-crm stage "Company" demo_scheduled
nex-crm stage "Company" won --reason "Growth package 799/mo"

# Log activities
nex-crm log "had a call with Jan about pricing"
nex-crm log --prospect "Company" --type email --summary "Sent proposal"

# Manage follow-ups
nex-crm follow-up "Company" --in 3
nex-crm follow-up

# View pipeline
nex-crm pipeline
nex-crm stats

# Search
nex-crm search "Gent"

# Export
nex-crm export csv
nex-crm export json
```

## Pipeline Stages

1. **Lead** - New prospect, initial contact
2. **Contacted** - Initial outreach completed
3. **Demo Scheduled** - Demo meeting scheduled
4. **Demo Done** - Demo completed
5. **Proposal Sent** - Proposal/quote sent
6. **Negotiation** - In negotiation phase
7. **Won** - Deal closed
8. **Lost** - Deal lost (end state)
9. **Churned** - Customer churned (end state)

## Retainer Tiers

Nex AI standard pricing tiers:

- **Starter** - EUR 299/month
- **Growth** - EUR 799/month
- **Premium** - EUR 1,499/month
- **Enterprise** - EUR 2,499/month

## For Your Agents

When the user asks to add a prospect, log an activity, update a stage, or check the pipeline:

1. Use the natural language `nex-crm add` command when possible
2. For structured operations, use flags: `--stage`, `--priority`, `--source`
3. When viewing data, use `--output json` for programmatic access
4. Always show `nex-crm follow-up` results to keep users on top of follow-ups
5. Use `nex-crm pipeline` to answer "how is sales looking?" questions
6. Use `nex-crm search` to find prospects by text (location, contact name, etc.)

## Data Privacy

- All prospect data is stored locally in SQLite3 at `~/.nex-crm/`
- No external services are contacted
- No analytics, telemetry, or tracking
- Database is fully portable and backupable
- You own your data completely

## Support

Built by Nex AI (https://nex-ai.be)

For issues or feature requests, please contact: hello@nex-ai.be
