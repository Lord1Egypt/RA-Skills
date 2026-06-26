# Infrastructure & Uptime Monitoring Skill

Monitor server health, uptime, and resource utilization with plain-language status reports. Built for small teams, solo operators, and self-hosters who need monitoring without enterprise tooling overhead.

## Status: v0.1.0 — Ready for Publish

## Files

| File | Purpose |
|---|---|
| `SKILL.md` | Skill definition: triggers, workflow, output structure, boundaries |
| `infra-monitoring-spec.md` | Product spec: purpose, users, capabilities, differentiation, success metrics |
| `references/metrics-thresholds.md` | Healthy/warning/critical thresholds for CPU, memory, disk, network, uptime |
| `references/monitoring-checklists.md` | Daily, weekly, incident response, and new server setup checklists |
| `references/alert-severity.md` | Severity classification system with escalation and de-escalation rules |
| `references/test-prompts.md` | 12 test cases: 4 happy path, 4 normal path, 4 edge cases |

## Usage

Install from ClawHub:

```
clawhub install infra-monitoring
```

Then ask your AI assistant to:

- "Check the health of my server" (paste output from `top`, `df -h`, `free -m`)
- "Monitor uptime for https://api.example.com"
- "When does my SSL cert expire?"
- "Give me a status report on my infrastructure"

The skill parses system metrics, classifies health as healthy/warning/critical, and returns a plain-language report with concrete next steps.

## Key Differentiator

This skill feels like a sharp ops engineer giving you a status report, not a dashboard dumping metrics. It leads with "here's what needs your attention" not "here are 47 numbers."

## Publisher

NorthlineAILabs
