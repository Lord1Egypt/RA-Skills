# Alert Severity Classification System

## Severity Levels

### Critical

**Definition:** Service is impacted, data is at risk, or failure is imminent without intervention.

**Characteristics:**
- User-facing service is down or returning errors
- Resource exhaustion is imminent (<1 hour at current rate)
- Data integrity is threatened (disk full on database volume, backup failures)
- Security compromise detected or critical vulnerability exposed

**Response expectation:** Act now. Drop other work. This is the fire.

**Examples:**
- Disk usage >95% on database volume
- All HTTP checks returning 5xx
- SSL certificate expired or expiring within 24 hours
- OOM killer actively terminating processes
- Load average >2x core count sustained for 15+ minutes
- No successful backup in 48+ hours

**Escalation:** If unresolvable within 30 minutes, escalate to the next person in your chain.

### Warning

**Definition:** System is functional but degraded, approaching limits, or showing concerning trends.

**Characteristics:**
- Performance is degraded but service is available
- Resource usage is above comfortable levels but not imminently dangerous
- A metric has crossed a soft threshold and is trending in the wrong direction
- A non-critical component has failed (redundancy is covering it)

**Response expectation:** Schedule a fix within 1-3 business days. Monitor for escalation to critical.

**Examples:**
- Disk usage 80-90% with positive growth trend
- Response times 2-3x normal baseline
- SSL certificate expiring in 7-30 days
- Memory usage >85% but stable (no swap)
- One of two redundant services down
- Pending security patches older than 7 days

**Escalation:** If the warning has persisted for >7 days without action, escalate to ensure it's tracked.

### Healthy

**Definition:** All metrics within normal operating parameters. No action required.

**Characteristics:**
- All resources well within thresholds
- Performance meets or exceeds expectations
- All redundancy intact
- Security patches current

**Response expectation:** None. Continue normal monitoring.

### Unknown

**Definition:** Insufficient data to classify. The check could not complete, or the data is ambiguous.

**Characteristics:**
- Monitoring check timed out or returned no data
- Metric values are outside expected ranges in ways that suggest bad data, not bad servers
- First check on a new server with no baseline established

**Response expectation:** Investigate the monitoring itself. Fix the data gap before drawing conclusions.

**Examples:**
- Health check endpoint not responding (is the server down or is the check misconfigured?)
- CPU reported as 0% (likely a monitoring bug)
- Disk usage reported as negative (data quality issue)
- No metrics received for a server that was previously reporting

## Classification Rules

### Single-metric classification
Apply thresholds from `metrics-thresholds.md`. The highest severity across all metrics determines the server's overall status.

### Compound signal escalation
Certain combinations of warnings should be escalated to critical. See the "Compound Signals" table in `metrics-thresholds.md`.

### Trend-based escalation
A warning-level metric that has been consistently worsening for 3+ consecutive checks should be noted as "warning, trending critical." Include the projected time to threshold breach.

### Duration-based classification
| Severity | Duration without resolution | Action |
|---|---|---|
| Critical | >1 hour | Escalate |
| Warning | >7 days | Escalate to ensure tracking |
| Unknown | >24 hours | Treat as warning (monitoring is broken) |

### De-escalation
A metric returns to healthy classification when:
- The value has been below the warning threshold for 2+ consecutive checks
- The trend has reversed (no longer climbing toward threshold)
- Manual resolution has been confirmed

Do not de-escalate based on a single good reading after a period of warnings — require sustained recovery.

## Alert Fatigue Prevention

### Grouping rules
- Multiple alerts from the same server within a 5-minute window = one incident notification
- Related alerts (e.g., disk full + database error + API 500) = one incident with root cause analysis
- Repeated identical alerts = one notification with "ongoing since [timestamp]" not repeated alerts

### Suppression rules
- Known maintenance windows: suppress non-critical alerts for the declared duration
- Expected spikes: if the user declares "deploying now" or "running batch job," suppress CPU/memory warnings for 30 minutes
- Flapping metrics: if a metric crosses the threshold and returns within 2 minutes, note it but don't alert at warning level

### Signal-to-noise principles
- Every alert should require a human decision or action
- If an alert consistently gets ignored, the threshold is wrong — adjust it, don't keep alerting
- "I noticed this but it's fine" is not a useful alert. Reserve alerts for things that need action.
- Batch non-urgent findings into scheduled reports instead of individual alerts
