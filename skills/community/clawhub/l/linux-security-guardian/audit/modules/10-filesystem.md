# Module 10 — Filesystem Security

## Commands
```bash
# SUID files (run as owner, not user)
find / -perm -4000 -type f 2>/dev/null | sort

# SGID files
find / -perm -2000 -type f 2>/dev/null | sort

# World-writable files (excluding /proc /sys /dev)
find / -xdev -perm -0002 -type f 2>/dev/null | grep -v "/proc\|/sys\|/dev"

# World-writable directories
find / -xdev -perm -0002 -type d 2>/dev/null | grep -v "/proc\|/sys\|/dev\|/tmp\|/var/tmp"

# Sticky bit on /tmp (should be set)
ls -la /tmp | head -2
stat /tmp | grep "Access:"

# No-owner files
find / -xdev \( -nouser -o -nogroup \) 2>/dev/null | grep -v "/proc\|/sys"

# /etc permission check
ls -la /etc/passwd /etc/shadow /etc/sudoers

# Recently modified system files (last 24h)
find /etc /bin /sbin /usr/bin /usr/sbin -newer /tmp -mtime -1 2>/dev/null

# Check /tmp for executables
find /tmp /var/tmp -perm -0111 -type f 2>/dev/null
```

## Checks & Findings

### SUID Binary Check
- Compare against SERVER_PROFILE.md known SUID list
- Unexpected SUID → HIGH (possible privilege escalation vector)
- Common legitimate SUID: sudo, passwd, ping, su, mount

### /tmp Permissions
- /tmp not world-writable+sticky (1777) → MEDIUM → AUTO-FIX (if whitelisted): `chmod 1777 /tmp`

### World-Writable System Dirs
- Any /etc, /usr, /bin, /sbin subdirectory world-writable → HIGH

### No-Owner Files
- Files with no owner (UID/GID not in /etc/passwd) → MEDIUM

### Critical File Permissions
- /etc/shadow not 640 or 000 → HIGH
- /etc/passwd not 644 → MEDIUM
- /etc/sudoers not 440 → HIGH

### Recently Modified System Files
- Any system binary modified in last 24h (without known update) → HIGH

### Executable in /tmp
- Any executable in /tmp or /var/tmp → HIGH (malware staging area)

## Output Format
```
[HIGH] 10-filesystem: unexpected_suid | file: /usr/bin/newexec | not in baseline
[MEDIUM] 10-filesystem: tmp_permissions | /tmp is 1755 | expected: 1777 | action: auto-fix
```
