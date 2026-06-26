---
name: outreach-crm
description: Track leads locally, manage outreach campaigns, and export as CSV for download.
version: 1.0.0
author: ModelFitAI <skills@modelfitai.com>
license: MIT
keywords: [openclaw, skill, crm, lead-gen, outreach, csv, sales]
requires: {}
---

# Outreach CRM Skill

Manage lead generation outreach. Leads are stored in a local JSON file inside the agent workspace — no external database required. Users can view leads in chat or export them as a CSV file.

## Available Tools

Run with Node.js: `node {baseDir}/outreach-crm.js <command> [args]`

- **add-lead** - Add a new lead to the local leads file
- **list** - List all tracked leads (displays in chat)
- **log** - Log an interaction with a lead
- **export-csv** - Export all leads to a CSV file and print the file path
- **clear** - Remove all leads (use with caution)

## Usage

```bash
node {baseDir}/outreach-crm.js add-lead --name "John" --source "twitter" --handle "@john" --score 75 --tier hot
node {baseDir}/outreach-crm.js list
node {baseDir}/outreach-crm.js log <lead_id> "Sent intro DM"
node {baseDir}/outreach-crm.js export-csv
```

## Storage

Leads are saved to `/root/.openclaw/workspace/leads.json` inside the container.
CSV exports are written to `/root/.openclaw/workspace/leads.csv`.
Always show the user the export path so they can download it.
