---
name: incident-communication
description: Write professional incident updates, blameless postmortems, maintenance announcements, and status reports for your status page. Includes real-world examples from Vercel, Stripe, GitHub, and Cloudflare. Start with status-page-context to configure your tone, components, and SLAs — all other skills reference it automatically.
version: 1.0.0
homepage: https://openstatus.dev
skills:
  - skills/status-page-context
  - skills/incident-communication
  - skills/postmortem
  - skills/maintenance
  - skills/status-report
---

# OpenStatus Skills

Status page & incident communication skills for AI agents — by [OpenStatus](https://openstatus.dev).

## Skills

| Skill | What it does |
|-------|-------------|
| [`status-page-context`](skills/status-page-context/) | Configure your product, components, SLAs, severity levels, and communication tone. All other skills read this automatically. |
| [`incident-communication`](skills/incident-communication/) | Write status page updates for any incident phase: investigating, identified, monitoring, resolved. |
| [`postmortem`](skills/postmortem/) | Write blameless postmortems with timeline, root cause analysis (5 Whys), and prioritized action items. |
| [`maintenance`](skills/maintenance/) | Write maintenance announcements: scheduled, in-progress, completed, extended, or cancelled. |
| [`status-report`](skills/status-report/) | Write periodic health reports (weekly, monthly, quarterly) with uptime metrics, SLA tracking, and trends. |

## How They Work Together

```
status-page-context     ← run this first (defines tone, components, SLAs)
  │
  ├── incident-communication   ← during an outage
  │     investigating → identified → monitoring → resolved
  │                                                  │
  │                                                  └── postmortem   ← after resolution
  │
  ├── maintenance              ← for planned work
  │     scheduled → in-progress → completed
  │
  └── status-report            ← periodic health updates
        weekly / monthly / quarterly
```

Each skill checks for `.agents/status-page-context.md` and uses your defined tone, component names, and severity levels. Without it, skills still work — they'll just prompt you for the details.

## What's Inside Each Skill

Every skill includes:

- **SKILL.md** — full instructions, principles, templates, and anti-patterns
- **references/examples.md** — real-world good and bad examples from Vercel, Stripe, GitHub, and Cloudflare
- **references/framework.md** — checklists and quality tests to verify output
- **evals/evals.json** — evaluation scenarios for testing skill behavior

## Who This Is For

- **On-call engineers** — write clear incident updates under pressure without starting from a blank page
- **SREs / DevOps** — produce consistent postmortems and reliability reports
- **Engineering managers** — publish regular status reports to stakeholders
- **Anyone with a status page** — communicate maintenance, outages, and health to users
