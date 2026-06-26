---
name: neckr0ik-newsletter-manager
version: 1.0.0
description: Manage newsletters with AI-generated content. Create, schedule, and send newsletters automatically. Supports multiple platforms (Substack, Beehiiv, ConvertKit). Use when you need to run a newsletter business or automate newsletter creation.
---

# Newsletter Manager

AI-powered newsletter creation and management.

## Quick Start

```bash
# Create a new newsletter draft
neckr0ik-newsletter-manager create --topic "AI agents" --style professional

# Schedule for specific time
neckr0ik-newsletter-manager schedule --id draft-123 --time "2026-03-07 09:00"

# Send to all subscribers
neckr0ik-newsletter-manager send --id draft-123
```

## What This Does

- **Generates content** — AI-written articles, summaries, curated links
- **Manages subscribers** — Import, segment, track engagement
- **Schedules delivery** — Optimal send times, timezone handling
- **Tracks analytics** — Open rates, click rates, unsubscribes
- **Multi-platform** — Substack, Beehiiv, ConvertKit, Mailchimp

## Income Potential

- Run 2-3 newsletters for clients: $300-1500/month each
- Build newsletter automation for businesses: $500-2000 setup
- Sell newsletter templates on ClawHub: $20-50 per template

## Commands

### create

Create a new newsletter draft.

```bash
neckr0ik-newsletter-manager create [options]

Options:
  --topic <topic>        Main topic or theme
  --style <style>        Writing style (professional, casual, technical)
  --length <words>       Target length (default: 500)
  --curate               Include curated links from web search
  --template <name>       Use saved template
```

### schedule

Schedule newsletter for delivery.

```bash
neckr0ik-newsletter-manager schedule --id <draft-id> --time <datetime>

Options:
  --timezone <tz>        Recipient timezone (default: sender's)
  --optimal              Auto-calculate optimal send time
```

### send

Send newsletter immediately.

```bash
neckr0ik-newsletter-manager send --id <draft-id> [options]

Options:
  --test <email>         Send test to specific email
  --segment <name>        Send to specific subscriber segment
  --platform <name>       Platform to send via (substack, beehiiv, convertkit)
```

### subscribers

Manage subscriber list.

```bash
neckr0ik-newsletter-manager subscribers <action> [options]

Actions:
  import <file>          Import subscribers from CSV
  export                 Export subscribers to CSV
  segment <name>         Create subscriber segment
  stats                  Show subscriber statistics
```

### analytics

View newsletter performance.

```bash
neckr0ik-newsletter-manager analytics [options]

Options:
  --period <days>        Time period (default: 30)
  --newsletter <id>       Specific newsletter ID
  --export <format>       Export format (csv, json)
```

## Platform Setup

### Substack

```bash
neckr0ik-newsletter-manager config set substack.publication <name>
```

### Beehiiv

```bash
neckr0ik-newsletter-manager config set beehiiv.api_key <key>
```

### ConvertKit

```bash
neckr0ik-newsletter-manager config set convertkit.api_key <key>
neckr0ik-newsletter-manager config set convertkit.api_secret <secret>
```

## Templates

Create reusable newsletter templates:

```
templates/
├── weekly-roundup.md      # Weekly curated links
├── product-update.md       # Product announcements
├── tutorial.md             # How-to guides
└── industry-news.md        # News analysis
```

### Weekly Roundup Template

```markdown
# [Topic] Weekly: [Date]

## Top Stories

1. [AI-generated summary of top news]
2. [AI-generated summary of top news]
3. [AI-generated summary of top news]

## Deep Dive

[AI-generated analysis of key topic]

## Quick Links

- [Link 1 with AI summary]
- [Link 2 with AI summary]
- [Link 3 with AI summary]

## Upcoming

[AI-generated upcoming events in the space]

---

*This newsletter was created with AI assistance.*
```

## Automation Examples

### Daily News Digest

```python
from newsletter import NewsletterManager

manager = NewsletterManager()

# Generate daily digest
digest = manager.create(
    topic="AI and Technology",
    style="professional",
    length=300,
    curate=True  # Auto-find relevant news
)

# Schedule for 9 AM
manager.schedule(digest.id, time="09:00", optimal=True)
```

### Client Newsletter Service

```python
# Manage multiple client newsletters
clients = [
    {"name": "Tech Startup", "topic": "SaaS growth"},
    {"name": "Marketing Agency", "topic": "Digital marketing"},
    {"name": "E-commerce", "topic": "DTC trends"},
]

for client in clients:
    newsletter = manager.create(
        topic=client["topic"],
        template="weekly-roundup"
    )
    manager.schedule(newsletter.id, optimal=True)
```

## Best Practices

1. **Consistency** — Send at the same time each week
2. **Value** — Lead with actionable insights
3. **Length** — 300-800 words optimal for engagement
4. **Personalization** — Use subscriber names when possible
5. **Analytics** — Track opens, clicks, unsubscribes to improve

## See Also

- `references/templates/` — Newsletter templates
- `references/platforms.md` — Platform-specific guides
- `scripts/newsletter.py` — Main implementation