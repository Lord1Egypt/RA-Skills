# Module 02 — User Accounts

## Commands
```bash
# All users with login shell
grep -v "nologin\|false\|sync\|halt\|shutdown" /etc/passwd | cut -d: -f1,3,6,7

# UID 0 accounts (should only be root)
awk -F: '($3 == 0) { print $1 }' /etc/passwd

# Sudo users
getent group sudo 2>/dev/null || getent group wheel 2>/dev/null
cat /etc/sudoers | grep -v "^#" | grep -v "^$"
ls /etc/sudoers.d/

# Empty passwords (CRITICAL)
awk -F: '($2 == "" || $2 == "!!" ) { print $1 }' /etc/shadow 2>/dev/null

# Password age
awk -F: '{print $1, $5}' /etc/shadow 2>/dev/null | grep "^[^:]*:[0-9]"

# Last login for all users
lastlog | grep -v "Never\|Username"

# Users logged in right now
who
w

# Recently created accounts (last 30 days)
find /home -maxdepth 1 -type d -newer /tmp -mtime -30 2>/dev/null
```

## Checks & Findings

### UID 0 Accounts
- Only 'root' should have UID 0
- Any other UID 0 account → CRITICAL immediate alert

### Unknown Sudo Users
- Compare against SERVER_PROFILE.md expected sudo users
- Unknown sudo user → CRITICAL

### Empty Passwords
- Any account with empty password → CRITICAL
- AUTO-ACTION if whitelisted: `passwd -l <username>`

### Inactive Accounts (> 90 days no login)
- Check lastlog, find accounts with login > 90 days ago
- Still active login shell → MEDIUM
- Queue confirm to lock: `usermod -L <username>`

### Password Policy
- Check /etc/login.defs for PASS_MAX_DAYS, PASS_MIN_DAYS
- PASS_MAX_DAYS > 90 → LOW
- No password expiry → MEDIUM

### Root Account Direct Login
- Check if anyone logged in as root via SSH recently
- grep "Accepted.*root" /var/log/auth.log → HIGH if found

## Output Format
```
[CRITICAL] 02-users: empty_password | account: <name> | action: auto-lock-queued
[PASS] 02-users: uid0_check | only root has uid 0
```
