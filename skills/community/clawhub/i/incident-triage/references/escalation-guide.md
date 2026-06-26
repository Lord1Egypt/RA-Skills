# Escalation Guide

Severity-based response policy. Customize for your team's on-call structure.

## Response Matrix

| Severity | Response Time | Who Responds | Communication |
|----------|--------------|-------------|---------------|
| **SEV-1** | Immediate (< 5 min) | On-call + team lead + stakeholders | Dedicated incident channel, continuous updates |
| **SEV-2** | 15 minutes | On-call engineer | Alert thread, updates every 15 min |
| **SEV-3** | Next business day | Team (async) | Ticket created, triaged in standup |
| **SEV-4** | Async | Anyone | Logged, reviewed periodically |

## Escalation Triggers

Escalate to the next level when:

- **SEV-2 → SEV-1:** Customer reports increase, duration exceeds 30 min, blast radius grows
- **SEV-3 → SEV-2:** Staging issue is blocking production deploy, internal SLA breach
- **Any → SEV-1:** Data loss confirmed or suspected, security breach, compliance impact

## Communication Templates

### SEV-1 — Opening message
```
🔴 [SEV-1] <service> — <short description>
Status: Active
Started: <time>
Impact: <who's affected>
Investigating: <who's looking>
Next update: <time>
```

### Status update (every 15 min for SEV-1/2)
```
🔴 [SEV-1] Update — <time>
Status: Investigating / Mitigating / Monitoring
Findings: <what we know now>
Actions: <what we're doing>
Next update: <time>
```

### Resolution
```
🟢 [SEV-1] Resolved — <time>
Duration: <start to resolution>
Root cause: <brief>
Fix: <what we did>
Follow-up: <ticket link for post-mortem>
```

## When NOT to Escalate

- Alert that auto-resolves within the monitoring tool's threshold (transient blip)
- Known maintenance window
- Alert on a non-production environment with no deployment blocked
- Duplicate of an already-tracked incident

## Customize

Replace the response matrix with your team's actual contacts and channels:

```
SEV-1: Page @oncall-primary + @oncall-secondary, notify #incidents
SEV-2: Notify @oncall-primary in #alerts
SEV-3: Create ticket, assign to team
SEV-4: Log in #alerts-low-priority
```