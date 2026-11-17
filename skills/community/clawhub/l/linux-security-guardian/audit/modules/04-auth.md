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

### fail2ban Auto-Install & Config
If fail2ban not installed:
```bash
# Check if installable
which apt >/dev/null 2>&1 && echo "apt available"
which yum >/dev/null 2>&1 && echo "yum available"

# Auto-install command (confirm required)
# apt install -y fail2ban  # Debian/Ubuntu
# yum install -y fail2ban   # RHEL/CentOS
```

If fail2ban installed but SSH jail not active:
```bash
# Check SSH jail status
fail2ban-client status sshd 2>/dev/null || echo "sshd jail not configured"

# Check jail.local config
cat /etc/fail2ban/jail.local 2>/dev/null | grep -A10 "\[sshd\]"

# Default SSH jail config to write (confirm required):
# [sshd]
# enabled = true
# port = ssh
# filter = sshd
# logpath = /var/log/auth.log
# maxretry = 5
# bantime = 3600
# findtime = 600
```

### fail2ban Auto-Install Flow
1. Check if fail2ban installed → if not, queue install to confirm
2. Check if SSH jail enabled → if not, queue config to confirm
3. After install + config → restart fail2ban → verify active
4. Log action to actions/auto-done/<client>/<server>/

### Output Format (fail2ban auto-install)
```
[HIGH] 04-auth: fail2ban_not_installed | action: install_queued | action_id: ACT-YYYYMMDD-XXX
[MEDIUM] 04-auth: fail2ban_ssh_jail_disabled | action: config_queued | action_id: ACT-YYYYMMDD-XXX
[PASS] 04-auth: fail2ban_ssh_jail | status: active | banned: 3 IPs
```

### PAM Configuration
- pam_tally2 or pam_faillock not configured → MEDIUM
- No account lockout policy → MEDIUM

### Login from Unknown IPs
- Compare login IPs against SERVER_PROFILE.md management IPs
- Unknown IP logged in successfully → HIGH

### Password Policy Enforcement
Check current password policy:
```bash
# Check PASS_MIN_LEN, PASS_MAX_DAYS, PASS_WARN_AGE
cat /etc/login.defs | grep -E "^PASS_|^#PASS_" | head -10

# Check password quality requirements
cat /etc/pam.d/common-password 2>/dev/null | grep -v "^#" | grep -E "pam_pwquality|pam_cracklib|pam_unix"

# Check if pwquality is installed
dpkg -l libpam-pwquality 2>/dev/null | grep "^ii" || echo "pwquality_not_installed"

# Check user password aging
for u in $(awk -F: '$3>=1000 && $3!=65534 {print $1}' /etc/passwd); do
  echo "$u: $(chage -l $u 2>/dev/null | grep 'Maximum' | cut -d: -f2)"
done
```

### Recommended Password Policy (confirm required)

**/etc/login.defs settings:**
```
PASS_MAX_DAYS   90
PASS_MIN_DAYS   7
PASS_MIN_LEN    12
PASS_WARN_AGE   14
```

**/etc/pam.d/common-password (pwquality):**
```
password requisite pam_pwquality.so retry=3 minlen=12 difok=3 ucredit=-1 lcredit=-1 dcredit=-1 ocredit=-1 enforce_for_root
```

If libpam-pwquality not installed:
```bash
# Auto-install command (confirm required)
# apt install -y libpam-pwquality  # Debian/Ubuntu
# yum install -y pam_pwquality     # RHEL/CentOS
```

### Auto-Install Flow
1. Check if libpam-pwquality installed → if not, queue install (confirm required)
2. Check PASS_MIN_LEN >= 12 → if not, queue login.defs update (confirm required)
3. Check PASS_MAX_DAYS <= 90 → if not, queue login.defs update (confirm required)
4. Check pwquality configured in common-password → if not, queue PAM config (confirm required)
5. After changes → verify with: `chage -l <user> | grep Maximum`
6. Log action to actions/auto-done/<client>/<server>/

### Password Policy Notes
- **Existing users are NOT affected** by login.defs changes — only new users
- **chage** can update existing users: `chage -M 90 <user>`
- **pwquality** affects all password changes (root + users)
- **enforce_for_root** applies quality checks to root too (optional — remove if risky)
- **retry=3** allows 3 attempts before failure
- **minlen=12** = minimum 12 characters
- **difok=3** = at least 3 characters different from old password
- **ucredit/lcredit/dcredit/ocredit=-1** = at least 1 upper/lower/digit/other character

## Output Format
```
[HIGH] 04-auth: brute_force | failed_logins_1hr: 47 | top_source: 1.2.3.4 (23 attempts)
[HIGH] 04-auth: fail2ban_down | status: inactive | action: auto-start queued
[MEDIUM] 04-auth: pwquality_not_installed | action: install_queued | action_id: ACT-YYYYMMDD-XXX
[MEDIUM] 04-auth: password_minlen | current: 6 | recommended: 12 | action: config_queued | action_id: ACT-YYYYMMDD-XXX
[MEDIUM] 04-auth: password_maxdays | current: 99999 | recommended: 90 | action: config_queued | action_id: ACT-YYYYMMDD-XXX
[PASS] 04-auth: password_policy | minlen: 12 | maxdays: 90 | pwquality: yes
```
