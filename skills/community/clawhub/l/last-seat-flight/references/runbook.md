# Execution Runbook

## Skill: last-seat-flight

### Overview
Last Seat Flights — Urgent Booking, Final Seat Availability Check

### Execution Log Format

```
[{timestamp}] Step {n}: {action}
  Input: {params}
  Output: {result_summary}
  Status: SUCCESS / FAILURE
```

### Key Metrics

| Metric | Target |
|--------|--------|
| CLI execution success rate | >= 95% |
| Average response time | < 10s |
| Booking link presence | 100% |

### Escalation

- CLI failure after retry -> inform user
- No flights available -> suggest alternative dates/routes
- Parameter extraction failure -> ask user (max 2 questions)
