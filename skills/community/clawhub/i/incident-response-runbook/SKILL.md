# Incident Response Runbook

Generate, maintain, and execute incident response runbooks for production systems. Use when setting up incident workflows, responding to outages, or documenting post-incident learnings.

## Usage

### Generate Runbook
```
Create an incident response runbook for [service/system]. 
Infrastructure: [cloud provider, key services].
Common failure modes: [list known issues].
```

### During Incident
```
Incident: [description]. Severity: [1-4]. 
Current symptoms: [what's happening].
Help me triage and respond.
```

### Post-Incident
```
Generate a post-incident review for: [incident summary].
Timeline: [key events with timestamps].
Resolution: [what fixed it].
```

## Runbook Structure

Generated runbooks follow this template:

```markdown
# [Service] Incident Response Runbook

## Quick Reference
- **On-call:** [rotation link]
- **Dashboards:** [monitoring links]
- **Escalation:** [contact chain]

## Severity Levels
- **SEV1**: Complete outage, revenue impact → respond in 5 min
- **SEV2**: Degraded service, user-facing → respond in 15 min
- **SEV3**: Internal impact, no users affected → respond in 1 hour
- **SEV4**: Cosmetic or minor, no urgency → next business day

## Triage Steps
1. Confirm the issue (check dashboards, reproduce)
2. Assess blast radius (which users/services affected)
3. Assign severity level
4. Start incident channel/thread
5. Communicate to stakeholders

## Failure Modes

### [Failure Mode 1: e.g., Database Connection Pool Exhaustion]
**Symptoms:** [what you'll see]
**Diagnosis:** [commands to run, logs to check]
**Mitigation:** [immediate steps to restore service]
**Root Fix:** [permanent solution]

### [Failure Mode 2: e.g., Memory Leak in Worker Process]
...

## Rollback Procedures
[Service-specific rollback steps]

## Communication Templates
[Internal + external status page templates]

## Post-Incident Review Template
[Blameless review structure]
```

## Scripts

### `scripts/generate_runbook.py`

Generate a runbook skeleton from service metadata:

```bash
python3 scripts/generate_runbook.py --service api-gateway \
  --provider aws --region us-east-1 \
  --monitors datadog,pagerduty \
  --output runbook-api-gateway.md
```

## AI Enhancement

When used as an agent skill, the incident responder:
- Guides triage in real-time with diagnostic commands specific to the stack
- Correlates symptoms with known failure modes from the runbook
- Drafts status page updates and internal communications
- Generates post-incident reviews with timeline, root cause analysis, and action items
- Learns from past incidents to improve future runbooks
