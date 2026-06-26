# INCIDENTS.md — Production Incident Log

> Log all production-level failures, issues, and near-misses. Severity classification required.

---

## Last Incident: None Recorded

---

## Severity Classification

| Level | Definition | Response Time |
|-------|------------|---------------|
| `CRITICAL` | Production down, data loss risk, security breach | Immediate escalation |
| `HIGH` | Major feature impacted, degraded performance | < 15 minutes |
| `MEDIUM` | Minor impact, workarounds available | < 1 hour |
| `LOW` | Cosmetic, documentation, minor inconvenience | Next business day |

---

## Template: Log New Incident

```
## Incident: <title>

### Severity: LOW | MEDIUM | HIGH | CRITICAL

### Detected: <ISO 8601 timestamp>

### Description:
<what happened>

### Impact:
<affected systems, users, services>

### Root Cause:
<technical root cause>

### Resolution:
<steps taken to resolve>

### Follow-up Actions:
- [ ] <action> - @<assignee> - <due date>
- [ ] <action> - @<assignee> - <due date>

### Lessons Learned:
<what could be improved>

### Related Logs:
<links to LOGS.md entries>
```

---

## Incident Categories

| Category | Examples |
|----------|----------|
| `CLUSTER_FAILURE` | Node down, API server outage, etcd issues |
| `DEPLOYMENT_FAILURE` | Failed GitOps sync, helm failures |
| `SECURITY_INCIDENT` | Unauthorized access, CVE, policy violation |
| `PERFORMANCE_DEGRADATION` | High latency, resource exhaustion |
| `DATA_LOSS` | Backup failure, data corruption |
| `AUTOMATION_FAILURE` | Skill/script errors |
| `CONFIGURATION_DRIFT` | Unintended state changes |

---

## Escalation Triggers

Create incident automatically when:

1. **Cluster availability < 99.9%**
2. **Security policy violation detected**
3. **Failed deployment to production**
4. **Data integrity concern**
5. **Agent unable to resolve within 3 attempts**
6. **Human approval requested and denied**
7. **Any deletion of production resources**

---

## Post-Incident Requirements

1. Document in INCIDENTS.md within 24 hours
2. Create TROUBLESHOOTING.md entry if new problem type
3. Update MEMORY.md with lessons learned
4. Assign follow-up actions with owners
5. Schedule incident review if severity HIGH or CRITICAL
