# Log-only workflow

Use this pattern when no issue tracker is available or when a lightweight local workflow is preferred.

## Storage options
- `cases.jsonl` with one case event per line
- `cases/YYYY-MM-DD.md` daily markdown logs
- both, if you want machine-readable state plus human-readable summaries

## Recommended JSONL event shape
```json
{
  "case_id": "mc-2026-04-15-001",
  "created_at": "2026-04-15T00:20:00+09:00",
  "updated_at": "2026-04-15T00:20:00+09:00",
  "source": "cs",
  "category": "incident",
  "severity": "high",
  "state": "TRIAGED",
  "title": "Payment confirmation delayed",
  "skeleton": {
    "customer_issue": "payment confirmation delayed",
    "reported_symptom": "webhook processing seems broken",
    "product_plan": "unknown"
  },
  "likely_module": "billing-webhook",
  "primary_owner": "Billing Engineering",
  "backup_owner": "Platform Backend Team",
  "next_actions": [
    "check webhook logs",
    "confirm impact scope",
    "prepare manual workaround"
  ],
  "notes": "initial triage"
}
```

## Recording pattern
1. Create a case record when the issue reaches TRIAGED.
2. Append new events for ASSIGNED, no-response follow-up, mitigation, and RESOLVED.
3. Keep a stable case id across all updates.
4. Never overwrite earlier reasoning without leaving a new event.
5. Keep the log factual and operational.

## Markdown daily log pattern
Example headings:
- `## mc-2026-04-15-001 — TRIAGED`
- `## mc-2026-04-15-001 — ASSIGNED`
- `## mc-2026-04-15-001 — NO RESPONSE FOLLOW-UP`
- `## mc-2026-04-15-001 — RESOLVED`
