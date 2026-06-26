---
name: hubspot-by-altf1be
description: "Full HubSpot platform CLI — CRM contacts/companies/deals/tickets, CMS blog posts/pages, Marketing emails/forms/lists, Conversations, Automation workflows. Private App token or OAuth 2.0 auth."
homepage: https://github.com/ALT-F1-OpenClaw/openclaw-skill-hubspot-by-altf1be
metadata:
  {"openclaw": {"emoji": "🟠", "requires": {"env": ["HUBSPOT_ACCESS_TOKEN"]}, "optional": {"env": ["HUBSPOT_CLIENT_ID", "HUBSPOT_CLIENT_SECRET", "HUBSPOT_REFRESH_TOKEN", "HUBSPOT_MAX_RESULTS"]}, "primaryEnv": "HUBSPOT_ACCESS_TOKEN"}}
---

# HubSpot by @altf1be

Full HubSpot platform CLI covering CRM, CMS, Marketing, Conversations, and Automation.

## Setup

1. Create a Private App in HubSpot: Settings > Integrations > Private Apps
2. Set environment variables (or create `.env` in `{baseDir}`):

```
# Required (Private App mode)
HUBSPOT_ACCESS_TOKEN=pat-na1-xxxxxxxx

# OR use OAuth 2.0 mode (set all three):
# HUBSPOT_CLIENT_ID=your-client-id
# HUBSPOT_CLIENT_SECRET=your-client-secret
# HUBSPOT_REFRESH_TOKEN=your-refresh-token

# Optional
# HUBSPOT_MAX_RESULTS=100
```

3. Configure the required **Private App scopes** in HubSpot (Settings > Integrations > Private Apps > your app > Scopes):

| Scope | Description |
|---|---|
| `crm.objects.contacts.read` | View properties and other details about contacts |
| `crm.objects.contacts.write` | Create, delete, or make changes to contacts |
| `crm.objects.companies.read` | View properties and other details about companies |
| `crm.objects.companies.write` | Create, delete, or make changes to companies |
| `crm.objects.deals.read` | View properties and other details about deals |
| `crm.objects.deals.write` | Create, delete, or make changes to deals |
| `crm.objects.owners.read` | View details about users assigned to a CRM record |
| `crm.schemas.contacts.read` | View details about property settings for contacts |
| `crm.schemas.companies.read` | View details about property settings for companies |
| `crm.schemas.deals.read` | View details about property settings for deals |
| `tickets` | View, create, delete, or make changes to tickets |
| `automation` | Workflows |
| `content` | Sites, landing pages, CTA, email, blog, campaigns |
| `conversations.read` | View messages, comments, threads, recipient/user/assignment details |
| `forms` | Access to the Forms API |

4. Install dependencies: `cd {baseDir} && npm install`

## Commands

### CRM — Contacts

```bash
# List contacts
node {baseDir}/scripts/hubspot.mjs contacts list

# Search contacts by email
node {baseDir}/scripts/hubspot.mjs contacts search --query "john@example.com"

# Read contact details
node {baseDir}/scripts/hubspot.mjs contacts read --id 123

# Create a contact
node {baseDir}/scripts/hubspot.mjs contacts create --email "jane@example.com" --firstname Jane --lastname Doe

# Update a contact
node {baseDir}/scripts/hubspot.mjs contacts update --id 123 --phone "+1234567890"

# Delete a contact (requires --confirm)
node {baseDir}/scripts/hubspot.mjs contacts delete --id 123 --confirm
```

### CRM — Companies

```bash
node {baseDir}/scripts/hubspot.mjs companies list
node {baseDir}/scripts/hubspot.mjs companies search --query "Acme"
node {baseDir}/scripts/hubspot.mjs companies read --id 456
node {baseDir}/scripts/hubspot.mjs companies create --name "Acme Corp" --domain "acme.com"
node {baseDir}/scripts/hubspot.mjs companies update --id 456 --industry "Technology"
node {baseDir}/scripts/hubspot.mjs companies delete --id 456 --confirm
```

### CRM — Deals

```bash
node {baseDir}/scripts/hubspot.mjs deals list
node {baseDir}/scripts/hubspot.mjs deals search --query "Enterprise"
node {baseDir}/scripts/hubspot.mjs deals read --id 789
node {baseDir}/scripts/hubspot.mjs deals create --name "Big Deal" --amount 50000 --stage appointmentscheduled
node {baseDir}/scripts/hubspot.mjs deals update --id 789 --stage closedwon
node {baseDir}/scripts/hubspot.mjs deals delete --id 789 --confirm
```

### CRM — Tickets

