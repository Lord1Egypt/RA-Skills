---
name: hubspot-crm
description: Full HubSpot CRM automation — contacts, deals, companies, activities, and pipeline reports via the HubSpot API.
---
# HubSpot CRM

Automate your entire HubSpot CRM from the command line. Create and manage contacts, deals, and companies; log activities (calls, emails, meetings, notes); and pull pipeline reports with conversion rates — all via the official HubSpot API with a single Bearer token.

## Setup

Set your HubSpot Private App token as an environment variable:

```bash
export HUBSPOT_API_KEY="pat-na1-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

Get your token: HubSpot → Settings → Integrations → Private Apps → Create a private app.
Required scopes: `crm.objects.contacts`, `crm.objects.deals`, `crm.objects.companies`, `crm.schemas.contacts`, `sales-email-read`.

## Commands / Usage

```bash
# ── CONTACTS ────────────────────────────────────────────
# List contacts (default 20, up to 100)
python3 scripts/hubspot_crm.py contacts-list
python3 scripts/hubspot_crm.py contacts-list --limit 50

# Search contacts by email or name
python3 scripts/hubspot_crm.py contacts-search --query "john@example.com"
python3 scripts/hubspot_crm.py contacts-search --query "John Smith"

# Create a contact
python3 scripts/hubspot_crm.py contacts-create --email "jane@acme.com" --firstname "Jane" --lastname "Doe" --phone "+1-555-0100" --company "Acme"

# Update a contact
python3 scripts/hubspot_crm.py contacts-update --id 12345 --phone "+1-555-9999" --jobtitle "CTO"

# Delete a contact
python3 scripts/hubspot_crm.py contacts-delete --id 12345

# ── DEALS ───────────────────────────────────────────────
# List all deals
python3 scripts/hubspot_crm.py deals-list
python3 scripts/hubspot_crm.py deals-list --limit 50

# Create a deal
python3 scripts/hubspot_crm.py deals-create --name "Acme Enterprise License" --stage "appointmentscheduled" --amount 12000 --contact-id 12345

# Update a deal
python3 scripts/hubspot_crm.py deals-update --id 67890 --stage "closedwon" --amount 15000

# Move deal stage
python3 scripts/hubspot_crm.py deals-move-stage --id 67890 --stage "contractsent"

# List pipeline stages
python3 scripts/hubspot_crm.py pipeline-list

# ── COMPANIES ───────────────────────────────────────────
# Create a company
python3 scripts/hubspot_crm.py companies-create --name "Acme Corp" --domain "acme.com" --industry "TECHNOLOGY"

# Search companies
python3 scripts/hubspot_crm.py companies-search --query "Acme"

# Associate contact with company
python3 scripts/hubspot_crm.py companies-associate --company-id 11111 --contact-id 22222

# ── ACTIVITIES ──────────────────────────────────────────
# Log an email activity
python3 scripts/hubspot_crm.py log-email --contact-id 12345 --subject "Follow-up" --body "Hi Jane, just checking in..."

# Log a call
python3 scripts/hubspot_crm.py log-call --contact-id 12345 --duration 300 --notes "Discussed pricing, very interested"

# Log a meeting
python3 scripts/hubspot_crm.py log-meeting --contact-id 12345 --title "Demo call" --notes "Showed product, positive feedback"

# Log a note
python3 scripts/hubspot_crm.py log-note --contact-id 12345 --body "Called and left voicemail"

# ── REPORTS ─────────────────────────────────────────────
# Get deal pipeline summary
python3 scripts/hubspot_crm.py report-pipeline

# Get conversion rates per stage
python3 scripts/hubspot_crm.py report-conversions
```

## Requirements

- Python 3.8+
- `requests` (standard: `pip install requests`)
- `HUBSPOT_API_KEY` environment variable
