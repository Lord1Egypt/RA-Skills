# Module 04 — Authentication & Login Audit

## Commands
```bash
# Failed login attempts
grep "Failed password" /var/log/auth.log | tail -100
grep "Failed password" /var/log/auth.log | awk '{print $11}' | sort | uniq -c | sort -rn | head -20  # top source IPs

# Successful logins
grep "Accepted" /var/log/auth.log | tail -50

# Sudo usage
grep "sudo:" /var/log/auth.log | tail -50

# Failed sudo
grep "sudo:.*NOT in sudoers" /var/log/auth.log

# Login from unexpected locations
last | head -30

# Brute force threshold check
FAILED=$(grep "Failed password" /var/log/auth.log | grep "$(date '+%b %e')" | wc -l)
echo "Failed logins today: $FAILED"

# PAM configuration
cat /etc/pam.d/sshd | grep -v "^#"
cat /etc/pam.d/login | grep -v "^#"

# fail2ban status
systemctl is-active fail2ban 2>/dev/null
fail2ban-client status sshd 2>/dev/null
```

## Checks & Findings

### Failed Login Spike
- > 20 failed logins in last hour → HIGH alert
- > 100 failed logins in last hour → CRITICAL alert
- Single IP with > 10 failures → HIGH (may not be in fail2ban)

### Successful Root SSH Login
- Any "Accepted.*root" in auth.log → HIGH (if PermitRootLogin is yes)

### Unauthorized Sudo Usage
- "NOT in sudoers" entries → HIGH

### fail2ban Status
- Not running → HIGH → AUTO-START (if whitelisted)
- Not configured for SSH → MEDIUM

### PAM Configuration
- pam_tally2 or pam_faillock not configured → MEDIUM
- No account lockout policy → MEDIUM

### Login from Unknown IPs
- Compare login IPs against SERVER_PROFILE.md management IPs
- Unknown IP logged in successfully → HIGH

## Output Format
```
[HIGH] 04-auth: brute_force | failed_logins_1hr: 47 | top_source: 1.2.3.4 (23 attempts)
[HIGH] 04-auth: fail2ban_down | status: inactive | action: auto-start queued
```
