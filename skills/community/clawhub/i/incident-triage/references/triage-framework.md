# Triage Framework

## Contents

- [Step 1: Classify](#step-1-classify) — alert type and initial severity
- [Step 2: Scope](#step-2-scope) — blast radius, environment, duration
- [Step 3: Correlate](#step-3-correlate) — recent deploys, merges, config changes
- [Step 4: Investigate](#step-4-investigate) — guided checks by alert type
  - [Downtime](#downtime)
  - [Error Spike](#error-spike)
  - [Resource Exhaustion](#resource-exhaustion)
  - [Deployment Failure](#deployment-failure)
  - [Security](#security)
  - [Performance](#performance)
- [Step 5: Act](#step-5-act) — summarize, create ticket, escalate or close

---

Walk through all 5 steps in order for every alert. Don't skip steps — a SEV-4 that skipped correlation can turn into a SEV-1 that nobody saw coming.

## Step 1: Classify

Determine the alert type and assign initial severity.

### Alert Types

| Type | Signals |
|------|---------|
| **Downtime** | Health check failure, 5xx responses, DNS resolution failure, connection refused |
| **Error spike** | Error rate increase, new exception types, elevated 4xx/5xx ratio |
| **Resource exhaustion** | CPU/memory/disk threshold, OOM kills, connection pool exhaustion |
| **Deployment failure** | CI/CD pipeline failure, failed rollout, container crash loop |
| **Security** | Unauthorized access, suspicious activity, exposed credentials, WAF triggers |
| **Performance** | Latency increase, slow queries, timeout rate increase |

### Severity Levels

| Level | Definition | Example |
|-------|-----------|---------|
| **SEV-1** | Customer-facing outage, data loss risk | Production API returning 500s, database unreachable |
| **SEV-2** | Degraded service, partial functionality loss | One region down, elevated error rate, slow responses |
| **SEV-3** | Internal impact, no customer-facing effect | Staging broken, internal tool down, non-critical job failing |
| **SEV-4** | Informational, no immediate action needed | Budget alert, certificate expiring in 30 days, dependency deprecation |

Classify severity *before* investigating. You can upgrade/downgrade later, but having a starting severity drives the response urgency.

## Step 2: Scope

Determine blast radius before diving into root cause.

- **Environment** — production, staging, development, all?
- **Region** — single region, multi-region, global?
- **Services affected** — one service, multiple, entire platform?
- **Users affected** — all users, specific segments, internal only?
- **Duration** — when did it start? Is it ongoing or intermittent?
- **Trend** — getting worse, stable, or recovering?

## Step 3: Correlate

What changed recently? Most incidents are caused by a change.

### Check in order:

1. **Recent deploys** (last 2 hours):
   ```bash
   scripts/correlate-recent-deploys.sh <owner/repo> [hours-back]
   ```

2. **Recent merges to main/production**:
   ```bash
   scripts/correlate-recent-merges.sh <owner/repo> [limit]
   ```

3. **Infrastructure changes** — recent Terraform applies, config changes, scaling events

4. **External factors** — AWS service health, third-party API status, DNS changes

5. **Similar past incidents** — has this happened before? Check incident history.

If you find a correlation, note it but don't stop here — complete the investigation to confirm.

## Step 4: Investigate

Guided investigation based on the alert type from Step 1.

### Downtime
- [ ] Check health endpoints (HTTP status, response time)
- [ ] Check load balancer target health
- [ ] Check container/instance status (running, crash looping, OOM killed)
- [ ] Check DNS resolution
- [ ] Check SSL/TLS certificate validity
- [ ] Check database connectivity
- [ ] Check recent deployment status

### Error Spike
- [ ] Pull error logs — identify the error pattern (same error or multiple types?)
- [ ] Check if errors correlate with a specific endpoint or user action
- [ ] Check if errors started with a deploy (compare timestamps)
- [ ] Check upstream dependencies (are they healthy?)
- [ ] Check request volume (error spike vs traffic spike)

### Resource Exhaustion
- [ ] Check CPU/memory metrics — is it a gradual leak or a sudden spike?
- [ ] Check disk usage — log rotation working? temp files cleaned up?
- [ ] Check connection pools — max connections hit? connections not being released?
- [ ] Check scaling policies — is autoscaling responding? Hitting limits?
- [ ] Check for noisy neighbor (shared resources, multi-tenant)

### Deployment Failure
- [ ] Check CI/CD logs for the specific failure step
- [ ] Check if the same build passed on a previous commit
- [ ] Check for dependency issues (package registry down, version conflicts)
- [ ] Check if infrastructure changes are needed (new env vars, IAM permissions)
- [ ] Check if rollback is needed and possible

### Security
- [ ] Identify the source (IP, user, API key)
- [ ] Check access logs for scope of unauthorized access
- [ ] Check if credentials need rotation
- [ ] Check if the exposure is ongoing or already contained
- [ ] Check CloudTrail / audit logs for related activity

### Performance
- [ ] Identify the slow component (database, external API, application code)
- [ ] Check for query plan changes or missing indexes
- [ ] Check cache hit rates
- [ ] Check if traffic patterns changed
- [ ] Check for resource contention

## Step 5: Act

### Summarize in thread

Post a structured summary:

```
🔴/🟡/🟢 [SEV-X] <short description>

**Status:** Active / Monitoring / Resolved
**Started:** <timestamp>
**Affected:** <services, users, regions>
**Root cause:** <confirmed or suspected>

**What happened:**
<2-3 sentences>

**What we did:**
<actions taken>

**Next steps:**
- [ ] <follow-up action>
- [ ] <follow-up action>
```

### Create ticket

Create an incident ticket with:
- Title: `[SEV-X] <short description>`
- Description: summary from above + investigation findings
- Priority: mapped from severity (SEV-1 → Urgent, SEV-2 → High, SEV-3 → Medium, SEV-4 → Low)
- Labels: `incident`, alert type

```bash
scripts/create-incident-issue.sh <owner/repo> <severity> "<short description>" <body-file>
```

### Escalation decision

Based on severity and findings:
- **SEV-1/SEV-2 unresolved** → escalate per [escalation-guide.md](escalation-guide.md)
- **SEV-3/SEV-4** → ticket created, handled during business hours
- **Resolved during triage** → document what fixed it, close or downgrade
- **False alarm** → note why, consider tuning the alert threshold