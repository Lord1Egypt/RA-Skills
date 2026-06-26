---
name: neckr0ik-automation-templates
version: 1.0.0
description: Ready-to-use automation templates for n8n, Make.com, and Zapier. Pre-built workflows for common use cases. Copy, customize, deploy. Use when you need quick automation setups.
---

# Automation Templates

Ready-to-use workflows for n8n, Make.com, and Zapier.

## What This Provides

- **50+ pre-built templates** — Copy and customize
- **Multi-platform** — n8n, Make.com, Zapier compatible
- **Common use cases** — Email, CRM, data sync, notifications
- **Production-ready** — Tested and documented

## Quick Start

```bash
# List all templates
neckr0ik-automation-templates list

# Get a specific template
neckr0ik-automation-templates get --name email-drip-campaign --platform n8n

# Search templates
neckr0ik-automation-templates search --keyword email --platform make

# Generate from template
neckr0ik-automation-templates generate --template lead-capture --output ./workflow.json
```

## Template Categories

### Email & Marketing

| Template | Platform | Description |
|----------|----------|-------------|
| email-drip-campaign | All | Multi-email sequence with delays |
| newsletter-signup | All | Add to list + welcome email |
| lead-capture | All | Form → CRM → Email sequence |
| social-scheduler | All | Schedule posts across platforms |
| abandoned-cart | All | E-commerce cart recovery |

### CRM & Sales

| Template | Platform | Description |
|----------|----------|-------------|
| crm-sync | All | Sync contacts across CRMs |
| lead-scoring | All | Score leads based on activity |
| deal-pipeline | All | Move deals through stages |
| follow-up-sequence | All | Automated follow-ups |
| meeting-scheduler | All | Book meetings + confirmations |

### Data & Sync

| Template | Platform | Description |
|----------|----------|-------------|
| sheets-to-database | All | Google Sheets → Airtable/Notion |
| webhook-to-slack | All | Webhook notifications to Slack |
| file-backup | All | Auto-backup files to cloud |
| data-pipeline | All | Extract → Transform → Load |
| api-sync | All | Sync data between APIs |

### Notifications & Alerts

| Template | Platform | Description |
|----------|----------|-------------|
| error-alert | All | Error notifications to Slack/Email |
| daily-report | All | Scheduled summary reports |
| keyword-monitor | All | Monitor mentions/keywords |
| price-change-alert | All | Track price changes |
| uptime-monitor | All | Website uptime monitoring |

### E-commerce

| Template | Platform | Description |
|----------|----------|-------------|
| order-confirmation | All | Order → Email → CRM |
| inventory-sync | All | Sync inventory across channels |
| payment-receipt | All | Payment → Receipt → CRM |
| customer-onboarding | All | Welcome sequence for new customers |
| review-request | All | Request reviews post-purchase |

## Template Format

Each template includes:

```json
{
  "name": "template-name",
  "platform": "n8n|make|zapier",
  "category": "email|crm|data|notification|ecommerce",
  "description": "What this template does",
  "trigger": { ... },
  "nodes": [ ... ],
  "connections": { ... },
  "settings": { ... },
  "variables": {
    "API_KEY": "Your API key",
    "WEBHOOK_URL": "Your webhook URL"
  },
  "docs": "Setup instructions"
}
```

## Commands

### list

List available templates.

```bash
neckr0ik-automation-templates list [options]

Options:
  --category <name>    Filter by category
  --platform <name>    Filter by platform
```

### get

Get a specific template.

```bash
neckr0ik-automation-templates get --name <template> --platform <platform>

Options:
  --output <file>      Save to file
  --format <format>    Output format (json, yaml)
```

### search

Search templates by keyword.

```bash
neckr0ik-automation-templates search --keyword <term> [options]

Options:
  --platform <name>    Filter by platform
  --category <name>    Filter by category
```

### generate

Generate workflow from template.

```bash
neckr0ik-automation-templates generate --template <name> [options]

Options:
  --platform <name>    Target platform
  --output <dir>       Output directory
  --customize          Interactive customization
```

## Use Cases

### 1. Quick Email Drip Campaign

```bash
# Get template
neckr0ik-automation-templates get --name email-drip-campaign --platform n8n

# Import to n8n
# Copy workflow.json content
# Paste into n8n workflow editor
# Configure your email provider
# Activate
```

### 2. Lead Capture System

```bash
# Get template
neckr0ik-automation-templates get --name lead-capture --platform make

# Configure
# Set form webhook URL
# Add your CRM credentials
# Customize email templates
# Activate
```

### 3. Daily Report

```bash
# Get template
neckr0ik-automation-templates get --name daily-report --platform zapier

# Configure
# Set data sources
# Set report destination
# Set schedule
# Activate
```

## Customization

Each template has variables you need to set:

```json
{
  "variables": {
    "EMAIL_FROM": "noreply@yourcompany.com",
    "EMAIL_TO": "team@yourcompany.com",
    "SLACK_WEBHOOK": "https://hooks.slack.com/...",
    "AIRTABLE_API_KEY": "key...",
    "MAKE_WEBHOOK": "https://hook.make.com/..."
  }
}
```

## Contribution

To add a new template:

1. Create `templates/your-template.json`
2. Include all required fields
3. Test on target platform
4. Submit PR

## See Also

- `templates/` — Template files
- `scripts/generator.py` — Template generator
- `references/platforms.md` — Platform-specific notes