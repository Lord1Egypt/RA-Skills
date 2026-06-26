#!/usr/bin/env python3
"""Generate incident response runbook skeleton from service metadata."""

import argparse
from datetime import datetime

TEMPLATE = """# {service} Incident Response Runbook

*Generated: {date}*
*Provider: {provider} | Region: {region}*

## Quick Reference

| Item | Value |
|------|-------|
| Service | {service} |
| Provider | {provider} |
| Region | {region} |
| Monitoring | {monitors} |
| On-call | [Add rotation link] |
| Runbook owner | [Add name] |

## Severity Levels

- **SEV1** — Complete outage, revenue/user impact → respond in **5 min**, all hands
- **SEV2** — Degraded service, user-facing errors → respond in **15 min**, on-call + lead
- **SEV3** — Internal impact, no users affected → respond in **1 hour**, on-call
- **SEV4** — Cosmetic or minor issue → **next business day**

## Triage Checklist

1. [ ] Confirm the issue is real (not a monitoring false positive)
2. [ ] Check dashboards: {monitors}
3. [ ] Identify blast radius (which users/regions/services affected)
4. [ ] Assign severity level
5. [ ] Start incident channel: `#incident-{service_slug}-YYYY-MM-DD`
6. [ ] Post initial status update

## Diagnostic Commands

```bash
# Health check
curl -s https://{service_slug}.example.com/health | jq .

# Recent logs
# AWS: aws logs tail /aws/lambda/{service_slug} --since 30m
# Docker: docker logs {service_slug} --since 30m --tail 500
# K8s: kubectl logs -l app={service_slug} --since=30m --tail=500

# Resource usage
# K8s: kubectl top pods -l app={service_slug}
# Docker: docker stats {service_slug}
```

## Known Failure Modes

### 1. [Add: e.g., Database Connection Exhaustion]

**Symptoms:**
- [What alerts fire]
- [What users see]

**Diagnosis:**
```bash
# [Commands to confirm this specific failure mode]
```

**Mitigation:**
1. [Immediate step to restore service]
2. [Follow-up step]

**Root Fix:**
- [Permanent solution to prevent recurrence]

---

### 2. [Add: e.g., Memory Leak]

**Symptoms:**
- [Gradual response time increase]
- [OOM kills in logs]

**Diagnosis:**
```bash
# [Commands to check memory]
```

**Mitigation:**
1. [Rolling restart]

**Root Fix:**
- [Find and fix the leak]

---

## Rollback Procedure

```bash
# Option 1: Revert to previous deployment
# [deployment-specific rollback command]

# Option 2: Feature flag disable
# [feature flag command]

# Option 3: DNS failover
# [DNS update command]
```

## Communication Templates

### Internal (Slack/Teams)
```
🔴 INCIDENT — {service} — SEV[X]
Impact: [what's broken]
Status: [investigating/mitigating/resolved]
Lead: [name]
Channel: #incident-{service_slug}-[date]
```

### External (Status Page)
```
[Service Name] — [Investigating/Identified/Monitoring/Resolved]

We are aware of issues affecting [description].
Our team is actively investigating.
Updates will be posted every [30 minutes].

Last updated: [time UTC]
```

## Post-Incident Review Template

### Timeline
| Time (UTC) | Event |
|------------|-------|
| HH:MM | [First alert fired] |
| HH:MM | [Incident declared] |
| HH:MM | [Root cause identified] |
| HH:MM | [Mitigation applied] |
| HH:MM | [Service restored] |

### Five Whys
1. Why did the service fail? →
2. Why did that happen? →
3. Why? →
4. Why? →
5. Root cause: →

### Action Items
- [ ] [Preventive action 1] — owner: [name] — due: [date]
- [ ] [Preventive action 2] — owner: [name] — due: [date]
- [ ] [Detection improvement] — owner: [name] — due: [date]
"""

def main():
    p = argparse.ArgumentParser(description="Generate incident response runbook")
    p.add_argument("--service", required=True, help="Service name")
    p.add_argument("--provider", default="generic", help="Cloud provider")
    p.add_argument("--region", default="us-east-1", help="Deployment region")
    p.add_argument("--monitors", default="custom", help="Monitoring tools (comma-separated)")
    p.add_argument("--output", help="Output file path")
    args = p.parse_args()

    service_slug = args.service.lower().replace(" ", "-")
    content = TEMPLATE.format(
        service=args.service,
        service_slug=service_slug,
        provider=args.provider,
        region=args.region,
        monitors=args.monitors,
        date=datetime.now().strftime("%Y-%m-%d"),
    )

    if args.output:
        with open(args.output, "w") as f:
            f.write(content)
        print(f"Runbook written to {args.output}")
    else:
        print(content)

if __name__ == "__main__":
    main()
