---
name: incident-triage
description: >
  Structured incident triage for alerts from any monitoring source. Five-step framework:
  classify severity, scope blast radius, correlate with recent changes, investigate by
  alert type, and act (summarize, create ticket, escalate). Parses alerts from PagerDuty,
  Datadog, CloudWatch, Sentry, uptime monitors, GitHub Actions, AWS SNS/EventBridge,
  and custom webhooks. Customizable escalation policy and runbook. Uses `gh` CLI for
  deploy correlation. Use when: an alert fires, something is down, error rates spike,
  a deployment fails, investigating an incident, triaging a monitoring alert, responding
  to a page, or an exception tracker reports a new or regressed error.
---

# Incident Triage

Structured incident triage for alerts from any monitoring source. Five steps, consistent every time.

Pass in the raw alert message, a link to the alert, or a description of what's happening.

## Triage Process

When an alert appears:

1. **Classify** — what type and severity?
2. **Scope** — blast radius: who's affected, which environment, since when?
3. **Correlate** — what changed recently? Check deploys, merges, config changes
4. **Investigate** — guided checks based on alert type
5. **Act** — summarize, create ticket, escalate or close

Read [references/triage-framework.md](references/triage-framework.md) for the full framework with checklists and bash snippets for each step.

## Alert Parsing

Before starting the triage framework, identify the alert source and extract key fields.

Read [references/alert-patterns.md](references/alert-patterns.md) for patterns covering PagerDuty, Datadog, CloudWatch, Sentry, uptime monitors, GitHub Actions, AWS SNS/EventBridge, and custom webhooks.

## Escalation

When to page, when to watch, when to close. Severity-based response times and communication templates.

Read [references/escalation-guide.md](references/escalation-guide.md) for defaults — customize for your team's on-call structure.

## Runbook

During Step 4 (Investigate), load [references/runbook-template.md](references/runbook-template.md) to find service health endpoints, dashboards, log locations, and common fixes.

> ⚠️ **This file is a template — it must be filled in before use.** If it still contains `<!--` placeholder comments, tell the user to populate it with their actual infrastructure before relying on it during an incident.

## Scripts

The `scripts/` directory contains helper scripts for the correlation and action steps:

- `scripts/correlate-recent-deploys.sh` — list recent CI/CD runs for a repo (Step 3)
- `scripts/correlate-recent-merges.sh` — list recently merged PRs for a repo (Step 3)
- `scripts/create-incident-issue.sh` — create a GitHub incident issue (Step 5)

## Works Well With

- **github** (Step 3 — Correlate): check recent deploys, merged PRs, and CI run history for affected repos
- **aws-ecs-monitor** (Step 4 — Investigate): ECS service health, ALB targets, and CloudWatch logs for downtime and resource alerts
- **gh-issues** (Step 5 — Act): create incident tickets automatically

## References

- [references/triage-framework.md](references/triage-framework.md) — full 5-step triage process with checklists
- [references/alert-patterns.md](references/alert-patterns.md) — parsing alerts from common sources
- [references/escalation-guide.md](references/escalation-guide.md) — severity levels, response times, escalation policy
- [references/runbook-template.md](references/runbook-template.md) — your infrastructure map (⚠️ fill in before use)
