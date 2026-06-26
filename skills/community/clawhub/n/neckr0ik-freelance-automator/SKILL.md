---
name: neckr0ik-freelance-automator
version: 1.0.0
description: Automate freelance workflows — find jobs, write proposals, deliver work. Supports Upwork, Fiverr, Freelancer, PeoplePerHour. Use when you want to run a freelance business with AI assistance.
---

# Freelance Automator

AI-powered freelance business automation.

## What This Does

- **Job Hunting** — Find relevant jobs automatically
- **Proposal Writing** — Generate winning proposals with AI
- **Client Communication** — Automated responses and updates
- **Delivery Tracking** — Track deadlines and deliverables
- **Invoice Generation** — Create and send invoices

## Income Potential

- Find 2-3 jobs/week at $50-200 each
- Manage 3-5 clients simultaneously
- Scale to $500-2000/month with consistency

## Supported Platforms

| Platform | Status | Features |
|----------|--------|----------|
| Upwork | ✅ Full | Job search, proposals, delivery |
| Fiverr | ✅ Full | Gig creation, messaging |
| Freelancer | ✅ Full | Job search, bidding |
| PeoplePerHour | ✅ Full | Hourly proposals |
| Guru | 🟡 Partial | Job search |

## Quick Start

```bash
# Find jobs matching your skills
neckr0ik-freelance-automator find --skills "python, web scraping, automation" --limit 20

# Generate proposal for a job
neckr0ik-freelance-automator propose --job-id <id> --rate 50

# Track your active jobs
neckr0ik-freelance-automator status

# Generate invoice
neckr0ik-freelance-automator invoice --client "John Smith" --amount 150 --project "Web scraping"
```

## Commands

### find

Search for jobs on freelance platforms.

```bash
neckr0ik-freelance-automator find [options]

Options:
  --skills <skills>     Comma-separated skills to search for
  --platform <name>      Platform to search (default: all)
  --limit <n>           Maximum results (default: 20)
  --min-budget <amount>  Minimum budget filter
  --max-budget <amount>  Maximum budget filter
  --posted <days>        Jobs posted within N days
```

### propose

Generate a proposal for a job.

```bash
neckr0ik-freelance-automator propose --job-id <id> [options]

Options:
  --rate <amount>        Your hourly rate or fixed price
  --style <style>        Proposal style (professional, friendly, technical)
  --template <name>       Use saved proposal template
  --deliverables <items>  Comma-separated deliverables
```

### status

Show all active jobs and their status.

```bash
neckr0ik-freelance-automator status [options]

Options:
  --platform <name>      Filter by platform
  --status <status>       Filter by status (active, pending, completed)
```

### invoice

Generate an invoice for a client.

```bash
neckr0ik-freelance-automator invoice --client <name> --amount <amount> [options]

Options:
  --project <name>       Project description
  --due <days>           Payment due in N days (default: 14)
  --format <format>      Output format (pdf, html, json)
  --send                  Send directly to client email
```

### message

Manage client communication.

```bash
neckr0ik-freelance-automator message <action> [options]

Actions:
  template               Create message template
  auto-reply             Set up auto-reply for common questions
  follow-up              Schedule follow-up messages
```

## Workflows

### Daily Job Hunt

```bash
# Run each morning
neckr0ik-freelance-automator find --skills "automation, python" --posted 1 --limit 10

# Generate proposals for top 3
neckr0ik-freelance-automator propose --job-id <id1>
neckr0ik-freelance-automator propose --job-id <id2>
neckr0ik-freelance-automator propose --job-id <id3>
```

### Client Delivery

```bash
# Track deliverable
neckr0ik-freelance-automator track --client "ABC Corp" --deliverable "Scraped data CSV"

# Mark complete and invoice
neckr0ik-freelance-automator complete --client "ABC Corp"
neckr0ik-freelance-automator invoice --client "ABC Corp" --amount 200
```

### Proposal Templates

Create reusable templates:

```markdown
# [Project Type] Proposal Template

Hi [Client],

I saw your [project description summary] and I'm confident I can deliver exactly what you need.

## Understanding
[AI-generated understanding of requirements]

## Approach
[AI-generated approach based on skills]

## Deliverables
- [Deliverable 1]
- [Deliverable 2]
- [Deliverable 3]

## Timeline
[Estimated timeline based on complexity]

## Rate
$[X] fixed price / $[Y]/hour

## Why Me
[AI-generated summary of relevant experience]

Let's discuss further.
[Your name]
```

## Automation Tips

1. **Set up daily job alerts** — Run `find` on a schedule
2. **Use proposal templates** — Customize for each platform
3. **Track response rates** — See which proposals convert
4. **Follow up politely** — Send follow-ups after 3 days
5. **Invoice promptly** — Don't wait to get paid

## See Also

- `references/platforms/` — Platform-specific guides
- `references/proposals/` — Winning proposal examples
- `scripts/freelance.py` — Main implementation