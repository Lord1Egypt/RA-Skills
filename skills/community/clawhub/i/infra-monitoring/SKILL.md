---
name: infra-monitoring
description: Monitor server health, uptime, resource utilization, SSL certificate expiry, and incident detection for small teams and self-hosters. Delivers plain-language status reports prioritizing what needs attention, not metric dumps. Supports single-server health checks, HTTP/TCP uptime pings, and incident timelines without enterprise tooling overhead.
---

# Infrastructure & Uptime Monitoring

Monitor your servers and endpoints like a sharp ops engineer who tells you what needs attention, not a dashboard that dumps 47 numbers.

## Trigger conditions

Activate this skill when the user:
- Asks to check server health, status, or resource usage
- Provides server metrics (CPU, memory, disk, network) for assessment
- Asks about uptime, downtime, or availability of endpoints
- Asks to check SSL certificate expiry dates
- Provides system output from commands like `top`, `htop`, `df`, `free`, `uptime`, `vmstat`, `iostat`
- Asks for a status report on their infrastructure
- Mentions monitoring, health checks, or incident detection for servers
- Asks about capacity planning or resource trending
- Provides ping, curl, or HTTP response data for analysis
- Asks to set up monitoring for a new server or endpoint

Do NOT activate when:
- The user wants application-level business metrics (suggest data-analysis-reporting skill)
- The user needs APM or distributed tracing (suggest Datadog/New Relic)
- The user wants to build a monitoring dashboard UI
- The user needs real-time streaming metrics ingestion
- The user wants network security scanning or penetration testing
- The user asks about cloud provider billing or cost optimization without infra context

## Work the request in this order

1. **Understand the scope** — before running any checks, understand what the user is monitoring and why:
   - "What servers or endpoints do you need checked?"
   - "Is this a routine check or are you investigating a specific issue?"
   - "What does 'healthy' look like for your setup?"
   If the user provides clear context (paste of system metrics, specific endpoint to check), skip to step 2.

2. **Gather the data** — collect or parse the infrastructure data:
   - Parse user-provided system command output (top, df, free, uptime, etc.)
   - Execute HTTP/HTTPS checks against provided endpoints
   - Parse provided log snippets or monitoring data exports
   - Detect the data type and validate completeness
   - If data is insufficient for a meaningful assessment, ask for specifics before proceeding

3. **Assess health** — evaluate each metric against thresholds:
   - Classify each metric as **healthy**, **warning**, or **critical** using `references/metrics-thresholds.md`
   - Consider context: 85% disk on a 20GB volume is more urgent than on a 2TB volume
   - Detect change direction: is the metric stable, climbing, or dropping
   - Identify correlations: high CPU + high swap often means memory pressure, not CPU problem
   - Check for compound risk: multiple warnings that individually are fine but together signal trouble

