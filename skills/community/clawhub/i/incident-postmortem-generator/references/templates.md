# Postmortem Templates & Guidelines

## Incident JSON Schema

Use `--from incident.json` to load a complete incident definition:

```json
{
  "title": "Database connection pool exhaustion",
  "severity": "P1",
  "date": "2026-03-28",
  "duration": "45 minutes",
  "status": "Resolved",
  "author": "oncall-team",
  "summary": "Primary database became unresponsive due to connection pool exhaustion caused by a leaked connection in the new payment service.",
  "impact": "All API requests returned 503 for 45 minutes. ~12,000 users affected. Estimated revenue impact: $8,500.",
  "root_cause": "The payment service v2.3.1 deployed at 14:20 introduced a code path that opened database connections without closing them on error. Under load, this exhausted the 100-connection pool within 15 minutes.",
  "detection": "PagerDuty alert fired at 14:35 when API error rate exceeded 50% threshold. Time to detect: 15 minutes.",
  "resolution": "1. Rolled back payment service to v2.3.0 at 14:50\n2. Manually cleared stale connections\n3. Database recovered at 15:05",
  "timeline": [
    {"time": "2026-03-28T14:20:00", "event": "Payment service v2.3.1 deployed", "type": "action"},
    {"time": "2026-03-28T14:35:00", "event": "API error rate alert fired", "type": "detection"},
    {"time": "2026-03-28T14:38:00", "event": "Oncall engineer acknowledged", "type": "action"},
    {"time": "2026-03-28T14:42:00", "event": "Identified connection pool exhaustion", "type": "action"},
    {"time": "2026-03-28T14:50:00", "event": "Rolled back to v2.3.0", "type": "action"},
    {"time": "2026-03-28T15:05:00", "event": "All services recovered", "type": "resolution"}
  ],
  "lessons_learned": [
    "Connection pool monitoring was not alerting on utilization, only on total failures",
    "Rollback process took 12 minutes — should be automated",
    "The leak was caught in code review but not flagged as blocking"
  ],
  "action_items": [
    {"action": "Add connection pool utilization alerts at 80% threshold", "owner": "Platform", "priority": "P1", "due": "2026-04-05", "status": "Open"},
    {"action": "Implement automated rollback on error rate spike", "owner": "SRE", "priority": "P1", "due": "2026-04-15", "status": "Open"},
    {"action": "Add integration test for connection cleanup on error paths", "owner": "Payments", "priority": "P2", "due": "2026-04-10", "status": "Open"}
  ]
}
```

## Timeline Event Types

| Type | Meaning | Example |
|------|---------|---------|
| `action` | Something someone did | "Deployed v2.3.1", "Restarted service" |
| `detection` | Issue was noticed | "Alert fired", "Customer reported" |
| `escalation` | Escalated to another team | "Paged database oncall" |
| `communication` | Status update sent | "Posted to #incidents", "Updated status page" |
| `resolution` | Issue resolved | "Service recovered", "Fix deployed" |

## Blame-Free Language Guide

### Principles

1. **Describe system conditions, not human failings** — "The monitoring gap allowed..." not "The engineer failed to..."
2. **Use passive voice for errors** — "The config was deployed without validation" not "They deployed without validating"
3. **Focus on process gaps** — "The review process did not catch..." not "The reviewer missed..."
4. **Assume competence** — People made the best decisions with the information available at the time

### Replacements

| Blameful | Blame-free |
|----------|-----------|
| "Engineer X caused the outage" | "The deployment triggered a failure in..." |
| "Human error" | "A process gap allowed..." |
| "Should have known" | "The system did not surface..." |
| "Failed to check" | "The check was not part of the process" |
| "Careless mistake" | "The existing safeguards did not prevent..." |
| "Forgot to" | "The runbook did not include..." |

### Use `--check-blame` to scan existing documents:

```bash
python3 scripts/generate_postmortem.py --check-blame existing-postmortem.md
```
