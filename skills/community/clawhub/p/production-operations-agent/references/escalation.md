# Escalation & Incident Communications Reference

Load this when the investigation is complete and the agent needs to help with severity assessment, stakeholder comms, or post-incident documentation.

## Severity Framework

| Severity | Criteria | Response Time |
|----------|----------|--------------|
| SEV1 | Complete outage, all users affected, revenue impact | Immediate, war room now |
| SEV2 | Major feature down, >20% users affected, workaround exists | 15 min response |
| SEV3 | Degraded performance, <20% users, workaround exists | 1 hour response |
| SEV4 | Minor issue, cosmetic, no user impact | Next business day |

## Initial Incident Notification Template

```
🔴 [SEV{N}] {Service} Incident — {Short description}

Status: Investigating
Started: {time}
Impact: {who/what is affected}
On-call: {name}
Bridge: {link}

We are investigating and will update in 15 minutes.
```

## Status Update Template (every 15-30 min during SEV1/2)

```
🟡 [UPDATE] {Service} Incident — {time}

Status: {Investigating | Identified | Mitigating | Monitoring}
Finding: {one sentence on what we know}
Action: {what we are doing right now}
ETA: {best estimate or "unknown"}

Next update in {15|30} minutes.
```

## Resolution Template

```
✅ [RESOLVED] {Service} Incident — {time}

Duration: {start} → {end} ({total time})
Impact: {description of user impact}
Root Cause: {one paragraph}
Fix: {what was done to resolve}
Follow-up: Post-incident review scheduled for {date}
```

## Blameless Post-Incident Template

```markdown
# Post-Incident Review — {Service} — {Date}

## Summary
{2-3 sentence plain language summary}

## Timeline
| Time | Event |
|------|-------|
| {HH:MM} | {what happened} |

## Root Cause
{Detailed explanation — focus on system/process failure, not individual blame}

## Contributing Factors
- {factor 1}
- {factor 2}

## What Went Well
- {thing 1}

## What Went Poorly
- {thing 1}

## Action Items
| Action | Owner | Due |
|--------|-------|-----|
| {item} | {name} | {date} |
```
