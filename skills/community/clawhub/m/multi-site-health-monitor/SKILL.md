---
name: multi-site-health-monitor
description: "Monitor dozens of websites with configurable health checks, auto-restart alerts, and intelligent alert routing. Use when the user needs uptime tracking, performance monitoring, or automated incident response across multiple domains."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["SLACK_WEBHOOK_URL","PAGERDUTY_API_KEY","DATADOG_API_KEY"],"bins":["curl","jq"]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"📡"}}
---

# Multi-Site Health Monitor

## Overview

The **Multi-Site Health Monitor** skill automates continuous monitoring of 10-100+ websites with configurable health checks, intelligent alert routing, and automatic incident escalation. This production-grade monitoring solution integrates with **Slack**, **PagerDuty**, **Datadog**, **Google Sheets**, and **WordPress** to provide real-time visibility into your digital infrastructure.

### Why This Matters
- **Prevent Revenue Loss**: Detect downtime in seconds, not hours
- **Reduce Alert Fatigue**: Smart thresholds and deduplication prevent notification overload
- **Automate Incident Response**: Auto-restart failed services, escalate to on-call teams
- **Multi-Channel Alerts**: Route critical issues to PagerDuty, warnings to Slack, metrics to Datadog
- **Historical Analysis**: Track uptime trends, identify patterns, generate compliance reports

### Key Integrations
- **Slack**: Real-time alerts, incident channels, status dashboards
- **PagerDuty**: Automatic incident creation, on-call escalation, incident tracking
- **Datadog**: Metric ingestion, custom dashboards, anomaly detection
- **Google Sheets**: Automated reporting, SLA tracking, audit logs
- **WordPress**: Monitor plugin health, theme updates, core vulnerabilities
- **AWS/Azure**: Auto-restart EC2 instances, trigger Lambda functions, scale infrastructure

---

## Quick Start

Try these example prompts immediately:

### Example 1: Monitor 5 Critical Sites with Slack Alerts
```
Monitor these sites every 5 minutes and alert Slack if any fail:
- https://api.example.com/health
- https://app.example.com/status
- https://cdn.example.com/ping
- https://wordpress.example.com/wp-json/health
- https://db.example.com/check

Alert rules:
- Critical (page down): Slack #incidents + PagerDuty
- Warning (slow >3s): Slack #alerts
- Info (cert expires <30d): Google Sheets log
```

### Example 2: Auto-Restart Failed Services
```
Monitor https://payment-service.example.com/health every 2 minutes.
If it fails 3 times in a row:
1. POST to https://restart-api.example.com/restart-payment-service
2. Alert PagerDuty with incident "Payment Service Down"
3. Notify Slack #critical-incidents
4. Log to Google Sheets with timestamp, error details, restart status

Response timeout: 10 seconds
Expected response: HTTP 200 with {"status":"healthy"}
```

### Example 3: WordPress Multi-Site Monitoring
```
Monitor these WordPress sites for health + security:
- https://site1.example.com/wp-json/wp/v2/health-check
- https://site2.example.com/wp-json/wp/v2/health-check
- https://site3.example.com/wp-json/wp/v2/health-check

Check for:
- Core updates available (warning if >1 week old)
- Plugin vulnerabilities (critical if any)
- Database connectivity (critical if down)
- SSL certificate expiry (warning if <30 days)

Alert destinations:
- Critical: PagerDuty + Slack #wordpress-critical
- Warning: Slack #wordpress-alerts
- Info: Google Sheets #monitoring-log
```

### Example 4: Performance Threshold Monitoring
```
Monitor https://api.example.com/metrics every 10 minutes.
Alert if:
- Response time > 2000ms (warning) or > 5000ms (critical)
- Error rate > 1% (warning) or > 5% (critical)
- CPU usage > 70% (warning) or > 90% (critical)
- Memory usage > 80% (warning) or > 95% (critical)

Send metrics to Datadog with tags: env:prod, service:api, team:backend
```

---

## Capabilities

### 1. **Multi-Protocol Health Checks**
Monitor endpoints via:
- **HTTP/HTTPS**: GET, POST, HEAD requests with custom headers
- **TCP**: Port connectivity checks (e.g., database ports 3306, 5432)
- **DNS**: Domain resolution, DNS propagation verification
- **SSL/TLS**: Certificate validity, expiration warnings, chain verification
- **Ping/ICMP**: Basic connectivity for infrastructure nodes

**Example**: Monitor API health with custom authentication
```
Endpoint: https://api.example.com/health
Method: POST
Headers: 
  Authorization: Bearer YOUR_API_KEY
  User-Agent: MultiSiteMonitor/1.0.0
Expected Status: 200
Expected Body: {"status":"healthy","version":"2.1.0"}
Timeout: 10 seconds
```

