# Module 12 — Log Analysis

## Commands
```bash
# Auth log analysis
LOGFILE="/var/log/auth.log"
[ -f /var/log/secure ] && LOGFILE="/var/log/secure"  # RHEL

# Failed logins last 24h
grep "Failed password" $LOGFILE | grep "$(date '+%b %e')" | wc -l

# Successful logins last 24h
grep "Accepted" $LOGFILE | grep "$(date '+%b %e')"

# Sudo commands used
grep "sudo:" $LOGFILE | grep "$(date '+%b %e')" | grep "COMMAND"

# SSH disconnections with error
grep "error:" $LOGFILE | grep "$(date '+%b %e')" | tail -20

# Kernel errors
dmesg | grep -iE "error|warn|crit|fail" | tail -20
grep -iE "error|crit|oom" /var/log/kern.log 2>/dev/null | tail -20

# Syslog anomalies
grep -iE "segfault|killed|oom|panic" /var/log/syslog 2>/dev/null | tail -20

# Last 50 lines of auth log
tail -50 $LOGFILE

# Check log rotation health
ls -lh /var/log/auth.log* 2>/dev/null
cat /etc/logrotate.d/rsyslog 2>/dev/null

# Journald disk usage
journalctl --disk-usage 2>/dev/null
```

## Checks & Findings

### Brute Force Detection
- > 20 failed SSH logins in last hour → HIGH
- > 100 in last hour → CRITICAL
- Top offending IPs (if fail2ban not blocking) → HIGH

### Log Tampering
- auth.log missing or zero-size → CRITICAL (possible tampering)
- Gaps in timestamps → HIGH

### OOM Events
- Out-of-memory killer fired → HIGH (system under memory pressure)

### Kernel Panics
- Any kernel panic in dmesg → HIGH

### Successful Root Logins
- Root SSH login detected → HIGH

### Anomalous Sudo
- sudo commands run by unexpected users → HIGH
- sudo to sensitive commands (passwd, visudo, etc.) → MEDIUM

### Log Rotation
- Logs not rotating → MEDIUM (disk fill risk)

## Output Format
```
[HIGH] 12-logs: brute_force | failed_logins_1hr: 89 | top_ip: 45.66.77.88 (67 attempts)
[CRITICAL] 12-logs: auth_log_missing | /var/log/auth.log not found — possible tampering
```
