# Module 13 — Cron Job Audit

## Commands
```bash
# System crontabs
cat /etc/crontab 2>/dev/null
ls -la /etc/cron.d/ 2>/dev/null
cat /etc/cron.d/* 2>/dev/null
ls /etc/cron.hourly/ /etc/cron.daily/ /etc/cron.weekly/ /etc/cron.monthly/ 2>/dev/null

# User crontabs
for user in $(cut -d: -f1 /etc/passwd); do
  crontab -l -u $user 2>/dev/null && echo "=== $user ==="
done

# Systemd timers (modern cron equivalent)
systemctl list-timers --all --no-pager 2>/dev/null

# At jobs
atq 2>/dev/null
```

## Checks & Findings

### Unknown Cron Jobs
- Compare against BASELINE.md expected crons
- Any new cron entry not in baseline → HIGH (persistence mechanism used by malware)

### Cron Scripts Writable by Non-Root
- find /etc/cron* -writable -not -user root 2>/dev/null
- Any world-writable cron script → CRITICAL

### Cron Running as Root
- Review root's crontab for potentially dangerous commands
- wget/curl piped to bash in cron → CRITICAL

### Unexpected At Jobs
- Any at job not set by owner → HIGH

## Output Format
```
[HIGH] 13-crons: new_cron_job | user: www-data | job: "*/5 * * * * /tmp/update.sh" | not in baseline
[CRITICAL] 13-crons: writable_cron_script | file: /etc/cron.daily/backup.sh | perms: 0777
```