### 2. **Intelligent Alert Routing**
- **Severity-Based Routing**: Critical → PagerDuty + Slack + SMS, Warning → Slack only, Info → Sheets log
- **Deduplication**: Suppress duplicate alerts within 5-minute window
- **Escalation Rules**: Auto-escalate if critical issue unresolved for 30+ minutes
- **Custom Thresholds**: Define per-endpoint sensitivity (e.g., API endpoint stricter than blog)
- **Quiet Hours**: Suppress non-critical alerts during maintenance windows

### 3. **Automatic Incident Response**
- **Webhook Triggers**: POST to custom endpoints (restart services, scale infrastructure)
- **AWS Integration**: Auto-restart EC2 instances, trigger Lambda functions
- **Service Restart**: Execute shell commands on remote servers via SSH
- **Rollback Triggers**: Revert deployments if health checks fail
- **Notification Actions**: Create tickets in Jira, GitHub Issues, or Linear

### 4. **Performance Metrics & Trending**
- **Response Time Tracking**: Detect slowdowns before they become critical
- **Uptime Calculation**: Real-time SLA tracking (99.9%, 99.95%, 99.99%)
- **Error Rate Monitoring**: Track HTTP 4xx, 5xx, timeout errors
- **Datadog Integration**: Send custom metrics for dashboards and alerts
- **Historical Reporting**: Generate monthly uptime reports, SLA compliance docs

### 5. **WordPress-Specific Monitoring**
- **Core Updates**: Alert when WordPress core updates available
- **Plugin Vulnerabilities**: Check against WordPress vulnerability database
- **Theme Security**: Monitor for outdated or vulnerable themes
- **Database Health**: Monitor wp_options, table integrity, query performance
- **User Activity**: Track suspicious login attempts, new admin accounts
- **Backup Verification**: Confirm backups complete successfully

### 6. **Compliance & Audit Logging**
- **Google Sheets Integration**: Automatic logging of all checks, alerts, actions
- **Audit Trail**: Who triggered what, when, and what happened
- **SLA Reports**: Monthly/quarterly compliance reports (99.9% uptime proof)
- **Change Tracking**: Document all configuration changes with timestamps
- **Export Formats**: CSV, JSON, PDF for compliance submissions

---

## Configuration

### Required Environment Variables
```bash
# Slack notifications
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
export SLACK_CHANNEL="#incidents"  # or #alerts, #monitoring, etc.

# PagerDuty incident creation
export PAGERDUTY_API_KEY="YOUR_PAGERDUTY_API_KEY"
export PAGERDUTY_SERVICE_ID="YOUR_SERVICE_ID"

# Datadog metrics ingestion
export DATADOG_API_KEY="YOUR_DATADOG_API_KEY"
export DATADOG_APP_KEY="YOUR_DATADOG_APP_KEY"
export DATADOG_SITE="datadoghq.com"  # or datadoghq.eu

# Google Sheets logging
export GOOGLE_SHEETS_ID="YOUR_SPREADSHEET_ID"
export GOOGLE_SERVICE_ACCOUNT_JSON="/path/to/service-account.json"

# AWS auto-restart (optional)
export AWS_ACCESS_KEY_ID="YOUR_AWS_KEY"
export AWS_SECRET_ACCESS_KEY="YOUR_AWS_SECRET"
export AWS_REGION="us-east-1"

# SSH for remote service restart (optional)
export SSH_PRIVATE_KEY="/path/to/private/key"
export SSH_USER="deploy"
```

### Configuration File Format (YAML)
```yaml
# monitors.yaml
monitors:
  - name: "Production API"
    url: "https://api.example.com/health"
    interval: 300  # seconds
    timeout: 10
    method: "GET"
    expected_status: 200
    expected_body_contains: "healthy"
    alert_rules:
      critical:
        - slack_channel: "#critical-incidents"
        - pagerduty_severity: "critical"
      warning:
        - slack_channel: "#alerts"
    auto_restart:
      enabled: true
      command: "systemctl restart api-service"
      max_retries: 3
      retry_delay: 60

  - name: "WordPress Site"
    url: "https://wordpress.example.com/wp-json/wp/v2/health-check"
    interval: 600
    timeout: 15
    method: "GET"
    headers:
      Authorization: "Bearer YOUR_WP_TOKEN"
    checks:
      - type: "wordpress_core_updates"
        alert_if: "available"
        severity: "warning"
      - type: "plugin_vulnerabilities"
        alert_if: "found"
        severity: "critical"
      - type: "ssl_certificate"
        expires_in_days: 30
        severity: "warning"
    alert_rules:
      critical:
        - pagerduty_severity: "critical"
        - slack_channel: "#wordpress-critical"
      warning:
        - slack_channel: "#wordpress-alerts"
        - google_sheets: true

  - name: "Database Health"
    url: "https://db-monitor.example.com/health"
    interval: 120
    timeout: 20
    method: "POST"
    headers:
      Content-Type: "application/json"
      Authorization: "Bearer YOUR_DB_TOKEN"
    body: '{"check":"full"}'
    expected_status: 200
    performance_thresholds:
      response_time_ms: 2000
      error_rate_percent: 1.0
    alert_rules:
      critical:
        - pagerduty_severity: "critical"
        - datadog_metric: "db.health.critical"
      warning:
        - datadog_metric: "db.health.warning"
        - slack_channel: "#database-alerts"
```

