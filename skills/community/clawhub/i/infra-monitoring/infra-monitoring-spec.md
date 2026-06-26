# Infrastructure & Uptime Monitoring — Skill Spec v0.1

## Purpose

Give small teams, solo operators, and self-hosters a practical infrastructure monitoring skill — server health, uptime tracking, resource utilization, SSL cert expiry, and incident detection without enterprise tooling overhead.

The skill should feel like a sharp ops engineer giving you a plain-language status report, not a dashboard dumping metrics. Lead with "here's what needs your attention" not "here are 47 numbers."

## Target Users

- **Indie developers** running OpenClaw/Paperclip instances on VPS or bare metal
- **Small hosting providers** managing a handful of client servers without Datadog-level spend
- **DevOps teams at startups** who need monitoring but can't justify $30+/server/month tooling
- **Self-hosters** managing VPS fleets, home labs, or side-project infrastructure
- **Solo SaaS operators** who need to know when their service is down before their users do

## Core Capabilities (Free Tier)

### Single-Server Health Checks
- CPU utilization: current load, load average (1m/5m/15m), process count
- Memory: total, used, available, swap usage, OOM risk assessment
- Disk: usage per mount, inode usage, growth rate estimation, days-until-full projection
- Network: interface status, basic throughput, error/drop counts
- System: uptime, kernel version, pending security updates, reboot-required flags

### Uptime Ping Monitoring
- HTTP/HTTPS endpoint checks with status code validation
- Response time measurement and latency tracking
- SSL certificate expiry detection and days-remaining countdown
- DNS resolution checks
- TCP port connectivity verification
- Plain-language uptime summaries ("your API has been up 99.7% this week, with one 12-minute outage Tuesday at 3:14 AM UTC")

### Status Summaries
- Plain-language health assessments per server/endpoint
- Traffic-light severity: healthy / warning / critical
- "Needs your attention" prioritized list — most urgent items first
- Change detection: what shifted since last check
- Resource trend direction: stable, climbing, dropping

### Incident Log
- Timeline of detected issues with severity and duration
- Automatic incident grouping (related alerts clustered, not spammed)
- Resolution tracking: when did the metric return to healthy
- Post-incident summary generation

## Premium Capabilities (Future Roadmap)

### Multi-Server Fleet Monitoring
- Fleet-wide dashboard summaries across N servers
- Comparative health: which server is the outlier
- Resource allocation analysis across the fleet
- Capacity planning recommendations

### Response Time Analytics
- Endpoint performance trending over time
- P50/P95/P99 latency breakdowns
- Geographic response time variance (if multi-region)
- Degradation detection before full outage

### Alerting Integrations
- PagerDuty integration for on-call escalation
- Slack channel notifications with severity routing
- Email digest reports (daily/weekly)
- Webhook support for custom integrations
- Alert deduplication and flood protection

### Scheduled Reports
- Daily health digest: overnight events, current state, day's outlook
- Weekly trend report: resource usage direction, uptime stats, incident recap
- Monthly capacity review: growth projections, cost-per-server tracking
- Historical trend analysis with anomaly flagging

### Cost Tracking
- Per-server cost attribution (if user provides pricing)
- Cost-per-uptime-point analysis
- Capacity vs. spend efficiency scoring
- Rightsizing recommendations

## Boundaries

- **No access without explicit configuration.** The skill does not connect to servers, endpoints, or services unless the user explicitly provides connection details and credentials.
- **No credential storage in skill files.** Connection strings, API keys, SSH keys, and passwords must never be written to skill output files. Reference environment variables or secret managers only.
- **No automated remediation without user approval.** The skill monitors and reports. It does not restart services, kill processes, scale infrastructure, or modify system configuration unless the user explicitly requests and confirms the action.
- **Monitoring data vs. diagnostic speculation.** Clearly separate what the data shows (CPU is at 92%) from what might be causing it (possible memory leak in process X). Label observations as facts and interpretations as inferences.
- **No guarantee of real-time detection.** The skill operates within its check interval. It is not a replacement for kernel-level monitoring, APM, or hardware watchdogs. State this clearly.
- **No PII in monitoring output.** If server responses contain user data, the skill must not include that data in status reports or incident logs.
- **Scope limit: infrastructure, not application.** The skill monitors servers and endpoints, not application-level business metrics. Recommend the data-analysis-reporting skill for business data.

## Differentiation

### vs. Datadog / New Relic / Grafana Cloud
- Zero setup: describe your server and endpoints, get a status report
- No agent installation required for basic checks (ping, HTTP, SSL)
- Plain-language output instead of metric dashboards
- Fraction of the cost for small-scale monitoring
- Trade-off: less depth, no APM, no distributed tracing, no real-time streaming

### vs. UptimeRobot / Pingdom
- Infrastructure-aware: not just "is the URL up" but "how is the server doing"
- Resource utilization context alongside uptime
- Incident narratives instead of just alert/resolve timestamps
- Integrated with the OpenClaw skill ecosystem
- Trade-off: not a dedicated uptime SaaS with 1-minute checks from 10 global locations

### vs. DIY scripts (cron + curl + Slack webhook)
- Structured, consistent output format
- Built-in threshold intelligence (knows what "high CPU" means in context)
- Incident grouping and timeline generation
- No scripting or maintenance required
- Trade-off: less customizable than writing your own monitoring stack

### vs. Generic LLM "check my server"
- Structured workflow (configure -> check -> assess -> report -> recommend)
- Consistent severity classification with defined thresholds
- Historical context awareness (change detection, not just point-in-time snapshots)
- Monitoring-specific knowledge built in (knows that 85% disk on a 20GB volume is more urgent than 85% on a 2TB volume)

## Market Context

- Only 1-2 basic infrastructure monitoring offerings on ClawHub
- The shift to self-hosted AI (OpenClaw itself) creates a natural user base that needs this
- Enterprise monitoring tools are overkill and overpriced for 1-10 server setups
- The "sharp ops engineer on call" framing fills a gap between DIY scripts and enterprise platforms
- Adjacent to our data-analysis-reporting skill — natural cross-sell for operators who want both business and infra visibility

## Success Metrics (Post-Launch)

- Activation: >35% of users who trigger the skill complete at least one full health check
- Retention: >30% return within 7 days for another check (infra monitoring is more frequent than data analysis)
- Accuracy: <5% false-positive rate on warning/critical classifications
- Revenue signal: >8% of free-tier users inquire about fleet monitoring or alerting features within 30 days
- User satisfaction: status reports are actionable — users take action on >50% of "needs attention" items
