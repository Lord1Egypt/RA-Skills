# Module 01 — System Info

## Commands
```bash
uname -r                           # kernel version
uname -a                           # full kernel info
lsb_release -a 2>/dev/null        # OS info
cat /etc/os-release                # OS info fallback
uptime -p                          # uptime
last reboot | head -5              # reboot history
df -h                              # disk usage
free -h                            # memory
nproc                              # CPU count
cat /proc/cpuinfo | grep "model name" | head -1
timedatectl                        # NTP sync status
```

## Checks & Findings

### OS EOL Check
- Ubuntu 20.04 LTS → EOL April 2025 → if still running: HIGH finding
- Ubuntu 22.04 LTS → EOL April 2027 → OK
- Ubuntu 24.04 LTS → EOL April 2029 → OK
- Debian 11 → EOL June 2026 → OK
- Debian 10 → EOL June 2024 → HIGH if still running

### Kernel Version Check
- Compare against latest stable for the distro
- More than 2 major versions behind → HIGH
- Security patch available → MEDIUM

### NTP Sync
- timedatectl | grep "NTP service: active" → PASS
- NTP not synced → MEDIUM (time drift breaks certs/logs)

### Disk Usage
- < 80% → PASS
- 80-85% → LOW
- 85-95% → WARNING
- > 95% → CRITICAL (auto-alert)

### Last Reboot
- No reboot in > 90 days with kernel updates pending → MEDIUM
- Server rebooted unexpectedly (not matching known maintenance) → HIGH

## Output Format
```
[PASS/FINDING] 01-system: <check> | <result>
```
