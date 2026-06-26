# Alert Patterns

## Contents

- [PagerDuty](#pagerduty)
- [Datadog](#datadog)
- [AWS CloudWatch](#aws-cloudwatch)
- [AWS SNS / EventBridge](#aws-sns--eventbridge)
- [Uptime Monitors](#uptime-monitors-better-uptime-uptime-robot-pingdom)
- [GitHub Actions](#github-actions)
- [Sentry / Error Trackers](#sentry--error-trackers)
- [Custom Webhooks / Generic Alerts](#custom-webhooks--generic-alerts)

---

How to parse alerts from common monitoring sources. Extract key fields to feed into the triage framework.

## PagerDuty

**Signals:** messages containing `TRIGGERED`, `ACKNOWLEDGED`, `RESOLVED`

**Extract:**
- Service name (which service is affected)
- Severity/urgency (high, low)
- Description (what the monitor detected)
- Trigger time
- Incident URL (for details and timeline)

## Datadog

**Signals:** messages containing `Monitor Alert`, `Warn`, `Alert`, `Recovered`, `No Data`

**Extract:**
- Monitor name (identifies what's being checked)
- Status (Alert, Warn, OK, No Data)
- Tags (environment, service, region — usually in `key:value` format)
- Metric value and threshold (what triggered it)
- Graph/dashboard link

**Note:** `No Data` alerts often indicate the metric source itself is down (agent, service, network) — treat as potential downtime, not just a missing metric.

## AWS CloudWatch

**Signals:** messages containing `ALARM`, `OK`, `INSUFFICIENT_DATA`

**Extract:**
- Alarm name (usually follows a naming convention like `<env>-<service>-<metric>`)
- State (ALARM, OK, INSUFFICIENT_DATA)
- Metric name and namespace (e.g., `AWS/ECS CPUUtilization`)
- Threshold and current value
- Region and account (if multi-account)

**Common patterns:**
- `CPUUtilization > 80%` → resource exhaustion
- `HealthyHostCount < 1` → downtime
- `5XXError > threshold` → error spike
- `EstimatedCharges > budget` → cost alert (SEV-4)

## AWS SNS / EventBridge

**Signals:** JSON payloads via webhook or Slack integration

**Extract:**
- `Subject` or `Message` field for the alert summary
- `TopicArn` to identify the alert source
- Parse the JSON `Message` body for structured data (alarm details, state change)

## Uptime Monitors (Better Uptime, Uptime Robot, Pingdom)

**Signals:** messages containing `DOWN`, `UP`, `degraded`, `maintenance`

**Extract:**
- Monitor name / URL being checked
- Status (down, up, degraded)
- Response code (if available)
- Downtime duration (on recovery alerts)
- Check location/region

## GitHub Actions

**Signals:** messages containing workflow run status — `completed`, `failure`, `success`, `cancelled`

**Extract:**
- Repository and workflow name
- Branch (main, staging, feature)
- Conclusion (success, failure, cancelled)
- Failed step name (from the run details)
- Commit SHA and author

```bash
# Get details on a failed run
gh run view <run-id> --repo <owner/repo> --json conclusion,name,headBranch,jobs
gh run view <run-id> --repo <owner/repo> --log-failed
```

## Sentry / Error Trackers

**Signals:** messages containing `New issue`, `Regression`, `Resolved`, exception names

**Extract:**
- Error title / exception type
- Frequency (first occurrence vs regression)
- Affected users count
- Stack trace location (file, line)
- Release/version where it appeared

## Custom Webhooks / Generic Alerts

For alerts that don't match known patterns:

1. Check if the message is JSON — parse and extract structured fields
2. Look for severity indicators: `critical`, `warning`, `error`, `info`
3. Look for service identifiers: hostnames, URLs, service names
4. Look for timestamps
5. Look for metric values and thresholds

When in doubt, ask the user what monitoring system sent the alert.

## General Note

For PagerDuty, Datadog, CloudWatch, and other third-party tools, deeper investigation requires accessing their UI or API (which needs tool-specific credentials). During triage, use the links/URLs in the alert message to jump directly to the relevant dashboard, incident, or alarm detail page. The `gh` CLI covers deploy correlation — the monitoring tools themselves handle metric and log investigation.