4. **Build the status report** — structured output following the default format below:
   - Lead with what needs attention, not what's fine
   - Group related issues (don't spam 5 separate disk alerts for one full server)
   - Include temporal context: is this new, ongoing, or recurring
   - Note what has improved since last check (if prior context available)

5. **Recommend actions** — concrete next steps prioritized by urgency:
   - Immediate actions for critical items
   - Scheduled maintenance for warning items
   - Monitoring adjustments for better visibility
   - Capacity planning notes for trending concerns

## Default output structure

Use this structure unless the user clearly wants a different format:

1. **Attention required** — the critical and warning items, sorted by severity then urgency. Each item:
   - What is the issue (plain language)
   - How severe (critical / warning)
   - What action to take
   - How urgent (act now / schedule this week / monitor)

   If nothing needs attention: "All systems healthy. No action required."

2. **Server health summary** — per-server overview:
   - Hostname / identifier
   - Overall status: healthy / warning / critical
   - Key metrics: CPU, memory, disk, uptime
   - One-line assessment ("Running well, disk growing steadily — ~45 days until 90%")

3. **Endpoint status** — per-endpoint overview:
   - URL / endpoint identifier
   - Status: up / degraded / down
   - Response time and status code
   - SSL certificate days remaining (if HTTPS)
   - Uptime percentage over monitoring window

4. **Resource trends** — directional indicators for key metrics:
   - Which metrics are climbing, stable, or dropping
   - Rate of change where meaningful
   - Projected thresholds (e.g., "disk will hit 90% in ~30 days at current growth")
   - Comparison to prior check if available

5. **Incident timeline** — recent events if any:
   - When the incident started and ended (or "ongoing")
   - What triggered detection
   - Impact assessment
   - Resolution or current mitigation status

6. **Recommended actions** — 3 concrete next steps:
   - One immediate action (if anything is critical or warning)
   - One preventive measure (based on trends)
   - One monitoring improvement (better visibility for next time)

7. **System details** — raw metric values for reference:
   - Full metric breakdown per server
   - Presented in a clean table format
   - Thresholds shown alongside actuals
   - This section is for the user who wants the numbers after reading the summary

## Health assessment logic

Apply thresholds from `references/metrics-thresholds.md` with these principles:

- **Context matters more than absolute numbers.** A web server at 70% CPU during peak hours is different from 70% at 3 AM.
- **Trends matter more than snapshots.** 60% disk usage climbing 2% per day is more urgent than 80% stable for months.
- **Compound signals.** High CPU + high memory + high disk I/O together = investigate. Any one alone at warning level = monitor.
- **Volume-aware thresholds.** Percentage thresholds must account for absolute capacity. 90% of 10GB needs action sooner than 90% of 1TB.
- **Uptime context.** A 12-minute outage matters more for an API endpoint than for a weekly batch job server.

## Severity classification

Read `references/alert-severity.md` for the full classification system. Summary:

| Severity | Meaning | Response |
|---|---|---|
| **Critical** | Service impacted or imminent failure | Act now |
| **Warning** | Approaching threshold or degraded but functional | Schedule fix this week |
| **Healthy** | Within normal operating parameters | No action needed |
| **Unknown** | Insufficient data to classify | Investigate or provide more data |

## SSL certificate monitoring

When checking HTTPS endpoints:
- Report days until certificate expiry
- Determine the renewal type before applying thresholds:

**Auto-renew certs** (Let's Encrypt, managed cloud certs, etc.):
- **Critical**: <7 days remaining (renewal has almost certainly failed)
- **Warning**: <14 days remaining (renewal should have triggered — investigate)
- **Healthy**: >14 days remaining

**Manual renewal certs** (purchased certs, enterprise CA, self-managed):
- **Critical**: <14 days remaining (not enough lead time for procurement/install)
- **Warning**: <45 days remaining (start renewal process now)
- **Healthy**: >45 days remaining

**Unknown renewal type** (cannot determine auto vs. manual):
- **Critical**: <7 days remaining
- **Warning**: <30 days remaining
- **Healthy**: >30 days remaining

How to determine renewal type: check the certificate issuer. Let's Encrypt, AWS ACM, Cloudflare, and Google-managed certs are auto-renew. Enterprise CAs (DigiCert, Sectigo, internal PKI) and self-signed certs are typically manual. When in doubt, classify as unknown and note the ambiguity.

- Flag certificate chain issues, mismatched hostnames, or expired intermediate certs

## Incident detection and grouping

When multiple alerts fire for the same root cause:
- Group them into a single incident narrative
- Identify the likely root cause ("disk full caused the database to stop, which caused the API to return 500s" = one incident, not three)
- Track the timeline: first detection, escalation, peak impact, resolution
- Generate a plain-language post-incident summary

## Sparse-data and partial-check handling

When the user provides incomplete data:

1. **Assess what you can** — don't refuse the whole check because one metric is missing
2. **Name the gaps** — "I can assess CPU and memory but you didn't provide disk usage — want me to check?"
3. **Adjust confidence** — partial data gets a qualified assessment, not a definitive one
4. **Suggest the full picture** — "For a complete health check, I'd also need: [list]"

## No-data gate

When the user asks for monitoring but provides no server details or metrics:

1. Ask what they're monitoring (server, endpoint, or both)
2. Suggest the minimum viable check: provide hostname/IP and what services run on it
3. Offer a starter monitoring checklist from `references/monitoring-checklists.md`
4. Provide a sample health check output so they know what to expect

Do not generate fictional server metrics or pretend to check nonexistent infrastructure.

## Boundaries

- **No access without explicit configuration.** Do not connect to servers, endpoints, or services unless the user explicitly provides connection details.
- **No credential storage in skill files.** Never write passwords, API keys, SSH keys, or connection strings to output. Reference environment variables or secret managers only.
- **No direct remediation — guidance only.** This skill provides monitoring, diagnosis, and guidance. It does not execute remediation actions (restarting services, deleting files, scaling resources, modifying configurations) directly. When the user requests remediation, provide step-by-step guidance and commands they can run themselves. Explain risks before each step.
- **Monitoring data vs. diagnostic speculation.** Clearly separate observed facts ("CPU is at 92%") from inferences ("likely caused by the Java process using 4.2GB heap"). Label each.
- **No real-time detection guarantee.** The skill runs on-demand or at check intervals. It is not a kernel-level monitor or hardware watchdog. State this clearly.
- **No PII in monitoring output.** If server responses contain user data, exclude it from reports and incident logs.
- **Scope: infrastructure, not application.** This skill monitors servers and endpoints, not business-level KPIs. Recommend the data-analysis-reporting skill for business data analysis.