### Setup Instructions
1. **Create monitoring config**: Save YAML above as `monitors.yaml`
2. **Set environment variables**: Source `.env` file with all required API keys
3. **Initialize Google Sheets**: Create spreadsheet, share with service account email
4. **Test endpoints**: Run `multi-site-health-monitor --validate` to verify all URLs respond
5. **Deploy**: Run as systemd service or Docker container for continuous monitoring

---

## Example Outputs

### Slack Alert (Critical)
```
🚨 CRITICAL: Production API Down
Service: Production API (api.example.com/health)
Status: HTTP 500 Internal Server Error
Response Time: 12.3s (timeout threshold: 10s)
Last Healthy: 2024-01-15 14:32:15 UTC
Incident Duration: 5 minutes 23 seconds
Alert Count: 3 consecutive failures

Auto-Restart Status: ✅ Triggered (attempt 1/3)
PagerDuty Incident: INC-12345 (assigned to @oncall-backend)

Next Check: 2024-01-15 14:42:15 UTC
Escalation: Will escalate to #management if unresolved in 25 minutes
```

### Google Sheets Log Entry
```
Timestamp          | Service           | Status | Response Time | Error       | Action Taken
2024-01-15 14:37   | Production API    | FAIL   | 12300ms       | HTTP 500    | Auto-restart triggered
2024-01-15 14:32   | Production API    | FAIL   | 10100ms       | Timeout     | Alert sent
2024-01-15 14:27   | Production API    | OK     | 245ms         | -           | -
2024-01-15 14:22   | WordPress Site    | WARN   | 3200ms        | Slow        | Alert sent
2024-01-15 14:17   | Database Health   | OK     | 145ms         | -           | -
```

### PagerDuty Incident
```
Incident: INC-12345
Service: Production API
Severity: Critical
Status: Triggered
Title: Production API Down - HTTP 500 (5min+ duration)
Description: 
  Endpoint: https://api.example.com/health
  Status: HTTP 500 Internal Server Error
  Response Time: 12.3s
  Consecutive Failures: 3
  Last Healthy: 2024-01-15 14:32:15 UTC
  Auto-Restart: Triggered (attempt 1/3)
  
Assigned To: @oncall-backend
Created: 2024-01-15 14:37:00 UTC
Escalation Policy: Backend On-Call → Manager → VP Engineering
```

### Datadog Metrics Sent
```
multi_site_monitor.health_check.response_time:245ms (tags: service:api, env:prod)
multi_site_monitor.health_check.status:200 (tags: service:api, env:prod)
multi_site_monitor.health_check.availability:99.87 (tags: service:api, env:prod)
multi_site_monitor.auto_restart.attempts:1 (tags: service:api, env:prod)
```

---

## Tips & Best Practices

### 1. **Optimal Check Intervals**
- **Critical APIs**: 60-120 seconds (detects issues in 2-4 minutes)
- **Standard Services**: 300 seconds (5 minutes, good balance)
- **Non-Critical Endpoints**: 600-900 seconds (10-15 minutes, reduces noise)
- **Batch Jobs**: 1800+ seconds (30+ minutes, less frequent monitoring)

### 2. **Threshold Tuning**
- **Start Conservative**: Begin with loose thresholds, tighten over 2 weeks
- **Account for Variance**: Set response time thresholds 2-3x slower than baseline
- **Error Rate**: 0.1-1% warning, 5%+ critical (adjust per service SLA)
- **Test Thresholds**: Deliberately fail endpoints to verify alert routing works

### 3. **Reducing Alert Fatigue**
- **Deduplication**: Suppress identical alerts within 5-minute window
- **Smart Escalation**: Only escalate if issue persists >30 minutes
- **Quiet Hours**: Disable non-critical alerts 2am-6am (adjust per timezone)
- **Severity Mapping**: Not everything is critical; use warning/info for minor issues

### 4. **WordPress-Specific Best Practices**
- **Check Core Updates Weekly**: Set interval to 604,800 seconds (7 days)
- **Monitor Plugin Health Daily**: Check for vulnerabilities, outdated plugins
- **Database Backups**: Verify backup completion status in health endpoint
- **Staging Environment**: Monitor staging sites separately to catch issues before production
- **Custom Health Endpoints**: Create `/wp-json/custom/health` returning comprehensive data

### 5. **Cost Optimization**
- **Batch Checks**: Group 5-10 checks into single HTTP request where possible
- **Datadog Sampling**: Send detailed metrics every 5 minutes, summary every hour
- **Google Sheets**: Batch writes (max 100 rows per request) to reduce API calls
- **PagerDuty**: Use deduplication to avoid triggering duplicate incidents

### 6. **Security Hardening**
- **API Key Rotation**: Rotate all API keys monthly
- **VPC Monitoring**: Monitor internal endpoints from private subnets only
- **IP Whitelisting**: Restrict health check endpoints