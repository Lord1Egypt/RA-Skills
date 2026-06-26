# OpenStatus Skills for Agents

Status page & incident communication skills for AI agents — by [OpenStatus](https://openstatus.dev).

Write better incident updates, postmortems, maintenance announcements, and status reports.

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

## Getting Started

1. Install the skills using one of the methods above
2. Run the `status-page-context` skill first to set up your product context
3. Use any other skill — they'll automatically read your context for consistent tone and component names

### Example: Write an incident update

```
> Our API is returning 500 errors, started about 10 minutes ago

The skill will:
1. Check for your status-page-context
2. Ask which phase you're in (or detect it from your message)
3. Write a scoped update with timestamps, user impact, and next-update commitment
4. Suggest the next phase when you're ready
```

---

Built by [OpenStatus](https://openstatus.dev). Need help? Join our [Discord](https://openstatus.dev/discord) or message us at [ping@openstatus.dev](mailto:ping@openstatus.dev).
