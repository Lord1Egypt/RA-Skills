---
name: incident-response-plan
description: >
  Generate a tailored incident response plan for AI agent deployments and SaaS operations.
  Covers detection, triage, containment, recovery, and post-mortem. Use when deploying
  agents to production, preparing for SOC2 audits, or building operational resilience.
  Built by AfrexAI.
metadata:
  version: 1.0.0
  author: AfrexAI
  tags: [incident-response, security, operations, devops, enterprise]
---

# Incident Response Plan Generator

Generate a production-ready incident response plan tailored to your AI agent deployment.

## When to Use
- Deploying AI agents to production for the first time
- Preparing for SOC2 or ISO 27001 audits
- Client asks "what happens when something breaks?"
- Building operational runbooks for managed AI services
- After an incident — to prevent recurrence

## Input
```
Service: [Name of AI agent/service]
Environment: [cloud provider, region, architecture]
Data Sensitivity: [low/medium/high/critical]
Team Size: [number of responders]
SLA: [uptime target, e.g., 99.9%]
Integrations: [list of connected systems]
```

## Plan Structure

### 1. Severity Classification
| Level | Description | Response Time | Examples |
|-------|------------|---------------|----------|
| SEV1 — Critical | Service down, data breach, financial impact | 15 min | Agent sending wrong data to clients, API keys exposed |
| SEV2 — High | Degraded service, partial outage | 1 hour | Agent responses slow, one integration failing |
| SEV3 — Medium | Non-critical issue, workaround exists | 4 hours | Minor accuracy drop, cosmetic errors |
| SEV4 — Low | Enhancement, no immediate impact | Next business day | Feature request, optimization |

### 2. Detection & Alerting
- Health check endpoints (every 60s)
- Error rate thresholds (>1% = SEV3, >5% = SEV2, >25% = SEV1)
- Response time monitoring (p99 > 2x baseline = alert)
- Cost anomaly detection (>150% daily average)
- Output quality sampling (random audit of agent responses)
- Uptime monitoring (UptimeRobot, Pingdom, or custom)

### 3. Triage Checklist
```markdown
□ Confirm the alert is real (not false positive)
□ Classify severity (SEV1-4)
□ Identify affected scope (which agents, which clients)
□ Check recent changes (deploys, config changes, upstream)
□ Assign incident commander
□ Open incident channel/thread
□ Notify affected stakeholders per SLA
```

### 4. Containment Actions by Type

**Agent Misbehavior:**
- Pause agent processing (kill switch)
- Revert to last known good config
- Enable human-in-the-loop mode
- Queue messages for manual review

**Infrastructure Failure:**
- Failover to backup region/instance
- Scale horizontally if capacity issue
- Check upstream dependencies (API providers, databases)
- Enable circuit breakers

**Security Incident:**
- Rotate all credentials immediately
- Isolate affected systems
- Preserve logs and evidence
- Engage security team / legal if data breach

**Data Quality Issue:**
- Halt automated outputs
- Identify contamination window
- Notify affected clients with timeline
- Prepare correction batch

### 5. Communication Templates

**Client notification (SEV1/2):**
```
Subject: [Service Name] — Incident Update

We've identified an issue affecting [description].
- Impact: [what's affected]
- Status: [investigating/identified/monitoring/resolved]
- ETA: [estimated resolution time]
- Workaround: [if available]

We'll provide updates every [30 min / 1 hour].
```

**Internal escalation:**
```
🚨 SEV[X] — [Service]: [Brief description]
Impact: [scope]
Started: [time]
Commander: [name]
Channel: [link]
Action needed: [specific ask]
```

### 6. Recovery & Validation
```markdown
□ Root cause identified and documented
□ Fix deployed and verified
□ All affected data corrected/reconciled
□ Client communication sent (resolution)
□ Monitoring confirms stable for 30+ min
□ Incident timeline documented
```

### 7. Post-Mortem Template
```markdown
# Incident Post-Mortem: [Title]
**Date:** YYYY-MM-DD
**Severity:** SEV[X]
**Duration:** [start] — [end] ([total time])
**Commander:** [name]

## Summary
[2-3 sentence description]

## Timeline
- HH:MM — [event]
- HH:MM — [event]

## Root Cause
[Technical root cause]

## Impact
- Users affected: [number]
- Duration: [time]
- Data impact: [description]
- Financial impact: [if applicable]

## What Went Well
- [item]

## What Went Wrong
- [item]

## Action Items
| Action | Owner | Due Date | Status |
|--------|-------|----------|--------|
| [item] | [name] | [date] | Open |

## Lessons Learned
- [lesson]
```

## Best Practices
- Test your incident response plan quarterly (tabletop exercises)
- Keep runbooks next to the code they support
- Automate detection — humans are slow at noticing things
- Over-communicate during incidents — silence breeds anxiety
- Blameless post-mortems — focus on systems, not people
- Track MTTR (mean time to recover) as your north star metric

---

*Need incident response built into your AI operations from day one? AfrexAI deploys production-grade AI agents with monitoring, alerting, and response plans included. Book a call: [calendly.com/cbeckford-afrexai/30min](https://calendly.com/cbeckford-afrexai/30min)*
