# Module 21 — Mount Hardening Audit

> **Purpose:** Audit mount points for security options (noexec, nosuid, nodev). These mount flags prevent execution of unauthorized binaries, SUID/SGID escalation, and device file exploitation on writable filesystems.

## Commands
```bash
# Check all mounted filesystems with their options
mount | grep -E "^/" | column -t

# Check /etc/fstab for persistent mount hardening
cat /etc/fstab 2>/dev/null | grep -v "^#" | grep -v "^$"

# Quick check: partitions missing hardening
mount | grep -E "^/" | grep -v "noexec" | grep -v "/boot" | grep -v "/efi"
mount | grep -E "^/" | grep -v "nosuid"
mount | grep -E "^/" | grep -v "nodev" | grep -v "^/dev" | grep -v "^/sys" | grep -v "^/proc"

# Check /tmp specifically (should be noexec,nosuid,nodev)
findmnt /tmp 2>/dev/null || echo "/tmp_not_separate_partition"

# Check /var/tmp (should be noexec,nosuid)
findmnt /var/tmp 2>/dev/null || echo "/var_tmp_not_separate_partition"

# Check /dev/shm (should be noexec,nosuid)
findmnt /dev/shm 2>/dev/null || echo "/dev_shm_default"

# Check /home if separate partition
findmnt /home 2>/dev/null && mount | grep "/home" | grep -o "noexec\|nosuid\|nodev" || echo "/home_not_separate"
```

## Checks & Findings

### Mount Hardening Matrix

| Mount Point | noexec | nosuid | nodev | Severity if Missing |
|------------|--------|--------|-------|---------------------|
| /tmp | CRITICAL | CRITICAL | MEDIUM | Malware staging + SUID exploits |
| /var/tmp | HIGH | HIGH | MEDIUM | Similar risk to /tmp |
| /dev/shm | HIGH | HIGH | — | Shared memory exploits |
| /home | MEDIUM | MEDIUM | — | User-compiled exploits |
| /var | LOW | MEDIUM | — | Log/service writable areas |

### noexec Missing
- /tmp without noexec → **CRITICAL** (malware execution vector, common in CVEs)
- /dev/shm without noexec → **HIGH** (often used in privilege escalation exploits)
- /var/tmp without noexec → **HIGH** (persistent malware staging)
- /home without noexec → **MEDIUM** (user-compiled tools)

### nosuid Missing
- /tmp without nosuid → **CRITICAL** (SUID escalation path)
- /dev/shm without nosuid → **HIGH**
- /var/tmp without nosuid → **HIGH**
- /home without nosuid → **MEDIUM**

### nodev Missing
- /tmp without nodev → **MEDIUM** (device file creation)
- /var without nodev → **LOW**

### Systemd tmp.mount vs /etc/fstab
- If systemd manages /tmp via tmp.mount, check override at /etc/systemd/system/tmp.mount.d/
- If /etc/fstab entry exists, check options column

## Auto-Fix Eligible (Confirm Required)
- Adding mount options to /etc/fstab for writable partitions:
```bash
# Example fstab entry with hardening
# /dev/sdaX  /tmp  ext4  defaults,noexec,nosuid,nodev  0  2
```

- For systemd /tmp:
```bash
mkdir -p /etc/systemd/system/tmp.mount.d/
cat > /etc/systemd/system/tmp.mount.d/security.conf << 'EOF'
[Mount]
Options=mode=1777,strictatime,noexec,nosuid,nodev
EOF
systemctl daemon-reload
```

## Output Format
```
[CRITICAL] 21-mount: tmp_noexec_missing | /tmp lacks noexec | mount: /dev/sda1 on /tmp type ext4 (rw,relatime) | action_id: ACT-YYYYMMDD-XXX
[HIGH] 21-mount: dev_shm_noexec_missing | /dev/shm lacks noexec | action_id: ACT-YYYYMMDD-XXX
[HIGH] 21-mount: tmp_nosuid_missing | /tmp lacks nosuid | action_id: ACT-YYYYMMDD-XXX
[MEDIUM] 21-mount: home_nosuid_missing | /home lacks nosuid | action_id: ACT-YYYYMMDD-XXX
[PASS] 21-mount: all_mounts_hardened | /tmp, /var/tmp, /dev/shm all properly hardened ✓
[INFO] 21-mount: summary | 5 mount points checked | 2 CRITICAL | 1 HIGH | 2 PASS
```