```bash
node {baseDir}/scripts/hubspot.mjs tickets list
node {baseDir}/scripts/hubspot.mjs tickets search --query "Bug"
node {baseDir}/scripts/hubspot.mjs tickets read --id 101
node {baseDir}/scripts/hubspot.mjs tickets create --subject "Login broken" --priority HIGH
node {baseDir}/scripts/hubspot.mjs tickets update --id 101 --stage 2
node {baseDir}/scripts/hubspot.mjs tickets delete --id 101 --confirm
```

### CRM — Owners

```bash
node {baseDir}/scripts/hubspot.mjs owners list
node {baseDir}/scripts/hubspot.mjs owners list --email "john@company.com"
node {baseDir}/scripts/hubspot.mjs owners read --id 55
```

### CRM — Pipelines

```bash
# List deal pipelines (default)
node {baseDir}/scripts/hubspot.mjs pipelines list

# List ticket pipelines
node {baseDir}/scripts/hubspot.mjs pipelines list --object-type tickets
```

### CRM — Associations (v4)

```bash
# List associations from contact to companies
node {baseDir}/scripts/hubspot.mjs associations list --from-type contacts --from-id 123 --to-type companies

# Create an association
node {baseDir}/scripts/hubspot.mjs associations create --from-type contacts --from-id 123 --to-type companies --to-id 456 --type-id 1

# Delete an association (requires --confirm)
node {baseDir}/scripts/hubspot.mjs associations delete --from-type contacts --from-id 123 --to-type companies --to-id 456 --confirm
```

### CRM — Properties

```bash
# List contact properties (default)
node {baseDir}/scripts/hubspot.mjs properties list

# List deal properties
node {baseDir}/scripts/hubspot.mjs properties list --object-type deals
```

### CRM — Engagements

```bash
node {baseDir}/scripts/hubspot.mjs engagements notes
node {baseDir}/scripts/hubspot.mjs engagements emails
node {baseDir}/scripts/hubspot.mjs engagements calls
node {baseDir}/scripts/hubspot.mjs engagements tasks
node {baseDir}/scripts/hubspot.mjs engagements meetings
```

### CMS — Blog Posts

```bash
node {baseDir}/scripts/hubspot.mjs blog-posts list
node {baseDir}/scripts/hubspot.mjs blog-posts list --state PUBLISHED
node {baseDir}/scripts/hubspot.mjs blog-posts read --id 1001
node {baseDir}/scripts/hubspot.mjs blog-posts create --name "My Post"
node {baseDir}/scripts/hubspot.mjs blog-posts update --id 1001 --name "Updated Title"
```

### CMS — Pages

```bash
node {baseDir}/scripts/hubspot.mjs pages list
node {baseDir}/scripts/hubspot.mjs pages read --id 2001
```

### CMS — Domains

```bash
node {baseDir}/scripts/hubspot.mjs domains list
```

### Marketing — Email Campaigns

```bash
node {baseDir}/scripts/hubspot.mjs email-campaigns list
node {baseDir}/scripts/hubspot.mjs email-campaigns read --id 3001
```

### Marketing — Forms

```bash
node {baseDir}/scripts/hubspot.mjs forms list
node {baseDir}/scripts/hubspot.mjs forms read --id 4001
```

### Marketing — Marketing Emails

```bash
node {baseDir}/scripts/hubspot.mjs marketing-emails list
node {baseDir}/scripts/hubspot.mjs marketing-emails read --id 5001
node {baseDir}/scripts/hubspot.mjs marketing-emails stats --id 5001
```

### Marketing — Contact Lists

```bash
node {baseDir}/scripts/hubspot.mjs lists list
node {baseDir}/scripts/hubspot.mjs lists read --id 6001
```

### Conversations

```bash
node {baseDir}/scripts/hubspot.mjs conversations list
node {baseDir}/scripts/hubspot.mjs conversations read --id 7001
node {baseDir}/scripts/hubspot.mjs messages list --thread-id 7001
```

### Automation — Workflows

```bash
node {baseDir}/scripts/hubspot.mjs workflows list
node {baseDir}/scripts/hubspot.mjs workflows read --id 8001
```

## Security

- Auth method: Bearer token (Private App) or OAuth 2.0 with auto-refresh
- No secrets or tokens printed to stdout
- All delete operations require explicit `--confirm` flag
- Built-in rate limiting with exponential backoff retry (3 attempts)
- OAuth tokens cached in `~/.cache/openclaw/hubspot-token.json`
- Lazy config validation (only checked when a command runs)

## Dependencies

- `commander` — CLI framework
- `dotenv` — environment variable loading
- Node.js built-in `fetch` (requires Node >= 18)

## Author

Abdelkrim BOUJRAF — [ALT-F1 SRL](https://www.alt-f1.be), Brussels 🇧🇪 🇲🇦
X: [@altf1be](https://x.com/altf1be)
