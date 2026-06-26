# Module 05 — Services Audit

## Commands
```bash
# All running services
systemctl list-units --type=service --state=running --no-pager

# Failed services
systemctl list-units --type=service --state=failed --no-pager

# Services enabled at boot
systemctl list-unit-files --type=service --state=enabled --no-pager

# Listening processes
ss -tulpn
# or: netstat -tulpn

# Processes listening on all interfaces (0.0.0.0 or :::)
ss -tulpn | grep -E "0\.0\.0\.0|:::"

# Check for suspicious processes
ps aux --sort=-%cpu | head -20
ps aux | awk '{if ($3 > 50.0) print $0}'  # high CPU

# Docker if running
docker ps 2>/dev/null
docker ps -a 2>/dev/null
```

## Checks & Findings

### Unknown Running Services
- Compare against SERVER_PROFILE.md expected services
- Any unlisted service running → MEDIUM (queue confirm to investigate/stop)

### Failed Services
- Any failed service → HIGH (could indicate attack or config issue)
- Check if service was recently working: journalctl -u <service> --since "1 hour ago"

### Services Listening on All Interfaces
- Services bound to 0.0.0.0 that should be internal only → HIGH
- Cross-check with expected open ports in SERVER_PROFILE.md

### Unnecessary Services Running
Common unnecessary services to flag:
- telnet → CRITICAL (plaintext)
- rsh, rlogin, rexec → CRITICAL
- finger → MEDIUM
- rpcbind (if not NFS server) → LOW
- avahi-daemon (if not needed) → LOW
- cups (if not print server) → LOW

### Auditd Status
- Not running → HIGH → AUTO-START (if whitelisted)
- systemctl enable auditd + systemctl start auditd

## Output Format
```
[CRITICAL] 05-services: telnet_running | service: telnet | action: confirm-to-stop ACT-XXX
[HIGH] 05-services: auditd_down | action: auto-starting
[PASS] 05-services: expected_services | all 5 expected services running
```
